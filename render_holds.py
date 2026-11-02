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
    from indic_transliteration import sanscript
    def to_deva(s):
        return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)
except Exception:
    def to_deva(s):
        return s

def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)

def Fail(s):
    return None

def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    # holds (term groups chunked to max 3 pairs so the stack + subtitle
    # never collide; bounds asserted per card, fail loudly like make_card)
    MAX_PAIRS = 3
    holds = []
    cur = None
    for b in sb['blocks']:
        if b['id'] == 'b_opener':
            holds.append([b]); continue
        if b['type'] == 'verse':
            if cur is None: cur = []
            cur.append(b)
            if len(cur) >= MAX_PAIRS:
                holds.append(cur); cur = None
        else:
            if cur: holds.append(cur); cur = None
            if b['type'] in ('title', 'figure'):
                holds.append([b])
    if cur: holds.append(cur)
    # subtitle = first narration/dialogue line after hold end
    flat = sb['blocks']
    idx = {b['id']: i for i, b in enumerate(flat)}
    files = []
    for hi, h in enumerate(holds):
        im = Image.new('RGB', (W, H), LIGHT)
        d = ImageDraw.Draw(im)
        first = h[0]
        bottom = 700  # default stack bottom for opener/title/figure
        if first['id'] == 'b_opener':
            ct(d, 430, 'Chapter Six', F(FE, 96))
            ct(d, 560, 'Kālādhva — the Path of Time', F(FR, 48), FADE)
        elif first['type'] == 'title':
            t = first['text']
            t = re.sub(r'^\d+\.\s*', '', t)
            ct(d, 430, t, F(FE, 96))
        elif first['type'] == 'figure':
            t = first['text']
            m = re.match(r'^#?\s*(\d+)\s*(.*)$', t)
            if m and len(t) < 40:
                ct(d, 360, m.group(1), F(FE, 150))
                if m.group(2).strip():
                    ct(d, 580, m.group(2).strip(), F(FE, 44))
            else:
                ct(d, 430, t, F(FE, 72))
        else:  # term card(s), noen-exact ruby pairs
            y = 1080 // 2 - (len(h) * (113 + 26) - 26) // 2 - 60
            y = max(180, y)
            bottom = y
            for b in h:
                s = b['text'].strip().rstrip('.')
                try:
                    deva = to_deva(s)
                except Exception:
                    deva = s
                ct(d, y, deva, F(FD, 84))
                ct(d, y + 113, s, F(FR, 40), FADE)
                y += 113 + 26 + 40
            bottom = y
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
