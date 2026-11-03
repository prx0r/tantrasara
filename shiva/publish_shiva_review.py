#!/usr/bin/env python3
"""Publish the shiva pre-render review pack: readable storyboard + holds
timeline + contact sheets, uploaded to R2 for owner sign-off.
Usage: python3 publish_shiva_review.py <sNN>
Writes shiva/review/sNN/ {storyboard.md, timeline.md, manifest.json}
(sheets stay on volume/R2, never committed) and uploads to
r2:svread-audio/shiva/review/s<NN>/. Owner confirms by message; engineer
records shiva/approved_s<NN>.json (the render gate).
Mirrors publish_review.py with the shiva lane (paths + R2 prefix).
"""
import json, os, subprocess, sys, hashlib, datetime

BASE = os.path.expanduser('~/tantrasara')
SHIVA = os.path.join(BASE, 'shiva')
ch = sys.argv[1]
assert ch.startswith('s') and ch[1:].isdigit(), 'want sNN'
SB = f'{SHIVA}/storyboards/storyboard_{ch}.json'
GL = f'{SHIVA}/glossary_{ch}.json'
OUT = f'{SHIVA}/review/{ch}'
os.makedirs(OUT, exist_ok=True)

sb = json.load(open(SB, encoding='utf-8'))
gl = json.load(open(GL, encoding='utf-8')) if os.path.exists(GL) else {}
confirmed = sorted(k for k, v in gl.items() if v.get('status') == 'confirmed')

errs = sb.get('validation', {}).get('errors', [])
assert not errs, f'{ch}: storyboard not green — publish refused'

lines = [f'# Review — shiva {ch}', '',
         f'{len(sb["blocks"])} blocks. Voices: ' +
         ', '.join(f'{v}={sum(1 for b in sb["blocks"] if b["voice"]==v)}'
                   for v in sorted(set(b['voice'] for b in sb['blocks']))) + '.',
         f'Confirmed glossary terms ({len(confirmed)}): ' + (', '.join(confirmed) or 'none') + '.', '']
for b in sb['blocks']:
    t = b['text'].replace('\n', ' / ')
    lines += [f"## {b['id']} · {b['type']} · {b['voice']} · [{b.get('section','')[:40]}]", '',
              (t[:220] + ('…' if len(t) > 220 else '')), '']
open(f'{OUT}/storyboard.md', 'w', encoding='utf-8').write('\n'.join(lines))

r = subprocess.run(['python3', f'{BASE}/holds_timeline.py', SB, GL, f'{OUT}/timeline.md'],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'timeline: no terms')

r = subprocess.run(['python3', f'{BASE}/render_holds.py', SB, f'/tmp/shiva_review_holds_{ch}'],
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

subprocess.run(['rclone', 'copyto', f'{OUT}/storyboard.md',
                f'r2:svread-audio/shiva/review/{ch}/storyboard.md'], check=True)
subprocess.run(['rclone', 'copyto', f'{OUT}/timeline.md',
                f'r2:svread-audio/shiva/review/{ch}/timeline.md'], check=True)
subprocess.run(['rclone', 'copy', f'/tmp/shiva_review_holds_{ch}',
                f'r2:svread-audio/shiva/review/{ch}/sheets'], check=True)
print(f'published: shiva/review/{ch}/ (manifest approved=false — awaiting owner)')
print(f'https://pub-87169194562a44fcb8279a799d626c62.r2.dev/shiva/review/{ch}/storyboard.md')
