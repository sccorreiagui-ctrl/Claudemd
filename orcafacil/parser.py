"""Leitura de extratos em CSV.

Aceita arquivos com as colunas ``data``, ``descricao`` e ``valor``. Datas
podem vir em ISO (``AAAA-MM-DD``) ou no formato brasileiro
(``DD/MM/AAAA``). Valores podem usar vírgula ou ponto como separador
decimal e opcionalmente o símbolo ``R$``.
"""

from __future__ import annotations

import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Iterator

from .models import Transacao

COLUNAS_OBRIGATORIAS = {"data", "descricao", "valor"}


class ErroDeParsing(ValueError):
    """Erro levantado quando uma linha ou cabeçalho é inválido."""


def _parse_data(texto: str) -> date:
    texto = texto.strip()
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ErroDeParsing(f"Data inválida: {texto!r}")


def _parse_valor(texto: str) -> Decimal:
    limpo = (
        texto.strip()
        .replace("R$", "")
        .replace(" ", "")
    )
    if not limpo:
        raise ErroDeParsing("Valor vazio")

    # Normaliza separadores: se houver vírgula e ponto, assume padrão
    # brasileiro (ponto = milhar, vírgula = decimal).
    if "," in limpo and "." in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    elif "," in limpo:
        limpo = limpo.replace(",", ".")

    try:
        return Decimal(limpo)
    except InvalidOperation as exc:
        raise ErroDeParsing(f"Valor inválido: {texto!r}") from exc


def parse_linhas(linhas: Iterable[dict[str, str]]) -> Iterator[Transacao]:
    """Converte dicionários de linhas CSV em transações."""
    for numero, linha in enumerate(linhas, start=2):  # linha 1 = cabeçalho
        faltando = COLUNAS_OBRIGATORIAS - set(linha.keys())
        if faltando:
            raise ErroDeParsing(
                f"Linha {numero}: colunas ausentes {sorted(faltando)}"
            )
        try:
            yield Transacao(
                data=_parse_data(linha["data"]),
                descricao=linha["descricao"].strip(),
                valor=_parse_valor(linha["valor"]),
            )
        except ErroDeParsing as exc:
            raise ErroDeParsing(f"Linha {numero}: {exc}") from exc


def ler_csv(caminho: str | Path) -> list[Transacao]:
    """Lê um extrato CSV do disco e retorna a lista de transações."""
    caminho = Path(caminho)
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames is None:
            raise ErroDeParsing("Arquivo CSV vazio")
        cabecalho = {c.strip().lower() for c in leitor.fieldnames}
        faltando = COLUNAS_OBRIGATORIAS - cabecalho
        if faltando:
            raise ErroDeParsing(
                f"Cabeçalho inválido, faltam colunas: {sorted(faltando)}"
            )
        # Normaliza chaves para minúsculas.
        linhas = (
            {k.strip().lower(): v for k, v in linha.items()} for linha in leitor
        )
        return list(parse_linhas(linhas))
