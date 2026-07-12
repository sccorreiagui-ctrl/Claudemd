"""OrçaFácil — motor de análise de finanças pessoais.

Exemplo rápido::

    from orcafacil import ler_csv, categorizar_todas, gerar_relatorio

    transacoes = categorizar_todas(ler_csv("extrato.csv"))
    relatorio = gerar_relatorio(transacoes)
    print(relatorio.saldo)
"""

from __future__ import annotations

from .analytics import (
    Relatorio,
    ResumoCategoria,
    ResumoMensal,
    gerar_relatorio,
)
from .categorizer import categorizar, categorizar_descricao, categorizar_todas
from .models import Categoria, Transacao
from .parser import ErroDeParsing, ler_csv, parse_linhas

__version__ = "1.0.0"

__all__ = [
    "Categoria",
    "Transacao",
    "ler_csv",
    "parse_linhas",
    "ErroDeParsing",
    "categorizar",
    "categorizar_descricao",
    "categorizar_todas",
    "gerar_relatorio",
    "Relatorio",
    "ResumoCategoria",
    "ResumoMensal",
]
