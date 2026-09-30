# -*- coding: utf-8 -*-
"""Собирает переведённые заметки обратно в одну строку и кладёт её в перевод.

python tools/join_big.py <stem> <id> [<id> ...]
Читает work/<stem>/<id>/ru*.json — словари {номер заметки: перевод}.
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

stem = sys.argv[1]
out = {}
for sid in sys.argv[2:]:
    d = os.path.join(ROOT, 'work', stem, sid)
    seps = json.load(open(os.path.join(d, 'seps.json'), encoding='utf-8'))
    n_en = len([f for f in os.listdir(d) if f.endswith('.en.txt')])
    ru = {}
    for f in sorted(os.listdir(d)):
        if re.fullmatch(r'ru.*\.json', f):
            for k, v in json.load(open(os.path.join(d, f), encoding='utf-8')).items():
                if not k.startswith('_'):
                    ru[int(k)] = v
    missing = [i for i in range(n_en) if i not in ru]
    if missing:
        print(f'{sid}: не хватает заметок {len(missing)} из {n_en}: {missing[:12]}')
        continue
    parts = []
    for i in range(n_en):
        parts.append(ru[i])
        if i < len(seps):
            parts.append(seps[i])
    out[sid] = ''.join(parts)
    print(f'{sid}: собрано {n_en} заметок, {len(out[sid])} симв')
if out:
    out['_comment'] = 'архивы новостей, собраны из отдельных заметок'
    p = os.path.join(ROOT, 'translation', stem + '.news.json')
    if os.path.exists(p):
        old = json.load(open(p, encoding='utf-8'))
        old.update(out)
        out = old
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('записано в', p)
