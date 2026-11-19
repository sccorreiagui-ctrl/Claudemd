#!/usr/bin/env python3
"""Pós-processa build/book.pdf → CTG_ELETROMAGNETISMO_PAS3_UNB_2026.pdf

- metadados (título, autor, assunto, palavras-chave, idioma pt-BR);
- marcadores de navegação (módulos I–VI e as 28 páginas);
- página 1 abre com o documento ajustado à largura da janela.
Não altera o conteúdo das páginas.
"""
import json
import os
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NameObject as N, TextStringObject, NumberObject

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'build', 'book.pdf')
OUT = os.path.join(ROOT, 'CTG_ELETROMAGNETISMO_PAS3_UNB_2026.pdf')

meta = json.load(open(os.path.join(ROOT, 'src', 'meta.json'), encoding='utf8'))

reader = PdfReader(SRC)
if len(reader.pages) != 28:
    sys.exit(f'ERRO: o PDF de origem tem {len(reader.pages)} páginas (esperado: 28)')

writer = PdfWriter(clone_from=reader)
writer.add_metadata({
    '/Title': 'Apostila CTG de Eletromagnetismo — PAS 3 / UnB 2026',
    '/Author': 'CTG',
    '/Subject': 'Física · Eletromagnetismo · Magnetismo, indução, motores, geradores, transformadores e ressonância magnética (PAS 3 / UnB)',
    '/Keywords': 'eletromagnetismo, magnetismo, PAS 3, UnB, Lei de Ampère, Lei de Faraday, Lei de Lenz, força magnética, transformadores, ressonância magnética',
    '/Creator': 'CTG · HTML/CSS + SVG + KaTeX · Chromium (Playwright)',
})
writer.root_object[NameObject('/Lang')] = TextStringObject('pt-BR')

# marcadores: módulo → páginas
pages_meta = {p['n']: p for p in meta['pages']}
for key, mod in meta['modules'].items():
    a, b = mod['pages']
    parent = writer.add_outline_item(f"Módulo {key} · {mod['name']}  (p. {a}–{b})", a - 1)
    for n in range(a, b + 1):
        writer.add_outline_item(f"{n:02d} · {pages_meta[n]['title']}", n - 1, parent=parent)

writer.page_mode = '/UseOutlines'
writer.write(OUT)
print('gerado:', OUT, f'({os.path.getsize(OUT) / 1e6:.2f} MB)')
