#!/usr/bin/env python3
"""One-shot: transcribe one chunk wav -> partial json. Separate process per
chunk keeps RSS bounded (the box OOM-kills sustained whisper runs)."""
import json, sys
from faster_whisper import WhisperModel
src, dst, offset = sys.argv[1], sys.argv[2], float(sys.argv[3])
m = WhisperModel('tiny', device='cpu', compute_type='int8', cpu_threads=1)
segs, info = m.transcribe(src, language='en', vad_filter=True)
out = [{'t': round(s.start + offset, 2), 'end': round(s.end + offset, 2),
        'text': s.text.strip()} for s in segs]
json.dump({'dur': round(info.duration, 2), 'sentences': out}, open(dst, 'w'))
print(f'{dst}: {len(out)} segs', flush=True)
