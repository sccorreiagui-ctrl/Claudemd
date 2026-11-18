# CTG · Apostila de Matemática — Números Complexos e Polinômios (PAS 3 / UnB)

PDF final: `dist/CTG_MATEMATICA_COMPLEXOS_POLINOMIOS_PAS3_2026.pdf` (40 páginas A4: p. 1–20 Complexos, p. 21–40 Polinômios).
Relatório de qualidade: [`RELATORIO_QUALIDADE.md`](RELATORIO_QUALIDADE.md).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `content/pages/p01.html … p40.html` | uma página por arquivo (HTML + math em `$…$`/`$$…$$` + `{{fig:nome}}`) |
| `build/style.css`, `build/build.cjs` | identidade visual CTG, composição, KaTeX no servidor, PDF via Playwright/Chromium, relatório de estouro por página |
| `build/add_extras.py` | acrescenta «Itens PAS comentados» e «Treinos rápidos» às páginas com folga (idempotente) |
| `figs/svgkit.py`, `figs/figs_c.py`, `figs/figs_p.py`, `figs/figs_flow.py`, `figs/figs_mpl.py` | todas as figuras, geradas por código (SVG vetorial; gráficos de polinômios com matplotlib a partir das funções) |
| `figs/svg/` | SVGs gerados |
| `verify/verify.py`, `verify/verify_figs.py` | verificação com SymPy de exemplos, gabaritos e dados das figuras |
| `assets/katex/` | CSS e fontes do KaTeX (cópia local; o PDF não depende de rede) |

## Regerar o PDF

```bash
npm ci                      # katex
pip install -r requirements.txt
npm run all                 # figuras → verificações → HTML/PDF (dist/)
```

Requer `playwright` com Chromium disponível para o Node (`require('playwright')`). A saída traz, por página, a folga em px e erros de estouro (`dist/layout_report.json`).

## Convenções

* Cores com papel fixo: azul = parte real/coeficientes; roxo = parte imaginária/complexos; verde = resultados e verificações; laranja = ângulos e etapas; vermelho = erros; cinza = auxiliar.
* Níveis discretos `N1` fundamentos, `N2` aplicações, `N3` desafios; formatos `C/E` (tipo A) e `B` (inteiro 000–999).
* Todos os itens são **autorais**, inspirados nas habilidades MAT8–MAT12; nenhum é atribuído à banca.
