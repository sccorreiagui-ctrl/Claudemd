# Apostila Estratégica de Física Moderna — PAS 3/UnB

PDF final: `../APOSTILA_FISICA_MODERNA_PAS3_UNB_2026.pdf` (15 páginas A4).

## Estrutura
- `src/pages/p01.html … p15.html` — conteúdo de cada página (HTML + fórmulas em LaTeX dentro de `<m>…</m>`).
- `src/styles.css` — identidade visual (cores semânticas, caixas, tabelas, grade A4).
- `src/figures.py` — gera as 18 figuras vetoriais (SVG) **a partir das equações** (Planck, Einstein, Bohr, Hubble, decaimento…). Saída em `figures/`.
- `src/build.py` — roda as figuras, monta `out/apostila.html` e chama `src/render.js`.
- `src/render.js` — Playwright/Chromium: renderiza as fórmulas (KaTeX local em `vendor/katex`), ajusta a escala de cada página para preencher o A4 sem estourar (1,00–1,22×), mede o layout (`out/layout_report.json`) e exporta o PDF.

## Regenerar
```bash
python3 src/build.py          # figuras + HTML + PDF
python3 src/build.py --html   # só o HTML (out/apostila.html)
```
Requisitos: Python 3, Node com `playwright` (Chromium) acessível via `NODE_PATH`, fonte Inter instalada. `pdftoppm`/`pdftotext` (poppler) servem para conferir o resultado.

Para alterar um texto, edite a página correspondente em `src/pages/`; para alterar uma curva ou diagrama, edite a função da figura em `src/figures.py`.
