# -*- coding: utf-8 -*-
"""Показывает только те абзацы, которых нет в официальном переводе, — их и надо
перевести вручную. Готовые абзацы берутся из ванили, блок данных о планете
переводится механически.

python tools/paradraft.py <stem> [--from N] [--limit N]   — что перевести
python tools/paradraft.py <stem> --build                  — собрать строки

Переводы абзацев кладутся в work/paras/<stem>.json ключами "<номер строки>#<абзац>".
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parafill as P
from common import skip as is_skip

ROOT = os.path.dirname(HERE)
TR = os.path.join(ROOT, 'translation')
WORK = os.path.join(ROOT, 'work', 'paras')
os.makedirs(WORK, exist_ok=True)


def arg(name, default):
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def pending(stem):
    d = json.load(open(os.path.join(ROOT, 'source', stem + '.json'), encoding='utf-8'))
    en, ru = d['en'], d['ru_existing']
    done = set()
    for f in sorted(os.listdir(TR)):
        if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.para.json':
            done |= set(json.load(open(os.path.join(TR, f), encoding='utf-8')))
    ids = [k for k, v in en.items()
           if k not in done and v.strip() and ru.get(k, v) == v and not is_skip(v) and len(v) >= 60]
    return en, sorted(ids, key=int)


def pieces(text):
    """Возвращает список (вид, содержимое): 'sep', 'ready' (уже по-русски), 'todo'."""
    out = []
    for part in re.split(r'(\n\s*\n)', text):
        if re.fullmatch(r'\n\s*\n', part) or not part.strip():
            out.append(('sep', part))
            continue
        b = P.try_block(part)
        if b is not None:
            out.append(('ready', b))
            continue
        r = P.PARA.get(P.norm(part))
        if r is not None:
            out.append(('ready', r))
            continue
        sp = P.split_tail_block(part)
        if sp is not None:
            prose, tail = sp
            rr = P.PARA.get(P.norm(prose))
            out.append(('ready', rr) if rr is not None else ('todo', prose))
            out.append(('sep', '\n'))
            out.append(('ready', tail))
            continue
        out.append(('todo', part))
    return out


def main():
    stem = sys.argv[1]
    en, ids = pending(stem)
    path = os.path.join(WORK, stem + '.json')
    tr = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}

    # одинаковые абзацы встречаются в разных строках — учим их по тексту
    bytext = {}
    for sid in ids:
        for n, (kind, val) in enumerate(pieces(en[sid])):
            if kind == 'todo' and f'{sid}#{n}' in tr:
                bytext.setdefault(P.norm(val), tr[f'{sid}#{n}'])

    if '--build' in sys.argv:
        out, miss = {}, 0
        for sid in ids:
            res, ok = [], True
            for n, (kind, val) in enumerate(pieces(en[sid])):
                if kind == 'todo':
                    key = f'{sid}#{n}'
                    if key in tr:
                        res.append(tr[key])
                    elif P.norm(val) in bytext:
                        res.append(bytext[P.norm(val)])
                    else:
                        ok = False
                        break
                else:
                    res.append(val)
            if ok:
                out[sid] = ''.join(res)
            else:
                miss += 1
        if out:
            out['_comment'] = 'собрано по абзацам: ваниль + переведённые абзацы мода'
            json.dump(out, open(os.path.join(TR, stem + '.para.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
        print(f'{stem}: собрано {len(out) - 1 if out else 0}, не хватает абзацев в {miss} строках')
        return

    start, limit = arg('--from', 0), arg('--limit', 12)
    shown = 0
    for sid in ids[start:]:
        ps = pieces(en[sid])
        todo = [(n, v) for n, (k, v) in enumerate(ps)
                if k == 'todo' and f'{sid}#{n}' not in tr and P.norm(v) not in bytext]
        if not todo:
            continue
        ready = sum(1 for k, _ in ps if k == 'ready')
        print(f'=== {sid}  (готовых абзацев: {ready})')
        for n, v in todo:
            print(f'--- {sid}#{n}')
            print(v)
        shown += 1
        if shown >= limit:
            break


main()
