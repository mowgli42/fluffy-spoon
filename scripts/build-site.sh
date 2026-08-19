#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="${ROOT}/recipe-system/scripts"
WEB_DIR="${ROOT}/recipe-system/web"
DIST_DIR="${ROOT}/dist"

if [[ ! -f "${WEB_DIR}/recipe-box.html" ]]; then
  echo "ERROR: Missing ${WEB_DIR}/recipe-box.html in repository."
  exit 1
fi

# Regenerate pages when Python + lxml are available (Vercel, local dev).
if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install --quiet -r "${ROOT}/requirements.txt" 2>/dev/null \
    || python3 -m pip install --quiet -r "${SCRIPTS_DIR}/requirements.txt" 2>/dev/null \
    || true

  if python3 -c "import lxml" 2>/dev/null; then
    # ponytail: fall back to committed HTML if one bad XML breaks regen
    if (
      cd "${SCRIPTS_DIR}"
      python3 recipe-gen.py
      python3 cookbook-pkg.py
    ); then
      :
    else
      echo "WARN: recipe generation failed; deploying committed static files."
    fi
  else
    echo "WARN: lxml not available; deploying committed static files."
  fi
else
  echo "WARN: python3 not available; deploying committed static files."
fi

rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"
cp -a "${WEB_DIR}/." "${DIST_DIR}/"

if [[ ! -f "${DIST_DIR}/recipe-box.html" ]]; then
  echo "ERROR: Build output missing recipe-box.html"
  exit 1
fi

echo "Static site ready in ${DIST_DIR}"
ls -la "${DIST_DIR}" | head -20
