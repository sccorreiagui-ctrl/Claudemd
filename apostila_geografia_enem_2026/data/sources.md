# Fontes de dados e referências

## Dados geoespaciais (baixados por `src/fetch_data.py`, não versionados: ≈ 95 MB)
| Camada | Fonte | Licença / observação |
|---|---|---|
| Países, estados, rios, lagos, linhas disputadas, indicador marítimo (nove traços), lugares | Natural Earth (espelho GitHub `nvkelso/natural-earth-vector`) | Domínio público. Limites "de fato"; sem posição oficial. A Crimeia e Sevastopol vêm dentro da Rússia e são tratadas e rotuladas no mapa de Ucrânia; o Golã vem dentro de Israel e é separado pela linha de reivindicação síria. |
| Limites de placas tectônicas | Bird (2003), modelo PB2002 (espelho `fraxen/tectonicplates`) | Tipos: OSR/CRB→divergente; OTF/CTF→transformante; SUB/OCB/CCB→convergente, suavizados por maioria em janela de 5 segmentos |
| Biomas do Brasil 1:5.000.000 | IBGE/MMA (espelho `SamanthaReiis/Biomas-Brasileiros`) | Domínios de Ab'Saber **não** têm vetor acessível: mapa aproximado a partir dos biomas |

## Séries processadas (`data/processed/`)
- `piramide_etaria_ibge.json` — Censos 1980 (SIDRA t. 200) e 2022 (t. 9514)
- `urbanizacao_ibge.json` — Censos 1970–2022 (SIDRA t. 202 e Censo 2022)
- `climogramas_inmet_1991_2020.json` — Normais Climatológicas 1991–2020 (Manaus, Brasília, Petrolina, Porto Alegre)
- `populacao_uf_2022.json` — SIDRA t. 4709, var. 93 (soma 203.080.756), consulta em 14/11/2026

## Estatísticas e situações datadas (consultas em 14/11/2026)
Censo Agropecuário 2017 (IBGE); Censo 2022; Contas Nacionais Trimestrais 2025 (IBGE, 3/3/2026); BEN 2026 (EPE, ano-base 2025);
CNT Boletim Unificado (mar/2022); MDIC balança comercial 2025 (6/1/2026); ONU/DESA International Migrant Stock 2024; ACNUR 2024;
Comissão Europeia (acordo UE–Mercosul, aplicação provisória desde 1/5/2026); Reuters Fact Check 24/7/2026 (tarifas EUA);
NATO (32 membros; cúpula de Ancara 7–8/7/2026); presidência indiana do BRICS 2026; ASEAN (Timor-Leste, 26/10/2025);
PCA caso 2013-19 (12/7/2016); AGNU 68/262 e ES-11/4; CIJ parecer 19/7/2024; IEA (terras raras 2025); China Briefing (9/11/2026);
ISW, NPR, Atlantic Council (Rússia–Ucrânia, nov/2026).

## Não reauditado
Percentuais de incidência por tema no ENEM (Aprova Total 2016–2025) vêm do briefing do projeto.
