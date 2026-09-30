# -*- coding: utf-8 -*-
import os, zipfile, shutil
REL = 'release'
VER = 'v1.0'
if os.path.isdir(REL):
    shutil.rmtree(REL)
os.makedirs(REL)

TOP = ['install.ps1', 'uninstall.ps1', 'Install.bat', 'Uninstall.bat',
       'Установить.bat', 'Удалить.bat', 'README.md', 'README.en.md']


def arc(p, base):
    return os.path.relpath(p, base).replace(os.sep, '/')


full = os.path.join(REL, 'LE3-RU-Mods-Translation-%s-full.zip' % VER)
with zipfile.ZipFile(full, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in TOP:
        z.write(f, f)
    for dp, _, fns in os.walk('dist'):
        for fn in fns:
            p = os.path.join(dp, fn)
            z.write(p, arc(p, '.'))
print('%-46s %6d KB' % (os.path.basename(full), os.path.getsize(full) // 1024))

for comp in sorted(os.listdir('dist')):
    cd = os.path.join('dist', comp)
    if not os.path.isdir(cd):
        continue
    zp = os.path.join(REL, 'LE3-RU-%s-%s.zip' % (comp, VER))
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, _, fns in os.walk(cd):
            for fn in fns:
                p = os.path.join(dp, fn)
                z.write(p, arc(p, cd))
    print('%-46s %6d KB' % (os.path.basename(zp), os.path.getsize(zp) // 1024))
