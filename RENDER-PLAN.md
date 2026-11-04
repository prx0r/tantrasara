# RENDER PLAN — all 22 Tantrasara + 78 Shiva Sutras, fastest path (2026-11-04)

> STALE: the Nov-03 batch failed (see EVENTS FAILs + M21). Current
> pipeline is PLAYBOOK.md: bless → audio → chunks → prove → verify
> → ship, one video at a time, this box. Fleet sharding on hold.

Goal: every chapter a verified mp4, goldens sealed, R2 shipped, one film + zip.
Two boxes: opencode3 (here, 6c) runs the main line; opencode2 (4c, volume host)
takes re-runs, then shiva shards. opencode1 joins when reachable.

## Where things stand (measured, not estimated)

- Tantrasara ch01/ch02: rendered, verified, finals on volume. DONE.
- ch03: audio done; 2 groups need re-voicing (verse-split fix); video failed
  (latent sa-IN digit bug, now fixed at source). Needs: render (2 groups) +
  video + verify.
- ch04/ch05: audio complete; videos killed by concurrent /tmp builds from this
  box (proven, owned). Needs: video + verify, clean.
- ch06-22: main batch running (on ch06 TTS now), zero new FAILs. Untouched path.
- ch12/ch22: same digit bug as ch03, fixed at source BEFORE the batch reaches
  them (remapped, re-mined, green). The save of the week.
- Shiva: 78/78 green, canonical flow restructured, s00+s01 voiced, sheets
  green. Blocked on: owner confirms (glossaries/casting/literals), approvals,
  post-batch engine pass (H1+BOOK silence, staged reveal, Deva persist,
  s00-only art, ref-only header, documented [long-break], stale-opath assert),
  render-path parametrization, bells decision.
- opencode2: factory synced, deps + fonts + 569MB aligner + 1.2GB model cached,
  volume symlinked. Blocked once on RAM (onnx peaks ~3.9GB vs 2.5G free);
  /tmp (tmpfs!) cleared 3.7G→1.6G of stale files into a reversible disk stash.
  Align retest pending — expected to fit now (~5.4G avail).

## The plan (critical path first)

1. **Main batch finishes ch06-22 on opencode3.** Nothing competes with its video
   stages — no concurrent builds, ever. ETA ~1-2 days wall (measured ~1.3x
   audio for video+verify, plus fresh TTS for uncached chapters).
2. **opencode2 takes ch04 video the moment align passes**, then ch05, then ch03
   (after its 2 groups are voiced). All video-only; audio is cached on the
   shared volume. Verify outputs HERE, finals to volume.
3. **ch03's 2 groups** get voiced HERE during the next batch video window
   (2 short calls, monitored; 0 FAILs across all prior concurrent TTS), or on
   opencode2 if the owner places a Fish key there.
4. **Seal + ship tantrasara**: per-chapter verify as each lands,
   owner ears, `golden.py seal`, `rclone copyto` + HEAD verify, `release.py`
   film + zip (copy finals back to /tmp for the release step).
5. **Shiva engine pass** (only after tantrasara videos are done — shared code):
   implement the queued list, byte-identical re-proof on all 22 tantrasara
   storyboards, rebuild shiva sheets, republish packs.
6. **Shiva render**: approvals + confirms in hand, then shard units across
   opencode3/opencode2 (/opencode1 if reachable) — TTS is the bulk (~6-10h for
   5.6h audio), video ~5h. Shared volume cache, one video build per box.
   Verify per unit, ears, seal, upload.

## Why the fleet is shaped this way (review of the attempt)

- One video build per box is LAW (fixed /tmp paths). ch04/ch05 died proving it.
- opencode2's aligner needs ~3.9GB (1.2GB fp32 onnx + arena); tmpfs-as-RAM was
  the hidden hog (3.7GB of "disk" was actually RAM). Fix was moving stale
  tmpfs files to disk, not deleting anything. Quantized models would fit but
  change alignment behavior — rejected (gates must match across boxes).
- Never trust an assert on a stale file: node failures hid behind old opaths
  twice (my s01 + ch04/ch05). Builder fix queued: delete opath before aligning.
- opencode1: unreachable from here (no alias/key). Owner action to wire in.

## Owner gates (the true critical path — machines wait on these)

Ears on ch01/ch02 (seal goldens) · ch03-05 re-run blessing (mechanical, assumed
yes) · shiva casting bless (120+3) + glossary/literal bulk confirms · approvals
(all lanes) · drops positions + lengths · book-marker silence + bells call ·
Fish key on opencode2 (only needed for ch03's 2 groups; else voiced here).

## Rules that hold throughout

Free Fish only · no concurrent video builds · renders to volume, finals to
volume/finals, R2 gets review packs + sealed videos only · never commit audio,
frames, keys · code freeze on shared builders until tantrasara videos land
(shiva lane-scoped data work excepted) · every stage logs to EVENTS.jsonl.

## Update 2026-11-04 — back-half failure, recovery in motion
- Batch 1 finished: ch01/ch02 verified. ch03 video (digit bug), ch04/ch05
  video (concurrent-build interference), ch06 video (slug bug) failed;
  ch07-22 refused at the approval gate (M19: full-lane remine changed
  glossary SHAs + wiped Deva citations).
- Fixed: digit splits (ch03/12/22), slug fallback (assemble+build_clip,
  lookup-only), glossaries restored byte-identical (except 03/12/22, which
  kept every data field with refreshed cue_blocks only).
- Continuation batch running NOW (opencode3): 04,05,06,07,08,09,10,11,13,
  14,15,16,17,18,19,20,21,22 — all gate-clean. ch03/12/22 wait on owner
  re-bless (one word — sources changed since approval).
- Audio/chant code untouched throughout (lookup paths + source splits only).
