# HANDOVER — start here (2026-10-29: intake, day zero)

You are the next agent on **tantrasara**: Abhinavagupta's *Tantrasara*,
compressed into an argument (six questions, four rungs) and a listening path,
with the analayo-nibbana machine. Nothing here is decoration.

## State: EMPTY (intake)

No primary text ingested. No audio landed. No chain, no seed, no picks.
Everything below is the intake queue — work it top to bottom.

## Intake (in order — nothing downstream starts until its line is green)

1. **Sources (owner — researched 2026-10-29):**
   - TEXT (LANDED FREE, verified): full Chakravarty/Marjanovic at
     `sources/text/reference/tantrasara-chakravarty-marjanovic.txt`
     (gitignored — copyrighted; 11,891 lines, clean text layer,
     from gochema stash). No need to buy the book for the build.
     AVOID the "Gautam Chatterjee" Indian Mind edition (documented
     plagiarism of B.N. Pandit's manuscript).
   - TEXT (Sanskrit, FREE): GRETIL Tantrasara e-text (KSTS ed. base) +
     1918 KSTS Nirnaya Sagara scan on archive.org (public domain).
     shaivism.net hosts a Tantrasara text (provenance TBD).
   - AUDIO+TRANSCRIPTS (BUY): Dyczkowski 54-lecture Tantrasara (ch.1-9) +
     Tantraloka (ch.1-13) course, ~78h + PDF transcripts, $100 at
     anuttaratrikakula.org. This is the build's voice (archive reader +
     explainer, same seat as Analayo/Bäumer).
   - AUDIO (free/adjacent): Lakshmanjoo has NO direct Tantrasara series;
     nearest is Secret Supreme (TL 1-15, free 14.5h audio w/ book) +
     Tantraloka ch.2-3 + Paramarthasara (free audios). Background only.
   - AUDIO (free/orientation — study only, NEVER build from these):
     Wallis "Essence of Tantra" podcast (chapter-by-chapter Tantrasara
     readings + guided meditations, free on Acast) · Nish "Very Heart of
     Tantra" intro ep + free live Zooms (yogawithnish, Mon/Fri) · INDICA
     Abhinavagupta symposium playlist incl. Timalsina intro (free YouTube)
     · Dyczkowski free courses + YouTube (Locating Trika etc.).
   - Record what lands in VISION.md + below, then intake item 2.
2. **Provenance home (2026-10-29 DONE for text):** `build/canon/spans_pool.json`
   = 98 spans, {file,start_line,end_line,quote}, 98/98 verified, contiguity
   checked (tools/build_span_pool.py). Views: spans_gold/core. Beat-level
   excavation of key spans into full quote pools comes with audio.
3. **Chain (2026-10-29 RATIFIED by owner):** 6 questions locked in VISION.md §3.
   Sharpening: Q4 final = "How do I see this?" (owner decree, supersedes
   "Which way in is mine?"); Q6 = "What remains after death?" (owner merge of
   old Q6+Q7). Rebirth = destinations only (faithful — text never teaches
   rebirth mechanics).
4. **Essay-0 (2026-10-29 CANONICAL):** `build/canon/essay0.json` — 6 units,
   questions+plains owner-approved same day ("i love our answers"), text
   anchors line-ranged, alternates kept, audio[] pending audio.
   Process notes: BUILD-NOTES.md (analayo structure, §1-10).
5. **Rungs (2026-10-29 ASSIGNED + PICKED + TEXT GATED):** spans_pool (98) →
   spans_gold (74) → spans_core (32) → beats_core (32) → rung_picks.json
   (A 18.7m <20 · B 51.8m <60 · A⊂B · text-order flow, gate check_picks).
   `bash process/verify.sh` = TEXT GATE + PICKS GATE, ALL PASS.
   Manifests/assemblies/renders come when audio+transcripts land
   (scripts ported per 08-PORTING; rung_picks.json feeds build_newA/build_rungs).
6. **Audio:** render 0 → ears → A → ears → stamp (DONE.md).

## Where everything will live (mirrors the reference build)

- `sources/lectures/` — lecture mp3s + transcripts (when landed).
- `sources/text/excavations/` — the 1st-pass quote pools = verbatim home.
- `sources/text/readings/` — timestamped sermon/reading transcripts.
- `build/canon/` — essay0, assemblies, manifests, segs, keys, rhythm.json,
  voice_match.json, FINAL_ESSAY_TEXT_*.md (see canon/README.md).
- `build/ears/` — ear rounds + EAR_LEDGER.md (DONE evidence).
- `build/assets/` — motto/zoom bells + sfx kit (ported from the reference build).

## Process home (read-only reference until ported)

The machinery lives in `../analayo-nibbana/process/` (00–18 + AXIOMS) and
`../analayo-nibbana/tools/`. Port per `08-PORTING.md` (language layer +
source-specific inputs only; everything structural transfers unchanged).
Copy a script here ONLY when this text needs it, retarget its `D`, and note
the port in BUILD-NOTES.md. Never fork preemptively.

## Traps (inherited, all loaded)

R1 prose reflex · R2 wrong-path reads · R4 memory-claims · R5 happy-path
gates · R6 drifting copies · R9 proxies-not-content (see RECURRING-MISTAKES).
Plus, from hard experience: cache keys cover every input (axiom 16);
`find -xtype l` after any move; whisper is nondeterministic — transcript wins.
