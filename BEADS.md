# Beads — fluffy-spoon PWA programme

Source of truth: `bd list` / `bd ready`.  
Graph plan: `openspec/changes/pwa-offline-windows-app/beads-graph.json`.  
OpenSpec change: `openspec/changes/pwa-offline-windows-app/`.

## Epic

`fluffy-spoon-m0f` — PWA offline Windows app (prototype + production roadmap)

## Prototype chain

| Key | Bead ID | Priority | Depends on | Notes |
|-----|---------|----------|------------|-------|
| openspec-init | `fluffy-spoon-c3j` | P1 | — | **closed** — OpenSpec + Gherkin landed |
| svelte-shell | `fluffy-spoon-n9c` | P1 | openspec-init | **next** — Svelte+Vite shell + build-time JSON |
| manifest-icons | `fluffy-spoon-93f` | P1 | svelte-shell | Fluffy Spoon manifest + icons |
| sw-precache | `fluffy-spoon-9vy` | P1 | manifest-icons | vite-plugin-pwa app-shell |
| idb-seed | `fluffy-spoon-d8b` | P1 | sw-precache | IndexedDB recipes/plans seed |
| cache-assets | `fluffy-spoon-3rl` | P2 | sw-precache | Images/static allowlist |
| vercel-demo | `fluffy-spoon-0xw` | P1 | idb-seed, cache-assets | Static Vercel viewing path |
| e2e-offline | `fluffy-spoon-pqj` | P2 | vercel-demo | Playwright + screenshot |
| demo-md | `fluffy-spoon-y5g` | P2 | e2e-offline | DEMO.md walkthrough |
| gherkin-promote | `fluffy-spoon-vxb` | P2 | vercel-demo | `@prototype` → `@validated` |
| offline-sync | `fluffy-spoon-zvl` | P3 | idb-seed | Aspirational queue; related to prod-backend |

## Production rebuild (do not implement now)

| Key | Bead ID | Priority | Depends on | Notes |
|-----|---------|----------|------------|-------|
| prod-auth | `fluffy-spoon-le9` | P3 | — | Auth |
| prod-backend | `fluffy-spoon-c28` | P3 | — | Durable store beyond SQLite |
| prod-conflicts | `fluffy-spoon-67z` | P3 | offline-sync, prod-backend | Conflict policy |
| prod-msix | `fluffy-spoon-uaf` | P3 | related: manifest-icons | PWABuilder MSIX |
| prod-observability | `fluffy-spoon-5fr` | P3 | related: prod-backend | Metrics/logging |
| prod-multidevice | `fluffy-spoon-di1` | P3 | prod-auth, prod-conflicts | Multi-device sync |

## Production differences vs prototype

- API-backed IndexedDB hydration instead of build-time seed only.
- Real sync protocol + conflicts; not a stub queue.
- Auth-scoped data; observability on SW/sync failures.
- Optional Store packaging after web install works.
