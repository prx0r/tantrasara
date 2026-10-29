#!/usr/bin/env python3
"""Transcribe study mp3s with faster-whisper small.en into CF transcript
schema ({source, duration, engine, sentences:[{t,end,text}]}), same shape
as analayo-nibbana lecture transcripts. Study-only outputs.
Usage: python3 tools/transcribe_study.py [outdir]   # default sources/lectures/transcripts-study/
"""
import json, os, sys
from faster_whisper import WhisperModel
D = '/root/tantrasara'
SRC = D + '/sources/lectures/audio/study'
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sources/lectures/transcripts-study'
os.makedirs(OUT, exist_ok=True)
names = {'wallis_01.mp3': 'wallis-three-effective-methods',
 'wallis_02.mp3': 'wallis-ch5-part3', 'wallis_03.mp3': 'wallis-ch5-part2',
 'wallis_04.mp3': 'wallis-ch5-part1', 'wallis_05.mp3': 'wallis-ch4-part2',
 'wallis_06.mp3': 'wallis-ch4-part1', 'wallis_07.mp3': 'wallis-ch3-abridged',
 'wallis_08.mp3': 'wallis-ch2', 'wallis_09.mp3': 'wallis-ch1'}
m = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=2)
for fn, key in names.items():
    dst = f'{OUT}/{key}.transcript.json'
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        print('have', key, flush=True); continue
    src = f'{SRC}/{fn}'
    segs, info = m.transcribe(src, language='en', vad_filter=True)
    out = {'source': fn, 'duration': round(info.duration, 2), 'engine': 'faster-whisper base (study-only; small.en at canon time)',
           'sentences': [{'t': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs]}
    json.dump(out, open(dst, 'w'), indent=1)
    print('wrote', key, len(out['sentences']), 'sentences', flush=True)
print('DONE')
