# CodexDashboard

Native Leantime 3.9.8 plugin for Codex-assisted workflow work.

## What It Adds

- `Codex Overview` dashboard widget
- `Codex Dashboard` menu/settings page
- dry-run listener for `TicketStatusUpdated`
- automation idempotency key shape: `ticket-status:{ticketId}:{status}`

The automation listener does not mutate comments in v0.1.0. It logs the intended action only. This is deliberate: persistent processed-event storage, lock/transaction boundaries, and replay/concurrency tests should be added inside the target Leantime instance before mutation is enabled.

## Install

Copy or extract this folder to:

```text
app/Plugins/CodexDashboard
```

Then enable it in Leantime:

```bash
php ./bin/leantime plugin:list
php ./bin/leantime plugin:enable --plugin=CodexDashboard
```

Or open Leantime as an admin and go to:

```text
Plugins > My Apps
```

Then activate `CodexDashboard` after the folder has been copied into `app/Plugins`.

## Validate

From the Codex skillset repo:

```bash
python leantime-plugin-builder/scripts/validate_leantime_plugin.py plugins/CodexDashboard
```

Expected result: OK with compatibility warnings for documented Leantime Core/Domain extension classes.
