# PROCESS NOTES — how chapter audio/video gets built and proven (ch01 first full run)

## The chain (each step's output is the next step's input, nothing estimated)

1. **Storyboard** (`build_storyboard.py`): markdown → blocks with voice +
   direction tags. Gate: 0 errors 0 warnings. Overrides are positional —
   if chapter text moves, remap by quote text, never reuse stale IDs.
2. **Render** (`render_chapter.py`): consecutive same-voice blocks per
   section merge into one Fish call (`s2.1-pro-free`). Filename carries
   `sha1(voice|directed-text)` — re-runs only render changed groups.
   Receipt per call (chars, hash, ffprobe duration) in
   `renders/<ch>/receipts/calls.jsonl`.
3. **Assemble** (`assemble_chapter.py`): bell (ding, +6dB, peak checked
   under 0dB) + groups with rhythm beds (0.8 structural / 0.6 verse /
   0.3 flow). Groups resolved BY CONTENT HASH, never by stale block IDs.
   Duration asserted against sum of parts.
4. **Holds** (`render_holds.py` → `holds.py`): thumbnail / verse (Deva
   only) / term (Deva + confirmed gloss) / title / figure / white.
   Every card asserts stack clears subtitle zone — collisions fail loud.
5. **Align** (`align_group.js`, MMS forced align — same engine as the
   chant pipeline): en-IN narration, sa-IN Sanskrit. Diacritics folded
   and numbers spelled FOR THE ALIGNER ONLY (1:1 mapping asserted).
   Bar: mean ≥0.85, zero non-monotonic. sa-IN takes raw Devanagari;
   en-IN takes folded ASCII (its romanizer rejects IAST diacritics and
   bare digits — both handled in `spoken()`).
6. **Video** (`build_clip.py`): one frame per word, boundaries AT word
   onsets (gaps belong to the prior word — never distribute time
   proportionally). Subtitles: IAST for verse (Devanagari has no glyphs
   in the subtitle face — tofu otherwise), verbatim otherwise. Thumbnail
   holds until first chant; verse cards while chanting; term cards pop
   at confirmed-gloss mentions; clean white otherwise.

## How timings are confirmed (no trust, only checks)

- **MMS scores**: mean + min + nonmono printed per group; anything under
  bar stops the line for that group (not the chapter).
- **Duration math**: assembly total == bell + Σ groups + Σ beds, verified
  by ffprobe. A mismatch means a wrong file got in — investigate, never
  adjust a constant to make it fit.
- **Whisper head-check**: transcribe the mix head; the words must be
  there in order. Whisper is a CONTENT check only (words present), never
  a timing authority — short clips and Sanskrit garble it.
- **Frame reads**: pull frames at every section boundary (hold changes)
  plus 2–3 mid-section karaoke states and READ them: right card, right
  subtitle, no overflow, no tofu, highlight on the spoken word.
- **Qwen omni**: taste and flow ONLY. Timing/identity claims need
  transcript-or-waveform corroboration. Timestamps past file length void
  the pass. Single passes are hints; corroborated structure is evidence.
- **Owner ears dispose.** Everything above is just the ticket to get heard.

## Failure log (ch01 full run, 2026-11-02)

- ch01 full chapter: 111 blocks, 7m19s, 15MB. Render 9/9 groups, MMS means
  0.92–0.96 across groups, assembly == sum of parts, frames verified at
  opener/verse/term/narration checkpoints, whisper head-check clean.
- Lesson: `rclone copy <file> <remote-dir>/<filename>` creates a directory
  named like the file — always `copyto` for exact keys, verify with HEAD.
- Lesson: the rclone sftp mount flakes on reads under load ("Impossible to
  open") — single `cp` retries or `rclone copy` down, never assume.
- Lesson: Fish TTS on Devanagari returns short garbage-free clips, but MMS
  sa-IN needs Devanagari tokens (its romanizer rejects IAST diacritics and
  bare digits) — fold + spell numbers for the aligner only.
- Lesson: subtitle face (Cormorant) has no Devanagari glyphs — verse
  subtitles render in IAST transliteration, never Devanagari.
- Lesson: verse subtitles in an earlier cut showed the wrong block's text
  because the clip range split a rendered group — clip ranges must align
  to group boundaries (builder asserts).
