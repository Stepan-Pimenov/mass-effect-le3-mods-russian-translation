"""Выводит непереведённые строки мода.
python dump.py <stem> [--min N] [--max N] [--skip N] [--limit N]
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import skip as is_skip, has_russian

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'source')
TR = os.path.join(ROOT, 'translation')

stem = sys.argv[1]


def arg(name, default):
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


mn, mx = arg('--min', 0), arg('--max', 10 ** 9)
offset, limit = arg('--skip', 0), arg('--limit', 10 ** 9)

d = json.load(open(os.path.join(SRC, stem + '.json'), encoding='utf-8'))
en, ru = d['en'], d['ru_existing']
done = {}
for f in sorted(os.listdir(TR)):
    if f.startswith(stem + '.') and f.endswith('.json'):
        done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))

todo = [(k, v) for k, v in en.items()
        if v.strip() and not has_russian(ru.get(k), v) and k not in done
        and not is_skip(v)
        and mn <= len(v) <= mx]
todo.sort(key=lambda x: len(x[1]))
sel = todo[offset:offset + limit]
for k, v in sel:
    print(f'{k}\t{v}')
print(f'### показано {len(sel)} из {len(todo)} подходящих', file=sys.stderr)
