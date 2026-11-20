# Offline write queue and sync

## Purpose

Queue simple writes (e.g. mark meal cooked) while offline and sync when connectivity returns.

## Status

**Aspirational** — no write API or mutation UI in the prototype viewing path. Do not mark Validated until a backend accepts sync payloads.

## Requirements

### Requirement: Queue offline mutations

The client SHALL enqueue local writes when offline.

### Requirement: Sync on reconnect

When online, queued mutations SHALL be sent to the backend and cleared on success.

### Requirement: Conflict policy (production)

Production rebuild SHALL define conflict resolution; out of prototype scope.
