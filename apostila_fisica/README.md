# Apostila de Física Elétrica — ENEM + PAS 3 (UnB)

Curso compacto do básico ao avançado: **Fundamentos → Eletrostática → Eletrodinâmica → Magnetismo e eletromagnetismo → Revisão final** (55 páginas A4, vertical).

* **PDF final:** `APOSTILA_FISICA_ELETRICA_ENEM_PAS3_2026.pdf`
* **Relatório de qualidade:** `RELATORIO_QUALIDADE.md` (conteúdo, verificações, correções ao inventário, limitações)

## Estrutura do projeto

```
src/pages/      páginas p01…p55 (HTML + marcação: <fig name="…"/>, {{lvl:N}}, \( … \) e \[ … \] em KaTeX)
src/figures/    figuras em Python → SVG vetorial (registro @fig("nome"))
src/lib/        svgkit.py (texto/vetores/gráficos/linhas de campo + lint) e circuit.py (símbolos de circuitos)
src/style.css   tema, caixas (conceito, fórmula, exemplo, erro frequente, fixação…), cores semânticas
assets/         KaTeX e fontes (Source Sans 3) locais — o build não usa a internet
tools/          build.py, render.js, preview.py, verify_physics.py, make_report.py
figures_svg/    cópia de todas as figuras em SVG (geradas pelo build)
build/          apostila.html (montado), layout_report.json
```

## Como regenerar

Requisitos: Python 3.10+, Node 18+, Playwright com Chromium (`npm i`, `npx playwright install chromium`), `poppler-utils` (para `pdftoppm`/`pdfinfo`).

```bash
cd apostila_fisica
npm install                                  # KaTeX e fontes (já copiados em assets/)
python3 tools/build.py                       # monta build/apostila.html e figures_svg/ (mostra avisos de lint das figuras)
node tools/render.js APOSTILA_FISICA_ELETRICA_ENEM_PAS3_2026.pdf   # gera o PDF e mede cada página
python3 tools/verify_physics.py              # recalcula todos os números dos exemplos e exercícios
python3 tools/preview.py APOSTILA_FISICA_ELETRICA_ENEM_PAS3_2026.pdf 100   # PNGs em build/preview/
python3 tools/make_report.py                 # atualiza RELATORIO_QUALIDADE.md
```

O `render.js` imprime, por página, o preenchimento (%), estouros vertical e horizontal, equações mais largas que a coluna e erros do KaTeX; o build só é aceito quando **“com problema: 0”**.

## Convenções

* **Cores semânticas** (sempre acompanhadas de sinais, setas e rótulos): coral = cargas/polos +; azul = cargas − e elétrons; laranja = corrente convencional e trajetórias; roxo = campo magnético e indução; verde = energia e potência; ciano = campo elétrico e equipotenciais; cinza = neutros, condutores e estrutura.
* Cada seção: intuição → conceito → desenho → fórmula (variáveis, unidades, validade, sinais) → exemplo resolvido em 9 passos → erro frequente → fixação → aprofundamento; níveis ●○○, ●●○, ●●● discretos.
* Questões e itens C/E são **autorais**; nenhuma prova oficial é reproduzida.
* Segurança: nenhum experimento com rede elétrica, fios energizados ou capacitores de alta tensão.

## Créditos

KaTeX (MIT), Source Sans 3 (SIL OFL), Chromium/Playwright para o PDF. Matrizes de referência: INEP (ENEM) e Cebraspe/UnB (PAS 3).
