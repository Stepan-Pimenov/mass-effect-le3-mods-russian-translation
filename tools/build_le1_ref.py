# -*- coding: utf-8 -*-
"""Строит словарь en->ru из ванильных текстов первой части."""
import sys, os, struct, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from le1tlk import load, P
from le1dump import parse_tlk
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tlk_exports(pkg):
    d, names, meta = load(os.path.join(P, pkg))
    ec, eo, ic, io_ = meta
    want = {names.index(x) for x in ('GlobalTlk_tlk', 'GlobalTlk_tlk_M') if x in names}
    res = []
    for i in range(eo, len(d) - 40, 4):
        v, = struct.unpack_from('<i', d, i)
        if v in want:
            cls, = struct.unpack_from('<i', d, i - 12)
            size, off = struct.unpack_from('<2i', d, i + 20)
            if cls < 0 and 0 < off < len(d) and 0 < size and off + size <= len(d):
                res.append((off, size))
        if i > eo + 400000: break
    return d, res

def strings(pkg):
    d, exp = tlk_exports(pkg)
    out = {}
    for off, size in exp:
        out.update(parse_tlk(d[off:off + size]))
    return out

en = strings('Startup_INT.pcc')
ru = strings('Startup_RU.pcc')
print('en', len(en), 'ru', len(ru))
pairs = {}
for i, e in en.items():
    r = ru.get(i)
    if r and e.strip() and r != e:
        pairs[e] = r
print('пар:', len(pairs))
json.dump(pairs, open(os.path.join(BASE, 'reference/le1_en_ru.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for t in ['Therum', 'Edolus', 'Binthu', 'Presrop', 'Artemis Tau', 'Styx Theta', 'Xawin', 'Erebus', 'Amazon']:
    print(t, '->', pairs.get(t, '—'))
