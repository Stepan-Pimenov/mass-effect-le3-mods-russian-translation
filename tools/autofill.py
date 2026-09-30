"""Подставляет официальный русский текст из ванильной игры там, где мод
переиспользует ванильную строку (совпадение по номеру строки и/или по тексту).
Пишет результат в translation/<stem>.auto.json и печатает статистику покрытия.
"""
import os, sys, json, re, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tlk import read_tlk

ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'source')
TR = os.path.join(ROOT, 'translation')
GAME = r"D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME3\BioGame\CookedPCConsole"


def load(p):
    return {s['id']: s['text'] for s in read_tlk(p, msb_first=False)['strings']}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('\u2019', "'").replace('\u2018', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2013', '-').replace('\u2014', '-').replace('\u2026', '...')
    # \u043f\u0440\u0438\u0442\u044f\u0436\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0444\u043e\u0440\u043c\u044b: \u043f\u0430\u0442\u0447 \u043f\u0438\u0448\u0435\u0442 Garrus', \u0432\u0430\u043d\u0438\u043b\u044c \u2014 Garrus's. \u0421\u0432\u043e\u0434\u0438\u043c \u043a \u043e\u0431\u0449\u0435\u043c\u0443 \u0432\u0438\u0434\u0443.
    s = re.sub(r"'s\b", '', s)
    s = re.sub(r"'(?=\W|$)", '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


ven = load(os.path.join(GAME, 'BIOGame_INT.tlk'))
vru = load(os.path.join(GAME, 'BIOGame_RUS.tlk'))
by_text = {}
for k, v in ven.items():
    r = vru.get(k)
    if r and v.strip():
        by_text.setdefault(norm(v), r)

stems = [a for a in sys.argv[1:]] or [f[:-5] for f in sorted(os.listdir(SRC)) if f.endswith('.json') and not f.startswith('_')]

total_todo = total_hit = 0
for stem in stems:
    p = os.path.join(SRC, stem + '.json')
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    en, ru = d['en'], d['ru_existing']
    todo = {k: v for k, v in en.items()
            if v.strip() and ru.get(k, v) == v and v.strip() not in ('Male', 'Female', 'en-us')}
    auto = {}
    for k, v in todo.items():
        sid = int(k)
        cand = None
        # 1) тот же номер строки в ванили и тот же английский текст
        if sid in ven and vru.get(sid) and norm(ven[sid]) == norm(v):
            cand = vru[sid]
        # 2) совпадение по самому тексту
        if cand is None:
            cand = by_text.get(norm(v))
        if cand and cand.strip() and norm(cand) != norm(v):
            auto[k] = cand
    if todo:
        total_todo += len(todo)
        total_hit += len(auto)
        pct = 100 * len(auto) / len(todo)
        print(f'{stem:<40} {len(auto):>5} / {len(todo):<5} ({pct:5.1f}%)')
    if auto:
        json.dump(auto, open(os.path.join(TR, stem + '.auto.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)

print()
print(f'ИТОГО автоподстановка: {total_hit} из {total_todo} строк '
      f'({100*total_hit/max(total_todo,1):.1f}%)')
