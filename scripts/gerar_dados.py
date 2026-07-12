"""Gera um extrato de exemplo realista e determinístico (seed fixa).

Cria seis meses de movimentações típicas de uma pessoa física no Brasil,
com salário mensal, gastos recorrentes e despesas variáveis aleatórias.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42

# (descricao, valor_min, valor_max) — despesas variáveis
VARIAVEIS = [
    ("iFood *Restaurante", 25, 90),
    ("Uber *Trip", 12, 45),
    ("Supermercado Pao de Acucar", 80, 320),
    ("Drogasil Farmacia", 15, 120),
    ("Amazon Marketplace", 30, 400),
    ("Posto Shell Combustivel", 90, 260),
    ("Magazine Luiza", 50, 600),
    ("Cinema Ingresso", 30, 80),
    ("Padaria Sao Jorge", 8, 35),
    ("99 App Corrida", 10, 38),
    ("Shopee Compra", 20, 180),
    ("Bar do Ze", 40, 150),
]

# (descricao, valor, dia_do_mes) — recorrentes de despesa
RECORRENTES = [
    ("Aluguel Imobiliaria Santos", -1800, 5),
    ("Condominio Edificio Aurora", -650, 10),
    ("Enel Energia Eletrica", -180, 12),
    ("Sabesp Agua", -95, 12),
    ("Vivo Internet Fibra", -120, 8),
    ("Netflix Assinatura", -55, 15),
    ("Spotify Premium", -22, 15),
    ("Unimed Plano de Saude", -420, 7),
    ("Alura Cursos Mensalidade", -85, 20),
]

SALARIO = ("Salario Empresa XYZ Ltda", 7500, 5)


def gerar(saida: Path, meses: int = 6) -> int:
    rng = random.Random(SEED)
    hoje = date(2026, 6, 30)
    # Início: primeiro dia do mês, `meses` atrás.
    ano = hoje.year
    mes = hoje.month - (meses - 1)
    while mes <= 0:
        mes += 12
        ano -= 1
    inicio = date(ano, mes, 1)

    linhas: list[tuple[str, str, str]] = []

    cursor_ano, cursor_mes = inicio.year, inicio.month
    for _ in range(meses):
        def d(dia: int) -> date:
            return date(cursor_ano, cursor_mes, min(dia, 28))

        # Salário
        desc, val, dia = SALARIO
        linhas.append((d(dia).isoformat(), desc, f"{val:.2f}"))

        # Recorrentes
        for desc, val, dia in RECORRENTES:
            linhas.append((d(dia).isoformat(), desc, f"{val:.2f}"))

        # Variáveis: 18 a 30 gastos no mês
        n = rng.randint(18, 30)
        for _ in range(n):
            desc, vmin, vmax = rng.choice(VARIAVEIS)
            valor = -round(rng.uniform(vmin, vmax), 2)
            dia = rng.randint(1, 28)
            linhas.append((d(dia).isoformat(), desc, f"{valor:.2f}"))

        cursor_mes += 1
        if cursor_mes > 12:
            cursor_mes = 1
            cursor_ano += 1

    linhas.sort(key=lambda x: x[0])

    saida.parent.mkdir(parents=True, exist_ok=True)
    with saida.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["data", "descricao", "valor"])
        writer.writerows(linhas)

    return len(linhas)


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "data" / "extrato_exemplo.csv"
    total = gerar(destino)
    print(f"{total} transações geradas em {destino}")
