"""Registro de figuras. Cada função @fig('nome') devolve um objeto Fig (svgkit)."""
import importlib, pkgutil
REGISTRY = {}

def fig(name):
    def deco(fn):
        if name in REGISTRY:
            raise ValueError(f"figura duplicada: {name}")
        REGISTRY[name] = fn
        return fn
    return deco

def load_all():
    for m in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{m.name}")
