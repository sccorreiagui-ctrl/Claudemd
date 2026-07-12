# Mapa de habilidades exercitadas

Este projeto foi construído em uma única sessão como um teste de capacidade do
Claude Code. Abaixo, o que cada parte demonstra.

| Habilidade | Onde aparece |
|---|---|
| **Engenharia de software** | Pacote modular `orcafacil/` com separação clara (models / parser / categorizer / analytics / cli), tipos, `Decimal` para dinheiro, dataclasses imutáveis. |
| **Testes automatizados** | `tests/` com 43 casos `pytest` cobrindo parsing, categorização e analytics, incluindo casos de erro e de borda. |
| **`verify` (execução real)** | A suíte foi executada e a CLI exercitada de ponta a ponta antes de commitar — não só "escrever e torcer". |
| **`dataviz`** | `dashboard/index.html`: formas escolhidas por função (KPIs, barras agrupadas, ranking, linha de saldo), paleta validada para daltonismo (`validate_palette.js`), tooltips, legenda e rótulos diretos. |
| **`artifact-design`** | Tratamento de *design de informação*: hierarquia tipográfica, tokens de tema claro/escuro, `tabular-nums`, layout em grid, foco acessível. |
| **Renderização e inspeção** | O dashboard foi renderizado em Chromium headless (Playwright) nos dois temas; layout, overflow e erros de console verificados; um rótulo de eixo cortado foi corrigido. |
| **`init` (CLAUDE.md)** | `CLAUDE.md` com comandos, convenções e estrutura para orientar agentes futuros. |
| **`session-start-hook`** | `.claude/settings.json` + `.claude/hooks/session_start.sh` preparam o ambiente (instalam pytest, geram dados) em sessões web. |
| **Fluxo Git** | Desenvolvimento na branch designada, commits descritivos, push. |

## Como reproduzir a verificação

```bash
python3 -m pytest                                   # 43 passed
python3 -m orcafacil.cli analisar data/extrato_exemplo.csv
```
