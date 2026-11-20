# Offline viewing — recipes, meal plans, BBQ prep

## Purpose

After a first online visit, users can open recipes, the current week plan, and BBQ prep lists without network.

## Status

**Prototype / aspirational** — not exercised yet. Vercel viewing without backend is `@prototype`.

## Requirements

### Requirement: Seeded client store

The PWA SHALL persist recipes and meal-plan seed data in IndexedDB (or equivalent) and cache shell assets.

### Requirement: Offline recipe detail

Ingredients, instructions, and images for previously available recipes SHALL render offline.

### Requirement: Offline week + BBQ prep

Current-week meals and BBQ prep items from the seed SHALL render offline.

### Requirement: Vercel demo without local backend

The hosted demo SHALL serve viewing from static (or serverless sample) assets only.
