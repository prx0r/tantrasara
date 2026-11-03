# READINESS — all 22 blocks to exact render, one chain

2026-11-04 (refreshed). Storyboard is the render. There is no separate
rendering process. Publish is a view of the same file, assembly resolves the
same hashes, video burns the same onsets. Anything that changes the picture
changes the storyboard first.

## What was done

All 22 chapters exist as blocks. ch14–22 built on provisional overrides
(476 calls, every one UNSURE in `PROVISIONAL_CASTING_14-22.md`, awaiting
owner M/G). Cards: four term layers (Deva + IAST + T1 literal + final),
count-decided list engine, single-word chant persist, M15 Deva-citation
fix. Whole-chant T1/L3 layers tried and reverted same day — verses stay
Deva + IAST; `mine_verse_gloss.py` output parked proposed in
`verse_gloss_chNN.json`. Text to blocks, group hashing and full-chapter
assembly documented in `BLOCKS.md`. Intro shape and amendable b2 visual in
`INTRO_BLOCKS.md`.

## Validation 2026-11-04

Storyboards all green, 0 errors 0 warnings, 110 blocks in ch01 up to 2106
in ch20. Glossaries: ch01 16 of 16 confirmed (+ T1 literals proposed);
ch02–22 all proposed, which renders as white by design. Approvals: none
exist, so the render gate refuses every chapter. Review packs: ch01 and
ch20 published, manifests approved false, SHAs match current files.
Overrides ch14–22 provisional, unblessed. Storage: local ~0.5G free against
1.0G preflight (batch fails before any token spend), volume has room.
Intro budget flags ch06 and ch14 over 150 words. Golden store empty,
nothing sealed. ch01 sheets rebuild green with the four layers; ch20
sheets build 208 holds green.

## Storyboard with timings and visuals, and how it becomes the mp4

For ch01 open review/ch01/storyboard.md for every block with voice and
first 220 chars, timeline.md for holds in order with confirmed term cues,
and the sheets for the cards themselves. Beats are the directed tags:
slowly on verse, long pause on titles, short pause on dialogue and on
granny catchwords plus colon-enders, audit proving the body untouched.

The same file renders. Groups are consecutive same-voice blocks per
section, one Fish call each, filename carrying sha1 of voice plus directed
text, receipts mapping bids to files. Assembly resolves by that hash never
by stale bid, bell plus 6dB opens, beds deterministic. Clip aligns each
group with MMS, en-IN for narration sa-IN for chant, folding for the
aligner only with one-to-one word map asserted, mean 0.85 minimum,
boundaries at word onsets with gaps belonging to the prior word. Frames
are burned per word onset, holds from holds.py shared with the sheets
(four layers on terms, accumulations on lists, persist on lone chants),
coverage printed with fail over 85 percent white, render_meta.json written
with cuts duration coverage and cue sequence beside the mp4. Verify then
proves geometry levels silence coverage and motion, golden seals the
blessed render and fails later ones on drift. No step improvises.

## Ready

Not yet. Technically green but unblessed. Bless provisional casting for
ch14–22 or correct it, confirm glossaries (and ch01 literals) where cards
matter, publish all 22 and record approved files with matching SHAs, free
local past 1G, grant or trim the two intro exceptions, then ch01 renders
with zero new TTS and seals the golden the rest must match.
