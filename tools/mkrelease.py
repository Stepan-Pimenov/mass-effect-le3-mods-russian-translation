# -*- coding: utf-8 -*-
"""Собирает архивы для страницы релизов.

  python tools/mkrelease.py [версия]

Полный архив включает программу-установщик, скриптовую версию и папку dist.
Отдельные архивы по компонентам предназначены для ручной распаковки в DLC.
"""
import os
import sys
import shutil
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.join(ROOT, 'release')
DIST = os.path.join(ROOT, 'dist')
VER = sys.argv[1] if len(sys.argv) > 1 else 'v1.0'
EXE = 'ME3LE-Русификатор-модов.exe'

TOP = [EXE, 'install.ps1', 'uninstall.ps1', 'README.md', 'README.en.md', 'LICENSE']


def arc(path, base):
    return os.path.relpath(path, base).replace(os.sep, '/')


def main():
    missing = [f for f in TOP if not os.path.exists(os.path.join(ROOT, f))]
    if missing:
        print('не хватает файлов: ' + ', '.join(missing))
        if EXE in missing:
            print('установщик собирается так: '
                  'powershell -ExecutionPolicy Bypass -File tools\\build_installer.ps1')
        return 1

    if os.path.isdir(REL):
        shutil.rmtree(REL)
    os.makedirs(REL)

    full = os.path.join(REL, 'ME3LE-Russian-Mods-%s-full.zip' % VER)
    with zipfile.ZipFile(full, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in TOP:
            z.write(os.path.join(ROOT, f), f)
        for dirpath, _, names in os.walk(DIST):
            for name in names:
                p = os.path.join(dirpath, name)
                z.write(p, arc(p, ROOT))
    print('%-46s %6d КБ' % (os.path.basename(full), os.path.getsize(full) // 1024))

    for comp in sorted(os.listdir(DIST)):
        cdir = os.path.join(DIST, comp)
        if not os.path.isdir(cdir):
            continue
        zp = os.path.join(REL, 'ME3LE-Russian-%s-%s.zip' % (comp, VER))
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for dirpath, _, names in os.walk(cdir):
                for name in names:
                    p = os.path.join(dirpath, name)
                    z.write(p, arc(p, cdir))
        print('%-46s %6d КБ' % (os.path.basename(zp), os.path.getsize(zp) // 1024))

    print('\nархивы готовы: ' + REL)
    return 0


if __name__ == '__main__':
    sys.exit(main())
