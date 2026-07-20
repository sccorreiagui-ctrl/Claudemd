"""Conversao de valores monetarios em reais para texto por extenso (PT-BR)."""

_UNIDADES = [
    "", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
    "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete",
    "dezoito", "dezenove",
]
_DEZENAS = [
    "", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta",
    "oitenta", "noventa",
]
_CENTENAS = [
    "", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
    "seiscentos", "setecentos", "oitocentos", "novecentos",
]


def _grupo_por_extenso(numero: int) -> str:
    """Converte um numero de 0 a 999 por extenso."""
    if numero == 0:
        return ""
    if numero == 100:
        return "cem"

    partes = []
    centena, resto = divmod(numero, 100)
    if centena:
        partes.append(_CENTENAS[centena])

    if resto:
        if resto < 20:
            partes.append(_UNIDADES[resto])
        else:
            dezena, unidade = divmod(resto, 10)
            if unidade:
                partes.append(f"{_DEZENAS[dezena]} e {_UNIDADES[unidade]}")
            else:
                partes.append(_DEZENAS[dezena])

    return " e ".join(partes)


_ESCALAS = [
    ("", ""),
    ("mil", "mil"),
    ("milhão", "milhões"),
    ("bilhão", "bilhões"),
]


def _inteiro_por_extenso(numero: int) -> str:
    if numero == 0:
        return "zero"

    grupos = []
    n = numero
    while n > 0:
        n, grupo = divmod(n, 1000)
        grupos.append(grupo)

    partes = []
    for indice in range(len(grupos) - 1, -1, -1):
        grupo = grupos[indice]
        if grupo == 0:
            continue
        texto_grupo = _grupo_por_extenso(grupo)
        if indice == 1:
            if grupo == 1:
                partes.append("mil")
            else:
                partes.append(f"{texto_grupo} mil")
        elif indice >= 2:
            singular, plural = _ESCALAS[indice]
            escala = singular if grupo == 1 else plural
            partes.append(f"{texto_grupo} {escala}")
        else:
            partes.append(texto_grupo)

    if len(partes) > 1 and grupos[0] != 0 and grupos[0] < 100:
        return ", ".join(partes[:-1]) + " e " + partes[-1]
    return ", ".join(partes)


def valor_por_extenso(valor: float) -> str:
    """Ex: 14846.01 -> 'quatorze mil, oitocentos e quarenta e seis reais e um centavo'."""
    valor = round(float(valor) + 1e-9, 2)
    inteiro = int(valor)
    centavos = round((valor - inteiro) * 100)

    reais_str = _inteiro_por_extenso(inteiro)
    sufixo_reais = "real" if inteiro == 1 else "reais"
    texto = f"{reais_str} {sufixo_reais}"

    if centavos:
        centavos_str = _inteiro_por_extenso(centavos)
        sufixo_centavos = "centavo" if centavos == 1 else "centavos"
        texto += f" e {centavos_str} {sufixo_centavos}"

    return texto
