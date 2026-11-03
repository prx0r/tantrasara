#!/usr/bin/env bash
# status: the whole line on one screen. Read-only, safe anytime.
echo "== capacity =="; ~/tantrasara/sysload.sh; df -h /tmp | tail -n 1
echo "== video lock =="; cat /tmp/video_build.lock 2>/dev/null || echo "(free)"
echo "== jobs =="; python3 ~/tantrasara/watch.py --check 2>/dev/null | head -n 8
echo "== board =="; python3 ~/tantrasara/run_queue.py --refresh --dry-run 2>/dev/null | head -n 12
echo "== progress (from EVENTS.jsonl) =="; python3 -c "
import json
from collections import Counter
try:
    evs=[json.loads(l) for l in open('/home/ubuntu/tantrasara/EVENTS.jsonl')]
except OSError:
    evs=[]
for lane in ['tantrasara','shiva']:
    le=[e for e in evs if e.get('lane')==lane]
    ok=sum(1 for e in le if e['status']=='ok'); bad=sum(1 for e in le if e['status']=='FAIL')
    chans=sorted(set(e['chapter'] for e in le))
    print(f'{lane}: {len(le)} events, {ok} ok, {bad} FAIL, {len(chans)} chapters touched')
    for e in le[-3:]:
        print(f'  {e[\"ts\"]} {e[\"chapter\"]}/{e[\"stage\"]} {e[\"status\"]} {e[\"secs\"]}s')
"
