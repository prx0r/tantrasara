#!/usr/bin/env python3
"""Emit build/canon/spans_pool.json from the 98-span assignment (2026-10-29
3-agent read of the full translation, lines 2436-9842) + verify contiguity
and quote presence against the source text. Run: python3 tools/build_span_pool.py"""
import json, re, sys, unicodedata

SRC = '/root/tantrasara/sources/text/reference/tantrasara-chakravarty-marjanovic.txt'
OUT = '/root/tantrasara/build/canon/spans_pool.json'

# (id, start, end, question 1-6, grade A/B/C, essay0?, gist, quote)
# questions: 1 nature 2 why-not-see 3 bound 4 ways-in 5 practice 6 death-remains
S = [
("TS1.1",2436,2509,1,"A",0,"benedictory heart/visarga + TS purpose","May my heart (hrdaya) pulsate in the form of emission"),
("TS1.2",2510,2605,2,"B",0,"twofold ignorance; initiation needs determinate conviction","knowledge is the cause of liberation"),
("TS1.3",2606,2663,3,"B",0,"ajnana=mala; self-knowledge destroys impurities","The lack of right knowledge"),
("TS1.4",2664,2754,1,"A",1,"svabhava=autonomous light, 4 upayas preview","The freedom belonging to that light is its energy of bliss"),
("TS2.1",2755,2801,4,"A",1,"anupaya: saktipata, once-hearing, no means","Could the thousand-rayed sun be illuminated by a jar"),
("TS2.2",2802,2856,4,"C",0,"Sanskrit seal of anupaya","This kind of person does not need to be restrained by disciplines"),
("TS3.1",2857,2909,4,"A",0,"sambhava: reflections, no bimba, paranada","That which cannot shine separately, but shines when merged with others"),
("TS3.2",2910,3008,1,"B",0,"alphabet cosmogony I: a-i-u, sun/moon","The Lord possesses three principal powers"),
("TS3.3",3009,3091,1,"B",0,"alphabet cosmogony II: bindu, visarga, 16 bija","Thus, visarga is the power belonging to the Lord"),
("TS3.4",3092,3161,1,"A",1,"self-as-resort = living liberation","The entire universe is shining on the clear inner core of the Self"),
("TS4.1",3162,3237,3,"B",0,"suddha-vikalpa purifies vikalpa","it is because of the power of thought constructs"),
("TS4.2",3238,3283,5,"B",0,"sattarka/bhavana; limbs rejected for Siva","determinate knowledge fulfills its purpose simply by removing the impressions of duality"),
("TS4.3",3284,3372,5,"B",0,"tarka; svabhava blossoming; yaga/homa as conviction","it ultimately terminates in consciousness free from vikalpa"),
("TS4.4",3373,3443,5,"A",1,"internalized worship definitions (yoga/homa/japa)","Yoga is offering of all entities to the Lord"),
("TS4.5",3444,3556,5,"C",0,"Para/Matrsadbhava, 12 Kalis, kalana","She is known as Kall on account of projecting, knowing, and enumerating"),
("TS4.6",3557,3645,5,"A",0,"purity not in objects; antinomian corollary","Purity is not the essential attribute of an object"),
("TS4.7",3646,3715,3,"A",0,"bound credo flipped to pati by contrary conviction","Upon perfect attainment of a firm conviction contrary"),
("TS5.1",3716,3768,5,"A",1,"anava: heart-wheel dhyana, 12-flame fire/sun/moon","One should meditate in the blissful and luminous abode"),
("TS5.2",3769,3865,5,"B",0,"uccara: prana up through vayus, duality consumed","the highest knower, free from limitation, becomes manifest"),
("TS5.3",3866,3947,5,"A",1,"7 anandas to jagadananda; sa-ha seeds","is the one blissful state, which unifies all the other"),
("TS5.4",3948,4025,5,"A",1,"varna practice: sa/ha, ka-ma, heart-throat-lips unity","seed mantras of creation"),
("TS5.5",4026,4083,5,"C",0,"recap: limited means, non-distinct result","They have been explained as limited, but at the attainment of the result"),
("TS6.1",4084,4138,5,"B",0,"sixfold path in breath; 36-digit measure","The length of the breath, both the inhalation and exhalation"),
("TS6.2",4139,4219,5,"B",0,"tithi/month rise; visuvat; eclipse unity moment","indivisible unity of the knower, known, and knowledge takes place"),
("TS6.3",4220,4310,5,"B",0,"year rise: yugas in breath, sankranti","Now the rise of the year will be described"),
("TS6.4",4311,4394,5,"A",1,"21,600 breaths = one day-night","the number of inhalations and exhalations of the breath"),
("TS6.5",4395,4474,6,"B",0,"yuga/manvantara/Brahma-day chains (cosmic cycles)","One manvantara 81 consists of 71 cycles of these four yugas"),
("TS6.6",4475,4560,5,"B",0,"creations in one breath; apana 6 causes; samana nadis","numerous creations and dissolutions occur in one breath"),
("TS6.7",4561,4675,5,"B",0,"varna counting, ksana=one thought, time-path verse","In the rising of one breath, one thought exists"),
("TS6.8",4676,4732,5,"C",0,"Sanskrit close of Ch6","Visualizing one's own power of breath"),
("TS7.1",4733,4801,1,"B",0,"desadhva: 36 tattvas, reverse dissolution","The knower of the truth of the real nature of the thirty-six tattvas"),
("TS7.2",4802,4921,6,"C",0,"bhuvana lords lists (lower to upper by initiation)","These sixteen worlds are included in the sphere of the earth"),
("TS7.3",4922,4975,1,"A",1,"conceive adhvas in body/prana/void = Bhairava fullness","Conceiving all these paths"),
("TS8.1",4976,5045,1,"B",0,"absolute vs imagined causality","the Lord, as the ultimate causal agent, manifests in all forms"),
("TS8.2",5046,5156,1,"B",0,"potter/egoism dissolved; five powers","the great Lord is consciousness and independent freedom of will"),
("TS8.3",5157,5274,3,"B",0,"pure/impure paths, longing, mala, maya","Siva is the direct creator"),
("TS8.4",5275,5379,3,"B",0,"kala/kancukas emerge; above maya/kala discrimination","the kala principle which is the bestower of limited doership"),
("TS8.5",5380,5421,3,"A",1,"veil-functions define the bound soul","then it is called a bound soul"),
("TS8.6",5422,5554,3,"C",0,"guna agitation, buddhi mirrors","the reflection of objects take place"),
("TS8.7",5555,5621,3,"C",0,"ahamkara births senses/mind/motor organs","the sense organs are born of egoity"),
("TS8.8",5622,5691,1,"A",1,"bhutas from tanmatras; all waves are own consciousness","are nothing but the order of expansion of the waves"),
("TS9.1",5692,5792,1,"B",0,"sevenfold knowers sakala-to-Siva","Lord himself has taught the existence of the sevenfold variation"),
("TS9.2",5793,5896,1,"A",1,"self-luminous svarupa for all knowers","self-luminous and it shines with reference to none"),
("TS9.3",5897,6002,1,"B",0,"13/11/9/7/5/3 variations; earth as Brahman","The earth itself is Brahman"),
("TS9.4",6003,6083,5,"A",0,"vital-energy tuitis, avesa/omniscience","analytically discerns the state of fifteen everywhere"),
("TS9.5",6084,6155,1,"C",0,"Sanskrit source verses for states block","cm 3l~cr"),
("TS9.6",6156,6201,1,"B",0,"waking/dream/sleep/fourth/turyatita","the state that transcends all"),
("TS9.7",6202,6254,1,"A",1,"fifteenfold table + attain-your-own-Self verse","Take recourse to this multitude of principles"),
("TS10.1",6255,6371,5,"C",0,"kala path, five kalas, 36 tattvas","which threads through all the worlds is called"),
("TS10.2",6372,6488,5,"C",0,"threefold/ninefold schemes; sixfold path","one path possesses sixfold divisions"),
("TS11.1",6489,6555,2,"B",0,"saktipata question; merit theories refuted","Who is entitled to receive initiation"),
("TS11.2",6556,6692,2,"A",0,"autonomous grace; ninefold typology","The descent of grace is ninefold"),
("TS11.3",6693,6783,2,"A",1,"intense grades; pratibha teacher; jivanmukti","immediately attains liberation while still living"),
("TS11.4",6784,6876,2,"B",0,"true vs incompetent teachers; independent grace","descent of energy, having grace as"),
("TS12.1",6877,6961,5,"A",1,"bath as purity/absorption","Bathing"),
("TS12.2",6962,7034,5,"A",1,"eightfold nyasa; vira bath; inner/outer","Immersion into the very nature of the Lord is called"),
("TS13.1",7035,7129,5,"B",0,"worship place, malini nyasa, vessel/door","becomes filled with satisfaction"),
("TS13.2",7130,7237,5,"B",0,"facing north; dik/center; sun as jnanasakti","itself is the center"),
("TS13.3",7238,7330,5,"B",0,"quarters, burning body-ego, cakras","fullness of Lord Bhairava"),
("TS13.4",7331,7443,5,"A",1,"trident; puja/dhyana/japa/homa redefined","the very essence of all entities, is called worship"),
("TS13.5",7444,7565,5,"C",0,"Sanskrit source verses for fire/mandala","cm 3l~cr"),
("TS13.6",7566,7648,5,"B",0,"jars, caru, blindfold, 48 rites to samayin","he should worship the mantra with flowers"),
("TS13.7",7649,7740,5,"C",0,"samayin rules, fees, Self-fullness verse","see the son of the spiritual guide"),
("TS14.1",7741,7860,5,"B",0,"putraka setup; jars; animal grace","the procedure of putraka"),
("TS14.2",7861,7932,5,"A",1,"marrow offering; pasu attains Siva-nature","then the pasu attains the nature of Siva"),
("TS14.3",7933,7991,6,"C",0,"Sanskrit bridge to death-lifting","31~ qXlct~"),
("TS15.1",7992,8042,6,"B",0,"deathbed samutkrama; brahmavidya; Sivahasta","he may become identical with Lord"),
("TS15.2",8043,8110,6,"C",0,"Sanskrit original for Ch15","3l~ tS115~"),
("TS16.1",8111,8153,6,"B",0,"absent/dead initiation; great net","to drag the desired soul near"),
("TS16.2",8154,8219,6,"C",0,"Sanskrit for net-dragging","3ilCf5tfo11e"),
("TS16.3",8220,8261,6,"A",0,"rescue via teacher; absent-living initiation","grace has unthinkably glorious capacity"),
("TS16.4",8262,8301,6,"C",0,"Sanskrit for rescue",None),  # Sanskrit-scan span (OCR), no English in range
("TS17.1",8302,8339,4,"B",0,"lingoddhara: crossing lineages, water disposal","You, Vratesvara, be impartial to him"),
("TS17.2",8340,8382,4,"C",0,"Sanskrit for reclamation","3lmF'~1"),
("TS18.1",8383,8417,5,"B",0,"abhiseka: knowledge authorizes transmission","he should not initiate an unworthy one"),
("TS18.2",8418,8470,5,"C",0,"Sanskrit for anointment","31[1 Cbl"),
("TS19.1",8471,8535,6,"A",1,"corpse rites + sraddha + festival-death + grace axiom","Siva is by nature inclined to show grace"),
("TS19.2",8536,8612,6,"C",0,"Sanskrit for final rites","3l~ ~1 ~a c=f"),
("TS20.1",8613,8655,5,"B",0,"nitya/naimittika/kamya calendar","The nitya is the one which occurs regularly"),
("TS20.2",8656,8733,5,"A",1,"mirror-identity altar worship; bonds dissolved","the net of all the bonds has dissolved"),
("TS20.3",8734,8852,5,"C",0,"living lingas list + substratum","particularly true for the vyakta form"),
("TS20.4",8853,8896,5,"C",0,"sixfold parva calendar","day of festivities"),
("TS20.5",8897,8941,5,"B",0,"cakra/murtiyaga; 1-year putraka fruit","the teacher occupies the seat in the center"),
("TS20.6",8942,8982,5,"C",0,"Sanskrit for cakra section","31~ 4 fa"),
("TS20.7",8983,9051,5,"C",0,"pavitraka timing/materials; rich-man sin","offering of the sacred thread"),
("TS20.8",9052,9121,5,"B",0,"how to expound: opponent-first, no contradiction","He should represent properly the viewpoint of the opponent"),
("TS20.9",9122,9198,3,"B",0,"knower needs no atonement; models it","steadily established in knowledge does not require"),
("TS20.10",9199,9251,5,"A",0,"gurupuja principal; ritual alone liberates","attains liberation only by the practice of rituals"),
("TS21.1",9252,9332,1,"A",1,"universe = vimarsa consciousness; sastra = Lord","This universe is composed solely of consciousness"),
("TS21.2",9333,9376,2,"B",0,"prasiddhi is agama; choose excellent results","the tradition"),
("TS21.3",9377,9458,1,"A",1,"steadiness in highest prasiddhi becomes Lord","when he becomes the supreme Lord"),
("TS22.1",9459,9499,1,"A",1,"Bliss-Brahman in body; sixfold Kaula hierarchy","Bliss is Brahman which abides in the body"),
("TS22.2",9500,9557,5,"C",0,"27 tattvas flame; sikha; trident enclosure","flame of consciousness"),
("TS22.3",9558,9658,5,"B",0,"sakti rite: mutual eagerness, secret center","The pair is mutually eager to have the nature"),
("TS22.4",9659,9705,1,"A",0,"yamala: beyond caste; compact unity","the compact unity"),
("TS22.5",9706,9746,5,"B",0,"rest/rising absorption; Kula transmission","On account of the mutual absorption of both, the very nature"),
("TS22.6",9747,9793,5,"B",0,"triangle lotus; 8 cakras; khecari","Remaining steady in firm conviction"),
("TS22.7",9794,9842,5,"B",0,"vyomacari; glance-initiation + colophon","given initiation only by mere glance"),
]

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s.lower())
    return s.strip()

