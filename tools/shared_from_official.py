"""DLC_Shared у Project Variety — это копия общего файла официальных DLC.
Берём официальный русский DLC_Shared_RUS.tlk и подставляем по номерам строк.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tlk import read_tlk

ROOT = os.path.dirname(HERE)
OFF = (r"D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME3"
       r"\BioGame\DLC\DLC_CON_DH1\CookedPCConsole")

off_en = {s['id']: s['text'] for s in read_tlk(os.path.join(OFF, 'DLC_Shared_INT.tlk'), msb_first=False)['strings']}
off_ru = {s['id']: s['text'] for s in read_tlk(os.path.join(OFF, 'DLC_Shared_RUS.tlk'), msb_first=False)['strings']}

d = json.load(open(os.path.join(ROOT, 'source', 'DLC_Shared.json'), encoding='utf-8'))
en = d['en']

out = {}
missed = []
for k, v in en.items():
    sid = int(k)
    ru = off_ru.get(sid)
    if ru and ru.strip() and ru != v:
        out[k] = ru
    elif v.strip() and v.strip() not in ('Male', 'Female', 'en-us'):
        missed.append((k, v))

json.dump(out, open(os.path.join(ROOT, 'translation', 'DLC_Shared.auto.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('подставлено официальных строк:', len(out))
print('осталось без перевода:', len(missed))
for k, v in missed[:40]:
    print('   ', k, '|', v[:70])
