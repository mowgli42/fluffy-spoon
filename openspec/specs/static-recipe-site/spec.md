# Static recipe site (baseline)

## Purpose

Capture **already-working** static cookbook behaviour so the PWA change does not rewrite history. Detailed Gherkin lives in root `features/*.feature`; this spec summarises the contract.

## Status

**Validated** by existing features and the current Vercel/static deploy path.

## Requirements

### Requirement: Static build output

The repository SHALL produce a static `dist/` suitable for Vercel.

#### Scenario: npm build produces dist (@validated)

- **GIVEN** committed files under `recipe-system/web/` including `recipe-box.html`
- **WHEN** `npm run build` runs from the repository root
- **THEN** `dist/recipe-box.html` exists
- **AND** recipe pages are available under `dist/recipes/`

### Requirement: Vercel demo surface

Vercel SHALL serve the cookbook without a local backend.

#### Scenario: Root rewrite to recipe box (@validated)

- **GIVEN** a successful deploy using root `vercel.json`
- **WHEN** a visitor requests `/`
- **THEN** the response is rewritten to `/recipe-box.html`

### Requirement: Searchable recipe index

Visitors SHALL filter recipes in the browser from embedded metadata.

#### Scenario: Search and filter (@validated)

- **GIVEN** `recipe-box.html` has been generated
- **WHEN** a visitor searches or activates difficulty/time filters
- **THEN** matching recipes remain visible and non-matches are hidden

### Requirement: Meal-plan CLI (not web)

Weekly meal plans SHALL be generable via CLI today; browser planner is out of baseline scope.

#### Scenario: Week plan on stdout (@validated)

- **GIVEN** `meal-plan-generator.py` is available
- **WHEN** it is run with `--week` and `--year`
- **THEN** a weekday/weekend-themed week prints to stdout
