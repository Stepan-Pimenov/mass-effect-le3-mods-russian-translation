import json, sys, re, difflib
sys.stdout.reconfigure(encoding='utf-8')
ref = json.load(open('reference/vanilla_en_ru.json', encoding='utf-8'))
def norm(s):
    return re.sub(r'\s+',' ', s).strip().lower()
q = norm(sys.argv[1])
qp = q[:100]
scored = []
for k, v in ref.items():
    nk = norm(k)
    if len(nk) < 30: continue
    r = difflib.SequenceMatcher(None, qp, nk[:100]).quick_ratio()
    if r > 0.7:
        scored.append((difflib.SequenceMatcher(None, qp, nk[:100]).ratio(), k, v))
scored.sort(reverse=True, key=lambda x: x[0])
for r, k, v in scored[:3]:
    print(f'=== {r:.3f}  len_en={len(k)}')
    print('EN:', k[:200])
    print('RU:', v[:250])
    print()
