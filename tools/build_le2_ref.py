# -*- coding: utf-8 -*-
"""Строит словарь en->ru из ванильных .tlk второй части (LE2) как вспомогательный."""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlk import read_tlk
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = r'D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME2\BioGame\CookedPCConsole'
en = {s['id']: s['text'] for s in read_tlk(os.path.join(P, 'BIOGame_INT.tlk'), False)['strings']}
ru = {s['id']: s['text'] for s in read_tlk(os.path.join(P, 'BIOGame_RUS.tlk'), False)['strings']}
pairs = {}
for i, e in en.items():
    r = ru.get(i)
    if r and e.strip() and r != e:
        pairs[e] = r
print('пар:', len(pairs))
json.dump(pairs, open(os.path.join(BASE, 'reference/le2_en_ru.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for t in ['Therum', 'Edolus', 'Binthu', 'Presrop', 'Ontahe', 'Erebus', 'Artemis Tau', 'Styx Theta', 'M35 Mako']:
    print(t, '->', pairs.get(t, '—'))
