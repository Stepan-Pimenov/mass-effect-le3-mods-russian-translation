# -*- coding: utf-8 -*-
"""Минимальный читатель пакетов Legendary Edition (.pcc) — только чтобы достать тексты."""
import struct, os, sys, ctypes
sys.stdout.reconfigure(encoding='utf-8')
MAGIC = 0x9E2A83C1
_ood = None
def oodle():
    global _ood
    if _ood is None:
        dll = r'D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME1\Binaries\Win64\oo2core_8_win64.dll'
        _ood = ctypes.WinDLL(dll)
        _ood.OodleLZ_Decompress.restype = ctypes.c_longlong
    return _ood

def ood_decompress(src, outsize):
    o = oodle()
    dst = ctypes.create_string_buffer(outsize)
    r = o.OodleLZ_Decompress(ctypes.c_char_p(src), ctypes.c_longlong(len(src)),
                             dst, ctypes.c_longlong(outsize),
                             0, 0, 0, None, 0, None, None, None, 0, 3)
    if r != outsize:
        raise RuntimeError(f'oodle вернул {r}, ожидалось {outsize}')
    return dst.raw[:outsize]

def find_chunk_table(d, hsize):
    for o in range(28, min(hsize, 2000)):
        cf, n = struct.unpack_from('<Ii', d, o)
        if cf not in (0x100, 0x200, 0x400, 0x800, 1, 2, 4, 8): continue
        if not (0 < n < 500): continue
        end = o + 8 + 16 * n
        if end > hsize: continue
        ok = True
        prev = -1
        for i in range(n):
            uo, us, co, cs = struct.unpack_from('<4i', d, o + 8 + 16 * i)
            if not (0 <= uo and 0 < us and 0 < co < len(d) and 0 < cs and co + cs <= len(d)):
                ok = False; break
            if uo <= prev: ok = False; break
            prev = uo
            if struct.unpack_from('<I', d, co)[0] != MAGIC: ok = False; break
        if ok:
            return o, cf, n
    return None

def decompress(path):
    d = open(path, 'rb').read()
    tag, ver, lic, hsize = struct.unpack_from('<IhhI', d, 0)
    assert tag == MAGIC
    r = find_chunk_table(d, hsize)
    if r is None:
        return d, hsize, ver, lic
    o, cf, n = r
    first = struct.unpack_from('<i', d, o + 8)[0]
    out = bytearray(d[:first])
    for i in range(n):
        uo, us, co, cs = struct.unpack_from('<4i', d, o + 8 + 16 * i)
        m, blocksize, csize, usize = struct.unpack_from('<4I', d, co)
        nb = (usize + blocksize - 1) // blocksize
        p = co + 16
        blocks = []
        for b in range(nb):
            bc, bu = struct.unpack_from('<2I', d, p); p += 8
            blocks.append((bc, bu))
        data = bytearray()
        for bc, bu in blocks:
            data += ood_decompress(d[p:p + bc], bu)
            p += bc
        if len(out) < uo: out += b'\x00' * (uo - len(out))
        out[uo:uo + us] = data
    return bytes(out), hsize, ver, lic

if __name__ == '__main__':
    p = sys.argv[1]
    d = open(p, 'rb').read()
    tag, ver, lic, hsize = struct.unpack_from('<IhhI', d, 0)
    print('ver', ver, lic, 'hsize', hsize, 'size', len(d))
    print('chunk table:', find_chunk_table(d, hsize))
