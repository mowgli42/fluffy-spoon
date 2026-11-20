# Tasks — pwa-offline-windows-app

Prototype slice first; production items stay open as Beads.

## Prototype (implement later — specs + beads created now)

| # | Task | Bead key | Status |
|---|------|----------|--------|
| # | Task | Bead ID | Status |
|---|------|---------|--------|
| 0 | OpenSpec behaviour-driven init + this change | `fluffy-spoon-c3j` | **closed** |
| 1 | Scaffold Svelte + Vite PWA shell; consume generated JSON | `fluffy-spoon-n9c` | pending (ready) |
| 2 | Web app manifest + icons; installability checklist (Edge/Chrome) | `fluffy-spoon-93f` | pending |
| 3 | Service worker via vite-plugin-pwa — app-shell precache | `fluffy-spoon-9vy` | pending |
| 4 | IndexedDB store for recipes + sample week/BBQ prep | `fluffy-spoon-d8b` | pending |
| 5 | Cache recipe images / static assets (allowlisted) | `fluffy-spoon-3rl` | pending |
| 6 | Vercel offline-viewing happy path (static export + seed) | `fluffy-spoon-0xw` | pending |
| 7 | Playwright: offline recipe view + screenshot artifact | `fluffy-spoon-pqj` | pending |
| 8 | DEMO.md — Vercel URL, local run, screenshot walkthrough | `fluffy-spoon-y5g` | pending |
| 9 | Promote exercised Gherkin from `@prototype` → `@validated` | `fluffy-spoon-vxb` | pending |

## Aspirational / production (do not implement in this prototype)

| # | Task | Bead ID |
|---|------|---------|
| A1 | Offline write queue + sync-on-reconnect | `fluffy-spoon-zvl` |
| P1 | Proper auth | `fluffy-spoon-le9` |
| P2 | Durable backend persistence beyond SQLite | `fluffy-spoon-c28` |
| P3 | Conflict resolution on sync | `fluffy-spoon-67z` |
| P4 | Microsoft Store MSIX via PWABuilder | `fluffy-spoon-uaf` |
| P5 | Observability | `fluffy-spoon-5fr` |
| P6 | Multi-device sync | `fluffy-spoon-di1` |

Epic: `fluffy-spoon-m0f`.

## Dependency sketch

```text
openspec-init
    └─► svelte-shell
            ├─► manifest-icons ─► sw-precache ─┬─► idb-seed ─► vercel-demo ─┬─► e2e-offline ─► demo-md
            │                                  └─► cache-assets ────────────┤
            │                                                               └─► gherkin-promote
            └─► offline-sync (aspirational; needs write API — blocked conceptually by prod-backend)
prod-* beads: no prototype blockers; track for rebuild only
```

Map to `bd` IDs after `bd create --graph` (see `BEADS.md`).
