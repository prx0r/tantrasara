# VISUAL CANON — Tantrasara explained (locked 2026-11-03, owner-confirmed)

One screen language for all 22 chapters. `holds.py` is the single
implementation (sheets and video share it); this file is the law it
implements. Change only by owner call, same commit as the code.

## Canvas
- 1920×1080, 30fps, libx264 + AAC. White ground `#FFFFFF`, ink `#17140F`,
  gloss grey `#CFC9BE`.
- Subtitle safe zone: y=860, max 2 lines. No card element may enter the
  subtitle zone or touch frame edges — collisions fail the render.

## Type stack (three faces, no others)
- Devanagari: Tiro Devanagari Sanskrit Regular. Verse 84pt, wrapped 64pt.
- Gloss: Cormorant Garamond Italic 40, grey. One line under the Deva.
- Subtitles: Cormorant Garamond Medium 46 → 40 if 3 lines threaten.
  Ink = lit (spoken), grey = unlit. Verse subtitles in IAST transliteration
  (the face owns no Devanagari glyphs); narration subtitles verbatim.

## Cards (owner-confirmed 2026-11-03: term cards as now, ~20% white target)
1. **Thumbnail** — frame 0 until first chant. Fitted above subtitle zone,
   never fullscreen-bleed.
2. **Verse** — Devanagari ONLY, no romanisation ever. Up the moment chanting
   starts, clears the instant speech resumes. Max 3 Deva line-pairs per hold.
3. **Term** — Devanagari headword + one grey English gloss. Pops the instant
   she says the word; holds until the next cue or tone break (newer cue
   always supersedes). Only `confirmed` glossary terms render — `proposed`
   plays over white. Single Sanskrit words stay with granny + term card;
   the verse voice is multi-line passages only.
4. **Title / figure** — spoken titles stay spoken; no title cards in video.
   Figures (rare) render large numeral + short caption.
5. **White** — the default. Returns at every tone break, section break,
   long-pause beat, dialogue entry. House target ≈ 20% white per chapter;
   builds print COVERAGE and fail over 85% white (60s+ clips).

## Sanskrit breakdowns (owner call 2026-11-03)
Breakdown = the term card: full compound in Devanagari + one gloss line.
No compound-splitting, no interlinear verse gloss, no IAST on cards.
If a term needs parts explained, the narration says it; the card stays whole.

## Voices on screen (unchanged)
Granny narrates; man objects and dialogues at 75%; verse chants. Cards are
voiceless — they anchor what is heard, never add text of their own.

## Proof (every clip, no skipping)
Pull frames at: chant start, mid-verse, first term pop, a rapid-fire cue
pair, a dialogue turn, a tone-break return to white. Read each: right card,
right subtitle, karaoke on the spoken word, no tofu, no overflow, no
subtitle-zone collision. Then Whisper head-check (words present, not timing),
then Qwen taste-only, then owner ears.
