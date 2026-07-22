# Automation Safety

Use this reference for Leantime plugins that mutate records from events, hooks, cron jobs, webhooks, API calls, MCP tools, background jobs, or scheduled syncs.

## Required Safety Model

Before writing mutating automation, define:

- trigger source: hook, cron, webhook, UI action, API, MCP, or manual button
- event identity: event id, source id, timestamp, object id plus state version, or generated idempotency key
- mutation target: tickets, milestones, comments, time entries, projects, users, settings, files, or external systems
- failure policy: retry, skip, compensate, or require manual review
- audit trail: what changed, why, by whom/what, and when

## Idempotency

Every mutating automation must handle replay safely.

Patterns:

- store processed event ids
- write idempotency keys with mutation records
- check current state before writing
- use compare-and-set style guards when available
- make duplicate notification/comment/time-entry creation impossible

## Concurrency And Transactions

For actions that can overlap:

- decide lock scope: global, project, ticket, user, external-account, or event
- keep transactions short
- never hold a lock across slow external calls
- re-read state after acquiring a lock
- make partial failure visible in logs or audit records

## Dry Run And Audit

For non-trivial automation, add:

- dry-run mode that reports intended mutations
- audit log entries for real mutations
- clear error logging with object ids
- admin-visible status when feasible

## Test Matrix

Test or explicitly document:

- first execution
- exact replay of the same event
- retry after transient failure
- two concurrent triggers for the same object
- stale read followed by newer user edit
- partial failure after one of multiple mutations
- disable/re-enable plugin behavior

## Red Flags

- Happy-path tests only.
- Automation writes comments, time entries, or status changes without dedupe.
- Webhooks have no signature/authentication check.
- Cron job mutates every matching record without recording last processed state.
- Error handling logs a message but leaves data half-updated.
