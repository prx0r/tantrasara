#!/usr/bin/env python3
"""Generic opening/section clip: bell + groups + MMS karaoke + verse hold.
Usage: python3 build_clip.py <storyboard.json> <b1,b2,...> <out.mp4>
Hold: first verse block's card for the whole clip (verse-first standard).
Karaoke: MMS forced alignment per group (sa-IN verse, en-IN narration).
"""
import json, os, re, subprocess, sys, glob, hashlib, shutil

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
VOL = os.path.expanduser('~/vol/tantrasara/renders')
BELL = '/home/ubuntu/vatulanatha/sfx/bell_ding.wav'
NODE_MOD = '/tmp/mmsmod/node_modules'
ALIGN = os.path.expanduser('~/tantrasara/align_group.js')

from PIL import Image, ImageDraw, ImageFont
def F(p, s): return ImageFont.truetype(p, s)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]
def group_wav(ch, sec, voice, text):
    h = hashlib.sha1(f'{voice}|{text}'.encode()).hexdigest()[:12]
    found = glob.glob(f'{VOL}/{ch}/groups/{slug(sec)}/*_{voice}_{h}.wav')
    return found[0] if found else None
def to_deva(s):
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return ' '.join(transliterate(w, IAST, DEVANAGARI) if not re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())
def to_iast(s):
    from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST
    return ' '.join(transliterate(w, DEVANAGARI, IAST) if re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())

