# -*- coding: utf-8 -*-
"""Готовит мод к переводу: собирает всё, что ещё не переведено, в текстовый файл.

    python tools/prep.py <stem> [размер куска]

Пишет в work/<stem>/:
    prose_en.txt   строки для перевода, по кускам, каждая со своим номером
    todo.json      те же строки списком, чтобы собрать обратно

Строки, которые переводить не надо (заглушки, титры, коды), отсеиваются по
common.skip() и по разделу «не_переводим» в tools/glossary.json. Строки, для
которых у самого мода есть настоящий русский текст, тоже пропускаются.
"""
import os, sys, io, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common

CHUNK = 60


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    stem = sys.argv[1]
    chunk = int(sys.argv[2]) if len(sys.argv) > 2 else CHUNK

    src = json.load(io.open(os.path.join(ROOT, 'source', stem + '.json'), encoding='utf-8'))
    en, ex = src['en'], src.get('ru_existing', {})

    tp = os.path.join(ROOT, 'translation', stem + '.json')
    done = set()
    if os.path.exists(tp):
        done = {k for k in json.load(io.open(tp, encoding='utf-8')) if not k.startswith('_')}

    gl = json.load(io.open(os.path.join(HERE, 'glossary.json'), encoding='utf-8'))
    skip_ids = set(gl.get('не_переводим', {}).get(stem, []))

    todo = collections.OrderedDict()
    for sid in sorted(en, key=int):
        text = en[sid]
        if sid in done or sid in skip_ids or common.skip(text):
            continue
        if common.has_russian(ex.get(sid), text):
            continue
        todo[sid] = text

    out = os.path.join(ROOT, 'work', stem)
    os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, 'todo.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(todo, ensure_ascii=False, indent=1) + '\n')

    ids = list(todo)
    with io.open(os.path.join(out, 'prose_en.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for i in range(0, len(ids), chunk):
            f.write('\n===== кусок %02d =====\n\n' % (i // chunk + 1))
            for sid in ids[i:i + chunk]:
                f.write('### %s\n%s\n\n' % (sid, todo[sid]))

    chars = sum(len(v) for v in todo.values())
    print('%s: к переводу %d строк, %d знаков, кусков %d'
          % (stem, len(todo), chars, (len(ids) + chunk - 1) // chunk))
    print('файлы: %s' % os.path.relpath(out, ROOT))
    print('переводы складывать туда же файлами ru_01.json, ru_02.json … вида {"номер": "перевод"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
