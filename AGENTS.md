# AGENTS.md — Tantrasara factory. Read this first.

22 chapters, one chain. Storyboard is the render. Publish is a view of the
same file. Anything that changes the picture changes the storyboard first.

## Goal (right now)

Render each Tantrasara chapter validated exactly the known way: blocks →
edits → storyboard PNG proofs → bless → perfect mp4 → Qwen final → ears →
seal. `REGISTRY.json` is the live board — stages per chapter, locks, queue.
`run_queue.py` picks the next work. The line never sleeps: while a render
runs, do light prep (gates, sheets, publishes, docs, the shiva lane).

## Rules of the line

- One video build at a time (`/tmp/video_build.lock`) — the builder uses
  fixed `/tmp` paths; concurrent builds clobber each other.
- No approval, no render. Approval is an owner act, never self-granted.
- Renders go to the volume mount, never local disk; storage preflight
  opens every batch (local ≥1G, volume ≥4G).
- Never idle while `REGISTRY.json` has queue: rendering → prep; stuck →
  log it in BUILD-NOTES and take the next queue item.

## Execution discipline (learned 2026-11-04 — never sleep-block again)

- Long work runs under `nohup ... &` with logs to `/tmp/*.log`, then POLL
  with short-timeout reads. Never `sleep N` to wait — sleeps get aborted
  and waste the turn; polls return state.
- Before parallel work, read capacity: `sysload.sh`
  (`cpus=… ram_free=…G load=…`). Video builds stay exclusive regardless
  (lock); prep (sheets, publishes, gates, docs) may parallelize only when
  load comfortably trails cpu count with RAM free.
- Free Fish only, always: every render path calls `tts_line.py`, which
  pins `fish-audio/s2.1-pro-free` on the compat endpoint. Before any
  render batch, dry-run must print ~$0.00 and the model string must read
  `-free`. A paid model string anywhere stops the line cold.

## Awareness (registry timers, not sleep)

- `REGISTRY.json` tracks every active process (name, pid, log, stage).
  Register on launch: `watch.py --register NAME PID LOG`.
- Poll with `watch.py --check`: aliveness via `/proc`, completion from
  log tails, ALERT lines on finish/fail, stages flipped in the registry.
- Never sleep-block on a job. Launch under nohup, register, do the next
  queue item, poll.

## Read order (every agent, no skipping)

0. `RUNTIME.md` — the owner's verbatim gospel and northstar. The routine:
   blocks → edits → storyboard PNG proofs → perfect mp4 → Qwen final pass.
   `PIPELINE.md` is the complete operating manual with readings — read it
   next, before anything else. `NEW-LANE.md` is how to render a new series
   (shiva pattern); `GATES.md` is binary law.
1. `GATES.md` — the binary gate list. Every rule pass/fail, no cheating.
2. `PROCESS.md` — the canonical chain. Then `BUILD-NOTES.md`, the log,
which wins on conflict with anything except PROCESS open deltas. Then
`HANDOVER.md` for current state, `VISION.md` for taste, `MISTAKES.md` for
the traps, `VISUAL.md` for the screen law, `LAYERS.md` for every layer's
source and gate. `BLOCKS.md`, `INTRO_BLOCKS.md`,
`READINESS.md`, `CHAPTER_PREP.md` and `PROVISIONAL_CASTING_14-22.md` are
working notes folded into PROCESS.md already.

## Factory layout

chapters/chNN.md source, ch06 file is ch06-kaladhva.md. storyboard_chNN.json
blocks, ch06 file is storyboard_ch6.json with overrides_ch6.json. All other
chapters use matching chNN names. Thumbnails live in
assets/thumbnail/chNN.png, ch01 rainbow emblem, legacy thumb_ch1.png is
fallback only. review/chNN holds the publish pack and manifest. R2 mirrors
it under svread-audio/tantrasara/review/chNN. Renders live on the volume
mount ~/vol/tantrasara/renders, never local disk, never committed.

## Canonical scripts

run_all.py drives everything: preflight board cast-check publish render mms
assemble holds video verify golden-check review-pack cleanup. Single
chapter dry run first, then overnight batch. build_storyboard,
render_chapter, assemble_chapter, holds_timeline, render_holds, build_clip,
verify_clip, publish_review, golden and holds are the line. Pilot,
firstmin, board, make_card and audit scripts are legacy experiments, read
only, never build from them.

## Run it

python3 run_all.py --chapters 01 --dry-run. Then publish, get the owner
bless recorded as approved_chNN.json with matching SHAs, then render. Green
is 0 errors 0 warnings. Ready is green plus confirmed glossary where cards
matter plus approval plus local 1G and volume 4G free plus golden sealed
after owner ears. ch14-22 casting is provisional until blessed. Proposed
glosses play over white by design. White target 20 percent, fail over 85.

## Laws

Never author prose. Never default an UNCAST. Never split a paragraph to
share voices. Never edit frozen JSON by hand. Never relax a gate, fix the
data. Never commit audio frames caches or keys. Model verdicts never gate:
meters for mechanical claims, transcript for text claims. One concern per
commit, push same day.
