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
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
MAX_PAIRS = 3


def F(p, size):
    return ImageFont.truetype(p, size)


def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)


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


def to_deva(s):
    import re as _re
    if _re.search(r'[\u0900-\u097F]', s):
        return s  # already Devanagari
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return transliterate(s, IAST, DEVANAGARI)


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
    """Render one hold card. glossary: {folded_term: {'gloss': ...}} —
    matched terms get their English gloss in grey beneath the Devanagari.
    (Contact sheets show proposed glosses for review; video gates on
    confirmed status separately.)"""
    """Render one hold card. sub_text: optional single-line subtitle (ink)."""
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
    else:  # verse: Deva lines + English gloss in grey (no romanisation)
        import unicodedata
        fold = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
        raw = []
        for b in hold:
            for ln in b['text'].strip().splitlines():
                s = ln.strip().rstrip('.')
                if s:
                    raw.append(s)
        dl = []
        for s in raw:
            try:
                deva = to_deva(s)
            except Exception:
                deva = s
            gloss = (glossary or {}).get(fold(s.strip('.,!?')), '')
            if isinstance(gloss, dict):
                gloss = gloss.get('gloss', '')
            if d.textlength(deva, font=F(FD, 84)) <= 1700:
                dl.append(([deva], gloss, 84))
            else:
                # greedy wrap at 64 (Sanskrit compounds can need 3+ lines)
                f64 = F(FD, 64)
                parts, cur = [], ''
                for w_ in deva.split():
                    t = (cur + ' ' + w_).strip()
                    if d.textlength(t, font=f64) > 1700 and cur:
                        parts.append(cur)
                        cur = w_
                    else:
                        cur = t
                if cur:
                    parts.append(cur)
                for ln in parts:
                    assert d.textlength(ln, font=f64) <= 1780, f'verse overflow: {ln[:40]}'
                dl.append((parts, gloss, 64))
        lh = lambda sz: int(sz * 1.35)
        total = sum(lh(sz) * len(lines) + (45 if gloss else 0) + 26 for lines, gloss, sz in dl) - 26
        y = max(90, 540 - total // 2 - 40)
        for lines, gloss, sz in dl:
            fnt = F(FD, sz)
            for ln in lines:
                assert d.textlength(ln, font=fnt) <= 1780, f'verse overflow: {ln[:40]}'
                d.text(((W - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=INK)
                y += lh(sz)
            if gloss:
                ct(d, y, gloss, F(FR, 40), FADE)
                y += 45
            y += 26
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
