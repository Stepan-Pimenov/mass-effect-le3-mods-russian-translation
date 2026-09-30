# -*- coding: utf-8 -*-
"""Подставляет официальный русский текст из первой и второй частей — там, где моды
возвращают в игру контент ME1/ME2 (планеты, кодекс, названия систем)."""
import os, sys, json, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'source')
TR = os.path.join(ROOT, 'translation')

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('…', '...')
    s = re.sub(r"'s\b", '', s)
    s = re.sub(r"'(?=\W|$)", '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

by_text = {}
for name in ('reference/dlc_en_ru.json', 'reference/dlc2_en_ru.json', 'reference/le1_en_ru.json', 'reference/le2_en_ru.json'):
    p = os.path.join(ROOT, name)
    if not os.path.exists(p): continue
    for e, r in json.load(open(p, encoding='utf-8')).items():
        if e.strip() and r.strip():
            by_text.setdefault(norm(e), r)
print('словарь ME1/ME2:', len(by_text))

stems = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(SRC)) if f.endswith('.json')]
grand = 0
for stem in stems:
    p = os.path.join(SRC, stem + '.json')
    if not os.path.exists(p): continue
    d = json.load(open(p, encoding='utf-8'))
    if not isinstance(d, dict) or 'en' not in d: continue
    en, ru = d['en'], d['ru_existing']
    done = {}
    for f in sorted(os.listdir(TR)):
        if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.auto1.json':
            done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))
    out = {}
    for k, v in en.items():
        if k in done or not v.strip(): continue
        if ru.get(k, v) != v or is_skip(v): continue
        cand = by_text.get(norm(v))
        if cand and norm(cand) != norm(v):
            out[k] = cand
    if out:
        json.dump(out, open(os.path.join(TR, stem + '.auto1.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print(f'{stem:<40} {len(out)}')
        grand += len(out)
print('ИТОГО из ME1/ME2:', grand)
