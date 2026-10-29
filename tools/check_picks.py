#!/usr/bin/env python3
"""Gate the rung picks (rung_picks.json): budgets, A⊂B, flow, pointer sync.
Run: python3 tools/check_picks.py   (exit 0 = green)"""
import json
import sys

D = '/root/tantrasara'
fails = []
picks = json.load(open(f'{D}/build/canon/rung_picks.json'))
pool = {s['span']: s for s in json.load(open(f'{D}/build/canon/spans_pool.json'))['spans']}
e0 = json.load(open(f'{D}/build/canon/essay0.json'))['units']
src = open(f'{D}/sources/text/reference/tantrasara-chakravarty-marjanovic.txt',
           encoding='utf-8', errors='replace').read().splitlines()
words = {k: len(' '.join(src[v['start']-1:v['end']]).split()) for k, v in pool.items()}
BUD = picks['budgets']

# 1. spans exist, grade rules: A-runghits are grade A; B-runghits are A/B (no C)
for rung in ('A', 'B'):
    for q, sec in picks['rungs'][rung]['sections'].items():
        for sp in sec['spans']:
            if sp not in pool:
                fails.append(f'{rung} Q{q}: unknown span {sp}')
            elif rung == 'A' and pool[sp]['grade'] != 'A':
                fails.append(f'{rung} Q{q}: {sp} grade {pool[sp]["grade"]} (A-rung needs A)')
            elif rung == 'B' and pool[sp]['grade'] == 'C':
                fails.append(f'{rung} Q{q}: {sp} grade C in B (depth only)')

# 2. A subset B per question
for q in map(str, range(1, 7)):
    a = set(picks['rungs']['A']['sections'][q]['spans'])
    b = set(picks['rungs']['B']['sections'][q]['spans'])
    if not a <= b:
        fails.append(f'Q{q}: A not subset of B ({a - b})')

# 3. flow = text-order monotone (argument order = the text's own order)
for rung in ('A', 'B'):
    for q, sec in picks['rungs'][rung]['sections'].items():
        starts = [pool[sp]['start'] for sp in sec['spans']]
        if starts != sorted(starts):
            fails.append(f'{rung} Q{q}: not text-ordered: {sec["spans"]}')

# 4. budgets (reading-time proxy @150wpm; pointers = essay0 quote+plain)
for rung, key in (('A', 'A_words'), ('B', 'B_words')):
    r = picks['rungs'][rung]
    for q, sec in r['sections'].items():
        # pointer words must equal essay0's quote+plain (sync check)
        eq = e0[q]
        want = len(eq['text'].split()) + len(eq['plain'].split())
        if sec['pointer_words'] != want:
            fails.append(f'{rung} Q{q}: pointer_words {sec["pointer_words"]} != essay0 {want}')
        if sec['span_words'] != sum(words[sp] for sp in sec['spans']):
            fails.append(f'{rung} Q{q}: span_words drift')
    if r['total_words'] > BUD[key]:
        fails.append(f"{rung}: {r['total_words']}w > {BUD[key]}w")
    if r['total_min'] > BUD[key.replace('words', 'min')]:
        fails.append(f"{rung}: {r['total_min']}m > {BUD[key.replace('words','min')]}m")
# per-question B ceiling (1500 + pointer slack 100)
for q, sec in picks['rungs']['B']['sections'].items():
    if sec['total_words'] > BUD['B_per_q_words'] + 100:
        fails.append(f"B Q{q}: {sec['total_words']}w > {BUD['B_per_q_words']}+100")

# 5. every question has a body beat (not pointer-only)
for rung in ('A', 'B'):
    for q, sec in picks['rungs'][rung]['sections'].items():
        if not sec['spans']:
            fails.append(f'{rung} Q{q}: no body spans (pointer-only)')

if fails:
    print('PICKS GATE: FAIL')
    for f in fails:
        print(' -', f)
    sys.exit(1)
a, b = picks['rungs']['A'], picks['rungs']['B']
print(f"PICKS GATE: ALL PASS  A={a['total_min']}m ({a['total_words']}w)  "
      f"B={b['total_min']}m ({b['total_words']}w)  A⊂B, text-order, grades, pointers synced")
