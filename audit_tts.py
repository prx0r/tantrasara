#!/usr/bin/env python3
"""TTS-cleanliness audit: finds text a voice would read wrong.
Usage: python3 audit_tts.py
Checks: unbalanced quotes/parens, URLs, markdown artifacts, digits,
HTML entities, non-Devanagari foreign scripts, abbreviations, gmail leftovers,
double spaces, straight quotes.
"""
import re, os, glob

BASE = os.path.expanduser('~/tantrasara/chapters')
ABBR = re.compile(r'\b(?:St|Dr|Mr|Mrs|Ms|vs|etc|e\.g|i\.e|cf|viz|approx|dept|St)\.')
CHROME = re.compile(r'Keep reading|Prior Trades|tradesprior|\+1$|TextGrid Repository ?\+1|Sanskrit & Trika Shaivism \+1|tylergneill|gretil\.sub|Skip to content|Using Gmail|screen readers|Inbox$|\(no subject\)|s2/favicons|\[image\]')

for path in sorted(glob.glob(f'{BASE}/ch*.md')):
    ch = os.path.basename(path)
    lines = open(path, encoding='utf-8').read().splitlines()
    full = '\n'.join(lines)
    issues = []
    if full.count('"') % 2:
        issues.append(f"unbalanced straight quotes ({full.count(chr(34))})")
    if full.count('(') != full.count(')'):
        issues.append('unbalanced parens')
    for i, l in enumerate(lines, 1):
        if re.search(r'https?://|www\.', l):
            issues.append(f'L{i}: URL [{l[:70]}]')
        if re.search(r'\*\*|\[.*\]\(.*\)|^#{3,}', l):
            issues.append(f'L{i}: md artifact [{l[:70]}]')
        if re.search(r'&(#x?[0-9a-f]+|[a-z]+);', l):
            issues.append(f'L{i}: html entity [{l[:70]}]')
        if ABBR.search(l):
            issues.append(f'L{i}: abbreviation [{ABBR.search(l).group(0)}] {l[:60]}')
        if CHROME.search(l):
            issues.append(f'L{i}: chrome leftover [{l[:80]}]')
        if re.search(r'[⌀-〿぀-ヿ가-힯]', l):
            issues.append(f'L{i}: non-Devanagari foreign script [{l[:60]}]')
        if re.search(r'  +', l):
            issues.append(f'L{i}: double space')
    digits = sorted(set(re.findall(r'\d[\d,\.]*(?:\^\d+)?', full)), key=lambda s: (len(s), s))
    if digits:
        issues.append(f"digits: {', '.join(digits[:20])}")
    print(f'== {ch}: {len(issues)} issues')
    for x in issues[:14]:
        print('  -', x)
