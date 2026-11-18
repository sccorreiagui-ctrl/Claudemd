#!/usr/bin/env bash
# uso: scripts/render.sh [dpi] [pagina_inicial] [pagina_final]   -> build/pages/p-NN.png
cd "$(dirname "$0")/.."
DPI=${1:-100}; F=${2:-1}; L=${3:-28}
mkdir -p build/pages && rm -f build/pages/p-*.png
pdftoppm -r "$DPI" -f "$F" -l "$L" -png build/book.pdf build/pages/p
ls build/pages | head -40
