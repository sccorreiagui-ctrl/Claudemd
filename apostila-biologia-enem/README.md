# Apostila Visual de Biologia para o ENEM 2026

PDF final: `APOSTILA_BIOLOGIA_ENEM_2026.pdf` (40 páginas, A4).

## Reconstruir
```
python3 tools/gen_*.py ; node tools/gen_*.mjs   # gera os SVGs em src/svg (rodar os scripts gen_*)
node tools/build.mjs APOSTILA_BIOLOGIA_ENEM_2026.pdf
tools/render.sh APOSTILA_BIOLOGIA_ENEM_2026.pdf 100   # PNGs para inspeção em build/png
```
- `src/style.css`: identidade visual e cores com significado permanente.
- `src/pages/pNN-*.html`: uma página por arquivo (HTML + SVG inline; `{{svg:nome}}` inclui `src/svg/nome.svg`).
- `tools/gen_*`: geradores dos diagramas vetoriais; `tools/build.mjs`: monta o HTML, exporta o PDF com Playwright/Chromium e audita overflow, cortes e sobreposição de rótulos.
