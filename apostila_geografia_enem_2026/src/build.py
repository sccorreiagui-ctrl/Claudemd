#!/usr/bin/env python3
"""Build da apostila: gera figuras (SVG), renderiza páginas (Jinja2) em html/apostila.html.

Uso:
  python src/build.py                 # figuras + páginas
  python src/build.py --pages         # apenas páginas (usa SVGs já gerados)
  python src/build.py --figs f_a f_b  # gera apenas módulos de figuras indicados (e as páginas)
"""
import argparse, importlib, pathlib, re, sys, time, traceback
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from common import FIG_DIR  # noqa

PAGES = ROOT / "pages"


def build_figures(only=None):
    names = sorted(p.stem for p in (ROOT / "src" / "figs").glob("f_*.py"))
    for n in names:
        if only and n not in only:
            continue
        t0 = time.time()
        try:
            mod = importlib.import_module(f"figs.{n}")
            importlib.reload(mod)
            mod.build()
            print(f"  fig  {n:<22} {time.time()-t0:5.1f}s")
        except Exception:
            print(f"  FALHA em {n}")
            traceback.print_exc()
            sys.exit(1)


_page_counter = {"n": 0}


def next_page():
    _page_counter["n"] += 1
    return _page_counter["n"]


def fig(name):
    p = FIG_DIR / f"{name}.svg"
    if not p.exists():
        return f'<div style="border:1px dashed red;padding:4px;font-size:8px">FIGURA AUSENTE: {name}</div>'
    return p.read_text(encoding="utf-8")


def build_pages():
    env = Environment(loader=FileSystemLoader(str(PAGES)), undefined=StrictUndefined, autoescape=False,
                      trim_blocks=True, lstrip_blocks=True)
    files = sorted(p.name for p in PAGES.glob("p[0-9]*.html"))
    qindex = []
    for i, fn in enumerate(files, 1):
        txt = (PAGES / fn).read_text(encoding="utf-8")
        qs = re.findall(r'<div class="qh">Questão · ([^<]*)</div>', txt)
        gs = re.findall(r'<b class="l">([A-E])</b>', txt)
        qindex += [(i, q, g) for q, g in zip(qs, gs)]
    env.globals.update(next_page=next_page, fig=fig, qindex=qindex)
    _page_counter["n"] = 0
    chunks = []
    for f in files:
        chunks.append(env.get_template(f).render())
    css = (ROOT / "assets" / "css" / "apostila.css").read_text(encoding="utf-8")
    fonts = (ROOT / "assets" / "css" / "fonts.css").read_text(encoding="utf-8") if (ROOT / "assets" / "css" / "fonts.css").exists() else ""
    html = ("<!doctype html><html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            "<title>Apostila Visual de Geografia para o ENEM 2026</title>"
            f"<style>{fonts}\n{css}</style></head><body>\n" + "\n".join(chunks) + "\n</body></html>")
    out = ROOT / "html" / "apostila.html"
    out.write_text(html, encoding="utf-8")
    print(f"  html {out.relative_to(ROOT)}  páginas={_page_counter['n']}  {len(html)/1e6:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", action="store_true")
    ap.add_argument("--figs", nargs="*")
    a = ap.parse_args()
    if not a.pages:
        build_figures(set(a.figs) if a.figs else None)
    build_pages()
