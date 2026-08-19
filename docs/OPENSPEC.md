# OpenSpec — FluffySpoon (fluffy-spoon)

Agent-oriented capability and architecture spec for the current static recipe site.
This document reflects **what exists today**, not the full roadmap in the README.

## Surfaces

| Surface | Role | Deployed? |
|---------|------|-----------|
| Static recipe site | Searchable cookbook + per-recipe HTML | Yes (Vercel / TrueNAS / any static host) |
| Local Flask creator | Optional form that writes recipe XML to disk | Local only |
| Meal-plan CLI | Demo weekly / 52-week plan printer | Local CLI only |

There is no authenticated multi-user API, shopping-list service, or hosted recipe editor on Vercel.

## Architecture (current)

```text
recipe-system/recipes/*.xml   ──►  recipe-gen.py (+ XSLT)
                                  └──► web/recipes/<slug>.html

recipe-system/recipes/*.xml   ──►  cookbook-pkg.py (+ recipe.xsd)
                                  └──► web/recipe-box.html

scripts/build-site.sh         ──►  copy web/ → dist/
                                  (regenerates HTML when python3 + lxml available)
```

Source of truth is **XML under `recipe-system/recipes/`**. Committed HTML under `recipe-system/web/` is the build artifact and fallback when `lxml` is unavailable at build time.

## XML recipe schema

- **Schema:** `recipe-system/schemas/recipe.xsd`
- **Namespace:** `http://www.example.com/recipe`
- **Root:** `<recipe id="…">` with:
  - `title`, `description` (`summary`, optional `tags/tag`)
  - optional `metadata` (`servings`, `prepTime`, `cookTime`, `totalTime`, `difficulty`)
  - optional `source` (text + optional `url`)
  - optional `category` (enumerated meal types)
  - `ingredients/ingredient` (`quantity`, `unit` attributes)
  - `preparation/step` (`number` attribute)
  - optional `created` (ISO dateTime)

`cookbook-pkg.py` validates against the XSD when the schema loads successfully and embeds validation status in the cookbook index.

## Generation scripts

| Script | Capability |
|--------|------------|
| `scripts/build-site.sh` | Root build: optional regen via Python, then copy `recipe-system/web` → `dist/` |
| `recipe-system/scripts/recipe-gen.py` | XML + `stylesheets/recipe-style.xsl` → `web/recipes/<name>.html` |
| `recipe-system/scripts/cookbook-pkg.py` | Scan XML → searchable `web/recipe-box.html` (client-side filter/search) |
| `recipe-system/scripts/recipe-web-generator.py` | Local CLI sample + optional Flask create UI |
| `recipe-system/scripts/meal-plan-generator.py` | CLI demo meal plans (hardcoded catalog; not XML-backed yet) |

Root npm scripts: `npm run build` / `npm run vercel-build` → `bash scripts/build-site.sh`.  
`npm run generate` runs `recipe-gen.py` then `cookbook-pkg.py` only.

## Static site output contract

After a successful build, **`dist/`** (and committed `recipe-system/web/`) must contain:

| Path | Contract |
|------|----------|
| `recipe-box.html` | Primary cookbook UI (required; build fails if missing) |
| `index.html` | Redirect / link to `recipe-box.html` |
| `recipes/<slug>.html` | One page per `recipes/<slug>.xml` |

Vercel serves `/` → `/recipe-box.html` via rewrite. Output directory is **`dist`** (root `vercel.json`), not `recipe-system/web` directly.

## Optional local Flask creator

- **Entry:** `recipe-web-generator.py --serve`
- **Gates:** `ENABLE_RECIPE_CREATE=true`, `FLASK_SECRET_KEY` (see `.env.example`)
- **Behavior:** Writes validated filenames (`[a-z0-9-]+.xml`) under `recipe-system/recipes/`; POST `/create` rejected off localhost
- **Boundary:** Not part of the Vercel deploy; filesystem is read-only there. After creating XML locally, run `npm run build` to refresh HTML.

Details: [SECURITY.md](../SECURITY.md).

## Meal-plan generator behavior

`meal-plan-generator.py` is a **CLI demo**, not a web route.

```bash
cd recipe-system/scripts
python3 meal-plan-generator.py --week 28 --year 2026
```

- Prints a weekday crockpot / weekend batch-BBQ themed week to stdout
- Uses an in-script recipe catalog and a small `HOLIDAYS` map (not live XML tags yet)
- `--week 52` prints a stub note for full-year generation

Out of scope today: HTML calendar export, shopping lists, browser planner in `recipe-box.html`.

## Deployment boundaries

| Target | What runs | What must not run |
|--------|-----------|-------------------|
| **Vercel** | `npm run build` → static `dist/`; security headers from root `vercel.json` | Flask creator, meal-plan CLI as a hosted service |
| **TrueNAS** | Clone/build via `scripts/truenas-deploy.sh` / [TRUENAS_DEPLOY.md](../TRUENAS_DEPLOY.md); serve `dist/` (or `web/`) with nginx or similar | Exposing Flask without auth |
| **Local preview** | `npm run build` then `python3 -m http.server` in `recipe-system/web` or `dist` | — |

Production model: **read-only static HTML**. Recipe changes = edit/commit XML → rebuild → redeploy.

## Planned (not current capabilities)

- Bulk recipe import with schema validation
- Browser meal planner / shopping lists
- Full 52-week calendar with holiday overrides reading the XML catalog

Track those in the README roadmap; do not assume they exist when automating against this repo.
