# Apostila Visual de História do Brasil — ENEM e PAS 3 (UnB) 2026

Apostila de **24 páginas A4** (Era Vargas, República de 1946, Ditadura Militar e Nova República), com foco em
**medidas, crises, causas e consequências** de cada governo e nas **transições presidenciais**.

**Entregável:** `APOSTILA_HISTORIA_BRASIL_ENEM_PAS3_2026.pdf` (também em `dist/`).
Relatório de qualidade: `docs/RELATORIO_QUALIDADE.md` · Fontes: `docs/FONTES.md`.

## Como reconstruir o PDF

Requisitos: Node 22+, o pacote `playwright` com Chromium instalado e `pdftoppm` (poppler) para as miniaturas.

```bash
node build.js --pdf            # gera dist/apostila.html e dist/APOSTILA_HISTORIA_BRASIL_ENEM_PAS3_2026.pdf
node build.js --pdf --check    # idem + verifica estouro de página, margens e sobreposição de rótulos
DPI=80 node build.js --pdf --png   # idem + PNG de cada página em dist/png/ (para inspeção)
```

## Estrutura do projeto

| Caminho | Conteúdo |
|---|---|
| `src/pages/p01.js … p24.js` | Uma página por arquivo (HTML em *template string*); edite o texto aqui |
| `src/lib/h.js` | Componentes: página, linha do tempo (`tl`, `vtl`), fluxograma (`flow`), mapa de sucessão (`succ`), cabeçalho de governo (`gov`), gráficos SVG (`barChart`, `lineChart`), barras (`hbars`), fotos |
| `src/lib/data.js` | Séries econômicas e eleitorais usadas nos gráficos (com fonte) |
| `src/styles.css` | Identidade visual e cores semânticas |
| `assets/fonts/` | Inter (SIL OFL 1.1) |
| `assets/img/` | Fotografias com licença verificada + `credits.json` (autor, licença, página de origem) |
| `build.js` | Monta o HTML, gera o PDF com Playwright/Chromium e roda as verificações |

## Cores semânticas

azul-escuro = instituições · âmbar = crises e mudanças de governo · vermelho = repressão ·
verde = direitos e democratização · roxo = contexto internacional · ciano = economia.

## Adicionar ou trocar uma foto

1. Coloque o arquivo em `assets/img/<slug>.jpg` (ou `.png`).
2. Registre autor, licença e página de origem em `assets/img/credits.json` (`curto` = crédito exibido sob a foto).
3. Os retratos usam o `slug` informado em `gov({ foto: '<slug>' })`; fotos de evento usam `photo('<slug>', { h, cap })`.
Sem arquivo, o retrato cai numa silhueta neutra (nenhuma imagem é gerada por IA).
