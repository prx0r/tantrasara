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