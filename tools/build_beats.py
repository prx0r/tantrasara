#!/usr/bin/env python3
"""Build beat records from the span pool (analayo segN_script parity, text side).

Per core span (grade A): {span, question, grade, provenance, verbatim,
plain, tts_line, plain_sha1}. Rules:
- verbatim = the span's carrying quote, EXACT (round-trip assert vs source).
- plain = blunt_key applied (deterministic; identity while key is empty
  except mechanical foreign-parenthetical strip — the English already
  surrounds the term: "my heart (hrdaya)" -> "my heart").
- tts_line = plain, speech-hygiene applied: markdown stripped, no foreign
  tokens (Sanskrit/diacritics) remain, no dangling punctuation.
- R1: nothing authored; plain/tts are functions of (quote, key).

Run: python3 tools/build_beats.py   -> build/canon/beats_core.json
"""
import hashlib
import json
import re
import unicodedata

D = '/root/tantrasara'
SRC = f'{D}/sources/text/reference/tantrasara-chakravarty-marjanovic.txt'
POOL = f'{D}/build/canon/spans_pool.json'
KEY = f'{D}/build/canon/blunt_key.json'
OUT = f'{D}/build/canon/beats_core.json'

FOREIGN = re.compile(r'\(([^)]*[^\x00-\x7f][^)]*)\)')  # parens containing non-ASCII
FOREIGN_TOKEN = re.compile(r'[āīūṛṝḷṅñṣśṭḍḥṃ]|svabhava|vikalpa|saktipata|mala|'
                           r'upaya|anupaya|sambhava|pasu|bhairava|paramesvara|'
                           r'jagadananda|nirvikalpa|svatantrya|visarga|hrdaya|'
                           r'prakasa|vimarsa|jivanmukti|prasiddhi|kancuka')


def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s.lower())
    return s.strip()


def apply_blunt(quote, swaps):
    out = quote
    for k, v in swaps.items():
        out = out.replace(k, v)
    return out


SPOKEN = {  # bare foreign token -> spoken form (Fish never speaks source terms, axiom 6)
    'pasu': 'bound soul',
    'siva': 'Siva',       # loanword, owner-approved class (analayo: arahant/tathagata/dhamma)
    'mala': 'impurity',
    'saktipata': 'descent of grace',
    'hrdaya': 'heart',
    'visarga': 'emission',
}


def strip_foreign_parens(text):
    # "my heart (hrdaya) pulsate" -> "my heart pulsate" (English already there);
    # also drops parens holding foreign tokens written in ASCII ("(hrdaya)").
    def _drop(m):
        inner = m.group(1)
        if re.search(r'[^\x00-\x7f]', inner) or FOREIGN_TOKEN.search(inner):
            return ''
        return m.group(0)
    return re.sub(r'\s*\(([^)]*)\)', _drop, text)


def spoken_forms(text):
    # bare foreign tokens -> English (longest first; word-boundary safe)
    for t in sorted(SPOKEN, key=len, reverse=True):
        text = re.sub(r'\b' + t + r'\b', SPOKEN[t], text, flags=re.I)
    return text


def tts_hygiene(text):
    t = strip_foreign_parens(text)
    t = spoken_forms(t)
    t = re.sub(r'[#*_`]', '', t)                 # markdown
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'[,;:]\s*$', '', t)              # dangling connectors
    t = re.sub(r'\s+([,.])', r'\1', t)           # space before punct
    if t and t[-1] not in '.!?':
        t += '.'                                 # full stop for speech
    return t


def main():
    src = open(SRC, encoding='utf-8', errors='replace').read()
    nsrc = norm(src)
    pool = json.load(open(POOL))
    key = json.load(open(KEY))
    swaps = key.get('swaps', {})
    core = [s for s in pool['spans'] if s['grade'] == 'A']
    beats, fails = [], []
    for s in core:
        v = s['quote']
        if norm(v) not in nsrc:
            fails.append(f"{s['span']}: verbatim does not round-trip")
            continue
        p = strip_foreign_parens(apply_blunt(v, swaps))
        t = tts_hygiene(p)
        if FOREIGN_TOKEN.search(t):
            fails.append(f"{s['span']}: foreign token in tts_line (add to SPOKEN map): {t[:70]}")
        if not p or not t:
            fails.append(f"{s['span']}: empty plain/tts")
        beats.append({
            'span': s['span'],
            'question': s['question'],
            'grade': s['grade'],
            'provenance': {'file': pool['source'],
                           'start_line': s['start'], 'end_line': s['end']},
            'verbatim': v,
            'plain': p,
            'tts_line': t,
            'plain_sha1': hashlib.sha1(p.encode()).hexdigest()[:16],
            'sanskrit_span': s.get('sanskrit_span', False),
        })
    out = {
        'schema': 'tantrasara beats_core v1 (2026-10-29, text side; audio pending)',
        'rule': 'verbatim extracted (round-trip asserted) -> plain = blunt_key(t) + foreign-paren strip -> tts = hygiene. R1: none authored.',
        'blunt_key': 'build/canon/blunt_key.json (owner-driven; mostly identity — translation already plain)',
        'counts': {'total': len(beats)},
        'beats': beats,
    }
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print(f'beats_core.json: {len(beats)} beats')
    from collections import Counter
    print('per-question:', dict(sorted(Counter(b["question"] for b in beats).items())))
    if fails:
        print('FAILS:')
        for f in fails:
            print(' -', f)
    else:
        print('verbatim round-trips: %d/%d  tts clean: %d/%d' % (
            len(beats), len(core), len(beats), len(core)))
    # determinism proof: re-apply and compare
    again = [hashlib.sha1(strip_foreign_parens(apply_blunt(b['verbatim'], swaps)).encode()).hexdigest()[:16] for b in beats]
    same = sum(1 for a, b in zip(again, [x['plain_sha1'] for x in beats]) if a == b)
    print(f'determinism: {same}/{len(beats)} byte-identical on re-apply')
    raise SystemExit(1 if fails or same != len(beats) else 0)


if __name__ == '__main__':
    main()
