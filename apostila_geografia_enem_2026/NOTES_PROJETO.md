# NOTAS DO PROJETO — Apostila Visual de Geografia ENEM 2026

> Arquivo de trabalho (memória do projeto). Atualizado ao longo da produção.
> Data de referência da produção: 14/nov/2026.

## Situação dos insumos
- O anexo `Texto colado(2).txt` **não existe no filesystem**; o conteúdo integral do inventário NotebookLM veio **inline** na mensagem do usuário e foi usado como fonte pedagógica principal.
- Não há acesso a vídeos. Nada é atribuído ao prof. Pedro Assaad além do que consta no inventário. Em cada módulo diferenciamos: **[Inventário]** (conteúdo extraído da síntese) × **[Complemento]** (verificado independentemente).

## Rede / ferramentas
- Hosts acessíveis por curl: `raw.githubusercontent.com`, `pypi.org`, `registry.npmjs.org`. IBGE, Natural Earth oficial, Wikipedia, INMET etc. **bloqueados** no sandbox.
- Estatísticas oficiais foram obtidas via Firecrawl (SIDRA API, EPE, IBGE news) — ver abaixo.
- Python venv: `/tmp/claude-0/-home-user-Claudemd/6ef9e843-2bbf-50f0-912b-d4e67e910ead/scratchpad/venv` (geopandas 1.2, matplotlib 3.11, shapely 2.2, pyproj 3.8). requirements em `requirements.txt`.
- PDF: Node global `playwright` 1.63 + Chromium (`/opt/pw-browsers`). Render de páginas: `pdftoppm` (poppler).
- Fonte Inter instalada no sistema (e Inter Display).

## Dados geoespaciais (reais) — data/raw (re-baixar com `python3 src/fetch_data.py`)
| Camada | Fonte | Observação |
|---|---|---|
| Países 110m/50m/10m, estados BR (50m admin_1), rios, lagos, disputed lines, maritime indicator (CHN), lugares | Natural Earth (nvkelso/natural-earth-vector, domínio público) | NE inclui a Crimeia no polígono da Rússia (de facto) → tratado explicitamente nos mapas |
| Limites de placas (classes OSR/CRB, OTF/CTF, SUB/OCB/CCB) | Bird (2003) PB2002 (espelho fraxen/tectonicplates) | steps com `STEPCLASS` |
| Biomas | IBGE/MMA – Mapa de Biomas do Brasil 1:5.000.000 (shapefile `biomas_2005`) | 6 polígonos; áreas: Amazônia 4,20 mi km², Cerrado 2,04, Mata Atlântica 1,12, Caatinga 0,83, Pampa 0,17, Pantanal 0,15 |
- **Domínios morfoclimáticos de Ab'Saber: não há vetor oficial acessível** → mapa derivado dos biomas IBGE (aproximação por correspondência) e **rotulado como tal**; Araucárias/Mares de Morros/faixas de transição são representados de forma esquemática onde não houver dado.
- Linha dos nove traços: NE "maritime_indicator_chn" (aprox.; a China nunca publicou coordenadas).

## Estatísticas verificadas (usar exatamente estes números)
- **Censo Agro 2017 (IBGE)**: agricultura familiar = 3.897.408 estabelecimentos (77%), 80,9 mi ha (23% da área), 23% do valor da produção (R$ 107 bi de R$ 465 bi), 67% do pessoal ocupado. Estabelecimentos ≥ 1.000 ha: 51.203 = 1,0% dos estab. e 47,6% da área. (<10 ha ≈ 50% dos estab. e ~2,3% da área: *conferir antes de usar*).
- **Censo 2022 (IBGE)**: ≈ 203,1 mi hab. (SIDRA 9514: 203.080.756; IBGE "Comentários": 203.062.512); 65+ = 10,9% (2010: 7,4%); 60+ = 32.113.490 (15,6%); índice de envelhecimento 55,2 (2010: 30,7); idade mediana 29 → 35; TFT 1,55 (2022); taxa de urbanização 87,4% (177,5 mi urbana / 25,6 mi rural); 61,1% em concentrações urbanas.
- **Pirâmides**: `data/processed/piramide_etaria_ibge.json` (SIDRA t200/1980 e t9514/2022; somas conferem com totais oficiais).
- **Urbanização 1970–2010** (SIDRA t202): 55,9 / 67,6 / 75,6 / 81,2 / 84,4 %; 2022 = 87,4% → `data/processed/urbanizacao_ibge.json`.
- **Climogramas** (INMET 1991–2020): `data/processed/climogramas_inmet_1991_2020.json` (Manaus, Brasília, Petrolina, Porto Alegre).
- **BEN 2026 (EPE, ano-base 2025)**: Oferta Interna de Energia 328,5 Mtep; renováveis 49,4%. Fontes: petróleo e der. 33,7; biomassa da cana 15,8; hidráulica 10,7; gás natural 10,3; licor preto e outras renováveis 8,9; lenha e carvão vegetal 8,3; carvão mineral 4,5; eólica 3,0; solar 2,7; urânio 1,3; outras não renováveis 0,8.
  Matriz **elétrica** 2025: renováveis 86,8% (não renováveis 13,2%): hidráulica 51,2; eólica 14,9; solar 11,4; biomassa 8,4; gás natural 7,5; carvão e der. 2,2; nuclear 2,0; der. de petróleo 1,5; importação 0,9. (BEN 2025/ano-base 2024: renováveis 88,2% na matriz elétrica; ~50% na matriz energética.)
