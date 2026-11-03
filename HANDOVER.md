# HANDOVER — Tantrasara explained pipeline (2026-11-04)

All 22 chapters blocked and green. Nothing is approved to render yet.

## Right now (latest first)

- 2026-11-04: four-layer term cards live (Deva + IAST + T1 literal +
  final), list engine locked (count decides shape), single-word chants
  persist one block, M15 Deva-citation fix filed and fixed. Whole-chant
  T1/L3 layers tried and reverted same day — verses stay Deva + IAST.
  Miner `mine_verse_gloss.py` + parked `verse_gloss_chNN.json` (proposed)
  ready for a revisit. Pushed `ce62c38`.
- 2026-11-04: all 22 storyboards green (ch14–22 on provisional casting,
  476 calls awaiting owner M/G in `PROVISIONAL_CASTING_14-22.md`).
  Thumbnails: `assets/thumbnail/chNN.png` (ch01 rainbow only; rest fall
  back to legacy art — wrong art, flagged). No `approved_chNN.json`
  exists, so the render gate refuses everything. Local disk under the 1G
  preflight. Golden store empty.
- 2026-11-02: ch01 FULL v2 DONE + uploaded (16MB, 439s, 898 cuts):
  `https://pub-87169194562a44fcb8279a799d626c62.r2.dev/tantrasara/ch01_full_v2.mp4`
  (pre-layers cut; current cards are richer — re-render on approval).
- Previous full video (2 terms only) is STALE, do not link.
- Read `MISTAKES.md` M1–M15 before touching renders or links.
- Cards print COVERAGE per build and fail >85% white; assert subtitle
  zone, frame edges, pairwise non-overlap, column width.

## State

- Chapters `chapters/ch01.md`–`ch22.md` (ch06 file is `ch06-kaladhva.md`).
  Canonical set is all 22; `tantrasara3` dump ignored forever.
- Storyboards `storyboard_chNN.json` (ch06: `storyboard_ch6.json`): 0 errors
  0 warnings everywhere, ch14–22 provisional. Casting encoded in
  `overrides_chNN.json` (ch06: `overrides_ch6.json`).
- Glossaries `glossary_chNN.json`: ch01 all 16 confirmed (+ T1 literals
  proposed); ch02–22 proposed (renders as white until confirmed — by
  design, not a blocker).
- Voices: granny `614f…`, man `fcfd…` (75%), verse `4e87…`, Fish
  `s2.1-pro-free` only. Key: `~/.config/opencode/.env`.
- Renders go to `~/vol` (opencode2 sftp mount — local disk is full, never
  render locally). MMS deps: `/tmp/mssmod` (npm reinstallable).
- Law: `STANDARD.md` (canonical). Skills: `tantrasara-storyboard` (casting),
  `tantrasara-holds` (cards). Process: `PROCESS.md`. Log: `BUILD-NOTES.md`.

## Render one chapter (example ch02 — blocked on approval + glossary)

```bash
nohup python3 ~/tantrasara/run_all.py --chapters 02 > /tmp/run02.log 2>&1 &
tail -f /tmp/run02.log
```

## Render everything (overnight, resume-safe)

```bash
nohup python3 ~/tantrasara/run_all.py > /tmp/runall.log 2>&1 &
```

Idempotent: content-hash cache skips finished groups. One chapter failing
never blocks others (see report JSON at end). ~137k words ≈ 15h audio;
watch the free-tier usage in `renders/*/receipts/calls.jsonl`.

## When output looks wrong, check in this order

1. Which link/video? Old R2 keys are stale history — always rebuild from
   current storyboard, never trust a previous mp4.
2. Storyboard green? Re-run the builder; block IDs shift when text moves,
   overrides are positional — remap by quote text if needed.
3. Subtitle tofu? Verse blocks must show IAST in subtitles, never
   Devanagari (subtitle face has no Devanagari glyphs).
4. Hold wrong? `holds.py` is shared by sheets and video; fix once there.
5. Timing off? MMS means <0.85 or nonmono >0 — re-check folding
   (precomposed ṃḥṅ need the explicit fold table in `align_group.js`).
6. Deva wrong (स for श)? Display must come from the glossary citation
   Deva, never the folded key (M15) — check the card's data source.
7. Qwen claims something? Taste only; corroborate timing/identity with
   transcript or waveform. Timestamps past file length void the pass.

## Never

- Never render from a red storyboard. Never default an UNCAST.
- Never commit audio, frames, keys, or model caches.
- Never `rclone copy file remote/path/file` (creates a directory) — use
  `copyto` for exact keys, verify with HEAD (200 + byte match).
- Never trust `rclone mount` reads blindly — retry or `rclone copy` down
  on "Impossible to open"; the mount flakes under load.
- Never split a paragraph to share voices. Never edit frozen JSON by hand.
- Never resize Sanskrit per list — one standard Deva 84 everywhere.
