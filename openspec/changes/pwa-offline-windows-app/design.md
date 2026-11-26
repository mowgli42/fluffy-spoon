# Design — pwa-offline-windows-app (prototype)

## Shape

```text
recipe XML + meal-plan scripts
        │
        ▼
 build step emits JSON seed (+ keep/static HTML as needed)
        │
        ▼
 Svelte + Vite app (PWA)
   ├── manifest.webmanifest
   ├── service worker (vite-plugin-pwa / Workbox)
   ├── IndexedDB: recipes, week plans, BBQ prep, offline write queue (stub)
   └── Cache API: app shell, CSS/JS, images
        │
        ▼
 Vercel static output (dist) — viewing needs no backend
```

Local happy path: `npm`/`pnpm` in the Vite app → preview; optional existing `npm run build` for legacy static site until the shell owns `dist/`.

## Key decisions

| Decision | Choice | Why |
|----------|--------|-----|
| UI shell | **Svelte + Vite** | Matches preferred stack; small SPA for install/offline demo without rewriting generators |
| Data for demo | **Build-time JSON seed** | Vercel-friendly; no SQLite on the edge |
| Offline structure | **IndexedDB** | Query week plans / recipes by id; better than stuffing JSON only in Cache |
| Offline assets | **Cache API** via Workbox precache | App shell + images |
| SW tooling | **vite-plugin-pwa** | Standard Workbox integration; less hand-rolled SW risk |
| Sync | **Queue stub only** | No write API yet — mark sync scenarios `@aspirational` |
| Install proof | Manifest criteria + manual Windows checklist; Playwright for offline view | Install UI is browser/OS gated |

## Caching strategy (prototype)

1. **Precache**: shell HTML/JS/CSS, manifest, icons, seed JSON, small set of recipe images.
2. **Runtime**: stale-while-revalidate for images not in precache; navigation falls back to cached shell.
3. **Do not** unbounded-cache every navigation URL (quota risk).

## IndexedDB vs alternatives

| Store | Use here | Skip for now |
|-------|----------|--------------|
| IndexedDB | Recipes, 52-week sample, BBQ prep, pending mutations | — |
| Cache API | Opaque HTTP responses (shell, images) | Structured queries |
| localStorage | Tiny flags only | Large meal-plan payloads |
| SQLite WASM | — | Heavier; production-ish |

## Vercel demo surface

- Primary: static export of the Vite app + seeded data.
- Optional later: serverless route that returns the same sample JSON (not required for viewing if seed is baked in).
- Must not depend on Flask or local SQLite for the shared demo URL.

## Windows install experience

Criteria for installability (HTTPS, manifest, SW, icons). User flow: Edge/Chrome → Install → Start menu / taskbar → standalone window. Automated assertion of Start menu entry is **out of prototype CI**; capture screenshots in DEMO.md when exercised.

## Production rebuild differences

- Hydrate IndexedDB from authenticated API, not only build seed.
- Background Sync / periodic sync + conflict policy.
- Durable server store (not SQLite file on a laptop).
- Observability (SW update metrics, sync failures).
- PWABuilder → MSIX for Store if desired.
