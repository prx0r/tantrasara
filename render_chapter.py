#!/usr/bin/env python3
"""Render a chapter's audio from its frozen storyboard. Idempotent and $0-safe.
Usage: python3 render_chapter.py <storyboard.json> [--dry-run] [--force] [--limit N]
Layout (all on the volume mount — local disk stays out of it):
  renders/<ch>/groups/<sec>/g<k>_<voice>_<hash>.wav   one Fish call per group
  renders/<ch>/blocks/<bid>.json                      group->block timing map
  renders/<ch>/assembly/<ch>_full.wav                 bell + sections + gaps
  renders/<ch>/receipts/calls.jsonl                   every Fish call logged
Grouping: consecutive blocks, same section, same voice (voice none skipped —
figures/labels are visual-only, narration covers them). Opener bell is an
asset copy, never a render.
Cache: group filename carries sha1(voice+directed text); skip if present
unless --force. --dry-run prints the plan + char usage, calls nothing.
"""
import json, os, re, sys, hashlib, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from holds import drops_for, split_after

VOL = os.path.expanduser('~/vol/tantrasara/renders')
SECTION_GAP_S = 1.0   # silence between sections (ear review)
BELL_MIX_DB = 6.0     # bell_ding; owner call 2026-11-02: short bell, +6dB
MAN_ATTEN = 0.75      # man reads at 75% amplitude of granny/verse (-2.5 dB)

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]

def main():
    sb_path, args = sys.argv[1], sys.argv[2:]
    dry = '--dry-run' in args
    force = '--force' in args
    limit = int(args[args.index('--limit') + 1]) if '--limit' in args else 0
    sb = json.load(open(sb_path, encoding='utf-8'))
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    groups, cur = [], []
    def flush():
        nonlocal cur
        if cur:
            groups.append(cur)
            cur = []
    for b in sb['blocks']:
        if b['id'] == 'b_opener':
            flush()
            groups.append([dict(b, group_kind='opener')])
            continue
        if b['voice'] == 'none' or b.get('type') in ('figure', 'label', 'meta'):
            continue  # visual-only; narration covers it
        key = (b['section'], b['voice'])
        if cur and (cur[0]['section'], cur[0]['voice']) != key:
            flush()
        cur.append(b)
    flush()
    # impact drops split groups so pauses land anywhere (re-rendered halves
    # are content-hash cache misses — automatic, prosody-safe by bed)
    _drops = drops_for(sb_path)
    if _drops:
        _have = {b['id'] for g in groups for b in g if 'group_kind' not in b}
        for _bid in _drops:
            assert _bid in _have, f"drop {_bid}: block not rendered (skipped type?)"
        groups = split_after(groups, set(_drops))
        print(f'impact splits at: {sorted(set(_drops))}', flush=True)
    print(f'chapter={ch} groups={len(groups)}')
    total_chars, n_calls, skipped = 0, 0, 0
    plan = []
    sec_seen, sec_slug = {}, {}
    for b in sb['blocks']:
        if b['section'] not in sec_seen:
            sec_seen[b['section']] = len(sec_seen)
    for sec in sec_seen:
        sec_slug[sec] = slug(sec) or f"sec{sec_seen[sec]:02d}"
    for i, g in enumerate(groups):
        if g[0].get('group_kind') == 'opener':
            plan.append({'kind': 'opener', 'asset': g[0]['asset']})
            continue
        voice, sec = g[0]['voice'], g[0]['section']
        text = ' '.join(b.get('directed', b['text']) for b in g)
        h = hashlib.sha1(f'{voice}|{text}'.encode()).hexdigest()[:12]
        gdir = f'{VOL}/{ch}/groups/{sec_slug[sec]}'
        fn = f'{gdir}/g{i:03d}_{voice}_{h}.wav'
        exists = os.path.exists(fn) and os.path.getsize(fn) > 1000
        total_chars += len(text)
        if exists and not force:
            skipped += 1
            plan.append({'kind': 'cached', 'file': fn, 'bids': [b['id'] for b in g]})
        else:
            n_calls += 1
            plan.append({'kind': 'render', 'file': fn, 'voice': voice,
                         'chars': len(text), 'bids': [b['id'] for b in g],
                         'text': text})
        if limit and n_calls >= limit:
            break
    print(f'tts calls: {n_calls} new, {skipped} cached, {total_chars} chars total')
    for p in plan:
        if p['kind'] == 'render':
            print(f"  RENDER {p['file']} [{p['voice']}] {p['chars']}ch {p['bids'][0]}..{p['bids'][-1]}")
        elif p['kind'] == 'cached':
            print(f"  cached {p['file']}")
        else:
            print(f"  opener {p['asset']}")
    if dry:
        print(f'DRY RUN — no API calls, est. {total_chars} Fish chars (~${total_chars * 0:.2f} on free tier)')
        return
    # real render: one Fish call per uncached group, receipts appended, failures logged
    VOICES = {'granny': '614f8afd83f841048c040b2c6234d2c1',
              'man': 'fcfd5ebf496949ed9f76b3a533ee4738',
              'verse': '4e873c37d4cb439e9bccc4dc1f633290'}
    import hashlib as _hl
    rdir = f'{VOL}/{ch}/receipts'
    os.makedirs(rdir, exist_ok=True)
    log = open(f'{rdir}/calls.jsonl', 'a', encoding='utf-8')
    done, failed = 0, []
    for p in plan:
        if p['kind'] != 'render':
            continue
        os.makedirs(os.path.dirname(p['file']), exist_ok=True)
        r = subprocess.run(
            ['python3', '/home/ubuntu/shiva-sutras/tools/tts_line.py',
             p['text'], p['file'], '1.0', VOICES[p['voice']]],
            capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.exists(p['file']):
            dur = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=nw=1:nk=1', p['file']],
                capture_output=True, text=True).stdout.strip()
            rec = {'file': p['file'], 'voice': p['voice'], 'chars': p['chars'],
                   'bids': p['bids'],
                   'sha': _hl.sha256(open(p['file'], 'rb').read()).hexdigest()[:16],
                   'dur': dur}
            log.write(json.dumps(rec) + '\n')
            log.flush()
            done += 1
            print(f'ok {done} {p["file"]} {dur}s', flush=True)
        else:
            failed.append(p['file'])
            print(f'FAIL {p["file"]}: {r.stderr[-300:] or r.stdout[-300:]}', flush=True)
    print(f'rendered={done} failed={len(failed)}')
    for f in failed:
        print('FAILED:', f)

if __name__ == '__main__':
    main()
