# MISTAKES — Tantrasara explained (append-only; newest last)

Format: what happened → why → the structural fix. No scolding, no deletion.

## M1. Shipped the wrong video link twice (2026-11-02)
Built ch1_opening2/3/4... while iterating and linked each in turn, so the
owner reviewed stale cuts against current notes. Cause: versioned filenames
with no LATEST pointer and no "superseded" marking. Fix: one canonical name
per deliverable (`ch01_full.mp4`), dated archive copies only; every link
message names what changed since the last link.

## M2. Believed a Qwen clean sweep (2026-11-02)
Qwen scored the full chapter 5/5 with zero findings; I agreed, citing
machine evidence — while ~5 of 7 minutes were blank white. Cause: my brief
defined "dead hold" as blank *with no subtitle movement*, and subtitles move
constantly, so the check could never fire. The judge passed theater. Fix:
`qwen_watch.py` brief defines dead holds as no CARD regardless of subtitles;
`build_clip.py` prints COVERAGE (seconds per hold kind + white_pct) and FAILS
over 85% white on clips longer than 60s. Corroboration is against the
STANDARD (term cards for Sanskrit mentions), not against vibes.

## M3. Subtitle tofu on verse chanting (2026-11-02)
Rendered Devanagari words in the Latin subtitle face during chanting —
every word a hollow box. Cause: assumed the face covered the script; never
render-tested a verse-subtitle frame before shipping. Fix: verse subtitles
render in IAST transliteration (face-owned glyphs); rule recorded in
STANDARD; self-review frames now mandatory at chant start.

## M4. Mixed scripts on one card line (2026-11-02)
First verse card drew Devanagari + IAST on the same line ("garbled").
Cause: no script separation. Fix: `split_scripts()` — Devanagari and roman
never share a line, enforced in code, not taste.

## M5. NFD-strip folding misses precomposed diacritics (2026-11-02)
`unicodedata.normalize('NFD')` + strip-Mn leaves ṃḥṅṭḍṇṣ (U+1E00 block,
no decompositions) intact — broke MMS input (sa-IN rejects them) and term
matching (pauruṣa cue never fired while bauddha did). Cause: assumed
folding is total. Fix: explicit `IAST_FOLD` table before NFD-strip in
`align_group.js`, `build_clip.py`, `holds_timeline.py` — and the missing-
capitals twin (Ā never matched `[ā-ʯ]`) fixed the same day.

## M6. Clip ranges must align to render-group boundaries (2026-11-02)
Requested b1..b15; group spans b12..b24; assert failed. Cause: groups are
the atomic unit (content hash), bids are not. Fix: builder asserts exact
group match — extend the range, never split a group.

## M7. `rclone copy file remote/path/file` creates a directory (2026-11-02)
Uploaded a video to a path that became a folder twice. Cause: `copy`
treats destination as directory. Fix: `copyto` for exact keys, verify
with HEAD (200 + byte match). In STANDARD.

## M8. Concat demuxer chokes on lavfi-generated wav tails (2026-11-02)
"Invalid PCM packet" truncated two assemblies to half length with exit 0
on the demuxer... actually non-zero, but the partial mp3 looked shippable.
Cause: assumed demuxer concat handles all wavs identically. Fix:
filter_complex concat with inline `anullsrc` beds everywhere; assert final
duration against sum of parts.

## M9. Read truncated dumps as complete evidence (2026-11-02)
Decided casting from `head`-cut monitor output and missed half the quotes
in three chapters (wrong IDs encoded). Cause: treated a sample as a
census. Fix: decided only from complete per-chapter UNCAST dumps with
frames; validator confirms zero remaining.

## M10. Agreed with a stale position (2026-11-02)
Told the owner the role line sat in two different places in two messages
because the storyboard moved under me between reads. Cause: reasoning from
memory across turns. Fix: re-read the file before every positional claim
(the 30-second rule — cheap local evidence beats recall).

## M11. Newer term cue swallowed by older span (2026-11-02)
Cue ends came only from structural events, so a 127s samsara span covered
the diksa cue 3s later — her card never appeared while the word was
spoken. Cause: spans assumed sparse cues. Fix: each span clamps at the
next cue start (latest mention wins); coverage printout per build proves
every cue got screen time.

## M12. New storyboard blocks break positional overrides (2026-11-03)
Extracting witness labels to meta inserted blocks mid-stream, shifting every
downstream ID — 192 voice changes in ch13. Cause: overrides key on position.
Fix: remap overrides by text identity (duplicates by occurrence order),
rebuild green, diff same-text voices (only intended changes allowed).

## M13. Cleanup deleted all paragraph breaks (2026-11-03)
A blank-guard `continue` skipped empty lines — 10k lines collapsed, every
paragraph merged. Cause: no diff --stat after the run. Fix: blanks append
first, always; diff --stat after every cleanup; scope with `--only` so
frozen chapters are never touched.

## M14. Batch driver recursed forever on every chapter (2026-11-03)
`sb_path`/`src_path` fell through to themselves instead of formatting the
chapter number — run_all could never run a non-06 chapter. Cause: written
once, never dry-run (`--dry-run` exists and was never used). Fix: paths
format directly; dry-run the driver before trusting it.

## M15. Rebuilt Devanagari from folded glossary keys (2026-11-04)
Folded keys strip ś/ṣ/ṇ (cit-sakti) and `to_deva()` re-transliterated them
as स/स/न — every term card showed चित्-सक्ति (wrong) instead of चित्शक्तिः.
Cause: display text derived from the lookup key instead of the glossary's
citation Deva. Fix: term cards always render `glossary.deva`, IAST derived
from that Deva; folded keys used for lookup only. Sheets and video share
the rule via `holds.term layers`.

