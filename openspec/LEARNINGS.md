# Learnings — fluffy-spoon PWA programme

Living notes. Update when a slice lands or a hypothesis fails.

## Starting constraints (2026-11)

1. **Stack mismatch vs. prompt**  
   Kickoff text assumed Svelte + FastAPI + SQLite. Repo is static XML→HTML + optional Flask + meal-plan CLI.  
   **Chose:** document honesty in OpenSpec; prototype a Svelte+Vite shell (option B) on top of generated data; leave FastAPI/SQLite as production beads.

2. **OpenSpec bootstrap**  
   Had `docs/OPENSPEC.md` + root `features/*.feature`, but no `openspec/` tree.  
   **Chose:** behaviour-driven `openspec/` (verified-xfer pattern) without deleting root features yet.

3. **Vercel boundary**  
   Viewing must work as static (or light serverless sample JSON). No writable filesystem, no Flask on Vercel.  
   Offline writes / sync stay aspirational until a real write API exists.

## Trade-offs to revisit

| Topic | Prototype lean | Revisit when |
|-------|----------------|--------------|
| IndexedDB vs Cache-only | IndexedDB for recipes/plans; Cache for shell + images | If query needs stay trivial |
| vite-plugin-pwa vs hand-rolled SW | Prefer vite-plugin-pwa with Svelte shell | If shell is abandoned |
| Seed JSON at build vs live API | Build-time seed for demo | Production sync |
| Windows install E2E | Manual checklist + Playwright offline view | Store / MSIX packaging |

## Validated so far

- Static build → `dist/` and Vercel rewrite (existing `features/static-site-build.feature`).
- Recipe-box search/filter and recipe pages (existing features).
- Meal-plan CLI week output (existing feature).

## Not validated

Anything under `@aspirational` / `@prototype` in `openspec/changes/pwa-offline-windows-app/features/`.
