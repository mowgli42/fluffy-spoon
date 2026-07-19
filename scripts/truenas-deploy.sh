#!/bin/bash
# fluffyspoon-truenas-deploy.sh
# TrueNAS deployment helper for FluffySpoon static recipe site
# Run on TrueNAS Scale (preferred) or Core shell
# Usage: ./truenas-deploy.sh [optional-deploy-base-path]

set -euo pipefail

echo "=== FluffySpoon TrueNAS Deploy Script v1 ==="
echo "This will clone/update the repo, build the static site, and prepare files for serving."

echo ""

# Allow passing deploy base as argument or prompt
if [ -n "${1:-}" ]; then
  DEPLOY_BASE="$1"
else
  echo "Enter your TrueNAS apps dataset path (e.g. /mnt/tank/apps/fluffyspoon or /mnt/pool/apps/fluffyspoon):"
  read -r DEPLOY_BASE
fi

if [ -z "${DEPLOY_BASE}" ]; then
  echo "ERROR: No deploy path provided."
  exit 1
fi

REPO_DIR="${DEPLOY_BASE}/repo"
DIST_DIR="${DEPLOY_BASE}/dist"

echo "Using deploy base: ${DEPLOY_BASE}"
mkdir -p "${DEPLOY_BASE}"

# Clone or update repo
if [ ! -d "${REPO_DIR}" ]; then
  echo "Cloning FluffySpoon repository..."
  git clone https://github.com/mowgli42/fluffy-spoon.git "${REPO_DIR}"
else
  echo "Pulling latest changes..."
  cd "${REPO_DIR}"
  git pull --ff-only origin main || git pull origin main
fi

cd "${REPO_DIR}"

# Detect OS and install build dependencies
echo "Checking/installing Python build dependencies (lxml for XML processing)..."

if command -v apt-get >/dev/null 2>&1; then
  # TrueNAS Scale (Debian)
  if ! python3 -c "import lxml" 2>/dev/null; then
    echo "Installing via apt... (may require sudo)"
    sudo apt-get update -qq || true
    sudo apt-get install -y -qq python3-pip python3-lxml || pip3 install --quiet lxml || true
  fi
  pip3 install --quiet lxml 2>/dev/null || true
elif command -v pkg >/dev/null 2>&1; then
  # TrueNAS Core (FreeBSD)
  if ! python3 -c "import lxml" 2>/dev/null; then
    echo "Installing via pkg..."
    sudo pkg install -y py39-lxml || sudo pkg install -y python3-lxml || true
  fi
else
  echo "WARNING: Unknown package manager. Ensure python3 and lxml are installed."
fi

# Run the official build
if [ -f "scripts/build-site.sh" ]; then
  echo "Running official build script..."
  bash scripts/build-site.sh
else
  echo "ERROR: build-site.sh not found."
  exit 1
fi

# Prepare clean dist folder for mounting
echo "Preparing static files for serving..."
rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"

if [ -d "recipe-system/web" ]; then
  cp -a recipe-system/web/. "${DIST_DIR}/"
elif [ -d "dist" ]; then
  cp -a dist/. "${DIST_DIR}/"
else
  echo "WARNING: No web/ or dist/ found after build."
fi

if [ -f "${DIST_DIR}/recipe-box.html" ]; then
  echo "SUCCESS: Static site ready in ${DIST_DIR}"
  echo "Contents preview:"
  ls -la "${DIST_DIR}" | head -15
else
  echo "Note: recipe-box.html may be in source location. Use recipe-system/web if needed."
fi

echo ""
echo "=== Serving Recommendations ==="
echo "1. TrueNAS Apps (Scale): Install 'Nginx' or 'Nginx Proxy Manager' app."
echo "   Mount Host Path: ${DIST_DIR}   -> Container: /usr/share/nginx/html"
echo "   Expose port 80 or 8080."
echo ""
echo "2. Docker Compose (self-contained, run in ${DEPLOY_BASE}):"

echo "Creating docker-compose.yml..."

cat > "${DEPLOY_BASE}/docker-compose.yml" << 'EOF'
version: '3.8'
services:
  web:
    image: nginx:alpine
    container_name: fluffyspoon
    ports:
      - "8080:80"
    volumes:
      - ./dist:/usr/share/nginx/html:ro
    restart: unless-stopped
EOF

echo "docker-compose.yml created at ${DEPLOY_BASE}/docker-compose.yml"
echo "Run with: cd ${DEPLOY_BASE} && docker compose up -d"
echo "(Works in TrueNAS Custom App or if you have Docker Compose available)"
echo ""
echo "3. For HTTPS: Install Nginx Proxy Manager app and add proxy host to http://truenas-ip:8080"
echo ""
echo "=== Done! Your recipe site is ready on TrueNAS. ==="
echo "Re-run this script anytime to update with new recipes or code changes."
echo "Add recipes by editing XML files in repo/recipe-system/recipes/ then re-run build."

# Optional: Show how to add to cron for auto-update (example)
echo ""
echo "Tip: For daily auto-update, add cron job (Tasks > Cron Jobs in UI):"
echo "0 4 * * * $(pwd)/truenas-deploy.sh ${DEPLOY_BASE} > /dev/null 2>&1"
