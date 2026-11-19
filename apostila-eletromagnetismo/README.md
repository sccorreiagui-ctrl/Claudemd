# Apostila CTG de Eletromagnetismo — PAS 3 / UnB 2026

Projeto editável que gera o PDF **`CTG_ELETROMAGNETISMO_PAS3_UNB_2026.pdf`** (28 páginas A4, texto pesquisável,
diagramas vetoriais, fórmulas em KaTeX). Tudo é regenerável a partir dos arquivos-fonte deste diretório.

> Relatório de qualidade (conteúdo, contagens, correções científicas, verificações e limitações):
> [`RELATORIO_QUALIDADE.md`](RELATORIO_QUALIDADE.md).

## Regenerar tudo

```bash
bash scripts/rebuild_all.sh            # figuras → HTML → PDF → PDF final → checagens → validação física (~2,5 min)
bash scripts/rebuild_all.sh --sem-fisica
```

Requisitos: Node ≥ 18 (com `npm install`: `katex`, `cheerio`, `@fontsource/source-serif-4`, `@fontsource/source-sans-3`),
Playwright com Chromium (`require('playwright')` precisa resolver), Python 3 com `numpy`, `scipy`, `pillow`, `fonttools`
(+ `brotli`), `pypdf`, e `poppler-utils` (`pdftotext`, `pdffonts`, `pdfinfo`, `pdfimages`, `pdftoppm`).
Na primeira execução o script copia KaTeX/fontes para `assets/` (`scripts/vendor.mjs`) e cria `scripts/_fonts/` (TTFs só para
medir largura de texto nas figuras; `scripts/make_ttf.py`).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/pages/p01.html … p28.html` | **O texto do livro**, uma página por arquivo (português). |
| `src/meta.json` | Título, módulos (faixas de páginas) e, para cada página: título, assunto do rodapé e subtítulo. |
| `src/css/book.css` | Identidade visual CTG: paleta semântica, tipografia, caixas, cartões de fórmula, exemplos, exercícios. |
| `scripts/figs_m1.py … figs_m5.py` | **Geradores de todas as figuras SVG** (uma função por figura). Saída: `build/figures/*.svg`. |
| `scripts/svglib.py` | Biblioteca de desenho (setas em polígono, medida real de texto, projeções 3D, gráficos). |
| `scripts/fields.py` | Modelos numéricos de campo (espira por integrais elípticas, solenoide, dipolo, linhas de campo por RK4). |
| `scripts/build.mjs` | Monta `build/book.html` (KaTeX pré-renderizado, figuras, numeração, rodapé). |
| `scripts/make_pdf.mjs` | Gera `build/book.pdf` (Chromium) e mede folga/estouro (mm) de cada página. |
| `scripts/finalize_pdf.py` | Cria o PDF final: metadados, idioma pt-BR e marcadores de navegação. |
| `scripts/check_pdf.py` | Confere 28 páginas A4, rodapé exato, texto, fontes incorporadas, ausência de raster. |
| `scripts/validate_physics.py` | Validação numérica independente dos exemplos, exercícios e gabaritos. |
| `scripts/fonts_audit.mjs`, `stats.py` | Auditoria de fontes de fallback; estatísticas (exemplos, exercícios, figuras…). |
| `scripts/render.sh`, `inspect.mjs`, `shots.mjs` | Apoio à revisão visual (PNG das páginas, alturas dos blocos, PNG das figuras). |
| `build/` | Saídas intermediárias versionadas (`book.html`, `book.pdf`, `figures/`). |
| `report/` | Relatórios gerados (`verificacoes.txt`, `checagem_pdf.txt`, `estatisticas.txt`). |

## Como editar

1. **Texto**: edite `src/pages/pNN.html` e rode `node scripts/build.mjs && node scripts/make_pdf.mjs`.
   O relatório impresso no terminal mostra, por página, a folga em mm (`folga`) e marca `<<< PROBLEMA` se algo estourar.
   O conteúdo de cada página cabe numa área fixa: se estourar, enxugue texto/figuras; se sobrar muito, a folga é distribuída
   entre os blocos (`.main` com `space-between`).
2. **Figuras**: edite a função em `scripts/figs_mN.py` e rode `cd scripts && python3 figs_mN.py`. Os geradores calculam
   os vetores com produtos vetoriais (`numpy`) e **abortam (`assert`) se o sentido desenhado contradiz a física**.
3. **PDF final**: `python3 scripts/finalize_pdf.py && python3 scripts/check_pdf.py`.

### Marcação usada nas páginas (processada por `build.mjs`)

| Marcação | Resultado |
|---|---|
| `$…$` / `$$…$$` | fórmula KaTeX (vírgula decimal automática; macros: `\vB`, `\vv`, `\vF`, `\un{m/s}`, `\tx{-5}` = `×10⁻⁵`, `\sen`, `\dd`…) |
| `<x-fig name="arquivo"><cap>legenda</cap></x-fig>` | figura de `build/figures/arquivo.svg` com legenda numerada (“Fig. P.n”); sem `<cap>`, sem número |
| `<x-ref f="arquivo">` | referência à numeração da figura (use sempre com tag de fechamento) |
| `<x-fc t="…" s="…" eq="eq1 ;; eq2">` + `<p data-k="Variáveis">…` | cartão de fórmula (cada `;;` = uma linha de equação) |
| `<x-ex n l t>` + `<p data-k="Situação">…` | exemplo resolvido (`l` = nível 1–3); linhas: Situação, Esquema, Dados, Fenômeno, Método, Cálculo, Resultado, Verificação |
| `<x-box k="warn|mem|pre|hist|ok" t="título">` | caixa colorida |
| `<x-exs>` · `<x-exe n l [p="Q"]>` · `<x-ans>` | bloco de exercícios (rodapé da página), exercício e respostas |
| `<x-ok></x-ok>` ou `✓` | ícone vetorial de conferência (o glifo ✓ não existe nas fontes do livro) |

Atributos (`t=`, `s=`, `cap=`) podem conter matemática (`t="Antes de usar $BLv$"`).

## Convenções do livro

- **Cores com significado fixo**: azul = campo externo/referência · roxo = campo/efeito induzido · laranja = corrente convencional ·
  verde = força e itens conferidos · ciano = velocidade · vermelho = polaridades, erros e alertas · cinza = estrutura.
- Todo vetor desenhado tem rótulo; a cor nunca é a única informação.
- Progressão de cada assunto: Intuição → Fenômeno → Desenho → Explicação → Fórmula → Exemplo → Exercício.
- Rodapé de todas as páginas: `CTG · FÍSICA · ELETROMAGNETISMO · ASSUNTO · NN/28`.
- Todos os exercícios são **autorais** (nenhuma questão oficial foi reproduzida).

## Licenças de terceiros

Source Serif 4 e Source Sans 3 (SIL OFL 1.1), KaTeX (MIT), cheerio (MIT). Os arquivos de fonte incorporados ao PDF
mantêm suas licenças originais.
