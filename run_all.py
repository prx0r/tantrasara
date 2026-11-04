#!/usr/bin/env python3
"""Batch driver: every chapter through storyboard->render->MMS->assemble->video.
Usage: python3 run_all.py [--chapters 01,02] [--from STAGE] [--dry-run]
Stages: preflight board cast-check publish render mms assemble holds video verify golden-check review-pack cleanup.
publish = review pack to R2 for owner sign-off (render REFUSES without
approved_chNN.json whose SHAs match current files). golden-check compares
each render against the owner-blessed golden before review-pack.
Idempotent everywhere (content hashes); resume by re-running. One chapter
failing never blocks the others. Overnight-safe under nohup.
Owner gates (NOT automated): casting marks, glossary confirms, final ears.
"""
import json, os, subprocess, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
VOL = os.path.expanduser('~/vol/tantrasara/renders')
VOL_FREE_MIN_GB = 4.0
LOCAL_FREE_MIN_GB = 1.0

def storage_preflight():
    import shutil as _sh
    local_free = _sh.disk_usage('/tmp').free / 1e9
    r = subprocess.run(['ssh', '-i', os.path.expanduser('~/.ssh/id_ed25519'),
                        '-o', 'BatchMode=yes', 'root@2.28.50.109',
                        'df -BG /mnt/HC_Volume_106427611 | tail -1'],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError('cannot verify volume free space: ' + (r.stderr.strip() or f'ssh exited {r.returncode}'))
    try:
        vol_free = float(r.stdout.split()[3].rstrip('G'))
    except (IndexError, ValueError) as exc:
        raise RuntimeError('cannot parse volume free space from df') from exc
    if not __import__('math').isfinite(vol_free):
        raise RuntimeError('volume free space is not a finite number')
    print(f'storage: local {local_free:.1f}G free, volume {vol_free:.0f}G free', flush=True)
    if local_free < LOCAL_FREE_MIN_GB:
        raise RuntimeError(f'local disk critical ({local_free:.1f}G)')
    if vol_free < VOL_FREE_MIN_GB:
        raise RuntimeError(f'volume critical ({vol_free:.0f}G)')


def free_tier_preflight():
    # free Fish only, always: the shared renderer must pin the -free model.
    # A paid model string anywhere stops the line cold (owner call to waive).
    from factory_contract import require_free_tier
    model = require_free_tier()
    print(f'fish model: {model}', flush=True)

def stage_cleanup():
    from factory_contract import video_build_lock
    # The video worker owns these paths. Hold its lock while cleaning them;
    # do not glob-delete unrelated pilots or first-minute work.
    with video_build_lock():
        for p in ['/tmp/clip_frames', '/tmp/fm2_frames', '/tmp/ts_holds', '/tmp/mmsclip']:
            shutil.rmtree(p, ignore_errors=True)
        for p in ['/tmp/mms_grp.f32', '/tmp/mms_eng_test.f32']:
            if os.path.isfile(p):
                os.unlink(p)
    print('cleanup: transient frames/tmp audio removed (R2 holds the shipped copies)', flush=True)
    return True
CHAPTERS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
            '14', '15', '16', '17', '18', '19', '20', '21', '22']
STAGES = ['preflight', 'free-tier', 'board', 'cast-check', 'publish', 'render', 'mms', 'assemble', 'holds', 'video', 'verify', 'voices', 'qwen', 'golden-check', 'review-pack', 'cleanup']

