# SHIVA INTAKE — Śiva Sūtras explained, factory intake (2026-11-04)

Source: `shivasutrasfinal` (gmail dump, committed 13,737 lines as `aec744c`).
Same factory as tantrasara (RUNTIME.md routine, GATES.md gates, same three
Fish seats, same holds/cards). Shared builders stay single-copy; only lane
paths live in `shiva/`.

## Shape

78 units: s00 series intro + s01–s22 (1.1–1.22) + s23–s32 (2.1–2.10) +
s33–s77 (3.1–3.45). ~50.8k words total (147–1744 per chapter).

## Split decisions (`split_shiva.py`, all deliberate 30-second calls)

- Headings consumed IN SUTRA ORDER (1.1..3.45 exactly once; assert).
  Same-ref lines elsewhere (the 2.1–2.10 recap inside 2.10) stay content.
- Post-boundary material (after a trailer/label/header) attaches FORWARD
  to the next sutra (recaps belong ahead, not behind).
- Dropped: gmail headers anywhere, `Source Library +N`, Attachment
  carriers, U+2060 joiners (blanks preserved first — M13), `Continue` /
  `End of Book` / `Part I-III` / `Book III, Part` labels, title repeat and
  book subtitles past the intro.
- Appendix (condensed re-reading from 2nd BOOK I) is reference only;
  the 4-line colophon (॥ शिवम् ॥ … all 77 completed) closes s77.
- `## BOOK I/III` markers from source verbatim; `## BOOK II — ŚĀKTOPĀYA`
  from the appendix line (no header in flow — sourced, not invented).
  H1s are series labels (`# Śiva Sūtras <ref>`, splitter precedent).
- `Textual basis:` paragraphs kept (builder routes them to meta).
  `Literal:` lines kept as narration (granny reads them in flow; verse
  voice for translations is an owner call per chapter — same as rule 13).

## Casting

211 UNCAST quotes across 49 chapters, 0 lexicon gaps, 0 auto-man (no
Abhinav rule hits — skeptic never names him; Vasugupta/Kṣemarāja mentions
stay narration). Provisional auto-cast by tantrasara rules (runs
alternate man-first, demonstrations stay granny), 120 UNSURE calls logged
below; owner blesses. All 78 rebuilt green 0/0.

