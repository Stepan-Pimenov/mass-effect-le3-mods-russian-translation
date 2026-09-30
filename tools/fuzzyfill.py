# -*- coding: utf-8 -*-
"""Подставляет официальный русский текст для строк мода, почти совпадающих с ванильными."""
import json, sys, re, difflib, os, argparse
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'tools'))
from common import skip as is_skip, has_russian

ref = json.load(open(os.path.join(BASE, 'reference/vanilla_en_ru.json'), encoding='utf-8'))
for extra in ('reference/dlc_en_ru.json', 'reference/dlc2_en_ru.json', 'reference/le1_en_ru.json', 'reference/le2_en_ru.json'):
    p2 = os.path.join(BASE, extra)
    if os.path.exists(p2):
        for k, v in json.load(open(p2, encoding='utf-8')).items():
            ref.setdefault(k, v)

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

WORD = re.compile(r"[a-zA-Z]{5,}")
index = defaultdict(list)
refn = {}
for k in ref:
    n = norm(k)
    refn[k] = n
    for w in set(WORD.findall(n.lower())):
        index[w].append(k)

def find(q, minratio):
    qn = norm(q)
    words = set(WORD.findall(qn.lower()))
    if not words: return None
    cnt = defaultdict(float)
    for w in words:
        lst = index.get(w)
        if not lst or len(lst) > 8000: continue
        wt = 1.0 / len(lst)
        for k in lst:
            cnt[k] += wt
    if not cnt: return None
    cands = sorted(cnt.items(), key=lambda x: -x[1])[:60]
    best = (0, None)
    for k, _ in cands:
        rn = refn[k]
        if abs(len(rn) - len(qn)) > max(60, len(qn) * 0.35): continue
        r = difflib.SequenceMatcher(None, qn, rn).ratio()
        if r > best[0]: best = (r, k)
    if best[0] >= minratio: return best
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--min', type=float, default=0.93)
    ap.add_argument('--minlen', type=int, default=40)
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    TR = os.path.join(BASE, 'translation')
    for stem in a.files:
        d = json.load(open(os.path.join(BASE, 'source', stem + '.json'), encoding='utf-8'))
        ens, rux = d['en'], d['ru_existing']
        done = {}
        for f in sorted(os.listdir(TR)):
            if f.startswith(stem + '.') and f.endswith('.json') and f not in (stem + '.fuzzy.json',):
                done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))
        out = {}
        for sid, en in ens.items():
            if sid in done or not en.strip(): continue
            if has_russian(rux.get(sid), en): continue
            if len(en) < a.minlen or is_skip(en): continue
            res = find(en, a.min)
            if res:
                out[sid] = ref[res[1]]
                if a.report: print(f'-- {sid} {res[0]:.3f} {en[:70]!r}')
        if out:
            path = os.path.join(TR, stem + '.fuzzy.json')
            out['_comment'] = 'автоподстановка официального текста по близкому совпадению'
            json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'{stem}: подставлено {len(out)-1}')
        else:
            print(f'{stem}: нет совпадений')

main()
