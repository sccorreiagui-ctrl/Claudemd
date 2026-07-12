#!/usr/bin/env bash
# Hook de SessionStart do OrçaFácil.
# Prepara o ambiente para desenvolvimento e testes em sessões do Claude Code.
set -euo pipefail

echo "[OrçaFácil] Preparando ambiente…"

# Garante o pytest disponível para rodar a suíte.
if ! python3 -c "import pytest" >/dev/null 2>&1; then
  echo "[OrçaFácil] Instalando pytest…"
  pip install --quiet pytest || echo "[OrçaFácil] aviso: falha ao instalar pytest"
fi

# Gera os dados de exemplo se ainda não existirem.
if [ ! -f data/extrato_exemplo.csv ]; then
  echo "[OrçaFácil] Gerando dados de exemplo…"
  python3 scripts/gerar_dados.py || echo "[OrçaFácil] aviso: falha ao gerar dados"
fi

echo "[OrçaFácil] Pronto. Rode 'python3 -m pytest' para validar."
