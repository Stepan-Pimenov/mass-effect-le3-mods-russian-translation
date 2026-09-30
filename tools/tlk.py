import struct, sys, json, io

def read_tlk(path, msb_first=True):
    d = open(path, 'rb').read()
    magic, ver, minver, n1, n2, nodecount, datalen = struct.unpack_from('<4s6i', d, 0)
    assert magic == b'Tlk\x00', magic
    off = 28
    entries = []
    for i in range(n1 + n2):
        sid, boff = struct.unpack_from('<iI', d, off); off += 8
        entries.append((sid, boff))
    nodes = []
    for i in range(nodecount):
        l, r = struct.unpack_from('<ii', d, off); off += 8
        nodes.append((l, r))
    data = d[off:off + datalen]

    def bit(n):
        byte = data[n >> 3]
        if msb_first:
            return (byte >> (7 - (n & 7))) & 1
        return (byte >> (n & 7)) & 1

    total_bits = datalen * 8

    def decode(start):
        out = []
        node = 0
        p = start
        while p < total_bits:
            b = bit(p); p += 1
            nxt = nodes[node][1] if b else nodes[node][0]
            if nxt < 0:
                ch = -nxt - 1
                if ch == 0:
                    return ''.join(out)
                out.append(chr(ch))
                node = 0
            else:
                node = nxt
        return ''.join(out)

    res = []
    for sid, boff in entries:
        res.append({'id': sid, 'text': decode(boff)})
    return {'version': ver, 'minver': minver, 'male': n1, 'female': n2, 'strings': res}

if __name__ == '__main__':
    path = sys.argv[1]
    for msb in (True, False):
        try:
            r = read_tlk(path, msb)
            sample = ' | '.join(s['text'][:60] for s in r['strings'][:6])
            print(f'--- msb_first={msb} ---')
            print(sample)
        except Exception as e:
            print(f'--- msb_first={msb} ОШИБКА: {e}')
