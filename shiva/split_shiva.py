#!/usr/bin/env python3
"""Split shivasutrasfinal (gmail dump) into per-sutra chapters s00..s77.
Usage: python3 split_shiva.py
s00 = series intro; s01-s22 = 1.1-1.22; s23-s32 = 2.1-2.10; s33-s77 = 3.1-3.45.
Section headings are consumed IN SUTRA ORDER (1.1..3.45 exactly once each);
same-ref lines elsewhere (e.g. the 2.1-2.10 recap inside 2.10) stay content.
Post-boundary material (after a trailer/label/header) attaches FORWARD to
the next sutra. Appendix (condensed re-reading) is reference only, except
the 4-line colophon which closes s77. Ref: shiva/SHIVA-INTAKE.md.
"""
import re, os

SRC = os.path.expanduser('~/tantrasara/shivasutrasfinal')
OUT = os.path.expanduser('~/tantrasara/shiva/chapters')

BOOK_LINE = {
    1: 'BOOK I — ŚĀMBHAVOPĀYA',   # source line 8 verbatim
    2: 'BOOK II — ŚĀKTOPĀYA',     # appendix line verbatim (no header in flow)
    3: 'BOOK III — ĀṆAVOPĀYA',    # source line 3486 verbatim
}
TITLE_LINE = 'शिवसूत्राणि — THE ŚIVA SŪTRAS'

DROP_PATTERNS = [
    r'^(Gmail|Skip to content|Using Gmail|.*screen readers|.*browser version|Inbox|Summarize|Prior Trades|To:|\(no subject\)|1 of \d+|^As$)',
    r'2 November 2026 at \d+:\d+',
    r'^Source Library \+\d+$',
    r'Attachment',
    r'^Continue Book .*$',
    r'^End of Book .*$',
    r'^Book III, Part .*$',
    r'^Part (I|II|III) — Sūtras .*$',
    r'^Welcome back to Kashmir\.$',
]

APPENDIX_BOOK = 'BOOK I — ŚĀMBHAVOPĀYA'  # 2nd occurrence ends the chapters
COLOPHON = ['॥ शिवम् ॥', 'Iti śivam.',
            'Thus, Śiva. Thus, the auspicious conclusion.',
            'End of the Śiva Sūtras — all 77 sūtras completed.']

EXPECTED = ([f'1.{i}' for i in range(1, 23)] + [f'2.{i}' for i in range(1, 11)]
            + [f'3.{i}' for i in range(1, 46)])


def is_drop(s):
    return any(re.match(p, s) for p in DROP_PATTERNS)


def clean(lines):
    out = []
    for l in lines:
        s = l.rstrip('\n').replace('⁠', '')
        if is_drop(s.strip()):
            continue
        s = re.sub(r'\s+[a-z0-9_.-]+\.[a-z]+ \+1$', '', s)
        s = re.sub(r'\s+(?:Source Library|Sanskrit Documents|Sanskrit & Trika Shaivism) \+\d+$', '', s)
        out.append(s)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def main():
    lines = open(SRC, encoding='utf-8').read().splitlines()
    seen_book1 = False
    appx = None
    for i, l in enumerate(lines):
        if l.strip() == APPENDIX_BOOK:
            if seen_book1:
                appx = i
                break
            seen_book1 = True
    assert appx is not None, 'appendix start not found'
    body = lines[:appx]
    for c in COLOPHON:
        assert any(c == l.strip().replace('⁠', '') for l in lines[appx:]), f'colophon missing: {c}'

    order = list(EXPECTED)
    files, cur_ref, cur_lines, fwd_lines, in_fwd = {}, None, [], [], False
    pi = 0
    books_seen = set()
    for l in body:
        s = l.rstrip('\n')
        m = re.match(r'^(\d\.\d+)\s*—\s*(.+)$', s)
        if m and pi < len(order) and m.group(1) == order[pi]:
            if cur_ref is not None:
                files[cur_ref] = (cur_lines, fwd_lines)
            elif cur_lines or fwd_lines:
                files['__intro__'] = (cur_lines, fwd_lines)
            cur_ref = order[pi]
            pi += 1
            cur_lines, fwd_lines, in_fwd = [l], [], False
            continue
        t = s.replace('⁠', '')
        if is_drop(t.strip()):
            in_fwd = True
            continue
        # title repeat / book subtitles are header material past the intro
        if cur_ref is not None and (t.strip() == TITLE_LINE or t.strip().startswith('The Way of ')
                                    or t.strip().startswith('Part I ')):
            in_fwd = True
            continue
        if t.strip() in (BOOK_LINE[1], BOOK_LINE[3]):
            if t.strip() in books_seen:
                in_fwd = True  # bare repeat: boundary, following attaches forward
                continue
            books_seen.add(t.strip())
            (fwd_lines if in_fwd else cur_lines).append('## ' + t.strip())
            continue
        (fwd_lines if in_fwd else cur_lines).append(l)
    if cur_ref is not None:
        files[cur_ref] = (cur_lines, fwd_lines)
    assert pi == len(order), f'consumed {pi}/77 sutras'
    assert set(r for r in files if r != '__intro__') == set(order), 'ref mismatch'

    os.makedirs(OUT, exist_ok=True)
    # s00: series intro (H1 is the verbatim source title line)
    intro_cur, intro_fwd = files.get('__intro__', ([], []))
    intro_lines = [l for l in (intro_cur + intro_fwd)
                   if l.strip() != BOOK_LINE[1] and not l.startswith('## ')
                   and l.strip() != TITLE_LINE]
    with open(f'{OUT}/s00.md', 'w', encoding='utf-8') as f:
        f.write('# ' + TITLE_LINE + '\n\n' + '\n'.join(clean(intro_lines)) + '\n')
    print(f's00: series intro')

    book_of = {}
    for i, r in enumerate(order):
        book_of[r] = 1 if i < 22 else (2 if i < 32 else 3)
    for i, ref in enumerate(order):
        sid = f's{i + 1:02d}'
        cur_lines, _fwd = files[ref]
        prev_ref = order[i - 1] if i > 0 else None
        prev_fwd = files[prev_ref][1] if prev_ref else []
        parts = [f'# Śiva Sūtras {ref}']
        bk = BOOK_LINE[book_of[ref]]
        if (i == 0 or book_of[ref] != book_of[order[i - 1]]
                or ref == '2.1') and not any(x.startswith('## BOOK') for x in prev_fwd):
            parts.append('## ' + bk)
        body = clean(cur_lines + prev_fwd)
        headed = []
        for ln in body:
            headed.append(ln)
            if re.match(r'^\d\.\d+\s*—', ln):
                headed.append('')
        parts += headed
        if ref == '3.45':
            parts += [''] + COLOPHON
        with open(f'{OUT}/{sid}.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(parts) + '\n')
    print(f's01..s77 written ({len(order)} sutra chapters + s00)')


if __name__ == '__main__':
    main()
