#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${WORKSPACE_DIR}"

python -m pip install --upgrade pip
python -m pip install --upgrade uv ruff

projects=(
  "teaine-common"
  "teaine-ruler"
  "teaine-archer"
  "teaine-grail"
)

for project in "${projects[@]}"; do
  if [ -f "${project}/pyproject.toml" ]; then
    echo "Syncing ${project}..."
    (cd "${project}" && uv sync)
  fi
done
