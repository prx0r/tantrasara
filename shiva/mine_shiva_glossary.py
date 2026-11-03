#!/usr/bin/env python3
"""Draft per-sutra glossaries for the shiva lane: IAST terms + appositives.
Usage: python3 mine_shiva_glossary.py
Every entry starts proposed (white until confirmed). Mirrors
mine_glossary.py with a shiva SKIP set (common English-loan Sanskrit and
series names are not terms).
"""
import json, os, re, unicodedata

BASE = os.path.expanduser('~/tantrasara')
SHIVA = os.path.join(BASE, 'shiva')
SKIP = {'shiva', 'siva', 'sutra', 'sutras', 'vasugupta', 'ksemaraja',
        'kashmir', 'guru', 'tantra', 'yoga', 'mantra', 'gurus',
        'abhinavagupta', 'kashmir', 'donut', 'mate', 'bloke'}


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


CAPS = 'ĀĪŪṚṜḶṂḤṄÑṬḌṆŚṢ'
WORD = f'[A-Za-zāīūṛṝḷṃḥṅñṭḍṇśṣ{CAPS}·-]+'

CHS = [f's{i:02d}' for i in range(78)]
for ch in CHS:
    sb = json.load(open(f'{SHIVA}/storyboards/storyboard_{ch}.json'))
    terms = {}
    for b in sb['blocks']:
        if b['type'] not in ('narration', 'dialogue') or not b['text'].strip():
            continue
        for w in re.findall(WORD, b['text']):
            c = fold(w.strip('.,!?;:\'"—-'))
            if c in terms or len(c) < 4 or c in SKIP:
                continue
            if not re.search(r'[āīūṛṝḷṃḥṅñṭḍṇśṣĀĪŪṚṜḶṂḤṄÑṬḌṆŚṢ]', w):
                continue
            terms[c] = b['id']
    gl = {}
    for k, bid in sorted(terms.items()):
        gl[k] = {'deva': '', 'gloss': '', 'status': 'proposed', 'cue_blocks': [bid],
                 'note': 'auto-mined; needs Deva + gloss review'}
    full = ' '.join(b['text'] for b in sb['blocks'] if b['type'] in ('narration', 'dialogue'))
    for k in list(gl):
        surf = None
        for w in re.findall(WORD, full):
            if fold(w.strip('.,!?')) == k:
                surf = w.strip('.,!?')
                break
        if not surf:
            continue
        m = re.search(re.escape(surf) + r'\s*,?\s+(?:the|a|an)\s+([^,.;]{3,60})', full)
        if m:
            gl[k]['gloss'] = m.group(0)[len(surf):].strip(' ,')[:80]
            gl[k]['note'] = 'appositive-mined, confirm'
    json.dump(gl, open(f'{SHIVA}/glossary_{ch}.json', 'w'), ensure_ascii=False, indent=1)
    filled = sum(1 for v in gl.values() if v['gloss'])
    print(f'{ch}: {len(gl)} terms, {filled} appositive glosses')
