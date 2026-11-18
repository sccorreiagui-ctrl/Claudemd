# Relatório de qualidade — Apostila CTG (Complexos e Polinômios · PAS 3)

## Entrega
* **PDF:** `dist/CTG_MATEMATICA_COMPLEXOS_POLINOMIOS_PAS3_2026.pdf` — **40 páginas A4**, 20 + 20 (p. 1–20 Números Complexos; p. 21–40 Polinômios). Texto selecionável/pesquisável; fontes embutidas (Inter e KaTeX); figuras vetoriais.
* **Fontes-fonte:** HTML/CSS por página, scripts de figuras, scripts de verificação e de geração (ver `README.md`).

## Conteúdo
* **Parte I (p. 1–20):** conjuntos e unidade imaginária; potências de *i*; forma algébrica; igualdade; operações; conjugado; divisão; plano de Argand-Gauss; vetores, distâncias e lugares geométricos; módulo; revisão trigonométrica (tabela de 0° a 360°); argumento e quadrantes; forma trigonométrica; rotações; produto/quociente polar; 1ª e 2ª fórmulas de De Moivre; raízes da unidade e polígonos; revisão (mapa de decisão, formulário, erros, teste).
* **Parte II (p. 21–40):** definição e anatomia; grau; valor numérico, raiz e gráfico; identidade; operações; fatoração; divisão pela chave; quocientes/restos/parâmetros; Teorema do Resto e D'Alembert; Briot-Ruffini; divisões sucessivas; raízes racionais; T.F.A. e decomposição; multiplicidade e gráficos; raízes conjugadas; Girard (2º/3º graus e graus superiores); equações de grau 2–4 e biquadráticas; revisão final.
* **Cobertura das habilidades:** MAT8 (p. 9–11, 15), MAT9 (p. 1–19), MAT10 (p. 21–25, 33–37), MAT11 (p. 26–32), MAT12 (p. 38–39).
* **Integração das duas partes:** 4 exemplos marcados «Integra Complexos + Polinômios» (p. 35, 37, 38, 39: par conjugado + Girard; *z³+1* por fatoração e por forma polar; *x⁴+4* por três caminhos) e pontes explícitas nas páginas de cada módulo; os exercícios 31–32 também integram as partes.

## Quantidades (reais)
| Item | Meta do pedido | Entregue |
|---|---|---|
| Exemplos resolvidos numerados (enunciado → estratégia → resolução → resposta → verificação) | ≈ 24 | **99** (curtos, 1–2 por assunto; excedem a meta) |
| Exercícios numerados, com gabarito explicado | ≈ 30 | **32** (C/E: 9; tipo B: 19; «Resolva»: 4) |
| …em formato do PAS (C/E ou B) | ≥ 12 | **28** |
| Itens PAS comentados (extras, autorais) | — | 12 blocos (15 afirmações) |
| Treinos rápidos (sem numeração, com resposta) / testes rápidos / recordações ativas | — | 13 / 34 / 34 |
| Formulários de revisão | 2 | 2 (p. 20 e p. 40) |
| Figuras | 18 + 16 temas | 40 figuras: 37 SVG vetoriais gerados por código (geometria, diagramas, grades de Ruffini, divisão pela chave, fluxogramas) + 3 gráficos de polinômios gerados por matplotlib a partir das funções reais |

**Distribuição de níveis dos 32 exercícios:** N1 = 11 (34%), N2 = 16 (50%), N3 = 5 (16%) — a meta era 40/40/20; o desvio é para o nível intermediário.

## Correções matemáticas realizadas
* **Divisão do inventário:** *6x⁴ − 3x³ + 3x² − x + 1 ÷ (2x² + x − 3)* tem *Q = 3x² − 3x + 15/2* e *R = −(35/2)x + 47/2* (p. 27, com a conferência *D·Q + R = P*; o par do inventário foi mostrado como incorreto).
* Radicais com fatores negativos; parte imaginária é *b* e não *bi*; zero é real e não tem argumento; argumento principal em [0, 2π); divisão exige denominador não nulo; De Moivre com expoente negativo exige base não nula; *wⁿ = z* tem *n* raízes distintas (e o caso *z = 0* é tratado à parte); a soma das raízes de *wⁿ = z* é nula **só para n ≥ 2**; casos degenerados *n = 1* e *n = 2*.
* Grau de constante e do polinômio nulo; grau do produto/da soma; condição *R ≡ 0 ou gr R < gr D* e caso *gr P < gr D*; T.F.A. com grau ≥ 1 e raízes contadas com multiplicidade; raízes conjugadas só com coeficientes reais; Teorema das Raízes Racionais como *candidatos* (e *a₀ = 0*); multiplicidade e gráfico apenas para raízes reais de polinômios reais; biquadráticas devem voltar a *x*.
* Tipos de erro encontrados **durante a produção** e corrigidos: expoente de dois dígitos nas figuras; rótulos sobrepostos; a conferência do Exemplo 65 (quociente da divisão por *2x − 4*), detectada pelo script de verificação; fórmula do produto das raízes de *zⁿ = k*.

## Verificações executadas
* `verify/verify.py`: **216 verificações simbólicas** (SymPy) de exemplos, treinos, itens e gabaritos de todas as páginas (inclui a tabela trigonométrica, conversões polar↔algébrica, De Moivre, raízes, Ruffini, chave, Girard, multiplicidade, biquadráticas).
* `verify/verify_figs.py`: **27 verificações dos dados das figuras** (grade de Ruffini e passos da divisão pela chave contra a divisão simbólica; vértices dos polígonos contra as raízes de *zⁿ = k*; argumentos dos quadrantes; sinais do polinômio perto de cada raiz; distâncias e produtos).
* Controle de layout: relatório por página (nenhuma página em estouro; verificação 20/20 por módulo; 40 páginas A4).
* Inspeção visual: as 40 páginas foram renderizadas em imagem e conferidas em lotes (cortes, sobreposições, alinhamento); defeitos achados foram corrigidos e as páginas regeneradas.

## Fontes utilizadas
Inter (texto), KaTeX (matemática, incluindo KaTeX_AMS para ℂ ℝ ℚ ℤ ℕ), geradas no PDF como fontes embutidas.

## Limitações e avisos
1. **Arquivo de referência:** `Texto colado(20261118-003855).txt` **não existia** no ambiente; o inventário foi usado a partir do texto colado na mensagem. Nada foi dito sobre ter assistido aos vídeos.
2. **Matriz oficial e Saber PAS:** os domínios do Cebraspe foram bloqueados pela política de rede do ambiente (HTTP 403) e uma consulta via Firecrawl falhou por falta de créditos. A apostila usa, portanto, as descrições de MAT8–MAT12 fornecidas no pedido; **não foi possível conferir o texto oficial** nem localizar o item de 2014 citado. Nenhuma questão oficial, estatística de incidência ou item da banca foi reproduzido ou inventado; todos os exercícios são autorais.
3. Algumas figuras densas (p. ex. painéis da divisão pela chave, p. 27, e os gráficos da p. 34) têm texto de ~6 pt: legíveis em A4, mas melhores na tela do que numa impressão reduzida.
4. Os gabaritos ficam logo abaixo de cada bloco de exercícios (não numa página separada), o que facilita a conferência mas exige disciplina de não olhar antes.
5. O número de exemplos (99) excede a meta do pedido (≈ 24); optou-se por preservar a progressão didática e as verificações, em vez de cortar exemplos fundamentais.
