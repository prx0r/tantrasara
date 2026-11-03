#!/usr/bin/env python3
"""Registry timer/alerts: poll background jobs, update REGISTRY.json.
Usage: python3 watch.py [--register NAME PID LOG] [--check]
No sleeping inside — call it to poll. A job is alive while /proc/PID
exists; completion is read from its log tail (report JSON or OK marker).
Finished/failed jobs print ALERT lines and flip their registry stage.
"""
import json, os, sys, time

BASE = os.path.expanduser('~/tantrasara')
REG = os.path.join(BASE, 'REGISTRY.json')


def alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError):
        return False


def main():
    reg = json.load(open(REG, encoding='utf-8'))
    procs = reg.setdefault('processes', {})
    if '--register' in sys.argv:
        i = sys.argv.index('--register')
        name, pid, log = sys.argv[i + 1:i + 4]
        procs[name] = {'pid': pid, 'log': log, 'started': time.strftime('%FT%TZ', time.gmtime()),
                       'alive': True, 'result': 'running'}
        json.dump(reg, open(REG, 'w'), indent=1)
        print(f'registered {name} pid={pid}')
        return
    for name, p in procs.items():
        if p.get('result') not in (None, 'running'):
            continue
        if alive(p['pid']):
            try:
                tail = open(p['log'], encoding='utf-8', errors='ignore').read().strip().splitlines()[-1:]
                print(f'RUNNING {name} pid={p["pid"]} started={p.get("started")} | {tail[0][:100] if tail else ""}')
            except OSError:
                print(f'RUNNING {name} pid={p["pid"]} (no log yet)')
        else:
            try:
                tail = open(p['log'], encoding='utf-8', errors='ignore').read()
            except OSError:
                tail = ''
            bad = ('FAIL' in tail or 'Traceback' in tail or 'EXCEPTION' in tail)
            p['alive'] = False
            p['result'] = 'FAILED' if bad else 'done'
            print(f'ALERT {name} finished: {p["result"]}')
    json.dump(reg, open(REG, 'w'), indent=1)


if __name__ == '__main__':
    main()
