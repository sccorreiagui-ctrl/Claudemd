#!/usr/bin/env python3
"""Copia KaTeX e Source Sans 3 de node_modules para assets/ (projeto autocontido).
Uso: npm install && python3 tools/setup_assets.py"""
import re, shutil, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
nm = ROOT / "node_modules"
out_k = ROOT / "assets" / "katex"
out_f = ROOT / "assets" / "fonts"
(out_k / "fonts").mkdir(parents=True, exist_ok=True)
out_f.mkdir(parents=True, exist_ok=True)

dist = nm / "katex" / "dist"
css = (dist / "katex.min.css").read_text(encoding="utf-8")
# manter apenas woff2
css = re.sub(r'src:url\((fonts/[^)]+?\.woff2)\) format\("woff2"\),url\([^)]+?\) format\("woff"\),url\([^)]+?\) format\("truetype"\)',
             r'src:url(\1) format("woff2")', css)
(out_k / "katex.min.css").write_text(css, encoding="utf-8")
shutil.copy(dist / "katex.min.js", out_k / "katex.min.js")
shutil.copy(dist / "contrib" / "auto-render.min.js", out_k / "auto-render.min.js")
for f in (dist / "fonts").glob("*.woff2"):
    shutil.copy(f, out_k / "fonts" / f.name)

ss = nm / "@fontsource" / "source-sans-3" / "files"
for sub in ("latin", "latin-ext", "greek"):
    for w in (400, 600, 700):
        for st in ("normal", "italic"):
            f = ss / f"source-sans-3-{sub}-{w}-{st}.woff2"
            if f.exists():
                shutil.copy(f, out_f / f.name)
print("assets ok:", len(list(out_k.glob('fonts/*'))), "katex fonts;", len(list(out_f.glob('*'))), "text fonts")
