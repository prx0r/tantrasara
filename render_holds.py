#!/usr/bin/env python3
"""Full hold-card set in locked house style + contact sheet.
Usage: python3 render_holds.py <storyboard.json> <outdir>
Style law (matches kashmir_audio noen cards exactly):
- Sanskrit terms: Devanagari 84 (Tiro) + IAST 40 italic, gap 40, centered
  rows, maxw 1600. IAST transliterated to Deva for the top line.
- Titles/thesis: Cormorant Medium 96/84 ink, centered, no kickers.
- Figures: numeral 150 + label 44.
- Subtitle: FE 46, top y=860 (safe zone 800-980), ink/lit demo state.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860

def F(p, s):
    from PIL import ImageFont as I
    return I.truetype(p, s)

try:
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    def to_deva(s):
        return transliterate(s, IAST, DEVANAGARI)
    def to_iast(s):
        return transliterate(s, DEVANAGARI, IAST)
except Exception:
    def to_deva(s):
        return s
    def to_iast(s):
        return s

def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)

def fit_font(draw, text, path, start, min_sz, maxw=1750):
    size = start
    while size > min_sz and draw.textlength(text, font=F(path, size)) > maxw:
        size -= 4
    return F(path, size), size

def ct_fit(d, y, s, path, start, min_sz=48, fill=INK):
    fnt, sz = fit_font(d, s, path, start, min_sz)
    assert d.textlength(s, font=fnt) <= 1780, f'too wide even at {min_sz}: {s[:60]}'
    ct(d, y, s, fnt, fill)
    return fnt

def Fail(s):
    return None

def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    # holds (term groups chunked to max 3 pairs so the stack + subtitle
    # never collide; bounds asserted per card, fail loudly like make_card)
    def npairs(b):
        return sum(1 for ln in b['text'].strip().splitlines() if ln.strip())
    MAX_PAIRS = 3
    holds = []
    cur, cur_pairs = None, 0
    for b in sb['blocks']:
        if b['id'] == 'b_opener':
            holds.append([b]); continue
        if b['type'] == 'verse':
            if cur is None:
                cur, cur_pairs = [], 0
            if cur_pairs + npairs(b) > MAX_PAIRS:
                holds.append(cur); cur, cur_pairs = [], 0
            cur.append(b)
            cur_pairs += npairs(b)
            if cur_pairs >= MAX_PAIRS:
                holds.append(cur); cur, cur_pairs = None, 0
        else:
            if cur: holds.append(cur); cur, cur_pairs = None, 0
            if b['type'] in ('title', 'figure'):
                holds.append([b])
    if cur: holds.append(cur)
    # subtitle = first narration/dialogue line after hold end
    flat = sb['blocks']
    idx = {b['id']: i for i, b in enumerate(flat)}
    files = []
    ch_title = next((b['text'] for b in sb['blocks'] if b['type'] == 'title'), 'Tantrasara')
    ch_title = re.sub(r'^\d+\.\s*', '', ch_title)
    for hi, h in enumerate(holds):
        im = Image.new('RGB', (W, H), LIGHT)
        d = ImageDraw.Draw(im)
        first = h[0]
        bottom = 700  # default stack bottom for opener/title/figure
        if first['id'] == 'b_opener':
            ct_fit(d, 430, ch_title, FE, 96)
        elif first['type'] == 'title':
            t = first['text']
            t = re.sub(r'^\d+\.\s*', '', t)
            ct_fit(d, 430, t, FE, 96)
        elif first['type'] == 'figure':
            t = first['text']
            m = re.match(r'^#?\s*(\d+)\s*(.*)$', t)
            if m and len(t) < 40:
                ct(d, 360, m.group(1), F(FE, 150))
                if m.group(2).strip():
                    ct(d, 580, m.group(2).strip(), F(FE, 44))
            else:
                ct_fit(d, 430, t, FE, 72)
        else:  # term card(s): Deva lines only (no romanisation), wrapped to <=2 at >=64
            raw = []
            for b in h:
                for ln in b['text'].strip().splitlines():
                    s = ln.strip().rstrip('.')
                    if s:
                        raw.append(s)
            dl = []  # (deva_lines[], roman, size)
            for s in raw:
                try:
                    deva = to_deva(s)
                    roman = to_iast(deva)
                except Exception:
                    deva, roman = s, s
                if d.textlength(deva, font=F(FD, 84)) <= 1700:
                    dl.append(([deva], roman, 84))
                    continue
                # wrap near the middle into 2 Deva lines at 64
                wl = deva.split()
                tot = sum(len(w) for w in wl)
                acc, bi = 0, 0
                for i, w_ in enumerate(wl[:-1]):
                    acc += len(w_) + 1
                    if abs(acc - tot / 2) < abs(sum(len(x) + 1 for x in wl[:bi + 1]) - tot / 2):
                        bi = i
                dl.append(([' '.join(wl[:bi + 1]), ' '.join(wl[bi + 1:])], roman, 64))
            lh = lambda sz: int(sz * 1.35)
            total = sum(lh(sz) * len(lines) + 26 for lines, _, sz in dl) - 26
            y = max(90, 540 - total // 2 - 40)
            bottom = y
            for lines, roman, sz in dl:
                fnt = F(FD, sz)
                for ln in lines:
                    ct(d, y, ln, fnt)
                    y += lh(sz)
                y += 26
            bottom = y
            assert bottom + 30 < SUB_Y, f'stack hits subtitle (bottom={bottom})'
        # subtitle: next spoken line after hold, wrapped to <=2 lines
        last_id = h[-1]['id']
        sub = ''
        for b in flat[idx[last_id] + 1:idx[last_id] + 6]:
            if b.get('type') in ('narration', 'dialogue') and b.get('voice') in ('granny', 'man'):
                sub = b['text'][:140]
                break
        sub_lines, fnt = [], F(FE, 46)
        if sub:
            words, cur_ln = sub.split(), ''
            for w_ in words:
                t = (cur_ln + ' ' + w_).strip()
                if d.textlength(t, font=fnt) > 1750 and cur_ln:
                    sub_lines.append(cur_ln); cur_ln = w_
                else:
                    cur_ln = t
            if cur_ln: sub_lines.append(cur_ln)
            if len(sub_lines) > 2:
                fnt = F(FE, 40)
                sub_lines, cur_ln = [], ''
                for w_ in sub.split():
                    t = (cur_ln + ' ' + w_).strip()
                    if d.textlength(t, font=fnt) > 1750 and cur_ln:
                        sub_lines.append(cur_ln); cur_ln = w_
                    else:
                        cur_ln = t
                if cur_ln: sub_lines.append(cur_ln)
            assert len(sub_lines) <= 3, f'subtitle still too long: {sub[:60]}'
        # bounds: stack must clear subtitle zone, everything inside frame
        if sub_lines:
            assert bottom + 30 < SUB_Y, f'stack hits subtitle (bottom={bottom})'
            assert SUB_Y + len(sub_lines) * 62 < H - 20, 'subtitle hits frame edge'
        for i, ln in enumerate(sub_lines):
            d.text(((W - d.textlength(ln, font=fnt)) / 2, SUB_Y + i * 62), ln, font=fnt, fill=INK)
        fn = f'{out}/hold{hi:03d}.png'
        im.save(fn)
        files.append(fn)
    print(f'rendered {len(files)} holds')
    # contact sheet
    cols, cw, chh = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new('RGB', (cw * cols, rows * chh + 40), (245, 243, 238))
    sd = ImageDraw.Draw(sheet)
    sd.text((16, 8), f'Tantrasara ch6 — {len(files)} holds, house style (SUB_Y={SUB_Y})',
            font=F(FE, 22), fill=INK)
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).resize((cw, chh)), ((i % cols) * cw, 40 + (i // cols) * chh))
    sheet.save(f'{out}/contact_sheet.png')
    print('sheet:', f'{out}/contact_sheet.png')

if __name__ == '__main__':
    main()
