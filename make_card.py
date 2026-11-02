#!/usr/bin/env python3
"""Tantrasara hold cards in the chant-video house style (white Essay-0).
Usage: python3 make_card.py <outdir>
Renders 6 representative ch6 holds as stills + contact sheet. Stills only.
Fonts/layout constants match kashmir_audio/make_card.py noen set.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, FADE, RED = (255, 255, 255), (23, 20, 15), (207, 201, 190), (165, 42, 42)
FD = "/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf"
FR = "/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf"
FE = "/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def centered(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)

def card(kind):
    im = Image.new("RGB", (W, H), LIGHT)
    return im, ImageDraw.Draw(im)

def save(im, path):
    im.save(path)
    print('still:', path)

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    # 1. chapter title
    im, d = card('title')
    fe72, fe40, fr36 = F(FE, 72), F(FE, 40), F(FR, 36)
    centered(d, 330, 'TANTRASĀRA · CHAPTER SIX', fe40, FADE)
    centered(d, 430, 'The Path of Time', fe72)
    centered(d, 540, 'or, how Śiva crammed sixty years, several billion', fr36, FADE)
    centered(d, 590, 'universes, and the history of existence into one breath', fr36, FADE)
    save(im, f'{outdir}/card1_title.png')
    # 2. term
    im, d = card('term')
    fd84, fr40 = F(FD, 84), F(FR, 40)
    centered(d, 420, 'Kālī-śakti', fd84)
    centered(d, 560, 'the divine power of time', fr40, FADE)
    save(im, f'{outdir}/card2_term.png')
    # 3. figure
    im, d = card('figure')
    fe150, fe44 = F(FE, 150), F(FE, 44)
    centered(d, 380, '36', fe150)
    centered(d, 580, 'aṅgulas · nirgamana', fe44)
    centered(d, 650, 'thirty-six finger-widths, outward', F(FR, 38), FADE)
    save(im, f'{outdir}/card3_figure.png')
    # 4. dialogue (tea scene, man + granny turn)
    im, d = card('dialogue')
    fr64, fe30 = F(FR, 64), F(FE, 30)
    centered(d, 300, '“Terrible business down there, isn’t it?”', fr64)
    centered(d, 420, '“Quite. Another dissolution?”', fr64, FADE)
    centered(d, 700, '— THE GODS, DURING PRALAYA', fe30, RED)
    save(im, f'{outdir}/card4_dialogue.png')
    # 5. closing verse (Devanagari)
    im, d = card('verse')
    fd64 = F(FD, 64)
    centered(d, 400, 'संविद्रूपस्यात्मनः प्राणशक्तिं', fd64)
    centered(d, 500, 'पश्यन्रूपं तत्रगं चातिकालम्।', fd64)
    centered(d, 640, 'Saṃvidrūpasyātmanaḥ prāṇaśaktiṃ paśyan', F(FR, 38), FADE)
    save(im, f'{outdir}/card5_verse.png')
    # 6. translation line (verse voice gloss)
    im, d = card('gloss')
    centered(d, 430, 'Contemplate the power of prāṇa belonging', F(FE, 56))
    centered(d, 510, 'to your own Self — consciousness itself.', F(FE, 56))
    centered(d, 640, 'beyond time · together with every cycle', F(FR, 38), FADE)
    save(im, f'{outdir}/card6_gloss.png')
    # contact sheet
    import glob as _g
    files = sorted(_g.glob(f'{outdir}/card*.png'))
    sheet = Image.new('RGB', (960 * 2, 540 * 3 + 40), (245, 243, 238))
    sd = ImageDraw.Draw(sheet)
    sd.text((20, 8), 'Tantrasara ch6 — house-style hold cards (stills for approval)',
            font=F(FE, 24), fill=INK)
    for i, f in enumerate(files):
        thumb = Image.open(f).resize((960, 540))
        sheet.paste(thumb, ((i % 2) * 960, 40 + (i // 2) * 540))
    sheet.save(f'{outdir}/contact_sheet.png')
    print('sheet:', f'{outdir}/contact_sheet.png')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ts_cards')
