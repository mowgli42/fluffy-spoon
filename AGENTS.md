# AGENTS.md - guide for AI coding agents

## Project context

fluffy-spoon is a static recipe site with optional Python recipe tooling.
Read `README.md`, `docs/OPENSPEC.md`, `scripts/`, and the recipe data before changing generation logic.

## Local setup

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Smoke test

```bash
npm run build
.venv/bin/python -c "import lxml"
```

## Agent notes

- This repo has no package lockfile; do not use `npm ci` unless a lockfile is added intentionally.
- Keep committed static output consistent with generator changes.
- Preserve existing local user changes; stage only files you intentionally modify.

## Issue Tracking

This project uses **bd (beads)** for issue tracking. Run `bd prime` for workflow context, or install hooks with `bd hooks install` for automatic context injection.

Quick reference:

- `bd ready` - find unblocked work
- `bd create "Title" --type task --priority 2` - create an issue
- `bd close <id>` - close completed work
- `bd dolt push` - push Beads data when using a shared Beads remote

For full workflow details, run `bd prime`.
