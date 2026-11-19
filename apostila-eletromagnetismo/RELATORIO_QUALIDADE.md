# Relatório de qualidade — Apostila CTG de Eletromagnetismo (PAS 3 / UnB 2026)

**Entrega:** `CTG_ELETROMAGNETISMO_PAS3_UNB_2026.pdf` (28 páginas A4, 1,95 MB, texto pesquisável, diagramas vetoriais) +
projeto editável neste diretório (`README.md` explica como regenerar tudo com `bash scripts/rebuild_all.sh`, ~2,5 min).

## 1. Páginas produzidas e conteúdo coberto

| Módulo | Páginas | Conteúdo |
|---|---|---|
| I · Fundamentos | 1–3 | ímãs, polos inseparáveis e linhas de campo; materiais (domínios, para/dia/ferromagnetismo, Curie); campo terrestre, bússola, vetores |
| II · Fontes de campo | 4–9 | Oersted e 1ª regra da mão direita; fio longo; superposição (dois fios, quatro fios, três fios); espira; solenoide e eletroímã; Lei de Ampère (+ toroide) |
| III · Força magnética | 10–15 | força sobre carga; orientação (produto vetorial; regras da mão direita, do tapa e esquerda); movimento circular, espectrômetro, ciclotron; reta/círculo/hélice e trabalho nulo; força sobre fios (inclusive fio em arco); interação entre fios |
| IV · Indução | 16–22 | fluxo (ângulo com a normal); Faraday; gráficos Φ(t)→ε(t); Lenz (método em 6 passos); quatro casos do ímã e anel parado; haste móvel; haste em plano inclinado e velocidade terminal |
| V · Dispositivos | 23–26 | motor (torque, comutador, força contraeletromotriz); gerador e corrente alternada; transformador; transmissão em alta tensão, ressonância magnética, captador, levitação, linha do tempo |
| VI · Consolidação | 27–28 | fluxograma de decisão, formulário com condições de uso, quadro das regras, 10 erros que mais custam pontos; mini-simulado (10 itens) com gabarito comentado |

**Matriz do PAS 3 (Cebraspe)** — itens de Física lidos na matriz: *Magnetismo: força e campo magnético; propriedades magnéticas dos
materiais* → p. 1–15; *Eletromagnetismo: leis de Ampère, Faraday e Lenz; geradores, transformadores e motores; ressonância magnética*
→ p. 9, 16–26; *História da eletricidade e do magnetismo* → p. 1, 4, 26. A p. 26 relaciona os objetivos educacionais da matriz
(CN1, CN3, CN4, CN5, CN9, CN10, CN11, CN12) que mobilizam o tema.

## 2. Números (gerados por `scripts/stats.py`)

| Item | Quantidade |
|---|---|
| Exemplos resolvidos (situação, esquema, dados, fenômeno, método, cálculo, resultado, verificação) | **21** (5 fundamentais · 14 intermediários · 2 avançados) |
| Exercícios de página (E1–E24, com respostas no pé da página) | **24** (8 · 12 · 4) |
| Itens do mini-simulado (Q1–Q10, p. 28, com gabarito comentado) | **10** (4 · 5 · 1) |
| Problemas integradores resolvidos em caixa (p. 15, quadrado de fios p. 6) | 2 (fora da contagem de níveis) |
| Figuras SVG vetoriais distintas | **68** (61 com legenda numerada) — nenhuma imagem raster no PDF |
| Expressões matemáticas (KaTeX) | 1 756 |

Distribuição de nível no total de 55 itens de prática: **31 % fundamental · 56 % intermediário · 13 % avançado** (a meta do projeto era 40/40/20).

## 3. Recursos visuais (todos originais, gerados por código)

