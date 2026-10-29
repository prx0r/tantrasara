# HANDOVER — start here (2026-10-29: intake, day zero)

You are the next agent on **tantrasara**: Abhinavagupta's *Tantrasara*,
compressed into an argument (six questions, four rungs) and a listening path,
with the analayo-nibbana machine. Nothing here is decoration.

## State: EMPTY (intake)

No primary text ingested. No audio landed. No chain, no seed, no picks.
Everything below is the intake queue — work it top to bottom.

## Intake (in order — nothing downstream starts until its line is green)

1. **Sources (owner):** which text edition (Sanskrit + which translation?),
   whose audio lectures/readings (mp3s?), transcript status (CF-whisper?
   YT subs? nothing yet?). Record the answer in VISION.md + below.
2. **Provenance home:** excavate into `sources/text/excavations/` (quote pools
   with {file,start,end}; NEVER typed verbatim — axiom 1).
3. **Chain:** six section-questions per the FORMULA (12-ARGUMENT); owner picks,
   tests inform. Write them in VISION.md; they are pointers, not topics.
4. **Essay-0:** six repaired units → `build/canon/essay0.json` (THE essay-0;
   builders read it with drift asserts, as in the reference build).
5. **Rungs:** pool → gold → core (scripts ported per 08-PORTING) →
   newA/ladder manifests. First verify run green before any audio.
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
