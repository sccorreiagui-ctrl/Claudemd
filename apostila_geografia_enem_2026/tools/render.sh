#!/bin/bash
# Uso: tools/render.sh [dpi] [first] [last]  -> build páginas, exporta PDF e gera PNGs em $SP/render/pg-XX.png
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SP=/tmp/claude-0/-home-user-Claudemd/6ef9e843-2bbf-50f0-912b-d4e67e910ead/scratchpad
DPI=${1:-80}; F=${2:-1}; L=${3:-999}
cd "$ROOT" && $SP/venv/bin/python src/build.py --pages && node tools/export_pdf.js | tail -n +1 && rm -f $SP/render/pg-*.png && pdftoppm -r $DPI -f $F -l $L -png output/APOSTILA_GEOGRAFIA_ENEM_2026.pdf $SP/render/pg 2>/dev/null && ls $SP/render/pg-*.png | head -50
