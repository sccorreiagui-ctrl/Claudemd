# Apostila Visual de Geografia — ENEM 2026

PDF final: `output/APOSTILA_GEOGRAFIA_ENEM_2026.pdf` (39 páginas, A4 vertical, texto selecionável).
Relatório de validação: `output/RELATORIO_VALIDACAO.md`. Fontes: `data/sources.md`.

## Como reconstruir
```bash
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt jinja2
python3 src/fetch_data.py          # baixa dados abertos para data/raw (≈ 95 MB)
python3 tools/make_fonts.py        # gera subconjuntos TrueType/WOFF2 da fonte Inter (requer Inter instalada)
python3 src/build.py               # gera figuras (SVG) e html/apostila.html
node tools/export_pdf.js           # exporta o PDF com Chromium (Playwright) e relata transbordamentos
```
Requer Node com `playwright` e Chromium. `src/build.py --pages` refaz só as páginas.

## Estrutura
- `pages/` páginas em HTML/Jinja2 (uma por arquivo, ordem alfabética) · `assets/css/` estilos
- `src/figs/` código dos mapas (GeoPandas/Matplotlib) e diagramas (SVG próprio, `src/svgkit.py`) · `assets/figures/` SVG gerados
- `data/processed/` séries conferidas · `NOTES_PROJETO.md` memória de trabalho