## Unsure log (provisional — owner disposes)
s03 run b10..b12 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I am only this.”
s03 run b25..b27 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I did this.”
s04 run b16..b18 (3): ALTERNATE man-first provisional. UNSURE, e.g. “This is terrible.”
s10 b11 lone -> GRANNY provisional single demonstrator UNSURE: “Excellent. No thoughts, no suffering, no separation. Therefore deep sleep is enlightenmen
s10 b15 lone -> GRANNY provisional single demonstrator UNSURE: “I am universal consciousness, intrinsically free, the source of manifestation.”
s10 b17 lone -> GRANNY provisional single demonstrator UNSURE: “Where’s my phone?”
s13 run b9..b11 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I fancy some tea.”
s16 b24 lone -> GRANNY provisional single demonstrator UNSURE: “Or.”
s17 b13 lone -> GRANNY provisional single demonstrator UNSURE: “I am indeed Śiva, whose Self is the universe.”
s17 run b17..b19 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I am this particular organism.”
s17 b24 lone -> GRANNY provisional single demonstrator UNSURE: “My personal opinions are infallible because I’m God.”
s22 b103 lone -> GRANNY provisional single demonstrator UNSURE: “The mind is mantra.”
s23 b58 lone -> GRANNY provisional single demonstrator UNSURE: “I am a small individual over here, desperately attempting to contact a distant divine bei
s24 run b9..b14 (6): ALTERNATE man-first provisional. UNSURE, e.g. “Make an enormous effort.”
s24 run b44..b46 (3): ALTERNATE man-first provisional. UNSURE, e.g. “What’s his name?”
s24 b63 lone -> GRANNY provisional single demonstrator UNSURE: “Just relax, mate, you’re already Śiva.”
s24 b65 lone -> GRANNY provisional single demonstrator UNSURE: “Clench every spiritual muscle until enlightenment pops out.”
s26 run b43..b45 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I have seen a divine light.”
s27 b52 lone -> GRANNY provisional single demonstrator UNSURE: “What amazing thing can I experience next?”
s29 b93 lone -> GRANNY provisional single demonstrator UNSURE: “I.”
s29 run b104..b106 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I am hungry.”
s30 b30 lone -> GRANNY provisional single demonstrator UNSURE: “Stop being attached to your body.”
s30 run b33..b36 (4): ALTERNATE man-first provisional. UNSURE, e.g. “I am this body.”
s30 b48 lone -> GRANNY provisional single demonstrator UNSURE: “I am nothing more than this limited organism.”
s30 b50 lone -> GRANNY provisional single demonstrator UNSURE: “My deepest nature is the consciousness in which this organism, its experiences, and the u
s31 b30 lone -> GRANNY provisional single demonstrator UNSURE: “There is something separate from me.”
s32 run b19..b21 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I cannot BELIEVE this person.”
s32 b100 lone -> GRANNY provisional single demonstrator UNSURE: “Stop thinking and become Śiva.”
s32 b102 lone -> GRANNY provisional single demonstrator UNSURE: “Think hard enough and manufacture Śiva.”
s33 run b35..b37 (3): ALL-GRANNY provisional - one mind. UNSURE, e.g. “This is a tree.”
s33 run b40..b42 (3): ALL-GRANNY provisional - one mind. UNSURE, e.g. “This is MY tree.”
s33 run b45..b48 (4): ALTERNATE man-first provisional. UNSURE, e.g. “What shall I do about this?”
s33 b57 lone -> GRANNY provisional single demonstrator UNSURE: “I am the universal consciousness in which these mental activities manifest.”
s33 b59 lone -> GRANNY provisional single demonstrator UNSURE: “I am this collection of thoughts, desires, judgements and personal history.”
s34 b25 lone -> GRANNY provisional single demonstrator UNSURE: “I like this.”
s34 b27 lone -> GRANNY provisional single demonstrator UNSURE: “I want this.”
s34 b29 lone -> GRANNY provisional single demonstrator UNSURE: “I need to keep this.”
s34 b31 lone -> GRANNY provisional single demonstrator UNSURE: “What happens if I lose this?”
s34 b33 lone -> MAN provisional skeptic challenge UNSURE: “Why does that bastard have a better one?”
s34 run b41..b44 (4): ALTERNATE man-first provisional. UNSURE, e.g. “I am here.”
s34 b57 lone -> GRANNY provisional single demonstrator UNSURE: “Flower.”
s34 b59 lone -> GRANNY provisional single demonstrator UNSURE: “Me.”
s34 b61 lone -> GRANNY provisional single demonstrator UNSURE: “That flower.”
s35 b7 lone -> GRANNY provisional single demonstrator UNSURE: “The world is an illusion, mate.”
s35 run b25..b27 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I can only do certain things.”
s35 run b35..b38 (4): ALTERNATE man-first provisional. UNSURE, e.g. “I know what’s in front of me.”
s35 run b43..b45 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I need that.”
s35 run b61..b63 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I was.”
s36 b66 lone -> GRANNY provisional single demonstrator UNSURE: “I am this organism, situated in this particular place, surrounded by a separate universe.
s38 b13 lone -> GRANNY provisional single demonstrator UNSURE: “Master, I have attained extraordinary abilities.”
s38 run b15..b19 (5): ALTERNATE man-first provisional. UNSURE, e.g. “Very impressive. That’s Māyā.”
s38 b21 lone -> GRANNY provisional single demonstrator UNSURE: “Still Māyā.”
s38 run b45..b47 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I can control this.”
s39 b44 lone -> GRANNY provisional single demonstrator UNSURE: “I am the awareness watching everything.”
s39 b46 lone -> GRANNY provisional single demonstrator UNSURE: “The reality of awareness is inseparable from the divine power through which everything ma
s41 run b67..b71 (5): ALTERNATE man-first provisional. UNSURE, e.g. “I am this person.”
s41 b104 lone -> GRANNY provisional single demonstrator UNSURE: “The Self is a spectator sitting motionless while the universe dances.”
s42 b19 lone -> GRANNY provisional single demonstrator UNSURE: “The stage is pure consciousness.”
s43 run b63..b65 (3): ALTERNATE man-first provisional. UNSURE, e.g. “Never look at anything.”
s45 b36 lone -> GRANNY provisional single demonstrator UNSURE: “I can now do whatever I want.”
s45 b39 lone -> GRANNY provisional single demonstrator UNSURE: “I am an exceptionally powerful personality who deserves to control everybody else.”
s45 b46 lone -> GRANNY provisional single demonstrator UNSURE: “I have a choice between several possibilities.”
s46 b41 lone -> GRANNY provisional single demonstrator UNSURE: “Wonderful. This is where I experience Śiva.”
s46 b48 lone -> GRANNY provisional single demonstrator UNSURE: “Ah, unfortunate. Śiva has apparently remained inside the meditation hall.”
s48 b13 lone -> GRANNY provisional single demonstrator UNSURE: “Can I attain supreme consciousness if my left ankle won’t go on my right thigh?”
s48 b93 lone -> GRANNY provisional single demonstrator UNSURE: “I am merely this limited organism.”
s49 b61 lone -> GRANNY provisional single demonstrator UNSURE: “You can imagine things creatively.”
s50 b53 lone -> GRANNY provisional single demonstrator UNSURE: “I have read that consciousness is the Self.”
s51 run b50..b54 (5): ALTERNATE man-first provisional. UNSURE, e.g. “Friend.”
s51 run b57..b59 (3): ALTERNATE man-first provisional. UNSURE, e.g. “This person is dangerous.”
s51 b84 lone -> GRANNY provisional single demonstrator UNSURE: “You’re wrong.”
s52 b85 lone -> GRANNY provisional single demonstrator UNSURE: “FOR FUCK’S SAKE, CAN EVERYONE PLEASE BE QUIET, I’M TRYING TO BE ŚIVA.”
s53 run b101..b105 (5): ALTERNATE man-first provisional. UNSURE, e.g. “Right. Now stop clinging to all the machinery.”
s53 b107 lone -> GRANNY provisional single demonstrator UNSURE: “Very impressive. Now enter.”
s55 run b82..b84 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I need to get back.”
s56 b34 lone -> GRANNY provisional single demonstrator UNSURE: “This sound is a completely independent thing confronting a fundamentally separate subject
s56 b36 lone -> GRANNY provisional single demonstrator UNSURE: “This sound is appearing within the luminous reality of consciousness.”
s58 b56 lone -> GRANNY provisional single demonstrator UNSURE: “My body is disgusting, and I must escape it.”
s58 b58 lone -> GRANNY provisional single demonstrator UNSURE: “My body is the supreme and complete identity.”
s58 b60 lone -> GRANNY provisional single demonstrator UNSURE: “My body is a manifestation of consciousness, and its activity can occur without obscuring
s59 b18 lone -> GRANNY provisional single demonstrator UNSURE: “Actually, I have just performed three hours of supreme tantric mantra practice.”
s59 b90 lone -> MAN provisional skeptic challenge UNSURE: “Could you pass the salt?”
s59 b103 lone -> GRANNY provisional single demonstrator UNSURE: “Everything you say is a mantra, therefore say whatever you like.”
s60 b98 lone -> GRANNY provisional single demonstrator UNSURE: “You’re standing in it.”
s62 b20 lone -> GRANNY provisional single demonstrator UNSURE: “I have manifested the universe with my thoughts.”
s62 b22 lone -> GRANNY provisional single demonstrator UNSURE: “Everything exists because I personally imagined it.”
s62 b66 lone -> GRANNY provisional single demonstrator UNSURE: “This is a pot.”
s62 b110 lone -> GRANNY provisional single demonstrator UNSURE: “I am a limited individual confronting an external universe.”
s62 b112 lone -> GRANNY provisional single demonstrator UNSURE: “The universe is the manifestation of the divine power inseparable from my true conscious 
s63 run b55..b56 (2): ALTERNATE man-first provisional. UNSURE, e.g. “It is.”
s63 b67 lone -> GRANNY provisional single demonstrator UNSURE: “A great tragedy has occurred.”
s64 b62 lone -> GRANNY provisional single demonstrator UNSURE: “I have disappeared.”
s65 run b28..b30 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I am happy.”
s65 b66 lone -> GRANNY provisional single demonstrator UNSURE: “I am sad.”
s65 b68 lone -> GRANNY provisional single demonstrator UNSURE: “My life is sad.”
s65 b70 lone -> GRANNY provisional single demonstrator UNSURE: “I have always been sad.”
s65 b72 lone -> GRANNY provisional single demonstrator UNSURE: “I will always be sad.”
s65 b83 lone -> GRANNY provisional single demonstrator UNSURE: “This is the entirety of what I am.”
s67 b22 lone -> GRANNY provisional single demonstrator UNSURE: “I happen to be mistaken about one particular thing.”
s67 run b41..b43 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I am the doer.”
s68 run b44..b48 (5): ALTERNATE man-first provisional. UNSURE, e.g. “Good morning, what do you do?”
s68 b59 lone -> GRANNY provisional single demonstrator UNSURE: “One becomes more psychologically creative.”
s68 b61 lone -> GRANNY provisional single demonstrator UNSURE: “One discovers a fresh perspective on one’s life.”
s68 b78 lone -> GRANNY provisional single demonstrator UNSURE: “Remain an ordinary finite person, but acquire increasingly spectacular powers.”
s69 b47 lone -> GRANNY provisional single demonstrator UNSURE: “Imagine something, therefore you can physically create anything.”
s69 b89 lone -> MAN provisional skeptic challenge UNSURE: “How does my consciousness relate to the world?”
s71 b29 lone -> GRANNY provisional single demonstrator UNSURE: “I have understood nonduality, therefore my entire life is now permanently liberated.”
s71 run b82..b84 (3): ALTERNATE man-first provisional. UNSURE, e.g. “You’ve done it.”
s71 b96 lone -> GRANNY provisional single demonstrator UNSURE: “I’ll be complete when I get that.”
s72 b27 lone -> GRANNY provisional single demonstrator UNSURE: “Where are we going?”
s72 run b29..b34 (6): ALTERNATE man-first provisional. UNSURE, e.g. “Another embodied existence.”
s72 b47 lone -> GRANNY provisional single demonstrator UNSURE: “I am incomplete.”
s72 run b49..b51 (3): ALTERNATE man-first provisional. UNSURE, e.g. “I need this.”
s72 b90 lone -> GRANNY provisional single demonstrator UNSURE: “I am incomplete, and this thing must complete me.”
s74 run b72..b76 (5): ALTERNATE man-first provisional. UNSURE, e.g. “Where’s the teacher?”
s76 b70 lone -> GRANNY provisional single demonstrator UNSURE: “I am this mind.”
s77 b119 lone -> GRANNY provisional single demonstrator UNSURE: “Destroy the world.”
s77 b121 lone -> GRANNY provisional single demonstrator UNSURE: “Suppress every thought.”
s77 b123 lone -> GRANNY provisional single demonstrator UNSURE: “Abandon every relationship.”
s77 b125 lone -> GRANNY provisional single demonstrator UNSURE: “Become an exceptionally impressive individual.”
## Open for render phase (NOT intake blockers)
- Volume/R2 paths: renders must land in a shiva volume dir + `r2:svread-audio/shiva/`
  (build_clip/render_chapter/assemble hardcode tantrasara paths — parametrize at render time).
