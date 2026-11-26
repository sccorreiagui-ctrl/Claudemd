# Relatório de qualidade — Apostila CTG, Geometria Analítica (PAS 3/UnB)

## Entrega
- `CTG_GEOMETRIA_ANALITICA_PAS3_2026.pdf`: **14 páginas A4 verticais** (conferido com `pdfinfo`), texto selecionável/pesquisável, gráficos vetoriais, rodapé "CTG | Geometria Analítica | Ponto e Reta / Circunferência | PAS 3/UnB | Página X/14" em todas as páginas.
- Distribuição: 01–02 teoria de ponto e reta · 03–06 exercícios R1–R7 · 07–09 teoria de circunferência · 10–14 exercícios C1–C8. **15 questões principais** resolvidas, cada uma com ideia geométrica, método, passos, resposta, verificação e armadilha.
- 35 diagramas SVG (todos usados); fontes, scripts e SVGs no repositório.

## Verificações executadas
1. **SymPy (`scripts/validate.py`)**: 105 verificações, 0 falhas — respostas das 15 questões, pés de perpendiculares, pontos de tangência, ponto médio de cordas, discriminantes, equação de C8 (`25x²−180x+180+16p`, `Δ=14400−1600p`), exemplos das páginas de teoria, treinos e autotestes.
2. **Diagramas (`scripts/diagrams.py`)**: cada ponto de apoio é calculado e conferido contra as equações antes de desenhar (a geração falha se um ponto não estiver na reta/circunferência); escala 1:1 nos dois eixos.
3. **Layout**: o build mede cada página (nenhuma com estouro) e ajusta o tamanho da fonte por página.
4. **Inspeção visual**: todas as 14 páginas foram renderizadas e vistas em pelo menos uma versão (as últimas alterações foram revistas só na folha de contato); o PDF final foi rasterizado e conferido numa folha de contato (60 dpi). Os diagramas alterados nas últimas rodadas foram revistos em folha própria.
5. **Matriz oficial**: o PDF da Matriz de Referências do PAS 3 (dez/2022) foi lido via ferramenta de scraping (acesso direto bloqueado pelo proxy). Confirmados textualmente MAT1 (retas, paralelismo, perpendicularismo), MAT2 (sistema 2×2 como interseção de retas), MAT4 (distâncias; equação da circunferência) e MAT7 (determinantes, áreas).

## Correções e decisões que mudam o que foi pedido (leia)
- **R4**: usado `C=(0,6)` conforme instrução. Confirmado por SymPy que o enunciado antigo `C=(2,7)` dava `H=M=(4,3)` (isósceles, `CA=CB`). Novo: `H=(2,2)`, `M=(4,3)`, `CH=2√5`; desenho e cálculos refeitos do zero.
- **R3**: o ponto `P=(1,4)` do diagnóstico se chamava `M`. Renomeei para `P`, porque `M` induz a leitura "ponto médio" — justamente a confusão que a apostila combate (o ponto médio real de `AB` é `(1,2)`). Coordenadas inalteradas.
- **Forma geral da circunferência**: a constante foi chamada de `D` (o material usa `C`, que colide com o centro `C`). Há nota na página 7.
- **Rótulos de origem**: "adaptado de padrão Uece 2024" (R6) e "URI-RS 2024" (R7) vêm do diagnóstico; **não consegui verificá-los** (sem ano/etapa/caderno/item). Mantidos como "padrão trabalhado", sem nenhum selo de prova oficial. Nenhuma questão é apresentada como oficial do PAS.
- **Acréscimos além do briefing** (preenchem espaço útil; podem ser removidos sem afetar o resto): treino-relâmpago de `m`/`n` (R2), treino de escolha de distância (R5), mapa "erro → exercício" e autoteste (pág. 6), mini-teste de leitura (pág. 7), seção 4 "equação a partir de condições geométricas" (pág. 8), exemplo curto Δ×d (pág. 9), roteiro e quadro "quantas tangentes" (pág. 13). Todos conferidos no SymPy.

## Limitações
- Os PDFs das aulas ("PV Matemática – L2…", "Gabarito…") **não estavam disponíveis; não foram consultados**. Os dois inventários foram usados como colados na conversa.
- O tamanho da fonte varia entre páginas (≈9,8–11,6 pt) porque o ajuste é automático; a página 6 é a mais densa (≈10 pt). Rótulos de eixos nos gráficos são pequenos (~5,5–7 pt equivalentes).
- Páginas 8, 9, 13 e 14 têm 22–36 mm de respiro vertical (distribuído entre blocos); poderiam receber mais conteúdo.
- Alguns rótulos de gráficos ainda tocam levemente linhas (ex.: `A(−1,3)` em R1); não afetam a leitura.
- O PDF tem ~7,7 MB (fontes Type 3 embutidas).
- Não foi feita revisão por professor humano; recomendo que o estudante resolva os exercícios antes de confiar em qualquer gabarito, inclusive nestes.
