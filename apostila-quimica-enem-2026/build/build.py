#!/usr/bin/env python3
"""Pipeline de build da Apostila de Química ENEM 2026.

    python3 build/build.py                 # gera HTML + PDF + relatório de layout
    python3 build/build.py --png 70        # além disso rasteriza todas as páginas (dpi)
    python3 build/build.py --png 110 --pages 3,4,5

Etapas: páginas (src/pages/*.html) -> macros (\\ce{}, $math$, {{fig:..}}, {{pg:..}}, {{icon:..}})
        -> build/out/apostila.html -> Chromium (Playwright) -> PDF -> metadados/marcadores (PyMuPDF).
"""
import argparse
import glob
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import registry  # noqa: E402
from chem import replace_ce  # noqa: E402
from svglib import SVG, save_svg  # noqa: E402

OUT = os.path.join(HERE, "out")
PAGES_DIR = os.path.join(ROOT, "src", "pages")
PDF_NAME = "APOSTILA_QUIMICA_ENEM_2026.pdf"

BLOCKS = {
    "A": "Polaridade, interações e solubilidade",
    "B": "Funções orgânicas",
    "C": "Reações, tensoativos, polímeros e isomeria",
    "D": "Soluções e cálculos",
    "E": "Química geral e ambiental",
    "F": "Físico-química",
    "G": "Fundamentos complementares",
    "R": "Revisão final",
    "I": "Como usar esta apostila",
}

ICONS = {
    "water": '<svg viewBox="0 0 12 12"><path d="M6 1C6 1 2.2 5.2 2.2 7.6a3.8 3.8 0 0 0 7.6 0C9.8 5.2 6 1 6 1Z" fill="currentColor"/></svg>',
    "lipid": '<svg viewBox="0 0 12 12"><circle cx="6" cy="3.2" r="2.3" fill="currentColor"/><path d="M4.7 5.6q-1.4 2 0 3.2t0 2.7M7.3 5.6q-1.4 2 0 3.2t0 2.7" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
    "func": '<svg viewBox="0 0 12 12"><path d="M6 1.2L10.2 3.6V8.4L6 10.8L1.8 8.4V3.6Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    "leaf": '<svg viewBox="0 0 12 12"><path d="M1.8 10.2C1.8 5.2 5 2 10.4 1.6C10.4 7 7.2 10.4 1.8 10.2Z" fill="currentColor"/><path d="M2 10L7 5" stroke="#fff" stroke-width="1" stroke-linecap="round"/></svg>',
    "react": '<svg viewBox="0 0 12 12"><path d="M1.2 6H9.4M6.2 2.4L9.9 6L6.2 9.6" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "alert": '<svg viewBox="0 0 12 12"><path d="M6 1.1L11.2 10.5H.8Z" fill="currentColor" stroke="currentColor" stroke-width=".8" stroke-linejoin="round"/><rect x="5.4" y="4.2" width="1.2" height="3.2" rx=".5" fill="#fff"/><circle cx="6" cy="8.8" r=".7" fill="#fff"/></svg>',
    "info": '<svg viewBox="0 0 12 12"><circle cx="6" cy="6" r="5" fill="currentColor"/><rect x="5.4" y="5" width="1.2" height="3.6" rx=".5" fill="#fff"/><circle cx="6" cy="3.5" r=".75" fill="#fff"/></svg>',
    "star": '<svg viewBox="0 0 12 12"><path d="M6 .9L7.5 4.5L11.2 6L7.5 7.5L6 11.1L4.5 7.5L.8 6L4.5 4.5Z" fill="currentColor"/></svg>',
    "calc": '<svg viewBox="0 0 12 12"><rect x="1.6" y="1.2" width="8.8" height="9.6" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M3.5 4h5M3.5 6.2h1.4M7.1 6.2h1.4M3.5 8.4h1.4M7.1 8.4h1.4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
}


# ---------------------------------------------------------------------------- utilidades
def load_figs():
    for path in sorted(glob.glob(os.path.join(HERE, "figs_*.py"))):
        importlib.import_module(os.path.basename(path)[:-3])


_fig_cache = {}
MISSING_KEYS = set()


def fig_html(name):
    if name in _fig_cache:
        return _fig_cache[name]
    if name not in registry.FIGS:
        raise KeyError(f"Figura não registrada: {name}")
    obj = registry.FIGS[name]()
    if isinstance(obj, SVG):
        save_svg(obj, name, os.path.join(ROOT, "assets", "svg"))
        html = obj.render()
    else:
        html = obj
    _fig_cache[name] = html
    return html


