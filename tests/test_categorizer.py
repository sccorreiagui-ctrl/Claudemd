from datetime import date
from decimal import Decimal

import pytest

from orcafacil.categorizer import (
    categorizar,
    categorizar_descricao,
    categorizar_todas,
)
from orcafacil.models import Categoria, Transacao


@pytest.mark.parametrize(
    "descricao,esperado",
    [
        ("iFood *Restaurante", Categoria.ALIMENTACAO),
        ("Supermercado Pao de Acucar", Categoria.ALIMENTACAO),
        ("Uber *Trip SP", Categoria.TRANSPORTE),
        ("Posto Shell Combustivel", Categoria.TRANSPORTE),
        ("Aluguel Imobiliaria", Categoria.MORADIA),
        ("Enel Energia Eletrica", Categoria.MORADIA),
        ("Drogasil Farmacia", Categoria.SAUDE),
        ("Netflix Assinatura", Categoria.LAZER),
        ("Alura Cursos", Categoria.EDUCACAO),
        ("Magazine Luiza", Categoria.COMPRAS),
        ("Vivo Internet Fibra", Categoria.SERVICOS),
    ],
)
def test_categorizar_despesas(descricao, esperado):
    assert categorizar_descricao(descricao) == esperado


def test_categorizar_ignora_acentos_e_caixa():
    assert categorizar_descricao("DROGARIA são joão") == Categoria.SAUDE


def test_despesa_desconhecida_vira_outros():
    assert categorizar_descricao("Xpto Zyzzyva") == Categoria.OUTROS


def test_receita_desconhecida_vira_renda():
    assert categorizar_descricao("Deposito qualquer", eh_receita=True) == Categoria.RENDA


def test_salario_vira_renda():
    assert categorizar_descricao("Salario Empresa XYZ", eh_receita=True) == Categoria.RENDA


def test_categorizar_transacao():
    t = Transacao(date(2026, 1, 1), "iFood pedido", Decimal("-45.00"))
    resultado = categorizar(t)
    assert resultado.categoria == Categoria.ALIMENTACAO
    # imutabilidade preservada
    assert t.categoria == Categoria.OUTROS


def test_categorizar_todas():
    transacoes = [
        Transacao(date(2026, 1, 1), "Uber", Decimal("-20")),
        Transacao(date(2026, 1, 2), "Salario", Decimal("5000")),
    ]
    resultado = categorizar_todas(transacoes)
    assert [t.categoria for t in resultado] == [
        Categoria.TRANSPORTE,
        Categoria.RENDA,
    ]
