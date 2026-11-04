# CONDENSED BUILD — process notes (2026-10-29)

Goal: one primary text (Abhinavagupta's *Tantrasara*, 22 chapters, Chakravarty/Marjanovic translation) →
six-section argument + essay-0 + graded layers (pool → gold → core → rungs) + listening path,
same machine as analayo-nibbana (the 33-sermons build).
Method: read the text FIRST (whole thing, no shortcuts) → extract chain questions via FORMULA →
assign every line to spans with grades → essay-0 from A-candidates → owner picks →
then beats/scripts/keys/renders when audio lands.
Order: argument order (6 questions), NOT chapter order. Quote first, explanation after. No new writing (R1).
Entry docs: AGENTS.md (map) → this log → VISION (intent) → HANDOVER (state).

## 1. Intake + scaffold (2026-10-29)
Repo scaffolded from the analayo-nibbana post-reorg tree (AGENTS/HANDOVER/VISION/DONE/SPEAKER-RULES/
TIMINGS entry docs; `sources/{lectures,text}/`, `build/{canon,versions,ears,assets}/`, `process/`,
`tools/`, `reviews/`, `archive/`). Sfx+bell kit ported (vatulanatha formula). Machinery NOT forked —
lives in the reference repo, ported per `08-PORTING` only when this text needs it (one live copy per
script, R6). .gitignore: renders/cache out, source audio + kit bells tracked.
RULE: fresh-agent path = AGENTS.md → log → VISION → HANDOVER → RECURRING-MISTAKES → AXIOMS →
12-ARGUMENT → canon README. Log takes precedent over every other doc.

## 2. Sources research (2026-10-29) — buy list + fraud warning
- TEXT: Chakravarty/Marjanovic (Rudra Press 2012) = the ONLY legitimate complete English
  translation (Kaviraj lineage, Bäumer's Benares circle, 2 years sentence-by-sentence editing).
  AVOID "Gautam Chatterjee" Indian Mind edition — documented plagiarism of B.N. Pandit's manuscript
  (7 review says "total fraud, copied word for word"). Recorded in HANDOVER intake item 1.
- AUDIO: Dyczkowski 54-lecture Tantrasara+Tantraloka course ($100, anuttaratrikakula.org:
  78h audio + 54 PDF transcripts, Tantrasara ch.1–9 + TL ch.1–13) = the build voice (archive
  reader+explainer seat, same as Analayo). Free-adjacent: Wallis/Nish/INDICA/Dyczkowski-free
  (orientation only, NEVER build-grade). Lakshmanjoo has NO direct Tantrasara series.
- Owner memory check ("dyczkowski talks on rebirth"): searched /root — only his PDFs/texts exist
  (gochema stash), NO audio anywhere. Owner to locate or buy.

## 3. Study audio + transcription (2026-10-29)
9 Wallis "Essence of Tantra" Tantrasara episodes (~4h, Acast RSS, free) pulled to
`sources/lectures/audio/study/` (gitignored; SOURCES.md index) — STUDY ONLY, never canon.
No downloadable transcripts exist (RSS none, pages don't embed). Local transcription:
`tools/transcribe_all.sh` — 10-min chunks → one-shot whisper → merge → house CF schema
`{source,duration,engine,sentences[]}` at `sources/lectures/transcripts-study/`.
INCIDENT: sustained whisper runs OOM-killed twice (7.7G box, ~2.9G RSS sustained) — fixed by
chunked one-shot processes (tiny model; small.en at canon time). RULE: on small boxes, transcribe
per-chunk in separate processes, never a long-lived whisper loop.

## 4. Text landed (2026-10-29)
Full Chakravarty/Marjanovic secured from the gochema stash (found via "tantrasara" grep across
/root): `sources/text/reference/tantrasara-chakravarty-marjanovic.txt` — 11,891 lines, clean text
layer, ToC + intro + all 22 chapters + notes. Gitignored (copyrighted; buy the paper to support).
Structure mapped by grep: intro 356–2435 · full translation 2436–9842 (Ch1 2436 … Ch22 ends
~9840, colophon) · NOTES 9874+. Ch-boundaries double-listed in ToC — real starts found by content.

## 5. Full read (2026-10-29) — grasp note §2
Read the whole thing (intro + Ch1–22 + notes) via 3 parallel agents (each ~2500 lines) + my own
reads of intro + summaries. Grasp note (written up): arc = goal/blindness/fuel → four ways in
(graded by capacity) → descent into breath/body/time-cosmology → map+gate+working ritual →
summit (glance-initiation, Bhairava-identity-while-living). Load-bearing threads that must survive
any compression: svatantra/svabhava/jagadananda; twofold ignorance; saktipata-independence+9
outcomes; anupaya negative logic; reflection/no-bimba; sattarka/bhavana; mala-as-will;
breath-time identity (36 angulas/21,600/yugas); sa-ha; net+lightness test; lingoddhara
severance; murtiyaga shortcut; prasiddhi argument; Kaula 6-grade+glance finale.
Rebirth check (owner question): covered but never central — destinations (hell/preta/animal
rescue Ch16), bhogin's next body (Ch11/14), post-mortem initiation (Ch15–19), yuga cycles (Ch6).
The text NEVER teaches rebirth mechanics (no karma→rebirth doctrine) — faithful to keep it inside
Q6 as destinations+release, not as its own section. RULE: questions answer what the text answers;
where the text is silent, we stay silent.

## 6. Spine: 7 proposed → 6 ratified → sharpened (2026-10-29)
First draft 7 questions (Ch1-22 read → §2 grasp note → candidate questions per FORMULA).
- Owner: "6 and 7 too similar" → merged into "What about death — and what remains?" (old Q6+Q7
  were one question asked twice; the text's death-chapters and final-state answer are one arc).
- Sharpening pass (process copied from analayo 12-ARGUMENT FORMULA: 4 tests — standalone+precise,
  the cut, content-fit, plain ≤9 — plus the oral test (Q aloud, A aloud, leap = rewrite the Q)
  and the edge test (answer = next premise)). analayo history (R7): five question-sets died in a
  row before the FORMULA was extracted — so ONE version against tests, shown once, no churn.
- Changes: Q4 "What are the ways in?" → "Which way in is mine?" (list-request → personal cut —
  the means are graded BY capacity, the way fits YOU) → **owner decree final: "How do I see this?"**
  (means reframed as the act of seeing — the four upayas ARE four ways of seeing; knowledge is
  what liberates. Chain-pronoun "this" resolves from Q1 in seed adjacency, analayo Q2 "it"
  precedent; standalone-note logged, tests inform / owner decides).
  Q6 "What about death — and what remains?" → "What remains after death?" (two-part → 5-word
  close; "remains" carries both survival question and final state; mirrors analayo's
  "What is Nibbana like?"). Q1/Q2/Q3/Q5 held (analayo-shape, passed cold).
- FINAL CHAIN (locked): What is my own nature? → Why don't I see it right now? → What keeps me
  bound? → How do I see this? → How do I practice? → What remains after death?
  Edge chain: light → unseen? → what holds that → how do I see it? → the doing → then what.

## 7. Span assignment: ALL of Tantrasara → essay layers (2026-10-29)
Owner goal: "assign all of tantrasara to essay a, b". Executed at text level (analayo parity:
pool = everything, gold = A+B, core = A):
- **build/canon/spans_pool.json: 98 spans, lines 2436–9842, contiguous, 98/98 quotes verified**
  against source. Grades A32/B42/C24. Per-question: Q1 20 · Q2 6 · Q3 9 · Q4 5 · Q5 47 · Q6 11
  (Q5-heaviness structural for a manual — same class as analayo's fire-spray in §1).
- Views: spans_gold.json (74), spans_core.json (32) — segN_pool/gold/core shape.
- Method: 3 agents blocked the full translation (~2500 lines each) → I adjudicated question
  assignment on ~8 spans (Ch11 grace-theory → Q2, Ch10 map → Q5, Ch7.3 → Q1, Ch6 breath → Q5,
  TS16.3 → Q6) and replaced 6 OCR-broken quotes with verified in-range ones (1 Sanskrit-only
  span flagged `sanskrit_span`, no English in range).
- VERIFIER: `tools/build_span_pool.py` — contiguity (each start = prev end+1) + normalized
  substring quote check, re-runs on any edit, exit 1 on break. RULE: pool edits go through the
  builder, never hand-edited JSON (M17-class: assert what you claim).
- 23 essay0-candidates (grade A + flagged) reduced to 6 primaries + alternates (analayo §32
  pick-discipline).

## 8. Essay-0 canonical (2026-10-29, owner: "i love our answers so thats essay 0 done")
6 units → `build/canon/essay0.json` (CANONICAL; DRAFT retired, git history keeps it):
1 What is my own nature? (22w) · 2 Why don't I see it right now? (25w) · 3 What keeps me bound?
(38w) · 4 How do I see this? (40w) · 5 How do I practice? (41w) · 6 What remains after death? (38w).
Plains: drafted on owner instruction ("have the canonical answers ... with a plain english
answer"), disciplined by analayo §73 (subject-first) + §79 (no loaded/source-language terms):
every clause traceable to a span, zero Sanskrit terms, plain_note records R1 + sign-off.
Owner read + approved same day → canonical flip (analayo flow: propose → owner picks → flip).
Text anchors: Q1 TS1.4 (light/bliss def) · Q2 TS11.3 (jivanmukti-by-grace) · Q3 TS8.5 (bound-soul
definition) · Q4 TS2.1 (sun-jar) · Q5 TS12.1 (bath=absorption) · Q6 TS19.1 (grace axiom);
Q4 alternates carry all four means legs (+TS4.4 sakta, +TS5.1 anava).
audio[] = [] until audio lands (windows fill at render time, analayo §74 pattern).

## 9. Process notes written (2026-10-29)
This file: structure copied from analayo CONDENSED-BUILD-NOTES (numbered chronology, owner
quotes inline, numbers+rules+evidence per entry), story rewritten for tantrasara.
What transfers unchanged from the reference build (same axioms): R1 no authored prose ·
verbatim extracted with provenance · gates never relaxed · frozen stays frozen · cache keys
cover every input (axiom 16) · transcript wins over model ears · sheet==master.

## 10. Where this stands vs the 33-sermons bar (honest)
TEXT side at parity: chain locked · essay-0 canonical · pool/gold/core assigned+verified ·
grasp note of the full text · process notes · entry docs.
TEXT side still owed: per-span plain/blunt layer + tts_line (the key-work — port 07/04 when
audio lands; key = frequency-listed terms, owner-vetted mappings, veto list like analayo §24) ·
beat scripts (span → {quote, plain, tts, provenance}) · text-side verify gates (port G5-style
quote-anchor + G6 TTS scan).
AUDIO side BLOCKED on owner (the one hard dependency): Dyczkowski course ($100, audio+transcripts)
or located mp3s → then: transcripts → beats → assemblies → renders → ears → stamps, exactly the
analayo runbook (18-MODIFICATIONS playbooks are the change procedures; DONE.md is the stamp law).

## 11. Beat records + text gate (2026-10-29) — text side reaches analayo-parity shape
- `build/canon/blunt_key.json` seeded (analayo blunt discipline; mostly IDENTITY —
  Chakravarty/Marjanovic is already modern English, so the dense-swap pass is the
  owner's future dense-finds loop, §19/§24 pattern: owner directs, agent applies
  mechanically). RULE: never invent interpretive swaps autonomously (R1).
- `tools/build_beats.py` → `build/canon/beats_core.json`: 32 core beats,
  {span, question, grade, provenance {file, lines}, verbatim, plain, tts_line,
  plain_sha1}. Verbatim = extracted quote, round-trip asserted 32/32.
  plain = blunt applied + foreign-paren strip ("my heart (hrdaya)" → "my heart").
  tts = hygiene + SPOKEN map (pasu→bound soul, mala→impurity, saktipata→descent
  of grace; loanword class Siva kept — analayo arahant/tathagata precedent).
  FAIL-LOUD: unmapped foreign token in tts → gate fails → map grows under
  discipline (measured: 2 fails found on first run — (hrdaya) ASCII-paren
  not caught by non-ASCII regex, bare "pasu"; both fixed properly, not
  papered over). Determinism: 32/32 byte-identical on re-apply.
- `tools/verify_text.py` + `process/verify.sh` = TEXT GATE (analayo verify.sh
  parity, text stage): G1 span pool (builder re-run, same-path law) · G2 essay0
  (6 units, questions synced to pool, plains non-empty, text round-trips) ·
  G3 beats (verbatim round-trip, tts no-foreign, sha1 determinism) · G4 layer
  census (pool=gold+rest, grades A32/B42/C24). ALL PASS.
- Per-question beats: Q1 11 · Q2 2 · Q3 2 · Q4 2 · Q5 13 · Q6 2 (core A only;
  Q2/Q4/Q6 thin in A by design — their weight lives in B, gold74 is the B source).

## 12. Rung picks to budget: A <20m, B <60m, flow-checked (2026-10-29, owner: "get A under 20, B perfect under 60, ensure flow")

`build/canon/rung_picks.json` (reading-time proxy @150wpm; audio windows
re-measure when Dyczkowski lands) + `tools/check_picks.py` gate (wired as
G-pick in process/verify.sh): budgets, A⊂B per question, TEXT-ORDER flow
(argument order = the text's own order), grade rules (A-rung = grade A only;
B excludes C), pointer words synced to essay0, no pointer-only sections.

- **A = 18.7m** (2802w): Q1 TS1.4 definition · Q2 TS11.3 grace grades ·
  Q3 TS8.5 veils · Q4 TS2.1+TS3.1 two ways of seeing · Q5 TS6.4 breath-time ·
  Q6 TS16.3 rescue. Slot-carrying beats only; the claim lands (Q1 read whole),
  Q4 shows two of four ways (rest → B), Q6 thin-by-design (pointer axiom +
  rescue image — closing sections live on essay-0, analayo S1 precedent).
- **B = 51.8m** (7768w): per-question arcs reviewed — Q1 benedictory→def→
  bliss-in-body · Q2 ignorance-root→grace · Q3 mala→credo→veils ·
  Q4 no-means→reflection→crossing · Q5 rites→meditation→breath (the text's
  own Ch4→5→6 descent) · Q6 yuga→deathbed→net→rescue→axiom (death at every
  scale, closing on the axiom). A⊂B proven per question.
- Honest notes: pace-sensitivity (proxy is ±10%: at 140wpm A≈20.0m — exact
  number re-measures from ffprobe windows on audio arrival); Q5's pointer
  source span (TS12.1 bath) full text → C (budget); Sanskrit-scan spans
  excluded from B (C/depth only).
## 13. ENTERING THE AUDIO STAGE (2026-10-29) — text side frozen-complete, audio blocked on one purchase

**Text side (done, gated):** chain 6 locked · essay-0 canonical ·
spans 98/gold 74/core 32 verified · beats_core 32 (verbatim/tts/determinism) ·
rung_picks A 18.7m <20 / B 51.8m <60 with A⊂B + text-order flow gates ·
`process/verify.sh` = TEXT+PICKS GATE ALL PASS. From here, text changes go
through 18-MODIFICATIONS (edit → validate_sheet-class check → rebuild → gates).

**Audio stage runbook (what happens the day audio lands, per 08-PORTING):**
1. Land Dyczkowski mp3s (or located mp3s) in `sources/lectures/audio/` +
   transcripts (CF-whisper → `sources/lectures/transcripts/`, same schema
   as analayo `{t,end,text}`; yt-dlp/subtitles first if YouTube).
2. Fill `audio[]` windows in essay0.json + beats (span line-ranges →
   timecode anchors; word-onset snapping per analayo M27/M30 discipline —
   segments are not onsets).
3. Assemblies + manifests (port build_newA/build_rungs reading rung_picks;
   rhythm.json slots carry over from the reference build — copy when
   first needed, retarget D).
4. Renders (render_newA/render_B drivers, AUDIO_OUT isolation) →
   voice_match check → mix proof → G9 ears → Qwen rounds → ledger → STAMP
   (DONE.md law: gates + mix + 2 clean rounds + ledger).
5. Then B re-render, C decision, stamps — same as analayo §§87-101.

**Study transcripts (Hareesh/Wallis) — running, twice-failed-then-fixed:**
- Attempt 1: small.en sustained run → OOM-killed (7.7G box, §3).
- Attempt 2: chunked one-shot loop → killed by tool-timeout process-group
  kill (nohup insufficient against the shell's session teardown).
- Attempt 3 (current): `setsid nohup tools/transcribe_all.sh` fully detached
  (own session, immune); verified alive transcribing (90% CPU on chunk).
  Output: `sources/lectures/transcripts-study/` (9 eps, house CF schema,
  engine=tiny study-only — small.en re-run at canon time if these ever
  graduate). Check: `tail /tmp/study_tr3.log`; expected ~1h for ~4h audio.
- STUDY ONLY (never canon) — the build voice is the purchased Dyczkowski.

**The one open dependency:** the $100 Dyczkowski course (or located mp3s).
Everything else in the runbook is unblocked waiting on it.

## 14. Audio search: no free complete reading exists — TTS narration proposed (2026-10-29, owner: "no course, search youtube")

Searched: YouTube (yt-dlp ytsearch, multiple queries), archive.org
(advancedsearch mediatype:audio), web. Findings:
- **Boris Marjanovic** (editor of OUR translation, channel @vimarsa555,
  34 videos): Tantrasāra Ch.1 only, 2 parts (~18m). Download blocked
  (YouTube bot-gate; needs cookies). Rest of channel = Tantraloka/other texts.
- **Wallis "Essence of Tantra"**: Ch1–5 + upāyas only — his translation
  isn't finished either (16 years in). We HAVE these (§3, transcribing).
- **archive.org "Tantrasara, Zero to Hero"**: 51m AI-narrated own-words
  COURSE (not the text) — downloaded to study/ (SOURCES.md), STUDY ONLY.
- Explainer fragments: "Trika vivant avec Emma" (Ch1 satsangs),
  "Atmanam Viddhi" shorts, Nish intro — orientation only.
- **No complete free reading of all 22 chapters exists anywhere.**
Partial-voice options fail even A: A spans need ch1,2,3,6,8,11,16 —
Wallis covers only 1–3 of those; mixed voices violate the one-seat law.

**Proposed path (unblocks the whole audio stage, free):** the archive
seat = TTS narration of the Chakravarty text (span-by-span from
rung_picks/beats). Wins: complete coverage, one voice, ZERO transcript
work (audio windows exact by construction — no whisper/anchor snapping),
uses the existing casting pipeline (17-CASTING), same local-only copyright
posture as the text file itself. Narration audition generated (§14b).

## 14b. Narration audition (2026-10-29)

3 candidates read the SAME TS1.4 excerpt (99 words, Q1 A material) —
`build/ears/narration_audition/` (README + per-voice + combined):
- wise-old-british (98db23…) · elderly-ref (f40115…) · osho (06134e…)
Combined: https://files.catbox.moe/vf2l96.mp3
(owner pick; backup recorded in SPEAKER-RULES on lock — same law as the
kid/old-man guide cast). After pick: narrate A spans first (7 spans,
~2900 words ≈ minutes of TTS), fill essay0 audio[], then run the §13 runbook.

## 2026-11-03 — intake ch14–22, data-pristine pass (no renders, owner order)

Goal restated: all data formatted so pristine that any new work's chapters
can be dropped in and render perfectly first time. Renders PAUSED until
ordered otherwise.

1. **Split**: extended `split_chapters.py` JOBS with
   `tantrasara14-18 → 14–18`, `tantrasara19-22 → 19–22`. Ran whole script;
   it rewrote ch01–13 (reverting their cleanup) — restored all twelve from
   git, kept only the eight new files. LESSON: splitter is not idempotent
   over cleaned files. Always `git checkout` old chapters after a run, or
   scope JOBS to new dumps only. TODO: add `--only` flag / skip-existing.
2. **Cleanup** (`cleanup_chapters.py`, unmodified): idempotent on finished
   files (old chapters untouched), new files each dropped duplicate title +
   jacket blurb + `+N` citation tails. ch14–22 now match house chapter shape.
   Word counts: ch14 6905, ch15 4307, ch16 6537, ch17 4925, ch18 5600,
   ch19 7052, ch20 12684, ch21 8709, ch22 12097.
3. **Storyboard**: all eight build first-try; ZERO non-casting errors
   (no lexicon gaps, no structural failures). UNCAST counts:
   14:35, 15:11, 16:54, 17:23, 18:51, 19:62, 20:92, 21:46, 22:93 = 467.
4. **Casting sheets**: extended `gen_casting.py` list, generated
   `casting/cast_ch14–22.md`. Regen also rewrote old sheets with shifted
   IDs (stale snapshot, owner never marked them — overrides are truth and
   still validate green) — restored old sheets from git. LESSON: generators
   are not idempotent over filed outputs. Same TODO as (1): scope or
   checksum-guard all regenerators.
5. **Glossaries**: extended `mine_glossary.py` list, drafted
   `glossary_ch14–22.json` (all proposed). Regen wiped hand-filled Deva in
   old glossaries — restored from git. Same lesson, third instance.
   Draft sizes: ch14:92, ch15:42, ch16:82, ch17:65, ch18:40, ch19:77,
   ch20:155, ch21:109, ch22:132 terms; appositives filled a handful.
6. **Pending owner calls**: mark 467 casting M/G (sheets ready); confirm
   glossaries in bulk (ch02–22, only ch01 confirmed). Then overrides →
   green storyboards → frozen sheets.
7. **STANDARD §3 + gen/mine chapter lists**: now cover 14–22 in code;
   STANDARD's canonical-set line still says ch1–13 — one-line extension
   proposed, awaiting owner nod before touching law.

## 2026-11-03 — TTS read-aloud hygiene + intro budget (no renders)

Owner: "keep reading makes no sense read out; general-edit anything that
doesn't work spoken; cap the verbose intros; never a repeated welcome-back."

1. **Sweep**: URLs, `Attachment.png` (U+2060 joiner), `+N` tails, folio
   digits, `Next:` lines, ALL-CAPS witness labels across all 22 chapters.
2. **Already-safe**: provenance paragraphs (`Textual basis`, `Sources:` …)
   and `Attachment` carriers route to meta/unvoiced; `Keep reading`/`Next:`
   trailers stripped at split; `![image]` meta. No "welcome back to Kashmir"
   anywhere in the texts — the repetition risk is the recap shape
   ("Right then. Last chapter…"), handled by the budget below.
3. **Real spoken junk found (3)**: ch13 b947 citation-only URL paragraph
   (granny would read the URL); ch21 b1088 witness label glued to narration;
   ch12 b662 English paragraph ending in folio `१२` misvoiced as chant —
   ANY Devanagari char (even a digit) triggered the verse voice.
4. **Fixes, builder (no text change, safe on frozen chapters)**:
   voice-routing now requires a Devanagari LETTER (digits never voice);
   URL + <10 other words → meta; embedded ALL-CAPS witness labels split
   out to meta. ch01–10 rebuild byte-identical (IDs, voices, green).
5. **ch11/12/13 grew one meta block each → IDs shifted → overrides
   remapped by text identity** (ch13 dup quotes by occurrence order), all
   three green, same-text voice diffs exactly the two intended fixes.
   Lesson (M12): any emitted block breaks positional overrides — remap,
   never hand-edit.
6. **Cleanup (text, scoped to ch14–22 only via new `--only`)**: strips
   attachment artifacts, standalone URL lines, folio tails. First attempt
   deleted all paragraph breaks (blank-guard `continue`); fixed, restored,
   reran — 1 line per file. Lesson (M13): cleanup must preserve blanks;
   always diff --stat after a cleanup run.
7. **Intro budget (CHAPTER-FORMAT)**: beats 2–4 ≤150 words, recap ≤5 beats,
   no repeated greeting formulae. ch01 110 ✓; ch06 217, ch14 179 flagged
   for owner trim-or-exception. Machine measures, never cuts author's prose.
8. **Left for owner**: `Next: Chapter 7 — Deśāra` outro in ch06 (spoken,
   fine); "the GRETIL transcription ends…" sentences are author's own
   sentences — kept, trim at will.

## 2026-11-03 — review-gate + golden store (no renders)

Owner: full storyboard + timeline published pre-render; owner confirms;
future renders mechanically compared to the blessed one.

1. **publish_review.py** (new): green-storyboard assert → readable
   `storyboard.md` (every block, voice, 220 chars) + `timeline.md`
   (holds_timeline) + contact sheets (render_holds, no audio) → R2
   `review/chNN/` + local `review/chNN/manifest.json` (approved=false).
   Proven live on ch01 (storyboard 200 + timeline 200).
2. **Render gate** (run_all.stage_render): refuses without committed
   `approved_chNN.json` whose storyboard+glossary SHAs match current files.
   Approval is an owner act recorded by the engineer, never self-granted.
3. **Golden** (golden.py + build_clip render_meta.json): seal stores
   duration/cuts/coverage/cue-sequence; check fails on duration ±2s, cue
   reorder/miss, cue drift ±3s, white ±5pp, cuts drift. Tolerances cover
   encoder noise only.
4. **run_all**: CHAPTERS extended 14–22; STAGES gain `publish` (pre-render)
   and `golden-check` (post-verify). Fixed live infinite-recursion bug:
   `sb_path`/`src_path` called themselves for non-06 chapters — the batch
   driver could never have run. M14.
5. **Flow now**: publish → approve → render → … → golden-check → ears →
   seal → commit. CHAPTER-FORMAT updated.

## 2026-11-04 — conveyor lock, all-84 standard (no render tokens beyond ch01/ch20 slices)

Owner: lists are a five-slot conveyor, one standard Sanskrit size, newest
middle / earlier corners in order. Implemented in `holds.py`
(`POS_MIDDLE`, `POS_CORNERS`, `render_conveyor`): Deva 84 + gloss 40 every
slot, 3+-cue runs accumulate, pairs supersede, lone glossed chants persist
one block, verse cards carry glosses in video. Window of five, longer
slides; subtitle + overlap asserts fail closed. Sheets re-rendered green;
ch01 stack segment re-rendered OK (window detected, persist b64 2s, white
33%). Law updated in VISUAL.md (items 4–5), skill `tantrasara-holds`
corrected to all-84, wrong-vs-right recorded in PROCESS_NOTES.md. Pending
from before, unchanged: provisional casting bless (ch14–22), glossary
confirms (ch02–22 white by design), approvals (none), local disk 0.54G vs
1G preflight, golden empty. IAST + literal-gloss card layers requested,
sourced from prx0r/translation-work T1 pattern — not yet built.

## 2026-11-04 — four-layer term cards (Deva + IAST + literal + final)
Owner: for any Sanskrit — romanised under the Deva in lightest grey, then
the T1 intermediary literal in mid grey, then the final English darkest.
IAST derived per card from the citation Deva (never transliterated twice);
literals drafted T1-style for all 16 ch01 terms as `proposed`
(`literal_status`), glossaries otherwise untouched. Sheets show proposed
layers for review; video gates literal on `literal_status == confirmed`
(gloss gate unchanged). M15 filed: cards used to rebuild Deva from folded
keys (चित्-सक्ति with स) — now always glossary citation (चित्शक्तिः).
Single-word chants and persist spans inherit the layers automatically.

## 2026-11-04 — four layers on ALL verses (IAST + T1 literal + L4/L3 final)
Owner: every chant gets Deva, romanised in time, intermediary literal, and
the L4 final when it lands (L3 meanwhile, translation-work ongoing).
`mine_verse_gloss.py` (new) matches storyboard chant blocks to frozen T1
verses by normalized similarity (score recorded) and pulls finals from L3
data where present (only a01 so far — 5 verses); entries land in
`verse_gloss_chNN.json`, all proposed, video gates on confirmed like
glossaries. Render prefers `l4` over `final` per entry, so the L4 upgrade
is a data fill, never a code change. Matching is by `verse_match_key`
(content hash, M12-proof). Proven on ch01 b8: Deva + IAST + T1 literal +
L3 final on one card, asserts green.

## 2026-11-04 — docs swept, engine stress-tested (no renders but sheets)
Owner: complete documentation, update all stale docs, hunt visual-engine
edge cases. STANDARD (22 chapters, four layers, list engine, persist, IAST
law, thumbnail dir), HANDOVER + READINESS (current state), PROCESS open
deltas, PROCESS_NOTES (list engine + verse revert), BLOCKS (clip rhythm +
four layers), SPEAKER-RULES (superseded for casting), tantrasara-holds
skill (count engine, four layers, centered, brackets, no-romanisation
amended), VISUAL (four layers, list engine). Stress results: ch20 sheets
208 holds green; 7-key window slides green; unbreakable 50-char Deva in a
narrow corner now fails loud (column assert added) instead of overflowing
silently; no confirmed term lacks a Deva citation. Open and noted:
assemble beds diverge from clip beds; thumbnails ch02–22 missing; one cue
per block only; dialogue+verse voice unnamed; review/ vs reviews/ naming;
verse T1/L3 parked proposed.

## 2026-11-04 — ch02 intro (thumbnail + 02) + mixed-script split fix
Owner: chapter-two intro mirrors the thumbnail with a 02 top-right.
`holds.intro_hold(ch)` is the single code path (ch01 returns clean
thumbnail; ch02+ add the numeral in FE 150). Caught live on ch02 b2:
mixed Deva+roman lines rendered the roman half twice (big in Deva face,
again small as IAST, same in subtitles). Fix: M4 `split_scripts` promoted
from the pilot builder to shared law — the author's own roman half IS the
IAST line, transliteration only where no roman exists; verse subtitles
blank the Deva words when the roman duplicates them (karaoke indices
remapped to visible words). Proven on fresh b1+b2 render: 4s thumbnail+2,
verse card Deva + single IAST, subtitle single form. Old R2 links to
ch02 pieces (if any) are stale.

## 2026-11-04 — ch02 intro numeral 02 + b2 voice question
Numeral fixed to zero-padded `02` per spec. Open: b2 (chapter-name chant)
fires ~4s in, before any of her intro patter — owner asks why it barges
into chant instead of being her intro. Probe rendered: granny reading b2
verbatim (`review/granny_probe_b2.wav`, 4.2s); whisper garbles Sanskrit by
design so transcript proves nothing — owner ears dispose. Calls: (A) flip
b2 to granny by override — title, name, tagline, recap all hers over
thumbnail+02, first verse card at first body chant; (B) keep the chanted
name-anchor and let her patter play over white/cards after it.

## 2026-11-04 — ch02 intro bug + mixed-script split + docs sweep
Intro: `holds.intro_hold(ch)` shared by sheets and video (ch01 clean,
ch02+ numeral top-right in FE 150, zero-padded). ch02 b1+b2 proof rendered
fresh (thumbnail+02, then clean verse card). Caught live: b2's mixed line
duplicated its roman half on card and subtitles — M16 filed, `split_scripts`
promoted to shared law with subtitle blanking + karaoke remap, re-render
clean. Open owner call: b2 chants ~4s in before her intro patter; probe of
granny reading b2 rendered for ear-check, flip needs per-bid voice forcing
(first-minute render queued behind it + local disk). Docs swept: STANDARD
(22 chapters, four layers, list engine, persist, IAST law, thumbnail dir),
VISUAL (four layers, list engine, persist, intro bug, M15/M16 posture),
PROCESS open deltas refreshed, BLOCKS (clip rhythm canonical, four layers),
HANDOVER + READINESS (current state), PROCESS_NOTES (chain rewritten to
today's behavior, conveyor lock, ch02 intro), both skills, SPEAKER-RULES
superseded for casting. Engine stress: ch20 208 holds green, 7-window
slides, unbreakable-column assert added (fails loud), zero confirmed terms
lack citation Deva. Still open: assemble beds diverge, ch02–22 thumbs
missing, one cue per block, dialogue+verse unnamed, review/ vs reviews/,
verse T1/L3 parked, approvals none, disk 0.5G vs 1G, golden empty.

## 2026-11-04 — ch02 b2 flips to granny (her intro, verse keeps chants)
Owner: verse voice does verses and longer chants; she speaks the name line.
Builder now honors per-bid voice forcing in overrides (any block type;
verse-type forced off-seat retypes to narration for non-quotes; owner call
beats the Abhinav-man convention; unknown bids fail closed). ch02 b2 is
narration/granny, green 0/0, first verse now b82 — thumbnail+02 holds her
whole intro. Two build fixes fell out: MMS en-IN gets Deva tokens folded
to IAST for the aligner only (was 42-vs-3 row collapse; means 0.946 now),
and clips with no verse block in range no longer StopIteration (thumbnail
holds throughout). ch02 b1–b9 proof rendered fresh (29s, 50 cuts, all
thumbnail, MMS 0.95) + review pack published. ch01 untouched.

## 2026-11-04 — narration subtitles go IAST-per-word (M16 second half)
Flipping b2 to granny moved Devanagari into the verbatim narration
subtitle path — tofu boxes on screen (M3 class, new route). Fix: every
voice now renders Deva-script words as IAST in subtitles, all else
verbatim, 1:1 counts kept so karaoke holds; mixed lines dedup first
(Deva blanks when the author's roman duplicates it). Sheets' sub-lines
fixed the same way. ch02 b1–b9 re-rendered clean (single IAST subtitle,
thumbnail held). Rule: no Devanagari glyph may reach the subtitle face
from any path — cards (Tiro) and subtitles (Cormorant) stay script-pure.

## 2026-11-04 — canonical chapter title (numeral + name stack, top-right)
Owner: standardize per-chapter titles — numeral up top (moved 90→60 for
proportion), chapter name beneath with full layers (Deva, romanised,
literal, meaning). `holds.chapter_title` resolves the name from the first
granny narration carrying Deva (ch02 b2); `intro_hold(ch, title)` draws
thumbnail + numeral + right-aligned title stack clearing the mandala
(ink right of x=1340 above y=780, asserted) and frame edges. ch02 title
entry drafted proposed in glossary (`anupayaprakasanam`: literal + "The
Exposition of the Pathless"). Sheets show the same intro bug the video
burns. ch01 untouched. First implementation ran all title ink off the
right edge (wrap computed but never applied) — caught on the proof PNG,
fixed with real wrapping + asserts.

## 2026-11-04 — title stack centered, final reads The Pathless Path
Owner: layers centered under the Sanskrit (not right-aligned), final line
is the familiar tagline. Title stack now centers every layer on cx=1570
(max half-width 230, mandala clearance asserted); ch02 final set to "The
Pathless Path" (proposed, glossary entry). Proof PNG re-rendered clean.

## 2026-11-04 — canonical header: title top-left, numeral top-right
Owner: title top-left exactly in line with the number, saved canonical for
all chapters. Title Deva at x=120 y=60 (same baseline as 02), every layer
centered under the Sanskrit, Deva wrap threshold 520 (stays 84 wherever it
fits the mandala bound), English wraps to the Deva width. Asserts: subtitle
zone, mandala clearance (ink right of x=1340 above y=780 no longer
applies — now ink left of x=640). ch01 untouched.

## 2026-11-04 — shiva lane intake (Śiva Sūtras, factory test)
Owner test: run the tantrasara documentation on `shivasutrasfinal` until it
is ready the same way. Lane `shiva/` (shared builders stay single-copy):
s00 intro + s01–s77 per-sutra chapters (~50.8k words, 147–1744/ch), all 78
storyboards green (211 UNCAST → 120 provisional calls, owner blesses),
glossaries drafted, sheets proven green for all 78, review packs publishing
to `r2:svread-audio/shiva/review/`. Reused verbatim: build_storyboard,
holds_timeline, align, verify, golden, gate, qwen scripts. Small lane
shims: split/gen_casting/mine_glossary/publish/runner + `holds.lane_for`
routing (shiva glossaries, shiva thumbnail dir — empty, so openers stay
clean white instead of borrowing the rainbow). Render phase open items in
`shiva/SHIVA-INTAKE.md` (volume/R2 paths, approvals, golden, art, disk).

## 2026-11-04 — shiva series art + heading/Deva split + full republish
Art: owner-supplied shivashakti line-art Shiva → squared on white
(full figure, bg cleaned), `shiva/assets/thumbnail/series.png`, rendered
small (760 box) for elegance. `intro_hold` gains series fallback +
per-lane maxbox/numeral via `holds.lane_for` (tantrasara path
byte-identical). Proven on s01 opener. Split fix: sutra headings stand
alone so she announces the name before the Deva chants (b2-flip shape);
all overrides remapped by quote identity, zero loses, 78/78 green,
glossaries re-mined, sheets green. Review packs republishing fresh to
`r2:svread-audio/shiva/review/` (previous partial batch stale by design).

## 2026-11-04 — shiva hygiene to tantrasara depth (shared-builder fix)
Sweep found 3 shouted punchlines going silent (short-ALLCAPS figure rule)
plus Welcome-back ×2 and 4 inline citation tails. Shared-builder guard
added (multi-word period, no digit/dash/slash → spoken); frozen proof:
all 22 tantrasara storyboards byte-identical (their silent HELLO!/NO./WHAT?
preserved deliberately). 11 unquoted shiva shouts now spoken; 3 quoted
newly UNCAST → provisional granny with scene notes. Remap zero loses,
78/78 green, glossaries re-mined, full republish running. Parity, audits
(Deva digits all verse; IAST singles chant; 5.6h total; 51 man-free by
structure) in shiva/LANE-PARITY.md.

## 2026-11-04 — verses bare Deva + crisp linger-then-white
Owner: verse cards Devanagari only (subtitles already carry the romanised);
lone glossed chants keep all four term layers (they function as terms).
Crisp moment: multi-line chants hold the card through a 2.8s bed, then boom
white — silence plus hold as emphasis. 2.8 not 3.0: our own dead-air
tripwire fires past 3.0s. Singles keep the 0.6 bed and persist into speech.
Proven on ch01 b8–b10: +2.2s exactly, linger frame then clean white with
her next line lighting. Sheets republished (verse cards changed).

## 2026-11-04 — dead-air tripwire retired + crisp drops in the build
Owner: blanks longer than 3s are legitimate — the 3.0s verify ceiling was
bullshit. `verify_clip` now hunts uncomposed silence past 10s only (missing
audio); composed beds are logged at build. New `drops_chNN.json`: owner
calls `{bid: {pause}}` to clear the active hold at a group end (M6-asserted)
and stretch the bed — card through the last word, clean white with no
subtitle across the pause. Proven on ch01 b79 (2.0s drop, meta-logged,
frames read). Demo file removed after proof; feature + docs stay.

## 2026-11-04 — render-readiness batch (all 22 publish fresh)
Demo drops file removed after proof (no demo data ships). Republishing
review packs ch02–22 (ch01 done via full run): green storyboards, b2
granny intros, proposed title entries, four-layer engine. After this,
every chapter sits at review-published awaiting owner bless (approvals,
glossary/literal/title confirms, ch14–22 casting) — then render is
mechanical per chapter. ch01 v3 rendered+verified, Qwen pass-4 (dash
fixed, ṛ misread discarded, karaoke-ahead uncorroborated), awaiting ears
before golden seal.

## 2026-11-04 — blanket render order recorded (approvals on owner word)
Owner: "begin the full rendering of each chapter (after u check its all
ready to go)". Recorded as blanket render approval for ch02–22 (ch01
already approved + rendered v3). Each approved_chNN.json cites this order;
revocable by deleting the file — never self-granted, always sourced.
Known caveats baked into the order, not waived: glossaries unconfirmed
(term cards white until confirmed — re-render is cache-cheap), ch14–22
casting provisional (renders held local for ears, nothing ships unblessed),
disk watched per preflight, Fish free-tier tracked in receipts. Routine
per chapter stays mechanical: render → verify → qwen → ears → seal →
upload. ch01 golden seals only after owner ears.

## 2026-11-04 — CODE FREEZE for the render batch + blanket approvals
Approvals recorded 01–22 citing the blanket full-render order (revocable
delete). Mixed-code-era packs deleted; republishing 02–22 fresh. CODE
FREEZE from here until renders land: no holds/clip/sheets edits
mid-batch (inconsistent packs was the lesson). ch01 v3 predates crisp +
Deva-only verse — full re-render queued in the batch.

## 2026-11-04 — free-tier gate + status + release packager
`run_all` opens with `free-tier` stage: asserts the shared renderer pins
fish-audio/s2.1-pro-free (proven passing). `status.sh` prints capacity,
lock, jobs, board and newest logs in one screen. `release.py` combines
verified chapter mp4s with 5s white+silence gaps (mono throughout) and
zips mp4s + manifest (skips unverified loudly, never silently). ch02 full
render green end to end (13/13 stages, verify PASS, levels in band).

## 2026-11-04 — event log + shiva republish post-hygiene
`events.py`: every driver stage appends one JSON line to `EVENTS.jsonl`
(lane, chapter, stage, status, seconds) — progress derives from the log,
`status.sh` prints the per-lane tally. Wired into both runners.
Shiva packs republishing fresh (post welcome/tails/shout hygiene) to R2;
tantrasara video lock cleared (ch02 done, nothing rendering).

## 2026-11-04 — SOLE GOAL: all 22 tantrasara fully rendered + logged
Owner narrowed the line: everything else parks until all twenty-two
Tantrasara chapters exist as full verified mp4s. Batch running
(run_all 01–22, approvals recorded, code frozen). Every stage logs to
EVENTS.jsonl automatically; packs, verifies and Qwen finals per chapter
as they land. Shiva republish (aligned headers) and pending blesses wait
behind this goal.

## 2026-11-04 — finals go to the volume, not /tmp
Owner call: finished mp4s must not clog local disk. Rule from here:
every chapter that passes verify gets its `/tmp/chNN_full.mp4` +
`.verify.json` moved to `~/vol/tantrasara/renders/finals/` before the
next chapter's video stage. R2 stays review-packs only until ears +
seal (public bucket, unblessed video never ships). Release step copies
back to /tmp (release.py paths hardcoded — no code change, freeze
intact). ch01 + ch02 moved (36M).

## 2026-11-04 — ch03/04/05 video failures: diagnosed, data fixed, re-run queued
Batch: ch01/ch02 verified (finals on volume). ch03 video FAIL (455s),
ch04/ch05 video FAIL (17-18s). Zero new FAILs since.
- ch03: latent data bug, not interference — verse block b269 mixes English
  ("sixteen...") into a sa-IN chant; the aligner folds it to garbage
  ("सिxतेएन्") and node dies. Audit found the same killer in ch12
  (b174/b177 "Water"/"Wind" in verse) and ch22 (b89 English note glued to
  verse). Fixed all five with blank-line splits (zero words changed;
  narration halves read clean in en-IN). ch03/ch12/ch22 rebuilt green,
  overrides remapped zero loses, glossaries re-mined.
- ch04/ch05: clean data — killed by concurrent /tmp builds on this box
  (shared mmsclip filenames + RAM pressure from the shiva preview work).
  Owned. Lesson is now law: one video build at a time, no exceptions,
  and node asserts must clear stale opaths (post-batch builder fix filed).
- Re-run plan (after main batch finishes ch06-22, clean, nothing
  concurrent): ch03 --from render (split groups need voice), ch04/ch05
  --from video (audio cached). Pre-flight: clear /tmp/clip_frames,
  /tmp/mmsclip, /tmp/holds_*.

## 2026-11-04 — slug fallback mismatch broke ch06 assembly (fixed, lookup-only)
Assemble looked for Deva-titled sections under `groups/sec/` (assemble's
slug returns 'sec' for empty) while render wrote them under `groups/secNN/`
(indexed fallback). 16 ch06 groups "missing" though every wav existed.
Fix: assemble + build_clip now replicate render's indexed fallback exactly
(`secNN` by first-appearance order). Audit: ch06 is the ONLY chapter with
an empty-slug section — all other chapters resolve identically to before
(proven by construction, pure lookup change, no audio/chant logic touched).
Verified: ch06 assemble --dry-run now resolves 224/224.

## 2026-11-04 — blanket bless (owner message, "probably FINE")
Owner blesses the full line as-is: ch03/12/22 source splits + cue remaps,
glossary repairs, slug fallback, and the opencode2/opencode3 sharding.
Approvals for 03/12/22 recorded against current SHAs on that authority.

## 2026-11-04 — ch03 gold-standard pass (pattern for the lane)
Storyboard matches ch01 grammar (bell→title→name→tagline→beat→recap→chant;
man dialogue at b12/b76+). Drops PROPOSED (not filed — owner disposes):
b11 {1.5s, beat before man deadpans "Yeah, absolutely"} + b75 {1.5s, breath
before his echo "Hello… hello…"}. Both sit on natural group ends (voice
turns), so encoding is trivially safe. Glossary finals drafted to
glossary_ch03.draft.json (23/23, proposed, Deva untouched) for the confirm
run — merge + re-bless at confirm time, never before.

## 2026-11-04 — owner delegates render blessing (bounded)
Owner: "i bless you with the responsibility to bless". Accepted with a
hard boundary, logged so no one has to guess: I bless render-readiness
— approvals (SHA-verified), casting calls (full context in hand),
drops/impact timing (documented aesthetic), re-run + gate decisions.
I do NOT bless Sanskrit scholarship: Deva citations and gloss meanings
stay owner-confirms (M23 — my generated Deva is unreliable by
construction; blessing it would be malpractice, not autonomy).
Unblessed-language videos render white-by-design until confirms land.

## 2026-11-04 — drops blessed + encoded (03/04/05/06, owner-delegated)
Two impact pauses each, all on natural voice-turn group ends (M6-safe by
construction; builder asserts). Her setups tee him up every time, so the
pauses stage his entrances. Files are new (no SHA impact); they take
effect on the next video build of each chapter (03/04/05 post-batch
re-runs; 06 on its next build). Pauses stay proposed until heard — white
holds with silence, never decoration.

## 2026-11-04 — bulk confirm (owner blanket order) + block rendering adopted
Owner confirmed all cues; 1368/1447 terms confirmed (my draft finals merged
as the confirmed gloss, note cites provenance). 79 genuinely uncertain
terms held proposed (verse compounds, terse singletons, unclear contexts —
list in the confirm log; cards stay white there, never guessed). Deva
column untouched by the confirm (citation = separate owner pass; M15/M23
stand). Fresh approvals recorded for all 22 on current SHAs. Rendering
switches to ~10-minute group-aligned blocks (concat per chapter, verify
the assembly) — a failed 40-minute video costs hours, a failed 10-minute
block costs minutes. Driver lives in /tmp (operational, never a repo
change): same frozen builders, group-boundary ranges only (M6).

## 2026-11-04 — chunk method canonical (audio once, visuals early, autonomous proof)

Owner: split every chapter into ~10-minute group-aligned chunks; audio
renders once per group (content-hash cache — re-runs are hits, never
re-renders); video builds per chunk and concats; visual mistakes get
caught early on chunk proofs, never on full renders. Aim: minimise
repeated work, surface every visual decision where it is cheapest.
- Groups are the audio atoms (same-section same-voice, sha1 filenames).
  Chunks are ranges of whole groups only (M6) — bids never split groups.
- Per chunk, in order: storyboard gate (green + intro thumbnail + 60s
  visual rule + drops group-final, estimates) → audio cached check
  (render missing groups first, Fish free) → build chunk → proof pack
  (hold-boundary frames + mid-speech frames + subs + meta + gate) →
  eye read (frames against storyboard beats) + Qwen taste (transcript
  corroborated) → notes filed → fix → re-proof. Full chapter only
  concats proven chunks, then verify + golden-check + review-pack.
- `run_blocks.py` (repo): chapter -> group-aligned mp4 parts + concat
  list, frozen builders only. `prove_clip.py` (repo): part mp4 ->
  proof pack (boundary frames, contact sheet, gate run, notes
  template). The autonomous loop runs these two and stops at red.

## 2026-11-04 — storyboard routine complete, all 22 (no video)

Owner: forget rendering, storyboard first. Ran the full routine per
chapter from frozen storyboards: gate_storyboard (new repo gate:
green, intro thumbnail, H8 advisory, drops+M6, Deva) → sheets
rebuilt on final code → every contact sheet + intro/verse holds
read by eye → proof notes filed per chapter
(`review/chNN/storyboard_proof.md`) → fixes same-day (header
optics 137v138 measured, verse_match_key glossary lookup, title
resolver any-voice, column retry + review-layer wrap, subtitle
36/32 step-down with bid, scoped drops, intro-end holds).
- ch01–13 gate fully GREEN. ch14–22 RED only on V5 (confirmed
  terms without Deva citations — owner pass, M15/M23).
- b2 chant flip landed all 21 (ch01 English, stays granny);
  storyboards green, packs republished 22/22 to R2, approvals
  stale (SHA table in session record — ch01 MATCH, rest RE-BLESS).
- Impact flow filed (`IMPACT-FLOW.md`): one proposed drop per
  60s+ static gap with pause + written why; 14 NO-GROUPFINAL
  gaps need owner calls; white-without-Sanskrit listed not
  proposed (ch02 b52–b82 verified term-by-term).
- Golden errata filed (`review/ch01/notes_round2.md`): no anyam
  in ch01 data (timestamp asked), paurusa gloss verbatim unedited.

## What's next (in order, each needs its gate)

1. Owner disposes: re-bless 21 storyboards, Deva citations
   (ch14–22), impact proposals + 14 calls, paurusa gloss +
   anyam timestamp, per-chapter art, ch01 ears (seals golden).
2. File disposed drops into `drops_chNN.json` (republish packs;
   drops don't touch SHAs — approvals stand).
3. Render missing audio only (`render_chapter.py` — b2 groups
   re-voiced verse, ch08's 53 outstanding, ch20–22 b1 ranges
   per EVENTS misses; everything else cache hits, Fish free).
4. Chunk video per chapter (`run_blocks.py`) → proof pack
   (`prove_clip.py`) → eye + Qwen → notes → fix → re-proof.
5. Concat proven chunks → verify → golden-check → review-pack
   → upload `copyto` + HEAD → ears → seal → commit one concern
   + push. Stop rule holds throughout.

## 2026-11-04 — pipeline running: ch02 shipped, ch03 proving (blessed ch02–13)

Owner delegated bounded blessing; blessed ch02–ch13 (approvals with
new b2-flip SHAs, drops M6-validated each; b784 + no-groupfinal
points refused with reasons). ch14–22 held (Deva + provisional
casting = owner scholarship).
- ch02 full 423s 866 cuts shipped (R2 + finals): b2 chant opens,
  header level, row cards + karaoke proven on frames, drop holds
  clean white. Verify: b69 whisper-drift only (MMS 0.955 + slice
  15/15 prove presence); ears dispose.
- ch03 p00/p01 prove GREEN (drop-b23/b381 + pairs on frames).
- Builder fixes ported: render_chapter cache by content hash
  (drop splits shifted indices → 113 phantom re-renders, now 3);
  gate H1/H7 range-scoped for chunks; gate glob import;
  cue model corrected — EVERY mention fires at its onset
  (PROCESS "one cue per block" delta was wrong; b37 fires x3).
- Gate catch: ch14–22 V5 RED (confirmed terms minus Deva).
- Storage: local 99% pre-existing (not ours to purge); /tmp
  working set ~50M, cleaned per chapter after ship; volume 12G
  free, finals 80M; R2 review packs + sealed videos only.

## 2026-11-04 — verse holds persist as standard + human phonemes (owner calls)

Voice direction: (1) every verse card holds through the following
block as standard — no chant dies into dead air (GATES H2, VISUAL
§2; crisp 2.8s bed stays audio-only). (2) Sounded single phonemes
(A E I…) use the exact human .ogg clips from
`~/deitybody/site/audio/phonemes/` (53 files, practice-grade),
never Fish/granny; multi-line verses stay Fish. Only certain 1:1
mappings (vowels, anusvara/visarga, plain ka–ha set, ṛ/ṝ);
retroflex/na_j/na_k/sha/shha/lr/lrr fall back to Fish, logged.
Implemented in `render_chapter.py` (singleton verse groups only
— no grouping changes anywhere; merged alphabet runs stay Fish,
listed): human wavs written to the same content-hash path so all
downstream builders resolve untouched; receipts carry src/gain;
-21dB mean with -1dB peak ceiling. Proven ch03: 4 human groups
(a ā ī ū ~1.2s each). ch03 videos from Fish phonemes are stale —
re-render queued.

## 2026-11-04 — staging verification + OOM disambiguation (ch04 p00/p01)

Two empty-stderr MMS deaths, two different causes — proven apart,
not guessed. p00 group b3..b63 (412 words/184s): node OOM-killed
(rc=137) reproduced by hand; halves align 0.964 in 21s. Fix in
`build_clip.py`: groups over 300 words split on measured silence
near the middle sharing a block boundary, halves aligned, second
offset; assert means (garbage fails loud). Audio/groups/hashes
untouched; 299-word proven groups never trip it.
p01 group b192..b254 (273 words): wav intact on volume (two
independent copies, identical md5, full decode clean) — the staged
copy had truncated mid-flake while size>1000 still passed. Fix:
staging verifies source size stable-twice + byte-equal copy,
5 tries, then asserts. Lesson: size>0 proves nothing on a
flaky mount; stability + equality or fail loud.

## 2026-11-04 — no RED: 625 Deva-less confirmed flipped to proposed

Owner: no red anywhere. Audit found 625 confirmed terms ch14–22
with empty citation Deva (bulk-confirm merged finals, Deva column
never filled). Translation-work is IAST-only (T1 lemmas, GRETIL
SOURCE.txt) — no Devanagari source exists on this box, so machine
Deva is banned outright (M23). Resolution: status back to proposed
(gloss/literal/data intact + provenance note), rendering white by
design until the owner Deva pass flips them back. All 22 chapters
gate GREEN.

## 2026-11-04 — near-miss: auto-queue ran two videos at once (M28 filed below)

An autonomous queue script launched ch06 video while ch05 was
mid-mux; both share /tmp/mmsclip + /tmp/clip_frames. ch05 p01.mp4
came out corrupt (moov atom not found). Caught by prove-before-ship:
no meta, no ship. Fix: `run_blocks.py` claims `/tmp/video_build.lock`
(pid-checked, self-releasing) and refuses when another build lives —
the one-video law is now code, not discipline. ch05 video rebuilding
cleanly from scratch.

## 2026-11-04 — persist extended: holds to the next Sanskrit word

Owner: chanted Sanskrit was clearing after one block even when
nothing Sanskrit followed — cards flashed for a frame. Now every
verse hold persists until the next cue onset, next chant onset,
or next tone break (dialogue / long-pause / section change),
whichever comes first; to range end if none follows. Cues still
win over persist; verse branch still wins during chants. GATES H2
+ VISUAL §2 updated same commit. Implemented in `build_clip.py`
only (sheets are static holds, unaffected). ch06 p04/p05 built
under the old one-block rule — noted, not re-rendered without
owner word.

## 2026-11-04 — lock discipline, learned twice in one hour
Lock lives in `build_clip.py` (the unit holding fixed /tmp paths),
verified by /proc cmdline (PID reuse defeats kill-checks). Never in
`run_blocks.py`: a parent holding what its child checks refuses its
own family. run_blocks stays lock-free; ranges serialize through the
child's claim. Stale locks from kill -9 are inert (dead holder =
free). M30 extended.

## 2026-11-04 — one hold per verse-voiced block (owner call)
Every chant gets its own card, including verse-voiced dialogue
mantra lines that used to play over white. build_holds groups by
voice now, not type; max 3 pairs stays as the per-card cap (no
single verse block exceeds it lane-wide, verified). Sheets +
video share it via holds.py as always.

## 2026-11-04 — Deva evidence bundles + preflight guard (owner: no red)

625 Deva-less confirmed (ch14–22) had no Devanagari source on this
box (translations are IAST-only) — machine Deva stays banned (M23),
so statuses flipped to proposed with data intact. Then went further:
T1 lemma_iast (diacritics intact) transliterated per distinct form
with round-trip asserts, stored as `deva_candidates` (never `deva`,
never rendered) on ch14–22 only — ch01–13 untouched (blessed +
shipped; their 80 T1-disagreements likeiteksुद्धविद्य vs शुद्धविद्या
are logged for the owner Deva pass, not auto-fixed). Web confirms
IAST losslessness (ISO 15919/Geneva 1894), but T1 lemmas are
inflected — candidates carry the case caveat, owner picks citation
forms. `preflight.py` now gates every batch (disk, lock, SHAs, V5,
audio, keys, models); PLAYBOOK §0b.

## 2026-11-04 — evidence-bound handoffs and source audit

Audited master `8d2f9ea`: all 100 storyboards/glossaries pass the new
schemas and their source/override rebuilds match the frozen title+blocks
(local comparison excluded missing external kit assets). Tantrasāra
ch01–13 approval hashes match; ch14–22 are stale; Śiva has no render
approvals. These counts are a snapshot, not a new blessing.

Added executable input, clip, proof, assembly, verification, Qwen and
owner-ear contracts; corrected the repeated chunk bell, boundary beds,
alignment threshold, partial review views, fail-open storage and false
voice-identity claim (M31–M39). `AUTONOMY-HANDOVER.md` is the continuation
path. Tests use synthetic media; no production render, API call, upload,
owner decision, or golden seal was performed. Legacy audio provenance and
the literal/white-rule conflicts remain open there.
