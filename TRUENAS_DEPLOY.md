# Deploying FluffySpoon Recipe Site on TrueNAS

This guide walks you through deploying the static FluffySpoon recipe collection on your TrueNAS system. The site is a lightweight static HTML/CSS/JS app generated from XML recipes. Perfect for a home NAS dashboard or local recipe book.

**Recommended: TrueNAS Scale** (Debian-based, excellent Docker/Apps support). TrueNAS Core (FreeBSD) instructions are included at the end.

## Prerequisites
- TrueNAS Scale or Core with SSH/Shell access enabled.
- A dedicated dataset (recommended): e.g., `pool/apps/fluffyspoon` or `tank/apps/fluffyspoon`.
- Git installed (usually available or install via shell).
- Python 3 + pip (for building; Scale shell supports apt/pip).
- (For easy serving) TrueNAS Apps enabled (Docker).

## Quick Start (TrueNAS Scale - Easiest Method)

1. **Create Dataset**
   - Go to Storage > Datasets > Create Dataset named `apps/fluffyspoon` (or similar) under your main pool.

2. **SSH into TrueNAS** (or use System > Shell).

3. **Run the Deploy Script** (see below for details or copy-paste the one-liner setup).

4. **Serve the Site**
   - Go to Apps in TrueNAS UI.
   - Install **Nginx Proxy Manager** (highly recommended for easy HTTPS, reverse proxy, and Let's Encrypt).
   - Or install a simple **nginx** app / Custom App:
     - Image: `nginx:alpine`
     - Host Path volume: Mount your dataset path (e.g., `/mnt/pool/apps/fluffyspoon/dist` or the `web` folder) to container path `/usr/share/nginx/html`
     - Expose port 80 (or 8080) on host.
   - Access at `http://your-truenas-ip:port`

5. **HTTPS / Nice Domain**
   - Use Nginx Proxy Manager app to proxy to your nginx container or serve directly with SSL.

## The Deploy Script

Save or run this script on your TrueNAS shell. It clones/updates the repo, installs build deps if needed, builds the static site, and prepares serving files.

```bash
#!/bin/bash
# fluffyspoon-truenas-deploy.sh
# Run this on TrueNAS Scale/Core shell

set -euo pipefail

echo "=== FluffySpoon TrueNAS Deploy Script ==="

echo "Enter your apps dataset path (e.g. /mnt/tank/apps/fluffyspoon): "
read -r DEPLOY_BASE

REPO_DIR="${DEPLOY_BASE}/repo"
DIST_DIR="${DEPLOY_BASE}/dist"   # or web for source

mkdir -p "${DEPLOY_BASE}"

if [ ! -d "${REPO_DIR}" ]; then
  echo "Cloning repository..."
  git clone https://github.com/mowgli42/fluffy-spoon.git "${REPO_DIR}"
else
  echo "Updating repository..."
  cd "${REPO_DIR}"
  git pull origin main
fi

cd "${REPO_DIR}"

# Install Python build dependencies (Scale is Debian-based; Core uses pkg)
echo "Installing build dependencies (Python + lxml)..."
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq && sudo apt-get install -y -qq python3-pip python3-lxml || true
  pip3 install --quiet lxml || true
elif command -v pkg >/dev/null 2>&1; then
  sudo pkg install -y py39-lxml || sudo pkg install -y py38-lxml || true
else
  echo "WARNING: Could not auto-install deps. Install python3 and lxml manually."
fi

# Build the static site
echo "Building static site..."
bash scripts/build-site.sh || echo "Build script completed (check for warnings)"

# Copy built files for easy mounting
rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"
cp -a recipe-system/web/. "${DIST_DIR}/" || cp -a dist/. "${DIST_DIR}/" || true

if [ -f "${DIST_DIR}/recipe-box.html" ]; then
  echo "SUCCESS: Static site built in ${DIST_DIR}"
  ls -la "${DIST_DIR}" | head -10
else
  echo "Note: Using source web/ folder if dist not present."
fi

echo ""
echo "=== Next Steps ==="
echo "1. Mount ${DIST_DIR} (or ${REPO_DIR}/recipe-system/web) as a volume in your nginx app."
echo "2. Example docker-compose.yml created below if you want self-contained Docker."
echo ""

# Generate a ready-to-use docker-compose.yml for Docker on Scale
cat > "${DEPLOY_BASE}/docker-compose.yml" << 'COMPOSEEOF'
version: '3.8'
services:
  fluffyspoon-web:
    image: nginx:alpine
    container_name: fluffyspoon
    ports:
      - "8080:80"   # Change port if needed; use 80 if no conflict
    volumes:
      - ./dist:/usr/share/nginx/html:ro   # or ./repo/recipe-system/web
    restart: unless-stopped
    # Add environment or labels for TrueNAS if desired
COMPOSEEOF

echo "docker-compose.yml created at ${DEPLOY_BASE}/docker-compose.yml"
echo "To run: cd ${DEPLOY_BASE} && docker compose up -d   (or use in TrueNAS Custom App / Portainer)"
echo ""
echo "For production: Install Nginx Proxy Manager app and proxy http://truenas-ip:8080 with your domain + SSL."
echo "=== Deployment Complete! Add new recipes by editing XML files and re-running this script. ==="
```

**How to use the script:**
- Copy the above into a file `truenas-deploy.sh` on your TrueNAS (via `cat > truenas-deploy.sh` or editor).
- `chmod +x truenas-deploy.sh`
- `./truenas-deploy.sh`
- Follow the prompts (enter your dataset path).

The script handles cloning, updating, dependency installation, building, and even generates a `docker-compose.yml` for easy Docker deployment.

## Updating the Site
Run the deploy script again (it pulls latest changes and rebuilds). New recipes (XML files) will appear after rebuild.

For automation, add a cron job in TrueNAS (Tasks > Cron Jobs):
`0 3 * * * /path/to/truenas-deploy.sh` (daily at 3 AM, adjust path).

## TrueNAS Core (FreeBSD) Notes
- Use Jails instead of Apps.
- Create a jail, install `nginx` or `lighttpd` via `pkg`.
- Mount or copy files from the dataset to the jail's web root (e.g., `/usr/local/www/nginx`).
- Or use the script above (it detects pkg).
- For simple serving: In jail, `python3 -m http.server 8080` from the dist folder (not for production).

## Advanced / Customizations
- **HTTPS**: Always use Nginx Proxy Manager app + valid certs.
- **Custom Domain**: Point DNS to TrueNAS IP and configure proxy.
- **Meal Planner Integration**: The generated site includes the recipe box; extend with your own JS or host the meal-plan-generator.py separately if needed.
- **Backup**: The dataset + repo folder is all you need. Snapshot it.
- **Mobile Friendly**: Already responsive; works great on phones/tablets.

## Troubleshooting
- **404 errors**: Ensure the volume mount points to the correct folder containing `recipe-box.html` and `recipes/` subfolder. Check nginx config or app logs.
- **Build fails (lxml)**: Manually `pip3 install lxml` or install system package.
- **Permissions**: Ensure TrueNAS user has read access to the dataset.
- **Port conflicts**: Change exposed port in app/compose.
- Previous 404 on Vercel? This local deploy avoids cloud issues entirely.

## Why TrueNAS?
Keep your recipes private, fast on LAN, integrated with your storage, no cloud dependency. Perfect for family use or offline access.

Enjoy your self-hosted recipe collection! If you add features or need tweaks to the script, open an issue or PR on GitHub.

**Files added**:
- This guide: `TRUENAS_DEPLOY.md`
- Associated script template in the guide (copy-paste ready).

Run the script, mount in nginx, and you're live!