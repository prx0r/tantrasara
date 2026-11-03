#!/usr/bin/env python3
"""Generic opening/section clip: bell + groups + MMS karaoke + verse hold.
Usage: python3 build_clip.py <storyboard.json> <b1,b2,...> <out.mp4>
Hold: first verse block's card for the whole clip (verse-first standard).
Karaoke: MMS forced alignment per group (sa-IN verse, en-IN narration).
"""
import json, os, re, subprocess, sys, glob, hashlib, shutil

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
VOL = os.path.expanduser('~/vol/tantrasara/renders')
BELL = '/home/ubuntu/vatulanatha/sfx/bell_ding.wav'
NODE_MOD = '/tmp/mmsmod/node_modules'
ALIGN = os.path.expanduser('~/tantrasara/align_group.js')

from PIL import Image, ImageDraw, ImageFont
def F(p, s): return ImageFont.truetype(p, s)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]
def group_wav(ch, sec, voice, text):
    h = hashlib.sha1(f'{voice}|{text}'.encode()).hexdigest()[:12]
    found = glob.glob(f'{VOL}/{ch}/groups/{slug(sec)}/*_{voice}_{h}.wav')
    return found[0] if found else None
def to_deva(s):
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return ' '.join(transliterate(w, IAST, DEVANAGARI) if not re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())
def to_iast(s):
    from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST
    return ' '.join(transliterate(w, DEVANAGARI, IAST) if re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())

