# -*- coding: utf-8 -*-
"""Разрезает очень длинную строку (архив новостей) на отдельные заметки,
чтобы переводить их по частям, и запоминает разделители для обратной сборки.

python tools/split_big.py <stem> <id>
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

stem, sid = sys.argv[1], sys.argv[2]
text = json.load(open(os.path.join(ROOT, 'source', stem + '.json'), encoding='utf-8'))['en'][sid]

# заметки начинаются с даты вида 01/26/2185
parts = re.split(r'(\n{2,})(?=\d{2}/\d{2}/\d{4} - )', text)
pieces, seps = [], []
i = 0
while i < len(parts):
    pieces.append(parts[i])
    if i + 1 < len(parts):
        seps.append(parts[i + 1])
    i += 2

d = os.path.join(ROOT, 'work', stem, sid)
os.makedirs(d, exist_ok=True)
for n, p in enumerate(pieces):
    open(os.path.join(d, f'{n:03d}.en.txt'), 'w', encoding='utf-8').write(p)
json.dump(seps, open(os.path.join(d, 'seps.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'{stem}/{sid}: заметок {len(pieces)}, всего {len(text)} симв')
print('размеры:', [len(p) for p in pieces])
