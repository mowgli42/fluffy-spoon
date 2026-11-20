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
   Offline writes / sync stay aspirational until a write API exists.

## Implementation slice (2026-11-20)

1. **Seed export** — `export-pwa-seed.py` (stdlib XML) → `pwa/public/data/seed.json` (28 recipes, 52 weeks + BBQ prep). No lxml required for the PWA path.

2. **Fonts offline** — Dropped Google Fonts CDN; used a distinctive system stack so offline UI does not flash unstyled webfonts / CSP issues.

3. **Sync** — Mutation queue in IndexedDB; “sync” while online is a **local demo flush** (mark pending → synced). No remote backend. Gherkin for real backend sync remains `@aspirational`.

4. **Classic site** — Kept under `dist/classic/` so Vercel `/` is the PWA without deleting the searchable HTML cookbook.

5. **Playwright on Omarchy** — Chromium fallback build works; Windows Start-menu install still manual.

6. **vite-plugin-pwa** — Precaches shell + seed + icons; image runtime cache is SWR with a small maxEntries guard.

## Trade-offs to revisit

| Topic | Prototype lean | Revisit when |
|-------|----------------|--------------|
| IndexedDB vs Cache-only | IndexedDB for recipes/plans; Cache for shell + images | If query needs stay trivial |
| vite-plugin-pwa vs hand-rolled SW | Prefer vite-plugin-pwa with Svelte shell | If shell is abandoned |
| Seed JSON at build vs live API | Build-time seed for demo | Production sync |
| Windows install E2E | Manual checklist + Playwright offline view | Store / MSIX packaging |
| Recipe images | None in seed | Add allowlisted assets + Cache API |

## Validated so far

- Static build → `dist/` with PWA `index.html`, `manifest.webmanifest`, `sw.js`, `data/seed.json`, `classic/`.
- Manifest name Fluffy Spoon / standalone (Playwright).
- Offline shell + recipe detail + week + BBQ prep after first visit (Playwright + screenshot).
- Local demo mutation queue flush when online.

## Still aspirational

- Real Windows Start-menu install proof (screenshots welcome in `docs/demo/`).
- Backend sync / conflict resolution / auth / MSIX / multi-device (production beads).