def sh(cmd, **kw):
    print('+', ' '.join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    tail = (r.stderr or r.stdout or '').strip().splitlines()[-3:]
    for l in tail:
        print('  |', l[:160], flush=True)
    return r.returncode == 0

def stage_board(ch):
    # The saved storyboard is the approved input. Rebuilding it in place
    # here changes its bytes (and can erase a blessing) before any gate runs.
    from factory_contract import validate_bundle, verify_storyboard_source
    validate_bundle(sb_path(ch))
    verify_storyboard_source(sb_path(ch))
    print(f'  | ch{ch}: source/overrides match frozen storyboard; no rewrite', flush=True)
    return True

def stage_cast_check(ch):
    from factory_contract import validate_bundle
    validate_bundle(sb_path(ch))
    print(f'  | ch{ch}: storyboard, glossary and drops validated', flush=True)
    return True

def stage_publish(ch):
    return sh(['python3', f'{BASE}/publish_review.py', ch])

def stage_render(ch):
    from factory_contract import validate_bundle
    a = validate_bundle(sb_path(ch), require_approval=True)['approval']
    print(f'ch{ch}: approval {a["date"]} verified, rendering', flush=True)
    return sh(['python3', f'{BASE}/render_chapter.py', sb_path(ch)])

def stage_mms(ch):
    # per-group MMS via build_clip's align path is per-clip; full-chapter
    # MMS runs inside build_video (group wavs already on volume).
    print('  | ch%s: MMS runs inside video build (no separate step)' % ch, flush=True)
    return True

def stage_assemble(ch):
    os.makedirs(f'{VOL}/finals', exist_ok=True)
    return sh(['python3', f'{BASE}/assemble_chapter.py', sb_path(ch),
               f'{VOL}/finals/ch{ch}_full.mp3'])

def stage_holds(ch):
    return sh(['python3', f'{BASE}/render_holds.py', sb_path(ch),
               f'/tmp/holds_ch{ch}'])

def stage_video(ch):
    from factory_contract import ContractError
    from proof_contract import require_reviewed_assembly
    sb, out = sb_path(ch), f'{VOL}/finals/ch{ch}_full.mp4'
    parts_dir = f'{VOL}/ch{ch}_parts'
    try:
        require_reviewed_assembly(sb, out)
        print(f'  | ch{ch}: current reviewed assembly already exists', flush=True)
        return True
    except (ContractError, OSError):
        pass
    result = subprocess.run(['python3', f'{BASE}/run_blocks.py', sb, parts_dir],
                            capture_output=True, text=True)
    if result.returncode == 2:
        print((result.stdout + result.stderr)[-1600:], flush=True)
        return 'pending_review'
    if result.returncode:
        print((result.stdout + result.stderr)[-1200:], flush=True)
        return False
    os.makedirs(f'{VOL}/finals', exist_ok=True)
    return sh(['python3', f'{BASE}/assemble_proven.py', sb, parts_dir, out])

def stage_verify(ch):
    sb = sb_path(ch)
    from proof_contract import require_reviewed_assembly
    out = f'{VOL}/finals/ch{ch}_full.mp4'
    require_reviewed_assembly(sb, out)
    return sh(['python3', f'{BASE}/verify_clip.py', sb, out])


def stage_voices(ch):
    from factory_contract import require_verified_video
    from proof_contract import require_reviewed_assembly
    sb, out = sb_path(ch), f'{VOL}/finals/ch{ch}_full.mp4'
    require_reviewed_assembly(sb, out)
    require_verified_video(sb, out)
    return sh(['python3', f'{BASE}/check_voices.py', sb, out])


def stage_qwen(ch):
    import tempfile
    from pathlib import Path
    from factory_contract import ContractError, require_verified_video, require_voice_energy, sha256
    from proof_contract import require_reviewed_assembly
    from qwen_review import load_report, require_disposition, write_template
    sb, out = sb_path(ch), Path(f'{VOL}/finals/ch{ch}_full.mp4')
    require_reviewed_assembly(sb, out)
    require_verified_video(sb, out)
    require_voice_energy(sb, out)
    report_path = out.with_suffix('.qwen.json')
    try:
        report = load_report(sb, out)
    except (ContractError, OSError):
        result = subprocess.run(['python3', f'{BASE}/qwen_final.py', str(out), sb,
                                 str(out.with_suffix('.transcript.txt')), '--cues',
                                 str(out.with_suffix('.render_meta.json'))], capture_output=True, text=True)
        if result.returncode:
            print('  | Qwen final failed: ' + (result.stderr or result.stdout)[-600:], flush=True)
            return False
        json.loads(result.stdout)  # never replace an old report with malformed output
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=out.parent, delete=False) as temp:
            temp.write(result.stdout)
            temp_path = temp.name
        os.replace(temp_path, report_path)
        report = load_report(sb, out)
    try:
        require_disposition(sb, out)
    except (ContractError, OSError) as exc:
        template = out.with_suffix('.qwen-disposition.template.json')
        try:
            template_current = json.loads(template.read_text(encoding='utf-8')).get('report_sha256') == sha256(report_path)
        except (OSError, ValueError, AttributeError):
            template_current = False
        if not template_current:
            write_template(out, report)
        print(f'  | Qwen findings need corroboration: {exc}; see {template}', flush=True)
        return 'pending_review'
    print('  | Qwen report current; any findings are disposed (model verdict is advisory)', flush=True)
    return True