def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    bids = sys.argv[2].split(',')
    out = sys.argv[3]
    byid = {b['id']: b for b in sb['blocks']}
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    blocks = [byid[i] for i in bids]
    groups = []
    for b in blocks:
        if b['voice'] == 'none':
            continue
        if groups and groups[-1][0]['voice'] == b['voice'] and groups[-1][0]['section'] == b['section']:
            groups[-1].append(b)
        else:
            groups.append([b])
    wavs = []
    for g in groups:
        text = ' '.join(x.get('directed', x['text']) for x in g)
        f = group_wav(ch, g[0]['section'], g[0]['voice'], text)
        assert f, f"missing render for {g[0]['id']}..{g[-1]['id']}"
        wavs.append((f, g))
    # MMS align each group
    os.makedirs('/tmp/mmsclip', exist_ok=True)
    al = []
    for i, (f, g) in enumerate(wavs):
        disp = []
        for b in g:
            disp += [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
        lang = 'sa-IN' if g[0]['voice'] == 'verse' else 'en-IN'
        wpath = f'/tmp/mmsclip/cw{i}.json'
        opath = f'/tmp/mmsclip/ct{i}.json'
        json.dump(disp, open(wpath, 'w'), ensure_ascii=False)
        r = subprocess.run(['node', ALIGN, f, wpath, opath, lang],
                           capture_output=True, text=True, env={**os.environ, 'NODE_PATH': NODE_MOD})
        assert os.path.exists(opath), f'MMS failed group {i}: {r.stderr[-300:]}'
        rows = json.load(open(opath, encoding='utf-8'))
        assert len(rows) == len(disp), f'{g[0]["id"]}: {len(disp)} vs {len(rows)}'
        mean = sum(x['mms'] for x in rows) / len(rows)
        print(f'group {i}: n={len(rows)} mean={mean:.3f}', flush=True)
        al.append((g, rows))
    # assembly: bell(+6dB) + groups with 0.4 beds
    final_inputs = ['-i', BELL]
    for i, (f, g) in enumerate(wavs):
        final_inputs += ['-i', f]
        if i < len(wavs) - 1:
            final_inputs += ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono:d=0.4']
    nAud = 1 + len(wavs) + max(0, len(wavs) - 1)
    mix = '/tmp/clip_mix.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + final_inputs +
                   ['-filter_complex',
                    '[0:a]volume=6dB[z0];[z0]' + ''.join(f'[{j}]' for j in range(1, nAud)) +
                    f'concat=n={nAud}:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', mix], check=True)
    # flat word timeline with absolute onsets (beds included via group durations)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                  '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.strip())
            for (f, g) in wavs]
    flat = []
    off = 0.99
    for gi, ((f, g), rows) in enumerate(zip(wavs, [r for _, r in al])):
        wi = 0
        for b in g:
            sw = [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
            seg = rows[wi:wi + len(sw)]
            assert len(seg) == len(sw), f"{b['id']}: {len(sw)} vs {len(seg)}"
            # subtitle display: IAST for verse blocks (Devanagari has no
            # glyphs in the subtitle face — bare boxes otherwise)
            sub = [to_iast(w) if b['type'] == 'verse' else w for w in sw]
            for j, r in enumerate(seg):
                flat.append((b, j, r['t_on'] + off, sw, sub, r['t_off'] + off))
            wi += len(sw)
        off += durs[gi] + (0.4 if gi < len(wavs) - 1 else 0)
    # holds: verse cards while chanting, clean white once speech starts.
    # (owner: no title cards shown; Sanskrit clears when granny takes over)
    import sys as _sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import holds as _H
    _holds = _H.build_holds([b for b in blocks if b['type'] != 'title' or True])
    hold_for = {}
    _blank = Image.new('RGB', (W, H), LIGHT)
    for h in _holds:
        img = _H.render_hold(h, None)
        for b in h:
            hold_for[b['id']] = img
    # title blocks never shown: map them (and opener) appropriately
    fdir = '/tmp/clip_frames'
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    entries, idx = [], 0
    # opener: thumbnail if it exists, else first verse hold (verse up fast)
    _first_verse = next(b for b in blocks if b['type'] == 'verse')
    _THUMB = os.path.expanduser('~/tantrasara/assets/thumb_ch1.png')
    if os.path.exists(_THUMB):
        _tb = Image.open(_THUMB).convert('RGB')
        _tb.thumbnail((1400, 730), Image.LANCZOS)
        _HOLD0 = Image.new('RGB', (W, H), LIGHT)
        _HOLD0.paste(_tb, ((W - _tb.width) // 2, 50))
    else:
        _HOLD0 = hold_for.get(_first_verse['id'], _blank)
    _HOLD0.save(f'{fdir}/00000.png')
    entries.append((0, max(0.05, flat[0][2] if flat else off)))
    idx = 1
    _first_verse_hold = hold_for.get(_first_verse['id'], _blank)
    _first_verse_fi = next(i for i, (b, *_r) in enumerate(flat) if b['type'] == 'verse')
    def hold_img(b, fi):
        if fi < _first_verse_fi:
            return _HOLD0  # thumbnail holds from frame 0 until chanting starts
        if b['type'] == 'verse':
            return hold_for.get(b['id'], _blank)
        return _blank
    for fi, (b, k, t_on, sw, sub, t_off) in enumerate(flat):
        im = hold_img(b, fi).copy()
        d = ImageDraw.Draw(im)
        # subtitle karaoke, wrapped <=2 lines
        fnt = F(FE, 46)
        lines, cur = [], ''
        for w_ in sub:
            t_ = (cur + ' ' + w_).strip()
            if d.textlength(t_, font=fnt) > 1750 and cur:
                lines.append(cur); cur = w_
            else:
                cur = t_
        if cur:
            lines.append(cur)
        if len(lines) > 2:
            fnt = F(FE, 40)
            lines, cur = [], ''
            for w_ in sub:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        assert len(lines) <= 2, 'subtitle too long'
        counts, acc = [], 0
        for ln in lines:
            counts.append(acc); acc += len(ln.split())
        li = next((i for i in range(len(lines)) if k < counts[i] + len(lines[i].split())), len(lines) - 1)
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
        nxt = flat[fi + 1][2] if fi + 1 < len(flat) else off
        entries.append((idx, max(0.03, nxt - t_on)))
        idx += 1
    # pre-render hold base once (after fonts load)
    lines = []
    for i, du in entries:
        lines += [f"file '{fdir}/{i:05d}.png'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir}/{entries[-1][0]:05d}.png'")
    open(f'{fdir}/concat.txt', 'w').write('\n'.join(lines) + '\n')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{fdir}/concat.txt', '-i', mix,
                    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', sys.argv[3]], check=True)
    print('OK:', sys.argv[3], f'{idx} cuts')


if __name__ == '__main__':
    import sys
    main()
