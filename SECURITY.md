# Security

## Vercel (static deployment)

The production site on Vercel is **read-only static HTML**. Recipe XML is compiled at build time; visitors cannot create or modify recipes through the deployed site.

Security headers (CSP, `X-Frame-Options`, etc.) are set in `vercel.json`.

## Local recipe creation (Flask)

The Flask app in `recipe-system/scripts/recipe-web-generator.py` writes XML to disk. It is **disabled by default** and intended for local development only.

| Control | Purpose |
|--------|---------|
| `ENABLE_RECIPE_CREATE=true` | Must be set to start the server |
| `FLASK_SECRET_KEY` | Required session signing secret |
| Bind to `127.0.0.1` | POST `/create` rejected when not on localhost |
| Input length limits | Reduces abuse and oversized payloads |
| Filename allowlist | Blocks path traversal when saving XML |

Do not expose this server to the public internet without authentication and a proper backend store.

## Risks addressed in this release

- **Stored XSS**: Recipe metadata rendered with `escapeHtml()` instead of raw template interpolation.
- **Open redirect / unsafe paths**: `openRecipe()` only allows `recipes/<slug>.html`.
- **Hardcoded Flask secret**: Removed; requires environment variable.
- **Arbitrary file write**: Filename validation and resolved-path check under `recipes/`.
- **Create link on production**: Shown only when `RECIPE_GENERATOR_URL` is explicitly set to `http(s)://…`.

## Recipe import (planned)

Importing external recipes will need schema validation, sanitization of text fields, and size limits. Track that work separately before enabling uploads on any hosted environment.
