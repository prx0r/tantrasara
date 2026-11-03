# SHIVA HANDOVER — to render-ready (2026-11-04)

78 units intake-complete (storyboards green, sheets green, packs
published). Nothing renders yet. Each item below names its owner and its
unblock command. Nothing here is guesswork — every gate already exists.

## 1. Casting bless (owner: ears + marks)
120 provisional calls + 3 shout calls in SHIVA-INTAKE.md unsure log.
Sheets: `shiva/casting/cast_sNN.md`. Action: mark M/G per sheet, engineer
encodes to `overrides_sNN.json`, rebuild, re-verify green (M12 remap if
text moved). Until then renders would bake unblessed voices — held local,
nothing ships.

## 2. Glossary confirms (owner: bulk confirm)
Zero confirmed terms across 78 glossaries — every card plays white right
now. Action: confirm in bulk per glossary (engineer flips status, never
edits glosses silently), starting with high-frequency terms. Title entries
do not exist yet for shiva intros — draft per chapter on the ch02 pattern
(Deva + literal + final, proposed), then confirm.

## 3. Render-path parametrization (engineer, ~30 min)
`render_chapter.py` / `assemble_chapter.py` VOL dirs and R2 prefixes still
point at tantrasara. Parametrize per `holds.lane_for` (the pattern is
proven in `build_clip`/`render_holds`), targeting
`~/vol/shiva/renders/` + `r2:svread-audio/shiva/`. Then dry-run one
chapter (receipts must show $0.00, free model string).

## 4. Thumbnails + numerals (owner: art + call)
`shiva/assets/thumbnail/series.png` live; openers clean-white-free and
correct. Per-chapter art: supply or bless shared-series for all 78.
Numerals decided (SHIVA-INTAKE.md): sutra ref via the intro header
(1.1 top-right), never the file index — `numeral: False` stays; header
ref+funny optically aligned (139/139, proven s01 + s63).

## 5. Approvals (owner: one word per batch or per chapter)
`shiva/approved_sNN.json` (mirrors `run_all.stage_render` — SHAs pinned,
render refuses without). Blanket order citable like tantrasara's; revocable
by deleting files.

## 6. Batch + seal (mechanical once 1–5 land)
`run_shiva.py` gains render stages (copy the tantrasara stage block).
Overnight nohup, one video lock, preflight storage, free-Fish tracking.
Per chapter: verify → Qwen final (beats vs transcript) → owner ears →
seal golden → upload + HEAD verify.

## 7. Standing blockers (not shiva-specific)
Local disk vs 1G preflight (triaged repeatedly — keep 2G+ headroom before
any batch). Fish free-tier quota tracked in receipts; ~50k shiva words
plus ~130k tantrasara words outstanding.
