#!/bin/bash
# renderiza o PDF em PNG para inspeção: tools/render.sh <pdf> <dpi> [primeira] [ultima]
PDF=${1:-build/apostila.pdf}; DPI=${2:-80}; F=${3:-1}; L=${4:-999}
mkdir -p build/png && rm -f build/png/pg-*.png
pdftoppm -r $DPI -f $F -l $L -png "$PDF" build/png/pg
ls build/png | head -80
