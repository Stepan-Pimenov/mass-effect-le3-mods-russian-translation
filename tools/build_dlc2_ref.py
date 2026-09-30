# -*- coding: utf-8 -*-
"""Добавляет официальный текст из DLC второй части (Логово Серого Посредника и прочее)."""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tlk import read_tlk
ROOT = os.path.dirname(HERE)
DLC = r"D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME2\BioGame\DLC"
pairs = {}
for d in sorted(os.listdir(DLC)):
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
                pairs.setdefault(t, v)
print('пар из DLC ME2:', len(pairs))
p = os.path.join(ROOT, 'reference/dlc2_en_ru.json')
json.dump(pairs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print([k for k in pairs if 'unable to tap geth' in k][:1])
