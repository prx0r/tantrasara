#!/usr/bin/env python3
"""Provisional casting for the shiva lane (same rules as tantrasara):
consecutive quote runs alternate man-first; short nominal demonstration
runs stay all-granny as one mind; lone quotes default granny unless they
read as skeptic challenges (you/why/how + ?). Every call UNSURE in
SHIVA-INTAKE.md; owner blesses. Writes shiva/overrides_sNN.json.
"""
import json, os, re, subprocess, sys

BASE = os.path.expanduser('~/tantrasara')
SHIVA = os.path.join(BASE, 'shiva')
CHS = sys.argv[1:] or [f's{i:02d}' for i in range(78)]
notes = []
for ch in CHS:
    src = f'{SHIVA}/chapters/{ch}.md'
    raw = f'/tmp/shiva_sb_{ch}_raw.json'
    subprocess.run(['python3', f'{BASE}/build_storyboard.py', src, raw],
                   capture_output=True, text=True)
    sb = json.load(open(raw))
    blocks = sb['blocks']
    ov, i = {}, 0
    while i < len(blocks):
        b = blocks[i]
        if not (b.get('type') == 'dialogue' and b.get('voice') in ('UNCAST', 'man')):
            i += 1
            continue
        j = i
        run = []
        while j < len(blocks) and blocks[j].get('type') == 'dialogue' and blocks[j].get('voice') in ('UNCAST', 'man'):
            run.append(blocks[j])
            j += 1
        uncast = [x for x in run if x['voice'] == 'UNCAST']
        texts = [x['text'] for x in run]
        all_short = all(len(re.findall(r"[A-Za-z'_-]+", t)) <= 8 for t in texts)
        demo = sum(1 for t in texts if re.search(r'(there|another|here|this is|that is|yes|no|wonderful|excellent|right|gone|hello)', t.lower()))
        first, last = run[0]['id'], run[-1]['id']
        ex = texts[0][:70].replace(chr(10), ' ')
        if len(run) >= 3 and all_short and demo >= len(run) - 1:
            for x in uncast:
                ov[x['id']] = 'granny'
            notes.append(f'{ch} run {first}..{last} ({len(run)}): ALL-GRANNY provisional - one mind. UNSURE, e.g. {ex}')
        elif len(run) >= 2:
            for k, x in enumerate(run):
                if x['voice'] == 'UNCAST':
                    ov[x['id']] = 'man' if k % 2 == 0 else 'granny'
            notes.append(f'{ch} run {first}..{last} ({len(run)}): ALTERNATE man-first provisional. UNSURE, e.g. {ex}')
        else:
            x, t = run[0], run[0]['text']
            if re.search(r"(you have|you've|you |your |why |how |what about)", t.lower()) and '?' in t:
                ov[x['id']] = 'man'
                notes.append(f"{ch} {x['id']} lone -> MAN provisional skeptic challenge UNSURE: {t[:90].replace(chr(10), ' ')}")
            else:
                ov[x['id']] = 'granny'
                notes.append(f"{ch} {x['id']} lone -> GRANNY provisional single demonstrator UNSURE: {t[:90].replace(chr(10), ' ')}")
        i = j
    json.dump(ov, open(f'{SHIVA}/overrides_{ch}.json', 'w'), indent=1)
    print(ch, len(ov), 'provisional calls')
open('/tmp/shiva_unsure_notes.txt', 'w').write('\n'.join(notes))
print('unsure notes:', len(notes))
