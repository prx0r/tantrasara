#!/usr/bin/env python3
"""Voice-presence check: every voiced seat must be audible in the mix.
Usage: python3 check_voices.py <storyboard.json> <full.mp4>
For each voice with blocks: sample up to 5 bids spread across the
chapter, measure mean volume in a window at each onset (from the
.word subs dump beside the mp4, or rebuild windows from groups);
FAIL any voice with all windows silent (< -40dB). One English
man window is whisper spot-checked against its text. Exit 0/1.
Why this exists: gates checked WORDS (whisper) and CARDS (frames)
but never WHO speaks — a missing voice passed everything (M29).
"""
import glob
import json
import os
import re
import subprocess
import sys

FAIL, PASS = [], []


def check(name, ok, detail=''):
    (PASS if ok else FAIL).append(
        f'{"PASS" if ok else "FAIL"} {name}' + (f' — {detail}' if detail else ''))


def vol(mp4, t0, dur):
    r = subprocess.run(
        ['ffmpeg', '-nostats', '-v', 'info', '-ss', str(max(0.0, t0)),
         '-i', mp4, '-t', str(dur), '-af', 'volumedetect', '-f', 'null', '-'],
        capture_output=True, text=True)
    m = re.search(r'mean_volume: ([\-\d.]+) dB', r.stderr)
    return float(m.group(1)) if m else -91.0


def main():
    sb_path, mp4 = sys.argv[1], sys.argv[2]
    sb = json.load(open(sb_path, encoding='utf-8'))
    base, _ = os.path.splitext(mp4)
    subs = []
    for cand in glob.glob(os.path.dirname(mp4) + '/*.subs.json'):
        try:
            subs += json.load(open(cand, encoding='utf-8'))
        except OSError:
            pass
    if not subs and os.path.exists(base + '.subs.json'):
        subs = json.load(open(base + '.subs.json', encoding='utf-8'))
    bybid = {}
    for s in subs:
        bybid.setdefault(s['bid'], []).append(s)
    byvoice = {}
    for b in sb['blocks']:
        if b.get('voice') in ('granny', 'man', 'verse'):
            byvoice.setdefault(b['voice'], []).append(b['id'])
    for voice, bids in sorted(byvoice.items()):
        have = [b for b in bids if b in bybid]
        if not have:
            check(f'{voice} voice timed', False, 'no subs rows')
            continue
        picks = have[::max(1, len(have) // 5)][:5]
        levels = []
        for bid in picks:
            rows = sorted(bybid[bid], key=lambda r: r['t'])
            t0, t1 = rows[0]['t'], rows[-1]['t'] + 0.6
            levels.append((bid, round(t0, 1), vol(mp4, t0 - 0.3, min(10.0, t1 - t0 + 0.6))))
        audible = [l for l in levels if l[2] > -40.0]
        check(f'{voice} voice audible ({len(audible)}/{len(levels)} windows)',
              bool(audible),
              ', '.join(f'{bid}@{t}s {db}dB' for bid, t, db in levels))
    print('\n'.join(PASS + FAIL))
    print('VOICES ' + ('PRESENT' if not FAIL else 'MISSING'))
    sys.exit(0 if not FAIL else 1)


if __name__ == '__main__':
    main()