- Thumbnails: `shiva/assets/thumbnail/` empty — openers stay clean white by
  design until art lands (never borrow the rainbow). Numeral semantics
  (sutra ref vs index) decided with the art.
- Approvals: `shiva/approved_sNN.json` gate (mirrors run_all.stage_render).
- Golden store, Qwen final, ears: same routine, after first render.
- Disk: local 0.5G vs 1G preflight blocks batch runs until freed.

## Series art (2026-11-04, owner-supplied)
`assets/thumbnail/series.png`: the shivashakti line-art Shiva, squared on
white (full figure kept, background cleaned to pure white), rendered small
(maxbox 760) for elegance against the tantrasara piece. Sheets and video
share it via `intro_hold` series fallback (`holds.lane_for` routing, shiva
numerals pending owner call — no numeral drawn until decided). Proven on
s01 opener: small centered emblem, clean white, no borrowed art.
## Re-split 2026-11-04 (heading/Deva separation + remap)
Sutra headings now stand on their own blank line: she announces the name
(narration), then the Deva chants (verse) — same shape as the b2-flip
intros. All provisional overrides remapped by quote-text identity (M12),
zero loses, all 78 green again. Glossaries re-mined against new IDs.

## Hygiene pass 2026-11-04 (tantrasara depth)
- "Welcome back to Kashmir." dropped ×2 (repeated formula; s72 title kept).
- Inline tails stripped: Source Library / Sanskrit Documents / Sanskrit &
  Trika Shaivism +N (4 hits).