def find_brace_end(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("chave não fechada: " + s[start:start + 80])


MATH_RE_DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)
MATH_RE_INLINE = re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<![\\$])\$", re.S)
KATEX_CACHE_FILE = os.path.join(OUT, "katex_cache.json")


def render_math(html_text):
    cache = {}
    if os.path.exists(KATEX_CACHE_FILE):
        cache = json.load(open(KATEX_CACHE_FILE, encoding="utf-8"))
    found = []

    def collect(m, display):
        found.append((m.group(1), display))
        return m.group(0)

    for m in MATH_RE_DISPLAY.finditer(html_text):
        collect(m, True)
    tmp = MATH_RE_DISPLAY.sub("", html_text)
    for m in MATH_RE_INLINE.finditer(tmp):
        collect(m, False)
    todo = []
    for tex, disp in found:
        key = ("D:" if disp else "I:") + tex
        if key not in cache and (tex, disp) not in todo:
            todo.append((tex, disp))
    if todo:
        payload = json.dumps([{"tex": t, "display": d} for t, d in todo])
        res = subprocess.run(["node", os.path.join(HERE, "katex_render.js")], input=payload, text=True,
                             capture_output=True)
        if res.returncode != 0:
            raise RuntimeError("KaTeX falhou:\n" + res.stderr[-1500:])
        for (t, d), h in zip(todo, json.loads(res.stdout)):
            cache[("D:" if d else "I:") + t] = h
        os.makedirs(OUT, exist_ok=True)
        json.dump(cache, open(KATEX_CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False)

    def rep_d(m):
        return '<div class="mathd">' + cache["D:" + m.group(1)] + "</div>"

    def rep_i(m):
        return cache["I:" + m.group(1)]

    html_text = MATH_RE_DISPLAY.sub(rep_d, html_text)
    html_text = MATH_RE_INLINE.sub(rep_i, html_text)
    return html_text


META_RE = re.compile(r"^\s*<!--(.*?)-->", re.S)


def parse_page(path):
    raw = open(path, encoding="utf-8").read()
    m = META_RE.match(raw)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    meta.setdefault("block", "R")
    meta.setdefault("title", os.path.basename(path))
    meta["file"] = os.path.basename(path)
    return meta, raw


QNUM = {}


def assign_questions(metas):
    """Numera {{q:chave}} na ordem das páginas/aparição."""
    k = 0
    for m in metas:
        for mm in re.finditer(r"\{\{q:(\w+)\}\}", m["raw"]):
            if mm.group(1) not in QNUM:
                k += 1
                QNUM[mm.group(1)] = k


def apply_macros(text, pages_idx):
    text = re.sub(r"\{\{q:(\w+)\}\}", lambda m: str(QNUM[m.group(1)]), text)
    text = re.sub(r"\{\{qn:(\w+)\}\}", lambda m: str(QNUM.get(m.group(1), "?")), text)
    # ícones
    text = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], text)
    # número de página
    def _pg(m):
        k = m.group(1)
        if k not in pages_idx:
            MISSING_KEYS.add(k)
            return "?"
        return str(pages_idx[k])
    text = re.sub(r"\{\{pg:(\w+)\}\}", _pg, text)
    # química e matemática (antes de inserir figuras, para não varrer SVG)
    text = replace_ce(text)
    text = render_math(text)
    # figuras
    text = re.sub(r"\{\{fig:([\w\-]+)\}\}", lambda m: fig_html(m.group(1)), text)
    return text


def build_html(selected=None):
    load_figs()
    files = sorted(glob.glob(os.path.join(PAGES_DIR, "p*.html")))
    metas = []
    for i, f in enumerate(files, start=1):
        meta, raw = parse_page(f)
        meta["n"] = i
        meta["raw"] = raw
        metas.append(meta)
    pages_idx = {m.get("key", f"p{m['n']:02d}"): m["n"] for m in metas}
    assign_questions(metas)
    sections = []
    for meta in metas:
        body = apply_macros(meta["raw"], pages_idx)
        blk = meta["block"]
        n = meta["n"]
        key = meta.get("key", f"p{n:02d}")
        if blk == "cover":
            sections.append(f'<section class="page blk-R cover" id="{key}">{body}</section>')
            continue
        bname = BLOCKS.get(blk, "")
        head = (f'<header class="pg-head"><div class="l"><span class="dot"></span>'
                f'<span>Química · ENEM 2026</span><span style="opacity:.5">|</span><span>{bname}</span></div>'
                f'<div class="r">{meta["title"]}</div></header>')
        foot = (f'<footer class="pg-foot"><span>Apostila de revisão intensiva · conceito → desenho → relação → exemplo → ENEM</span>'
                f'<span class="num">{n}</span></footer>')
        sections.append(f'<section class="page blk-{blk}" id="{key}">{head}<div class="pg-body">{body}</div>{foot}</section>')
    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Apostila de Química para o ENEM 2026 — Revisão intensiva</title>
