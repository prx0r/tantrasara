#!/usr/bin/env python3
"""Pilot video for one finished section: holds + karaoke subtitles + mix.
Usage: python3 build_pilot.py '<section substring>' <out.mp4>
Reads storyboard + receipts, concatenates group wavs (0.3s beds), whisper
word timings, renders word-interval frames in v2 house style, muxes.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
VOL = os.path.expanduser('~/vol/tantrasara/renders/tantras-ra-chapter-6')
FPS = 30

def F(p, s):
    from PIL import ImageFont as I
    return I.truetype(p, s)

def main():
    pat, out = sys.argv[1], sys.argv[2]
    sb = json.load(open(os.path.expanduser('~/tantrasara/storyboard_ch6.json'), encoding='utf-8'))
    secs = sorted(set(b['section'] for b in sb['blocks'] if pat.lower() in b['section'].lower()))
    sec = secs[0]
    print('section:', sec)
    recs = {}
    for l in open(f'{VOL}/receipts/calls.jsonl', encoding='utf-8'):
        r = json.loads(l)
        for b in r['bids']:
            recs[b] = r['file']
    fef, fdf, fref = F(FE, 54), F(FD, 84), F(FR, 44)
    # ordered audio parts with per-block boundaries
    parts, bounds, t = [], [], 0.0
    import wave as _w
    beds = []
    groups, cur = [], []
    for b in sb['blocks']:
        if b['section'] != sec or b['voice'] not in ('granny', 'man', 'verse'):
            continue
        cur.append(b)
    # regroup consecutive same-voice (matches render_chapter grouping)
    gs = []
    for b in cur:
        if gs and (gs[-1][0]['voice'], ) == (b['voice'],):
            gs[-1].append(b)
        else:
            gs.append([b])
    segs = []  # (wav, blocks)
    for g in gs:
        f = recs.get(g[0]['id'])
        if not f:
            # find receipt containing any bid
            for bid in [x['id'] for x in g]:
                if bid in recs:
                    f = recs[bid]; break
        assert f, f"missing audio for {[x['id'] for x in g]}"
        segs.append((f, g))
    mix = '/tmp/pilot_mix.wav'
    lst = '/tmp/pilot_list.txt'
    with open(lst, 'w') as fh:
        for i, (f, g) in enumerate(segs):
            fh.write(f"file '{f}'\n")
            if i < len(segs) - 1:
                import subprocess as sp
                sp.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
                        'anullsrc=r=44100:cl=mono', '-t', '0.3', '-c:a', 'pcm_s16le',
                        f'/tmp/pilot_bed{i}.wav'], check=True)
                fh.write(f"file '/tmp/pilot_bed{i}.wav'\n")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', lst, '-c:a', 'pcm_s16le', mix], check=True)
    # whisper words
    from faster_whisper import WhisperModel
    model = WhisperModel('base')
    segments, _ = model.transcribe(mix, word_timestamps=True)
    words = []
    for s in segments:
        for w in (s.words or []):
            words.append((w.word.strip(), w.start, w.end))
    words = [(w if w else '') for w in words]
    print('words:', len(words))
    # allocate words to blocks in order (normalized match walk)
    norm = lambda s: re.sub(r'[^a-z0-9āīūṛṝḷṃḥṅñṭḍṇśṣ]+', '', s.lower())
    alloc, wi = [], 0
    for (_, g) in segs:
        for b in g:
            bl = [w for w in norm(b['text']).split() if False]  # char-level below
            bt = norm(b['text'])
            acc = ''
            start = words[wi][1] if wi < len(words) else 0.0
            while wi < len(words) and len(acc) < len(bt):
                acc += norm(words[wi][0])
                wi += 1
            end = words[wi - 1][2] if wi > 0 else start
            alloc.append((b, start, end))
    # holds: title/term/figure/verse update main; everything updates subtitle
    def main_for(b):
        if b['type'] in ('title',):
            return ('title', b['text'])
        if b['type'] == 'figure':
            return ('figure', b['text'])
        return None
    holds, cur_hold = [], ('title', sec)
    # find last structural anchor at-or-before each alloc block
    anchors = [(b, b['id']) for (b, _, _) in alloc if b['type'] in ('title', 'figure')] + \
              [(b, b['id']) for (b, _, _) in alloc if b['type'] == 'verse']
    # simpler: walk alloc, track current hold
    seq = []
    hold = ('title', sec)
    hold_terms = []
    for (b, s, e) in alloc:
        if b['type'] == 'title':
            hold = ('title', b['text'])
        elif b['type'] == 'figure':
            hold = ('figure', b['text'])
        elif b['type'] == 'verse':
            hold = ('term', b['text'])
        seq.append((b, s, e, hold))
    # frames per word interval
    fdir = '/tmp/pilot_frames'
    import shutil
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    entries, idx = [], 0
    for (b, s, e, h) in seq:
        # word times inside [s,e]: slice proportionally by char count
        ws = b['text'].split()
        if not ws or e <= s:
            continue
        total_c = sum(len(w) for w in ws)
        t = s
        for k, w_ in enumerate(ws):
            frac = len(w_) / max(1, total_c)
            t1 = s + (e - s) * sum(len(x) for x in ws[:k + 1]) / max(1, total_c)
            # draw
            im = Image.new('RGB', (W, H), LIGHT)
            d = ImageDraw.Draw(im)
            hk, ht = h
            y0 = 300
            if hk == 'title':
                dd = ImageDraw.Draw(im)
                dd.text(((W - dd.textlength(ht, font=fef)) / 2, y0), ht, font=fef, fill=INK)
                y0 += 110
            elif hk == 'term':
                dd = ImageDraw.Draw(im)
                fnt = fdf if any(ord(c) > 2300 for c in ht) else fef
                dd.text(((W - dd.textlength(ht, font=fnt)) / 2, y0), ht, font=fnt, fill=INK)
                y0 += 130
            elif hk == 'figure':
                dd = ImageDraw.Draw(im)
                dd.text(((W - dd.textlength(ht, font=fef)) / 2, y0), ht, font=fef, fill=INK)
                y0 += 110
            # subtitle line: current block text, lit up to word k
            sub = b['text'][:140]
            sw = sub.split()
            # map k in ws (same thing) — lit = first k+1 words
            lit = ' '.join(sw[:k + 1]) + (' ' if k + 1 < len(sw) else '')
            rest = ' '.join(sw[k + 1:])
            fnt = fef
            tw = d.textlength((lit + rest) or ' ', font=fnt)
            x = (W - tw) / 2
            d.text((x, 720), lit, font=fnt, fill=INK)
            d.text((x + d.textlength(lit, font=fnt), 720), rest, font=fnt, fill=FADE)
            im.save(f'{fdir}/{idx:05d}.png')
            entries.append((idx, max(0.05, t1 - t)))
            t = t1
            idx += 1
    import json as _j
    lines = []
    for i, du in entries:
        lines += [f"file '{fdir}/{i:05d}.png'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir}/{entries[-1][0]:05d}.png'")
    open(f'{fdir}/concat.txt', 'w').write('\n'.join(lines) + '\n')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{fdir}/concat.txt', '-i', mix,
                    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    print('OK:', out, f'{idx} cuts')

def hold_for(seq, b):
    hold = ('title', seq[0][0]['section'])
    for (bb, s, e, h) in seq:
        if bb['id'] == b['id']:
            return h
        hold = h
    return hold

if __name__ == '__main__':
    main()
