# Tasks — pwa-offline-windows-app

## Prototype

| # | Task | Bead ID | Status |
|---|------|---------|--------|
| 0 | OpenSpec behaviour-driven init + this change | `fluffy-spoon-c3j` | **closed** |
| 1 | Scaffold Svelte + Vite PWA shell; consume generated JSON | `fluffy-spoon-n9c` | **closed** |
| 2 | Web app manifest + icons; installability checklist (Edge/Chrome) | `fluffy-spoon-93f` | **closed** |
| 3 | Service worker via vite-plugin-pwa — app-shell precache | `fluffy-spoon-9vy` | **closed** |
| 4 | IndexedDB store for recipes + sample week/BBQ prep | `fluffy-spoon-d8b` | **closed** |
| 5 | Cache recipe images / static assets (allowlisted) | `fluffy-spoon-3rl` | **closed** |
| 6 | Vercel offline-viewing happy path (static export + seed) | `fluffy-spoon-0xw` | **closed** |
| 7 | Playwright: offline recipe view + screenshot artifact | `fluffy-spoon-pqj` | **closed** |
| 8 | DEMO.md — Vercel URL, local run, screenshot walkthrough | `fluffy-spoon-y5g` | **closed** |
| 9 | Promote exercised Gherkin from `@prototype` → `@validated` | `fluffy-spoon-vxb` | **closed** |
| A1 | Offline write queue + demo sync-on-reconnect | `fluffy-spoon-zvl` | **closed** (demo local flush; no remote API) |

Epic: `fluffy-spoon-m0f` — close when production roadmap is accepted or deferred explicitly.

## Production (do not implement in this prototype)

| # | Task | Bead ID |
|---|------|---------|
| P1 | Proper auth | `fluffy-spoon-le9` |
| P2 | Durable backend persistence beyond SQLite | `fluffy-spoon-c28` |
| P3 | Conflict resolution on sync | `fluffy-spoon-67z` |
| P4 | Microsoft Store MSIX via PWABuilder | `fluffy-spoon-uaf` |
| P5 | Observability | `fluffy-spoon-5fr` |
| P6 | Multi-device sync | `fluffy-spoon-di1` |
