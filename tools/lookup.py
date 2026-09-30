"""Поиск по ванильному переводу LE3.  python lookup.py "Illusive Man" [ещё запросы...]"""
import json, os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, 'reference', 'vanilla_en_ru.json'), encoding='utf-8'))

for q in sys.argv[1:]:
    print(f'===== {q}')
    ql = q.lower()
    exact = [(e, r) for e, r in P.items() if e.strip().lower() == ql]
    short = [(e, r) for e, r in P.items() if ql in e.lower() and len(e) <= 60]
    seen = set()
    out = exact + sorted(short, key=lambda x: len(x[0]))
    n = 0
    for e, r in out:
        if e in seen:
            continue
        seen.add(e)
        print(f'  {e}  ->  {r}')
        n += 1
        if n >= 8:
            break
    if n == 0:
        print('  (не найдено)')
