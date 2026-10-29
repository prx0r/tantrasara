# BUILD-NOTES.md — THE LOG (append-only; latest entry is the truth)

## 0. Intake opened (2026-10-29)

Repo scaffolded from the analayo-nibbana tree (post-reorg shape):
AGENTS/HANDOVER/VISION/DONE/SPEAKER-RULES/TIMINGS entry docs;
`sources/{lectures,text}/`, `build/{canon,versions,ears,assets}/`,
`process/`, `tools/`, `reviews/`, `archive/`; sfx+bells kit ported.
Process machinery lives in the reference repo until ported per
08-PORTING (no preemptive forks). Cast: TBD by owner ear.
Next: intake item 1 (sources — owner).

## 1. Text landed, audio still missing (2026-10-29)

- Full Chakravarty/Marjanovic Tantrasara secured locally from the gochema
  stash (`sources/text/reference/`, gitignored): 11,891 lines, clean text,
  ToC + intro + chapter summaries + all chapters. This is the verbatim home
  to excavate from. Also on disk there: tantrasara-bertagni.pdf (unchecked).
- Dyczkowski "talks on rebirth etc." NOT found on any disk (searched /root:
  only his PDFs/texts — journey-in-the-world-of-the-tantras, spandakarika —
  no audio). Owner to say where they live (YouTube links? re-download?).
- Still to buy/get: Dyczkowski 54-lecture course ($100, audio + PDF
  transcripts — the build voice). Everything else needed is free.

## 2. Study audio landed (2026-10-29)

9 Wallis "Essence of Tantra" Tantrasara episodes (~4h, Acast RSS, free):
three-upayas overview + ch.1/2/3-abridged/4x2/5x3 at
sources/lectures/audio/study/ (mp3s gitignored, SOURCES.md index).
STUDY ONLY — never canon. Build voice stays: purchased Dyczkowski.
Still missing: Dyczkowski audio (owner to locate or buy $100 course).

## 3. Study transcripts in progress (2026-10-29)

No downloadable transcripts exist (RSS has none; episode pages don't
embed them). Transcribing the 9 study mp3s locally into the house CF
schema ({source,duration,engine,sentences[]}) at
sources/lectures/transcripts-study/ via tools/transcribe_all.sh:
10-min chunks -> one-shot whisper -> merge. Sustained whisper runs get
OOM-killed on this box, hence chunked one-shots (see §4).
Engine: tiny (study-only; small.en at canon time if these ever graduate).
