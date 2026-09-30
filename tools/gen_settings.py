# -*- coding: utf-8 -*-
"""Генерирует перевод однотипных строк настроек модов: «подпись: ВКЛ/ВЫКЛ»,
названия нарядов и причёсок, экраны внешности персонажей."""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip, has_russian
ROOT = os.path.dirname(HERE)

LABELS = json.load(open(os.path.join(HERE, 'labels.json'), encoding='utf-8'))
WEAPONS = json.load(open(os.path.join(HERE, 'weapons.json'), encoding='utf-8'))

NAMES = {
 'Jack': 'Джек', 'Aria': 'Арии', 'Brynn': 'Бринн', 'Ken': 'Кена', 'Gabby': 'Гэбби',
 'Sarah': 'Сары', 'Jenna': 'Дженны', 'Vosque': 'Воска', 'Balak': 'Балака',
 'Conrad': 'Конрада', 'Thane': 'Тейна', 'Liara': 'Лиары', 'Jacob': 'Джейкоба',
 'Kelly': 'Келли', 'Zaeed': 'Заида', 'Joker': 'Джокера', 'Mordin': 'Мордина',
 'Victus': 'Виктуса', 'Grunt': 'Грюнта', 'Udina': 'Удины', 'James': 'Джеймса',
 'Adams': 'Адамса', 'Narl': 'Нарла', 'Sayn': 'Сейна', 'Wreav': 'Рива',
 'Miranda': 'Миранды', 'Garrus': 'Гарруса', 'Tali': 'Тали', 'Javik': 'Явика',
 'Cortez': 'Кортеза', 'Traynor': 'Трейнор', 'Bray': 'Брэя', 'Ereba': 'Эребы',
 'Samara': 'Самары', 'Ashley': 'Эшли', 'Kaidan': 'Кайдена', 'Samantha': 'Саманты',
 'Steve': 'Стива', 'EDI': 'СУЗИ', 'Wrex': 'Рекса', 'Ghorek': 'Горека',
 'Aethyta': 'Этиты', 'Oriana': 'Орианы', 'Kolyat': 'Колята', 'Diana': 'Дианы',
 'Allers': 'Аллерс', 'Chakwas': 'Чаквас', 'Nyreen': 'Нирин', 'Kasumi': 'Касуми',
 'Brooks': 'Брукс', 'Anderson': 'Андерсона', 'Legion': 'Легиона',
}
ONOFF = {'ENABLED': 'ВКЛ', 'DISABLED': 'ВЫКЛ'}
EGMNOTE = ('. Если стоит Expanded Galaxy Mod, убедись, что в его настройках '
           'наряд {who} выставлен по умолчанию.')


def label(en):
    if en in LABELS:
        return LABELS[en]
    m = re.fullmatch(r'(\w+) New Outfits?', en)
    if m and m.group(1) in NAMES:
        return f'Новые наряды {NAMES[m.group(1)]}'
    m = re.fullmatch(r'(\w+) New Hairstyles?', en)
    if m and m.group(1) in NAMES:
        return f'Новая причёска {NAMES[m.group(1)]}'
    m = re.fullmatch(r'(\w+) Appearance', en)
    if m and m.group(1) in NAMES:
        return f'Внешность {NAMES[m.group(1)]}'
    return None


def gen(en):
    en = en.strip()
    m = re.fullmatch(r'(.+): (ENABLED|DISABLED)', en)
    if m:
        lab = label(m.group(1))
        if lab:
            return f'{lab}: {ONOFF[m.group(2)]}'
    lab = label(en)
    if lab:
        return lab
    if en in WEAPONS:
        return WEAPONS[en]
    m = re.fullmatch(r'(.+) (I{1,3}|IV|VI{0,3}|IX|X|V)', en)
    if m and m.group(1) in WEAPONS:
        return f'{WEAPONS[m.group(1)]} {m.group(2)}'
    m = re.fullmatch(r"Change (\w+)'?s? Appearance\.(?: If using Expanded Galaxy Mod.*)?", en)
    if m and m.group(1) in NAMES:
        who = NAMES[m.group(1)]
        if 'Expanded Galaxy Mod' in en:
            return f'Изменить внешность {who}' + EGMNOTE.format(who=who)
        return f'Изменить внешность {who}.'
    m = re.fullmatch(r"Change (\w+)'?s? [Aa]pp?e?a?rance\.?", en)
    if m and m.group(1) in NAMES:
        return f'Изменить внешность {NAMES[m.group(1)]}.'
    m = re.fullmatch(r'(\w+)(?:\'s)? Appearance Settings', en)
    if m and m.group(1) in NAMES:
        return f'Внешность {NAMES[m.group(1)]}'
    m = re.fullmatch(r'(\w+)(?:\'s)? Hair Settings', en)
    if m and m.group(1) in NAMES:
        return f'Причёска {NAMES[m.group(1)]}'
    m = re.fullmatch(r'(\w+) New Outfits?', en)
    if m and m.group(1) in NAMES:
        return f'Новые наряды {NAMES[m.group(1)]}'
    m = re.fullmatch(r'Outfit (\d+)', en)
    if m: return f'Наряд {m.group(1)}'
    m = re.fullmatch(r'Hair (\d+)', en)
    if m: return f'Волосы {m.group(1)}'
    m = re.fullmatch(r'Part (\d+)', en)
    if m: return f'Часть {m.group(1)}'
    m = re.fullmatch(r'Invite (\w+)', en)
    if m and m.group(1) in NAMES:
        return f'Пригласить {NAMES[m.group(1)]}'
    return None


def main():
    for stem in sys.argv[1:]:
        p = os.path.join(ROOT, 'source', stem + '.json')
        if not os.path.exists(p): continue
        d = json.load(open(p, encoding='utf-8'))
        en, ru = d['en'], d['ru_existing']
        TR = os.path.join(ROOT, 'translation')
        done = {}
        for f in sorted(os.listdir(TR)):
            if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.gen.json':
                done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))
        out, miss = {}, set()
        for k, v in en.items():
            if k in done or not v.strip() or has_russian(ru.get(k), v) or is_skip(v): continue
            r = gen(v)
            if r: out[k] = r
            elif re.search(r'(ENABLED|DISABLED)$', v) or 'Appearance' in v or 'New Outfit' in v:
                miss.add(v)
        if out:
            out['_comment'] = 'однотипные строки настроек, сгенерированы по шаблону'
            json.dump(out, open(os.path.join(TR, stem + '.gen.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
        print(f'{stem}: {len(out) - 1 if out else 0}')
        for v in sorted(miss): print('   нет шаблона:', v)


main()