def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    bids = sys.argv[2].split(',')
    out = sys.argv[3]
    byid = {b['id']: b for b in sb['blocks']}
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    blocks = [byid[i] for i in bids]
    groups = []
    for b in blocks:
        if b['voice'] == 'none':
            continue
        if groups and groups[-1][0]['voice'] == b['voice'] and groups[-1][0]['section'] == b['section']:
            groups[-1].append(b)
        else:
            groups.append([b])
    wavs = []
    for g in groups:
        text = ' '.join(x.get('directed', x['text']) for x in g)
        f = group_wav(ch, g[0]['section'], g[0]['voice'], text)
        assert f, f"missing render for {g[0]['id']}..{g[-1]['id']}"
        wavs.append((f, g))
    # MMS align each group
    os.makedirs('/tmp/mmsclip', exist_ok=True)
    al = []
    for i, (f, g) in enumerate(wavs):
        disp = []
        for b in g:
            disp += [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
        lang = 'sa-IN' if g[0]['voice'] == 'verse' else 'en-IN'
        wpath = f'/tmp/mmsclip/cw{i}.json'
        opath = f'/tmp/mmsclip/ct{i}.json'
        # sa-IN wants Devanagari (its romanizer rejects IAST diacritics);
        # display/subtitle mapping stays 1:1 either way
        from indic_transliteration.sanscript import transliterate as _tr, IAST as _IA, DEVANAGARI as _DV
        ali = [(_tr(w, _IA, _DV) if not re.search(r'[\u0900-\u097F]', w) else w) for w in disp] if lang == 'sa-IN' else disp
        json.dump(ali, open(wpath, 'w'), ensure_ascii=False)
        r = subprocess.run(['node', ALIGN, f, wpath, opath, lang],
                           capture_output=True, text=True, env={**os.environ, 'NODE_PATH': NODE_MOD})
        assert os.path.exists(opath), f'MMS failed group {i}: {r.stderr[-300:]}'
        rows = json.load(open(opath, encoding='utf-8'))
        assert len(rows) == len(disp), f'{g[0]["id"]}: {len(disp)} vs {len(rows)}'
        mean = sum(x['mms'] for x in rows) / len(rows)
        print(f'group {i}: n={len(rows)} mean={mean:.3f}', flush=True)
        al.append((g, rows))
    # assembly: bell(+6dB) + groups with rhythm beds by boundary —
    # 0.8 after titles / long-pause beats / dialogue / section ends,
    # 0.6 after verse, 0.3 in flow. Deterministic, no model-mood gaps.
    def bed_after(g, nxt):
        txt = ' '.join(x.get('directed', x['text']) for x in g)
        if g[0]['type'] == 'title' or (nxt and nxt[0]['section'] != g[0]['section']):
            return 0.8
        if any(x['type'] == 'dialogue' for x in g):
            return 0.8
        if g[0]['voice'] == 'verse':
            return 0.6
        if '[long pause]' in txt:
            return 0.8
        return 0.3
    beds = []
    final_inputs = ['-i', BELL]
    for i, (f, g) in enumerate(wavs):
        final_inputs += ['-i', f]
        if i < len(wavs) - 1:
            bd = bed_after(g, wavs[i + 1][1])
            beds.append(bd)
            final_inputs += ['-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono:d={bd}']
    nAud = 1 + len(wavs) + max(0, len(wavs) - 1)
    mix = '/tmp/clip_mix.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + final_inputs +
                   ['-filter_complex',
                    '[0:a]volume=6dB[z0];[z0]' + ''.join(f'[{j}]' for j in range(1, nAud)) +
                    f'concat=n={nAud}:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', mix], check=True)
    # flat word timeline with absolute onsets (beds included via group durations)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                  '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.strip())
            for (f, g) in wavs]
    flat = []
    off = 0.99
    for gi, ((f, g), rows) in enumerate(zip(wavs, [r for _, r in al])):
        wi = 0
        for b in g:
            sw = [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
            seg = rows[wi:wi + len(sw)]
            assert len(seg) == len(sw), f"{b['id']}: {len(sw)} vs {len(seg)}"
            # subtitle display: IAST for verse blocks (Devanagari has no
            # glyphs in the subtitle face — bare boxes otherwise)
            sub = [to_iast(w) if b['type'] == 'verse' else w for w in sw]
            for j, r in enumerate(seg):
                flat.append((b, j, r['t_on'] + off, sw, sub, r['t_off'] + off))
            wi += len(sw)
        off += durs[gi] + (beds[gi] if gi < len(beds) else 0)
    # glossary: confirmed terms only (proposed terms play over white).
    # entries carry citation Deva + T1 literal + final gloss; video shows
    # the literal only once its own literal_status is confirmed.
    import glob as _gg
    _gm = re.search(r'ch(\d+)', sys.argv[1])
    _gl = {}
    if _gm:
        _gp = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'glossary_ch{_gm.group(1)}.json')
        if os.path.exists(_gp):
            _raw = json.load(open(_gp, encoding='utf-8'))
            for k, v in _raw.items():
                if not (isinstance(v, dict) and v.get('status') == 'confirmed' and v.get('gloss')):
                    continue
                _gl[k] = {'deva': v.get('deva', ''), 'gloss': v.get('gloss', ''),
                          'literal': v.get('literal', '') if v.get('literal_status') == 'confirmed' else ''}
    print(f'confirmed glossary terms: {len(_gl)}', flush=True)
    # holds: verse cards while chanting, clean white once speech starts.
    # (owner: no title cards shown; Sanskrit clears when granny takes over)
    import sys as _sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import holds as _H
    _holds = _H.build_holds([b for b in blocks if b['type'] != 'title' or True])
    hold_for = {}
    _blank = Image.new('RGB', (W, H), LIGHT)
    for h in _holds:
        img = _H.render_hold(h, None, _gl)
        for b in h:
            hold_for[b['id']] = img
    # title blocks never shown: map them (and opener) appropriately
    fdir = '/tmp/clip_frames'
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    entries, idx = [], 0
    # opener: thumbnail if it exists, else first verse hold (verse up fast)
    # thumbnails live in assets/thumbnail/chNN.png (ch01 rainbow emblem law)
    import re as _re2
    _first_verse = next(b for b in blocks if b['type'] == 'verse')
    _m = _re2.search(r'ch(\d+)', sys.argv[1])
    _ch = _m.group(1) if _m else '01'
    _THUMB = os.path.expanduser(f'~/tantrasara/assets/thumbnail/ch{_ch}.png')
    if not os.path.exists(_THUMB):
        _THUMB = os.path.expanduser('~/tantrasara/assets/thumb_ch1.png')  # legacy fallback
    if os.path.exists(_THUMB):
        _tb = Image.open(_THUMB).convert('RGB')
        _tb.thumbnail((1400, 730), Image.LANCZOS)
        _HOLD0 = Image.new('RGB', (W, H), LIGHT)
        _HOLD0.paste(_tb, ((W - _tb.width) // 2, 50))
    else:
        _HOLD0 = hold_for.get(_first_verse['id'], _blank)
    _HOLD0.save(f'{fdir}/00000.png')
    entries.append((0, max(0.05, flat[0][2] if flat else off), 'thumbnail'))
    idx = 1
    _first_verse_hold = hold_for.get(_first_verse['id'], _blank)
    _first_verse_fi = next(i for i, (b, *_r) in enumerate(flat) if b['type'] == 'verse')
    # term cues: (start, end, image) from confirmed glossary mentions
    import unicodedata as _ud
    _fold = lambda s: ''.join(c for c in _ud.normalize('NFD', s.lower()) if _ud.category(c) != 'Mn')
    _cue_starts = {}
    for (b, k, t_on, sw, sub, t_off) in flat:
        if b['type'] not in ('narration', 'dialogue'):
            continue
        for j, w in enumerate(sw):
            key = _fold(w.strip('.,!?;:\'"—-'))
            if key in _gl and (b['id'], j) not in _cue_starts:
                _cue_starts[(b['id'], j)] = key
                break
    _events = []
    for (b, k, t_on, sw, sub, t_off) in flat:
        if b['type'] in ('verse', 'title', 'figure', 'dialogue') or b.get('directed', '').startswith('[long pause]'):
            _events.append(t_on)
    _events = sorted(set(_events))
    def _next_event(t):
        for e in _events:
            if e > t + 0.05:
                return e
        return off
    _term_imgs = {}
    def _stack_img(keys):
        # list engine: count decides the shape, one standard Deva size
        return _H.render_list(keys, {k: _gl[k] for k in keys})
    def _single_img(key):
        # single centered four-layer term card from the glossary entry
        e = _gl[key]
        return _H.render_term_card(e.get('deva') or key, _H.to_iast(e.get('deva') or key),
                                  e.get('literal', ''), e.get('gloss', ''))
    def _is_single_glossed_verse(b):
        return (b['type'] == 'verse' and len(b['text'].split()) <= 3
                and _fold(b['text'].strip('.,!?;:\'"—-')) in _gl)
    for key in set(_cue_starts.values()):
        _term_imgs[key] = _single_img(key)
    _cues = []
    for (bid, j), key in _cue_starts.items():
        t0 = next(t for (b, k, t, sw, sub, e) in flat if b['id'] == bid and k == j)
        _cues.append((t0, _next_event(t0), key))
    _cues.sort()
    # a newer cue always supersedes: clamp each span at the next cue start
    _cues = [(s, min(e, _cues[i + 1][0]) if i + 1 < len(_cues) else e, k)
             for i, (s, e, k) in enumerate(_cues)]
    # list runs: 2+ cues with no event gap between them (each span ends
    # exactly where the next begins) accumulate into one count-shaped card
    # (2 side by side, 3 row-or-triangle, 4 corners, 5 corners + middle).
    _run_of, _run_keys = {}, {}
    _i = 0
    while _i < len(_cues):
        _j = _i
        while _j + 1 < len(_cues) and _cues[_j][1] == _cues[_j + 1][0]:
            _j += 1
        if _j - _i + 1 >= 2:
            _keys = [_cues[_n][2] for _n in range(_i, _j + 1)]
            for _n in range(_i, _j + 1):
                _run_of[_n] = (_i, _n - _i)
                _run_keys[_i] = _keys
        _i = _j + 1
    for _ri, _keys in _run_keys.items():
        for _p in range(1, len(_keys) + 1):
            _term_imgs[('stack', _ri, _p)] = _stack_img(_keys[:_p])
    # persist: a single-word glossed chant stays up with its gloss through
    # the directly following block (e.g. "Aṇu." -> "That's you."), then
    # white. Cues always win over persist. Multi-line chant runs clear.
    _persists = []
    for _fi, (b, _k, _ton, _sw, _sub, _toff) in enumerate(flat):
        if b['type'] == 'verse' and _is_single_glossed_verse(b):
            _nxt = next((_gj for _gj in range(_fi + 1, len(flat))
                         if flat[_gj][0]['id'] != b['id']), None)
            if _nxt is not None and flat[_nxt][0]['type'] != 'verse':
                _end = next((_gk for _gk in range(_nxt + 1, len(flat))
                             if flat[_gk][0]['id'] != flat[_nxt][0]['id']),
                            len(flat))
                _term_imgs[('persist', b['id'])] = hold_for.get(b['id'], _blank)
                _persists.append((_ton, flat[_end - 1][5], b['id']))
    print(f'term cues: {[(k, round(s)) for s, e, k in _cues]}', flush=True)
    print(f'list runs: {[(_keys) for _keys in _run_keys.values()]}', flush=True)
    print(f'persists: {[(bid, round(s)) for s, e, bid in _persists]}', flush=True)
    def hold_img(b, fi):
        t = flat[fi][2]
        if fi < _first_verse_fi:
            return _HOLD0  # thumbnail holds from frame 0 until chanting starts
        if b['type'] == 'verse':
            return hold_for.get(b['id'], _blank)
        for _n, (s, e, key) in enumerate(_cues):
            if s <= t < e:
                if _n in _run_of:
                    _ri, _p = _run_of[_n]
                    return _term_imgs[('stack', _ri, _p + 1)]
                return _term_imgs[key]
        for (s, e, bid) in _persists:
            if s <= t < e:
                return _term_imgs[('persist', bid)]
        return _blank
    def hold_kind(b, fi):
        t = flat[fi][2]
        if fi < _first_verse_fi:
            return 'thumbnail'
        if b['type'] == 'verse':
            return 'verse'
        for _n, (s, e, key) in enumerate(_cues):
            if s <= t < e:
                if _n in _run_of:
                    return 'stack:' + key
                return 'term:' + key
        for (s, e, bid) in _persists:
            if s <= t < e:
                return 'verse-hold:' + bid
        return 'white'
    for fi, (b, k, t_on, sw, sub, t_off) in enumerate(flat):
        im = hold_img(b, fi).copy()
        d = ImageDraw.Draw(im)
        # subtitle karaoke, wrapped <=2 lines
        fnt = F(FE, 46)
        lines, cur = [], ''
        for w_ in sub:
            t_ = (cur + ' ' + w_).strip()
            if d.textlength(t_, font=fnt) > 1750 and cur:
                lines.append(cur); cur = w_
            else:
                cur = t_
        if cur:
            lines.append(cur)
        if len(lines) > 2:
            fnt = F(FE, 40)
            lines, cur = [], ''
            for w_ in sub:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        assert len(lines) <= 2, 'subtitle too long'
        counts, acc = [], 0
        for ln in lines:
            counts.append(acc); acc += len(ln.split())
        li = next((i for i in range(len(lines)) if k < counts[i] + len(lines[i].split())), len(lines) - 1)
        rel = k - counts[li]
        for j, ln in enumerate(lines):
            wl = ln.split()
            if j < li:
                lit, rest = ln, ''
            elif j > li:
                lit, rest = '', ln
            else:
                lit = ' '.join(wl[:rel + 1]) + (' ' if rel + 1 < len(wl) else '')
                rest = ' '.join(wl[rel + 1:])
            yy = SUB_Y + j * 62
            if lit:
                d.text(((W - d.textlength(ln, font=fnt)) / 2, yy), lit, font=fnt, fill=INK)
            d.text(((W - d.textlength(ln, font=fnt)) / 2 + d.textlength(lit, font=fnt), yy),
                   rest, font=fnt, fill=FADE)
        im.save(f'{fdir}/{idx:05d}.png')
        nxt = flat[fi + 1][2] if fi + 1 < len(flat) else off
        entries.append((idx, max(0.03, nxt - t_on), hold_kind(b, fi)))
        idx += 1
    # coverage: seconds per hold kind (white = clean default, not content).
    # opener frame has no kind yet — classify it as thumbnail.
    from collections import defaultdict as _dd
    _cov = _dd(float)
    for (_i, du, hk) in entries:
        _cov[hk if hk else 'thumbnail'] += du
    _tot = sum(_cov.values()) or 1
    print('COVERAGE ' + ' '.join(f'{k}={v:.0f}s' for k, v in sorted(_cov.items())) +
          f' white_pct={100 * _cov.get("white", 0) / _tot:.0f}%', flush=True)
    if _tot > 60 and _cov.get('white', 0) / _tot > 0.85:
        raise SystemExit('COVERAGE FAIL: >85% white on a >60s clip — missing cards?')
    # concat list (duration,idx pairs; kind is metadata only)
    lines = []
    for i, du, _hk in entries:
        lines += [f"file '{fdir}/{i:05d}.png'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir}/{entries[-1][0]:05d}.png'")
    open(f'{fdir}/concat.txt', 'w').write('\n'.join(lines) + '\n')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{fdir}/concat.txt', '-i', mix,
                    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', sys.argv[3]], check=True)
    print('OK:', sys.argv[3], f'{idx} cuts')
    # golden input: machine-readable render fingerprint (see golden.py)
    import json as _json
    _dur = float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=nw=1:nk=1', sys.argv[3]],
        capture_output=True, text=True, check=True).stdout.strip())
    _json.dump({'cuts': idx, 'duration': round(_dur, 2),
                'white_pct': round(100 * _cov.get('white', 0) / _tot),
                'coverage': {k: round(v) for k, v in sorted(_cov.items())},
                'cues': [{'t': round(s, 2), 'key': k} for s, e, k in _cues]},
               open(os.path.splitext(sys.argv[3])[0] + '.render_meta.json', 'w'))


if __name__ == '__main__':
    import sys
    main()
