# Relatório de validação — Apostila Visual de Geografia ENEM 2026

Data de referência: 14–15/11/2026. Arquivo: `output/APOSTILA_GEOGRAFIA_ENEM_2026.pdf`.

## Resultado
- **39 páginas** (limite: 40), A4 vertical, ≈ 6 MB. Verificação automática: 0 páginas com texto cortado ou transbordando (margem mínima negativa de 0,4 mm em 2 páginas, imperceptível: dentro da área de segurança).
- Texto **selecionável e pesquisável** (fonte Inter embutida; `pdftotext` extrai o conteúdo). Há 17 objetos "Type 3" gerados pelo Chromium para texto com contorno (halo) nos mapas; continuam com texto Unicode.
- Auditoria visual: todas as 39 páginas foram renderizadas e inspecionadas; foram corrigidos transbordamentos, rótulos sobrepostos, legendas e proporções (ex.: figuras de inversão térmica/ilha de calor, mapa de blocos, gráfico da balança comercial, mapas geopolíticos, linha do tempo das ordens mundiais).

## Distribuição
| Módulo | Páginas | Conteúdo |
|---|---|---|
| Capa e guia | 1–2 | método, símbolos, incidência por tema, índice de mapas |
| A Física, relevo, clima | 3–9 (7) | placas, limites, estrutura geológica, solos, massas de ar, El Niño, hidrografia, litoral |
| B Domínios e biomas | 10–12 (3) | Ab'Saber × IBGE, vegetações, impactos e biomas do mundo |
| C Agrária e ambiente | 13–19 (7) | sistemas, Revolução Verde, insumos, manejo, fronteira, terra, povos |
| D Urbana e demografia | 20–24 (5) | urbanização, ambiente urbano, segregação, pirâmides, migrações |
| E Economia e globalização | 25–30 (6) | Taylor/Ford/Toyota, indústria, DIT, trabalho, blocos, energia e transportes |
| F Geopolítica | 31–34 (4) | ordens mundiais, organizações, conflitos datados, rotas e Brasil |
| G Cartografia | 35–37 (3) | escala, coordenadas e fusos, projeções, curvas de nível, anamorfose, SIG |
| Revisão e auditoria | 38–39 (2) | cadeias, distinções, números-chave; gabaritos, correções, fontes |

Desvio em relação ao plano: Física/clima/solos/biomas ficou com 10 páginas (A 7 + B 3) em vez de 9, para acomodar os desenhos obrigatórios; Econômica (6), Urbana (5), Agrária (7), Geopolítica (4), Cartografia (3) e capa+revisão (4, incluindo guia e gabaritos) seguem o plano.

## Recursos visuais
- **Mapas e cartogramas: 20** (todos sobre bases reais — placas, hidrografia, biomas, estados, países — mais o mapa decorativo da capa): placas; massas de ar*; rios voadores*; hidrografia; domínios (aproximação)*; biomas; fronteira agrícola*; migrações*; polos industriais; blocos econômicos; Guerra Fria; Mar da China Meridional; Ucrânia; Israel–Palestina; rotas e gargalos*; coordenadas e fusos; fusos do Brasil; 4 projeções com círculos de Tissot; cartograma de anamorfose (IBGE 2022). *=sobreposição esquemática sobre base real, sempre rotulada.
- **Diagramas e gráficos vetoriais: ≈ 70** (camadas da Terra, convecção, limites de placas, perfis de solo, ciclo das rochas, chuvas, El Niño, climogramas INMET, costas, vegetações, sistemas agrários, Revolução Verde, eutrofização, manejo, pirâmides IBGE, urbanização, revoluções industriais, DIT, cadeias globais, integração regional, matrizes energéticas, ONU, curvas de nível, escala, SIG, etc.).
- **Questões originais: 26**, com gabarito comentado e letras balanceadas (A–E); **tabelas comparativas** exigidas presentes (intemperismo×erosão, El Niño×La Niña, intensiva×extensiva, familiar×empresarial, Taylor×Ford×Toyota, populoso×povoado, terceirização×terciarização, Mercator×Peters, barlavento×sotavento, estrutural×conjuntural).

## Principais correções ao inventário
Manto sólido (não "oceano de magma"); agricultura familiar pelo Censo 2017 (77% dos estabelecimentos, 23% da área e do valor; sem "70% dos alimentos"); populoso × povoado padronizados; solos amazônicos (nem todos arenosos; latossolos nem sempre férteis); Mata Atlântica 12,4%; infiltração urbana ≈ 15%; Revolução Verde ≠ transgenia ≠ agricultura de precisão; resistência de pragas por seleção; seca de 2014–15 com causas múltiplas; energia com BEN 2026 (ano-base 2025); projeções sem atribuição ideológica; geopolítica com separação fato × reivindicação × status legal e data.

## Limitações e transparência
1. O arquivo `Texto colado(2).txt` **não existia** no ambiente; usou-se o inventário colado na mensagem.
2. As videoaulas **não foram assistidas**; nada é atribuído ao professor além do inventário. Complementos independentes estão marcados com ◆.
3. Não há vetor oficial acessível dos **domínios de Ab'Saber**: o mapa é aproximação a partir dos biomas IBGE/MMA (Araucárias, Cocais e Agreste esquemáticos).
4. Mapas de massas de ar, rios voadores, migrações, MATOPIBA/arco do desmatamento e rotas da Seda são **esquemáticos**. Curvas de nível usam relevo hipotético (rotulado).
5. Natural Earth traz limites "de fato", sem posição oficial; frentes de combate e controle efetivo **não** são desenhados.
6. Modais de transporte (CNT 2022) e proporção escudos/bacias são aproximações didáticas; percentuais de incidência por tema (Aprova Total) vêm do briefing e **não foram reauditados**.
7. Situações políticas e comerciais (Mercosul–UE, tarifas dos EUA, Rússia–Ucrânia, Gaza, BRICS, trégua EUA–China) valem para 14/11/2026 e mudam; conferir antes de citar.
8. O sandbox bloqueia IBGE/INMET/Natural Earth oficiais: estatísticas vieram da API SIDRA e de buscas/páginas oficiais via Firecrawl; dados vetoriais, de espelhos no GitHub.
9. Adesão de Timor-Leste à ASEAN (26/10/2025) e número de membros da OTAN (32) conferidos em fontes citadas em `data/sources.md`.

## Fontes consultadas
Ver `data/sources.md` e o rodapé de cada página.
