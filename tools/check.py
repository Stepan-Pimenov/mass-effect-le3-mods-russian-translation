# -*- coding: utf-8 -*-
"""Ревизор перевода: ищет в translation/ всё, что похоже на ошибку.

    python tools/check.py            — проверить перевод, отчёт в work/check.txt
    python tools/check.py --build    — ещё и сверить сборку: build == dist, размеры в README
    python tools/check.py --quiet    — только итог

Правила берутся из tools/glossary.json, его же и правим, когда находим новый термин.
"""
import os, sys, io, re, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common

TR = os.path.join(ROOT, 'translation')
SRC = os.path.join(ROOT, 'source')
REPORT = os.path.join(ROOT, 'work', 'check.txt')

CYR = re.compile('[\u0410-\u044f\u0401\u0451]')
MIXED = re.compile('[\u0410-\u044f\u0401\u0451][a-zA-Z]|[a-zA-Z][\u0410-\u044f\u0401\u0451]')
WORD = re.compile('[a-zA-Z\u0400-\u04ff]+')
TOKEN = re.compile(r'\{[^{}]{1,40}\}|<[A-Za-z/][^<>]{0,60}>|%[sdif]|\[[A-Z0-9_ ]{2,40}\]')
BRACKET = re.compile(r'\[[A-Z0-9_ ]{2,40}\]')
DUPWORD = re.compile('\\b([\u0410-\u044f\u0401\u0451]{3,})\\s+\\1\\b', re.IGNORECASE)
LABEL = re.compile('(?m)^([\u0410-\u042f][^:\n]{3,42}): ?([^\n]{0,40})$')


def jl(p):
    return json.load(io.open(p, encoding='utf-8'))


def load_glossary():
    return jl(os.path.join(HERE, 'glossary.json'))


def load_translation():
    """{stem: {id: (текст, файл)}} плюс список ключей, переведённых дважды по-разному."""
    data = collections.defaultdict(dict)
    conflicts = []
    for p in sorted(glob.glob(os.path.join(TR, '*.json'))):
        name = os.path.basename(p)
        stem = name.split('.')[0]
        for k, v in jl(p).items():
            if k.startswith('_') or not isinstance(v, str):
                continue
            old = data[stem].get(k)
            if old and old[0] != v:
                conflicts.append((stem, k, old[1], old[0], name, v))
            data[stem][k] = (v, name)
    return data, conflicts


def load_english():
    en, existing = {}, {}
    for p in glob.glob(os.path.join(SRC, '*.json')):
        j = jl(p)
        if isinstance(j, dict) and 'en' in j:
            en[j['stem']] = j['en']
            existing[j['stem']] = j.get('ru_existing', {})
    return en, existing


class Report(object):
    def __init__(self):
        self.groups = collections.OrderedDict()

    def add(self, group, line):
        self.groups.setdefault(group, []).append(line)

    def total(self):
        return sum(len(v) for v in self.groups.values())

    def dump(self, quiet=False):
        os.makedirs(os.path.dirname(REPORT), exist_ok=True)
        with io.open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
            if not self.groups:
                f.write('Чисто.\n')
            for g, items in self.groups.items():
                f.write('== %s: %d\n' % (g, len(items)))
                for i in items:
                    f.write('   %s\n' % i)
                f.write('\n')
        if not quiet:
            for g, items in self.groups.items():
                print('== %s: %d' % (g, len(items)))
                for i in items[:6]:
                    print('   %s' % i)
                if len(items) > 6:
                    print('   ... ещё %d, целиком в work/check.txt' % (len(items) - 6))


