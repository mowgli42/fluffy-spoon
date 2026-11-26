# Proposal: pwa-offline-windows-app

## Why

Share Fluffy Spoon as an installable Windows app (Edge/Chrome “Install this site as an app”) that still shows recipes, meal plans, and BBQ prep lists when offline. Demos must work on Vercel without asking visitors to run FastAPI or SQLite locally.

## What (prototype scope — graham-bell)

- Initialise behaviour-driven OpenSpec for this change (this folder).
- **Svelte + Vite PWA shell** (option B) that consumes **build-time JSON** (and/or static assets) produced from the existing recipe / meal-plan pipeline.
- Web App Manifest: name **Fluffy Spoon**, icons, `start_url`, `display: "standalone"`, theme colors.
- Service worker via **vite-plugin-pwa** (Workbox) precaching the app shell and seeded offline data.
- IndexedDB (or equivalent) for structured recipes + sample 52-week / BBQ prep views; Cache API for shell + images.
- Vercel-hosted static (or lightly serverless sample-data) surface for the **offline viewing** happy path after first visit.
- Gherkin clearly tagged `@validated` vs `@aspirational` / `@prototype`.
- Beads roadmap for production rebuild items (auth, durable backend, sync conflicts, MSIX, observability).

## Non-goals / out of scope (Beads only)

- Full rewrite of every static HTML page into Svelte.
- Real FastAPI + SQLite as the Vercel viewing path.
- Auth, multi-user sessions, multi-device sync, conflict resolution.
- Microsoft Store MSIX packaging (PWABuilder) in this slice.
- Guaranteeing automated Windows install-prompt E2E on CI (often not automatable).

## Success

- OpenSpec change + Gherkin + Beads exist and match reality.
- When the implementation slice lands: DEMO.md with Vercel URL, local run commands, and screenshot walkthrough; `@prototype` scenarios promoted to `@validated` only when exercised.
- Offline **viewing** of seeded recipes / current-week plan works without a backend; offline **write queue + sync** remains aspirational until a write API exists.

## Related

- Baseline: `openspec/specs/static-recipe-site/spec.md`, root `features/*.feature`, `docs/OPENSPEC.md`
- Learnings: `openspec/LEARNINGS.md`
