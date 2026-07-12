# CLAUDE.md

Orientações para o Claude Code (e outros agentes) trabalharem neste repositório.

## Visão geral

**OrçaFácil** é um motor de análise de finanças pessoais em Python puro (sem
dependências de runtime além da biblioteca padrão). O pacote `orcafacil/`
expõe parser de CSV, categorizador e motor de analytics; a CLI e um dashboard
HTML consomem essa biblioteca.

## Comandos essenciais

```bash
# Rodar a suíte de testes (requer pytest)
python3 -m pytest

# Gerar dados de exemplo determinísticos
python3 scripts/gerar_dados.py

# Executar a CLI
python3 -m orcafacil.cli analisar data/extrato_exemplo.csv [--json]
```

## Convenções importantes

- **Dinheiro sempre em `Decimal`**, nunca `float`. O parser converte strings
  para `Decimal`; o motor de analytics arredonda com `quantize(Decimal("0.01"))`.
- **Sinal do valor define o tipo**: positivo = receita, negativo = despesa.
- **`Transacao` é imutável** (`@dataclass(frozen=True)`). Para alterar a
  categoria use `.com_categoria(...)`, que devolve uma cópia.
- **Categorização é baseada em regras ordenadas** em `categorizer.py`
  (`REGRAS`): a primeira categoria cujo termo casar vence. Termos são comparados
  sem acento e em minúsculas (`_normalizar`). Ao adicionar comerciantes, insira
  na categoria correta mantendo a ordem de prioridade.
- **Português** em identificadores de domínio, docstrings e mensagens ao usuário.

## Estrutura

| Caminho | Responsabilidade |
|---|---|
| `orcafacil/models.py` | `Transacao`, `Categoria` |
| `orcafacil/parser.py` | Leitura/normalização de CSV |
| `orcafacil/categorizer.py` | Regras de categorização |
| `orcafacil/analytics.py` | Relatórios, agregações e insights |
| `orcafacil/cli.py` | Interface de linha de comando |
| `dashboard/index.html` | Dashboard autocontido |
| `scripts/gerar_dados.py` | Gerador de extrato de exemplo |
| `tests/` | Testes pytest por módulo |

## Ao alterar código

1. Mantenha os testes verdes: `python3 -m pytest`.
2. Novas regras de categorização precisam de um caso em
   `tests/test_categorizer.py`.
3. Se mudar o formato do relatório, atualize `_relatorio_para_dict` na CLI e os
   dados embutidos no dashboard.
4. O dashboard não deve usar recursos externos (CDN/fontes remotas) — tudo
   inline, para funcionar offline e como artifact.
