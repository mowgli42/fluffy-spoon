# Verification — pwa-offline-windows-app

## How scenarios become `@validated`

| Tag | Meaning | Evidence required |
|-----|---------|-------------------|
| `@validated` | Exercised on this prototype | Manual checklist pass **or** Playwright/CI log; note date in LEARNINGS or DEMO.md |
| `@prototype` | Intended for the next implementation slice | Promote when evidence exists |
| `@aspirational` / `@future` | Production or deferred | Remains until a later change |

## Evidence (2026-11-20 America/New_York)

| Check | Result |
|-------|--------|
| `npm run build` → `dist/index.html`, `manifest.webmanifest`, `sw.js`, `data/seed.json`, `classic/` | pass |
| Playwright `pwa/e2e/offline-recipe.spec.ts` | pass |
| Screenshot `docs/demo/offline-recipe-view.png` | produced |
| Manifest name / standalone / theme | asserted in E2E |
| Windows Start-menu install | **not** automated — still `@aspirational` |
| Backend sync | demo local flush only — backend scenarios `@aspirational` |

## Commands

```bash
npm run build
npm run test:e2e
```
