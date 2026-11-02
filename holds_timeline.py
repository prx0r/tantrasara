#!/usr/bin/env python3
"""Visual holds timeline for a chapter: term cues + verse/title/figure holds
with white as the breathing default. No audio rendered (planning only).
Usage: python3 holds_timeline.py <storyboard.json> <glossary.json> <out.md>
Rules: thumbnail opener; verse cards while chanting; term card pops at first
mention (Devanagari + confirmed gloss only — proposed glosses listed, not
shown); white holds everywhere else, re-entered at section breaks, long-pause
beats, and dialogue entries. Durations estimated at 150wpm (real timings at
render).
"""
import json, re, sys, unicodedata

sb = json.load(open(sys.argv[1], encoding='utf-8'))
gl = json.load(open(sys.argv[2], encoding='utf-8'))
confirmed = {k for k, v in gl.items() if v.get('status') == 'confirmed'}

def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')

terms = {}
for b in sb['blocks']:
    if b['type'] not in ('narration', 'dialogue') or b['voice'] not in ('granny', 'man'):
        continue
    for w in re.findall(r"[A-Za-zāīūṛṝḷṃḥṅñṭḍṇśṣĀĪŪṚṜḶṂḤṄÑṬḌṆŚṢ·-]+", b['text']):
        c = fold(w.strip('.,!?;:\'"—-'))
        if c in gl and c not in terms:
            terms[c] = b['id']
print(f'{len(terms)} term mentions: ' + ', '.join(f'{k}@{v}' for k, v in sorted(terms.items())))

lines = ['# Holds timeline', '',
         'White is the default. Cards interrupt; white returns at section breaks,',
         '[long pause] beats, and dialogue entries. Proposed (unconfirmed) glosses',
         'do NOT render — their mentions play over white until confirmed.', '']
cur = 'thumbnail'
lines.append(f'start: THUMBNAIL (opener image, bell + intro until first verse)')
shown = set()
n = 0
for b in sb['blocks']:
    if b['id'] == 'b_opener':
        continue
    emitted = False
    if b['type'] == 'verse':
        if cur != 'verse':
            lines.append(f"{b['id']}: VERSE card ({b['text'][:45].strip()})")
            cur = 'verse'
        emitted = True
    if b['type'] in ('title', 'figure'):
        lines.append(f"{b['id']}: {b['type'].upper()} card")
        cur = b['type']
        emitted = True
    hit = [k for k in terms if any(k == fold(w.strip('.,!?;:\'"—-')) for w in re.findall(r"[A-Za-zāīūṛṝḷṃḥṅñṭḍṇśṣĀĪŪṚṜḶṂḤṄÑṬḌṆŚṢ·-]+", b['text']))]
    hit = [k for k in hit if k not in shown]
    for k in hit:
        g = gl[k]
        state = 'CONFIRMED' if k in confirmed else 'proposed — white until confirmed'
        lines.append(f"{b['id']}: TERM {k} ({g['deva']} — {g['gloss']}) [{state}]")
        shown.add(k)
    if not emitted and (b.get('directed', '').startswith('[long pause]') or b['type'] == 'dialogue'):
        if cur != 'white':
            lines.append(f"{b['id']}: WHITE (tone break)")
            cur = 'white'
    n += 1
    if n > 400:
        break
open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'wrote {sys.argv[3]} ({len(lines)} rows)')
