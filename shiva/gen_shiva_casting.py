#!/usr/bin/env python3
"""Casting sheets for the shiva lane: every quote needing a human call.
Usage: python3 gen_shiva_casting.py [sNN ...]
Reads shiva/chapters/sNN.md via the shared builder, writes
shiva/casting/cast_sNN.md. Owner marks M/G; engineer encodes to overrides.
Shared casting rules apply (Abhinav auto-man fires on Abhinavagupta
mentions too — listed for veto all the same).
"""
import json, os, subprocess, sys

BASE = os.path.expanduser('~/tantrasara')
SHIVA = os.path.join(BASE, 'shiva')
os.makedirs(os.path.join(SHIVA, 'casting'), exist_ok=True)


def blocks_for(ch):
    subprocess.run(['python3', f'{BASE}/build_storyboard.py',
                    f'{SHIVA}/chapters/{ch}.md', f'/tmp/shiva_sb_{ch}.json'],
                   capture_output=True, text=True)
    return json.load(open(f'/tmp/shiva_sb_{ch}.json'))['blocks']


CHS = sys.argv[1:] or [f's{i:02d}' for i in range(78)]
for ch in CHS:
    blocks = blocks_for(ch)
    byid = {b['id']: i for i, b in enumerate(blocks)}
    uncast = [b for b in blocks if b['voice'] == 'UNCAST']
    auto_man = [b for b in blocks if b['type'] == 'dialogue' and b['voice'] == 'man']
    lines = [f'# Casting — shiva {ch}', '',
             f'{len(uncast)} quotes need a call. Mark each `M` (man) or `G` (granny).',
             f'{len(auto_man)} already man via the name rule (listed at end for veto).', '']
    for b in uncast:
        i = byid[b['id']]
        prev = next((x['text'][:100] for x in reversed(blocks[:i]) if x['type'] == 'narration'), '—')
        nxt = next((x['text'][:100] for x in blocks[i + 1:i + 4] if x['type'] == 'narration'), '—')
        lines += [f"## {b['id']} · [{b['section'][:45]}]", '', f'> {b["text"]}', '',
                  f'before: {prev}', '', f'after: {nxt}', '', 'call: _', '']
    lines += ['---', '## Auto-man (veto with X)', '']
    for b in auto_man:
        lines.append(f"- {b['id']}: {b['text'][:80]}")
    open(f'{SHIVA}/casting/cast_{ch}.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'{ch}: {len(uncast)} calls, {len(auto_man)} auto-man')
