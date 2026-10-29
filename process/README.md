# process/ — port notes (machinery lives in the reference build)

The engine is `../analayo-nibbana/process/` (00–18 + AXIOMS) and
`../analayo-nibbana/tools/`. Port per `08-PORTING.md` there: everything
structural transfers unchanged (segments, grades, flow audit, provenance,
speakers, gates, rungs); only the LANGUAGE LAYER and source-specific inputs
change (transliteration scheme, key, loanwords, TTS rules).

Copy a script/tool HERE only when this text needs it:
1. Copy, retarget its `D` (repo root) + canon paths.
2. Note the port + reason in BUILD-NOTES.md.
3. The reference copy stays canonical until the port diverges by necessity.

Never fork preemptively — one live copy per script (R6).
Port checklist lives in HANDOVER.md intake item 1–5.
