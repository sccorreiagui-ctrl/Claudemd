"""Interface de linha de comando do OrçaFácil.

Uso::

    python -m orcafacil.cli analisar data/extrato_exemplo.csv
    python -m orcafacil.cli analisar extrato.csv --json
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal

from .analytics import Relatorio, gerar_relatorio
from .categorizer import categorizar_todas
from .parser import ErroDeParsing, ler_csv


def _fmt(valor: Decimal) -> str:
    """Formata como moeda brasileira: R$ 1.234,56."""
    inteiro = f"{valor:,.2f}"
    inteiro = inteiro.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {inteiro}"


def _relatorio_para_dict(rel: Relatorio) -> dict:
    return {
        "periodo": [d.isoformat() for d in rel.periodo] if rel.periodo else None,
        "total_receitas": str(rel.total_receitas),
        "total_despesas": str(rel.total_despesas),
        "saldo": str(rel.saldo),
        "taxa_poupanca": round(rel.taxa_poupanca, 2),
        "por_categoria": [
            {
                "categoria": r.categoria.value,
                "total": str(r.total),
                "quantidade": r.quantidade,
                "percentual": round(r.percentual, 2),
            }
            for r in rel.por_categoria
        ],
        "por_mes": [
            {
                "ano_mes": m.ano_mes,
                "receitas": str(m.receitas),
                "despesas": str(m.despesas),
                "saldo": str(m.saldo),
            }
            for m in rel.por_mes
        ],
        "maiores_despesas": [
            {
                "data": t.data.isoformat(),
                "descricao": t.descricao,
                "valor": str(t.valor_absoluto),
                "categoria": t.categoria.value,
            }
            for t in rel.maiores_despesas
        ],
        "insights": rel.insights,
    }


def _imprimir_texto(rel: Relatorio) -> None:
    largura = 56
    print("=" * largura)
    print("  OrçaFácil — Relatório Financeiro".center(largura))
    if rel.periodo:
        ini, fim = rel.periodo
        print(f"  Período: {ini.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}".center(largura))
    print("=" * largura)
    print(f"  Receitas : {_fmt(rel.total_receitas):>18}")
    print(f"  Despesas : {_fmt(rel.total_despesas):>18}")
    print(f"  Saldo    : {_fmt(rel.saldo):>18}")
    print(f"  Poupança : {rel.taxa_poupanca:>16.1f}%")
    print("-" * largura)
    print("  Gastos por categoria:")
    for r in rel.por_categoria:
        barra = "█" * max(1, round(r.percentual / 5))
        print(f"    {r.categoria.value:<14} {_fmt(r.total):>14}  {r.percentual:5.1f}% {barra}")
    print("-" * largura)
    print("  Maiores despesas:")
    for t in rel.maiores_despesas:
        print(f"    {t.data.strftime('%d/%m')} {t.descricao[:26]:<26} {_fmt(t.valor_absoluto):>12}")
    print("-" * largura)
    print("  Insights:")
    for i in rel.insights:
        print(f"    {i}")
    print("=" * largura)


def cmd_analisar(args: argparse.Namespace) -> int:
    try:
        transacoes = categorizar_todas(ler_csv(args.arquivo))
    except (ErroDeParsing, FileNotFoundError) as exc:
        print(f"Erro ao ler o arquivo: {exc}", file=sys.stderr)
        return 1

    try:
        relatorio = gerar_relatorio(transacoes)
    except ValueError as exc:
        print(f"Erro na análise: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(_relatorio_para_dict(relatorio), ensure_ascii=False, indent=2))
    else:
        _imprimir_texto(relatorio)
    return 0


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orcafacil",
        description="Analisa extratos financeiros e gera relatórios.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_analisar = sub.add_parser("analisar", help="Analisa um extrato CSV")
    p_analisar.add_argument("arquivo", help="Caminho para o extrato CSV")
    p_analisar.add_argument(
        "--json", action="store_true", help="Saída em JSON em vez de texto"
    )
    p_analisar.set_defaults(func=cmd_analisar)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
