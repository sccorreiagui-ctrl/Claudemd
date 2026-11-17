#!/usr/bin/env python3
"""Monta apostila.html a partir de src/pages/*.html + figuras SVG e gera o PDF.

Uso:  python3 src/build.py            (gera figuras, HTML e PDF)
      python3 src/build.py --html     (só HTML)
Requer: Node + Playwright/Chromium (render.js) e poppler (verificação).
"""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
PDF = os.path.abspath(os.path.join(ROOT, "..", "APOSTILA_FISICA_MODERNA_PAS3_UNB_2026.pdf"))
OUT_HTML = os.path.join(ROOT, "out", "apostila.html")

subprocess.run([sys.executable, "-I", os.path.join(HERE, "figures.py")], check=True)

def svg(name):
    p = os.path.join(ROOT, "figures", name + ".svg")
    return open(p, encoding="utf-8").read()

pages = sorted(glob.glob(os.path.join(HERE, "pages", "p*.html")))
N = len(pages)
sections = []
for i, p in enumerate(pages, 1):
    raw = open(p, encoding="utf-8").read()
    m = re.match(r"\s*<!--(.*?)-->", raw, re.S)
    meta = dict(kv.split("=", 1) for kv in m.group(1).strip().split("|")) if m else {}
    body = raw[m.end():] if m else raw
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda mm: svg(mm.group(1)), body)
    hero = meta.get("hero") == "1"
    hdr = "" if hero else (
        f'<div class="hdr"><div class="brand"><i>PAS 3</i>Física Moderna · UnB</div>'
        f'<div class="topic">{meta.get("topic","")}</div></div>')
    ftr = (f'<div class="ftr"><span><b>Ciências da Natureza · Física</b> — Física Moderna (PAS 3/UnB)</span>'
           f'<span>pág. <b>{i}</b> / {N}</span></div>')
    sections.append(
        f'<section class="page a-{meta.get("accent","gray")}" id="p{i}">{hdr}'
        f'<div class="content{" hero-page" if hero else ""}"><div class="zin">{body}</div></div>{ftr}</section>')

html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Apostila Estratégica de Física Moderna — PAS 3/UnB</title>
<link rel="stylesheet" href="../vendor/katex/katex.min.css">
<link rel="stylesheet" href="../src/styles.css">
</head><body>
{''.join(sections)}
</body></html>"""
os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
open(OUT_HTML, "w", encoding="utf-8").write(html)
print(f"HTML gerado: {N} páginas")
if "--html" in sys.argv:
    sys.exit(0)

env = dict(os.environ)
env["NODE_PATH"] = subprocess.check_output(["npm", "root", "-g"], text=True).strip()
subprocess.run(["node", os.path.join(HERE, "render.js"), OUT_HTML, PDF], check=True, env=env)
