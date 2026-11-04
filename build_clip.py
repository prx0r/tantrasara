#!/usr/bin/env python3
"""Generic opening/section clip: bell + groups + MMS karaoke + verse hold.
Usage: python3 build_clip.py <storyboard.json> <b1,b2,...> <out.mp4>
Hold: first verse block's card for the whole clip (verse-first standard).
Karaoke: MMS forced alignment per group (sa-IN verse, en-IN narration).
"""
import json, os, re, subprocess, sys, glob, hashlib, shutil

W, H = 1920, 1080
LIGHT, INK, FADE = (255, 255, 255), (23, 20, 15), (207, 201, 190)
FD = '/home/ubuntu/.fonts/TiroDevanagariSanskrit-Regular.ttf'
FR = '/home/ubuntu/.fonts/CormorantGaramond-Italic.ttf'
FE = '/home/ubuntu/.fonts/CormorantGaramond-Medium.ttf'
SUB_Y = 860
VOL = os.path.expanduser('~/vol/tantrasara/renders')
BELL = '/home/ubuntu/vatulanatha/sfx/bell_ding.wav'
NODE_MOD = '/tmp/mmsmod/node_modules'
ALIGN = os.path.expanduser('~/tantrasara/align_group.js')

from PIL import Image, ImageDraw, ImageFont
def F(p, s): return ImageFont.truetype(p, s)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]
def group_wav(ch, sec_slug, voice, text):
    h = hashlib.sha1(f'{voice}|{text}'.encode()).hexdigest()[:12]
    found = sorted(glob.glob(f'{VOL}/{ch}/groups/{sec_slug}/*_{voice}_{h}.wav'))
    return found[0] if found else None
def to_deva(s):
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return ' '.join(transliterate(w, IAST, DEVANAGARI) if not re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())
def to_iast(s):
    from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST
    return ' '.join(transliterate(w, DEVANAGARI, IAST) if re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())


def bed_after(group, following):
    text = ' '.join(block.get('directed', block['text']) for block in group)
    if group[0]['type'] == 'title' or (following and following[0]['section'] != group[0]['section']):
        return 0.8
    if any(block['type'] == 'dialogue' for block in group):
        return 0.8
    if group[0]['voice'] == 'verse':
        return 2.8 if any(block['type'] == 'verse' and len(block['text'].split()) > 3 for block in group) else 0.6
    if '[long pause]' in text:
        return 0.8
    return 0.3


def audio_mix_plan(wavs, all_spoken, drops, bell=BELL):
    """Build the same transitions inside parts and across safe boundaries."""
    if not wavs or not all_spoken:
        raise ValueError('cannot mix an empty clip')
    starts_at_top = wavs[0][1][0]['id'] == all_spoken[0]['id']
    last_pos = next(i for i, b in enumerate(all_spoken) if b['id'] == wavs[-1][1][-1]['id'])
    next_block = all_spoken[last_pos + 1] if last_pos + 1 < len(all_spoken) else None
    inputs = ['-i', bell] if starts_at_top else []
    count, beds, drop_at = (1 if starts_at_top else 0), [], {}
    for bid, spec in drops.items():
        gi = next((i for i, (_, group) in enumerate(wavs) if any(b['id'] == bid for b in group)), None)
        if gi is None or wavs[gi][1][-1]['id'] != bid or gi >= len(wavs) - 1:
            raise ValueError(f'drop {bid} must end a group with a following group in this part')
        drop_at[gi] = float(spec['pause'])
    for i, (path, group) in enumerate(wavs):
        inputs += ['-i', path]
        count += 1
        following = wavs[i + 1][1] if i < len(wavs) - 1 else ([next_block] if next_block else None)
        if following is not None:
            bed = bed_after(group, following) + drop_at.get(i, 0.0)
            beds.append(bed)
            inputs += ['-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono:d={bed}']
            count += 1
    streams = (('[0:a]volume=6dB[z0];[z0]' + ''.join(f'[{j}:a]' for j in range(1, count)))
               if starts_at_top else ''.join(f'[{j}:a]' for j in range(count)))
    return inputs, streams + f'concat=n={count}:v=0:a=1', beds, drop_at, starts_at_top


def validate_visual_duration(entries, audio_end):
    """Do not silently stretch many short word intervals out of sync."""
    visual_end = sum(entry[1] for entry in entries)
    if not entries or abs(visual_end - audio_end) > 0.08:
        raise RuntimeError(f'visual timeline {visual_end:.3f}s drifts from audio {audio_end:.3f}s')


def intro_end_index(starts_at_top, flat, break_bid):
    if not starts_at_top:
        return 0
    return next((i for i, (block, *_rest) in enumerate(flat) if block['id'] == break_bid), len(flat))

