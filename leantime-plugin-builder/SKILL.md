---
name: leantime-plugin-builder
description: Build, modify, review, validate, and package Leantime plugins and Leantime UI customizations. Use when Codex works on Leantime, LeanTime, app/Plugins, leantime-plugin composer packages, Leantime JSON-RPC/API integrations, Leantime MCP integrations, dashboard widgets, visual/UI tweaks, automation plugins, workflow hooks, or upgrade-safe Leantime customization.
---

# Leantime Plugin Builder

## Core Rule

Treat every Leantime customization as three jobs, not one:

1. **Compatibility:** identify the target Leantime version and avoid undocumented internals unless the user accepts the upgrade risk.
2. **Native UI:** inspect existing Leantime templates/styles before adding visual changes, dashboards, widgets, or CSS.
3. **Automation safety:** make mutating workflow automation idempotent, auditable, retry-safe, and testable under replay/concurrency.

If a task only touches one track, still state that the other tracks are not applicable.

## Repository Orientation

When working inside a Leantime checkout:

1. Inspect `composer.json`, release tags, `app/Plugins/`, `app/Domain/`, `app/Core/`, `resources/`, `public/`, and existing plugin examples before editing.
2. Prefer official plugin extension points, event hooks/filters, controllers, views, language files, services, CLI commands, JSON-RPC, or MCP integration over core edits.
3. If core edits are unavoidable, label them as core patches and explain the upgrade cost before making them.
4. Keep plugin code under `app/Plugins/PluginName/` unless the user explicitly asks for a core patch.

Read these references only as needed:

- `references/plugin-development.md`: plugin structure, installation, routing, packaging, and common checks.
- `references/compatibility.md`: version-aware development and upgrade-risk rules.
- `references/native-ui.md`: visual/dashboard/widget/UI work.
- `references/automation-safety.md`: hooks, jobs, duplicate prevention, retries, audit trails, and tests.
- `references/api-mcp.md`: JSON-RPC, API keys, personal tokens, and MCP bridge integration.

## Creation Workflow

1. Classify the plugin: `ui`, `automation`, `api`, `mcp`, `dashboard`, `workflow`, `service`, or mixed.
2. Identify the target Leantime version from the checkout, installed app, docs, or user-provided deployment details.
3. Scaffold with `scripts/scaffold_leantime_plugin.py` when creating a new plugin.
4. Implement the smallest plugin surface that solves the request.
5. Run `scripts/validate_leantime_plugin.py` before packaging.
6. Package with `scripts/package_leantime_plugin.py` only after validation is clean or all warnings are explained.

Example scaffold:

```bash
python leantime-plugin-builder/scripts/scaffold_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow \
  --description "Focus workflow helper" \
  --kind ui --kind automation --kind dashboard
```

Example validation:

```bash
python leantime-plugin-builder/scripts/validate_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow
```

Example packaging:

```bash
python leantime-plugin-builder/scripts/package_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow \
  --out /tmp
```

## Required Design Gates

### Compatibility Gate

Before using a Leantime class, service, hook, route, asset loader, or API method:

1. Determine whether it is documented, already used by a bundled/plugin example, or internal.
2. Prefer documented surfaces.
3. If using internals, add a compatibility note in the plugin docs or final answer with the exact file/class coupled to the target version.
4. Avoid copying code from core into the plugin unless there is no supported extension point.

### Native UI Gate

Before visual work:

1. Inspect at least two nearby Leantime views/components that already solve a similar layout.
2. Reuse existing layout wrappers, button classes, typography scale, icon style, table/list patterns, modal behavior, and translation patterns.
3. Avoid hard-coded colors, isolated design systems, or large custom CSS files.
4. Verify mobile behavior and basic contrast for dashboard/widget outputs.

### Automation Safety Gate

Before mutating records from hooks, API calls, cron, webhooks, or MCP-triggered actions:

1. Define the event identity or idempotency key.
2. Record processed events or last-safe state.
3. Decide lock and transaction boundaries.
4. Add dry-run and audit logging for non-trivial data changes.
5. Test replay, retry, concurrent trigger, stale read, and partial failure paths.

## Output Expectations

For Leantime plugin work, end with:

- plugin path and install/package command
- target Leantime version or compatibility assumption
- validation result
- UI/native checks performed, when relevant
- automation safety checks performed, when relevant
- any intentional upgrade risks or undocumented internals used
