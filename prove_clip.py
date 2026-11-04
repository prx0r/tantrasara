#!/usr/bin/env python3
"""Proof pack for one chunk part (the autonomous visual loop).
Usage: python3 prove_clip.py <storyboard.json> <part.mp4> <outdir>
Reads <part>.render_meta.json + .subs.json (written by build_clip):
boundary frames at thumbnail, every cue onset, every drop hold,
plus two mid-speech frames; contact sheet + index with the expected
card per the storyboard; gate_visual machine run; notes template.
Eye (human or Qwen) reads the pack against the storyboard beats —
that read is the gate. Nothing downstream runs on red.
"""
import json, os, re, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))


def frame(mp4, t, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(max(0.0, t)),
                    '-i', mp4, '-frames:v', '1', out], check=True)


def main():
    sb_path, mp4, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    sb = json.load(open(sb_path, encoding='utf-8'))
    meta = json.load(open(os.path.splitext(mp4)[0] + '.render_meta.json', encoding='utf-8'))
    byid = {b['id']: b for b in sb['blocks']}
    dur = meta['duration']
    shots = [('t0-thumbnail', 0.5, 'thumbnail opens')]
    for c in meta.get('cues', []):
        b = byid.get(meta.get('bids', [None])[0], {})
        shots.append((f"cue-{c['key']}", max(0.0, c['t'] + 0.15), f"card {c['key']} just on"))
    for bid, d in meta.get('drops', {}).items():
        shots.append((f"drop-{bid}", d['at'] + (d.get('pause', 1.0) / 2),
                      f"white hold across {d.get('pause')}s pause"))
    for frac, name in ((0.33, 'mid-speech-1'), (0.66, 'mid-speech-2')):
        shots.append((name, dur * frac, 'karaoke on the spoken word'))
    idx = []
    for name, t, expect in shots:
        fp = os.path.join(outdir, f'{name}.png')
        try:
            frame(mp4, t, fp)
            idx.append((name, round(t, 1), expect, 'ok'))
        except subprocess.CalledProcessError as e:
            idx.append((name, round(t, 1), expect, f'FRAME FAIL {e}'))
    with open(os.path.join(outdir, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(f'# Proof {os.path.basename(mp4)} — {meta["cuts"]} cuts, '
                f'{dur}s, white {meta["white_pct"]}%\n\n')
        for name, t, expect, st in idx:
            f.write(f'- [{st}] {name}.png @ {t}s — expect: {expect}\n')
        f.write('\n## Eye notes (fill per frame: right card / subtitle / karaoke / tofu / overflow)\n')
    # contact sheet
    from PIL import Image
    files = [os.path.join(outdir, n + '.png') for n, _, _, st in idx if st == 'ok']
    if files:
        cols, cw, chh = 3, 640, 360
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new('RGB', (cw * cols, rows * chh + 40), (245, 243, 238))
        for i, fp in enumerate(files):
            sheet.paste(Image.open(fp).resize((cw, chh)), ((i % cols) * cw, 40 + (i // cols) * chh))
        sheet.save(os.path.join(outdir, 'contact_sheet.png'))
    # machine gate (presence of meta/subs/mp4 asserted inside)
    lane_ch = re.search(r'ch(\d+)', sb_path)
    lane_ch = lane_ch.group(1).zfill(2) if lane_ch else None
    glp = os.path.join(BASE, f'glossary_ch{lane_ch}.json') if lane_ch else None
    cmd = ['python3', f'{BASE}/gate_visual.py', sb_path, '--meta',
           os.path.splitext(mp4)[0] + '.render_meta.json', '--subs',
           os.path.splitext(mp4)[0] + '.subs.json', '--mp4', mp4]
    if glp and os.path.exists(glp):
        cmd += ['--glossary', glp]
    if lane_ch:
        _ap = os.path.join(BASE, f'approved_ch{lane_ch}.json')
        if os.path.exists(_ap):
            cmd += ['--approved', _ap]
    r = subprocess.run(cmd, capture_output=True, text=True)
    open(os.path.join(outdir, 'gate.txt'), 'w').write(r.stdout + r.stderr)
    print(open(os.path.join(outdir, 'gate.txt')).read())
    print(f'proof: {outdir} ({len(files)} frames + gate + index)')


if __name__ == '__main__':
    main()
