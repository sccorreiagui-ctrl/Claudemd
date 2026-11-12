# Manual Estratégico de Matemática — ENEM 2026

PDF final: `out/Manual_Estrategico_Matematica_ENEM_2026.pdf` (26 páginas A4).

## Como regenerar
```bash
python3 build.py              # manual completo -> out/Manual_Estrategico_Matematica_ENEM_2026.pdf
python3 build.py --only 10,11 # prévia de páginas específicas -> out/preview.pdf
python3 tests/verify.py       # recalcula, de forma independente, os resultados dos exemplos
```
Requisitos: Python 3, Node + Playwright (Chromium). KaTeX está em `vendor/katex`.
O relatório do build lista, por página, transbordo, espaço livre, texto cortado e erros de KaTeX.

## Estrutura
- `src/style.css` — sistema visual (cores com significado fixo: azul-marinho = títulos, azul = explicação, verde = fórmula/resposta, laranja = erro, roxo = memorização).
- `src/lib.py` — componentes (cartão de tópico, fórmula, exemplo, "aplique", teste rápido, tabela).
- `src/svg.py` — biblioteca de figuras vetoriais (planos cartesianos, sólidos, arcos, cotas).
- `src/ch00..ch09_*.py` — um módulo por capítulo (figuras + conteúdo); edite só o capítulo afetado.
- `build.py` / `render.js` — montagem do HTML e impressão em PDF via Chromium.
