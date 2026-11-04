#!/usr/bin/env python3
"""Append-only pipeline event log. Every stage execution writes one line:
{ts, lane, chapter, stage, status, secs, detail}. Progress is DERIVED by
reading this file — never hand-edited, never deleted (-regulation).
Usage: from events import log_event
"""
import json, os, time

BASE = os.path.expanduser('~/tantrasara')
LOG = os.path.join(BASE, 'EVENTS.jsonl')


def log_event(lane, chapter, stage, status, secs=0.0, detail=''):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': time.strftime('%FT%TZ', time.gmtime()),
                            'lane': lane, 'chapter': chapter, 'stage': stage,
                            'status': status, 'secs': round(secs, 1),
                            'detail': detail[:200]}) + '\n')


def read_events(lane=None, chapter=None):
    out = []
    if not os.path.exists(LOG):
        return out
    for line in open(LOG, encoding='utf-8'):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if lane and e.get('lane') != lane:
            continue
        if chapter and e.get('chapter') != chapter:
            continue
        out.append(e)
    return out
