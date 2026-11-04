#!/usr/bin/env python3
"""Chapter -> group-aligned video chunk parts (canonical chunk method).
Usage: python3 run_blocks.py <storyboard.json> <outdir> [max_secs=600]
Groups are the audio atoms (content-hash cache — audio renders once, never
re-renders); chunks are ranges of whole groups only (M6). Ranges never end
on an owner drop group (the pause bed needs the next group in range).
Writes <outdir>/pN.mp4 + concat.txt. Verify the ASSEMBLED chapter after.
"""
import argparse, json, os, re, subprocess, sys, hashlib, glob

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import holds as H

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]


def _main():
    # no lock here: build_clip claims per range (parent must never hold
    # what its child checks — it would refuse its own parent).
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('storyboard')
    parser.add_argument('outdir')
    parser.add_argument('max_secs', nargs='?', type=float, default=600.0)
    parser.add_argument('--finalize', action='store_true', help='write concat.txt only after every part has a current proof and review')
    args = parser.parse_args()
    sb_path, outdir, cap = args.storyboard, args.outdir, args.max_secs
    if cap <= 0:
        parser.error('max_secs must be positive')
    from factory_contract import (ContractError, chunk_boundary_clears, read_json, require_current_review_pack, require_storyboard_gate,
                                  sha256, validate_bundle, validate_clip_artifacts, validate_schema)
    from proof_contract import require_reviewed_proof
    validate_bundle(sb_path, require_approval=True)
    require_current_review_pack(sb_path)
    require_storyboard_gate(sb_path)
    sb = json.load(open(sb_path, encoding='utf-8'))
    byid = {b['id']: b for b in sb['blocks']}
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    lane = H.lane_for(sb_path)
    groups, cur = [], []
    for b in sb['blocks']:
        if b['id'] == 'b_opener':
            continue
        if b['voice'] == 'none':
            continue
        if cur and (cur[0]['section'], cur[0]['voice']) != (b['section'], b['voice']):
            groups.append(cur)
            cur = []
        cur.append(b)
    if cur:
        groups.append(cur)
    _drops = set(H.drops_for(sb_path))
    groups = H.split_after(H.split_phoneme_groups(groups), _drops)
    sec_seen = {}
    for b in sb['blocks']:
        if b['section'] not in sec_seen:
            sec_seen[b['section']] = len(sec_seen)
    sec_slug = {s: (slug(s) or f'sec{i:02d}') for s, i in sec_seen.items()}
    vols = os.path.expanduser('~/vol/tantrasara/renders')

    def gdur(g):
        # estimate from chars (no mount I/O here — the mount flakes and
        # ffprobes stall; build_clip measures real durations at build).
        # ~15 chars/sec English, ~8 Sanskrit-heavy; ranges are soft caps.
        n = sum(len(x.get('directed', x['text'])) for x in g)
        rate = 8.0 if g[0]['voice'] == 'verse' else 15.0
        return n / rate

    def ends_on_drop(rg):
        return any(b['id'] in _drops for b in rg[-1]) if rg else False

    ranges, cur_r, cur_d = [], [], 0.0
    for g in groups:
        d = gdur(g)
        if (cur_r and cur_d + d > cap and not ends_on_drop(cur_r)
                and chunk_boundary_clears(cur_r[-1], g)):
            ranges.append(cur_r)
            cur_r, cur_d = [], 0.0
        cur_r.append(g)
        cur_d += d
    if cur_r:
        ranges.append(cur_r)
    print(f'chapter={ch} groups={len(groups)} ranges={len(ranges)}')
    os.makedirs(outdir, exist_ok=True)
    concat = os.path.join(outdir, 'concat.txt')
    if os.path.exists(concat):
        import time
        previous = os.path.join(outdir, f'concat.unverified.{time.time_ns()}.txt')
        os.replace(concat, previous)
        print(f'previous concat list preserved as {previous}; current parts need proof')
    parts = []
    for i, rg in enumerate(ranges):
        bids = [b['id'] for g in rg for b in g]
        out = os.path.join(outdir, f'p{i:02d}.mp4')
        audio = []
        for g in rg:
            text = ' '.join(b.get('directed', b['text']) for b in g)
            digest = hashlib.sha1(f"{g[0]['voice']}|{text}".encode()).hexdigest()[:12]
            matches = sorted(glob.glob(f'{vols}/{ch}/groups/{sec_slug[g[0]["section"]]}/*_{g[0]["voice"]}_{digest}.wav'))
            if not matches:
                audio = []
                break
            audio.append(matches[0])
        try:
            if not audio:
                raise ContractError('a required audio group is missing')
            validate_clip_artifacts(sb_path, out, expected_bids=bids, expected_audio=audio)
            cached = True
        except (ContractError, OSError, ValueError) as exc:
            cached = False
            print(f'range {i}: no reusable provenanced part ({exc})', flush=True)
        if cached:
            print(f'range {i}: {bids[0]}..{bids[-1]} ({len(bids)} blocks) -> {out} CACHED', flush=True)
        elif args.finalize:
            raise SystemExit(f'cannot finalize: range {i} is missing or stale')
        else:
            print(f'range {i}: {bids[0]}..{bids[-1]} ({len(bids)} blocks) -> {out}', flush=True)
            subprocess.run(['python3', f'{BASE}/build_clip.py', sb_path, ','.join(bids), out], check=True)
        parts.append(out)
        if not args.finalize:
            proof_dir = os.path.join(outdir, 'proofs', f'p{i:02d}')
            try:
                manifest_path = os.path.join(proof_dir, 'proof_manifest.json')
                manifest = read_json(manifest_path)
                validate_schema('proof-manifest', manifest, manifest_path)
                current = (manifest['machine_passed'] and manifest['video_sha256'] == sha256(out)
                           and manifest['meta_sha256'] == sha256(os.path.splitext(out)[0] + '.render_meta.json')
                           and manifest['subs_sha256'] == sha256(os.path.splitext(out)[0] + '.subs.json')
                           and manifest['gate_sha256'] == sha256(os.path.join(proof_dir, 'gate.txt'))
                           and all(sha256(os.path.join(proof_dir, item['file'])) == item['sha256']
                                   for item in manifest['frames']))
            except (ContractError, OSError):
                current = False
            if not current:
                subprocess.run(['python3', f'{BASE}/prove_clip.py', sb_path, out, proof_dir], check=True)
            try:
                require_reviewed_proof(sb_path, out, proof_dir)
            except (ContractError, OSError) as exc:
                print(f'PENDING_REVIEW: {proof_dir} — inspect each frame, complete review.json, then rerun. {exc}', flush=True)
                return 2
    if args.finalize:
        for i, part in enumerate(parts):
            require_reviewed_proof(sb_path, part, os.path.join(outdir, 'proofs', f'p{i:02d}'))
        list_path = concat
    else:
        list_path = os.path.join(outdir, 'concat.pending.txt')
    with open(list_path, 'w') as f:
        for p in parts:
            absolute = os.path.abspath(p)
            if '\n' in absolute or '\r' in absolute:
                raise ValueError('concat paths may not contain newlines')
            escaped = absolute.replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")
    if args.finalize:
        print(f'parts={len(parts)} reviewed; concat.txt ready (verify the assembled chapter)')
    else:
        print(f'parts={len(parts)} reviewed; run --finalize before assembly')
    print(json.dumps({'chapter': ch, 'ranges': len(ranges), 'parts': parts}))


def main():
    if len(sys.argv) < 3 or sys.argv[1].startswith('-'):
        return _main()  # let argparse print usage
    from factory_contract import require_current_review_pack, require_volume_output, validate_bundle, video_build_lock
    from run_all import storage_preflight
    outdir = sys.argv[2]
    require_volume_output(outdir)
    validate_bundle(sys.argv[1], require_approval=True)
    require_current_review_pack(sys.argv[1])
    storage_preflight()
    os.makedirs(outdir, exist_ok=True)
    # Separate per-output lock: the child still claims the global video lock.
    with video_build_lock(os.path.join(outdir, '.parts.lock')):
        return _main()


if __name__ == '__main__':
    sys.exit(main())
