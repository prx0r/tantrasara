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

## 2. Grasp note — what the Tantrasara is saying (2026-10-29, full read: intro + Ch 1-22 + notes)

**First third (Ch 1–4): the goal, the blindness, the fuel, the first three ways in.**
Ch 1 fixes the goal (svabhava = self-shining light-bliss-I, heart/jagadananda) and the twofold ignorance (buddhi: indeterminacy + mis-taking; paurusa: vikalpa), and sets the law: initiation without intellectual determination is ineffective.
Ch 2 (anupaya): no means — intense saktipata + once-hearing + self-discernment; strict negative logic (nothing to attain, no veil to remove) + the "condensed bliss-I with universe as reflection" positive content.
Ch 3 (sambhava): nirvikalpa absorption via reflection-view (no bimba) + the alphabet as creation's play (sun/moon vowels → bindu → visarga) + self-as-resort = living liberation.
Ch 4 (sakta): purify vikalpa by vikalpa (sattarka/bhavana = making-indistinct-distinct); yoga limbs demoted (can't touch consciousness); ritual redefined internally; antinomian corollary (purity is not in objects).
Handoff: what if vikalpa needs support in buddhi/prana/body/jars? -> Ch 5.

**Second third (Ch 5–9): the descent into means + the cosmology they rest on.**
Ch 5 (anava proper): dhyana (heart-wheel, fire/sun/moon, 12-flame Bhairava), prana-uccara (visranti through vayus), varna (sa-ha seed syllables); 7 anandas ending jagadananda; esoteric stop ("I should stop revealing...").
Ch 6: the whole 6-fold time-path lives IN breath (36 angulas, 21,600 breaths, yugas/manvantaras counted in respiration); resting/attenuating breath = consuming time = already liberated.
Ch 7: space-path — 36 tattvas + worlds catalogued as Sakti's expansion, dissolvable back into body/prana/buddhi/void ("no knowledge superior to prakriya").
Ch 8: bondage theory — two causalities (absolute vs imagined), mala as conceal-WILL (not entity), kancuka mechanics, guna genesis anti-Samkhya.
Ch 9: knower theory — 7 knowers, 15-fold prameya, tuti-moment perception (16-tuti schema, 2-tuti avesa with omniscience), 5 states to turyatita.
THIS is where the build's hardest compressions live: numbers, names, and the absolute/imagined-causality distinction must survive.

**Final third (Ch 10–22): the map, the gate, the working ritual, the summit.**
Ch 10: kala/adhvan map (5 kalas, 6 paths) — the instrument panel everything after purifies.
Ch 11: saktipata alone decides (9 outcomes incl. body-fall/Paramesvara, pratibha-guru); merit-theories refuted; true teacher = Bhairava.
Ch 12–13: purity/place/direction/trident all interiorized (bath = absorption; puja/dhyana/japa/homa redefined as ontology); outer retained to remove limitations.
Ch 14: putraka diksa (merit/demerit by bhogin-vs-mumuksu; sabija/nirbija; animal-grace; substitutes).
Ch 15: dying (Kalaratri piercing, brahmavid Administerin-whisper, Sivahasta, lightness test).
Ch 16: absent/dead initiation (great net, Sambhunatha attribution; no-mind movement by contemplation).
Ch 17: lingoddhara (crossing lineages: confession + water disposal + 100 + Vratesvara dismissal).
Ch 18: abhiseka (jnana authorizes; withholding-sin; 6-month rule; testing).
Ch 19: antya/sraddha (corpse as homa, shaking as pratyaya, festival-death of the knower, murtiyaga shortcut = putraka fruit in a year).
Ch 20: lifelong nitya/naimittika (parva calendar, pavitraka, cakra inclusivity, exposition rhetoric).
Ch 21: agama proof (prasiddhi pragmatism; Trika supremacy by fruit).
Ch 22: Kaula summit (6-grade hierarchy outer→consciousness; yamala nondual steadiness; 3 visargas + mantravIrya; khecari "I am not"; glance-initiation).
Closes by ascending inclusivity then contraction into Bhairava identity while living.

**Load-bearing threads (must survive any compression):** svatantra/svabhava/jagadananda; twofold ignorance; saktipata independence + 9 outcomes; anupaya negative logic; reflection/no-bimba; sattarka/bhavana; mala-as-will; breath-time identity (21600 etc.); sa-ha; net + lightness test; lingoddhara severance; murtiyaga shortcut; prasiddhi argument; Kaula 6-grade + glance finale.
**Known gaps (no span found):** P12-equivalent Chabbisodhana-style glossary (S6 analogue N/A here — different text); twig-fire-type intermittence mechanics appear under other names (kalana/tuti).
