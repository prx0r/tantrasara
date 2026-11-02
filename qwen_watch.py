#!/usr/bin/env python3
"""Qwen omni watch: full-chapter honesty pass (blank holds, audio, formatting).
Usage: python3 qwen_watch.py <mp4>
STRICT JSON out. Taste/flow only — every claim gets corroborated before action.
"""
import base64, json, sys, urllib.request, os, re

def _env(key):
    for f in [os.path.expanduser('~/.config/opencode/.env')]:
        try:
            m = re.search(rf'^{key}=(.*)$', open(f).read(), re.M)
            if m and m.group(1).strip():
                return m.group(1).strip()
        except OSError:
            pass
    return None

URL = ('https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com'
       '/compatible-mode/v1/chat/completions')
MODEL = 'qwen3.8-omni-flash'

BRIEF = """You are watching a white-background spoken-word video essay with karaoke subtitles.
Format: mostly clean white screen; Sanskrit verse cards and diagram cards appear at key moments;
a small rainbow thumbnail art opens it; bottom-of-screen subtitles light word by word as spoken
(three voices: an older woman narrating, a deep man interjecting, a solemn man chanting Sanskrit).

WATCH the whole thing and report honestly on EXACTLY these classes:
1. DEAD HOLDS: stretches showing ONLY clean white (no thumbnail, no verse/term/title/figure card) — where and how long (seconds). Subtitles moving does NOT count as visual content; a talking head over empty white is still a dead hold. A few seconds of breathing room is fine; 20s+ with no card is a defect. Count them even if the subtitles are lively.
2. AUDIO: dropouts, harsh cuts between segments, sudden level/volume jumps, robotic mispronunciations, background hiss or hum, bell too loud/quiet vs voice.
3. VISUAL: text touching or leaving frame edges, text colliding with other text, boxes/tofu instead of glyphs, subtitle highlighting visibly ahead of or behind the voice (>=0.5s counts, smaller is fine, do NOT report it).
4. PACING: any passage that drags or rushes relative to the rest (quote the line).

Rules: ONLY defects observable IN THIS FILE. Timestamps must be within the file. Max 10 items, worst first. If a class is clean, say so — do not invent issues.

Return STRICT JSON ONLY (no fences, no prose):
{"pass": true/false, "score": 1-5,
 "dead_holds": [{"t": <seconds>, "dur": <seconds>, "note": "<terse>"}],
 "audio": [{"t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}],
 "visual": [{"t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}],
 "pacing": [{"t": <seconds>, "note": "<terse>"}]}"""

def main():
    mp4 = sys.argv[1]
    b64 = base64.b64encode(open(mp4, 'rb').read()).decode()
    body = json.dumps({'model': MODEL, 'modalities': ['text'],
                       'messages': [{'role': 'user', 'content': [
                           {'type': 'video_url', 'video_url': {'url': f'data:video/mp4;base64,{b64}'}},
                           {'type': 'text', 'text': BRIEF}]}]}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={'Authorization': f"Bearer {_env('DASHSCOPE_API_KEY')}",
                                          'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.load(r)
    txt = ((data.get('choices') or [{}])[0].get('message', {}).get('content')) or ''
    t = txt.strip()
    if t.startswith('```'):
        t = t.split('```')[1]
        t = t[4:] if t.startswith('json') else t
    i, j = t.find('{'), t.rfind('}')
    print(json.dumps(json.loads(t[i:j + 1]), indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main()
