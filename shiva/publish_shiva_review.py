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
import json, os, subprocess, sys, hashlib, datetime, tempfile, atexit, shutil
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
SHIVA = os.path.join(BASE, 'shiva')
ch = sys.argv[1]
assert ch.startswith('s') and ch[1:].isdigit(), 'want sNN'
SB = f'{SHIVA}/storyboards/storyboard_{ch}.json'
GL = f'{SHIVA}/glossary_{ch}.json'
OUT = f'{SHIVA}/review/{ch}'
os.makedirs(OUT, exist_ok=True)

from factory_contract import read_json, sha256 as contract_sha256, validate_bundle
bundle = validate_bundle(SB)
sb, gl = bundle['storyboard'], bundle['glossary']
snapshot = {p: contract_sha256(p) for p in (SB, GL, __file__, f'{BASE}/holds_timeline.py')}
if read_json(SB) != sb or read_json(GL) != gl:
    raise RuntimeError('review inputs changed while they were loaded')
def check_snapshot():
    if any(contract_sha256(p) != digest for p, digest in snapshot.items()):
        raise RuntimeError('review inputs or builders changed during publication')
marker = Path(OUT) / '.publish-in-progress'
marker.write_text('Remove only after all review uploads and the manifest succeed.\n', encoding='utf-8')
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
              t, '']
Path(OUT, 'storyboard.md').write_text('\n'.join(lines), encoding='utf-8')

r = subprocess.run(['python3', f'{BASE}/holds_timeline.py', SB, GL, f'{OUT}/timeline.md'],
                   capture_output=True, text=True, check=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'timeline: no terms')

sheet_dir = tempfile.mkdtemp(prefix=f'shiva_review_{ch}_', dir='/tmp')
atexit.register(shutil.rmtree, sheet_dir, ignore_errors=True)
r = subprocess.run(['python3', f'{BASE}/render_holds.py', SB, sheet_dir],
                   capture_output=True, text=True, check=True)
if not os.path.isfile(f'{sheet_dir}/contact_sheet.png'):
    raise RuntimeError('contact sheet was not produced')
print('sheets:', (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'ok'))


def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


check_snapshot()
manifest = {'chapter': ch, 'date': datetime.date.today().isoformat(),
            'blocks': len(sb['blocks']),
            'storyboard_sha': snapshot[SB], 'glossary_sha': snapshot[GL],
            'confirmed_terms': confirmed, 'storyboard_view_sha': sha(f'{OUT}/storyboard.md'),
            'timeline_sha': sha(f'{OUT}/timeline.md'), 'sheet_sha': sha(f'{sheet_dir}/contact_sheet.png'),
            'publisher_sha': snapshot[__file__], 'timeline_builder_sha': snapshot[f'{BASE}/holds_timeline.py'],
            'approved': False}
from factory_contract import validate_schema
validate_schema('review-manifest', manifest, 'new review manifest')

subprocess.run(['rclone', 'copyto', f'{OUT}/storyboard.md',
                f'r2:svread-audio/shiva/review/{ch}/storyboard.md'], check=True)
subprocess.run(['rclone', 'copyto', f'{OUT}/timeline.md',
                f'r2:svread-audio/shiva/review/{ch}/timeline.md'], check=True)
subprocess.run(['rclone', 'copy', sheet_dir,
                f'r2:svread-audio/shiva/review/{ch}/sheets'], check=True)
check_snapshot()
with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=OUT, delete=False) as f:
    json.dump(manifest, f, indent=1)
    temp_manifest = f.name
os.replace(temp_manifest, f'{OUT}/manifest.json')
marker.unlink()
print(f'published: shiva/review/{ch}/ (manifest approved=false — awaiting owner)')
print(f'https://pub-87169194562a44fcb8279a799d626c62.r2.dev/shiva/review/{ch}/storyboard.md')
