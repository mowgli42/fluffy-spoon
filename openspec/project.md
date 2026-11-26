# Fluffy Spoon — OpenSpec project

## What exists today

- **Static cookbook**: XML recipes under `recipe-system/recipes/` → HTML via Python generators → `dist/` for Vercel / TrueNAS.
- **Local tools**: optional Flask recipe creator (localhost only); `meal-plan-generator.py` CLI (not a web surface).
- **Behaviour specs**: root `features/*.feature` (build, recipe-box, recipe pages, meal-plan CLI).
- **Architecture doc**: `docs/OPENSPEC.md` (agent-oriented current-state map).

There is **no** Svelte app, FastAPI API, or SQLite persistence in the tree today.

## Prototype direction (this programme)

Change `pwa-offline-windows-app`: a **small Svelte + Vite PWA shell** that:

1. Consumes generated recipe / meal-plan JSON (or static HTML assets) from the existing build.
2. Ships a Web App Manifest + service worker for install + offline viewing.
3. Deploys as a Vercel demo without requiring a local backend for viewing.

## Production rebuild (Beads only — not this slice)

Auth, durable backend beyond SQLite, sync conflict resolution, Microsoft Store MSIX (PWABuilder), observability, multi-device sync.

## Spec hygiene

- Tag Gherkin `@validated` only after a demo run or automated check exercises the scenario.
- Leave install-on-Windows and offline-write-sync under `@aspirational` until proven.
- Capture deliberate simplifications in `openspec/LEARNINGS.md` and the change `design.md`.
