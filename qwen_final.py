#!/usr/bin/env python3
"""Qwen omni final pass: render vs storyboard beats + transcript.
Usage: python3 qwen_final.py <mp4> <storyboard.json> <transcript.txt> [--cues cues.json]
Taste NEVER gates alone — every finding needs transcript/waveform
corroboration or a machine check before action. Timestamps past file
length void the pass.
"""
import base64, json, sys, urllib.request, os, re, subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _env(key):
    try:
        m = re.search(rf'^{key}=(.*)$', open(os.path.expanduser('~/.config/opencode/.env')).read(), re.M)
        if m and m.group(1).strip():
            return m.group(1).strip()
    except OSError:
        pass
    return None


URL = ('https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com'
       '/compatible-mode/v1/chat/completions')
MODEL = 'qwen3.8-omni-flash'

BRIEF = """You are the final honesty pass on a white-background spoken-word video essay with karaoke subtitles (three voices: older woman narrating, man interjecting, solemn chanting of Sanskrit). You get the video, the storyboard beats (block id, voice, first words, expected cue times) and the transcript. Report ONLY what you can tie to those materials.

1. BEATS VS PICTURE: for each beat below, is the right card on screen at the right time (thumbnail intro, verse cards while chanting, term cards on mention, white only at breaks)? List mismatches with beat id + seconds.
2. TIMINGS: do cue cards pop within 1s of their expected cue time? Flag drifts with seconds.
3. AUDIO: dropouts, harsh cuts, level jumps, robotic mispronunciations, hiss/hum, bell balance vs voice.
4. GARBLED DEVANAGARI / TOFU: hollow boxes or garbage glyphs anywhere (cards or subtitles), Sanskrit mis-split across lines, roman half duplicated (same word twice in a row, e.g. chant + identical transliteration).
5. NIGGLES (filed): text touching frame edges or the subtitle zone, cards colliding, karaoke highlight ahead of/behind voice by >=0.5s, dead white stretches 20s+ with no card (subtitles moving does not count), pacing that drags or rushes (quote the line).

Rules: ONLY defects observable IN THIS FILE + materials. Timestamps within the file. Max 12 items, worst first. Clean classes reported clean — never invent.

Return STRICT JSON ONLY (no fences, no prose):
{"pass": true/false, "score": 1-5,
 "beats": [{"bid": "...", "t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}],
 "timings": [{"key": "...", "expected": <s>, "seen": <s>}],
 "audio": [{"t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}],
 "script": [{"t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}],
 "niggles": [{"t": <seconds>, "defect": "<terse>", "fix": "<concrete>"}]}"""


def beats_summary(sb, cues):
    lines = []
    for b in sb['blocks']:
        t = b['text'].replace('\n', ' / ')
        lines.append(f"{b['id']} [{b['type']}/{b['voice']}]: {t}")
    return '\n'.join(lines)


def validate_timestamps(answer, duration):
    from factory_contract import ContractError
    for section in ('beats', 'timings', 'audio', 'script', 'niggles'):
        for item in answer[section]:
            for field in ('t', 'expected', 'seen'):
                if field in item and not 0 <= item[field] <= duration:
                    raise ContractError(f'Qwen {section}.{field} is outside the video')


def main():
    mp4, sbp, trp = sys.argv[1], sys.argv[2], sys.argv[3]
    cues = []
    for a in sys.argv[4:]:
        if a == '--cues':
            cues = json.load(open(sys.argv[sys.argv.index(a) + 1], encoding='utf-8'))
    sb = json.load(open(sbp, encoding='utf-8'))
    meta_path = Path(mp4).with_suffix('.render_meta.json')
    if meta_path.is_file():
        from factory_contract import validate_clip_artifacts
        selected = set(validate_clip_artifacts(sbp, mp4)['bids'])
        sb = dict(sb, blocks=[b for b in sb['blocks'] if b['id'] in selected])
    tr = open(trp, encoding='utf-8').read()
    cues = cues if isinstance(cues, list) else cues.get('cues', [])
    beats = beats_summary(sb, cues)
    b64 = base64.b64encode(open(mp4, 'rb').read()).decode()
    # Cues are recorded by time and key, not block ID. Do not invent a
    # block association by searching for folded ASCII inside IAST prose.
    brief = BRIEF + f"\n\nBEATS:\n{beats}\n\nCUES:\n{json.dumps(cues, ensure_ascii=False)}\n\nTRANSCRIPT:\n{tr}"
    body = json.dumps({'model': MODEL, 'modalities': ['text'],
                       'messages': [{'role': 'user', 'content': [
                           {'type': 'video_url', 'video_url': {'url': f'data:video/mp4;base64,{b64}'}},
                           {'type': 'text', 'text': brief}]}]}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={'Authorization': f"Bearer {_env('DASHSCOPE_API_KEY')}",
                                          'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=900) as r:
        data = json.load(r)
    txt = ((data.get('choices') or [{}])[0].get('message', {}).get('content')) or ''
    t = txt.strip()
    if t.startswith('```'):
        t = t.split('```')[1]
        t = t[4:] if t.startswith('json') else t
    i, j = t.find('{'), t.rfind('}')
    answer = json.loads(t[i:j + 1])
    from factory_contract import sha256, validate_schema
    validate_schema('qwen-review', answer, 'Qwen response')
    duration = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                    '-of', 'default=nw=1:nk=1', mp4], capture_output=True,
                                   text=True, check=True).stdout.strip())
    validate_timestamps(answer, duration)
    answer['provenance'] = {'video_sha256': sha256(mp4), 'storyboard_sha256': sha256(sbp),
                            'transcript_sha256': sha256(trp), 'transcript_path': str(Path(trp).resolve()),
                            'reviewer_sha256': sha256(__file__), 'model': MODEL}
    print(json.dumps(answer, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
