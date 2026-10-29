# AGENTS.md — read this first. Then you know where you are.

You are in **tantrasara**: Abhinavagupta's *Tantrasara* (The Essence of Tantra),
built with the same machine as `../analayo-nibbana` (same gospel, same gates,
same rung ladder). No other repo's rules apply here beyond what this file says.

## Read order (do not skip, do not reorder)

1. **This file** (you are here) — 2 minutes, the map.
2. `BUILD-NOTES.md` — THE LOG. Append-only; it takes precedence over every
   other doc including this one. Latest dated entry wins.
3. `VISION.md` — the owner's intent (north star; taste lives here, not in gates).
4. `HANDOVER.md` — current state: branch, numbers, queue, traps.
5. `../analayo-nibbana/process/RECURRING-MISTAKES.md` — R1 (never author prose)
   and R9 (verify content, not proxies) bite here exactly as hard.
6. `../analayo-nibbana/process/AXIOMS.md` — binding rules (same axioms,
   same numbers).
7. `../analayo-nibbana/process/12-ARGUMENT.md` — the six-slot chain, the
   question formula, the ritual (adapt slots to this text; law unchanged).

## The shape of this repo (mirrors analayo-nibbana post-reorg)

```
AGENTS.md · HANDOVER.md · VISION.md · DONE.md · SPEAKER-RULES.md
TIMINGS.md · BUILD-NOTES.md   living root docs
reviews/                      frozen first-listener reviews (read, never edit)
archive/era-0/                superseded method + intake history
sources/
  lectures/         PRIMARY AUDIO (when landed): audio/ transcripts/ yt-subs/
                    ds-full/ ds-mp3/ cutplans/ (+keeps/)
  text/             PRIMARY TEXT: excavations/ (verbatim home) · readings/
build/
  canon/            THE PRODUCT DATA (essay0, assemblies, manifests, segs, keys,
                    rhythm.json, voice_match.json) — see canon/README.md
  versions/         superseded, dated, do-not-build-from (see VERSIONS.md)
  ears/             ear rounds + ledger (DONE evidence)
  assets/           motto/zoom bells + sfx kit (vatulanatha formula, ported)
process/            port notes + runbooks (the machinery itself lives in
                    analayo-nibbana/process + tools/ — port per 08-PORTING,
                    copy scripts only when this text needs them, retarget D)
tools/              text-specific helpers only (nothing copied preemptively)
```

## Laws (identical to the reference build; violations fail the build)

1. **Gospel:** TEXT VERBATIM → PLAIN ENGLISH → AUDIO. Never author prose —
   not in files, not in chat (R1).
2. **Canon is single-source:** `build/canon/essay0.json` will be THE essay-0
   once built. Builders read `build/canon/`; gates check `build/canon/`.
3. **Gates before and after every change** (verify.sh lives here once the
   pipeline lands; until then, gates run from the reference repo against
   this repo's canon/). NEVER relax a gate; fix the data or the key.
4. **Rungs:** 0 seed ⊂ A newA ⊂ B ⊂ C ⊂ D, archive = reference (not a pass).
5. **Raw model verdicts never gate.** Mechanical claims → meters; text claims
   → whisper/transcript (transcript wins).
6. **Frozen stays frozen:** `reviews/`, `archive/`, BUILD-NOTES history,
   `build/versions/`, era-1 tools. Log new findings; never edit old ones.
7. **Audio never commits.** New artifact → note it in the log the same day.
