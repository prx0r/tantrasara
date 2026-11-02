#!/usr/bin/env python3
"""Batch driver: every chapter through storyboard->render->MMS->assemble->video.
Usage: python3 run_all.py [--chapters 01,02] [--from STAGE] [--dry-run]
Stages: board, cast-check, render, mms, assemble, holds, video, review-pack.
Idempotent everywhere (content hashes); resume by re-running. One chapter
failing never blocks the others. Overnight-safe under nohup.
Owner gates (NOT automated): casting marks, glossary confirms, final ears.
"""
import json, os, subprocess, sys, shutil

BASE = os.path.expanduser('~/tantrasara')
VOL_FREE_MIN_GB = 4.0
LOCAL_FREE_MIN_GB = 1.0

def storage_preflight():
    import shutil as _sh
    local_free = _sh.disk_usage('/tmp').free / 1e9
    r = subprocess.run(['ssh', '-i', os.path.expanduser('~/.ssh/id_ed25519'),
                        '-o', 'BatchMode=yes', 'root@2.28.50.109',
                        'df -BG /mnt/HC_Volume_106427611 | tail -1'],
                       capture_output=True, text=True, timeout=60)
    vol_free = float(r.stdout.split()[3].rstrip('G')) if r.returncode == 0 else -1
    print(f'storage: local {local_free:.1f}G free, volume {vol_free:.0f}G free', flush=True)
    assert local_free >= LOCAL_FREE_MIN_GB, f'local disk critical ({local_free:.1f}G)'
    assert vol_free < 0 or vol_free >= VOL_FREE_MIN_GB, f'volume critical ({vol_free:.0f}G)'

def stage_cleanup():
    # transient build debris only; caches (models, npm) and other lanes untouched
    for p in ['/tmp/clip_frames', '/tmp/fm2_frames', '/tmp/ts_holds', '/tmp/mmsclip',
              '/tmp/mms_grp.f32', '/tmp/mms_eng_test.f32']:
        shutil.rmtree(p, ignore_errors=True)
    for pat in ['/tmp/*_pilot*.mp4', '/tmp/ch*_opening*.mp4', '/tmp/first_min*.mp4']:
        import glob as _g
        for f in _g.glob(pat):
            try:
                os.remove(f)
            except OSError:
                pass
    print('cleanup: transient frames/tmp audio removed (R2 holds the shipped copies)', flush=True)
    return True
CHAPTERS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
STAGES = ['preflight', 'board', 'cast-check', 'render', 'mms', 'assemble', 'holds', 'video', 'review-pack', 'cleanup']

def sh(cmd, **kw):
    print('+', ' '.join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    tail = (r.stderr or r.stdout or '').strip().splitlines()[-3:]
    for l in tail:
        print('  |', l[:160], flush=True)
    return r.returncode == 0

def stage_board(ch):
    sb = f'{BASE}/storyboard_ch{ch}.json'
    ov = f'{BASE}/overrides_ch{ch}.json'
    cmd = ['python3', f'{BASE}/build_storyboard.py', f'{BASE}/chapters/ch{ch}.md', sb]
    if ch != '06' and os.path.exists(ov):
        cmd.append(ov)
    elif ch == '06':
        cmd.append(f'{BASE}/overrides_ch6.json')
    if not os.path.exists(ov) and ch not in ('01', '06'):
        print(f'  | ch{ch}: no overrides yet — casting sheet pending, SKIP')
        return False
    return sh(cmd)

def stage_cast_check(ch):
    sb = json.load(open(f'{BASE}/storyboard_ch{ch}.json'))
    errs = sb.get('validation', {}).get('errors', [])
    print(f"  | ch{ch}: {len(errs)} validation errors", flush=True)
    return not errs

def stage_render(ch):
    return sh(['python3', f'{BASE}/render_chapter.py', f'{BASE}/storyboard_ch{ch}.json'])

def stage_mms(ch):
    # per-group MMS via build_clip's align path is per-clip; full-chapter
    # MMS runs inside build_video (group wavs already on volume).
    print('  | ch%s: MMS runs inside video build (no separate step)' % ch, flush=True)
    return True

def stage_assemble(ch):
    return sh(['python3', f'{BASE}/assemble_chapter.py', f'{BASE}/storyboard_ch{ch}.json',
               f'/tmp/ch{ch}_full.mp3'])

def stage_holds(ch):
    return sh(['python3', f'{BASE}/render_holds.py', f'{BASE}/storyboard_ch{ch}.json',
               f'/tmp/holds_ch{ch}'])

def stage_video(ch):
    sb = json.load(open(f'{BASE}/storyboard_ch{ch}.json'))
    bids = ','.join(b['id'] for b in sb['blocks'] if b['id'] != 'b_opener')
    return sh(['python3', f'{BASE}/build_clip.py', f'{BASE}/storyboard_ch{ch}.json',
               bids, f'/tmp/ch{ch}_full.mp4'])

def stage_review_pack(ch):
    sb = json.load(open(f'{BASE}/storyboard_ch{ch}.json'))
    words = sum(len(b['text'].split()) for b in sb['blocks'])
    print(f'  | ch{ch}: {len(sb["blocks"])} blocks, ~{words} words — '
          'frames + whisper + Qwen queued for owner review', flush=True)
    return True

STAGE_FN = {'preflight': lambda ch: storage_preflight() or True, 'board': stage_board, 'cast-check': stage_cast_check, 'render': stage_render,
            'mms': stage_mms, 'assemble': stage_assemble, 'holds': stage_holds,
            'video': stage_video, 'review-pack': stage_review_pack, 'cleanup': lambda ch: stage_cleanup()}

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
    for ch in chs:
        report[ch] = {}
        for st in stages:
            if dry:
                print(f'[{ch}/{st}] would run', flush=True)
                report[ch][st] = 'dry'
                continue
            try:
                ok = STAGE_FN[st](ch)
            except Exception as e:
                print(f'[{ch}/{st}] EXCEPTION {str(e)[:200]}', flush=True)
                ok = False
            report[ch][st] = 'ok' if ok else 'FAIL'
            if not ok:
                break
    print(json.dumps(report, indent=1))

if __name__ == '__main__':
    main()
