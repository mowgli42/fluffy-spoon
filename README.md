# Recipe Collection

Standalone recipe book viewable in any web browser. Each recipe is stored as XML; Python scripts generate searchable static HTML for deployment.

![Recipe Collection](https://github.com/user-attachments/assets/f726a9a7-f2b8-4b6b-a386-de3a7ab26c8b)

## Deploy to Vercel

1. Import this repository in [Vercel](https://vercel.com).
2. Use the default settings (Vercel reads `vercel.json`):
   - **Build command:** `npm run build`
   - **Output directory:** `recipe-system/web`
3. Deploy. The site serves `recipe-box.html` at `/` with security headers applied.

To add or change recipes, edit XML files under `recipe-system/recipes/`, commit, and redeploy. The build step regenerates all HTML pages.

## Local development

```bash
# Generate static site
npm run build

# Preview locally
cd recipe-system/web && python3 -m http.server 8080
# Open http://localhost:8080/recipe-box.html
```

### Create recipes locally (optional)

A Flask form can write new XML files on your machine only. It is **disabled by default** and not suitable for Vercel (read-only filesystem).

```bash
cp .env.example .env
# Edit .env: set ENABLE_RECIPE_CREATE=true and FLASK_SECRET_KEY

pip install -r recipe-system/scripts/requirements.txt
cd recipe-system/scripts
python3 recipe-web-generator.py --serve
```

After creating recipes, run `npm run build` from the repo root and refresh the static site.

## Project layout

| Path | Purpose |
|------|---------|
| `recipe-system/recipes/` | Recipe XML source files |
| `recipe-system/scripts/recipe-gen.py` | XML → individual HTML pages (XSLT) |
| `recipe-system/scripts/cookbook-pkg.py` | Builds searchable `recipe-box.html` |
| `recipe-system/scripts/recipe-web-generator.py` | Local recipe creation UI (dev only) |
| `recipe-system/web/` | Generated static site (Vercel output) |

## Security

See [SECURITY.md](SECURITY.md) for deployment model, Flask controls, and XSS mitigations.

## Roadmap

- **Recipe import** — bulk import from external formats (next planned feature)