def check_text(rep, G, TRD, EN):
    forb = G['запрещено']
    labels = set(G['метки_блоков'])
    imper = G['повелительное']
    allow = G['повелительное_разрешено']

    for stem, d in sorted(TRD.items()):
        en = EN.get(stem, {})
        ok_imper = set(allow.get(stem, []))
        ok_newline = set(G.get('переносы_проверены', {}).get(stem, []))
        ok_braces = set(G.get('фигурные_скобки_разрешены', {}).get(stem, []))
        for sid in sorted(d, key=lambda x: (len(x), x)):
            v, f = d[sid]
            where = '%s %s (%s)' % (stem, sid, f)
            e = en.get(sid, '')

            for w in WORD.findall(v):
                if MIXED.search(w):
                    rep.add('смесь кириллицы и латиницы', '%s: %r' % (where, w))

            if G.get('ё_запрещена') and re.search('[\u0451\u0401]', v):
                rep.add('буква ё', '%s: %s' % (where, re.findall('\\S*[\u0451\u0401]\\S*', v)[:3]))

            if G.get('кавычки') == 'прямые':
                odd = [c for c in '«»“”„‘’' if c in v]
                if odd:
                    rep.add('кавычки не прямые: %s' % ''.join(odd),
                            '%s: %s' % (where, re.sub(r'\s+', ' ', v)[:90]))

            if v.count('\u00ab') != v.count('\u00bb'):
                rep.add('непарные кавычки', where)

            if re.search(r'\s[,.;:!?](?![.,])', v):
                rep.add('пробел перед знаком препинания', '%s: %s' % (where, re.findall(r'\S*\s[,.;:!?]\S*', v)[:2]))

            if '  ' in v.replace('\n', '') and '  ' not in e.replace('\n', ''):
                rep.add('наш двойной пробел', where)

            if v != v.strip() and e == e.strip():
                rep.add('наши пробелы по краям', where)

            for bad, good in forb.items():
                if bad in v:
                    rep.add('термин: %s -> %s' % (bad, good), where)

            for m in re.finditer(r'\{([^{}]*)\}', v):
                if CYR.search(m.group(1)) and sid not in ok_braces:
                    rep.add('кириллица в фигурных скобках', '%s: {%s}' % (where, m.group(1)))

            # кавычки внутри кавычек: вся статья взята в кавычки и названия внутри тоже
            if (len(v) > 200 and v.count('"') >= 4
                    and v.lstrip().startswith('"') and v.rstrip().endswith('"')):
                inner = v.strip()[1:-1]
                if '"' in inner:
                    rep.add('кавычки внутри кавычек', '%s: %s' % (where, re.sub(r'\s+', ' ', v)[:90]))

            m = DUPWORD.search(v)
            if (m and '\n' not in m.group(0) and v[m.end():m.end() + 1] != '-'
                    and m.group(0) not in G.get('повтор_слова_разрешен', [])):
                rep.add('повтор слова', '%s: %r' % (where, m.group(0)))

            if sid not in ok_imper:
                for w in imper:
                    if re.search('(?<![\u0410-\u044f\u0401\u0451])%s(?![\u0410-\u044f\u0401\u0451])' % re.escape(w), v):
                        i = v.find(w)
                        rep.add('обращение к игроку в повелительном наклонении',
                                '%s: …%s…' % (where, v[max(0, i - 40):i + 70].replace('\n', ' ')))
                        break

            if e:
                a = collections.Counter(TOKEN.findall(e))
                b = collections.Counter(TOKEN.findall(v))
                if a != b and sid not in ok_braces:
                    only_en = sorted((a - b).elements())
                    only_ru = sorted((b - a).elements())
                    # заглушки мода в квадратных скобках мы намеренно переводим
                    if not (only_ru == [] and all(BRACKET.fullmatch(x) for x in only_en)):
                        rep.add('подстановки и теги не совпадают с оригиналом',
                                '%s: оригинал %s, перевод %s' % (where, only_en, only_ru))
                if e.count('\n') != v.count('\n') and sid not in ok_newline:
                    block = any((lab + ':') in v for lab in labels)
                    rep.add('переносы строк в блоке данных' if block else 'переносы строк',
                            '%s: оригинал %d, перевод %d' % (where, e.count('\n'), v.count('\n')))

            # строка без кириллицы — ошибка, только если это не намеренный
            # пропуск (титры, названия песен): такие совпадают с оригиналом
            if (not CYR.search(v) and not common.skip(v)
                    and re.search('[a-zA-Z]{4,}', v) and v != e):
                rep.add('строка без кириллицы', '%s: %r' % (where, v[:70]))

    # метки проверяем только внутри блоков данных о планетах: это строки,
    # где уже стоят минимум две известные метки
    found = collections.Counter()
    for stem, d in TRD.items():
        for sid in d:
            v = d[sid][0]
            here = [m.group(1) for m in LABEL.finditer(v)]
            if sum(1 for x in here if x in labels) < 2:
                continue
            for x in here:
                if x not in labels:
                    found[x] += 1
    for lab, n in found.items():
        rep.add('метка блока данных не из словаря', '%s — %d строк' % (lab, n))


