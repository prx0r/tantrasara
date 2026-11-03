#!/usr/bin/env python3
"""Mine verse literal + final glosses from translation-work into
verse_gloss_chNN.json (all proposed — owner confirms in bulk like glossaries).

Sources (translation-work, frozen T1; L3 machine-proposed):
  literal: T1 token-gloss stream per verse, [and]- markers stripped.
  final:   L4 song lines when present, else L3 lines joined, else ''.
           final_source records which (L4|L3|T1draft|none) so the L4 upgrade
           is a data fill, never a code change.
Matching: storyboard multi-line verse blocks <-> T1 verses by normalized
similarity (folded IAST, hyphens/whitespace stripped, difflib ratio >= 0.5,
greedy best, each block used once). Scores recorded; owner confirms.
Render matches by verse_match_key(block text) — deterministic across
storyboard rebuilds (no positional overrides to remap, cf. M12).

Usage: python3 mine_verse_gloss.py [chNN ...]  (default: all 22)
Writes verse_gloss_chNN.json beside the glossaries.
"""
import json, os, re, sys, difflib, glob

BASE = os.path.expanduser('~/tantrasara')
TW = '/tmp/translation-work'
sys.path.insert(0, BASE)
from holds import to_iast, verse_match_key
import unicodedata


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')


def parse_t1(md_path):
    """Split frozen T1.md into verses at // abhts_X markers (end-markers:
    the text preceding each marker is that verse; markers may wrap across
    lines and sit mid-line)."""
    text = open(md_path, encoding='utf-8').read()
    text = re.sub(r'^#[^\n]*\n', '', text, flags=re.M)  # headings
    text = re.sub(r'\*.*?\*', '', text, flags=re.S)  # ledger/source notes
    text = re.sub(r'^##[^\n]*\n', '', text, flags=re.M)  # passage headers
    # reassign: each verse = text before its marker + text after previous marker
    verses, buf = [], ''
    segs = re.split(r'(//\s*abhts_[\d.]+\b)', text)
    for seg in segs:
        if re.fullmatch(r'//\s*abhts_[\d.]+\s*', seg):
            ref = re.search(r'abhts_[\d.]+', seg).group(0)
            verses.append({'ref': ref, 'raw': buf})
            buf = ''
        else:
            buf += ' ' + seg
    if buf.strip():
        verses.append({'ref': verses[-1]['ref'] + '+tail' if verses else 'tail',
                       'raw': buf})
    cleaned = []
    for v in verses:
        lit = v['raw'].replace('[and]-', '')
        lit = re.sub(r'\s+', ' ', lit).strip(' ;—-|')
        # drop attribution/source tail lines
        if len(lit) < 20:
            continue
        cleaned.append({'ref': v['ref'], 'literal': lit,
                        'surfaces': ' '.join(
                            re.findall(r'\(([^)]*)\)', v['raw']))})
    return cleaned


def load_l3(ch):
    """L3 finals keyed by order; {} when absent (L4/L3 still ongoing)."""
    for pat in [f'{TW}/tantrasara-a{ch}/data/tsa-a{ch}.l3.json']:
        if os.path.exists(pat):
            try:
                return json.load(open(pat, encoding='utf-8'))
            except Exception:
                return []
    return []


def norm(s):
    # T1 surfaces are IAST; storyboard blocks are Devanagari — both end up
    # folded ASCII via to_iast (Devanagari passes through untouched).
    try:
        s = to_iast(s)
    except Exception:
        pass
    return re.sub(r'[^a-z]', '', fold(s).replace('-', ''))


def mine(ch):
    sb_path = f'{BASE}/storyboard_ch6.json' if ch == '06' else f'{BASE}/storyboard_ch{ch}.json'
    sb = json.load(open(sb_path, encoding='utf-8'))
    blocks = [b for b in sb['blocks']
              if b['type'] == 'verse' and len(b['text'].split()) > 3]
    t1_path = f'{TW}/tantrasara-a{ch}/T1.md'
    if not os.path.exists(t1_path):
        print(f'ch{ch}: no T1.md, skipping')
        return
    t1 = parse_t1(t1_path)
    l3 = load_l3(ch)
    entries, used = {}, set()
    for i, t in enumerate(t1):
        best, score = None, 0
        for b in blocks:
            if b['id'] in used:
                continue
            s = difflib.SequenceMatcher(None, norm(t['surfaces']),
                                        norm(b['text'])).ratio()
            if s > score:
                best, score = b, s
        if best is None or score < 0.5:
            print(f'ch{ch} {t["ref"]}: NO MATCH (best {score:.2f})')
            continue
        used.add(best['id'])
        l3e = l3[i] if i < len(l3) and isinstance(l3, list) else None
        final, src = '', 'none'
        if l3e and l3e.get('lines'):
            final, src = ' '.join(l3e['lines']), 'L3'
        entries[t['ref']] = {
            'bids': [best['id']],
            'match_key': verse_match_key(best['text']),
            'match_score': round(score, 2),
            'literal': t['literal'],
            'final': final,
            'final_source': src,
            'l4': None,
            'status': 'proposed',
        }
        print(f'ch{ch} {t["ref"]} -> {best["id"]} ({score:.2f}) final:{src}')
    out = f'{BASE}/verse_gloss_ch{ch}.json'
    json.dump(entries, open(out, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'ch{ch}: {len(entries)} verse entries -> {out}')


if __name__ == '__main__':
    chs = sys.argv[1:] or [f'{i:02d}' for i in range(1, 23)]
    for ch in chs:
        mine(ch.zfill(2))
