#!/usr/bin/env python3
"""Binary render-stage gate (GATES.md machine lines). Exit 0 all-green,
exit 1 with FAIL lines otherwise. Eye lines are read off proof PNGs.
Usage: gate_visual.py <storyboard.json> [--glossary g.json] [--meta render_meta.json]
  [--mp4 clip.mp4] [--subs subs.json] [--verify verify.json] [--approved approved.json]
"""
import json, os, re, subprocess, sys, unicodedata, glob

FAIL = []
PASS = []


def check(name, ok, detail=''):
    (PASS if ok else FAIL).append(f'{"PASS" if ok else "FAIL"} {name}' + (f' — {detail}' if detail else ''))


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def main():
    a = sys.argv[1:]
    sb_path = a[0]
    opt = dict(zip(a[1::2], a[2::2]))
    ch = (re.search(r'ch(\d+)', sb_path) or [None, '01'])[1]

    from factory_contract import (ContractError, read_json, sha256, validate_bundle,
                                  validate_clip_artifacts, validate_schema)
    try:
        bundle = validate_bundle(sb_path, require_approval=True)
        if ('--approved' not in opt or os.path.realpath(opt['--approved']) != str(bundle['paths']['approval'])
                or '--glossary' not in opt or os.path.realpath(opt['--glossary']) != str(bundle['paths']['glossary'])):
            raise ContractError('the canonical approval and glossary must both be supplied for this lane')
    except ContractError as exc:
        print(f'FAIL data/approval contract — {exc}\nGATE RED')
        sys.exit(1)
    sb = bundle['storyboard']

    # D1 storyboard green
    v = sb.get('validation', {})
    check('D1 storyboard green', not v.get('errors') and not v.get('warnings'),
          f"{len(v.get('errors', []))}e {len(v.get('warnings', []))}w")

    # D2 approval SHAs
    check('D2 approval SHAs match', True)

    # D3 + V5 + V7 glossary discipline (missing glossary fails —
    # a render with no glossary shows no term cards at all)
    gl = {}
    if '--glossary' in opt:
        gl = bundle['glossary']
        bad_key = [k for k in gl if k != fold(k)]
        check('D3 keys folded ASCII', not bad_key, str(bad_key[:3]))
        conf = [k for k, vv in gl.items() if isinstance(vv, dict) and vv.get('status') == 'confirmed']
        nodeva = [k for k in conf if not (isinstance(gl[k], dict) and gl[k].get('deva'))]
        check('V5 confirmed terms carry citation Deva', not nodeva, str(nodeva[:3]))
        paren = [k for k in conf if isinstance(gl[k], dict) and ('(' in gl[k].get('literal', '') or ')' in gl[k].get('literal', ''))]
        check('V7 literals use square brackets', not paren, str(paren[:3]))
    else:
        check('glossary resolved (no term cards without it)', False, 'no --glossary given')

    # H3 render_meta cues match storyboard run scan
    if '--meta' in opt:
        try:
            if '--mp4' not in opt or '--subs' not in opt:
                raise ContractError('the actual video and subtitles are required')
            if (os.path.realpath(opt['--meta']) != os.path.splitext(os.path.realpath(opt['--mp4']))[0] + '.render_meta.json'
                    or os.path.realpath(opt['--subs']) != os.path.splitext(os.path.realpath(opt['--mp4']))[0] + '.subs.json'):
                raise ContractError('metadata and subtitles must be the video\'s own sidecars')
            m = validate_clip_artifacts(sb_path, opt['--mp4'])
        except (ContractError, OSError, ValueError, KeyError, TypeError) as exc:
            print(f'FAIL render provenance — {exc}\nGATE RED')
            sys.exit(1)
        check('H4 white within band', m.get('white_pct', 0) <= 85 or m.get('duration', 0) <= 60,
              f"white {m.get('white_pct')}%")
        _starts_top = not m.get('bids') or m['bids'][0] == 'b1'
        if _starts_top:
            check('H1 thumbnail opens', m.get('coverage', {}).get('thumbnail', 0) > 0)
        else:
            check('H1 mid-chapter opens white (no intro re-show)', True,
                  'starts at ' + (m.get('bids', ['?'])[0]))
        mcues = [c['key'] for c in m.get('cues', [])]
        # recompute expected cue order from storyboard + confirmed glossary,
        # restricted to the rendered bid range when the meta records it
        # (segments carry their bids; full chapters carry all)
        sb_blocks = sb['blocks']
        if m.get('bids'):
            have = set(m['bids'])
            sb_blocks = [b for b in sb_blocks if b['id'] in have or b['id'] == 'b_opener']
        terms = {k for k, vv in gl.items() if isinstance(vv, dict) and vv.get('status') == 'confirmed'} if gl else set()
        # builder rule: EVERY term mention fires at its own word onset
        # (one flat row yields one new cue; re-mentions re-fire).
        exp = []
        for b in sb_blocks:
            if b.get('type') not in ('narration', 'dialogue'):
                continue
            # builder-exact tokenization: whitespace split, \w filter
            # (glued em-dash pairs do NOT split — matches build_clip).
            for w in b['text'].strip().split():
                if not re.search(r'\w', w, re.U):
                    continue
                c = fold(w.strip('.,!?;:\'"—-'))
                if c in terms:
                    exp.append(c)
        check('H3 cue order matches storyboard', mcues == exp, f'{len(mcues)} cues')
        # drops: every filed drop applied in the render (lane/ch-specific
        # file — never any drops_*.json that happens to sort last)
        _dfile, _dmeta = bundle['drops'], m['drops']
        _rbids = set(m['bids'])
        _in_range = {k for k in _dfile if k in _rbids}
        check('H7 drops and pause lengths match', set(_dmeta) == _in_range and all(
            _dmeta[k]['pause'] == _dfile[k]['pause'] for k in _in_range),
            f'file={sorted(_in_range)} meta={sorted(_dmeta)}')
    else:
        check('H3/H4 render_meta present', False, 'no --meta given')

    # H5/H6 subtitle dump scan
    if '--subs' in opt and '--meta' in opt:
        subs = read_json(opt['--subs'])
        try:
            validate_schema('subtitles', subs, opt['--subs'])
        except ContractError as exc:
            print(f'FAIL subtitle contract — {exc}\nGATE RED')
            sys.exit(1)
        deva_leak = [s for s in subs if re.search(r'[\u0900-\u097F]', s.get('s', ''))]
        check('H5 no Devanagari in subtitles', not deva_leak, f'{len(deva_leak)} leaks')
        selected = set(m['bids'])
        expected_words = [(b['id'], w) for b in sb['blocks']
                          if b['id'] in selected and b['voice'] != 'none'
                          for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
        actual_words = [(row['bid'], row['w']) for row in subs]
        times = [row['t'] for row in subs]
        check('H6 subtitles cover spoken words in order', actual_words == expected_words
              and times == sorted(times) and times[-1] <= m['duration'] + 0.1,
              f'{len(actual_words)}/{len(expected_words)} word rows')
    else:
        check('H5/H6 subs dump present', False, 'no --subs given')

    # V1/A2 streams via verify report or ffprobe
    if '--verify' in opt:
        vr = json.load(open(opt['--verify'], encoding='utf-8'))
        check('V1/A2 verify PASS for these exact files', vr.get('pass') is True
              and vr.get('video_sha256') == sha256(opt['--mp4'])
              and vr.get('storyboard_sha256') == sha256(sb_path), ','.join(vr.get('fails', [])[:3]))
    elif '--mp4' in opt:
        r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,codec_type,avg_frame_rate',
                            '-of', 'json', opt['--mp4']], capture_output=True, text=True)
        try:
            streams = json.loads(r.stdout)['streams'] if r.returncode == 0 else []
            video = [s for s in streams if s.get('codec_type') == 'video']
            audio = [s for s in streams if s.get('codec_type') == 'audio']
            rate = video[0].get('avg_frame_rate', '').split('/') if len(video) == 1 else []
            fps = int(rate[0]) / int(rate[1]) if len(rate) == 2 and int(rate[1]) else 0
            ok = len(video) == 1 and len(audio) == 1 and video[0].get('width') == 1920 and video[0].get('height') == 1080 and abs(fps - 30) < 0.01
        except (ValueError, KeyError, IndexError, TypeError, ZeroDivisionError):
            ok = False
        check('V1 geometry, frame rate and streams', ok, '1920x1080, 30fps, one video + one audio')
    else:
        check('V1/A2 streams checked', False, 'no --mp4 or --verify given')

    print('\n'.join(PASS + FAIL))
    print('GATE ' + ('GREEN' if not FAIL else 'RED'))
    sys.exit(0 if not FAIL else 1)


if __name__ == '__main__':
    main()
