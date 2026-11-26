# Apostila CTG — Geometria Analítica (PAS 3/UnB 2026)

PDF final: `CTG_GEOMETRIA_ANALITICA_PAS3_2026.pdf` (14 páginas A4).

## Regenerar
```bash
npm install                       # katex (renderização das fórmulas)
pip install sympy pillow          # validação matemática
python3 scripts/validate.py       # 105 verificações simbólicas (SymPy) — deve terminar em "TODAS AS VERIFICAÇÕES PASSARAM"
python3 scripts/diagrams.py       # gera diagrams/*.svg (coordenadas exatas; falha se um ponto não estiver na reta/circunferência)
node scripts/build.js             # monta build/apostila.html, ajusta fonte por página, gera o PDF e PNGs de inspeção
```
Requer Node + Playwright (Chromium) e a fonte Inter instalada no sistema.

## Estrutura
- `pages/p01.html … p14.html` — conteúdo de cada página (fórmulas em `$…$`/`$$…$$`; figuras em `{{svg:nome}}`)
- `style.css` — identidade visual CTG e cores semânticas
- `scripts/` — `validate.py`, `diagrams.py`, `build.js`, `contact.js` (folha de contato dos SVGs)
- `diagrams/` — 35 SVG vetoriais (todos usados)
- `RELATORIO_QUALIDADE.md` — relatório de qualidade
