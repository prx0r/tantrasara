#!/usr/bin/env python3
"""Shared hold-card logic: storyboard blocks -> holds -> rendered cards.
One implementation used by render_holds.py (contact sheets) and build_clip.py
(video). Verse cards are Devanagari ONLY (no romanisation, owner call).
Narration with no anchor hold shows a clean blank card.
"""
import re
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
ROMAN_FILL = (221, 215, 203)   # IAST — lightest, closest to the Sanskrit
LIT_FILL = (188, 180, 165)     # intermediary literal — a step closer
FINAL_FILL = (105, 99, 86)     # final English — closest our English gets
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
MAX_PAIRS = 3


def F(p, size):
    return ImageFont.truetype(p, size)


def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)


def chapter_title(blocks, glossary=None):
    """Canonical title source: first granny narration block carrying
    Devanagari (the chapter-name line). Display Deva is the prakāśana
    name (roman half transliterated) so every chapter titles by name,
    not by ordinal — ch02's Deva already is the name, others normalize
    to it. Lookup key follows the display Deva. Layers from the glossary
    entry when present — Deva+IAST minimum, always."""
    import unicodedata
    for b in blocks:
        if b.get('id') == 'b_opener':
            continue
        if b.get('type') != 'narration' or b.get('voice') != 'granny':
            continue
        deva_part, roman_part = split_scripts(b['text'])
        if not deva_part:
            continue
        try:
            name_deva = to_deva(roman_part) if roman_part else deva_part
        except Exception:
            name_deva = deva_part
        v = (glossary or {}).get(verse_match_key(name_deva), '')
        literal = final = ''
        if isinstance(v, dict):
            literal, final = v.get('literal', ''), v.get('gloss', '')
            if isinstance(final, dict):
                final = final.get('gloss', '')
        try:
            iast = to_iast(name_deva)
        except Exception:
            iast = roman_part
        return {'deva': name_deva, 'iast': iast, 'literal': literal,
                'final': final if isinstance(final, str) else ''}
    return None


