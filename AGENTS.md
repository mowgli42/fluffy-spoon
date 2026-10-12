# fluffy-spoon

Static recipe cookbook: XML sources under `recipe-system/recipes/` generate searchable HTML via Python scripts, served from `dist/` on Vercel.

Stack: Python generators + static HTML/XML (no Svelte/FastAPI). Posture: ponytail (repo age >30 days).

Shared health pack: `.cursor/skills/` and `.cursor/rules/`. Follow for [Health] work.

## Commands

- Build site: `npm run build` (runs `scripts/build-site.sh` → `dist/`)
- Preview: `cd recipe-system/web && python3 -m http.server 8080` then open `/recipe-box.html`
- Meal-plan CLI: `cd recipe-system/scripts && python3 meal-plan-generator.py --week 28 --year 2026`
- Local creator (optional, disabled by default): `pip install -r recipe-system/scripts/requirements.txt` then `python3 recipe-web-generator.py --serve` after setting `ENABLE_RECIPE_CREATE=true` in `.env`
- Secrets: `bash scripts/scan-secrets.sh .`
- Beads: `bd ready` / `bd create "Title" --type task`

## Hard prohibitions

- Do not commit private keys, `*-key.pem`, `*.key`, `.env` secrets, or `BEGIN … PRIVATE KEY`. Generate locally; gitignore keys. Public certs OK.
- Do not expose Flask creator or meal-plan CLI as Vercel routes or hosted services. They are local-only. Keep production as read-only static HTML.
- Do not invent XML elements, attributes, or routes outside `recipe-system/schemas/recipe.xsd` and `docs/OPENSPEC.md`.
- Do not rewrite OpenSpec or Gherkin to claim unimplemented features (shopping lists, browser planner, bulk import). Update only when code already implements them.

## Verify by change type

| Change | Check |
| --- | --- |
| XML recipe or generator | `npm run build` succeeds; new/updated page appears under `dist/recipes/` |
| Spec / Gherkin | matching `features/*.feature` still describes current behavior |
| Deploy | https://fluffy-spoon-box.vercel.app/ returns HTTP 200 and links to `recipe-box.html` |
| Secrets / TLS | `bash scripts/scan-secrets.sh .` passes |

## Source of truth

- Behavior: `docs/OPENSPEC.md` + `features/*.feature`
- Remaining work: Beads (`.beads/`) or GitHub issues
- Health bar: do not duplicate SUCCESS_CRITERIA here

## House vocabulary

- `recipe-box.html` — primary searchable cookbook index. Do not call it "index.html" as the main entry.
- crockpot / weekend-batch / bbq-friendly — tags driving meal-plan rotation. Do not invent new tag schemes without updating the CLI catalog.
- meal-plan CLI — stdout weekly plan printer. Not a web endpoint.

## Borrowed patterns

- hard-prohibition from apache/airflow via ossrules.md — clear "do not" + alternative for local-only tools
- verification-matrix from debpalash/VoiceStudio via ossrules.md — change-type checks for build/deploy/spec
- single-source / house-vocabulary from browser-use and VoiceStudio — point at OpenSpec + real paths, use repo terms
