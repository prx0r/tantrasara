#!/usr/bin/env python3
"""First-minute video: shipped mix + v2 hold cards + karaoke subtitles.
Usage: python3 build_firstmin_vid.py <out.mp4>
Blocks: b_opener (bell/title card) + b1..b10 (verse, narration, first man line).
"""
import json, os, re, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
AUD = '/tmp/asm1/first_min.mp3'

def F(p, s):
    from PIL import ImageFont as I
    return I.truetype(p, s)

def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)

sb = json.load(open(os.path.expanduser('~/tantrasara/storyboard_ch6.json'), encoding='utf-8'))
byid = {b['id']: b for b in sb['blocks']}
ids = ['b_opener', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10']
blocks = [byid[i] for i in ids]

def main(out):
    # word timings on the shipped mix
    from faster_whisper import WhisperModel
    model = WhisperModel('base')
    words = []
    for s in model.transcribe(AUD, word_timestamps=True)[0]:
        for w in (s.words or []):
            words.append((w.word.strip(), w.start, w.end))
    print('words:', len(words))
    norm = lambda s: re.sub(r'[^a-z0-9\u0100-\u024f\u1e00-\u1eff]+', '', s.lower())
    alloc, wi = [], 0
    # b_opener = bell 0..12.76 fixed
    alloc.append((blocks[0], 0.0, 12.76))
    for b in blocks[1:]:
        bt = norm(b['text'])
        start = words[wi][1] if wi < len(words) else 12.76
        acc = ''
        while wi < len(words) and len(acc) < len(bt):
            acc += norm(words[wi][0])
            wi += 1
        end = words[wi - 1][2] if wi > 0 else start
        alloc.append((b, start, end))
    # hold per block
    def hold_for(b):
        if b['id'] == 'b_opener':
            return ('title', 'Chapter Six — Kālādhva')
        if b['type'] == 'verse':
            return ('term', b['text'].strip().rstrip('.'))
        return ('title', 'Chapter Six — Kālādhva')
    # frames per word interval
    fdir = '/tmp/fm_frames'
    import shutil
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    entries, idx = [], 0
    for (b, s, e) in alloc:
        ws = b['text'].split() if b['id'] != 'b_opener' else ['♪']
        if e <= s or not ws:
            continue
        hk, ht = hold_for(b)
        total_c = max(1, sum(len(w) for w in ws))
        t = s
        for k, w_ in enumerate(ws):
            frac = sum(len(x) for x in ws[:k + 1]) / total_c
            t1 = s + (e - s) * frac
            im = Image.new('RGB', (W, H), LIGHT)
            d = ImageDraw.Draw(im)
            if hk == 'title':
                d.text(((W - d.textlength(ht, font=F(FE, 96))) / 2, 300), ht, font=F(FE, 96), fill=INK)
            else:
                try:
                    from indic_transliteration import sanscript
                    deva = sanscript.transliterate(ht, sanscript.IAST, sanscript.DEVANAGARI)
                except Exception:
                    deva = ht
                ct(d, 330, deva, F(FD, 84))
                ct(d, 330 + 113, ht, F(FR, 40), FADE)
            # subtitle: current block karaoke, wrapped to <=2 lines
            if b['id'] != 'b_opener':
                sw = ws
                if sw and sw[0].startswith('"'):
                    sw = ['\u201c' + sw[0][1:]] + sw[1:]
                if sw and sw[-1].endswith('"'):
                    sw = sw[:-1] + [sw[-1][:-1] + '\u201d']
                fnt = F(FE, 46)
                lines_all = []
                for _size in (46, 40, 36):
                    fnt = F(FE, _size)
                    la, cur_ln = [], ''
                    for w_ in sw:
                        tx = (cur_ln + ' ' + w_).strip()
                        if d.textlength(tx, font=fnt) > 1750 and cur_ln:
                            la.append(cur_ln); cur_ln = w_
                        else:
                            cur_ln = tx
                    if cur_ln:
                        la.append(cur_ln)
                    if len(la) <= 2:
                        lines_all = la
                        break
                assert lines_all and len(lines_all) <= 2, f'subtitle too long: {b["text"][:60]}'
                # find current word's line
                counts, acc = [], 0
                for ln in lines_all:
                    counts.append(acc)
                    acc += len(ln.split())
                line_of = next((i for i in range(len(lines_all))
                                if k < counts[i] + len(lines_all[i].split())), len(lines_all) - 1)
                for li, ln in enumerate(lines_all):
                    wln = ln.split()
                    if li < line_of:
                        lit_l, rest_l, rel = ln, '', len(wln)
                    elif li > line_of:
                        lit_l, rest_l, rel = '', ln, -1
                    else:
                        rel = k - counts[li]
                        lit_l = ' '.join(wln[:rel + 1]) + (' ' if rel + 1 < len(wln) else '')
                        rest_l = ' '.join(wln[rel + 1:])
                    yline = SUB_Y + li * 62
                    if lit_l:
                        d.text(((W - d.textlength(ln, font=fnt)) / 2, yline), lit_l, font=fnt, fill=INK)
                    d.text(((W - d.textlength(ln, font=fnt)) / 2 + d.textlength(lit_l, font=fnt), yline),
                           rest_l, font=fnt, fill=FADE)
            im.save(f'{fdir}/{idx:05d}.png')
            entries.append((idx, max(0.05, t1 - t)))
            t = t1
            idx += 1
    lines = []
    for i, du in entries:
        lines += [f"file '{fdir}/{i:05d}.png'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir}/{entries[-1][0]:05d}.png'")
    open(f'{fdir}/concat.txt', 'w').write('\n'.join(lines) + '\n')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{fdir}/concat.txt', '-i', AUD,
                    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    print('OK:', out, f'{idx} cuts')

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
