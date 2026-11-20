# Beads — fluffy-spoon PWA programme

Source of truth: `bd list` / `bd ready`.  
Graph plan: `openspec/changes/pwa-offline-windows-app/beads-graph.json`.  
OpenSpec change: `openspec/changes/pwa-offline-windows-app/`.

## Epic

`fluffy-spoon-m0f` — remains **open** while production child beads are open (prototype children closed).

## Prototype chain (done)

| Key | Bead ID | Status |
|-----|---------|--------|
| openspec-init | `fluffy-spoon-c3j` | closed |
| svelte-shell | `fluffy-spoon-n9c` | closed |
| manifest-icons | `fluffy-spoon-93f` | closed |
| sw-precache | `fluffy-spoon-9vy` | closed |
| idb-seed | `fluffy-spoon-d8b` | closed |
| cache-assets | `fluffy-spoon-3rl` | closed |
| vercel-demo | `fluffy-spoon-0xw` | closed |
| e2e-offline | `fluffy-spoon-pqj` | closed |
| demo-md | `fluffy-spoon-y5g` | closed |
| gherkin-promote | `fluffy-spoon-vxb` | closed |
| offline-sync | `fluffy-spoon-zvl` | closed (demo local flush only) |

## Production rebuild (open — do not implement in graham-bell slice)

| Key | Bead ID | Priority | Notes |
|-----|---------|----------|-------|
| prod-auth | `fluffy-spoon-le9` | P3 | Auth |
| prod-backend | `fluffy-spoon-c28` | P3 | Durable store beyond SQLite |
| prod-conflicts | `fluffy-spoon-67z` | P3 | Conflict policy |
| prod-msix | `fluffy-spoon-uaf` | P3 | PWABuilder MSIX |
| prod-observability | `fluffy-spoon-5fr` | P3 | Metrics/logging |
| prod-multidevice | `fluffy-spoon-di1` | P3 | Multi-device sync |

## Production differences vs prototype

- API-backed IndexedDB hydration instead of build-time seed only.
- Real sync protocol + conflicts; not a stub queue.
- Auth-scoped data; observability on SW/sync failures.
- Optional Store packaging after web install works.
