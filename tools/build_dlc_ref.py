# -*- coding: utf-8 -*-
"""Добавляет в словарь официальный текст из всех штатных DLC третьей части."""
import os, sys, json, glob
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tlk import read_tlk
ROOT = os.path.dirname(HERE)
DLC = r"D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME3\BioGame\DLC"
pairs = {}
n = 0
for d in sorted(os.listdir(DLC)):
    if d.startswith('DLC_MOD'): continue
    cp = os.path.join(DLC, d, 'CookedPCConsole')
    if not os.path.isdir(cp): continue
    for f in os.listdir(cp):
        if not f.endswith('_INT.tlk'): continue
        ru = os.path.join(cp, f[:-8] + '_RUS.tlk')
        if not os.path.exists(ru): continue
        try:
            e = {s['id']: s['text'] for s in read_tlk(os.path.join(cp, f), False)['strings']}
            r = {s['id']: s['text'] for s in read_tlk(ru, False)['strings']}
        except Exception as ex:
            print('пропуск', d, f, ex); continue
        for i, t in e.items():
            v = r.get(i)
            if v and t.strip() and v != t:
                pairs.setdefault(t, v); n += 1
        print(f'{d}/{f}: {len(e)}')
print('пар:', len(pairs))
json.dump(pairs, open(os.path.join(ROOT, 'reference/dlc_en_ru.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for t in ['Piranha', 'N7 Piranha', 'Acolyte', 'Reegar Carbine', 'Venom Shotgun', 'Spectre Harrier', 'Geth SMG']:
    print(t, '->', pairs.get(t, '—'))
