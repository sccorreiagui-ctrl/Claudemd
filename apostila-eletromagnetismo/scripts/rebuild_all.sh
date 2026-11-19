#!/usr/bin/env bash
# Regenera TUDO a partir das fontes: figuras → HTML → PDF → PDF final → checagens.
#   uso: bash scripts/rebuild_all.sh [--sem-fisica]      (requer: node ≥ 18, python3 com numpy/scipy/pillow/fonttools/pypdf, poppler-utils)
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d node_modules ] || npm install                      # katex, cheerio, @fontsource/*, playwright (já instalado no ambiente)
[ -d assets/katex ] || node scripts/vendor.mjs          # copia KaTeX e as fontes para assets/
[ -d scripts/_fonts ] || python3 scripts/make_ttf.py    # TTFs só para medir largura de texto nas figuras

echo "== 1/6 figuras SVG (scripts/figs_m*.py → build/figures)"
( cd scripts && for f in figs_m1.py figs_m2.py figs_m3.py figs_m4a.py figs_m4b.py figs_m5.py; do python3 "$f" > /dev/null; done )

echo "== 2/6 HTML (src/pages + src/css + figuras → build/book.html)"
node scripts/build.mjs

echo "== 3/6 PDF (Chromium) + relatório de layout por página"
node scripts/make_pdf.mjs

echo "== 4/6 PDF final (metadados e marcadores)"
python3 scripts/finalize_pdf.py

echo "== 5/6 checagem do PDF (28 páginas A4, rodapé, texto, fontes, vetores)"
python3 scripts/check_pdf.py | tail -3

if [ "${1:-}" != "--sem-fisica" ]; then
  echo "== 6/6 validação física independente"
  python3 scripts/validate_physics.py | tail -2
fi
