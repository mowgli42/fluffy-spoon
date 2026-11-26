#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="${ROOT}/recipe-system/scripts"
WEB_DIR="${ROOT}/recipe-system/web"
DIST_DIR="${ROOT}/dist"
PWA_DIR="${ROOT}/pwa"

if [[ ! -f "${WEB_DIR}/recipe-box.html" ]]; then
  echo "ERROR: Missing ${WEB_DIR}/recipe-box.html in repository."
  exit 1
fi

# Regenerate classic pages when Python + lxml are available (Vercel, local dev).
if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install --quiet -r "${ROOT}/requirements.txt" 2>/dev/null \
    || python3 -m pip install --quiet -r "${SCRIPTS_DIR}/requirements.txt" 2>/dev/null \
    || true

  if python3 -c "import lxml" 2>/dev/null; then
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

  # Always export PWA seed JSON (stdlib only).
  python3 "${SCRIPTS_DIR}/export-pwa-seed.py"
else
  echo "WARN: python3 not available; deploying committed static files / seed."
fi

if [[ ! -f "${PWA_DIR}/package.json" ]]; then
  echo "ERROR: Missing PWA app at ${PWA_DIR}"
  exit 1
fi

# Install + build Svelte PWA into dist/
if [[ ! -d "${PWA_DIR}/node_modules" ]]; then
  (cd "${PWA_DIR}" && npm install)
fi
(cd "${PWA_DIR}" && npm run build)

# Preserve classic static cookbook beside the PWA
mkdir -p "${DIST_DIR}/classic"
cp -a "${WEB_DIR}/." "${DIST_DIR}/classic/"

if [[ ! -f "${DIST_DIR}/index.html" ]]; then
  echo "ERROR: PWA build did not produce dist/index.html"
  exit 1
fi
if [[ ! -f "${DIST_DIR}/classic/recipe-box.html" ]]; then
  echo "ERROR: classic recipe-box missing from dist"
  exit 1
fi

echo "PWA + classic site ready in ${DIST_DIR}"
ls -la "${DIST_DIR}" | head -25
