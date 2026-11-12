#!/usr/bin/env python3
"""Monta o manual: capítulos (src/ch*.py) -> build/manual.html -> out/*.pdf (via render.js / Chromium).

Uso:
  python3 build.py                 # manual completo
  python3 build.py --only 10,11    # apenas as páginas indicadas (prévia rápida)
"""
import importlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'src'))

import lib  # noqa: E402

MODULES = ['ch01_basico', 'ch02_estatistica', 'ch03_algebra', 'ch04_progressoes', 'ch05_plana',
           'ch06_trigonometria', 'ch07_espacial', 'ch08_analitica', 'ch09_final']
OUTFILE = 'Manual_Estrategico_Matematica_ENEM_2026.pdf'

KATEX_JS = """
<script src="../vendor/katex/katex.min.js"></script>
<script src="../vendor/katex/contrib/auto-render.min.js"></script>
<script>
window.addEventListener('load', () => {
  renderMathInElement(document.body, {
    delimiters: [{left:'\\\\[', right:'\\\\]', display:true}, {left:'\\\\(', right:'\\\\)', display:false}],
    throwOnError: false, errorColor: '#B42318',
    macros: {'\\\\sen':'\\\\operatorname{sen}', '\\\\tg':'\\\\operatorname{tg}', '\\\\mmc':'\\\\operatorname{mmc}',
             '\\\\mdc':'\\\\operatorname{mdc}', '\\\\cossec':'\\\\operatorname{cossec}', '\\\\ds':'\\\\displaystyle'}
  });
  document.fonts.ready.then(() => { window.__done = true; });
});
</script>
"""


def collect_pages():
    pages = []
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            print('(módulo ainda não escrito: %s)' % name)
            continue
        for body in mod.pages():
            pages.append((mod.LABEL, body))
    return pages


def main():
    only = None
    if '--only' in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')}
    rendered = collect_pages()
    # página 1 = capa/sumário (precisa do mapa tópico -> página)
    topic_pages = []
    for i, (label, body) in enumerate(rendered, start=2):
        for m in re.finditer(r'data-topics="([^"]+)"', body):
            topic_pages.append((m.group(1), i))
    try:
        cover = importlib.import_module('ch00_cover')
    except ModuleNotFoundError:
        class cover:  # protótipo: capa ainda não escrita
            body = staticmethod(lambda tp, total: '<h1>capa</h1>')
    html_pages = [lib.page(1, 'CAPA · SUMÁRIO · GUIA DE REVISÃO', cover.body(topic_pages, total=len(rendered) + 1), 'cover')]
    for i, (label, body) in enumerate(rendered, start=2):
        html_pages.append(lib.page(i, label, body))
    if only:
        html_pages = [p for p in html_pages if int(re.search(r'data-page="(\d+)"', p).group(1)) in only]
    css = open(os.path.join(ROOT, 'src', 'style.css'), encoding='utf-8').read()
    html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<title>Manual Estratégico de Matemática — ENEM 2026</title>'
            '<link rel="stylesheet" href="../vendor/katex/katex.min.css">'
            f'<style>{css}</style></head><body>{"".join(html_pages)}{KATEX_JS}</body></html>')
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    hpath = os.path.join(ROOT, 'build', 'manual.html')
    open(hpath, 'w', encoding='utf-8').write(html)
    out = os.path.join(ROOT, 'out', ('preview.pdf' if only else OUTFILE))
    res = subprocess.run(['node', os.path.join(ROOT, 'render.js'), hpath, out], capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr)
        sys.exit(1)
    rep = json.loads(res.stdout.strip().splitlines()[-1])
    print('PDF:', out)
    if rep['errs']:
        print('ERROS JS:', rep['errs'])
    if rep['katexErrors']:
        print('ERROS KaTeX:', rep['katexErrors'])
    print(f"{'pág':>3} {'overflow':>8} {'livre(px)':>9}  alertas")
    for p in rep['pages']:
        flag = []
        if p['overflow'] > 0:
            flag.append('TRANSBORDA')
        if p['free'] > 60:
            flag.append('espaço sobrando')
        if p['wide']:
            flag.append('largura:' + ','.join(p['wide']))
        if p['clipped']:
            flag.append('cortado:' + ','.join(p['clipped']))
        print(f"{p['n']:>3} {p['overflow']:>8} {p['free']:>9}  {' | '.join(flag)}")


if __name__ == '__main__':
    main()