Ímã com linhas internas/externas e bússolas; divisão do ímã; domínios; campo terrestre (dipolo equivalente); 1ª regra da mão
direita e tríade da força (v × B); fio, corte transversal e perfil B(r); superposição (dois, três e quatro fios); espira (faces
Norte/Sul, regra do relógio); solenoide e seu perfil de campo; circulações de Ampère; quatro casos de F = q v × B e exercício de seis
painéis; trajetórias reta/circular/helicoidal (com raio *r* e passo *p*); espectrômetro; fio em campo e fio em arco; fios paralelos e
espira perto de fio (forças à escala); fluxo (θ com a normal; casos 0°, 60°, 90°, 180°); Faraday (bobina, anel de Faraday); gráficos
Φ(t) e ε(t); Lenz (algoritmo em 6 passos, **quatro casos do ímã**, anel parado em quatro casos); haste móvel e leitura de
Lorentz; rampa (vista lateral com forças, vista superior, curva v(t)); motor, gerador e comparação motor × gerador; tensão alternada;
transformadores elevador e abaixador; cadeia de transmissão; RM, captador de guitarra, levitação; fluxograma de decisão e mapa dos
fenômenos.

## 4. Complementações em relação ao inventário

Exemplo de quadrado de fios (80 µT) e exercício de três fios com geometria definida (p. 6); toroide e quadro “quando a lei de Ampère
dá o campo diretamente” (p. 9); aceleração por tensão e ordens de grandeza de raios (p. 12); trabalho nulo com seu escopo (p. 13);
força sobre fio em arco = corda (p. 14); espira retangular perto de um fio, com resultante 7,5×10⁻⁵ N (p. 15); gráficos de fluxo e FEM
(p. 18); convenção de sinais de Φ e ε (p. 19); conferência de geometria antes de usar BLv, leitura de Lorentz e polaridade da haste
(p. 21); força contraeletromotriz do motor (p. 23); valor eficaz (p. 24); perdas na transmissão com números (p. 26); formulário com
condições de uso e lista dos 10 erros (p. 27).

## 5. Correções e cuidados científicos

1. **Três fios (inventário: “i₁ = 24 A ou valor equivalente conforme a simetria exata”, sem dedução).** Foi definida uma geometria
   explícita (AC = CD = 10 cm; P a 5 cm de C e de D; A e D com 24 A entrando). Por superposição vetorial a corrente em C é **16 A,
   entrando** (verificada por Biot–Savart numérico). Não se afirma que seja a questão original, cujo enunciado não estava acessível.
2. **Haste em rampa (inventário misturava expressões).** Com B vertical: ε = BLv cos α; F = BIL é *horizontal* e só F cos α atua ao
   longo da rampa; v_term = mgR sen α /(B²L² cos² α) e τ = mR/(B²L² cos² α). Variante B ⟂ rampa também resolvida (E21). Conferido por
   integração numérica da equação do movimento (produtos vetoriais) e por balanço de energia.
3. Lenz: não se usa “o campo induzido sempre se opõe ao campo externo”; ele se opõe à **variação** do fluxo (p. 19–20).
4. Ampère magnetostática vale para correntes estacionárias e qualquer caminho fechado; só o *cálculo* de B depende de simetria (p. 9).
5. Origem microscópica: não se reduz tudo ao spin — há momento orbital e interação de troca/domínios (p. 2).
6. Campo terrestre: nome geográfico × polaridade física do dipolo equivalente; inclinação ≈ 10° apresentada como variável no tempo (p. 3).
7. Trabalho nulo vale para a força magnética sobre carga pontual; em motores a energia vem da fonte (p. 13, 23).
8. Fluxo com ângulo na normal; fluxo constante não gera FEM; N espiras (fluxo concatenado); BLv só com geometria adequada;
   transformador não funciona com CC estacionária; RM não usa radiação ionizante (p. 16–17, 21, 25–26).
9. Atribuição de mnemônico a pessoa específica (regra da mão esquerda) foi substituída pela denominação padrão (Fleming), por não
   ser verificável.

## 6. Verificações executadas

