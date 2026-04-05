#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/Teaine-Project

python -m pip install --upgrade pip
python -m pip install uv

if [ -f "teaine-grail/pyproject.toml" ]; then
  (cd teaine-grail && uv sync)
fi

if [ -f "teaine-ruler/pyproject.toml" ]; then
  (cd teaine-ruler && uv sync)
fi

if [ -f "teaine-common/pyproject.toml" ]; then
  (cd teaine-common && uv sync)
fi
