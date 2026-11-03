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
    found = glob.glob(f'{VOL}/{ch}/groups/{sec_slug}/*_{voice}_{h}.wav')
    return found[0] if found else None
def to_deva(s):
    from indic_transliteration.sanscript import transliterate, IAST, DEVANAGARI
    return ' '.join(transliterate(w, IAST, DEVANAGARI) if not re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())
def to_iast(s):
    from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST
    return ' '.join(transliterate(w, DEVANAGARI, IAST) if re.search(r'[\u0900-\u097F]', w) else w
                    for w in s.split())

def main():
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
    # impact drops split groups identically in every builder (shared rule)
    _drops = _H.drops_for(sys.argv[1])
    if _drops:
        _have = {b['id'] for g in groups for b in g}
        for _bid in _drops:
            assert _bid in _have, f"drop {_bid}: block not in this render"
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
        assert f, f"missing render for {g[0]['id']}..{g[-1]['id']}"
        wavs.append((f, g))
    # MMS align each group
    os.makedirs('/tmp/mmsclip', exist_ok=True)
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
        r = subprocess.run(['node', ALIGN, f, wpath, opath, lang],
                           capture_output=True, text=True, env={**os.environ, 'NODE_PATH': NODE_MOD})
        assert os.path.exists(opath), f'MMS failed group {i}: {r.stderr[-300:]}'
        rows = json.load(open(opath, encoding='utf-8'))
        assert len(rows) == len(disp), f'{g[0]["id"]}: {len(disp)} vs {len(rows)}'
        mean = sum(x['mms'] for x in rows) / len(rows)
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
    CRISP_BED = 2.8
    def bed_after(g, nxt):
        txt = ' '.join(x.get('directed', x['text']) for x in g)
        if g[0]['type'] == 'title' or (nxt and nxt[0]['section'] != g[0]['section']):
            return 0.8
        if any(x['type'] == 'dialogue' for x in g):
            return 0.8
        if g[0]['voice'] == 'verse':
            if any(x['type'] == 'verse' and len(x['text'].split()) > 3 for x in g):
                return CRISP_BED
            return 0.6
        if '[long pause]' in txt:
            return 0.8
        return 0.3
    beds = []
    final_inputs = ['-i', BELL]
    _drop_at = {}  # group index -> pause seconds (owner-called crisp drops)
    for _bid, _spec in _drops.items():
        _gi = next((i for i, (_f, _g) in enumerate(wavs) if any(x['id'] == _bid for x in _g)), None)
        assert _gi is not None, f"drop {_bid}: block not in this render"
        _gg = wavs[_gi][1]
        assert _gg[-1]['id'] == _bid, f"drop {_bid}: not group-final — audio pauses only exist at group boundaries (M6)"
        assert _gi < len(wavs) - 1, f"drop {_bid}: nothing after it to pause before"
        assert isinstance(_spec, dict) and _spec.get('pause', 0) > 0, f"drop {_bid}: needs {{pause: seconds}}"
        _drop_at[_gi] = float(_spec['pause'])
    for i, (f, g) in enumerate(wavs):
        final_inputs += ['-i', f]
        if i < len(wavs) - 1:
            bd = bed_after(g, wavs[i + 1][1]) + _drop_at.get(i, 0.0)
            beds.append(bd)
            final_inputs += ['-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono:d={bd}']
    nAud = 1 + len(wavs) + max(0, len(wavs) - 1)
    mix = '/tmp/clip_mix.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + final_inputs +
                   ['-filter_complex',
                    '[0:a]volume=6dB[z0];[z0]' + ''.join(f'[{j}]' for j in range(1, nAud)) +
                    f'concat=n={nAud}:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', mix], check=True)
    # flat word timeline with absolute onsets (beds included via group durations)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                  '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.strip())
            for (f, g) in wavs]
    flat = []
    off = 0.99
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
    _HOLD0 = _H.intro_hold(_ch, _H.chapter_title(blocks, _gl), _lane['assets'], _lane['thumbbox'], _lane['numeral'], _lane['art_center'], _H.shiva_header(blocks) if _lane['lane'] == 'shiva' else None)
    if _HOLD0 is None:
        _HOLD0 = hold_for.get(_first_verse['id'], _blank) if _first_verse else _blank
    _HOLD0.save(f'{fdir}/00000.png')
    entries.append((0, max(0.05, flat[0][2] if flat else off), 'thumbnail'))
    idx = 1
    _first_verse_fi = next((i for i, (b, *_r) in enumerate(flat) if b['type'] == 'verse'),
                           len(flat))  # no chant in range: thumbnail holds throughout
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
    # persist: a single-word glossed chant stays up with its gloss through
    # the directly following block (e.g. "Aṇu." -> "That's you."), then
    # white. Cues always win over persist. Multi-line chant runs clear.
    _persists = []
    for _fi, (b, _k, _ton, _sw, _sub, _toff) in enumerate(flat):
        if b['type'] == 'verse' and _is_single_glossed_verse(b):
            _nxt = next((_gj for _gj in range(_fi + 1, len(flat))
                         if flat[_gj][0]['id'] != b['id']), None)
            if _nxt is not None and flat[_nxt][0]['type'] != 'verse':
                _end = next((_gk for _gk in range(_nxt + 1, len(flat))
                             if flat[_gk][0]['id'] != flat[_nxt][0]['id']),
                            len(flat))
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
        if fi < _first_verse_fi:
            return _HOLD0  # thumbnail holds from frame 0 until chanting starts
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
        if fi < _first_verse_fi:
            return 'thumbnail'
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
        assert len(lines) <= 2, 'subtitle too long'
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
        if fi in _drop_last and fi >= _first_verse_fi:
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
    _json.dump({'cuts': idx, 'duration': round(_dur, 2),
                'white_pct': round(100 * _cov.get('white', 0) / _tot),
                'coverage': {k: round(v) for k, v in sorted(_cov.items())},
                'cues': [{'t': round(s, 2), 'key': k} for s, e, k in _cues],
                'bids': bids,
                'drops': _meta_drops},
               open(os.path.splitext(sys.argv[3])[0] + '.render_meta.json', 'w'))


if __name__ == '__main__':
    import sys
    main()
