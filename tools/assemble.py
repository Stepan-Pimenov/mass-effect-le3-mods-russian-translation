# -*- coding: utf-8 -*-
"""Собирает переведённые куски обратно в translation/<stem>.json.

    python tools/assemble.py <stem>

Читает work/<stem>/ru_*.json — словари {номер строки: перевод} — и вливает их
в основной файл перевода. Существующие строки перезаписываются, порядок
ключей восстанавливается. Сообщает о номерах, которых нет в моде, и о том,
сколько строк осталось непереведёнными.
"""
import os, sys, io, json, re, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    stem = sys.argv[1]
    work = os.path.join(ROOT, 'work', stem)
    if not os.path.isdir(work):
        print('нет папки %s — сначала запустить prep.py' % os.path.relpath(work, ROOT))
        return 1

    en = json.load(io.open(os.path.join(ROOT, 'source', stem + '.json'), encoding='utf-8'))['en']

    new = collections.OrderedDict()
    files = sorted(f for f in os.listdir(work) if re.fullmatch(r'ru.*\.json', f))
    for f in files:
        for k, v in json.load(io.open(os.path.join(work, f), encoding='utf-8')).items():
            if not k.startswith('_') and isinstance(v, str):
                new[k] = v
    if not files:
        print('в %s нет файлов ru_*.json' % os.path.relpath(work, ROOT))
        return 1

    unknown = [k for k in new if k not in en]
    for k in unknown:
        del new[k]

    tp = os.path.join(ROOT, 'translation', stem + '.json')
    cur = collections.OrderedDict()
    if os.path.exists(tp):
        cur = json.load(io.open(tp, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    added = sum(1 for k in new if k not in cur)
    cur.update(new)
    cur = collections.OrderedDict((k, cur[k]) for k in sorted(cur, key=lambda x: (len(x), x)))
    io.open(tp, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(cur, ensure_ascii=False, indent=1) + '\n')

    todo = os.path.join(work, 'todo.json')
    left = 0
    if os.path.exists(todo):
        left = sum(1 for k in json.load(io.open(todo, encoding='utf-8')) if k not in cur)

    print('%s: файлов с переводом %d, строк внесено %d (новых %d), всего в переводе %d'
          % (stem, len(files), len(new), added, len(cur)))
    if unknown:
        print('пропущено — таких строк в моде нет: %s' % ', '.join(unknown[:10]))
    print('осталось перевести: %d' % left)
    print('дальше: python tools/check.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
