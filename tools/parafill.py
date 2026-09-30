# -*- coding: utf-8 -*-
"""Собирает перевод по абзацам: моды часто берут ванильную статью кодекса и
добавляют к ней свои абзацы. Официальный перевод раскладывается на абзацы, и те
абзацы мода, что совпали, берутся из него. Блок данных о планете переводится
механически. Если хоть один абзац не опознан, строка пропускается.

python tools/parafill.py <stem> [...] [--report]
"""
import os, sys, json, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip
ROOT = os.path.dirname(HERE)

REFS = ['vanilla_en_ru.json', 'dlc_en_ru.json', 'dlc2_en_ru.json',
        'le1_en_ru.json', 'le2_en_ru.json']


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('…', '...')
    s = re.sub(r"'s\b", '', s)
    s = re.sub(r"'(?=\W|$)", '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def paras(t):
    return [p for p in re.split(r'\n\s*\n', t) if p.strip()]


PARA = {}
for name in REFS:
    p = os.path.join(ROOT, 'reference', name)
    if not os.path.exists(p):
        continue
    for en, ru in json.load(open(p, encoding='utf-8')).items():
        pe, pr = paras(en), paras(ru)
        if len(pe) == len(pr):
            for a, b in zip(pe, pr):
                if len(norm(a)) > 40:
                    PARA.setdefault(norm(a), b)

NUMF = r'-?\d[\d,.]*'
FIELDS = [
    (r'^Orbital Distance:\s*(?:\(barycenter\)\s*)?(' + NUMF + r')\s*AU$', 'Высота орбиты: {0} АЕ'),
    (r'^Orbital Period:\s*(' + NUMF + r')\s*Earth Years?$', 'Период обращения (в земных годах): {0}'),
    (r'^Keplerian Ratio:\s*(' + NUMF + r')$', 'Кеплеровское отношение: {0}'),
    (r'^Radius:\s*(' + NUMF + r')\s*km$', 'Радиус: {0} км'),
    (r'^Day Length:\s*(' + NUMF + r')\s*Earth Hours?$', 'Продолжительность суток: {0} земных часов'),
    (r'^Atmospheric Pressure:\s*(' + NUMF + r')\s*Earth Atmospheres?$',
     'Атмосферное давление: {0} земных атмосфер'),
    (r'^Atmospheric Pressure:\s*Trace$', 'Атмосферное давление: следы'),
    (r'^Surface Temperature:\s*(' + NUMF + r')\s*Celsius$', 'Температура на поверхности: {0} °C'),
    (r'^(?:Surface )?Gravity:\s*(' + NUMF + r')\s*G?$', 'Сила тяжести: {0} G'),
    (r'^Mass:\s*(' + NUMF + r')\s*Earth Masses$', 'Масса: {0} земных масс'),
    (r'^Satellites:\s*(.+)$', 'Спутники: {0}'),
    (r'^Capital:\s*(.+)$', 'Столица: {0}'),
    (r'^Orbital Distance:\s*(' + NUMF + r')\s*km$', 'Высота орбиты: {0} км'),
    (r'^Day Length:\s*(' + NUMF + r')\s*Earth Years?$', 'Продолжительность суток: {0} земных лет'),
    (r'^Atmospheric Pressure:\s*None$', 'Атмосферное давление: нет'),
    (r'^Surface Temperature:\s*Unknown$', 'Температура на поверхности: неизвестно'),
    (r'^Surface Gravity:\s*Unknown$', 'Сила тяжести: неизвестно'),
    (r'^Colony Founded:\s*(.+)$', 'Основание колонии: {0}'),
    (r'^Population:\s*(.+)$', 'Население: {0}'),
]

HAZ = {'Heat': 'Опасность высокой температуры', 'Cold': 'Опасность низкой температуры',
       'Toxic': 'Опасность токсичных веществ', 'Pressure': 'Опасность атмосферного давления',
       'Radiation': 'Опасность излучения'}


def numru(s):
    s = s.strip()
    if re.fullmatch(r'-?\d{1,3}(,\d{3})+(\.\d+)?', s):
        s = s.replace(',', ' ')
    s = s.replace('.', ',')
    return s


def block_line(line):
    s = line.strip()
    if not s:
        return None
    m = re.match(r'^WARNING: Level (\d) (\w+) Hazard$', s)
    if m and m.group(2) in HAZ:
        return f'ВНИМАНИЕ: {HAZ[m.group(2)]} {m.group(1)} уровня'
    for pat, out in FIELDS:
        m = re.match(pat, s, re.I)
        if m:
            g = [numru(x) if re.fullmatch(NUMF, x.strip()) else x for x in m.groups()]
            return out.format(*g) if g else out
    return None


def try_block(par):
    lines = par.split('\n')
    out = []
    for ln in lines:
        r = block_line(ln)
        if r is None:
            return None
        out.append(r)
    return '\n'.join(out)


def split_tail_block(par):
    """Если в конце абзаца идут строки блока данных, отделяет их: (проза, блок)."""
    lines = par.split('\n')
    i = len(lines)
    while i > 0 and block_line(lines[i - 1]) is not None:
        i -= 1
    if i == 0 or i == len(lines):
        return None
    tail = try_block('\n'.join(lines[i:]))
    if tail is None:
        return None
    return '\n'.join(lines[:i]), tail


def translate(t):
    res = []
    for par in re.split(r'(\n\s*\n)', t):
        if re.fullmatch(r'\n\s*\n', par):
            res.append(par)
            continue
        if not par.strip():
            res.append(par)
            continue
        b = try_block(par)
        if b is not None:
            res.append(b)
            continue
        r = PARA.get(norm(par))
        if r is None:
            return None
        res.append(r)
    return ''.join(res)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    report = '--report' in sys.argv
    TR = os.path.join(ROOT, 'translation')
    for stem in args:
        p = os.path.join(ROOT, 'source', stem + '.json')
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        en, ru = d['en'], d['ru_existing']
        done = set()
        for f in sorted(os.listdir(TR)):
            if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.para.json':
                done |= set(json.load(open(os.path.join(TR, f), encoding='utf-8')))
        out = {}
        for k, v in en.items():
            if k in done or not v.strip() or ru.get(k, v) != v or is_skip(v):
                continue
            if len(v) < 60:
                continue
            r = translate(v)
            if r:
                out[k] = r
                if report:
                    print('--', k, repr(v[:60]))
        if out:
            out['_comment'] = 'собрано по абзацам из официального перевода'
            json.dump(out, open(os.path.join(TR, stem + '.para.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            print(f'{stem}: подставлено {len(out) - 1}')
        else:
            print(f'{stem}: нет совпадений')


if __name__ == '__main__':
    main()
