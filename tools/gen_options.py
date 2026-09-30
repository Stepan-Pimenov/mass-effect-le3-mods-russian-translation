# -*- coding: utf-8 -*-
"""Собирает перевод описаний настроек вида
«... This option requires you to save and reload the game. This option is currently enabled.»
из словаря смысловых частей tools/cores.json."""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip, has_russian
ROOT = os.path.dirname(HERE)
CORES = json.load(open(os.path.join(HERE, 'cores.json'), encoding='utf-8'))
RELOAD = ' Потребуется сохраниться и перезагрузить игру.'
STATE = {'enabled': ' Сейчас эта настройка включена.',
         'disabled': ' Сейчас эта настройка выключена.'}


def gen(en):
    m = re.match(r'^(.*?)\s*This option is currently (enabled|disabled)\s*\.?\s*$', en, re.S)
    if not m:
        return None
    body, state = m.group(1).strip(), m.group(2)
    reload_needed = bool(re.search(r'This option requires you to save and reload the game', body)) \
        or bool(re.search(r'This outfit requires you to save and reload the game', body))
    core = re.sub(r'\s*Th(is|e) (option|outfit) requires you to save and reload the game\.?', '', body)
    core = re.sub(r'\s+', ' ', core).strip().rstrip(',').rstrip('.')
    ru = CORES.get(core)
    if ru is None:
        return None
    out = ru.rstrip('.') + '.'
    if reload_needed:
        out += RELOAD
    return out + STATE[state]


def main():
    for stem in sys.argv[1:]:
        p = os.path.join(ROOT, 'source', stem + '.json')
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        en, ru = d['en'], d['ru_existing']
        TR = os.path.join(ROOT, 'translation')
        done = {}
        for f in sorted(os.listdir(TR)):
            if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.opts.json':
                done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))
        out, miss = {}, set()
        for k, v in en.items():
            if k in done or not v.strip() or has_russian(ru.get(k), v) or is_skip(v):
                continue
            r = gen(v)
            if r:
                out[k] = r
            elif 'This option is currently' in v:
                miss.add(v)
        if out:
            out['_comment'] = 'описания настроек, собраны по шаблону'
            json.dump(out, open(os.path.join(TR, stem + '.opts.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
        print(f'{stem}: {len(out) - 1 if out else 0}')
        for v in sorted(miss):
            print('   нет части:', v[:120])


main()