- **Transportes (CNT, Boletim Unificado mar/2022, t·km útil)**: rodoviário ≈ 64,9%; ferroviário ≈ 14,95%; aquaviário ≈ 15,7%; dutoviário+aéreo ≈ resíduo (~4,5%). Fontes divergem por ano/metodologia (ex.: CNT 2013: 61,1/20,7…). Citar ano e fonte.
- **Mata Atlântica**: restam **12,4%** da cobertura florestal original em florestas maduras >3 ha (SOS Mata Atlântica/INPE, Atlas) — *corrige* "3% a 10%" do inventário.
- **REGIC 2018 (IBGE)**: 5 níveis (Metrópoles, Capitais Regionais, Centros Sub-Regionais, Centros de Zona, Centros Locais); 15 metrópoles (1A SP; 1B RJ e Brasília; 1C demais).
- **Geopolítica (ref. out–nov/2026)**: Mercosul–UE assinado 17/01/2026 (Assunção); aplicação provisória desde 01/05/2026 (UE + AR, BR, PY, UY); entrada em vigor definitiva pendente do consentimento do Parlamento Europeu (consulta ao TJUE). BRICS: Brasil, Rússia, Índia, China, África do Sul + Egito, Etiópia, Irã, EAU (2024) + Indonésia (jan/2025); Arábia Saudita listada pela presidência indiana 2026 (status tratado de modo distinto por fontes); Índia preside em 2026. Guerra Rússia–Ucrânia (invasão em larga escala desde 24/fev/2022) segue sem acordo de paz em out/2026. Gaza: cessar-fogo de out/2025 frágil. Crimeia: anexação pela Rússia em 2014 **não reconhecida** (AGNU Res. 68/262).

## Correções ao inventário (registrar no relatório)
1. Manto não é líquido (é sólido que flui lentamente); "oceano de magma" corrigido.
2. Agricultura familiar ≠ "70% dos alimentos": usar dados do Censo Agro 2017.
3. Populoso/povoado: inventário (seção 3.1) está correto no texto mas verificar inversões em outros trechos — padronizar: POPULOSO = população absoluta; POVOADO = densidade.
4. Solos amazônicos: predominam Latossolos/Argissolos ácidos e pobres (não "todos arenosos"); latossolos nem sempre férteis.
5. Mata Atlântica 12,4% (não 3–10%).
6. Transgênicos ≠ Revolução Verde inicial (anos 1940–70); transgenia difundida a partir de 1996.
7. Projeções: propriedades matemáticas ≠ ideologia; Mercator (conforme) × Peters/Gall-Peters (equivalente).
8. "Aquífero Alter do Chão = maior do mundo": estimativas variam; tratar como hipótese/estimativa.
9. Seca 2014–15 no Sudeste: bloqueio atmosférico; relação com Amazônia é hipótese em pesquisa (não causa única).
10. Crimeia/Xinjiang/Israel-Palestina: reescrever com fatos documentados × reivindicações × status jurídico.

## Plano de páginas (meta 38; limite 40)
1 Capa · 2 Guia/incidência ENEM · **A** 3 Terra e placas I · 4 Limites/subducção/Andes · 5 Estruturas geológicas + ciclo das rochas · 6 Intemperismo×erosão + solos · 7 Massas de ar + chuvas · 8 El Niño/La Niña + rios voadores + climogramas · 9 Hidrografia + litoral · **B** 10 Domínios (mapa) · 11 Vegetações · 12 Impactos/diferenciações/transições/biomas mundiais · **C** 13 Sistemas agrários · 14 Revolução Verde · 15 Impactos químicos/biológicos · 16 Solos e manejo · 17 Fronteira agrícola · 18 Estrutura fundiária · 19 Povos tradicionais + agro 4.0 + exercícios · **D** 20 Urbanização/hierarquia · 21 Cidade e ambiente · 22 Segregação/mobilidade · 23 Demografia · 24 Migrações + exercícios · **E** 25 Revoluções/Taylor-Ford-Toyota · 26 Locacional/desindustrialização · 27 DIT/globalização/Milton Santos · 28 Trabalho · 29 Blocos/comércio · 30 Energia/transportes · **F** 31 Guerra Fria/nova ordem · 32 Organizações · 33 Conflitos I (Mar da China, Ucrânia) · 34 Conflitos II (Israel-Palestina) + Rota da Seda + Brasil/Amazônia · **G** 35 Escala/coordenadas/fusos · 36 Projeções/anamorfose · 37 Curvas de nível/sensoriamento/SIG/GPS · 38 Revisão final (encadeamentos + distinções) · (39–40 reserva: gabarito comentado e fontes/auditoria)

## Progresso
- [x] Dados geoespaciais baixados e inspecionados
- [x] Estatísticas principais verificadas
- [x] Biblioteca SVG + CSS + build
- [x] Mapas
- [x] Páginas (39)
- [x] Auditoria visual
- [x] Relatório/README/commit/push