| Verificação | Resultado |
|---|---|
| `scripts/validate_physics.py` — 89 conferências independentes (Biot–Savart numérico para fio, espira, solenoide, superposição, Ampère; RK4 da força de Lorentz; integração de I dℓ×B; fluxo/Faraday/Lenz com fluxo de sinal e dipolo; haste e rampa; torque por Σ r×F; gerador por derivada numérica; transformador, perdas, Larmor) | **89 OK, 0 falhas** (`report/verificacoes.txt`) |
| 33 `assert` de geometria nos geradores de figuras (sentido de B, F = q v×B, I L×B, B induzido, ε de movimento) | passam; as figuras não são geradas se a regra for violada |
| Folga/estouro de cada página (mm, por medição no Chromium) | 28/28 páginas sem estouro |
| `scripts/check_pdf.py` — 28 páginas A4; rodapé exato `CTG · FÍSICA · ELETROMAGNETISMO · ASSUNTO · NN/28` em todas; ≥ 673 palavras selecionáveis por página; metadados e marcadores; fontes incorporadas; **nenhuma fonte de fallback**; nenhuma imagem raster | **APROVADO** (`report/checagem_pdf.txt`) |
| Revisão visual das 28 páginas em 110 dpi + ampliações de cerca de 12 figuras (regras da mão direita, produtos vetoriais, Lenz, rampa, trajetórias) | defeitos encontrados foram corrigidos (item 7) |
| Conferência manual de cada exemplo, resposta e gabarito contra o cálculo | feita página a página |
| Matriz do PAS 3 (Cebraspe) | lida por raspagem de `pas3_matriz_referencias.pdf`; itens de Física e objetivos CN citados conferidos |

## 7. Defeitos de composição encontrados na revisão e corrigidos

Equações cortadas na lateral (p. 21); fórmulas que sumiam do cartão por falha ao interpretar matemática em atributos (p. 12–13, e
títulos de caixa nas p. 9, 12, 19, 21); **caixa-alta alterando símbolos** (ε virava Ε, v virava V em títulos); legendas riscadas ou
sobrepostas por elementos (p. 2, 13, 15, 21, 22); rótulos fora do quadro e setas atravessando o fio (p. 15); texto sobre a aresta da
rampa (p. 22); glifos fora das fontes do livro (⟂, ✓, subíndices Unicode) que o navegador trocava por fontes de fallback.

## 8. Limitações e riscos (leia antes de distribuir)

- **Fontes originais inacessíveis.** Os 22 documentos/vídeos do NotebookLM e o arquivo de texto citado no briefing não estavam
  disponíveis; o único insumo foi o inventário colado. Nada foi conferido contra o Guia do PAS, as provas ou as videoaulas, e
  **nenhuma questão oficial foi reproduzida** — todos os exercícios são autorais e assim declarados (p. 28).
- **Desvios das metas:** 21 exemplos (meta 16–18) e níveis 31/56/13 (meta 40/40/20). O excesso de exemplos decorre de manter um
  exemplo por página de conteúdo; o déficit de itens avançados é real: o nível avançado está concentrado em E6, Ex. 9, Ex. 18,
  E13, E15, E21 e Q9.
- **Sem revisão humana independente.** A conferência visual e numérica foi feita pelo mesmo autor das páginas; a validação numérica
  usa modelos idealizados e constantes arredondadas (e = 1,6×10⁻¹⁹ C etc.). Recomenda-se leitura por um professor de Física antes de
  circular o material, e impressão de prova para checar legibilidade das fontes pequenas (rótulos e legendas a partir de ≈ 6 pt).
- **Densidade.** O limite de 28 páginas obrigou a texto compacto e fontes pequenas nas caixas; não há indutância, circuitos RL/RLC,
  corrente de deslocamento, efeito Hall (só menção) nem derivação de Biot–Savart — fora da lista de itens da matriz de Física lida.
- Sem estatísticas de incidência por tema (não havia fonte verificável). PDF sem marcação de acessibilidade (PDF/UA); a cor nunca é
  a única informação, mas não houve teste com simuladores de daltonismo.
