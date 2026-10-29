# build/canon/ — THE PRODUCT DATA (empty at intake; this file maps what lands here)

| file | what | written by |
|---|---|---|
| `essay0.json` | THE essay-0: Q + plain + TEXT + audio windows per unit | hand (owner-picked) |
| `assembly_s0_seed.json`, `assembly_s1..6.json` | full-core assemblies (events: bell/Q/pause/plain/breath/verbatim/analayo/water) | make_assembly.py + build_seed.py |
| `newA_manifest.json` | rung A picks (budget 340s/section) | build_newA.py |
| `ladder_manifest.json` | rungs B/C/D picks (budgets 600/1200/2700) | build_rungs.py |
| `film_manifest.json` | film cells (budgets 6/36/90/168) | build_film_manifest.py |
| `segN_{pool,gold,core_v4,script,terms,pads_full}.json` | corpus: pool → gold → core → scripts | assign/scorer + sharpen |
| `manifest_*.txt`, `manifest_index.json` | cut lists, clip census | build scripts |
| `quote_pool.json`, `verbatim_audio_v1.json`, `yt_anchor_map.json` | candidates, quote alignment, YT→DS offsets | align/locate tooling |
| `fish_filter.py`, `blunt_key.json` | THE translation key (deterministic) | hand (owner-vetted) |
| `rhythm.json` (+ `.md`) | silence engine: slots, per-unit overrides, word-pause marks | hand (owner-dated) |
| `voice_match.json` | post-production guide trims (match-archive) | voice_match.py measure |
| `human-scripts.md` | section questions + EMPTY owner intro slots | hand (owner only) |
| `FINAL_ESSAY_TEXT_0A.md`, `FINAL_ESSAY_TEXT_B.md` | complete spoken texts (generated, never typed) | build script |
| `STORYBOARD.md` | full-core shooting script | build_storyboard.py |

Rules: builders read AND write here (axiom 13); verify.sh gates read here;
never hand-edit derived files — regenerate. New artifact? Note it in
BUILD-NOTES.md the same day.
