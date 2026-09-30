# -*- coding: utf-8 -*-
"""Достаёт тексты из ванильных пакетов первой части (LE1)."""
import sys, os, struct, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from le1tlk import load, P

def parse_tlk(b):
    hts, = struct.unpack_from('<i', b, 40)
    o = 44
    idmap = {}
    for i in range(hts):
        h, c, idx = struct.unpack_from('<3i', b, o); o += 12
        if c: idmap[idx] = h
    n, = struct.unpack_from('<i', b, o); o += 4
    nodes = []
    for i in range(n):
        if b[o] == 0:
            l, r = struct.unpack_from('<2H', b, o + 1); o += 5; nodes.append((0, l, r))
        else:
            c, = struct.unpack_from('<H', b, o + 1); o += 3; nodes.append((1, c, 0))
    count, = struct.unpack_from('<i', b, o); o += 4
    strings = {}
    for i in range(count):
        nchar, clen = struct.unpack_from('<2i', b, o)
        blk = b[o + 8:o + 8 + clen]
        o += 8 + clen
        out = []
        node = 0
        for bi in range(clen * 8):
            bit = (blk[bi >> 3] >> (bi & 7)) & 1
            f, l, r = nodes[node]
            nxt = l if bit else r
            if nodes[nxt][0]:
                ch = nodes[nxt][1]
                node = 0
                if ch == 0: break
                out.append(chr(ch))
            else:
                node = nxt
        strings[idmap.get(i, -i)] = ''.join(out)
    return strings

def get(pkg, off, size):
    d, names, meta = load(os.path.join(P, pkg))
    return parse_tlk(d[off:off + size])

if __name__ == '__main__':
    s = get('Startup_RU.pcc', 135441, 994812)
    print('строк:', len(s))
    import itertools
    for k, v in itertools.islice(s.items(), 6):
        print(k, repr(v[:70]))
