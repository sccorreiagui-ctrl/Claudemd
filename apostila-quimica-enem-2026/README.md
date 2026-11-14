# Apostila de Química para o ENEM 2026

PDF final: `APOSTILA_QUIMICA_ENEM_2026.pdf` (40 páginas A4). Relatório: `docs/RELATORIO_VALIDACAO.md`. Plano e histórico: `docs/PLANO_E_PROGRESSO.md`.

## Reconstruir
```bash
npm install                                   # KaTeX e fontes
pip install rdkit pymupdf fonttools brotli    # estruturas, PDF e métricas de fonte
python3 build/build.py                        # gera APOSTILA_QUIMICA_ENEM_2026.pdf
python3 build/build.py --png 100 --pages 3,4  # PNGs em build/renders/ (páginas por número de ordem)
```
Requer Playwright com Chromium. O relatório de layout (`build/out/layout_report.json`) mostra estouro (`over`) e sobra (`free`) em px por página.

## Estrutura
- `src/pages/pNN_chave.html` — uma página por arquivo; cabeçalho em comentário (`key`, `block`, `title`).
- `src/css/style.css` — design system (cores semânticas por bloco, caixas, tabelas, cartões).
- `build/figs_*.py` — figuras SVG (`@fig("nome")`), usadas com `{{fig:nome}}`; `build/mol.py` desenha moléculas a partir de SMILES (RDKit).
- Macros: `\ce{H2SO4}`, `$formula$`, `{{icon:x}}`, `{{pg:chave}}`, `{{q:chave}}` (número da questão), `{{qn:chave}}`, `{{ans:chave}}` (letra do gabarito).
- Gabarito: a alternativa correta leva `data-ok="1"`; `build/shuffle_answers.py` foi usado uma única vez para distribuir as respostas.
