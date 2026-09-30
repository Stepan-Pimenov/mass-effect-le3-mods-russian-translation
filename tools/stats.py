import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import skip as is_skip
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'source')
TR = os.path.join(ROOT, 'translation')

todo_all = Counter()
per_file = {}
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.json') or f.startswith('_'):
        continue
    stem = f[:-5]
    d = json.load(open(os.path.join(SRC, f), encoding='utf-8'))
    en, ru = d['en'], d['ru_existing']
    done = {}
    for g in sorted(os.listdir(TR)):
        if g.startswith(stem + '.') and g.endswith('.json'):
            done.update(json.load(open(os.path.join(TR, g), encoding='utf-8')))
    todo = {k: v for k, v in en.items()
            if v.strip() and ru.get(k, v) == v and k not in done and not is_skip(v)}
    if todo:
        per_file[stem] = todo
        for v in todo.values():
            todo_all[v] += 1

print('--- по файлам ---')
for stem, t in sorted(per_file.items(), key=lambda x: -sum(len(v) for v in x[1].values())):
    print(f'{stem:<38}{len(t):>6} строк{sum(len(v) for v in t.values()):>10} симв')

tot = sum(todo_all.values())
print()
print(f'всего строк: {tot}, уникальных: {len(todo_all)}')

buckets = Counter()
chars = Counter()
for text, c in todo_all.items():
    L = len(text)
    b = ('1-30' if L <= 30 else '31-80' if L <= 80 else '81-200' if L <= 200
         else '201-500' if L <= 500 else '500+')
    buckets[b] += 1
    chars[b] += L
print()
for b in ('1-30', '31-80', '81-200', '201-500', '500+'):
    print(f'{b:>8}: {buckets[b]:>5} шт, {chars[b]:>9} симв')
