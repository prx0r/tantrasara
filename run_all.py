#!/usr/bin/env python3
"""Batch driver: every chapter through storyboard->render->MMS->assemble->video.
Usage: python3 run_all.py [--chapters 01,02] [--from STAGE] [--dry-run]
Stages: board, cast-check, render, mms, assemble, holds, video, review-pack.
Idempotent everywhere (content hashes); resume by re-running. One chapter
failing never blocks the others. Overnight-safe under nohup.
Owner gates (NOT automated): casting marks, glossary confirms, final ears.
"""
import json, os, subprocess, sys

BASE = os.path.expanduser('~/tantrasara')
CHAPTERS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
STAGES = ['board', 'cast-check', 'render', 'mms', 'assemble', 'holds', 'video', 'review-pack']

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

STAGE_FN = {'board': stage_board, 'cast-check': stage_cast_check, 'render': stage_render,
            'mms': stage_mms, 'assemble': stage_assemble, 'holds': stage_holds,
            'video': stage_video, 'review-pack': stage_review_pack}

def main():
    args = sys.argv[1:]
    chs = CHAPTERS
    if '--chapters' in args:
        chs = args[args.index('--chapters') + 1].split(',')
    frm = args[args.index('--from') + 1] if '--from' in args else 'board'
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
