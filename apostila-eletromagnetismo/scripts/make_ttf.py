"""Converte os subconjuntos woff2 das fontes (assets/fonts) em TTF para medir larguras de texto (svglib.py).
Uso: python3 scripts/make_ttf.py   (requer: pip install fonttools brotli)"""
import os
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__))
src, dst = os.path.join(HERE, '..', 'assets', 'fonts'), os.path.join(HERE, '_fonts')
os.makedirs(dst, exist_ok=True)
names = [('source-serif-4', '400', 'normal'), ('source-serif-4', '400', 'italic'), ('source-serif-4', '700', 'normal'), ('source-serif-4', '700', 'italic'),
         ('source-sans-3', '400', 'normal'), ('source-sans-3', '600', 'normal'), ('source-sans-3', '700', 'normal'), ('source-sans-3', '800', 'normal')]
n = 0
for fam, w, st in names:
    for sub in ('latin', 'greek'):
        f = os.path.join(src, f'{fam}-{sub}-{w}-{st}.woff2')
        if os.path.exists(f):
            t = TTFont(f); t.flavor = None; t.save(os.path.join(dst, f'{fam}-{sub}-{w}-{st}.ttf')); n += 1
print('convertidos', n)
