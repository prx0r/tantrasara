# HANDOVER — start here (2026-10-29: text side DONE, audio = one owner pick away)

You are the next agent on **tantrasara**: Abhinavagupta's *Tantrasara* (22
āhṇikas) compressed into a six-question argument + essay-0 + graded rungs,
built on the same machine as `../analayo-nibbana` (the 33-sermons build).
Nothing here is decoration. Read `AGENTS.md` first if you haven't; this
file is the state + the map + the exact way forward.

## State today (all verified by gates, not memory)

- Repo: `github.com/prx0r/tantrasara` (public, branch `master`), local
  `/root/tantrasara`. `bash process/verify.sh` = TEXT + PICKS GATE, ALL PASS.
- **Chain LOCKED** (owner): 6 questions — see VISION.md §3. Q4 final
  "How do I see this?" (owner decree); Q6 "What remains after death?"
  (owner merged old 6+7). Rebirth = destinations only (text never teaches
  rebirth mechanics — ruling recorded, don't reopen).
- **Essay-0 CANONICAL:** `build/canon/essay0.json` — 6 units, questions +
  plains owner-approved ("i love our answers"), line-ranged text anchors,
  alternates kept, **`audio[]` empty = the one thing that fills next**.
- **Spans:** `build/canon/spans_pool.json` = 98 spans covering lines
  2436–9842 contiguous, 98/98 quotes verified (tools/build_span_pool.py).
  Views: `spans_gold.json` (74 = A+B), `spans_core.json` (32 = A).
  Grades A32/B42/C24. Per-question: Q1 20 · Q2 6 · Q3 9 · Q4 5 · Q5 47 · Q6 11
  (Q5 fat = structural; manual text).
- **Beats:** `build/canon/beats_core.json` — 32 records (provenance lines,
  verbatim round-trip, plain/tts hygiene, SPOKEN map, sha1 determinism).
- **Rung picks LOCKED:** `build/canon/rung_picks.json` — **A 18.7m
  (<20 target) · B 51.8m (<60)**, A⊂B per question, text-order flow,
  gate `tools/check_picks.py` (wired in verify.sh).
- **Study material landed:** 9 Wallis "Essence of Tantra" mp3s (~4h,
  `sources/lectures/audio/study/`, gitignored) + all 9 transcripts
  (`sources/lectures/transcripts-study/`, committed, tiny) + the
  archive.org "Zero to Hero" course. ALL STUDY-ONLY, never build material.
  Build notes §3.
- **Audio search verdict (§14):** NO free complete Tantrasara reading exists
  anywhere (Boris Marjanovic has Ch.1 only; Wallis stops at ch.5). Owner said
  "no course" ($100 Dyczkowski off the table).

## How to continue — exact next steps

**STEP 1 (BLOCKING, owner): pick the narrator.** The archive seat will be
TTS narration of the Chakravarty text (§14 reasoning: complete, one voice,
free, audio windows exact by construction — kills the whole anchor-snapping
problem). Audition ready — 3 candidates on the SAME TS1.4 passage
(99 words, Q1's A material):
- combined: https://files.catbox.moe/vf2l96.mp3 (wise-old-british →
  elderly-ref → osho)
- files: `build/ears/narration_audition/` (README + singles + combined).
Owner picks; backup recorded in SPEAKER-RULES (17-CASTING law).

**STEP 2 (unblocked the moment the pick lands):** narrate the A spans —
`rung_picks.json` A = 7 spans (TS1.4, TS11.3, TS8.5, TS2.1+TS3.1, TS6.4,
TS16.3) ≈ 2900 words ≈ minutes of Fish TTS (free tier, `s2.1-pro-free`,
reference_id; retry on 503 — Fish flapped twice this week). Then:
1. Fill `essay0.json` `audio[]` windows (each narrated file = exact window).
2. Port the render driver (`../analayo-nibbana/tools/render_a_essay.py`
   pattern — copy, retarget D, set `AUDIO_OUT` ALWAYS) + copy
   `rhythm.json` slots from the reference build (5s plain-breath is house
   style now) — note every port in BUILD-NOTES §.
3. Render seed → mix proof → `voice_match.py check` → G9 → Qwen round →
   ledger → **stamp 0** (DONE.md law: gates + mix + 2 clean rounds + ledger).
4. Same for A. Then B (picks exist, 51.8m), then C decision (film-cells
   keep, owner decides audio).
Full runbook: BUILD-NOTES §13. Change procedures: read
`../analayo-nibbana/process/18-MODIFICATIONS.md` first — edit data →
`validate_sheet`-class check → rebuild → section-scoped render → prove →
log → commit. NEVER re-render everything for a local change.

## File map (everything important, one line each)

```
AGENTS.md                     read-first map + laws (log = precedent)
BUILD-NOTES.md                THE LOG §1–14 (analayo structure; append-only)
VISION.md                     intent; §3 = the locked 6 questions
TIMINGS.md                    rung budget table (A/B measured-proxy rows)
DONE.md                       stamp law + ear taxonomy (copy of reference)
SPEAKER-RULES.md              seats + ritual (guide = KID Q + OLD MAN plain;
                              archive seat = narrator, pending §14 pick)
process/verify.sh             G1-G4 + picks gate — run before any commit
process/README.md             machinery lives in reference repo; port rules
sources/README.md             input layout (what lands where)
sources/text/reference/
  tantrasara-chakravarty-marjanovic.txt   THE TEXT (11,891 lines; gitignored,
  lines 2436–9842 = full translation; 356–2435 intro/summaries; 9874+ notes)
sources/lectures/audio/study/  9 Wallis mp3s + tara course (gitignored, STUDY ONLY)
sources/lectures/transcripts-study/  9 Wallis transcripts (committed, house schema)
build/canon/README.md         what each canon file is + who writes it
build/canon/essay0.json       CANONICAL essay-0 (6 units; audio[] empty)
build/canon/spans_pool.json   98 spans (the assignment; verifier = tools/build_span_pool.py)
build/canon/spans_gold.json   74 = A+B view   · spans_core.json = 32 = A view
build/canon/beats_core.json   32 beat records (verbatim/plain/tts/provenance)
build/canon/rung_picks.json   A 18.7m / B 51.8m picks (gate: tools/check_picks.py)
build/canon/blunt_key.json    dense→plain swaps (owner-driven; mostly identity)
build/ears/narration_audition/  THE AUDITION (owner pick pending)
build/ears/                   future: ear rounds + EAR_LEDGER.md (DONE evidence)
build/versions/               superseded artifacts (VERSIONS.md)
build/assets/                 motto/zoom bells + sfx kit (ported from reference)
tools/build_span_pool.py      span builder + verifier (contiguity + quotes)
tools/build_beats.py          beats_core builder (SPOKEN map, tts hygiene)
tools/verify_text.py          text gate (pool/essay0/beats/census)
tools/check_picks.py          rung-picks gate (budgets/A⊂B/flow/pointers)
tools/transcribe_all.sh       chunked study transcription (setsid-detached)
```

## Machinery: reference repo, not forked

`../analayo-nibbana/process/` (00–18 + AXIOMS + verify.sh) and
`../analayo-nibbana/tools/` are the machine. Port per its `08-PORTING.md`
(language layer + inputs change; structure transfers). Copy a script here
ONLY when this text needs it, retarget its `D`, log the port in
BUILD-NOTES. One live copy per script (R6).

## Locked decisions (do not re-litigate)

- Chain: the 6 questions in VISION §3 (incl. Q4 decree + Q6 merge).
- Essay-0: canonical file, plains signed 2026-10-29.
- Guide cast: KID (`0c0f9d…`) asks, OLD MAN (`98db23…`) answers, backup
  elderly-ref (`f40115…`). Speech says "Nirvana" (data keeps Nibbana).
- Budgets: A <20m, B <60m — picks locked, gates enforce.
- Archive seat: TTS narration proposed (§14), awaiting owner audition pick.
- Study audio: never canon (Wallis/Tara = listening only).
- Rebirth: destinations-only ruling (§5).

## Traps (the ones that actually bit — all inherited)

R1 prose-reflex · R4 memory-claims · R5 happy-path gates · R6 drifting
copies · R9 proxies-not-content (see RECURRING-MISTAKES). Plus hard-won:
- **Cache keys cover every input** (axiom 16) — voice/trim changes ship
  stale audio silently (analayo §92 incident).
- **`find -xtype l` after any move** — symlinks rot under cache hits.
- **Whisper is nondeterministic** — transcript/CF wins; never gate on ASR.
- **Long jobs die with your tool call** — run them `setsid nohup … &`
  (§3 lost two transcription attempts).
- **Fish free-tier flaps** — 503s happen; retry, abort rather than pay.
- **Never render into the wrong dir** — set `AUDIO_OUT` explicitly
  (analayo §98: a B render overwrote A's stamped files).
- Audio never commits; new artifact → note in BUILD-NOTES same day.
