#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="${ROOT}/recipe-system/scripts"

python3 -m pip install --quiet -r "${SCRIPTS_DIR}/requirements.txt"

cd "${SCRIPTS_DIR}"
python3 recipe-gen.py
python3 cookbook-pkg.py

echo "Site built in ${ROOT}/recipe-system/web"
