# Relatório de validação · Apostila de Química para o ENEM 2026

**Entrega:** `APOSTILA_QUIMICA_ENEM_2026.pdf` (A4 vertical, **40 páginas**, 5,3 MB). Fonte editável: `src/pages/*.html` + `src/css/style.css` + `build/` (ver `README.md`).

## 1. Conferência técnica (automática)
| Item | Resultado |
|---|---|
| Páginas | 40 (limite: 40) |
| Estouro de conteúdo | 0 páginas (`build/out/layout_report.json`: `over = 0`, sem `hover` nem `clipped`) |
| Texto selecionável/pesquisável | sim (≈130 mil caracteres extraídos; 49 marcadores de navegação) |
| Imagens raster no PDF | 0 (tudo vetorial: HTML/CSS + SVG, renderizado por Chromium/Playwright) |
| Fontes | Source Sans 3 e Poppins (embutidas); DejaVu Sans, FreeSerif e KaTeX só como reserva de glifos |
| Macros não resolvidas (`{{ }}`, `\ce`, `?`) | 0 |
| Referências cruzadas “p. N” | todas geradas por macro; uma apontava para a página errada (ozônio) e foi corrigida |
| Gabarito | embutido nas alternativas (`data-ok`); o gabarito comentado é gerado a partir delas, então não pode divergir |

## 2. Conteúdo e recursos visuais
- **Blocos:** A polaridade e forças (p. 3–8) · B funções orgânicas (9–14) · C reações, tensoativos, polímeros, isomeria (15–19) · D soluções e estequiometria (20–24) · E matéria, separação, ambiente (25–28) · F físico-química (29–35) · G fundamentos (36–37) · revisão final (38–40) · capa e guia (1–2).
- **Números:** 163 figuras/esquemas únicos; 157 estruturas desenhadas por RDKit a partir de SMILES (65 com fórmula molecular validada automaticamente); ≈500 fórmulas químicas; 94 expressões matemáticas; 29 tabelas; **36 testes originais** com gabarito comentado, 9 respostas em cada letra A–D (a primeira versão tinha 24 de 36 em “B”; foi redistribuída).
- **Diagramas obrigatórios do pedido:** 6 moléculas com dipolos (p. 4) · fluxograma polar/apolar (5) · bicamada fosfolipídica (8) · tabela fosfolipídio × sabão × detergente × micela × bicamada (8) · cartões de funções orgânicas e comparações (10–12) · multifuncionais (13) · reações orgânicas (15–16) · adição × condensação (18) · isomeria (19) · destilação simples × fracionada (26) · fluxograma da ETA (27) · gráfico de aquecimento (25) · biomagnificação (28) · energia de ativação com/sem catalisador (29) · endo/exotérmica (32) · concentração × tempo no equilíbrio (30) · curva de solubilidade (20) · meia-vida (35) · pilha detalhada e pilha × eletrólise (33–34).
- **Selo “complemento”** marca o que não está no inventário: estequiometria completa (limitante, pureza, rendimento), contraste de bário, ΔG e calorimetria, tampão de Henderson–Hasselbalch.

## 3. Auditoria científica (correções sobre o inventário e sobre rascunhos)
London existe em **todas** as moléculas · cis/trans: polaridade depende dos ligantes · 2ⁿ estereoisômeros é **máximo** (meso) · catalisador não desloca o equilíbrio · centrifugação separa heterogêneas · biodegradabilidade de detergente sem regra universal · Cl (3,16) > N (3,04) e H (2,20) ≈ P (2,19) por Pauling · acidez: metanol ≈ água · basicidade de aminas: ordem é tendência, com exceções · metais pesados não vão só para gordura (Hg→proteínas, Pb→ossos) · chuva normal pH ≈ 5,6 · coligativas só com soluto não volátil e solução diluída · criolita baixa o P.F. na produção de Al · carvão ativado só em tratamento avançado · K_w e “pH 7 neutro” dependem da temperatura.
**Encontrados nesta última passada:** ordem de P.E. na p. 14 colocava amina acima de cetona, contra o próprio gráfico da página (corrigido); mapa na p. 10 remetia o ozônio à página errada; ícone de nitração com ligação N=O ilegível (HNO₃ passou a texto); rótulos sobrepostos ou cortados em 9 figuras (geometrias, escalas de pKa/pKb, adrenalina e capsaicina, estados da matéria, chuva ácida, efeito estufa, energia de ativação, perturbações do equilíbrio, cromatografia).

## 4. Fontes
Inep (Matriz de Referência do Enem; provas e gabaritos) · Raio-X ENEM SAS (Química, 599 itens, 2009–2025; PDF de 2026-04) · inventário de duas videoaulas fornecido no pedido (síntese do NotebookLM). Reportagens consultadas só para contexto, sem uso de números delas.

## 5. Limitações (sem maquiagem)
1. **Os vídeos não foram assistidos.** O conteúdo vem do inventário colado no pedido (o arquivo `Texto colado.txt` não existia). Se o inventário errou ou omitiu algo, a apostila herda isso, exceto onde a auditoria corrigiu.
2. **Priorização:** só o top 10 do Raio-X é público. Polaridade, forças intermoleculares e solubilidade **não aparecem nele**; abrem a apostila por serem pré-requisito, decisão pedagógica e não dado de incidência. O percentual 35,1% do top 10 vem do próprio Raio-X.
3. **Revisão feita por IA:** a inspeção visual das 40 páginas foi feita sobre PNGs renderizados, não por um professor. Recomendo revisão humana, principalmente dos valores numéricos (potenciais, K, entalpias arredondados para estudo) e dos 36 testes.
4. **Regras de ensino com exceções:** fila de descarga, “n.º de O − n.º de H” dos oxiácidos, regra de bolso de solubilidade de sais e sentido da hidrólise. Estão sinalizadas no texto.
5. **Tamanho da letra:** boxes e tabelas usam 9,4–11 px (≈ 7–8,5 pt) para caber em 40 páginas. É denso para leitura prolongada em papel.
6. **Estética de estruturas:** o grupo sulfonato (p. 17) e a ligação S=O saem pequenos no desenho RDKit; estão legíveis, mas não são perfeitos.
7. Dados de incidência de outras fontes não são comparáveis ao Raio-X e não foram usados nos números.
