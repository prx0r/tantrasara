#!/usr/bin/env python3
"""PNG storyboard (visual holds) + rough timings from storyboard + receipts.
Usage: python3 build_board.py <storyboard.json> <out.png> <timings.md>
Holds = titles + grouped term cards + figures + closing verse set + opener.
Timings prefer real receipt durations, fall back to 150wpm estimates.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

WPM = 150
sb = json.load(open(sys.argv[1], encoding='utf-8'))
recs = {}
rpath = os.path.expanduser('~/vol/tantrasara/renders/tantras-ra-chapter-6/receipts/calls.jsonl')
if os.path.exists(rpath):
    for l in open(rpath, encoding='utf-8'):
        r = json.loads(l)
        per = float(r['dur']) / max(1, len(r['bids']))
        for b in r['bids']:
            recs[b] = per

by_id = {b['id']: b for b in sb['blocks']}
def dur(b):
    if b['id'] in recs:
        return recs[b['id']], True
    return len(b['text'].split()) / WPM * 60, False

# visual holds in order
holds, cur = [], None
for b in sb['blocks']:
    if b['id'] == 'b_opener':
        holds.append([b]); continue
    if b['type'] == 'verse':
        if cur is None: cur = []
        cur.append(b)
    else:
        if cur: holds.append(cur); cur = None
        if b['type'] in ('title', 'figure'):
            holds.append([b])
if cur: holds.append(cur)
# closing verse set: standalone Devanagari heading section runs long — keep grouped, flag
print(f'holds={len(holds)} real_blocks={len(recs)}')

sec_time, sec_real, sec_n = {}, {}, {}
for b in sb['blocks']:
    d, real = dur(b)
    sec_time[b['section']] = sec_time.get(b['section'], 0) + d
    sec_n[b['section']] = sec_n.get(b['section'], 0) + 1
    if real: sec_real[b['section']] = sec_real.get(b['section'], 0) + d

total = sum(sec_time.values())
lines = ['# Ch6 rough timings', '', '| section | blocks | audio |', '|---|---|---|']
for s in dict(sorted(sec_time.items(), key=lambda x: -x[1])):
    pass
seen = []
for b in sb['blocks']:
    if b['section'] not in seen: seen.append(b['section'])
for s in seen:
    tag = ' (part real)' if s in sec_real else ' (est)'
    lines.append(f"| {s[:45]} | {sec_n[s]} | {sec_time[s]/60:.1f} min{tag} |")
lines.append(f"| **TOTAL** | {len(sb['blocks'])} | **{total/60:.1f} min** |")
open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines[-8:]))

# board
try:
    cap = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    deva = ImageFont.truetype('/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf', 20)
except OSError:
    cap = small = deva = ImageFont.load_default()
COL = {'title': (176, 141, 35), 'term': (165, 42, 42), 'figure': (35, 90, 160),
       'verse': (90, 30, 90), 'opener': (60, 60, 60), 'dialogue': (40, 110, 70)}
CW, CH, COLS = 470, 265, 4
rows = (len(holds) + COLS - 1) // COLS
img = Image.new('RGB', (CW * COLS, 60 + rows * CH), (245, 243, 238))
d = ImageDraw.Draw(img)
d.text((20, 15), f"Tantrasara ch6 — {len(holds)} holds, ~{total/60:.0f} min "
       f"({len(recs)}/{len(sb['blocks'])} blocks real-timed)", font=cap, fill=(20, 20, 20))
def wrap(t, fnt, w=44):
    words, lines, cur = t.split(), [], ''
    for w_ in words:
        if len(cur) + len(w_) + 1 > w:
            lines.append(cur); cur = w_
        else: cur = (cur + ' ' + w_).strip()
    if cur: lines.append(cur)
    return lines[:7]
for i, h in enumerate(holds):
    x, y = (i % COLS) * CW, 60 + (i // COLS) * CH
    kinds = set(b['type'] for b in h)
    kind = 'term' if kinds == {'verse'} else ('opener' if h[0]['id'] == 'b_opener' else h[0]['type'])
    c = COL.get(kind, (80, 80, 80))
    d.rectangle([x + 6, y + 6, x + CW - 6, y + CH - 6], fill=(255, 255, 255), outline=c, width=3)
    d.rectangle([x + 6, y + 6, x + CW - 6, y + 34], fill=c)
    label = f"{i + 1} · {kind} · {h[0]['section'][:32]}"
    dur_s = sum(dur(b)[0] for b in h)
    d.text((x + 14, y + 10), f'{label} · ~{dur_s:.0f}s', font=small, fill=(255, 255, 255))
    txt = ' / '.join(b['text'] for b in h)[:260]
    fnt = deva if any(ord(ch) > 2300 for ch in txt) else cap
    for j, ln in enumerate(wrap(txt, fnt)):
        d.text((x + 14, y + 44 + j * 26), ln, font=fnt, fill=(25, 25, 25))
img.save(sys.argv[2])
print('board ->', sys.argv[2], img.size)