def stage_review_pack(ch):
    sb = json.load(open(sb_path(ch)))
    words = sum(len(b['text'].split()) for b in sb['blocks'])
    print(f'  | ch{ch}: {len(sb["blocks"])} blocks, ~{words} words — '
          'Qwen and owner ears remain separate review steps', flush=True)
    return True


def sb_path(ch):
    return f'{BASE}/storyboard_ch6.json' if ch == '06' else f'{BASE}/storyboard_ch{ch}.json'

def src_path(ch):
    return f'{BASE}/chapters/ch06-kaladhva.md' if ch == '06' else f'{BASE}/chapters/ch{ch}.md'

def stage_golden_check(ch):
    if not os.path.exists(f'{BASE}/golden/ch{ch}.json'):
        print(f'  | ch{ch}: golden is unsealed; owner listening and sign-off are pending', flush=True)
        return 'pending_review'
    return sh(['python3', f'{BASE}/golden.py', 'check', ch, f'{VOL}/finals/ch{ch}_full.mp4'])

STAGE_FN = {'preflight': lambda ch: storage_preflight() or True, 'free-tier': lambda ch: free_tier_preflight() or True, 'board': stage_board, 'cast-check': stage_cast_check, 'publish': stage_publish, 'render': stage_render,
            'mms': stage_mms, 'assemble': stage_assemble, 'holds': stage_holds,
            'video': stage_video, 'verify': stage_verify, 'voices': stage_voices, 'qwen': stage_qwen, 'golden-check': stage_golden_check, 'review-pack': stage_review_pack, 'cleanup': lambda ch: stage_cleanup()}

def main():
    args = sys.argv[1:]
    chs = CHAPTERS
    if '--chapters' in args:
        chs = args[args.index('--chapters') + 1].split(',')
    frm = args[args.index('--from') + 1] if '--from' in args else STAGES[0]
    dry = '--dry-run' in args
    stages = STAGES[STAGES.index(frm):]
    print(f'chapters={chs} stages={stages} dry={dry}', flush=True)
    report = {}
    import time as _time
    from events import log_event
    for ch in chs:
        report[ch] = {}
        for st in stages:
            if dry:
                print(f'[{ch}/{st}] would run', flush=True)
                report[ch][st] = 'dry'
                continue
            _t0 = _time.time()
            try:
                ok = STAGE_FN[st](ch)
            except Exception as e:
                print(f'[{ch}/{st}] EXCEPTION {str(e)[:200]}', flush=True)
                ok = False
            status = 'PENDING_REVIEW' if ok == 'pending_review' else ('ok' if ok else 'FAIL')
            report[ch][st] = status
            log_event('tantrasara', ch, st, status,
                      _time.time() - _t0)
            if status != 'ok':
                break
    print(json.dumps(report, indent=1))
    if any('FAIL' in stages.values() for stages in report.values()):
        return 1
    return 2 if any('PENDING_REVIEW' in stages.values() for stages in report.values()) else 0

if __name__ == '__main__':
    rc = main()
    print('RUN_ALL_RESULT=' + {0: 'OK', 1: 'FAILED', 2: 'PENDING_REVIEW'}[rc], flush=True)
    sys.exit(rc)
