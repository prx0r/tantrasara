#!/usr/bin/env python3
"""Batch driver for the shiva lane: storyboard -> cast-check -> publish.
Usage: python3 run_shiva.py [--chapters s01,s02] [--from STAGE] [--dry-run]
INTAKE ONLY: render/mms/assemble/video stages unlock after owner approvals
plus volume/R2 parametrization (open items in SHIVA-INTAKE.md). Shared
builders stay single-copy; only lane paths live here.
"""
import json, os, subprocess, sys, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIVA = os.path.join(BASE, 'shiva')
CHAPTERS = [f's{i:02d}' for i in range(78)]
STAGES = ['preflight', 'board', 'cast-check', 'publish', 'cleanup']


def sh(*args):
    print('+', ' '.join(args), flush=True)
    r = subprocess.run(args, capture_output=True, text=True)
    tail = (r.stderr or r.stdout or '').strip().splitlines()[-3:]
    for line in tail:
        print('  |', line[:160], flush=True)
    return r.returncode == 0


def stage_preflight(_ch):
    sys.path.insert(0, BASE)
    from run_all import storage_preflight
    storage_preflight()
    return True


def stage_board(ch):
    sys.path.insert(0, BASE)
    from factory_contract import validate_bundle, verify_storyboard_source
    validate_bundle(f'{SHIVA}/storyboards/storyboard_{ch}.json')
    verify_storyboard_source(f'{SHIVA}/storyboards/storyboard_{ch}.json')
    print(f'  | {ch}: frozen storyboard loaded without rewriting it', flush=True)
    return True


def stage_cast_check(ch):
    sys.path.insert(0, BASE)
    from factory_contract import validate_bundle
    validate_bundle(f'{SHIVA}/storyboards/storyboard_{ch}.json')
    print(f'  | {ch}: storyboard and glossary validated', flush=True)
    return True


def stage_publish(ch):
    return sh('python3', f'{SHIVA}/publish_shiva_review.py', ch)


def stage_cleanup(_ch):
    shutil.rmtree('/tmp/shiva_review_holds_s01', ignore_errors=True)
    print('cleanup: shiva review tmp removed', flush=True)
    return True


STAGE_FN = {'preflight': stage_preflight, 'board': stage_board,
            'cast-check': stage_cast_check, 'publish': stage_publish,
            'cleanup': stage_cleanup}


def main():
    args = sys.argv[1:]
    chs = CHAPTERS
    if '--chapters' in args:
        chs = args[args.index('--chapters') + 1].split(',')
    frm = args[args.index('--from') + 1] if '--from' in args else STAGES[0]
    dry = '--dry-run' in args
    stages = STAGES[STAGES.index(frm):]
    print(f'chapters={chs} stages={stages} dry={dry}', flush=True)
    report = {}
    import time as _time
    sys.path.insert(0, BASE)
    from events import log_event
    for ch in chs:
        report[ch] = {}
        for st in stages:
            if dry:
                print(f'[{ch}/{st}] would run', flush=True)
                report[ch][st] = 'dry'
                continue
            _t0 = _time.time()
            try:
                ok = STAGE_FN[st](ch)
            except Exception as e:
                print(f'[{ch}/{st}] EXCEPTION {str(e)[:200]}', flush=True)
                ok = False
            report[ch][st] = 'ok' if ok else 'FAIL'
            log_event('shiva', ch, st, 'ok' if ok else 'FAIL',
                      _time.time() - _t0)
            if not ok:
                break
    print(json.dumps(report, indent=1))
    return 1 if any('FAIL' in stages.values() for stages in report.values()) else 0


if __name__ == '__main__':
    sys.exit(main())
