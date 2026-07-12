"""Modelos de domínio do OrçaFácil.

Define as estruturas centrais usadas em todo o projeto: categorias de
transação e a própria transação. Mantido sem dependências externas para
que o núcleo seja leve e fácil de testar.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class Categoria(str, Enum):
    """Categorias de classificação de gastos e receitas."""

    ALIMENTACAO = "Alimentação"
    TRANSPORTE = "Transporte"
    MORADIA = "Moradia"
    SAUDE = "Saúde"
    LAZER = "Lazer"
    EDUCACAO = "Educação"
    COMPRAS = "Compras"
    SERVICOS = "Serviços"
    RENDA = "Renda"
    OUTROS = "Outros"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.value


@dataclass(frozen=True)
class Transacao:
    """Uma única movimentação financeira.

    O valor é positivo para receitas e negativo para despesas, seguindo a
    convenção de extratos bancários. Usamos ``Decimal`` para evitar erros
    de ponto flutuante em dinheiro.
    """

    data: date
    descricao: str
    valor: Decimal
    categoria: Categoria = Categoria.OUTROS

    @property
    def eh_despesa(self) -> bool:
        return self.valor < 0

    @property
    def eh_receita(self) -> bool:
        return self.valor > 0

    @property
    def valor_absoluto(self) -> Decimal:
        return abs(self.valor)

    def com_categoria(self, categoria: Categoria) -> "Transacao":
        """Retorna uma cópia da transação com a categoria informada."""
        return Transacao(
            data=self.data,
            descricao=self.descricao,
            valor=self.valor,
            categoria=categoria,
        )
