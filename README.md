# OrçaFácil 💰

Motor de **análise de finanças pessoais** em Python. Lê extratos em CSV,
categoriza automaticamente os gastos por comerciante (regras adaptadas ao
Brasil), calcula indicadores e gera **insights** e um **dashboard interativo**.

> Projeto criado no repositório *Claudemd* como demonstração de capacidade
> máxima do Claude Code — engenharia de software, testes, visualização de dados
> e documentação num fluxo único. Veja [`docs/SKILLS.md`](docs/SKILLS.md) para o
> mapa de habilidades exercitadas.

---

## ✨ O que ele faz

- **Parser robusto de CSV** — datas em ISO ou `DD/MM/AAAA`, valores com `R$`,
  vírgula ou ponto decimal, cabeçalhos em qualquer caixa.
- **Categorização automática** — 10 categorias (Alimentação, Transporte,
  Moradia, Saúde, Lazer, Educação, Compras, Serviços, Renda, Outros) via regras
  de palavra-chave que ignoram acentos e maiúsculas.
- **Analytics** — totais, saldo, taxa de poupança, quebra por categoria,
  evolução mensal e maiores despesas.
- **Insights automáticos** — alerta de saldo negativo, concentração de gastos,
  variação mês a mês.
- **Saída flexível** — relatório em texto no terminal ou JSON para integração.
- **Dashboard** — página HTML autocontida, responsiva e com tema claro/escuro
  (`dashboard/index.html`).

## 🚀 Uso rápido

```bash
# 1. Gerar dados de exemplo (6 meses, determinístico)
python3 scripts/gerar_dados.py

# 2. Analisar no terminal
python3 -m orcafacil.cli analisar data/extrato_exemplo.csv

# 3. Ou obter JSON (alimenta o dashboard)
python3 -m orcafacil.cli analisar data/extrato_exemplo.csv --json
```

### Como biblioteca

```python
from orcafacil import ler_csv, categorizar_todas, gerar_relatorio

transacoes = categorizar_todas(ler_csv("meu_extrato.csv"))
rel = gerar_relatorio(transacoes)

print(rel.saldo)           # Decimal("8183.79")
print(rel.taxa_poupanca)   # 18.19
for ins in rel.insights:
    print(ins)
```

## 📄 Formato do CSV

```csv
data,descricao,valor
2026-01-05,Salario Empresa XYZ,7500.00
2026-01-10,iFood *Restaurante,-45.90
2026-01-12,Uber *Trip,-23.50
```

Valores **positivos = receitas**, **negativos = despesas**.

## 🧪 Testes

```bash
pip install pytest
python3 -m pytest        # 43 testes
```

## 🏗️ Arquitetura

```
orcafacil/
├── models.py         # Transacao, Categoria (Decimal para dinheiro)
├── parser.py         # leitura e normalização de CSV
├── categorizer.py    # regras de categorização PT-BR
├── analytics.py      # motor de relatórios e insights
└── cli.py            # interface de linha de comando
dashboard/index.html   # dashboard interativo (dataviz)
scripts/gerar_dados.py # gerador de extrato de exemplo
tests/                 # suíte pytest (43 testes)
```

## 📊 Dashboard

O arquivo `dashboard/index.html` é autocontido (sem dependências externas) e
pode ser aberto direto no navegador. Usa a paleta validada para daltonismo,
tooltips e alternância de tema. Regenere os dados embutidos com o JSON da CLI.

## Licença

MIT.
