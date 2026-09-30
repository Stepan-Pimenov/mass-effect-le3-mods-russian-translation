# -*- coding: utf-8 -*-
import sys, os, struct, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcc import decompress
P = r'D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME1\BioGame\CookedPCConsole'

def load(path):
    d, hsize, ver, lic = decompress(path)
    nameCount, nameOffset, exportCount, exportOffset, importCount, importOffset = struct.unpack_from('<6i', d, 25)
    o = nameOffset
    names = []
    for i in range(nameCount):
        n, = struct.unpack_from('<i', d, o); o += 4
        if n < 0:
            s = d[o:o - 2 * n - 2].decode('utf-16-le'); o += -2 * n
        else:
            s = d[o:o + n - 1].decode('latin1'); o += n
        names.append(s)
    return d, names, (exportCount, exportOffset, importCount, importOffset)

if __name__ == '__main__':
    d, names, meta = load(os.path.join(P, 'Startup_RU.pcc'))
    print('имён:', len(names), names[:10])
    print('мета:', meta)
    print('Tlk:', [x for x in names if 'lk' in x][:20])
