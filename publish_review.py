#!/usr/bin/env python3
"""Publish the pre-render review pack: full storyboard (readable) + holds
timeline + contact sheets, uploaded to R2 for owner sign-off.
Usage: python3 publish_review.py <ch>
Writes review/ch<NN>/ {storyboard.md, timeline.md, manifest.json} locally
(sheets stay on volume/R2, never committed) and uploads to
r2:svread-audio/tantrasara/review/ch<NN>/.
Owner confirms by message; engineer records approved_ch<NN>.json (that file
is the render gate — see run_all.stage_render).
"""
import json, os, subprocess, sys, hashlib, datetime

BASE = os.path.expanduser('~/tantrasara')
ch = sys.argv[1].zfill(2)
SB = f'{BASE}/storyboard_ch6.json' if ch == '06' else f'{BASE}/storyboard_ch{ch}.json'
GL = f'{BASE}/glossary_ch{ch}.json'
OUT = f'{BASE}/review/ch{ch}'
os.makedirs(OUT, exist_ok=True)

sb = json.load(open(SB, encoding='utf-8'))
gl = json.load(open(GL, encoding='utf-8')) if os.path.exists(GL) else {}
confirmed = sorted(k for k, v in gl.items() if v.get('status') == 'confirmed')

errs = sb.get('validation', {}).get('errors', [])
assert not errs, f'ch{ch}: storyboard not green — publish refused'

# 1. readable storyboard: every block, voice, first 220 chars
lines = [f'# Review — chapter {ch}', '',
         f'{len(sb["blocks"])} blocks. Voices: ' +
         ', '.join(f'{v}={sum(1 for b in sb["blocks"] if b["voice"]==v)}'
                   for v in sorted(set(b['voice'] for b in sb['blocks']))) + '.',
         f'Confirmed glossary terms ({len(confirmed)}): ' + (', '.join(confirmed) or 'none') + '.', '']
for b in sb['blocks']:
    t = b['text'].replace('\n', ' / ')
    lines += [f"## {b['id']} · {b['type']} · {b['voice']} · [{b.get('section','')[:40]}]", '',
              (t[:220] + ('…' if len(t) > 220 else '')), '']
open(f'{OUT}/storyboard.md', 'w', encoding='utf-8').write('\n'.join(lines))

# 2. holds timeline (planning estimate, 150wpm — real timings at render)
r = subprocess.run(['python3', f'{BASE}/holds_timeline.py', SB, GL, f'{OUT}/timeline.md'],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'timeline: no terms')

# 3. contact sheets (cards only, no audio)
r = subprocess.run(['python3', f'{BASE}/render_holds.py', SB, f'/tmp/review_holds_ch{ch}'],
                   capture_output=True, text=True)
print('sheets:', (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'ok'))

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

manifest = {'chapter': ch, 'date': datetime.date.today().isoformat(),
            'blocks': len(sb['blocks']),
            'storyboard_sha': sha(SB),
            'glossary_sha': sha(GL) if os.path.exists(GL) else None,
            'confirmed_terms': confirmed,
            'approved': False}
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), indent=1)

# 4. upload (storyboard + timeline + sheets)
subprocess.run(['rclone', 'copyto', f'{OUT}/storyboard.md',
                f'r2:svread-audio/tantrasara/review/ch{ch}/storyboard.md'], check=True)
subprocess.run(['rclone', 'copyto', f'{OUT}/timeline.md',
                f'r2:svread-audio/tantrasara/review/ch{ch}/timeline.md'], check=True)
subprocess.run(['rclone', 'copy', f'/tmp/review_holds_ch{ch}',
                f'r2:svread-audio/tantrasara/review/ch{ch}/sheets'], check=True)
print(f'published: review/ch{ch}/ (manifest approved=false — awaiting owner)')
print(f'https://pub-87169194562a44fcb8279a799d626c62.r2.dev/tantrasara/review/ch{ch}/storyboard.md')
