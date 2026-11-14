"""Registro de figuras: cada função decorada com @fig('nome') devolve um objeto SVG (svglib) ou string."""
FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco
