#!/usr/bin/env python3
"""Full hold-card set in locked house style + contact sheet.
Usage: python3 render_holds.py <storyboard.json> <outdir>
Single source of truth for cards: holds.py (shared with build_clip.py).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import holds as H
from PIL import Image, ImageDraw


def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    # chapter glossary for term glosses (review mode: proposed shown)
    import glob as _g, re as _re
    gl, m = {}, _re.search(r'ch(\d+)', sys.argv[1])
    if m:
        gp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           f'glossary_ch{m.group(1)}.json')
        if os.path.exists(gp):
            raw = json.load(open(gp, encoding='utf-8'))
            gl = {k: (v.get('gloss', '') if isinstance(v, dict) else v)
                  for k, v in raw.items()}
    groups = H.build_holds(sb['blocks'])
    flat = sb['blocks']
    idx = {b['id']: i for i, b in enumerate(flat)}
    files = []
    for hi, h in enumerate(groups):
        last_id = h[-1]['id']
        sub = ''
        for b in flat[idx[last_id] + 1:idx[last_id] + 6]:
            if b.get('type') in ('narration', 'dialogue') and b.get('voice') in ('granny', 'man'):
                sub = b['text'][:140]
                break
        im = H.render_hold(h, sub if sub else None, gl)
        fn = f'{out}/hold{hi:03d}.png'
        im.save(fn)
        files.append(fn)
    print(f'rendered {len(files)} holds')
    cols, cw, chh = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new('RGB', (cw * cols, rows * chh + 40), (245, 243, 238))
    sd = ImageDraw.Draw(sheet)
    sd.text((16, 8), f'Tantrasara holds — {len(files)} cards', fill=H.INK,
            font=H.F(H.FE, 22))
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).resize((cw, chh)), ((i % cols) * cw, 40 + (i // cols) * chh))
    sheet.save(f'{out}/contact_sheet.png')
    print('sheet:', f'{out}/contact_sheet.png')


if __name__ == '__main__':
    main()
