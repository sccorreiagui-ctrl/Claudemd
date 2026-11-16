#!/usr/bin/env python3
"""PDF → PNGs (pdftoppm) e montagens lado a lado para inspeção visual.
Uso: preview.py [pdf] [dpi] [pag_ini-pag_fim] — grava em build/preview/"""
import subprocess, sys, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[1]
pdf = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "apostila.pdf"
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 80
rng = sys.argv[3] if len(sys.argv) > 3 else None
out = ROOT / "build" / "preview"
out.mkdir(parents=True, exist_ok=True)
args = ["pdftoppm", "-r", str(dpi), "-png"]
if rng:
    a, b = rng.split("-")
    args += ["-f", a, "-l", b]
subprocess.run(args + [str(pdf), str(out / "pg")], check=True)
print("ok", len(list(out.glob("pg-*.png"))), "png")