- 11 unquoted shouts rescued from silent figures (stage patter, all
  verified spoken in context); 3 quoted shouts newly UNCAST → provisional
  granny with scene notes (s05 self-mockery, s41 Hamlet enactment, s72
  rebirth-queue tail keeping filed alternation).
- Shared-builder shout guard (multi-word period, no digit/dash/slash):
  proven by byte-identical rebuild of all 22 frozen tantrasara
  storyboards — their silent HELLO!/NO./WHAT?/PHAṬ! behavior preserved
  deliberately.
- Deva digits: all 77 in verse chants (sutra numbers, safe). IAST singles
  chant via standalone-Sanskrit rule. Literal: lines read in flow.
- Gate D1/D3 green 78/78. ~50.8k words ≈ 5.6h. 51 chapters man-free by
  structure. Lane parity recorded in LANE-PARITY.md.

## Intro header (2026-11-04, owner call)
Mirrors the tantrasara canonical header in the same type: sutra ref
top-right (FE 150, numeral's mirror), funny title top-left (FE 64,
wrapped clear of the art). Verse hold follows at the chant — ref +
funny first, Sanskrit after. `holds.shiva_header` parses ref from the H1
and title from the heading line; asserts match the tantrasara set
(subtitle zone, per-row art overlap). Proven on s01 + longest title s63.
Numerals now decided: sutra ref (1.1), not file index.

