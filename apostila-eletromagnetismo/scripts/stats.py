#!/usr/bin/env python3
"""Estatísticas do material (lidas das fontes em src/pages e do HTML gerado). Saída: report/estatisticas.txt"""
import collections
import glob
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ex, exe, figs = [], [], []
for f in sorted(glob.glob(os.path.join(ROOT, 'src/pages/p*.html'))):
    n = int(re.search(r'p(\d+)\.html', f).group(1))
    s = open(f, encoding='utf8').read()
    ex += [(n, int(m.group(1)), int(m.group(2)), m.group(3)) for m in re.finditer(r'<x-ex n="(\d+)" l="(\d)" t="([^"]*)"', s)]
    for m in re.finditer(r'<x-exe ([^>]*)>', s):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        exe.append((n, a.get('p', 'E'), int(a['n']), int(a.get('l', 1))))
    figs += [(n, m.group(1), bool(m.group(2))) for m in re.finditer(r'<x-fig name="([^"]+)"[^>]*>(<cap>)?', s)]
    figs += [(n, m, False) for m in re.findall(r'\{\{svg:([A-Za-z0-9_]+)\}\}', s)]

E = [x for x in exe if x[1] == 'E']
Q = [x for x in exe if x[1] == 'Q']
lv = lambda items, k: collections.Counter(x[k] for x in items)
names = {1: 'fundamental', 2: 'intermediário', 3: 'avançado'}


def dist(c):
    return ', '.join(f'{names[k]} {c.get(k, 0)}' for k in (1, 2, 3))


html = open(os.path.join(ROOT, 'build/book.html'), encoding='utf8').read()
katex = len(re.findall(r'<span class="katex"', html))
svgs = sorted({n for _, n, _ in figs})
all_items = lv(ex, 2) + lv(E, 3) + lv(Q, 3)
tot = sum(all_items.values())
asserts = sum(open(f, encoding='utf8').read().count('assert ') for f in glob.glob(os.path.join(ROOT, 'scripts/figs_m*.py')))

L = []
L.append('ESTATÍSTICAS DO MATERIAL (geradas por scripts/stats.py)')
L.append(f'páginas: 28 (A4)')
L.append(f'exemplos resolvidos: {len(ex)}  → {dist(lv(ex, 2))}')
L.append(f'exercícios de página (E1–E{len(E)}): {len(E)}  → {dist(lv(E, 3))}')
L.append(f'itens do mini-simulado (Q1–Q{len(Q)}, p. 28): {len(Q)}  → {dist(lv(Q, 3))}')
L.append(f'total de itens de prática (exemplos + exercícios + mini-simulado): {tot}')
L.append('distribuição por nível no total: ' + ', '.join(f'{names[k]} {all_items.get(k, 0)} ({100 * all_items.get(k, 0) / tot:.0f}%)' for k in (1, 2, 3)))
L.append(f'figuras SVG vetoriais distintas usadas nas páginas: {len(svgs)}  (inserções: {len(figs)}; com legenda numerada: {sum(1 for *_, c in figs if c)})')
L.append(f'expressões matemáticas (KaTeX): {katex}')
L.append(f'verificações geométricas (assert) nos geradores de figuras: {asserts}')
L.append('')
L.append('exemplos resolvidos por página: ' + ', '.join(f'p.{n}: Ex.{k} ({t})' for n, k, _, t in ex))
open(os.path.join(ROOT, 'report', 'estatisticas.txt'), 'w', encoding='utf8').write('\n'.join(L) + '\n')
print('\n'.join(L))
