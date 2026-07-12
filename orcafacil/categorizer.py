"""Categorização automática de transações.

Usa um conjunto de regras baseadas em palavras-chave presentes na
descrição da transação, cobrindo comerciantes e termos comuns no Brasil.
Receitas (valor positivo) são sempre classificadas como ``RENDA`` a menos
que uma regra mais específica se aplique.
"""

from __future__ import annotations

from typing import Iterable

from .models import Categoria, Transacao

# Ordem importa: a primeira categoria cujo termo casar vence.
REGRAS: list[tuple[Categoria, tuple[str, ...]]] = [
    (
        Categoria.ALIMENTACAO,
        (
            "ifood", "rappi", "restaurante", "padaria", "mercado",
            "supermercado", "carrefour", "pao de acucar", "assai",
            "hortifruti", "lanchonete", "burger", "mcdonald", "pizza",
            "cafe", "bar ",
        ),
    ),
    (
        Categoria.TRANSPORTE,
        (
            "uber", "99", "99pop", "taxi", "posto", "shell", "ipiranga",
            "petrobras", "combustivel", "gasolina", "estacionamento",
            "metro", "onibus", "bilhete unico", "pedagio",
        ),
    ),
    (
        Categoria.MORADIA,
        (
            "aluguel", "condominio", "enel", "light", "energia", "cemig",
            "sabesp", "agua", "gas ", "comgas", "iptu", "imobiliaria",
        ),
    ),
    (
        Categoria.SAUDE,
        (
            "drogaria", "drogasil", "droga raia", "farmacia", "pague menos",
            "hospital", "clinica", "laboratorio", "unimed", "amil",
            "dentista", "psicolog",
        ),
    ),
    (
        Categoria.EDUCACAO,
        (
            "escola", "faculdade", "universidade", "curso", "udemy", "alura",
            "livraria", "coursera", "mensalidade escolar",
        ),
    ),
    (
        Categoria.LAZER,
        (
            "netflix", "spotify", "disney", "hbo", "max ", "prime video",
            "cinema", "ingresso", "steam", "playstation", "xbox", "viagem",
            "hotel", "airbnb", "booking",
        ),
    ),
    (
        Categoria.SERVICOS,
        (
            "vivo", "claro", "tim", "oi ", "internet", "netflix ", "assinatura",
            "google", "apple.com", "microsoft", "seguro", "banco", "tarifa",
            "anuidade", "cartorio",
        ),
    ),
    (
        Categoria.COMPRAS,
        (
            "magazine", "magalu", "americanas", "amazon", "mercado livre",
            "mercadolivre", "shopee", "aliexpress", "renner", "riachuelo",
            "zara", "shopping", "loja",
        ),
    ),
    (
        Categoria.RENDA,
        (
            "salario", "pagamento", "provento", "pix recebido", "transferencia recebida",
            "rendimento", "dividendo", "reembolso", "restituicao",
        ),
    ),
]


def _normalizar(texto: str) -> str:
    """Remove acentos e coloca em minúsculas para casamento robusto."""
    import unicodedata

    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def categorizar_descricao(descricao: str, eh_receita: bool = False) -> Categoria:
    """Determina a categoria a partir do texto da descrição."""
    texto = _normalizar(descricao)
    for categoria, termos in REGRAS:
        if any(termo in texto for termo in termos):
            return categoria
    # Fallback: receita sem regra específica é renda; despesa é "outros".
    return Categoria.RENDA if eh_receita else Categoria.OUTROS


def categorizar(transacao: Transacao) -> Transacao:
    """Retorna a transação com a categoria preenchida automaticamente."""
    categoria = categorizar_descricao(transacao.descricao, transacao.eh_receita)
    return transacao.com_categoria(categoria)


def categorizar_todas(transacoes: Iterable[Transacao]) -> list[Transacao]:
    return [categorizar(t) for t in transacoes]
