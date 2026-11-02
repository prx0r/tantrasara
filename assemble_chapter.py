#!/usr/bin/env python3
"""Assemble a chapter mix from rendered groups in storyboard order.
Usage: python3 assemble_chapter.py <storyboard.json> <out.mp3> [--dry-run]
Bell (ding, +6dB) opens; 0.4s beds between groups, 1.0s between sections.
Reads group wavs via receipts/calls.jsonl (bid -> file). Fails loud on gaps.
"""
import json, os, re, subprocess, sys
import glob as _glob
import hashlib as _hl

def group_file(ch, sec, voice, text):
    h = _hl.sha1(f'{voice}|{text}'.encode()).hexdigest()[:12]
    pat = f'{VOL}/{ch}/groups/{sec}/*_{voice}_{h}.wav'
    found = _glob.glob(pat)
    return found[0] if found else None

VOL = os.path.expanduser('~/vol/tantrasara/renders')
BELL = '/home/ubuntu/vatulanatha/sfx/bell_ding.wav'

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or 'sec'

def main():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    out, dry = sys.argv[2], '--dry-run' in sys.argv
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    recs = {}
    rpath = f'{VOL}/{ch}/receipts/calls.jsonl'
    if os.path.exists(rpath):
        for l in open(rpath, encoding='utf-8'):
            r = json.loads(l)
            for b in r['bids']:
                recs[b] = r['file']
    # group blocks consecutive same-voice (same rule as render_chapter)
    groups, cur, sec = [], [], None
    order = []
    for b in sb['blocks']:
        if b['id'] == 'b_opener':
            continue
        if b['voice'] == 'none':
            continue
        key = (b['section'], b['voice'])
        if cur and (cur[0]['section'], cur[0]['voice']) != key:
            groups.append(cur)
            cur = []
        cur.append(b)
    if cur:
        groups.append(cur)
    # resolve each group to its content-hashed wav (never trust stale bids)
    resolved, missing = [], 0
    for g in groups:
        voice = g[0]['voice']
        text = ' '.join(b.get('directed', b['text']) for b in g)
        f = group_file(ch, slug(g[0]['section']), voice, text)
        if f:
            resolved.append((g, f))
        else:
            missing += 1
            if missing <= 5:
                print(f'  missing: {g[0]["id"]}..{g[-1]["id"]} [{voice}]')
    print(f'groups={len(groups)} missing_audio={missing}')
    if dry or missing:
        print('DRY RUN' if dry else 'BLOCKED — render missing groups first')
        return
    inputs = ['-i', BELL]
    n = 1
    # bell at +6dB, then groups with beds
    for i, (g, f) in enumerate(resolved):
        inputs += ['-i', f]
        n += 1
        if i < len(resolved) - 1:
            nxt = resolved[i + 1][0]
            bed = '1.0' if nxt[0]['section'] != g[0]['section'] else '0.4'
            inputs += ['-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono:d={bed}']
            n += 1
    streams = ''.join(f'[{i}:a]' for i in range(n))
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + inputs +
                   ['-filter_complex',
                    f'[0:a]volume=6dB[b];[b]{streams[5:]}concat=n={n}:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', out], check=True)
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration', '-of', 'default=nw=1:nk=1', out],
                         capture_output=True, text=True).stdout.strip()
    print(f'OK: {out} {dur}s')

if __name__ == '__main__':
    main()
