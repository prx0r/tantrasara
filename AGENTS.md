# AGENTS.md — Tantrasara factory. Read this first.

22 chapters, one chain. Storyboard is the render. Publish is a view of the
same file. Anything that changes the picture changes the storyboard first.

## Read order

PROCESS.md first, it is the canonical chain. Then BUILD-NOTES.md, the log,
which wins on conflict with anything except PROCESS open deltas. Then
HANDOVER.md for current state, VISION.md for taste, MISTAKES.md for the
fourteen traps, VISUAL.md for the screen law. BLOCKS.md, INTRO_BLOCKS.md,
READINESS.md and PROVISIONAL_CASTING_14-22.md are working notes folded into
PROCESS.md already.

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
