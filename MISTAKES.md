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
