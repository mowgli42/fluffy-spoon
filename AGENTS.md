# fluffy-spoon

Static recipe cookbook: XML sources under `recipe-system/recipes/` generate searchable HTML via Python scripts, served from `dist/` on Vercel. The Fluffy Spoon **PWA** (`pwa/`) is a Svelte + Vite installable shell that consumes build-time `seed.json` for offline recipes and meal plans.

Stack: Python generators + static HTML/XML + Svelte/Vite PWA (no FastAPI/SQLite on Vercel). Posture: ponytail (repo age >30 days).

Read `README.md`, `DEMO.md`, `docs/OPENSPEC.md`, and `openspec/` (behaviour-driven; change `pwa-offline-windows-app`) before changing generation or PWA logic.

Shared health pack: `.cursor/skills/` and `.cursor/rules/`. Follow for [Health] work.

## Commands

- Build site + PWA: `npm run build` (runs `scripts/build-site.sh` → `dist/` with PWA at `/` and classic under `/classic/`)
- Preview PWA: `npm run preview` then open http://127.0.0.1:4173/
- Dev HMR: `npm run dev`
- Classic preview: `cd recipe-system/web && python3 -m http.server 8080` then open `/recipe-box.html`
- Export PWA seed only: `npm run seed`
- E2E offline: `npm run test:e2e`
- Meal-plan CLI: `cd recipe-system/scripts && python3 meal-plan-generator.py --week 28 --year 2026`
- Local creator (optional, disabled by default): `pip install -r recipe-system/scripts/requirements.txt` then `python3 recipe-web-generator.py --serve` after setting `ENABLE_RECIPE_CREATE=true` in `.env`
- Secrets: `bash scripts/scan-secrets.sh .`
- Beads: `bd ready` / `bd create "Title" --type task`

## Hard prohibitions

- Do not commit private keys, `*-key.pem`, `*.key`, `.env` secrets, or `BEGIN … PRIVATE KEY`. Generate locally; gitignore keys. Public certs OK.
- Do not expose Flask creator or meal-plan CLI as Vercel routes or hosted services. They are local-only. Keep production as read-only static / PWA viewing.
- Do not invent XML elements, attributes, or routes outside `recipe-system/schemas/recipe.xsd` and `docs/OPENSPEC.md`.
- Do not rewrite OpenSpec or Gherkin to claim unimplemented features (shopping lists, real backend sync, auth). Update only when code already implements them. Tag aspirational scenarios clearly.

## Verify by change type

| Change | Check |
| --- | --- |
| XML recipe or generator | `npm run build` succeeds; page under `dist/classic/recipes/`; seed refreshed |
| PWA / offline | `npm run build` && `npm run test:e2e`; manifest name Fluffy Spoon / standalone |
| Spec / Gherkin | matching `features/*.feature` and `openspec/changes/.../features/` still describe current behavior |
| Deploy | https://fluffy-spoon-box.vercel.app/ returns HTTP 200; `/` is PWA, `/classic/` is legacy box |
| Secrets / TLS | `bash scripts/scan-secrets.sh .` passes |

## Source of truth

- Behavior: `docs/OPENSPEC.md` + `openspec/` + root `features/*.feature`
- Remaining work: Beads (`.beads/`) — see `BEADS.md`
- Demo: `DEMO.md`
- Health bar: do not duplicate SUCCESS_CRITERIA here

## House vocabulary

- PWA shell — Svelte app at `/` after build; installable via Edge/Chrome.
- `recipe-box.html` — classic searchable cookbook index under `/classic/`. Do not call the PWA entry "recipe-box".
- crockpot / weekend-batch / bbq-friendly — tags driving meal-plan rotation. Do not invent new tag schemes without updating the CLI catalog and seed exporter.
- meal-plan CLI — stdout weekly plan printer. Not a web endpoint.
- seed.json — build-time offline data for IndexedDB hydration.

## Borrowed patterns

- hard-prohibition from apache/airflow via ossrules.md — clear "do not" + alternative for local-only tools
- verification-matrix from debpalash/VoiceStudio via ossrules.md — change-type checks for build/deploy/spec
- single-source / house-vocabulary from browser-use and VoiceStudio — point at OpenSpec + real paths, use repo terms
