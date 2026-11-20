# Verification — pwa-offline-windows-app

## How scenarios become `@validated`

| Tag | Meaning | Evidence required |
|-----|---------|-------------------|
| `@validated` | Exercised on this prototype | Manual checklist pass **or** Playwright/CI log; note date in LEARNINGS or DEMO.md |
| `@prototype` | Intended for the next implementation slice | Promote when evidence exists |
| `@aspirational` / `@future` | Production or deferred | Remains until a later change |

## Prototype verification plan (when implementing)

1. **Manifest**: `curl` / browser Application panel — name `Fluffy Spoon`, `display: standalone`, icons present.
2. **Service worker**: registers; offline reload shows shell + seeded list.
3. **IndexedDB**: Application panel shows recipes / week seed after first online visit.
4. **Vercel**: production URL loads without local backend; Lighthouse installable (or equivalent checklist).
5. **Windows install** (manual): Edge or Chrome → Install → Start menu entry → standalone window — screenshot to `docs/demo/` when available.
6. **Playwright**: go offline after first load; open a seeded recipe; attach screenshot artifact.

## Currently validated (baseline only)

See `openspec/specs/static-recipe-site/spec.md` and root `features/*.feature`. **No PWA scenarios are validated yet.**
