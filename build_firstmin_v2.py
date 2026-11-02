#!/usr/bin/env python3
"""First-minute video v2: bell_ding opener, verse-led holds (no chapter
title), karaoke from MMS word timings (same system as kashmir_audio).
Usage: python3 build_firstmin_v2.py <out.mp4>
"""
import json, os, re, subprocess
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

def ct(d, y, s, font, fill=INK):
    d.text(((W - d.textlength(s, font=font)) / 2, y), s, font=font, fill=fill)

sb = json.load(open(os.path.expanduser('~/tantrasara/storyboard_ch6.json'), encoding='utf-8'))
byid = {b['id']: b for b in sb['blocks']}
T = '/tmp/asm1'
# group -> (audio, mms json, block ids, voice)
GROUPS = [
    ('g001_verse_56ee08d85d25.wav', '/tmp/mms_g001.json', ['b1'], 'verse'),
    ('g002_clean.wav', '/tmp/mms_g002.json', [f'b{i}' for i in range(2, 10)], 'granny'),
    ('g003_man_75.wav', '/tmp/mms_g003.json', ['b10'], 'man'),
]

def load_words(path):
    return json.load(open(path, encoding='utf-8'))

def main(out):
    # assembly: bell_ding(+6dB) + groups with 0.4s lavfi beds
    # (filter_complex: concat demuxer chokes on anullsrc wav tails)
    mix = f'{T}/first_min_v2.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error',
                    '-i', '/home/ubuntu/vatulanatha/sfx/bell_ding.wav',
                    '-i', f'{T}/g001_verse_56ee08d85d25.wav',
                    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono:d=0.4',
                    '-i', f'{T}/g002_clean.wav',
                    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono:d=0.4',
                    '-i', f'{T}/g003_man_75.wav',
                    '-filter_complex',
                    '[0:a]volume=6dB[b];[b][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', mix], check=True)
    # timings per block from MMS
    alloc = []  # (block, start, end, words[(w,t_on,t_off)])
    t = 0.99  # bell
    # opener bell -> verse hold already
    alloc.append((None, 0.0, 0.99, []))
    for wav, mms, bids, voice in GROUPS:
        rows = load_words(mms)
        # split rows across bids by word count of each block's text
        wi = 0
        for bid in bids:
            nw = len(byid[bid]['text'].split())
            seg = rows[wi:wi + nw]
            wi += nw
            if not seg:
                continue
            alloc.append((byid[bid], seg[0]['t_on'] + t, seg[-1]['t_off'] + t,
                          [(r['w'], r['t_on'] + t, r['t_off'] + t) for r in seg]))
        # advance t by group audio duration
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                    'format=duration', '-of', 'default=nw=1:nk=1',
                                    f'{T}/{wav}'], capture_output=True,
                                   text=True).stdout.strip())
        t += dur + 0.4
    # render per-word frames (make_card law: boundaries at word onsets)
    fdir = '/tmp/fm2_frames'
    import shutil
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    # flatten to global word order; each frame lasts until next onset
    # (make_card law: boundaries at onsets, gaps belong to the prior word)
    flat = []
    for (b, s, e, ws) in alloc:
        if b is None:
            continue
        for k, (w, t_on, t_off) in enumerate(ws):
            flat.append((b, k, t_on))
    AUDIO_END = float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=nw=1:nk=1', mix],
        capture_output=True, text=True).stdout.strip())
    # opener bell hold (verse up from frame 0: right into it)
    first_on = flat[0][2] if flat else AUDIO_END
    im = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    ct(d, 420, 'षष्ठमाह्निकम्', F(FD, 84))
    ct(d, 420 + 113, 'Kālādhvaprakāśanam', F(FR, 40), FADE)
    im.save(f'{fdir}/00000.png')
    entries, idx = [(0, max(0.05, first_on))], 1
    for fi, (b, k, t_on) in enumerate(flat):
        t_off = flat[fi + 1][2] if fi + 1 < len(flat) else AUDIO_END
        # timed rows for this block + display words (must match 1:1)
        rows = None
        for (bb, s, e, wws) in alloc:
            if bb is not None and bb['id'] == b['id']:
                rows = wws
                break
        sw = [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
        if len(sw) != len(rows):
            sw = [r[0] for r in rows]  # fall back to timed tokens
        # main hold
        im = Image.new('RGB', (W, H), LIGHT)
        d = ImageDraw.Draw(im)
        if b['type'] == 'verse':
            deva = b['text'].strip().rstrip('.')
            ct(d, 420, deva, F(FD, 84))
            ct(d, 420 + 113, b['text'].strip(), F(FR, 40), FADE)
        else:
            ct(d, 420, 'षष्ठमाह्निकम्', F(FD, 84))
            ct(d, 420 + 113, 'Kālādhvaprakāśanam', F(FR, 40), FADE)
        # subtitle karaoke, wrapped to <=2 lines
        fnt = F(FE, 46)
        lines, cur = [], ''
        for w_ in sw:
            t_ = (cur + ' ' + w_).strip()
            if d.textlength(t_, font=fnt) > 1750 and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = t_
        if cur:
            lines.append(cur)
        if len(lines) > 2:
            fnt = F(FE, 40)
            lines, cur = [], ''
            for w_ in sw:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur)
                    cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        assert len(lines) <= 2, f'subtitle too long: {b["id"]}'
        counts, acc = [], 0
        for ln in lines:
            counts.append(acc)
            acc += len(ln.split())
        li = next((i for i in range(len(lines))
                   if k < counts[i] + len(lines[i].split())), len(lines) - 1)
        rel = k - counts[li]
        for j, ln in enumerate(lines):
            wl = ln.split()
            if j < li:
                lit, rest = ln, ''
            elif j > li:
                lit, rest = '', ln
            else:
                lit = ' '.join(wl[:rel + 1]) + (' ' if rel + 1 < len(wl) else '')
                rest = ' '.join(wl[rel + 1:])
            yy = SUB_Y + j * 62
            if lit:
                d.text(((W - d.textlength(ln, font=fnt)) / 2, yy), lit, font=fnt, fill=INK)
            d.text(((W - d.textlength(ln, font=fnt)) / 2 + d.textlength(lit, font=fnt), yy),
                   rest, font=fnt, fill=FADE)
        im.save(f'{fdir}/{idx:05d}.png')
        entries.append((idx, max(0.03, t_off - t_on)))
        idx += 1
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

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
