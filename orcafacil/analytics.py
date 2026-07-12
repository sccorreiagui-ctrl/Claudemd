"""Motor de analytics financeiro.

Recebe uma lista de transações (idealmente já categorizadas) e produz
resumos: totais, quebra por categoria, evolução mensal, maiores gastos,
taxa de poupança e insights automáticos.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Iterable

from .models import Categoria, Transacao

CENTAVOS = Decimal("0.01")


def _q(valor: Decimal) -> Decimal:
    """Arredonda para duas casas decimais."""
    return valor.quantize(CENTAVOS)


@dataclass
class ResumoCategoria:
    categoria: Categoria
    total: Decimal
    quantidade: int
    percentual: float  # sobre o total de despesas


@dataclass
class ResumoMensal:
    ano_mes: str  # "AAAA-MM"
    receitas: Decimal
    despesas: Decimal

    @property
    def saldo(self) -> Decimal:
        return _q(self.receitas - self.despesas)


@dataclass
class Relatorio:
    total_receitas: Decimal
    total_despesas: Decimal
    saldo: Decimal
    taxa_poupanca: float  # % das receitas que sobrou
    por_categoria: list[ResumoCategoria]
    por_mes: list[ResumoMensal]
    maiores_despesas: list[Transacao]
    insights: list[str] = field(default_factory=list)
    periodo: tuple[date, date] | None = None


def _agrupar_por_categoria(
    despesas: list[Transacao], total_despesas: Decimal
) -> list[ResumoCategoria]:
    acumulado: dict[Categoria, Decimal] = defaultdict(lambda: Decimal("0"))
    contagem: dict[Categoria, int] = defaultdict(int)
    for t in despesas:
        acumulado[t.categoria] += t.valor_absoluto
        contagem[t.categoria] += 1

    resumos = [
        ResumoCategoria(
            categoria=cat,
            total=_q(valor),
            quantidade=contagem[cat],
            percentual=float(valor / total_despesas * 100) if total_despesas else 0.0,
        )
        for cat, valor in acumulado.items()
    ]
    return sorted(resumos, key=lambda r: r.total, reverse=True)


def _agrupar_por_mes(transacoes: list[Transacao]) -> list[ResumoMensal]:
    receitas: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    despesas: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for t in transacoes:
        chave = f"{t.data.year:04d}-{t.data.month:02d}"
        if t.eh_receita:
            receitas[chave] += t.valor
        else:
            despesas[chave] += t.valor_absoluto

    meses = sorted(set(receitas) | set(despesas))
    return [
        ResumoMensal(
            ano_mes=m,
            receitas=_q(receitas[m]),
            despesas=_q(despesas[m]),
        )
        for m in meses
    ]


def _gerar_insights(relatorio: Relatorio) -> list[str]:
    insights: list[str] = []

    if relatorio.taxa_poupanca < 0:
        insights.append(
            "⚠️ Você gastou mais do que ganhou no período — saldo negativo."
        )
    elif relatorio.taxa_poupanca < 10:
        insights.append(
            f"💡 Sua taxa de poupança está baixa ({relatorio.taxa_poupanca:.0f}%). "
            "A recomendação clássica é poupar ao menos 10-20% da renda."
        )
    else:
        insights.append(
            f"✅ Ótimo! Você poupou {relatorio.taxa_poupanca:.0f}% da sua renda no período."
        )

    if relatorio.por_categoria:
        maior = relatorio.por_categoria[0]
        if maior.percentual >= 40:
            insights.append(
                f"📌 {maior.categoria} concentra {maior.percentual:.0f}% dos seus "
                "gastos — vale investigar se há espaço para reduzir."
            )
        else:
            insights.append(
                f"📊 Sua maior categoria de gasto é {maior.categoria} "
                f"({maior.percentual:.0f}% do total)."
            )

    if len(relatorio.por_mes) >= 2:
        ultimo, penultimo = relatorio.por_mes[-1], relatorio.por_mes[-2]
        if penultimo.despesas > 0:
            variacao = float(
                (ultimo.despesas - penultimo.despesas) / penultimo.despesas * 100
            )
            if variacao > 15:
                insights.append(
                    f"📈 Seus gastos subiram {variacao:.0f}% em relação ao mês anterior."
                )
            elif variacao < -15:
                insights.append(
                    f"📉 Seus gastos caíram {abs(variacao):.0f}% em relação ao mês anterior. Parabéns!"
                )

    return insights


def gerar_relatorio(
    transacoes: Iterable[Transacao], top_n_despesas: int = 5
) -> Relatorio:
    """Constrói o relatório completo a partir das transações."""
    transacoes = list(transacoes)
    if not transacoes:
        raise ValueError("Nenhuma transação fornecida para análise.")

    receitas = [t for t in transacoes if t.eh_receita]
    despesas = [t for t in transacoes if t.eh_despesa]

    total_receitas = _q(sum((t.valor for t in receitas), Decimal("0")))
    total_despesas = _q(sum((t.valor_absoluto for t in despesas), Decimal("0")))
    saldo = _q(total_receitas - total_despesas)
    taxa_poupanca = (
        float(saldo / total_receitas * 100) if total_receitas > 0 else 0.0
    )

    datas = [t.data for t in transacoes]
    relatorio = Relatorio(
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        taxa_poupanca=taxa_poupanca,
        por_categoria=_agrupar_por_categoria(despesas, total_despesas),
        por_mes=_agrupar_por_mes(transacoes),
        maiores_despesas=sorted(
            despesas, key=lambda t: t.valor_absoluto, reverse=True
        )[:top_n_despesas],
        periodo=(min(datas), max(datas)),
    )
    relatorio.insights = _gerar_insights(relatorio)
    return relatorio