## M16. Mixed-script line rendered its roman half twice (2026-11-04)
ch02 b2 ("... — Anupāyaprakāśanam") drew the roman half big in the Deva
face and again small as IAST, and the subtitle karaoke lit both copies in
turn. Cause: verse cards transliterated the whole mixed line instead of
splitting scripts first (M4 existed only in the pilot builder, never
promoted). Fix: `split_scripts` is shared law in `holds.py` — author's
roman half IS the IAST line, transliteration only where no roman exists;
subtitle Deva words blank when the roman duplicates them, karaoke indices
remapped to visible words.

## M17. sa-IN romanizer crashes on digit-only Devanagari tokens (2026-11-04)
Shiva s01 chant "चैतन्यमात्मा ॥१॥" killed `build_clip`: node
`RomanizeError: cleanNativeWord: "॥१॥" has no alphabetic content`, no
output file, stale rows loaded, 1:1 assert fired. Cause: assumed the
aligner tolerates what TTS tolerates (Fish spoke the digits fine).
Tantrasara chants carry ॥ but never digits — that is why they align.
Fix: strip ॥N॥ markers from all 77 shiva chants at source (tantrasara
danda-strip precedent; the ref lives top-right per canon). Rule for both
lanes: verse blocks carry words only, never bare digits or digit-danda
clusters. Rebuild was ID-stable (in-block strip), one chant group
re-voiced, rest cache hits.

## M18. Stale-bid overrides silently corrupt voices (2026-11-04)
Three successive shiva remaps produced green-looking storyboards while
quotes sat UNCAST and stale bids voiced wrong blocks — no error, because
a bid pointing at the wrong block is still a valid bid. Cause: carrying
bids across operations that shift IDs (moves, splits, period appends),
then "verifying" by error count instead of intent. Fix: overrides are
text-anchored, never bid-carried — remap by quoted-span identity
(period-proof, merge-proof), then prove (a) UNCAST count equals pre-op,
(b) every prior voice call honored on identical text (drift audit, zero
tolerance), (c) absolute rules hold (zero Deva in granny script). A remap
is not done until all three pass.

## M19. Full-lane remine after approvals silently unblesses everything (2026-11-04)
Ran mine_glossary.py lane-wide (to refresh 3 chapters' cue_blocks) — it
regenerated all 20 glossaries, wiping every hand-filled Deva citation and
changing every file's SHA. The render gate then refused chapters 07-22
en masse ("glossary_sha changed since approval"). Two harms: data loss
(Deva citations) + mass unblessing. Fix: restore untouched chapters from
git byte-identical (gate passes, no re-bless needed); repair touched ones
surgically (recompute cue_blocks only, preserve every data field —
proven: zero deva/gloss/status/note changes). Rule: miners run scoped
(`--only`, like cleanup) or not at all after approvals; a lane-wide regen
is a re-bless event, never hygiene.

## M20. Tool harness kills background jobs tied to the call (2026-11-04)
Launched the continuation batch with plain `nohup ... &` inside a tool
call that also slept/polled — the harness reaped the whole group twice,
both times mid-assemble, zero logs. nohup does not protect against group
SIGKILL. Fix (fleet pattern, always): `setsid nohup bash -c '...' <
/dev/null >log 2>&1 & disown` in ONE call that returns instantly, then
verify aliveness in a SEPARATE call. Never sleep/poll in the launch call.
Launch is not done until a later, separate call sees the pid working.

## M21. Stale align outputs mask node failures as count mismatches (2026-11-04)
build_clip asserts the opath EXISTS but never that node just wrote it —
a crashed align leaves the previous chapter's rows, and the failure
presents as `b1: 417 vs 3` instead of the real node stderr. Killed three
videos (ch04/05/06 b1) before the pattern was seen. Mitigation now:
clear /tmp/mmsclip before every video run (operational). Fix queued
post-batch: delete opath before invoking node so failures surface.
Contributing factor: rclone mount flaked reads 3x in a row on ch04 wavs
(STANDARD §14 — retry or copy down, never trust a single read).

## M22. Silent stage passes hide blocked assemblies (2026-11-04)
Assemble printed BLOCKED on missing audio yet returned exit 0, so the
batch rolled on into holds and video instead of stopping the chapter.
Same family as M21: failure paths must fail LOUD. Fix: assemble exits
nonzero on missing (dry-run exempt); build_clip deletes stale opaths
before every align. Both are control-flow only — no audio, chant, TTS,
or timing logic touched. Rule: a stage that cannot prove its output
must stop the chapter, never the run.

## M23. Fold-derived Deva is wrong even when it round-trips (2026-11-04)
Machine-filled 462 glossary Devas via to_deva(folded key) with a
round-trip check — and the check is USELESS for exactly the M15 error
class: folding destroys ā/ī/ū + ṇ/ṣ/ś both ways, so wrong forms
(अनुपय for अनुपाय, कुन्दलिनि for कुण्डलिनी) round-trip perfectly.
Reverted all 462 the same hour. Rule, final: Deva enters the lane ONLY
by (1) owner citation at confirm, or (2) verbatim source extraction.
Never by transliteration, however checked. (Pre-existing committed
Devas in ch02-13 carry the same fold-corruption from the old intake
miner — flagged for the confirm pass, not silently edited.)