## Optical header alignment (2026-11-04)
Same draw height is not the same line: FE150 numerals carry tall empty
bearings, so draw-height parity rendered title ink at y=73 against ref
ink at y=139 (measured, both lanes — tantrasara pair reads 68/138 and
stays frozen). Shiva header now offsets the funny title by the font
bearing gap (deterministic, from getbbox, no raster pass): 139/139
measured on s01, long titles (s63) still clear the art. Tantrasara
untouched — blessed pairs keep draw-height parity until an explicit call.

## Review pass 2026-11-04 (against tantrasara PROCESS/STANDARD, while batch plodded)
- Intros: s00 opens with the H1 as verse/verse (b1 chants शिवसूत्राणि before
  granny speaks) — tantrasara speaks its titles. M16 makes the English half
  the IAST line (cosmetic). Owner call: keep the chant, speak it (b1 override
  to title/granny), or clean emblem (b1 to none). s00 header correctly absent.
- s01–s77 intro shape mirrors the tantrasara b2-flip: spoken ref (b1), book
  marker (b2, only s01/s23/s33 — checked, no repetition wart), funny title
  (b3), chant (b4), spoken IAST (b5), spoken Literal (b6), show (b7). Clean.
- "Literal:" prefix IS voiced (no strip rule anywhere; tantrasara sources
  carry no such lines so shared law is silent). INTAKE's "reads them in flow"
  stands, but confirm the label word itself is wanted aloud vs stripped at
  render (shared-code change, post-freeze; tantrasara-immune by construction).
- Glossaries M15-safe by construction (deva empty forces human citation —
  heavier owner lift, zero folded-key risk). Strength, not gap. Title entries
  still missing → headers render ref+funny only, no literal/final layers.
- No drops_* / verse_gloss_* files: correct (owner-called / parked), nothing missing.
- Packs: 78 dirs on R2 but pre-alignment (stale headers) — republish queued
  behind the tantrasara goal, unchanged.

## Canonical-flow restructure 2026-11-04 (sources only, batch-safe)
- 77 units reordered to chant → IAST → gloss → funny. Ref prefixes off
  funny lines, Literal:/Literal components:/Interpretive gloss: labels
  off (all three flavors were the same slot; zero units lack a gloss).