def intro_hold(ch, title=None):
    """Intro bug shared by sheets and video: per-chapter thumbnail fitted
    above the subtitle zone; ch02+ carry the chapter numeral top-right plus
    the canonical title stack beneath it (Deva 84 + IAST/literal/final in
    corner sizes, right-aligned, clearing the mandala). ch01 blessed
    reference: thumbnail alone, never touched. Returns None when no
    thumbnail art exists -- caller falls back to first verse hold."""
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    tb = os.path.join(base, 'assets', 'thumbnail', 'ch' + ch + '.png')
    if not os.path.exists(tb):
        tb = os.path.join(base, 'assets', 'thumb_ch1.png')  # legacy fallback
    if not os.path.exists(tb):
        return None
    _tb = Image.open(tb).convert('RGB')
    _tb.thumbnail((1400, 730), Image.LANCZOS)
    im = Image.new('RGB', (W, H), LIGHT)
    im.paste(_tb, ((W - _tb.width) // 2, 50))
    # mandala clearance, measured from the art itself before any ink lands:
    # saturated pixels only (the paste rect is white-margined). Each ink
    # box is checked against the art rows it actually occupies.
    from PIL import ImageChops
    _sat = im.crop((0, 0, W, H)).convert('HSV').split()[1]
    _mask = _sat.point(lambda v: 255 if v > 30 else 0)
    if ch != '01':
        d = ImageDraw.Draw(im)
        fnt = F(FE, 150)
        num = ch.zfill(2)
        d.text((W - 120 - d.textlength(num, font=fnt), 60), num, font=fnt, fill=INK)
        if title:
            # canonical header: title top-left, numeral top-right, same
            # baseline (y=60). Deva 84 at x=120, every layer centered under
            # the Sanskrit; mandala clearance asserted on the left.
            y = 60
            dlines = [title['deva']]
            df = F(FD, 84)
            if d.textlength(title['deva'], font=df) > 520:
                df = F(FD, 64)
                parts, cur = [], ''
                for w_ in title['deva'].split():
                    t = (cur + ' ' + w_).strip()
                    if d.textlength(t, font=df) > 520 and cur:
                        parts.append(cur)
                        cur = w_
                    else:
                        cur = t
                if cur:
                    parts.append(cur)
                dlines = parts
            boxes = []
            cx = 120 + max(d.textlength(ln, font=df) for ln in dlines) / 2
            for ln in dlines:
                d.text((120, y), ln, font=df, fill=INK)
                boxes.append((120, y, 120 + d.textlength(ln, font=df),
                              y + int(df.size * 1.35)))
                y += int(df.size * 1.35)
            engw = max(d.textlength(ln, font=df) for ln in dlines)
            for txt, fp, fsz, fill in ((title.get('iast', ''), FE, 28, ROMAN_FILL),
                                      (title.get('literal', ''), FR, 24, LIT_FILL),
                                      (title.get('final', ''), FR, 36, FINAL_FILL)):
                if not txt:
                    continue
                gf = F(fp, fsz)
                for gln in wrap_lines(d, txt, gf, engw):
                    lx = cx - d.textlength(gln, font=gf) / 2
                    d.text((lx, y), gln, font=gf, fill=fill)
                    boxes.append((lx, y, lx + d.textlength(gln, font=gf),
                                  y + int(fsz * 1.35)))
                    y += int(fsz * 1.35)
            # mandala clearance, measured from the art itself: leftmost
            # non-white pixel over the title band rows is the hard bound.
            for (x0, y0, x1, y1) in boxes:
                assert y1 <= SUB_Y, 'title stack collides with subtitle zone'
                if y0 < 780:
                    _rows = _mask.crop((0, max(0, int(y0)), W, min(H, int(y1) + 1)))
                    _bb = _rows.getbbox()
                    if _bb is not None:
                        assert x1 <= _bb[0], f'title ink over the mandala ({x1:.0f} vs art {_bb[0]})'
    return im


def build_holds(blocks):
    """Group verse blocks (max 3 Deva lines per hold); titles/figures solo."""
    def npairs(b):
        return sum(1 for ln in b['text'].strip().splitlines() if ln.strip())
    holds, cur, cur_n = [], None, 0
    for b in blocks:
        if b['id'] == 'b_opener':
            holds.append([b])
            continue
        if b['type'] == 'verse':
            if cur is None:
                cur, cur_n = [], 0
            if cur and cur_n + npairs(b) > MAX_PAIRS:
                holds.append(cur)
                cur, cur_n = [], 0
            cur.append(b)
            cur_n += npairs(b)
            if cur_n >= MAX_PAIRS:
                holds.append(cur)
                cur, cur_n = None, 0
        else:
            if cur:
                holds.append(cur)
                cur, cur_n = None, 0
            if b['type'] in ('title', 'figure'):
                holds.append([b])
    if cur:
        holds.append(cur)
    return holds


# List screen engine: count decides the shape, positions never move, one
# standard Sanskrit size everywhere (Deva 84 + grey gloss 40 — locked
# 2026-11-04, owner call). 1 centered · 2 side by side · 3 in a row when
# they fit, else triangle (apex + two below) · 4 the corners · 5 corners
# plus middle (newest middle, earlier four in arrival order). Past five
# the window slides and the oldest drops off. Subtitles own y=860 alone.
POS_MIDDLE = {'kind': 'middle', 'y': 400, 'maxw': 1750}
POS_CORNERS = [
    {'kind': 'top-left', 'cx': 510, 'y': 90, 'maxw': 780},
    {'kind': 'top-right', 'cx': 1410, 'y': 90, 'maxw': 780},
    {'kind': 'bottom-left', 'cx': 510, 'y': 620, 'maxw': 780},
    {'kind': 'bottom-right', 'cx': 1410, 'y': 620, 'maxw': 780},
]
POS_PAIR = [{'cx': 560, 'y': 430, 'maxw': 780},
            {'cx': 1360, 'y': 430, 'maxw': 780}]
POS_ROW3 = [{'cx': 400, 'y': 430, 'maxw': 560},
            {'cx': 960, 'y': 430, 'maxw': 560},
            {'cx': 1520, 'y': 430, 'maxw': 560}]
POS_TRI = [{'cx': 960, 'y': 150, 'maxw': 800},
           {'cx': 480, 'y': 520, 'maxw': 640},
           {'cx': 1440, 'y': 520, 'maxw': 640}]
POS_WINDOW = 5  # middle + four corners; longer lists slide the window


def render_list(keys, glossary):
    """Count decides the shape. 1 centered, 2 side by side, 3 row-or-triangle,
    4 corners, 5 corners + middle. Window slides past five."""
    import unicodedata
    im = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    boxes = []

    def _item(k):
        # display layers from the glossary entry: citation Deva (never the
        # folded key — folding destroys ś/ṣ/ṇ), IAST derived from the Deva,
        # T1-style literal, final gloss. Missing layers render nothing.
        # Gating lives in the glossary dict each caller passes (sheets pass
        # proposed for review; video passes confirmed only).
        v = (glossary or {}).get(k, '')
        if isinstance(v, dict):
            deva = v.get('deva') or to_deva(k)
            gloss = v.get('gloss', '')
            literal = v.get('literal', '')
            if isinstance(gloss, dict):
                gloss = gloss.get('gloss', '')
        else:
            deva, gloss, literal = to_deva(k), (v or ''), ''
        try:
            iast = to_iast(deva)
        except Exception:
            iast = ''
        return deva, iast, literal, gloss

    def _col(cx, y, deva, iast, literal, gloss, maxw,
             DSZ=84, ISZ=32, LSZ=28, FSZ=40):
        # centered column: every layer centered under the Sanskrit above it.
        # Deva steps one size down if it cannot fit the column (verse rule);
        # anything still wider fails loud (owner restyles, never ships tofu).
        sz = DSZ
        lines = wrap_lines(d, deva, F(FD, sz), maxw) or [deva]
        if max(d.textlength(ln, font=F(FD, sz)) for ln in lines) > maxw:
            sz = 64
            raw = wrap_lines(d, deva, F(FD, sz), maxw) or [deva]
            lines = []
            for ln in raw:
                lines.extend(wrap_lines(d, ln, F(FD, sz), maxw) or [ln])
        w = max(d.textlength(ln, font=F(FD, sz)) for ln in lines)
        assert w <= maxw + 2, f'column overflow ({w:.0f}px > {maxw}px) — split or restyle the list'
        x = cx - w / 2
        for ln in lines:
            lx = cx - d.textlength(ln, font=F(FD, sz)) / 2
            d.text((lx, y), ln, font=F(FD, sz), fill=INK)
            y += int(sz * 1.35)
        boxes.append((x, y - sum(int(sz * 1.35) for _ in lines), x + w, y))
        for txt, fp, fsz, fill in ((iast, FE, ISZ, ROMAN_FILL),
                                  (literal, FR, LSZ, LIT_FILL),
                                  (gloss, FR, FSZ, FINAL_FILL)):
            if not txt:
                continue
            for gln in wrap_lines(d, txt, F(fp, fsz), maxw):
                lx = cx - d.textlength(gln, font=F(fp, fsz)) / 2
                d.text((lx, y), gln, font=F(fp, fsz), fill=fill)
                boxes.append((lx, y, lx + d.textlength(gln, font=F(fp, fsz)),
                              y + int(fsz * 1.35)))
                y += int(fsz * 1.35)
        return y

    def _fits_row(items):
        return all(d.textlength(deva, font=F(FD, 84)) <= 560
                   and all(not t or d.textlength(t, font=F(FD if f == FE else FR, s)) <= 560
                           for t, f, s in ((iast, FE, 32), (literal, FR, 28), (gloss, FR, 40)))
                   for deva, iast, literal, gloss in items)

    window = keys[-POS_WINDOW:]
    items = [_item(k) for k in window]
    n = len(items)
    if n == 1:
        _col(W / 2, 380, *items[0], 1750)
    elif n == 2:
        for item, slot in zip(items, POS_PAIR):
            _col(slot['cx'], slot['y'], *item, slot['maxw'])
    elif n == 3:
        slots = POS_ROW3 if _fits_row(items) else POS_TRI
        for item, slot in zip(items, slots):
            _col(slot['cx'], slot['y'], *item, slot['maxw'])
    elif n == 4:
        for item, slot in zip(items, POS_CORNERS):
            _col(slot['cx'], slot['y'], *item, slot['maxw'],
                 84, 28, 24, 36)
    else:
        for item, slot in zip(items[:-1], POS_CORNERS):
            _col(slot['cx'], slot['y'], *item, slot['maxw'],
                 84, 28, 24, 36)
        _col(W / 2, POS_MIDDLE['y'], *items[-1], POS_MIDDLE['maxw'],
             84, 32, 28, 40)
    for (x0, y0, x1, y1) in boxes:
        assert y1 <= SUB_Y, 'conveyor collides with subtitle zone'
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            overlap = a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
            assert not overlap, 'conveyor slots overlap — split or restyle the list'
    return im


def to_deva(s):
    import re as _re
    if _re.search(r'[\u0900-\u097F]', s):
        return s  # already Devanagari
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return transliterate(s, IAST, DEVANAGARI)


def split_scripts(t):
    """Devanagari tokens vs roman tokens — never mix scripts on one line
    (M4, promoted from the pilot builder to shared law)."""
    deva, roman = [], []
    for w in t.strip().split():
        c = w.strip('—.,!?;:')
        if not c:
            continue
        (deva if any('\u0900' <= ch <= '\u097f' for ch in c) else roman).append(w.strip('—.,!?;:'))
    return ' '.join(deva), ' '.join(roman)


def to_iast(s):
    import re as _re
    if not _re.search(r'[\u0900-\u097F]', s):
        return s  # already roman
    from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST
    return transliterate(s, DEVANAGARI, IAST)


def verse_match_key(devanagari_text):
    """Canonical key for a verse block: IAST, folded, alphanumeric only.
    Deterministic across storyboard rebuilds (no positional overrides)."""
    import re as _re, unicodedata
    s = _re.sub(r'\s+', ' ', devanagari_text.strip())
    try:
        s = to_iast(s)
    except Exception:
        pass
    return _re.sub(r'[^a-z]', '', ''.join(
        c for c in unicodedata.normalize('NFD', s.lower())
        if unicodedata.category(c) != 'Mn'))


def render_term_card(deva, iast, literal, final, DSZ=84, ISZ=32, LSZ=28,
                     FSZ=40):
    """Single centered four-layer term card. Returns the image."""
    im = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    boxes = []
    lines = wrap_lines(d, deva, F(FD, DSZ), 1750) or [deva]
    total = (sum(int(DSZ * 1.35) for _ in lines)
             + (sum(int(ISZ * 1.35) for _ in wrap_lines(d, iast, F(FE, ISZ), 1750)) if iast else 0)
             + (sum(int(LSZ * 1.35) for _ in wrap_lines(d, literal, F(FR, LSZ), 1750)) if literal else 0)
             + (sum(int(FSZ * 1.35) for _ in wrap_lines(d, final, F(FR, FSZ), 1750)) if final else 0))
    y = max(90, 540 - total // 2 - 40)
    for ln in lines:
        lx = (W - d.textlength(ln, font=F(FD, DSZ))) / 2
        d.text((lx, y), ln, font=F(FD, DSZ), fill=INK)
        boxes.append((lx, y, lx + d.textlength(ln, font=F(FD, DSZ)),
                      y + int(DSZ * 1.35)))
        y += int(DSZ * 1.35)
    for txt, fp, fsz, fill in ((iast, FE, ISZ, ROMAN_FILL),
                              (literal, FR, LSZ, LIT_FILL),
                              (final, FR, FSZ, FINAL_FILL)):
        if not txt:
            continue
        for gln in wrap_lines(d, txt, F(fp, fsz), 1750):
            lx = (W - d.textlength(gln, font=F(fp, fsz))) / 2
            d.text((lx, y), gln, font=F(fp, fsz), fill=fill)
            boxes.append((lx, y, lx + d.textlength(gln, font=F(fp, fsz)),
                          y + int(fsz * 1.35)))
            y += int(fsz * 1.35)
    for (x0, y0, x1, y1) in boxes:
        assert y1 <= SUB_Y, 'term card collides with subtitle zone'
    return im


def wrap_lines(draw, text, font, maxw=1750):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def render_hold(hold, sub_text=None, glossary=None):
    """Verse cards: Deva + IAST per line; single-word glossed chants resolve
    via glossary to the full four term layers. Callers gate: sheets pass
    proposed for review, video passes confirmed only."""
    first = hold[0]
    im = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    kind = 'opener' if first['id'] == 'b_opener' else first['type']
    if kind == 'opener':
        pass  # clean card under the bell
    elif kind == 'title':
        t = re.sub(r'^\d+\.\s*', '', first['text'])
        fnt = F(FE, 96)
        while d.textlength(t, font=fnt) > 1750 and fnt.size > 40:
            fnt = F(FE, fnt.size - 4)
        ct(d, 430, t, fnt)
    elif kind == 'figure':
        t = first['text']
        m = re.match(r'^#?\s*(\d+)\s*(.*)$', t)
        if m and len(t) < 40:
            ct(d, 360, m.group(1), F(FE, 150))
            if m.group(2).strip():
                ct(d, 580, m.group(2).strip(), F(FE, 44))
        else:
            fnt = F(FE, 72)
            while d.textlength(t, font=fnt) > 1750 and fnt.size > 40:
                fnt = F(FE, fnt.size - 4)
            ct(d, 430, t, fnt)
    else:  # verse: Deva + IAST + T1 literal + L4-or-L3 final, grey ramp down
        import unicodedata
        fold = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
        dl = []
        for b in hold:
            lines = [ln.strip().rstrip('.') for ln in b['text'].strip().splitlines()]
            lines = [s for s in lines if s]
            if not lines:
                continue
            # per-line: term singles via glossary, else Deva + IAST.
            # Mixed-script lines split first (M4): the author's own roman
            # half is the IAST line, never a transliteration duplicate.
            for s in lines:
                deva_part, roman_part = split_scripts(s)
                v = (glossary or {}).get(fold(s.strip('.,!?')), '')
                if isinstance(v, dict) and (v.get('deva') or v.get('gloss') or v.get('literal')):
                    deva = v.get('deva') or to_deva(deva_part or s)
                    gloss = v.get('gloss', '')
                    literal = v.get('literal', '')
                    if isinstance(gloss, dict):
                        gloss = gloss.get('gloss', '')
                else:
                    try:
                        deva = to_deva(deva_part or s)
                    except Exception:
                        deva = deva_part or s
                    gloss = (v or '') if isinstance(v, str) else ''
                    literal = ''
                if roman_part and not gloss and not literal:
                    iast = roman_part
                else:
                    try:
                        iast = to_iast(deva)
                    except Exception:
                        iast = ''
                if d.textlength(deva, font=F(FD, 84)) <= 1700:
                    dl.append({'deva': [(deva, 84)] if deva.strip() else [], 'iast': [iast] if iast else [],
                               'literal': [literal] if literal else [], 'final': [gloss] if gloss else []})
                    continue
                fsmall = F(FD, 64)
                parts, cur = [], ''
                for w_ in deva.split():
                    t = (cur + ' ' + w_).strip()
                    if d.textlength(t, font=fsmall) > 1700 and cur:
                        parts.append(cur)
                        cur = w_
                    else:
                        cur = t
                if cur:
                    parts.append(cur)
                for ln in parts:
                    assert d.textlength(ln, font=fsmall) <= 1780, f'verse overflow: {ln[:40]}'
                dl.append({'deva': [(ln, 64) for ln in parts] if deva.strip() else [], 'iast': [iast] if iast else [],
                           'literal': [literal] if literal else [], 'final': [gloss] if gloss else []})
        lh = lambda sz: int(sz * 1.35)
        total = 0
        for e in dl:
            for _, sz in e['deva']:
                total += lh(sz)
            for _ln in e['iast']:
                total += sum(lh(32) for _ in wrap_lines(d, _ln, F(FE, 32), 1750) or [0])
            for _ln in e['literal']:
                total += sum(lh(28) for _ in wrap_lines(d, _ln, F(FR, 28), 1750) or [0])
            for _ln in e['final']:
                total += sum(lh(40) for _ in wrap_lines(d, _ln, F(FR, 40), 1750) or [0])
            total += 26
        total -= 26
        y = max(90, 540 - total // 2 - 40)
        for e in dl:
            for ln, sz in e['deva']:
                fnt = F(FD, sz)
                assert d.textlength(ln, font=fnt) <= 1780, f'verse overflow: {ln[:40]}'
                d.text(((W - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=INK)
                y += lh(sz)
            for txts, fp, fsz, fill in ((e['iast'], FE, 32, ROMAN_FILL),
                                       (e['literal'], FR, 28, LIT_FILL),
                                       (e['final'], FR, 40, FINAL_FILL)):
                for t0 in txts:
                    if not t0:
                        continue
                    for gln in wrap_lines(d, t0, F(fp, fsz), 1750):
                        lx = (W - d.textlength(gln, font=F(fp, fsz))) / 2
                        d.text((lx, y), gln, font=F(fp, fsz), fill=fill)
                        y += lh(fsz)
            y += 26
        assert y - 26 <= SUB_Y, 'card collides with subtitle zone — split the stack'
    if sub_text:
        fnt = F(FE, 46)
        wrapped = wrap_lines(d, sub_text, fnt)
        if len(wrapped) > 2:
            fnt = F(FE, 40)
            wrapped = wrap_lines(d, sub_text, fnt)
        assert len(wrapped) <= 2, 'subtitle too long'
        for i, ln in enumerate(wrapped):
            d.text(((W - d.textlength(ln, font=fnt)) / 2, SUB_Y + i * 62), ln, font=fnt, fill=INK)
    return im
