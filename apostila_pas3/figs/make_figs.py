"""Gera todos os SVGs em figs/svg/. Uso: python3 figs/make_figs.py"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(__file__))
OUT = os.path.join(os.path.dirname(__file__), 'svg')
mods = ['figs_c', 'figs_flow', 'figs_p', 'figs_mpl']
n = 0
for m in mods:
    try:
        mod = importlib.import_module(m)
    except ModuleNotFoundError as e:
        if e.name == m:
            print('(sem', m, ')'); continue
        raise
    for fn in mod.ALL:
        r = fn()
        name = fn.__name__
        if r is None:      # figuras matplotlib salvam por conta própria
            continue
        r.save(name, OUT); n += 1
print('figuras vetoriais geradas:', n)