def main():
    # one video build at a time (M21/M28): fixed /tmp paths clobber
    # across concurrent builds. run_blocks also claims; this covers
    # direct invocations too.
    from factory_contract import (require_current_review_pack, require_storyboard_gate, require_volume_output, validate_bundle, validate_clip_range,
                                  verify_storyboard_source, video_build_lock)
    from run_all import storage_preflight
    require_volume_output(sys.argv[3])
    bundle = validate_bundle(sys.argv[1], require_approval=True)
    require_current_review_pack(sys.argv[1])
    verify_storyboard_source(sys.argv[1])
    require_storyboard_gate(sys.argv[1])
    validate_clip_range(bundle, sys.argv[2].split(','))
    storage_preflight()
    with video_build_lock():
        _main_inner()


def _main_inner():
    sb = json.load(open(sys.argv[1], encoding='utf-8'))
    bids = sys.argv[2].split(',')
    out = sys.argv[3]
    byid = {b['id']: b for b in sb['blocks']}
    ch = slug(sb.get('title', 'chapter')) or 'chapter'
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import holds as _H
    _lane = _H.lane_for(sys.argv[1])
    blocks = [byid[i] for i in bids]
    groups = []
    for b in blocks:
        if b['voice'] == 'none':
            continue
        if groups and groups[-1][0]['voice'] == b['voice'] and groups[-1][0]['section'] == b['section']:
            groups[-1].append(b)
        else:
            groups.append([b])
    # impact drops split groups identically in every builder (shared rule).
    # Phoneme singletons split first (same shared rule as render), then
    # drops. Chunk-scoped: ranges without the drop bid render clean
    # (full-chapter behavior unchanged — every drop sits in exactly
    # one chunk).
    groups = _H.split_phoneme_groups(groups)
    _drops = _H.drops_for(sys.argv[1])
    if _drops:
        _have = {b['id'] for g in groups for b in g}
        _drops = {k: v for k, v in _drops.items() if k in _have}
        if _drops:
            groups = _H.split_after(groups, set(_drops))
            print(f'impact splits at: {sorted(set(_drops))}', flush=True)
    # section dir scheme mirrors render_chapter exactly (indexed fallback)
    _sec_seen = {}
    for b in sb['blocks']:
        if b['section'] not in _sec_seen:
            _sec_seen[b['section']] = len(_sec_seen)
    _sec_slug = {s: (slug(s) or f'sec{i:02d}') for s, i in _sec_seen.items()}
    wavs = []
    for g in groups:
        text = ' '.join(x.get('directed', x['text']) for x in g)
        f = group_wav(ch, _sec_slug[g[0]['section']], g[0]['voice'], text)
        if not f:
            raise RuntimeError(f"missing render for {g[0]['id']}..{g[-1]['id']}")
        wavs.append((f, g))
    from factory_contract import clip_inputs, sha256, validate_alignment
    _source_wavs = [f for f, _ in wavs]
    _provenance = clip_inputs(sys.argv[1], bids, _source_wavs)
    # Stage wavs to local disk with retries (M21 kin): the volume mount
    # flakes reads under load ("Impossible to open" / I/O error), which
    # crashes node with empty stderr — indistinguishable from data bugs.
    # Every hot read below (align, mux, durations) uses staged copies.
    import hashlib as _hh2
    _stage = '/tmp/stage_' + re.sub(r'[^a-zA-Z0-9]+', '_', os.path.splitext(out)[0])[:60].strip('_')
    shutil.rmtree(_stage, ignore_errors=True)
    os.makedirs(_stage)
    _staged = []
    import time as _st
    for (f, g) in wavs:
        _dst = os.path.join(_stage, os.path.basename(f))
        _ok = False
        for _try in range(5):
            try:
                # source size must read stable twice (mount flakes lie)
                _s1 = os.path.getsize(f)
                _st.sleep(1)
                _s2 = os.path.getsize(f)
                if _s1 != _s2 or _s1 <= 1000:
                    _st.sleep(2 * (_try + 1))
                    continue
                shutil.copyfile(f, _dst)
                if (os.path.getsize(_dst) == _s1 and sha256(f) == sha256(_dst)):
                    _ok = True
                    break
            except OSError:
                _st.sleep(2 * (_try + 1))
        if not _ok:
            raise RuntimeError(f'unreadable or unequal wav after retries: {f} [{g[0]["id"]}]')
        _staged.append((_dst, g))
    wavs = _staged
    print(f'staged {len(wavs)} wavs -> {_stage}', flush=True)
    # MMS align each group
    os.makedirs('/tmp/mmsclip', exist_ok=True)

    def _align_one(wav, ali_words, lang, tag):
        _wp, _op = f'/tmp/mmsclip/cw{tag}.json', f'/tmp/mmsclip/ct{tag}.json'
        json.dump(ali_words, open(_wp, 'w'), ensure_ascii=False)
        # delete any stale output first: a crashed align must fail LOUD
        # here, never silently validate the previous chapter's rows (M21)
        if os.path.exists(_op):
            os.remove(_op)
        _r = subprocess.run(['node', ALIGN, wav, _wp, _op, lang],
                            capture_output=True, text=True,
                            env={**os.environ, 'NODE_PATH': NODE_MOD})
        if _r.returncode != 0 or not os.path.exists(_op):
            raise RuntimeError(f'MMS failed {tag} (exit {_r.returncode}): {_r.stderr[-300:]}')
        return json.load(open(_op, encoding='utf-8'))

    def _chunked_align(f, disp, ali, lang, gi, g):
        # Oversized groups (>300 words) OOM-kill the aligner (proven:
        # 200 words pass, 412 die) — split at a measured silence near
        # the block boundary closest to the middle, align halves,
        # offset the second. Audio, groups, hashes untouched.
        if len(disp) <= 300:
            return _align_one(f, ali, lang, gi)
        _dur = float(subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=nw=1:nk=1', f],
            capture_output=True, text=True).stdout.strip())
        _sil = subprocess.run(
            ['ffmpeg', '-v', 'info', '-i', f,
             '-af', 'silencedetect=noise=-35dB:d=0.4', '-f', 'null', '-'],
            capture_output=True, text=True).stderr
        _gaps = re.findall(r'silence_start: ([\d.]+)\nsilence_end: ([\d.]+)', _sil)
        _mids = sorted((float(a) + float(b)) / 2 for a, b in _gaps)
        _cut = _dur / 2
        if _mids:
            _cut = min(_mids, key=lambda m: abs(m - _dur / 2))
        # word index nearest the cut, snapped to a block boundary so no
        # block's words ever split across chunks
        _counts, _acc = [], 0
        for _b in g:
            _n = len([w for w in _b['text'].strip().split() if re.search(r'\w', w, re.U)])
            _counts.append(_n)
            _acc += _n
        _frac = _cut / _dur if _dur > 0 else 0.5
        _at = int(len(disp) * _frac)
        _run, _best, _bestd = 0, 0, None
        for _bi, _n in enumerate(_counts):
            _run += _n
            _dd = abs(_run - _at)
            if _bestd is None or _dd < _bestd:
                _bestd, _best = _dd, _run
        _at = min(max(_best, 1), len(disp) - 1)
        print(f'group {gi}: chunked align at {_cut:.1f}s (silence-measured)', flush=True)
        _lo, _hi = f'/tmp/mmsclip/ch{gi}a.wav', f'/tmp/mmsclip/ch{gi}b.wav'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f,
                        '-t', str(_cut), _lo], check=True)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(_cut), '-i', f,
                        _hi], check=True)
        _r1 = _align_one(_lo, ali[:_at] or ali[:1], lang, f'{gi}a')
        _r2 = _align_one(_hi, ali[_at:] or ali[-1:], lang, f'{gi}b')
        for _r in _r2:
            _r['t_on'] = round(_r['t_on'] + _cut, 3)
            _r['t_off'] = round(_r['t_off'] + _cut, 3)
        return _r1 + _r2

    al = []
    for i, (f, g) in enumerate(wavs):
        disp = []
        for b in g:
            disp += [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
        lang = 'sa-IN' if g[0]['voice'] == 'verse' else 'en-IN'
        wpath = f'/tmp/mmsclip/cw{i}.json'
        opath = f'/tmp/mmsclip/ct{i}.json'
        # sa-IN wants Devanagari (its romanizer rejects IAST diacritics);
        # en-IN wants roman (its romanizer rejects Devanagari script —
        # granny speaking inline Sanskrit, e.g. ch02 b2). Aligner input is
        # folded only; display text and 1:1 word mapping stay untouched.
        from indic_transliteration.sanscript import transliterate as _tr, IAST as _IA, DEVANAGARI as _DV
        if lang == 'sa-IN':
            ali = [(_tr(w, _IA, _DV) if not re.search(r'[\u0900-\u097F]', w) else w) for w in disp]
        else:
            ali = [(_tr(w, _DV, _IA) if re.search(r'[\u0900-\u097F]', w) else w) for w in disp]
        json.dump(ali, open(wpath, 'w'), ensure_ascii=False)
        # delete any stale output first: a crashed align must fail LOUD here,
        # never silently validate the previous chapter's rows (M21)
        if os.path.exists(opath):
            os.remove(opath)
        if len(disp) > 300:
            rows = _chunked_align(f, disp, ali, lang, i, g)
            mean = validate_alignment(rows, len(disp), g[0]['id'])
            print(f'group {i}: n={len(rows)} mean={mean:.3f} CHUNKED', flush=True)
            al.append((g, rows))
            continue
        r = subprocess.run(['node', ALIGN, f, wpath, opath, lang],
                           capture_output=True, text=True, env={**os.environ, 'NODE_PATH': NODE_MOD})
        if r.returncode != 0 or not os.path.exists(opath):
            raise RuntimeError(f'MMS failed group {i} (exit {r.returncode}): {r.stderr[-300:]}')
        rows = json.load(open(opath, encoding='utf-8'))
        mean = validate_alignment(rows, len(disp), g[0]['id'])
        print(f'group {i}: n={len(rows)} mean={mean:.3f}', flush=True)
        al.append((g, rows))
    # assembly: bell(+6dB) + groups with rhythm beds by boundary —
    # 0.8 after titles / long-pause beats / dialogue / section ends,
    # CRISP 2.8 after multi-line chants (the verse lingers and holds, then
    # boom white — beds belong to the prior word, so the card holds them),
    # 0.6 after single-word chants (they persist into speech, no white),
    # 0.3 in flow. Deterministic, no model-mood gaps.
    # Drops (drops_chNN.json, owner calls): {bid: {pause}} — the active
    # hold clears at that block's group end and the bed grows by pause.
    # Audio pauses only exist at group boundaries (M6: groups are atomic);
    # a non-final bid fails loud. Displayed in render_meta under 'drops'.
    _all_spoken = [b for b in sb['blocks'] if b['id'] != 'b_opener' and b['voice'] != 'none']
    final_inputs, audio_filter, beds, _drop_at, _starts_at_top = audio_mix_plan(wavs, _all_spoken, _drops)
    mix = '/tmp/clip_mix.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + final_inputs +
                   ['-filter_complex', audio_filter,
                    '-c:a', 'libmp3lame', '-b:a', '192k', mix], check=True)
    # flat word timeline with absolute onsets (beds included via group durations)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                  '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.strip())
            for (f, g) in wavs]
    flat = []
    off = (float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                '-of', 'default=nw=1:nk=1', BELL], capture_output=True,
                               text=True, check=True).stdout.strip()) if _starts_at_top else 0.0)
    _grp_start = {}
    for gi, ((f, g), rows) in enumerate(zip(wavs, [r for _, r in al])):
        _grp_start[gi] = off
        wi = 0
        for b in g:
            sw = [w for w in b['text'].strip().split() if re.search(r'\w', w, re.U)]
            seg = rows[wi:wi + len(sw)]
            assert len(seg) == len(sw), f"{b['id']}: {len(sw)} vs {len(seg)}"
            # subtitle display: Devanagari has no glyphs in the subtitle
            # face (tofu — M3), so Deva-script words render as IAST for
            # EVERY voice; all else verbatim. Mixed Deva+roman lines split
            # first (M4): when the roman half duplicates the chant, the
            # Deva words blank and the author's own romanisation carries
            # the karaoke — never both (karaoke indices remap to visible
            # words below). Counts stay 1:1 with sw throughout.
            import unicodedata as _ud2
            _dt = [_w for _w in sw if re.search(r'[\u0900-\u097F]', _w)]
            _rt = [_w for _w in sw if not re.search(r'[\u0900-\u097F]', _w) and re.search(r'\w', _w, re.U)]
            _f2 = lambda s: ''.join(c for c in _ud2.normalize('NFD', s.lower()) if _ud2.category(c) != 'Mn')
            _dup = bool(_dt and _rt and _f2(' '.join(_rt)) == _f2(to_iast(' '.join(_dt))))
            sub = ['' if (_dup and re.search(r'[\u0900-\u097F]', w) is not None) else (to_iast(w) if re.search(r'[\u0900-\u097F]', w) else w) for w in sw]
            # punctuation the \w filter dropped (em-dashes etc.) rides on the
            # neighboring display word — counts stay 1:1, karaoke untouched.
            # blank display words (deduped duplicates) take nothing.
            _raw = b['text'].strip().split()
            _sub2 = []
            for _w in _raw:
                if not re.search(r'\w', _w, re.U):
                    if _sub2 and _sub2[-1].strip():
                        _sub2[-1] = (_sub2[-1] + ' ' + _w.strip()).strip()
                    continue
                _sub2.append(sub[len(_sub2)])
            assert len(_sub2) == len(sub), f"{b['id']}: sub length drift"
            sub = _sub2
            for j, r in enumerate(seg):
                flat.append((b, j, r['t_on'] + off, sw, sub, r['t_off'] + off))
            wi += len(sw)
        off += durs[gi] + (beds[gi] if gi < len(beds) else 0)
    # subtitle word dump for the gate (H5/H6): every spoken word with its
    # displayed form and onset — the gate scans for Devanagari leaks and
    # asserts display-word counts match spoken-word counts per block.
    _subs = []
    for (b, k, t_on, sw, sub, t_off) in flat:
        _subs.append({'bid': b['id'], 't': round(t_on, 2), 'w': sw[k] if k < len(sw) else '',
                      's': sub[k] if k < len(sub) else ''})
    json.dump(_subs, open(os.path.splitext(out)[0] + '.subs.json', 'w', encoding='utf-8'),
              ensure_ascii=False)
    # entries carry citation Deva + T1 literal + final gloss; video shows
    # the literal only once its own literal_status is confirmed.
    # Lane-aware: shiva storyboards resolve the shiva lane.
    import glob as _gg
    _lane = _H.lane_for(sys.argv[1])
    _gl = {}
    if os.path.exists(_lane['glossary']):
        _raw = json.load(open(_lane['glossary'], encoding='utf-8'))
        for k, v in _raw.items():
            if not (isinstance(v, dict) and v.get('status') == 'confirmed' and v.get('gloss')):
                continue
            _gl[k] = {'deva': v.get('deva', ''), 'gloss': v.get('gloss', ''),
                      'literal': v.get('literal', '') if v.get('literal_status') == 'confirmed' else ''}
    print(f'confirmed glossary terms: {len(_gl)}', flush=True)
    # verse cards: Deva + IAST (plus full term layers on glossed singles
    # via _gl). Whole-chant T1/L3 layers parked — see BUILD-NOTES.
    # holds: verse cards while chanting, clean white once speech starts.
    # (owner: no title cards shown; Sanskrit clears when granny takes over)
    _holds = _H.build_holds([b for b in blocks if b['type'] != 'title' or True])
    hold_for = {}
    _blank = Image.new('RGB', (W, H), LIGHT)
    for h in _holds:
        img = _H.render_hold(h, None, _gl)
        for b in h:
            hold_for[b['id']] = img
    # title blocks never shown: map them (and opener) appropriately
    fdir = '/tmp/clip_frames'
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    entries, idx = [], 0
    # opener: intro bug (thumbnail; ch02+ carry the chapter numeral
    # top-right, ch01 blessed reference stays clean), else first verse hold
    _first_verse = next((b for b in blocks if b['type'] == 'verse'), None)
    _ch = _lane['ch']
    # Block ranges that do NOT start at the chapter top (b1) open on clean
    # white instead of the thumbnail: a mid-chapter segment must never
    # re-show the intro bug. Full-chapter runs always start at b1, so their
    # behavior is unchanged.
    # Mid-chapter ranges never show the intro: skip its render entirely
    # (a body chant resolved as "title" can never fit the header and
    # the image is discarded anyway).
    _HOLD0 = None
    if _starts_at_top:
        _HOLD0 = _H.intro_hold(_ch, _H.chapter_title(blocks, _gl), _lane['assets'], _lane['thumbbox'], _lane['numeral'], _lane['art_center'], _H.shiva_header(blocks) if _lane['lane'] == 'shiva' else None)
    if _HOLD0 is None:
        _HOLD0 = hold_for.get(_first_verse['id'], _blank) if _first_verse else _blank
    _PRE_IMG = _HOLD0 if _starts_at_top else _blank
    _PRE_KIND = 'thumbnail' if _starts_at_top else 'white'
    # A mid-chapter part can start at t=0. A forced 50ms blank would shift
    # every following subtitle/card relative to the audio at each join.
    prefix = flat[0][2] if flat else off
    idx = 0
    if prefix > 0:
        _PRE_IMG.save(f'{fdir}/00000.png')
        entries.append((0, prefix, _PRE_KIND))
        idx = 1
    # Intro scope (owner call 2026-11-04): the thumbnail holds the intro
    # only — through the first tone break (section change, long-pause
    # beat, dialogue entry) or the first chant, whichever comes first.
    # Never the whole road to a late first verse.
    def _is_break(b, prev):
        if b['type'] == 'verse':
            return True
        if b['type'] == 'dialogue':
            return True
        if b.get('directed', '').startswith('[long pause]'):
            return True
        return prev is not None and b['section'] != prev['section']
    _ib = next((b for b in blocks[1:] if _is_break(b, blocks[0])), None)
    _intro_end_fi = intro_end_index(_starts_at_top, flat, _ib['id'] if _ib else None)
    _first_verse_fi = next((i for i, (b, *_r) in enumerate(flat) if b['type'] == 'verse'),
                           len(flat))  # no chant in range: verse holds never fire
    # term cues: (start, end, image) from confirmed glossary mentions
    import unicodedata as _ud
    _fold = lambda s: ''.join(c for c in _ud.normalize('NFD', s.lower()) if _ud.category(c) != 'Mn')
    _cue_starts = {}
    for (b, k, t_on, sw, sub, t_off) in flat:
        if b['type'] not in ('narration', 'dialogue'):
            continue
        for j, w in enumerate(sw):
            key = _fold(w.strip('.,!?;:\'"—-'))
            if key in _gl and (b['id'], j) not in _cue_starts:
                _cue_starts[(b['id'], j)] = key
                break
    _events = []
    for (b, k, t_on, sw, sub, t_off) in flat:
        if b['type'] in ('verse', 'title', 'figure', 'dialogue') or b.get('directed', '').startswith('[long pause]'):
            _events.append(t_on)
    _events = sorted(set(_events))
    def _next_event(t):
        for e in _events:
            if e > t + 0.05:
                return e
        return off
    _term_imgs = {}
    def _stack_img(keys):
        # list engine: count decides the shape, one standard Deva size
        return _H.render_list(keys, {k: _gl[k] for k in keys})
    def _single_img(key):
        # single centered three-layer term card from the glossary entry
        # (literal withheld unless its own status is confirmed — gated above)
        e = _gl[key]
        return _H.render_term_card(e.get('deva') or key, _H.to_iast(e.get('deva') or key),
                                  e.get('literal', ''), e.get('gloss', ''))
    def _is_single_glossed_verse(b):
        return (b['type'] == 'verse' and len(b['text'].split()) <= 3
                and _fold(b['text'].strip('.,!?;:\'"—-')) in _gl)
    for key in set(_cue_starts.values()):
        _term_imgs[key] = _single_img(key)
    _cues = []
    for (bid, j), key in _cue_starts.items():
        t0 = next(t for (b, k, t, sw, sub, e) in flat if b['id'] == bid and k == j)
        _cues.append((t0, _next_event(t0), key))
    _cues.sort()
    # a newer cue always supersedes: clamp each span at the next cue start
    _cues = [(s, min(e, _cues[i + 1][0]) if i + 1 < len(_cues) else e, k)
             for i, (s, e, k) in enumerate(_cues)]
    # list runs: 2+ cues with no event gap between them (each span ends
    # exactly where the next begins) accumulate into one count-shaped card
    # (2 side by side, 3 row-or-triangle, 4 corners, 5 corners + middle).
    _run_of, _run_keys = {}, {}
    _i = 0
    while _i < len(_cues):
        _j = _i
        while _j + 1 < len(_cues) and _cues[_j][1] == _cues[_j + 1][0]:
            _j += 1
        if _j - _i + 1 >= 2:
            _keys = [_cues[_n][2] for _n in range(_i, _j + 1)]
            for _n in range(_i, _j + 1):
                _run_of[_n] = (_i, _n - _i)
                _run_keys[_i] = _keys
        _i = _j + 1
    for _ri, _keys in _run_keys.items():
        for _p in range(1, len(_keys) + 1):
            _term_imgs[('stack', _ri, _p)] = _stack_img(_keys[:_p])
    # persist (owner call 2026-11-04, extended same day): EVERY verse hold
    # stays up UNTIL THE NEXT SANSKRIT WORD — the next cue onset, the
    # next chant onset, or the next tone break (dialogue / long-pause /
    # section change returns white by law), whichever comes first; to
    # the range end if none follows. Verse cards hold as standard so no
    # chant ever dies into dead air. Cues always win over persist.
    # Tone-break onsets per flat row:
    _brk = []
    _psec = None
    for _fi2, (_bb, _kk, _tt, _sww, _ssb, _te) in enumerate(flat):
        if _bb['type'] == 'dialogue' or _bb.get('directed', '').startswith('[long pause]'):
            _brk.append(_tt)
        elif _psec is not None and _bb['section'] != _psec and _kk == 0:
            _brk.append(_tt)
        if _kk == 0:
            _psec = _bb['section']
    _brk = sorted(set(_brk))
    _cue_times = sorted(set(s for s, e, k in _cues))
    _persists, _persist_seen = [], set()
    for _fi, (b, _k, _ton, _sw, _sub, _toff) in enumerate(flat):
        if b['type'] == 'verse' and b['id'] not in _persist_seen:
            _persist_seen.add(b['id'])
            _after = [t for t in _cue_times if t > _ton + 0.05]
            _after += [t for t in _brk if t > _ton + 0.05]
            _end_t = min(_after) if _after else off
            _end = next((j for j in range(_fi + 1, len(flat) + 1)
                         if j >= len(flat) or flat[j][2] >= _end_t - 1e-6),
                        len(flat))
            if _end <= _fi + 1:
                continue
            _term_imgs[('persist', b['id'])] = hold_for.get(b['id'], _blank)
            _persists.append((_ton, flat[_end - 1][5], b['id']))
    print(f'term cues: {[(k, round(s)) for s, e, k in _cues]}', flush=True)
    print(f'list runs: {[(_keys) for _keys in _run_keys.values()]}', flush=True)
    print(f'persists: {[(bid, round(s)) for s, e, bid in _persists]}', flush=True)
    # drop split points: the final flat index of each dropped group, with
    # (bed start, next onset). The card holds through the last spoken word;
    # a clean white frame (no subtitle) spans the pause. Thumbnail sacred.
    _drop_last = {}
    for _gi in sorted(_drop_at):
        _t_end = _grp_start[_gi] + durs[_gi]
        _t_next = _grp_start[_gi + 1] if _gi + 1 in _grp_start else off
        _fis = [fi for fi, (b, *_r) in enumerate(flat)
                if any(x['id'] == b['id'] for x in wavs[_gi][1])]
        if _fis:
            _drop_last[_fis[-1]] = (_t_end, _t_next)
    if _drop_last:
        print(f'drops: {[(round(s, 1), round(e, 1)) for s, e in _drop_last.values()]}', flush=True)
    def hold_img(b, fi):
        t = flat[fi][2]
        if fi < _intro_end_fi:
            return _PRE_IMG  # thumbnail for the intro only; white for mid-chapter ranges
        if b['type'] == 'verse':
            return hold_for.get(b['id'], _blank)
        for _n, (s, e, key) in enumerate(_cues):
            if s <= t < e:
                if _n in _run_of:
                    _ri, _p = _run_of[_n]
                    return _term_imgs[('stack', _ri, _p + 1)]
                return _term_imgs[key]
        for (s, e, bid) in _persists:
            if s <= t < e:
                return _term_imgs[('persist', bid)]
        return _blank
    def hold_kind(b, fi):
        t = flat[fi][2]
        if fi < _intro_end_fi:
            return _PRE_KIND
        if b['type'] == 'verse':
            return 'verse'
        for _n, (s, e, key) in enumerate(_cues):
            if s <= t < e:
                if _n in _run_of:
                    return 'stack:' + key
                return 'term:' + key
        for (s, e, bid) in _persists:
            if s <= t < e:
                return 'verse-hold:' + bid
        return 'white'
    for fi, (b, k, t_on, sw, sub, t_off) in enumerate(flat):
        im = hold_img(b, fi).copy()
        d = ImageDraw.Draw(im)
        # subtitle karaoke, wrapped <=2 lines. blank words (deduped
        # duplicates) collapse for display; k maps to the visible index.
        vis = [w for w in sub if w.strip()]
        vk = sum(1 for x in sub[:k + 1] if x.strip()) - 1
        # subtitle karaoke, wrapped <=2 lines
        fnt = F(FE, 46)
        lines, cur = [], ''
        for w_ in vis:
            t_ = (cur + ' ' + w_).strip()
            if d.textlength(t_, font=fnt) > 1750 and cur:
                lines.append(cur); cur = w_
            else:
                cur = t_
        if cur:
            lines.append(cur)
        if len(lines) > 2:
            fnt = F(FE, 40)
            lines, cur = [], ''
            for w_ in vis:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        for _sz in (36, 32):
            if len(lines) <= 2:
                break
            fnt = F(FE, _sz)
            lines, cur = [], ''
            for w_ in vis:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        # windowed karaoke (owner call 2026-11-04): blocks that cannot
        # fit two lines at any readable size show a two-line window
        # around the spoken word (current line + next, last two at the
        # end) instead of shrinking to dust. Every word still appears
        # with karaoke over time; short blocks behave exactly as before.
        _win = False
        if len(lines) > 2:
            _win = True
            fnt = F(FE, 40)
            lines, cur = [], ''
            for w_ in vis:
                t_ = (cur + ' ' + w_).strip()
                if d.textlength(t_, font=fnt) > 1750 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
        counts, acc = [], 0
        for ln in lines:
            counts.append(acc); acc += len(ln.split())
        li = next((i for i in range(len(lines)) if vk < counts[i] + len(lines[i].split())), len(lines) - 1)
        if _win:
            _lo = li if li < len(lines) - 1 else max(0, len(lines) - 2)
            lines = lines[_lo:_lo + 2]
            counts, acc = [], 0
            for ln in lines:
                counts.append(acc); acc += len(ln.split())
            li = next((i for i in range(len(lines)) if vk < counts[i] + len(lines[i].split())), len(lines) - 1)
        rel = vk - counts[li]
        for j, ln in enumerate(lines):
            wl = ln.split()
            if j < li:
                lit, rest = ln, ''
            elif j > li:
                lit, rest = '', ln
            else:
                lit = ' '.join(wl[:rel + 1]) + (' ' if rel + 1 < len(wl) else '')
                rest = ' '.join(wl[rel + 1:])
            yy = SUB_Y + j * 62
            if lit:
                d.text(((W - d.textlength(ln, font=fnt)) / 2, yy), lit, font=fnt, fill=INK)
            d.text(((W - d.textlength(ln, font=fnt)) / 2 + d.textlength(lit, font=fnt), yy),
                   rest, font=fnt, fill=FADE)
        im.save(f'{fdir}/{idx:05d}.png')
        nxt = flat[fi + 1][2] if fi + 1 < len(flat) else off
        if fi in _drop_last and fi >= _intro_end_fi:
            # crisp drop: card holds through the last spoken word, then a
            # clean white frame (no subtitle) across the pause to next onset
            _tend, _tnext = _drop_last[fi]
            entries.append((idx, max(0.03, _tend - t_on), hold_kind(b, fi)))
            idx += 1
            _blank.copy().save(f'{fdir}/{idx:05d}.png')
            entries.append((idx, max(0.03, _tnext - _tend), 'white'))
            idx += 1
            continue
        entries.append((idx, max(0.03, nxt - t_on), hold_kind(b, fi)))
        idx += 1
    validate_visual_duration(entries, off)
    # coverage: seconds per hold kind (white = clean default, not content).
    # opener frame has no kind yet — classify it as thumbnail.
    from collections import defaultdict as _dd
    _cov = _dd(float)
    for (_i, du, hk) in entries:
        _cov[hk if hk else 'thumbnail'] += du
    _tot = sum(_cov.values()) or 1
    print('COVERAGE ' + ' '.join(f'{k}={v:.0f}s' for k, v in sorted(_cov.items())) +
          f' white_pct={100 * _cov.get("white", 0) / _tot:.0f}%', flush=True)
    # White gate REMOVED per owner order 2026-11-04 ("get them live"):
    # unconfirmed glossaries render white BY DESIGN, so a white-heavy clip
    # is a data state, not a defect. Coverage still prints for the log.
    # (Was: SystemExit past 85% white on 60s+ clips.)
    # concat list (duration,idx pairs; kind is metadata only)
    lines = []
    for i, du, _hk in entries:
        lines += [f"file '{fdir}/{i:05d}.png'", f"duration {du:.4f}"]
    lines.append(f"file '{fdir}/{entries[-1][0]:05d}.png'")
    open(f'{fdir}/concat.txt', 'w').write('\n'.join(lines) + '\n')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', f'{fdir}/concat.txt', '-i', mix,
                    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', sys.argv[3]], check=True)
    print('OK:', sys.argv[3], f'{idx} cuts')
    # golden input: machine-readable render fingerprint (see golden.py)
    import json as _json
    _dur = float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=nw=1:nk=1', sys.argv[3]],
        capture_output=True, text=True, check=True).stdout.strip())
    _meta_drops = {}
    for _fi, (_tend, _tnext) in _drop_last.items():
        _bid = flat[_fi][0]['id']
        _meta_drops[_bid] = {'pause': _drops.get(_bid, {}).get('pause'),
                             'at': round(_tend, 2)}
    if clip_inputs(sys.argv[1], bids, _source_wavs)['inputs_sha256'] != _provenance['inputs_sha256']:
        raise RuntimeError('render inputs changed during the build; output is not proven')
    _provenance['video_sha256'] = sha256(sys.argv[3])
    _provenance['subs_sha256'] = sha256(os.path.splitext(sys.argv[3])[0] + '.subs.json')
    _json.dump({'cuts': idx, 'duration': round(_dur, 2),
                'white_pct': round(100 * _cov.get('white', 0) / _tot),
                'coverage': {k: round(v) for k, v in sorted(_cov.items())},
                'cues': [{'t': round(s, 2), 'key': k} for s, e, k in _cues],
                'bids': bids,
                'drops': _meta_drops, 'provenance': _provenance},
               open(os.path.splitext(sys.argv[3])[0] + '.render_meta.json', 'w'))


if __name__ == '__main__':
    import sys
    main()
