# HANDOVER — Tantrasara explained pipeline (2026-11-02)

All 13 chapters are green and turnkey. To render, you only render.

## Right now (latest first)

- 2026-11-02: ch01 FULL v2 rendering with all 16 terms (diksa/cit cards
  verified on screen). MISTAKES M1–M11 read-first. qwen_watch brief fixed.
  run_all has preflight/verify/cleanup stages. Next agent: run_all for
  ch02–13 (casting all green, glossaries drafted-proposed), then confirm
  glossaries with owner for term cards, then review-pack + ears.
- Previous full video (2 terms only) is STALE, do not link.
- Read `MISTAKES.md` M1–M10 before touching renders or links.
- `qwen_watch.py` brief fixed (dead = no card, subtitles don't count).
- `build_clip.py` prints COVERAGE per build and fails >85% white.
- Single-word Sanskrit goes to granny + term card, never the verse voice
  (verse seat = multi-line passages only).

## State

- Chapters `chapters/ch01.md`–`ch13.md` (ch06 file is `ch06-kaladhva.md`).
  Canonical set only; `tantrasara3` dump ignored forever.
- Storyboards `storyboard_chNN.json` (ch06: `storyboard_ch6.json`): 0 errors
  0 warnings everywhere. Casting fully encoded in `overrides_chNN.json`
  (ch06: `overrides_ch6.json`).
- Glossaries `glossary_chNN.json`: ch01 has 2 confirmed terms, everything
  else proposed (renders as white until confirmed — by design, not a blocker).
- Voices: granny `614f…`, man `fcfd…` (75%), verse `4e87…`, Fish
  `s2.1-pro-free` only. Key: `~/.config/opencode/.env`.
- Renders go to `~/vol` (opencode2 sftp mount — local disk is 98% full,
  never render locally). MMS deps: `/tmp/mssmod` (npm reinstallable).
- Law: `STANDARD.md` (canonical). Skill: `tantrasara-storyboard`.

## Render one chapter (example ch02)

```bash
nohup python3 ~/tantrasara/run_all.py --chapters 02 > /tmp/run02.log 2>&1 &
tail -f /tmp/run02.log
```

## Render everything (overnight, resume-safe)

```bash
nohup python3 ~/tantrasara/run_all.py > /tmp/runall.log 2>&1 &
```

Idempotent: content-hash cache skips finished groups. One chapter failing
never blocks others (see report JSON at end). ~72k words ≈ 8h audio;
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
6. Qwen claims something? Taste only; corroborate timing/identity with
   transcript or waveform. Timestamps past file length void the pass.

## Never

- Never render from a red storyboard. Never default an UNCAST.
- Never commit audio, frames, keys, or model caches.
- Never `rclone copy file remote/path/file` (creates a directory) — use
  `copyto` for exact keys, verify with HEAD (200 + byte match).
- Never trust `rclone mount` reads blindly — retry or `rclone copy` down
  on "Impossible to open"; the mount flakes under load.
- Never split a paragraph to share voices. Never edit frozen JSON by hand.