- 214 provisional overrides remapped by text identity, 0 loses; 67
  verse-voiced IAST lines forced to granny (opening repeat uniform).
  All 78 rebuilt green 0/0. verse_gloss_sNN.json mined (77, proposed,
  owner bulk-confirms — author's own words). Term glossaries re-mined:
  no terms lost, no gloss changed.
- SHEET PROOF s01: chant card is Deva-only, exactly canon. Two gaps found
  (both post-batch engine work, NOT data): (1) sheet opener shows the
  tantrasara rainbow — render_holds never lane-routes, so no shiva sheet
  has the right art (direct intro_hold proofs aside); per canon units get
  no pic at all (s00 only), so the fix is lane-aware + s00-only art in one
  edit. (2) b1/b2 title cards render in sheets (video never shows them per
  law — sheets-only, no action). Full sheets + republish deferred until
  the post-batch engine pass so packs prove final cards, not interim.
- Post-batch engine list: H1 ref-silence rule, staged verse reveal
  (Deva → +IAST → +literal), sutra-Deva persist-by-default, s00-only
  series art, header ref-only. Then tantrasara byte-identical re-proof.

## First preview 2026-11-04 (audio only — gate held on video)
s01 fully voiced (4 groups, verse chant re-voiced after ॥१॥ strip) and
assembled (150s). Video refused by the white gate (94% white: glossaries
unconfirmed + staged reveal pending) — no wave-through, no artifact.
Preview = full mp3 (voices/order/pacing) + chant card PNG.
https://pub-87169194562a44fcb8279a799d626c62.r2.dev/shiva/preview/s01_full.mp3
https://pub-87169194562a44fcb8279a799d626c62.r2.dev/shiva/preview/s01_chant_card.png
M17 filed (digit-only Deva tokens crash sa-IN). Batch untouched: 0 FAILs.

## Intro mirror 2026-11-04 (tantrasara ch01 vs s00, ch02-22 vs s01-77)
- s00 is the series chapter-0: bell + spoken series title (b1 forced to
  granny via override, mixed-script Deva proven path) + historical
  overview over the centered pic, mirroring ch01's role/tagline/handoff
  shape. No handoff line exists — owner one-liner or cold cut to s01.
  s00 never chants (no sutra in it) — correct.
- s01+ open bell → chant with numbered header, mirroring ch02-22 minus
  spoken intros (canon: refs never spoken). Book markers (3 units) stay
  spoken — tantrasara speaks its ## headings too, so this is parity, not
  drift. H1 silence is the post-batch lane rule.
- All 78 sheet sets render green (every card asserts clean) — but the
  sheet path is lane-blind: rainbow opener, no headers anywhere. The
  s01/s63 header proofs stand via direct calls only. Full sheet +
  republish pass deferred to post-engine so packs prove final cards.
- Mirror status: karaoke/typography/engine/drops all shared code — same
  behavior by construction. Deltas are exactly the post-batch engine
  list (staged reveal, persist, ref-only header, s00-only art, H1
  silence) + owner calls (handoff, confirms, blesses, drops).

## Handoff + bell decision 2026-11-04
- s00 closes with owner's "Lets get into it." (their words, added
  verbatim). Rebuilt green.
- Bells: 77 unit bells = one every ~4 min across the series — overkill
  agreed. Canon: bell on s00 + book openers (s01/s23/s33) only; 74 units
  open cold at the chant. Needs a lane opener rule in the shared builder
  (opener is hardcoded) → post-batch engine list. Nothing changes until
  then.
- All 78 review packs republished fresh post-restructure (flow, voices,
  gloss labels all current; opener art + headers still pre-engine).

## Direction parity audit 2026-11-04 (fish scripting vs tantrasara)
- Same engine, same taste line, proven by counts: titles 100% [long pause]
  both lanes; verse 100% [slowly] both; dialogue 100% [short pause] both;
  narration beats 8.7% tantra / 4.3% shiva — content-driven (shiva runs
  longer flowing exposition + rhetorical questions), not a gap.
- Punch-word check ("Well./Wonderful./Again./Congratulations./No.") is
  0-tagged in BOTH lanes (tantrasara: 0/20, 0/10...); "Lovely." tagged in
  both. BEAT_LEXICON stays frozen — changing it would re-voice tantrasara
  mid-batch for zero parity gain.
- The "different language" laugh is the spoken scaffolding, not the
  scripting: b1 ref + b2 book marker front-load three Sanskrit-heavy lines
  in 15s. Both go silent under the lane rule (H1 refs + BOOK headings —
  sections keep the names, packs keep them readable). Chant-first cold
  opens per canon. Remaining Sanskrit-first ~15s (chant + her repeat
  before first English) IS the ordered canon; English opener only on
  owner call. Silencing shifts no IDs and re-voices nothing (b1/b2 groups
  vanish; chant/body hashes unchanged).

## Pausing pass 2026-11-04 (every block ends, fish directions hold)
- 158 narration blocks lane-wide lacked terminal punctuation and joined
  into breathless runs (s00's opening was the exhibit). All terminated at
  source; zero unterminated remain; quotes untouched (0 existed); Deva
  blocks untouched (verse owns them).
- Opening stacks canonicalized: Deva / IAST / gloss / funny, each its own
  paragraph (s16's Interpretive-variant + merges fixed; "Interpreted
  through Kṣemarāja:" was the 4th gloss label).
- Absolute rule recorded: never Deva in granny script (0 violations lane-
  wide after cleanup; tantrasara's 24 b2-flips flagged for post-batch
  ears, frozen until then).
- s00 H1 is now clean English ("The Śiva Sūtras"); opening mp3 re-cut and
  re-uploaded (pauses land where periods do).
- FISH-DIRECTION.md is the lane law (S2-only, free-pro); M17/M18 filed.
