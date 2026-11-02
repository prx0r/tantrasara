#!/usr/bin/env python3
"""One-pass chapter cleanup: blurbs, duplicate titles, Keep reading,
citation tails. Run once; verified by audit + storyboard gates after.
"""
import re, glob

BLURB = re.compile(r'slang \w+ (retelling|adaptation)|slang (retelling|adaptation)|irreverent retelling', re.I)
CITE = re.compile(r'\s*(?:[A-Z][\w&.-]*(?: [A-Z][\w&.-]*){0,3}|[\w.-]+\.[\w.]+) \+\d\s*$')
PROV = ('Textual basis', 'Source note', 'Sources:', 'Textual sources')

for f in sorted(glob.glob('/home/ubuntu/tantrasara/chapters/ch*.md')):
    lines = open(f, encoding='utf-8').read().splitlines()
    # drop duplicate title (first non-blank line == H1 text)
    if lines and lines[0].startswith('# '):
        for i in range(1, min(4, len(lines))):
            if lines[i].strip() == lines[0][2:].strip():
                print(f'{f.split("/")[-1]}: drop duplicate title')
                del lines[i]
                break
    out = []
    for l in lines:
        s = l
        if s.strip() == 'Keep reading':
            print(f'{f.split("/")[-1]}: drop Keep reading')
            continue
        if BLURB.search(s) and len(s.split()) > 8 and not s.startswith('#'):
            print(f'{f.split("/")[-1]}: drop blurb [{s[:60]}]')
            continue
        ns = CITE.sub('', s)
        if ns != s:
            print(f'{f.split("/")[-1]}: strip citation [{s[-40:]}]')
            s = ns
        out.append(s)
    open(f, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('done')
