import struct, heapq
from collections import Counter

def build_nodes(strings):
    """strings: list of str (terminator \\0 added automatically). Returns nodes, codes."""
    freq = Counter()
    for s in strings:
        for ch in s:
            freq[ord(ch)] += 1
        freq[0] += 1
    if len(freq) == 1:
        freq[1] = freq.get(1, 0) + 1

    heap = []
    tie = 0
    for c, f in sorted(freq.items()):
        heap.append((f, tie, ('L', c)))
        tie += 1
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, tie, ('N', n1, n2)))
        tie += 1
    root = heap[0][2]
    if root[0] == 'L':
        root = ('N', root, ('L', 0))

    nodes = []

    def add(n):
        idx = len(nodes)
        nodes.append([0, 0])
        for side in (0, 1):
            child = n[1 + side]
            if child[0] == 'L':
                nodes[idx][side] = -(child[1] + 1)
            else:
                nodes[idx][side] = add(child)
        return idx

    add(root)

    codes = {}

    def walk(n, path):
        for side in (0, 1):
            child = n[1 + side]
            if child[0] == 'L':
                codes[child[1]] = path + [side]
            else:
                walk(child, path + [side])

    walk(root, [])
    return nodes, codes


def write_tlk(path, male, female, version=3, minver=2):
    """male/female: list of (id, text) preserving order."""
    entries = list(male) + list(female)
    nodes, codes = build_nodes([t for _, t in entries])

    bits = []
    offsets = []
    for _, text in entries:
        offsets.append(len(bits))
        for ch in text:
            bits.extend(codes[ord(ch)])
        bits.extend(codes[0])

    data = bytearray((len(bits) + 7) // 8)
    for i, b in enumerate(bits):
        if b:
            data[i >> 3] |= (1 << (i & 7))

    out = bytearray()
    out += struct.pack('<4s6i', b'Tlk\x00', version, minver,
                       len(male), len(female), len(nodes), len(data))
    for (sid, _), off in zip(entries, offsets):
        out += struct.pack('<iI', sid, off)
    for l, r in nodes:
        out += struct.pack('<ii', l, r)
    out += data
    open(path, 'wb').write(bytes(out))
    return len(out)
