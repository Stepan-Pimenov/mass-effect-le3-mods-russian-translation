# -*- coding: utf-8 -*-
"""Ищет имя собственное в ванильных словарях LE3 и LE2: точное совпадение, затем вхождение."""
import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d3 = json.load(open(os.path.join(BASE, 'reference/vanilla_en_ru.json'), encoding='utf-8'))
p2 = os.path.join(BASE, 'reference/le2_en_ru.json')
d2 = json.load(open(p2, encoding='utf-8')) if os.path.exists(p2) else {}
def _ld(n):
    p = os.path.join(BASE, 'reference', n)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
dD = _ld('dlc_en_ru.json')
dD.update(_ld('dlc2_en_ru.json'))
d1 = _ld('le1_en_ru.json')

def report(q):
    for tag, d in (('LE3', d3), ('DLC', dD), ('LE1', d1), ('LE2', d2)):
        if q in d:
            print(f'{q}\t[{tag} точно]\t{d[q]}')
            return
    for tag, d in (('LE3', d3), ('DLC', dD), ('LE1', d1), ('LE2', d2)):
        hits = [(k, v) for k, v in d.items() if len(k) < 260 and re.search(r'\b' + re.escape(q) + r'\b', k)]
        if hits:
            k, v = min(hits, key=lambda x: len(x[0]))
            print(f'{q}\t[{tag}]\t{v}')
            return
    print(f'{q}\t—')

for q in sys.argv[1:]:
    report(q)
