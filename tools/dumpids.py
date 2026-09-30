# -*- coding: utf-8 -*-
"""Выводит непереведённые строки указанного мода в порядке номеров, с номером и текстом."""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip, has_russian
ROOT = os.path.dirname(HERE)
stem = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
d = json.load(open(os.path.join(ROOT, 'source', stem + '.json'), encoding='utf-8'))
en, ru = d['en'], d['ru_existing']
TR = os.path.join(ROOT, 'translation')
done = set()
for f in sorted(os.listdir(TR)):
    if f.startswith(stem + '.') and f.endswith('.json'):
        done |= set(json.load(open(os.path.join(TR, f), encoding='utf-8')))
ids = sorted(int(k) for k, v in en.items()
             if k not in done and v.strip() and not has_russian(ru.get(k), v) and not is_skip(v)
             and lo <= int(k) <= hi)
print(f'### всего подходит {len(ids)}', file=sys.stderr)
for i in ids[:limit]:
    print(f'=== {i}')
    print(en[str(i)])
