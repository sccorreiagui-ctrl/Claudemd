#!/usr/bin/env python3
"""Confere o PDF final: 28 páginas A4, rodapé exato em todas as páginas, texto pesquisável, fontes incorporadas,
sem imagens rasterizadas, sem marcas de erro. Saída: relatório texto (também gravado em report/checagem_pdf.txt)."""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PDF = os.path.join(ROOT, 'CTG_ELETROMAGNETISMO_PAS3_UNB_2026.pdf')
LOG, FAIL = [], 0


def ok(name, cond, note=''):
    global FAIL
    LOG.append(f"[{'OK ' if cond else 'ERRO'}] {name} {note}")
    if not cond:
        FAIL += 1


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


info = run('pdfinfo', '-f', '1', '-l', '28', PDF)
n_pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
ok('número de páginas = 28', n_pages == 28, f'(encontrado {n_pages})')
sizes = re.findall(r'Page\s+\d+ size:\s+([\d.]+) x ([\d.]+) pts', info)
ok('todas as páginas A4 (595×842 pt, tolerância 1 pt)', len(sizes) == 28 and all(abs(float(w) - 595.3) < 1.0 and abs(float(h) - 841.9) < 1.0 for w, h in sizes))
ok('título nos metadados', 'Apostila CTG de Eletromagnetismo' in info)
ok('idioma pt-BR e marcadores de navegação', '/Lang' in open(PDF, 'rb').read().decode('latin-1') and '/Outlines' in open(PDF, 'rb').read().decode('latin-1'))

foot_re = re.compile(r'CTG · FÍSICA · ELETROMAGNETISMO · (.+?) · (\d\d)/28')
words_per_page = []
for n in range(1, 29):
    txt = run('pdftotext', '-f', str(n), '-l', str(n), '-layout', PDF, '-')
    words_per_page.append(len(txt.split()))
    m = list(foot_re.finditer(txt))
    ok(f'p.{n:02d}: rodapé "CTG · FÍSICA · ELETROMAGNETISMO · ASSUNTO · {n:02d}/28"', bool(m) and int(m[-1].group(2)) == n, f'→ {m[-1].group(0) if m else "ausente"}')
ok('texto selecionável (≥ 250 palavras por página)', min(words_per_page) >= 250, f'(mínimo {min(words_per_page)}, média {sum(words_per_page) // 28})')

full = run('pdftotext', PDF, '-')
for bad in ('undefined', 'NaN', '[figura', '[página', '$'):
    ok(f'sem marcas de erro «{bad}» no texto', bad not in full)

fonts = run('pdffonts', PDF)
rows = [l for l in fonts.splitlines()[2:] if l.strip()]
not_emb = [l for l in rows if not re.search(r'\s(yes)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', l)]
ok('todas as fontes incorporadas', not not_emb, f'({len(rows)} fontes)')
fam = sorted({re.sub(r'^[A-Z]{6}\+', '', l.split()[0]) for l in rows})
LOG.append('     fontes: ' + ', '.join(fam))
unexpected = [f for f in fam if not re.match(r'(SourceSerif|SourceSans|KaTeX_)', f)]
ok('somente Source Serif/Sans e KaTeX', not unexpected, f'{unexpected}')

# varredura por texto: nenhum trecho pode ter sido composto em fonte inesperada (fallback do navegador)
from pypdf import PdfReader
stray = []
for i, pg in enumerate(PdfReader(PDF).pages, 1):
    def visitor(text, cm, tm, font_dict, font_size, _i=i):
        fn = str((font_dict or {}).get('/BaseFont', ''))
        if text.strip() and fn and not re.search(r'(SourceSerif|SourceSans|KaTeX_)', fn):   # fn vazio = dicionário de fonte indisponível no visitante
            stray.append((_i, fn, text.strip()[:30]))
    pg.extract_text(visitor_text=visitor)
ok('nenhum trecho de texto em fonte de fallback', not stray, f'{stray[:5]}')

imgs = run('pdfimages', '-list', PDF).splitlines()[2:]
ok('diagramas vetoriais: nenhuma imagem raster no PDF', len(imgs) == 0, f'({len(imgs)} imagens)')

LOG.append(f'\nRESULTADO: {"APROVADO" if not FAIL else str(FAIL) + " FALHA(S)"}')
os.makedirs(os.path.join(ROOT, 'report'), exist_ok=True)
open(os.path.join(ROOT, 'report', 'checagem_pdf.txt'), 'w', encoding='utf8').write('CHECAGEM DO PDF FINAL — gerada por scripts/check_pdf.py\n' + '\n'.join(LOG) + '\n')
print('\n'.join(LOG))
sys.exit(1 if FAIL else 0)