def check_untranslated(rep, TRD, EN, EX, G):
    """Строки, которые стоило перевести: ни у нас, ни у самого мода русского нет."""
    for stem, en in sorted(EN.items()):
        d = TRD.get(stem)
        if not d:
            continue
        ex = EX.get(stem, {})
        skip_ids = set(G.get('не_переводим', {}).get(stem, []))
        for sid, e in sorted(en.items(), key=lambda x: (len(x[0]), x[0])):
            if sid in d or common.skip(e) or not re.search('[a-zA-Z]{3,}', e):
                continue
            if common.has_russian(ex.get(sid), e) or sid in skip_ids:
                continue
            if BRACKET.fullmatch(e.strip()):
                continue
            rep.add('нет перевода', '%s %s: %r' % (stem, sid, e[:60]))


def check_build(rep):
    import subprocess, filecmp
    build = os.path.join(ROOT, 'build')
    dist = os.path.join(ROOT, 'dist')
    subprocess.run([sys.executable, os.path.join(HERE, 'build.py')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for p in sorted(glob.glob(os.path.join(build, '*.tlk'))):
        name = os.path.basename(p)
        matches = glob.glob(os.path.join(dist, '*', '*', 'CookedPCConsole', name))
        if not matches:
            rep.add('сборка', 'нет в dist: %s' % name)
        elif not filecmp.cmp(p, matches[0], shallow=False):
            rep.add('сборка', 'build и dist расходятся: %s' % name)
    readme = io.open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    for p in sorted(glob.glob(os.path.join(dist, '*', '*', 'CookedPCConsole', '*_RUS.tlk'))):
        name = os.path.basename(p)
        kb = int(round(os.path.getsize(p) / 1024.0))
        m = re.search('`%s`[^|]*\\|[^|]*\\|\\s*(\\d+)\\s*КБ' % re.escape(name), readme)
        if m and int(m.group(1)) != kb:
            rep.add('README: размер файла',
                    '%s: написано %s КБ, на самом деле %d КБ' % (name, m.group(1), kb))


def main():
    quiet = '--quiet' in sys.argv
    G = load_glossary()
    TRD, conflicts = load_translation()
    EN, EX = load_english()
    rep = Report()

    for stem, sid, f1, v1, f2, v2 in conflicts:
        rep.add('один ключ переведён дважды по-разному',
                '%s %s: %s «%s» / %s «%s»' % (stem, sid, f1, v1[:40], f2, v2[:40]))

    check_text(rep, G, TRD, EN)
    check_untranslated(rep, TRD, EN, EX, G)
    if '--build' in sys.argv:
        check_build(rep)

    rep.dump(quiet)
    strings = sum(len(d) for d in TRD.values())
    print('\nпроверено строк: %d, замечаний: %d' % (strings, rep.total()))
    print('полный отчёт: %s' % os.path.relpath(REPORT, ROOT))
    return 1 if rep.total() else 0


if __name__ == '__main__':
    sys.exit(main())
