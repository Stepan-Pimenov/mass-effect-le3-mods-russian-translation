"""Собирает русские .tlk из source/*.json + translation/*.json и раскладывает в build/.
Запуск:  python build.py [stem ...]   (без аргументов — все, для которых есть перевод)
Установка в игру:  python build.py --install [stem ...]
"""
import os, sys, json, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tlk import read_tlk
from tlkwrite import write_tlk

ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'source')
TR = os.path.join(ROOT, 'translation')
BUILD = os.path.join(ROOT, 'build')
BACKUP = os.path.join(ROOT, 'backup_original')
# Путь к папке DLC третьей части. Можно переопределить переменной окружения:
#   ME3LE_DLC  — сразу папка ...\Game\ME3\BioGame\DLC
#   ME3LE_PATH — корень игры ...\Mass Effect Legendary Edition
DLC = os.environ.get('ME3LE_DLC')
if not DLC and os.environ.get('ME3LE_PATH'):
    DLC = os.path.join(os.environ['ME3LE_PATH'], 'Game', 'ME3', 'BioGame', 'DLC')
if not DLC:
    DLC = r"D:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME3\BioGame\DLC"

CYR = re.compile(r'[А-яЁё]')


def has_russian(existing, english):
    """Свой перевод мода берём только если это действительно русский текст:
    некоторые моды держат в RUS.tlk устаревшую английскую версию строки."""
    return bool(existing) and existing != english and bool(CYR.search(existing))


os.makedirs(BUILD, exist_ok=True)
os.makedirs(BACKUP, exist_ok=True)

args = [a for a in sys.argv[1:] if not a.startswith('--')]
install = '--install' in sys.argv

def has_translation(stem):
    for f in os.listdir(TR):
        if f.startswith(stem + '.') and f.endswith('.json'):
            return True
    return os.path.exists(os.path.join(TR, stem + '.json'))


stems = args or [f[:-5] for f in sorted(os.listdir(SRC))
                 if f.endswith('.json') and has_translation(f[:-5])]

for stem in stems:
    sp = os.path.join(SRC, stem + '.json')
    tp = os.path.join(TR, stem + '.json')
    if not os.path.exists(sp) or not has_translation(stem):
        print(f'{stem}: пропуск (нет source или перевода)')
        continue
    src = json.load(open(sp, encoding='utf-8'))
    tr = {}
    # сначала автоподстановка, потом все ручные части, потом основной файл
    for f in sorted(os.listdir(TR)):
        if f.startswith(stem + '.') and f.endswith('.json') and f != stem + '.json':
            tr.update({k: v for k, v in json.load(open(os.path.join(TR, f), encoding='utf-8')).items()
                       if not k.startswith('_')})
    if os.path.exists(tp):
        tr.update({k: v for k, v in json.load(open(tp, encoding='utf-8')).items() if not k.startswith('_')})

    game_int = os.path.join(DLC, src['mod'], 'CookedPCConsole', stem + '_INT.tlk')
    r = read_tlk(game_int, msb_first=False)
    ru_existing = src.get('ru_existing', {})

    out = []
    used = 0
    for s in r['strings']:
        sid = s['id']
        key = str(sid)
        if key in tr:
            text = tr[key]; used += 1
        elif has_russian(ru_existing.get(key), s['text']):
            text = ru_existing[key]
        elif has_russian(ru_existing.get(sid), s['text']):
            text = ru_existing[sid]
        else:
            text = s['text']
        out.append((sid, text))

    male = out[:r['male']]
    female = out[r['male']:]
    dst = os.path.join(BUILD, stem + '_RUS.tlk')
    size = write_tlk(dst, male, female, r['version'], r['minver'])
    print(f'{stem}: применено {used} строк из {len(tr)}, файл {size} байт')

    if install:
        target = os.path.join(DLC, src['mod'], 'CookedPCConsole', stem + '_RUS.tlk')
        bak = os.path.join(BACKUP, stem + '_RUS.tlk')
        if os.path.exists(target) and not os.path.exists(bak):
            shutil.copy(target, bak)
        shutil.copy(dst, target)
        print(f'   установлено в игру: {target}')