<link rel="stylesheet" href="../../assets/katex/katex.min.css">
<link rel="stylesheet" href="../../src/css/style.css">
</head><body>
{chr(10).join(sections)}
</body></html>"""
    os.makedirs(OUT, exist_ok=True)
    html_path = os.path.join(OUT, "apostila.html")
    open(html_path, "w", encoding="utf-8").write(html)
    return html_path, metas


def render_pdf(html_path):
    pdf_tmp = os.path.join(OUT, "raw.pdf")
    report = os.path.join(OUT, "layout_report.json")
    r = subprocess.run(["node", os.path.join(HERE, "render_pdf.js"), html_path, pdf_tmp, report],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit("Falha ao renderizar PDF")
    return pdf_tmp, json.load(open(report))


def finalize_pdf(pdf_tmp, metas):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_tmp)
    doc.set_metadata({
        "title": "Apostila de Química para o ENEM 2026 — Revisão intensiva",
        "author": "Material de estudo (HTML/CSS/SVG)",
        "subject": "Química — revisão intensiva para o ENEM 2026",
        "keywords": "Química, ENEM 2026, polaridade, funções orgânicas, reações orgânicas, soluções, estequiometria, eletroquímica",
        "creator": "build.py (Chromium/Playwright + RDKit)",
    })
    toc = []
    last_block = None
    for m in metas:
        if m["block"] == "cover":
            toc.append([1, "Capa", m["n"]])
            continue
        if m["block"] != last_block:
            toc.append([1, f"Bloco {m['block']} — {BLOCKS.get(m['block'], '')}", m["n"]])
            last_block = m["block"]
        toc.append([2, f"p. {m['n']} — {m['title']}", m["n"]])
    doc.set_toc(toc)
    out_pdf = os.path.join(ROOT, PDF_NAME)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = doc.page_count
    doc.close()
    return out_pdf, pages


def rasterize(pdf, dpi, pages=None):
    outdir = os.path.join(HERE, "renders")
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "p-*.png")):
        if pages is None:
            os.remove(f)
    cmd_base = ["pdftoppm", "-r", str(dpi), "-png"]
    if pages:
        for p in pages:
            subprocess.run(cmd_base + ["-f", str(p), "-l", str(p), pdf, os.path.join(outdir, "p")], check=True)
    else:
        subprocess.run(cmd_base + [pdf, os.path.join(outdir, "p")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", type=int, default=0, help="dpi para rasterizar páginas")
    ap.add_argument("--pages", type=str, default="", help="lista de páginas para rasterizar, ex.: 3,4")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    html_path, metas = build_html()
    pdf_tmp, audit = render_pdf(html_path)
    out_pdf, npages = finalize_pdf(pdf_tmp, metas)
    print("Questões:", len(QNUM), dict(list(QNUM.items())[:3]), "...")
    if MISSING_KEYS:
        print("AVISO: chaves {{pg:..}} sem página:", sorted(MISSING_KEYS))
    print(f"PDF: {out_pdf} — {npages} páginas ({len(metas)} fontes)")
    bad = 0
    print("pág  over   free  observações")
    for a in audit:
        flag = ""
        if a["over"] > 0.5:
            flag += " ESTOURO"
            bad += 1
        if a["hover"]:
            flag += " H:" + "; ".join(a["hover"][:2])
        if a["clipped"]:
            flag += " CLIP:" + "; ".join(a["clipped"][:2])
        if not args.quiet or flag:
            fr = a["free"]
            print(f"{a['page']:>3}  {a['over']:>5}  {'' if fr is None else fr:>6} {flag}")
    if npages != len(metas):
        print(f"ATENÇÃO: {len(metas)} páginas-fonte geraram {npages} páginas no PDF")
    if args.png:
        pg = [int(x) for x in args.pages.split(",") if x.strip()] if args.pages else None
        rasterize(out_pdf, args.png, pg)
        print(f"PNG ({args.png} dpi) em build/renders/")
    if bad:
        print(f"{bad} página(s) com estouro de conteúdo")


if __name__ == "__main__":
    main()
