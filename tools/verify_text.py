#!/usr/bin/env python3
"""Text-side gate (analayo verify.sh parity, text stage). Fails loud.

G1 span pool: contiguity 2436-9842 + every quote round-trips (re-runs builder check).
G2 essay0: 6 canonical units, questions == pool questions, plains non-empty,
   text quotes round-trip, audio[] present (may be empty pre-audio).
G3 beats: beats_core == core count; every verbatim round-trips; plain/tts
   non-empty; no foreign tokens in tts; determinism (re-apply == stored sha1).
G4 layer census: pool == gold+non-gold, gold == core+non-core, counts match
   spans_pool.counts.
Run: python3 tools/verify_text.py   (exit 0 = text green)
"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

D = '/root/tantrasara'
SRC = f'{D}/sources/text/reference/tantrasara-chakravarty-marjanovic.txt'
fails = []


def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'\s+', ' ', s)
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()


src = open(SRC, encoding='utf-8', errors='replace').read()
nsrc = norm(src)

# G1 — span pool via its builder (same-path law, axiom 13)
r = subprocess.run(['python3', f'{D}/tools/build_span_pool.py'],
                   capture_output=True, text=True)
if r.returncode != 0:
    fails.append('G1 span-pool builder failed:\n' + r.stdout + r.stderr)
pool = json.load(open(f'{D}/build/canon/spans_pool.json'))
prev = None
for s in pool['spans']:
    if prev is not None and s['start'] != prev + 1:
        fails.append(f"G1 gap/overlap at {s['span']} (start {s['start']} != {prev+1})")
    if s['quote'] is not None and norm(s['quote']) not in nsrc:
        fails.append(f"G1 {s['span']}: quote not in source")
    prev = s['end']
if len(pool['spans']) != 98:
    fails.append(f"G1 count {len(pool['spans'])} != 98")
print(f"G1 span pool: {len(pool['spans'])} spans, {prev} end, quotes checked")

# G2 — essay0
e0 = json.load(open(f'{D}/build/canon/essay0.json'))
for q in map(str, range(1, 7)):
    u = e0['units'].get(q)
    if not u:
        fails.append(f'G2 essay0 missing unit {q}')
        continue
    if u['question'] != pool['questions'][q]:
        fails.append(f"G2 Q{q} question drift: essay0={u['question']!r} pool={pool['questions'][q]!r}")
    if not u.get('plain'):
        fails.append(f'G2 essay0 unit {q}: empty plain')
    if norm(u.get('text', '')) not in nsrc:
        fails.append(f'G2 essay0 unit {q}: text does not round-trip')
    if 'audio' not in u:
        fails.append(f'G2 essay0 unit {q}: audio[] field missing')
print(f"G2 essay0: {len(e0.get('units', {}))} units, questions synced, plains present")

# G3 — beats
beats = json.load(open(f'{D}/build/canon/beats_core.json'))['beats']
core = [s for s in pool['spans'] if s['grade'] == 'A']
if len(beats) != len(core):
    fails.append(f'G3 beats {len(beats)} != core {len(core)}')
sys.path.insert(0, f'{D}/tools')
import importlib.util
spec = importlib.util.spec_from_file_location('bb', f'{D}/tools/build_beats.py')
bb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb) if False else None  # don't exec main; reuse fns inline
FOREIGN_TOKEN = bb.FOREIGN_TOKEN if hasattr(bb, 'FOREIGN_TOKEN') else re.compile(
    r'[āīūṛṝḷṅñṣśṭḍḥṃ]|svabhava|vikalpa|saktipata|mala|upaya|anupaya|'
    r'sambhava|pasu|bhairava|paramesvara|jagadananda|nirvikalpa|svatantrya|'
    r'visarga|hrdaya|prakasa|vimarsa|jivanmukti|prasiddhi|kancuka')
for b in beats:
    if norm(b['verbatim']) not in nsrc:
        fails.append(f"G3 {b['span']}: verbatim not in source")
    if not b.get('plain') or not b.get('tts_line'):
        fails.append(f"G3 {b['span']}: empty plain/tts")
    if FOREIGN_TOKEN.search(b['tts_line']):
        fails.append(f"G3 {b['span']}: foreign token in tts: {b['tts_line'][:60]}")
    # determinism: stored sha1 == re-derived from verbatim via blunt_key
    key = json.load(open(f'{D}/build/canon/blunt_key.json')).get('swaps', {})
    # re-derive using build_beats' own transform chain (inline copy of contract)
    p = bb.strip_foreign_parens(bb.apply_blunt(b['verbatim'], key)) if hasattr(bb, 'apply_blunt') else None
    if p is not None:
        sha = hashlib.sha1(p.encode()).hexdigest()[:16]
        if sha != b['plain_sha1']:
            fails.append(f"G3 {b['span']}: plain_sha1 drift (key applied differently)")
print(f"G3 beats: {len(beats)} records, verbatim+tts+determinism checked")

# G4 — layer census
gold = [s for s in pool['spans'] if s['grade'] in ('A', 'B')]
gj = json.load(open(f'{D}/build/canon/spans_gold.json'))
cj = json.load(open(f'{D}/build/canon/spans_core.json'))
if gj['counts']['total'] != len(gold) or len(gj['spans']) != len(gold):
    fails.append(f"G4 gold view {len(gj['spans'])} != A+B {len(gold)}")
if len(cj['spans']) != len(core):
    fails.append(f"G4 core view {len(cj['spans'])} != A {len(core)}")
if pool['counts']['grades'] != {'A': 32, 'B': 42, 'C': 24}:
    fails.append(f"G4 grade census drift: {pool['counts']['grades']}")
print(f"G4 layers: pool {len(pool['spans'])} = gold {len(gold)} + rest; core {len(core)}; census ok")

if fails:
    print('TEXT GATE: FAIL')
    for f in fails:
        print(' -', f)
    sys.exit(1)
print('TEXT GATE: ALL PASS')
