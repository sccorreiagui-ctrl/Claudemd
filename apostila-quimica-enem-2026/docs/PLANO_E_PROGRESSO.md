# Plano editorial e progresso (arquivo de trabalho)

Projeto: `apostila-quimica-enem-2026/` · Saída: `APOSTILA_QUIMICA_ENEM_2026.pdf` (40 páginas A4)
Build: `python3 build/build.py [--png DPI] [--pages 3,4]` (requer `npm install`, `pip install rdkit pymupdf fonttools brotli`, Playwright/Chromium)

## Fluxo técnico
- Páginas: `src/pages/pNN_chave.html` (cabeçalho em comentário: key, block, title). Corpo = HTML do `.pg-body`.
- Macros: `\ce{H2SO4}` (química, build/chem.py) · `$...$`/`$$...$$` (KaTeX, só matemática) · `{{fig:nome}}` (build/figs_*.py, registro com @fig) · `{{icon:water|lipid|func|leaf|react|alert|info|star|calc}}` · `{{pg:chave}}`.
- Moléculas: build/mol.py (RDKit; SMILES + SMARTS de grupos; `formula=` valida legenda). Esquemas de reação: `scheme()`.
- SVG: build/svglib.py (SVG, Axes, tw() com métrica real da fonte). Cores semânticas em C{} / CSS vars.
- Auditoria: build/render_pdf.js grava build/out/layout_report.json (over=estouro, free=sobra em px).

## Mapa das 40 páginas
1 capa · 2 como usar (legenda, prioridades Raio-X, conexões)
A (azul) 3 eletronegatividade/ligações · 4 geometria e polaridade (6 moléculas) · 5 fluxograma polar/apolar + hidro/lipofílico + cadeia apolar · 6 forças intermoleculares + gráfico PE hidretos · 7 solubilidade/miscibilidade · 8 membrana, sabão, detergente, micela
B (roxo) 9 carbono/hidrocarbonetos · 10 álcool/fenol/enol/éter · 11 carbonilas, ácido, éster · 12 nitrogenadas e halogenadas · 13 multifuncionais · 14 propriedades físicas e ácido-base orgânico
C (laranja) 15 substituição/adição/eliminação · 16 oxidação/esterificação/hidrólise/saponificação · 17 lipídios, sabões, detergentes · 18 polímeros · 19 isomeria
D (ardósia) 20 soluções I · 21 soluções II (diluição, mistura, titulação) · 22 estequiometria I · 23 estequiometria II · 24 gases + coligativas/osmose
E (verde) 25 matéria/estados/gráfico aquecimento · 26 separação de misturas + destilações · 27 ETA + chuva ácida/ozônio · 28 efeito estufa, eutrofização/DBO, biomagnificação
F (laranja) 29 cinética · 30 equilíbrio · 31 ácido-base/pH/tampão/Kps · 32 termoquímica · 33 pilhas/corrosão · 34 eletrólise · 35 radioatividade
G 36 atomística + tabela periódica · 37 inorgânicas, tipos de reação, MACHO
R 38 fórmulas essenciais · 39 mapa conceitual + tabela rápida de funções · 40 confusões, gabaritos comentados, referências

## Dados do Raio-X SAS (Química, 599 itens, 2009-2025; só top 10 é publicado)
Funções orgânicas 36 (6,01%) · Reações orgânicas 28 (4,67%) · Cinética 25 (4,17%) · Pilhas 19 (3,17%) · Separação de misturas 19 (3,17%) · Tecnologias ambientais 18 (3,01%) · Controle de poluição 17 (2,84%) · Concentração de soluções 17 (2,84%) · Poluição da água 16 (2,67%) · Tipos de reações químicas 15 (2,50%). Soma top10 = 210 itens = 35,1%.
Limitação: polaridade/forças intermoleculares/solubilidade NÃO aparecem no top 10 publicado (priorizados por serem pré-requisito transversal, a pedido do usuário). Biologia (Raio-X): Bioquímica 18 itens, Biologia celular 18.

## Correções feitas sobre o inventário NotebookLM (auditoria)
London em todas as moléculas · cis/trans polaridade depende dos ligantes · 2^n é máximo (meso) · catalisador não desloca equilíbrio · centrifugação separa heterogêneas · biodegradabilidade de detergente não por regra única · eletronegatividade (Cl>N por Pauling; H≈P) · metais pesados não vão só para gordura (Hg→proteínas, Pb→ossos; DDT→lipídios) · oxiácidos: H ionizáveis · fila de descarga ("D+" = demais cátions) · basicidade de aminas (exceções) · acidez (metanol≈água) · coligativas: soluto não volátil, solução diluída, i ideal · fusão "sem resíduos" é simplificação · carvão ativado só em tratamento avançado · chuva normal pH≈5,6 · criolita baixa o P.F. na produção de Al.

## Progresso
(ver lista de tarefas da sessão; atualizar abaixo)
- [x] Pipeline técnico validado (página de teste)