src = open(SRC, encoding='utf-8', errors='replace').read()
nsrc = norm(src)
lines = src.splitlines()

# 1. contiguity + ranges
fails = []
prev_end = None
for (i, s, e, q, g, e0, gis, quo) in S:
    if s < 2436 or e > 9842 or s > e:
        fails.append(f'{i} range {s}-{e} out of bounds')
    if prev_end is not None and s != prev_end + 1:
        fails.append(f'{i} start {s} != prev end+1 {prev_end+1}')
    prev_end = e
if len(S) != 98:
    fails.append(f'count {len(S)} != 98')

# 2. quote presence (normalized substring; quotes come from agents w/ OCR)
missing = []
for (i, s, e, q, g, e0, gis, quo) in S:
    if quo is None:
        continue
    if norm(quo) not in nsrc:
        missing.append(i)

# 3. grade/question census
from collections import Counter
grades = Counter(x[4] for x in S)
quest = Counter(x[3] for x in S)
e0 = [x[0] for x in S if x[5]]

# 4. emit
spans = []
for (i, s, e, q, g, e0f, gis, quo) in S:
    spans.append({
        'span': i, 'start': s, 'end': e, 'question': q,
        'grade': g, 'essay0_candidate': bool(e0f),
        'gist': gis, 'quote': quo,
        'sanskrit_span': quo is None,
        'chapter': int(i[2:i.index('.')]) if i[2].isdigit() else int(i[3:i.index('.')]),
        'text': 'sources/text/reference/tantrasara-chakravarty-marjanovic.txt',
    })
out = {
    'schema': 'tantrasara span pool v1 (2026-10-29)',
    'source': 'sources/text/reference/tantrasara-chakravarty-marjanovic.txt',
    'line_range': [2436, 9842],
    'questions': {
        '1': 'What is my own nature?',
        '2': "Why don't I see it right now?",
        '3': 'What keeps me bound?',
        '4': 'What are the ways in?',
        '5': 'How do I practice?',
        '6': 'What about death - and what remains?',
    },
    'counts': {'total': len(spans), 'grades': dict(grades),
               'per_question': {str(k): v for k, v in sorted(quest.items())},
               'essay0_candidates': e0},
    'spans': spans,
}
json.dump(out, open(OUT, 'w'), indent=1)

print(f'total spans: {len(spans)}')
print(f'grades: {dict(grades)}')
print(f'per-question: {dict(sorted(quest.items()))}')
print(f'essay0 candidates ({len(e0)}): {", ".join(e0)}')
print(f'contiguity: {"OK 2436->9842" if not [f for f in fails if "start" in f] else "FAIL " + "; ".join(fails)}')
print(f'quotes found: {98 - len(missing)}/98  missing: {missing if missing else "none"}')
sys.exit(1 if fails or len(missing) > 10 else 0)
