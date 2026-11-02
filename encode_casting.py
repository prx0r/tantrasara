#!/usr/bin/env python3
"""Encode casting decisions for ch02-13 (owner-delegated review 2026-11-02).
Rules applied: skeptic/interlocutor questions -> man; demonstrations,
teachings-in-English, single-character runs -> granny; two-speaker scenes
alternate man-first; Sanskrit mantra lines -> verse. Run: python3 encode_casting.py
"""
import json, subprocess, os

BASE = os.path.expanduser('~/tantrasara')
G = 'granny'
M = 'man'
V = 'verse'

D = {
# ch02: all skeptic address
'02': {'b9': M, 'b52': M, 'b120': M},
# ch03: objections man; hello-echo + demonstrations granny... echo is 2nd voice
'03': {'b12': M, 'b76': M, 'b98': M, 'b125': G, 'b142': G, 'b408': M, 'b438': M},
# ch04
'04': {'b14': G, 'b28': G, 'b29': G, 'b30': G, 'b31': G, 'b32': G, 'b33': G,
       'b34': G, 'b46': G, 'b99': G, 'b100': G, 'b101': G, 'b102': G,
       'b126': M, 'b128': M, 'b174': G, 'b257': M, 'b265': M, 'b304': G,
       'b368': V, 'b592': G, 'b594': G, 'b616': G,
       'b700': G, 'b701': G, 'b702': G, 'b703': G, 'b704': G, 'b705': G,
       'b724': M, 'b787': G},
# ch05
'05': {'b13': G, 'b15': G, 'b17': G, 'b19': G, 'b120': G, 'b161': M,
       'b614': G, 'b630': G, 'b631': G, 'b632': G, 'b633': G, 'b637': M,
       'b732': M, 'b733': M, 'b734': M, 'b753': G, 'b754': G, 'b755': G,
       'b249': G, 'b270': G, 'b271': G, 'b272': G, 'b346': M, 'b379': M,
       'b442': G, 'b461': M, 'b539': G, 'b601': G},
# ch07: thinker chains all granny
'07': {'b16': G, 'b113': G, 'b148': G, 'b229': G, 'b267': G, 'b268': G,
       'b269': G, 'b270': G, 'b271': G},
# ch08: potter scene alternates; rest granny except skeptic
'08': {'b85': G, 'b95': G, 'b126': G, 'b162': M, 'b164': G, 'b184': G,
       'b360': G, 'b361': G, 'b362': G, 'b386': G, 'b387': G, 'b388': G,
       'b554': G, 'b555': G, 'b566': G, 'b568': G, 'b619': G, 'b620': G,
       'b621': G, 'b622': G, 'b645': G, 'b646': G, 'b647': G, 'b648': G,
       'b671': G, 'b673': G, 'b681': G, 'b689': G, 'b706': G, 'b708': G,
       'b710': G, 'b711': G, 'b730': G, 'b732': G, 'b735': G, 'b750': G,
       'b751': G, 'b752': G, 'b753': G, 'b789': G, 'b987': G, 'b991': G,
       'b992': G, 'b993': G, 'b1011': G, 'b1013': G, 'b1047': G, 'b1049': G,
       'b1347': M, 'b1420': G, 'b1421': G, 'b1422': G, 'b1440': G,
       'b1442': G, 'b1465': G, 'b1484': G},
# ch09: flower scene alternates; questions man; demonstrations granny
'09': {'b23': M, 'b24': G, 'b79': G, 'b80': G, 'b81': G, 'b82': G,
       'b188': G, 'b191': G, 'b272': G, 'b316': G, 'b318': G, 'b331': M,
       'b340': M, 'b345': M, 'b379': G, 'b380': G, 'b381': G, 'b419': M,
       'b507': G, 'b627': G, 'b654': G, 'b674': G, 'b783': G, 'b835': G,
       'b853': G, 'b1000': G, 'b1001': G, 'b1002': G, 'b1009': M},
# ch10
'10': {'b25': G, 'b27': G, 'b58': M, 'b60': M, 'b477': G, 'b488': M,
       'b564': G, 'b813': G},
# ch11: questions man; answers + demonstrations granny
'11': {'b40': M, 'b42': M, 'b44': M, 'b51': M, 'b62': M,
       'b75': G, 'b76': G, 'b77': G, 'b78': G, 'b109': M, 'b117': M, 'b123': M, 'b131': G, 'b133': G,
       'b134': G, 'b135': G, 'b161': G, 'b233': G, 'b234': G, 'b235': G,
       'b236': G, 'b237': G, 'b291': M, 'b359': M, 'b361': G, 'b363': G,
       'b365': G, 'b430': G, 'b431': G, 'b432': G, 'b433': G, 'b434': G,
       'b510': G, 'b512': G, 'b514': G, 'b516': G, 'b576': M, 'b578': G,
       'b626': G, 'b627': G, 'b628': G, 'b656': G, 'b672': M, 'b871': M,
       'b873': M, 'b875': M, 'b954': G, 'b955': G, 'b956': G, 'b1089': M,
       'b1164': G, 'b1176': M},
# ch12: self-talk chains granny; wine Q man; practitioner pair alternates
'12': {'b84': G, 'b85': G, 'b86': G, 'b87': G, 'b384': M, 'b386': M,
       'b471': G, 'b487': M, 'b490': G},
# ch13: newcomer/explainer alternate; guru demo granny; mantra verse
'13': {'b44': G, 'b45': G, 'b46': G, 'b47': G, 'b235': G, 'b237': G,
       'b239': G, 'b241': G, 'b245': G, 'b282': G, 'b310': G, 'b311': M,
       'b312': G, 'b313': M, 'b314': G, 'b315': M, 'b316': G, 'b317': M,
       'b318': G, 'b319': M, 'b465': G, 'b466': G, 'b682': G, 'b884': M,
       'b885': G, 'b886': M, 'b887': G, 'b888': M, 'b889': G, 'b890': M,
       'b891': G, 'b892': M, 'b893': M, 'b894': G, 'b950': V, 'b952': G,
       'b955': G, 'b956': G, 'b957': G, 'b958': G, 'b959': G, 'b960': G,
       'b1247': M, 'b1248': G, 'b1249': M, 'b1265': G, 'b1445': G,
       'b1537': G, 'b1538': G, 'b1539': G},
}

for ch, ov in D.items():
    json.dump(ov, open(f'{BASE}/overrides_ch{ch}.json', 'w'))
    r = subprocess.run(['python3', f'{BASE}/build_storyboard.py',
                        f'{BASE}/chapters/ch{ch}.md',
                        f'{BASE}/storyboard_ch{ch}.json',
                        f'{BASE}/overrides_ch{ch}.json'],
                       capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith('blocks=')]
    print(f'ch{ch}:', line[0] if line else r.stdout[:200] + r.stderr[:200])
