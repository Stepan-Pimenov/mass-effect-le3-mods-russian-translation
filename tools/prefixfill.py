# -*- coding: utf-8 -*-
"""Многие моды берут ванильную статью кодекса и обрезают её (например, выкидывают
блок данных о планете). Скрипт находит такую ванильную статью, у которой начало
совпадает с текстом мода, и берёт соответствующую часть официального перевода."""
import os, sys, json, re, difflib, argparse
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import skip as is_skip
ROOT = os.path.dirname(HERE)

ref = {}
for name in ('vanilla_en_ru.json', 'dlc_en_ru.json', 'dlc2_en_ru.json',
             'le1_en_ru.json', 'le2_en_ru.json'):
    p = os.path.join(ROOT, 'reference', name)
    if os.path.exists(p):
        for k, v in json.load(open(p, encoding='utf-8')).items():
            ref.setdefault(k, v)

DATA = re.compile(r'(Расстояние до звезды|Период обращения|Продолжительность суток|'
                  r'Атмосферное давление|Температура поверхности|Сила тяжести|'
                  r'Основание колонии|Радиус:|Население:|Столица:)')


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


WORD = re.compile(r'[a-zA-Z]{5,}')
index = defaultdict(list)
refn = {}
for k in ref:
    n = norm(k)
    refn[k] = n
    for w in set(WORD.findall(n.lower())):
        index[w].append(k)


def sentences(t):
    parts = re.split(r'(?<=[.!?])\s+', t.strip())
    return [p for p in parts if p]


def cut_ru(ru, frac, nsent):
    """Обрезает русский текст: сначала по блоку данных, иначе по числу предложений."""
    target = frac * len(ru)
    s = sentences(ru)
    # 1) по числу предложений — самый надёжный способ
    if 0 < nsent <= len(s):
        c = ' '.join(s[:nsent])
        if 0.55 * target <= len(c) <= 1.9 * target:
            return c
    # 2) по блоку данных о планете
    m = DATA.search(ru)
    if m:
        c = ru[:m.start()].rstrip()
        if c.strip() and 0.5 * target <= len(c) <= 2.0 * target:
            return c
    # 3) целиком, если длина и так сопоставима
    if 0.7 * target <= len(ru) <= 1.6 * target:
        return ru
    return None


def find(q, minratio):
    qn = norm(q)
    words = set(WORD.findall(qn.lower()))
    if not words:
        return None
    cnt = defaultdict(float)
    for w in words:
        lst = index.get(w)
        if not lst or len(lst) > 8000:
            continue
        wt = 1.0 / len(lst)
        for k in lst:
            cnt[k] += wt
    if not cnt:
        return None
    best = (0, None)
    for k, _ in sorted(cnt.items(), key=lambda x: -x[1])[:60]:
        rn = refn[k]
        if len(rn) < len(qn) * 1.15:
            continue
        r = difflib.SequenceMatcher(None, qn, rn[:len(qn)]).ratio()
        if r > best[0]:
            best = (r, k)
    if best[0] >= minratio:
        return best
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--min', type=float, default=0.93)
    ap.add_argument('--minlen', type=int, default=120)
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    TR = os.path.join(ROOT, 'translation')
    for stem in a.files:
        p = os.path.join(ROOT, 'source', stem + '.json')
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        ens, rux = d['en'], d['ru_existing']
        done = {}
        for f in sorted(os.listdir(TR)):
            if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.pref.json':
                done.update(json.load(open(os.path.join(TR, f), encoding='utf-8')))
        out = {}
        for sid, en in ens.items():
            if sid in done or not en.strip():
                continue
            if rux.get(sid, en) != en or is_skip(en) or len(en) < a.minlen:
                continue
            res = find(en, a.min)
            if not res:
                continue
            ru_full = ref[res[1]]
            frac = len(norm(en)) / max(len(refn[res[1]]), 1)
            cut = cut_ru(ru_full, frac, len(sentences(en)))
            if cut:
                out[sid] = cut
                if a.report:
                    print(f'-- {sid} {res[0]:.3f} {en[:60]!r}')
        if out:
            out['_comment'] = 'обрезанные ванильные статьи кодекса, официальный текст'
            json.dump(out, open(os.path.join(TR, stem + '.pref.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            print(f'{stem}: подставлено {len(out) - 1}')
        else:
            print(f'{stem}: нет совпадений')


main()
