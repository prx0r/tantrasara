#!/usr/bin/env python3
"""Never-idle queue runner. Usage: python3 run_queue.py [--dry-run]
Reads REGISTRY.json, then either starts the next approved render (setting
the video lock) or prints the next light-prep task. One video build at a
time — build_clip uses fixed /tmp paths. Render stages run under nohup;
this picker never blocks on them.
"""
import json, os, sys

BASE = os.path.expanduser('~/tantrasara')
REG = os.path.join(BASE, 'REGISTRY.json')
LOCK = '/tmp/video_build.lock'


def lock_holder():
    if os.path.exists(LOCK):
        try:
            return open(LOCK).read().strip() or None
        except OSError:
            return None
    return None


def refresh():
    """Recompute stages from files on disk (manifests, approvals, videos).
    Stage labels are derived, never hand-waved."""
    import hashlib
    reg = json.load(open(REG, encoding='utf-8'))
    for ch, st in reg.get('tantrasara', {}).items():
        if not isinstance(st, dict):
            continue
        mp = f'/tmp/ch{ch}_full.mp4'
        man_p = os.path.join(BASE, 'review', f'ch{ch}', 'manifest.json')
        ap_p = os.path.join(BASE, f'approved_ch{ch}.json')
        sb = os.path.join(BASE, 'storyboard_ch6.json' if ch == '06' else f'storyboard_ch{ch}.json')
        gl = os.path.join(BASE, f'glossary_ch{ch}.json')
        man_ok, ap_ok = False, False
        if os.path.exists(man_p):
            try:
                man = json.load(open(man_p, encoding='utf-8'))
                man_ok = all(hashlib.sha256(open(p, 'rb').read()).hexdigest() == man[k]
                             for k, p in (('storyboard_sha', sb), ('glossary_sha', gl)))
            except (OSError, KeyError):
                man_ok = False
        if os.path.exists(ap_p):
            try:
                ap = json.load(open(ap_p, encoding='utf-8'))
                ap_ok = all(hashlib.sha256(open(p, 'rb').read()).hexdigest() == ap[k]
                            for k, p in (('storyboard_sha', sb), ('glossary_sha', gl)))
            except (OSError, KeyError):
                ap_ok = False
        if os.path.exists(mp) and st.get('stage') not in ('rendered-awaiting-ears',):
            st['stage'] = 'rendered-awaiting-ears'
        elif ap_ok and man_ok and st.get('stage') not in ('rendered-awaiting-ears', 'rendering'):
            st['stage'] = 'approved-ready'
        elif man_ok and not ap_ok:
            st['stage'] = 'review-published'
    json.dump(reg, open(REG, 'w'), indent=1)
    print('board refreshed from disk')


def main():
    args = sys.argv[1:]
    if '--refresh' in args:
        refresh()
        args = [a for a in args if a != '--refresh']
    dry = '--dry-run' in args
    reg = json.load(open(REG, encoding='utf-8'))
    holder = lock_holder()
    if holder:
        print(f'video lock held by {holder} — light prep only')
    else:
        for ch, st in reg.get('tantrasara', {}).items():
            if isinstance(st, dict) and st.get('stage') == 'approved-ready':
                print(f'NEXT RENDER: ch{ch} (approved, validated)')
                if not dry:
                    open(LOCK, 'w').write(f'tantrasara-ch{ch}')
                    os.system(f'nohup python3 {BASE}/run_all.py --chapters {ch} > /tmp/runall_ch{ch}.log 2>&1 &')
                    reg['tantrasara'][ch] = {'stage': 'rendering', 'log': f'/tmp/runall_ch{ch}.log'}
                    reg['locks'] = {'video_build': ch}
                    json.dump(reg, open(REG, 'w'), indent=1)
                return
        print('no approved-ready chapter — light prep next:')
    for q in reg.get('queue', []):
        print(f' - {q}')


if __name__ == '__main__':
    main()
