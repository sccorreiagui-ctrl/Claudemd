from datetime import date
from decimal import Decimal

import pytest

from orcafacil.parser import (
    ErroDeParsing,
    _parse_data,
    _parse_valor,
    ler_csv,
    parse_linhas,
)


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("2026-03-15", date(2026, 3, 15)),
        ("15/03/2026", date(2026, 3, 15)),
        ("15-03-2026", date(2026, 3, 15)),
        ("  2026-01-01 ", date(2026, 1, 1)),
    ],
)
def test_parse_data_formatos(texto, esperado):
    assert _parse_data(texto) == esperado


def test_parse_data_invalida():
    with pytest.raises(ErroDeParsing):
        _parse_data("31/31/2026")


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("1234.56", Decimal("1234.56")),
        ("1234,56", Decimal("1234.56")),
        ("1.234,56", Decimal("1234.56")),
        ("R$ 1.234,56", Decimal("1234.56")),
        ("-89,90", Decimal("-89.90")),
        ("7500.00", Decimal("7500.00")),
    ],
)
def test_parse_valor(texto, esperado):
    assert _parse_valor(texto) == esperado


def test_parse_valor_vazio():
    with pytest.raises(ErroDeParsing):
        _parse_valor("   ")


def test_parse_linhas_ok():
    linhas = [
        {"data": "2026-01-05", "descricao": "Salario", "valor": "7500,00"},
        {"data": "2026-01-06", "descricao": "iFood", "valor": "-45,90"},
    ]
    transacoes = list(parse_linhas(linhas))
    assert len(transacoes) == 2
    assert transacoes[0].eh_receita
    assert transacoes[1].eh_despesa
    assert transacoes[1].valor == Decimal("-45.90")


def test_parse_linhas_coluna_ausente():
    with pytest.raises(ErroDeParsing) as exc:
        list(parse_linhas([{"data": "2026-01-05", "valor": "10"}]))
    assert "descricao" in str(exc.value)


def test_ler_csv(tmp_path):
    csv_file = tmp_path / "extrato.csv"
    csv_file.write_text(
        "data,descricao,valor\n"
        "2026-01-05,Salario,7500.00\n"
        "2026-01-10,Uber,-23.50\n",
        encoding="utf-8",
    )
    transacoes = ler_csv(csv_file)
    assert len(transacoes) == 2
    assert transacoes[0].descricao == "Salario"


def test_ler_csv_cabecalho_invalido(tmp_path):
    csv_file = tmp_path / "ruim.csv"
    csv_file.write_text("coluna1,coluna2\na,b\n", encoding="utf-8")
    with pytest.raises(ErroDeParsing):
        ler_csv(csv_file)


def test_ler_csv_normaliza_cabecalho_maiusculo(tmp_path):
    csv_file = tmp_path / "maiusc.csv"
    csv_file.write_text(
        "Data,Descricao,Valor\n2026-02-01,Teste,-10.00\n", encoding="utf-8"
    )
    transacoes = ler_csv(csv_file)
    assert len(transacoes) == 1
