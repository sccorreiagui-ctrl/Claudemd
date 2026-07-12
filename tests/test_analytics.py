from datetime import date
from decimal import Decimal

import pytest

from orcafacil.analytics import gerar_relatorio
from orcafacil.categorizer import categorizar_todas
from orcafacil.models import Categoria, Transacao


def _t(dia_iso, desc, valor):
    return Transacao(date.fromisoformat(dia_iso), desc, Decimal(str(valor)))


@pytest.fixture
def transacoes():
    dados = [
        _t("2026-01-05", "Salario", 5000),
        _t("2026-01-10", "Aluguel", -1500),
        _t("2026-01-12", "iFood", -50),
        _t("2026-01-15", "Uber", -30),
        _t("2026-02-05", "Salario", 5000),
        _t("2026-02-10", "Aluguel", -1500),
        _t("2026-02-20", "Magazine Luiza", -700),
    ]
    return categorizar_todas(dados)


def test_totais(transacoes):
    rel = gerar_relatorio(transacoes)
    assert rel.total_receitas == Decimal("10000.00")
    assert rel.total_despesas == Decimal("3780.00")
    assert rel.saldo == Decimal("6220.00")


def test_taxa_poupanca(transacoes):
    rel = gerar_relatorio(transacoes)
    assert rel.taxa_poupanca == pytest.approx(62.2, abs=0.1)


def test_por_categoria_ordenado(transacoes):
    rel = gerar_relatorio(transacoes)
    # Moradia (3000) deve ser a maior categoria.
    assert rel.por_categoria[0].categoria == Categoria.MORADIA
    assert rel.por_categoria[0].total == Decimal("3000.00")
    # Percentuais somam ~100.
    soma = sum(r.percentual for r in rel.por_categoria)
    assert soma == pytest.approx(100.0, abs=0.01)


def test_por_mes(transacoes):
    rel = gerar_relatorio(transacoes)
    assert [m.ano_mes for m in rel.por_mes] == ["2026-01", "2026-02"]
    jan = rel.por_mes[0]
    assert jan.receitas == Decimal("5000.00")
    assert jan.despesas == Decimal("1580.00")
    assert jan.saldo == Decimal("3420.00")


def test_maiores_despesas(transacoes):
    rel = gerar_relatorio(transacoes, top_n_despesas=3)
    assert len(rel.maiores_despesas) == 3
    assert rel.maiores_despesas[0].valor_absoluto == Decimal("1500.00")


def test_insights_gerados(transacoes):
    rel = gerar_relatorio(transacoes)
    assert rel.insights  # não vazio
    assert any("poupou" in i.lower() or "poupança" in i.lower() for i in rel.insights)


def test_saldo_negativo_gera_alerta():
    dados = categorizar_todas([
        _t("2026-01-05", "Salario", 1000),
        _t("2026-01-10", "Aluguel", -1500),
    ])
    rel = gerar_relatorio(dados)
    assert rel.saldo < 0
    assert any("negativo" in i.lower() for i in rel.insights)


def test_relatorio_vazio_levanta_erro():
    with pytest.raises(ValueError):
        gerar_relatorio([])


def test_periodo(transacoes):
    rel = gerar_relatorio(transacoes)
    assert rel.periodo == (date(2026, 1, 5), date(2026, 2, 20))
