# Leantime Skillset

Codex skill for building, reviewing, validating, and packaging Leantime plugins.

The main skill is `leantime-plugin-builder`. It is designed for:

- Leantime plugins under `app/Plugins`
- automated workflow plugins
- visual functions, dashboard widgets, and UI tweaks
- JSON-RPC/API and MCP integrations
- upgrade-safe customization planning

This repository also includes a first plugin source under `plugins/CodexDashboard`.

## Why This Exists

Leantime plugins can install cleanly while still failing in three painful ways:

1. They depend on Leantime internals and break across upgrades.
2. They work technically but look unlike the native Leantime UI.
3. They automate record changes without idempotency, locking, audit logs, or replay tests.

This skill makes Codex check those risks before and after it creates plugin code.

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/13fingerfx/Leantime-skillset.git
mkdir -p ~/.codex/skills
cp -R Leantime-skillset/leantime-plugin-builder ~/.codex/skills/
```

Restart Codex or start a new task so the skill list refreshes.

## Use

Ask Codex for Leantime plugin work, for example:

```text
Use the Leantime plugin builder skill to create a dashboard plugin that shows overdue tasks by project.
```

```text
Use the Leantime plugin builder skill to add an automation that comments when a task is moved to Done, with replay-safe behavior.
```

```text
Use the Leantime plugin builder skill to review this plugin for upgrade safety and native UI fit.
```

## Included Tools

Scaffold a plugin:

```bash
python leantime-plugin-builder/scripts/scaffold_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow \
  --description "Focus workflow helper" \
  --kind ui --kind automation --kind dashboard
```

Validate a plugin:

```bash
python leantime-plugin-builder/scripts/validate_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow
```

Package a plugin:

```bash
python leantime-plugin-builder/scripts/package_leantime_plugin.py \
  /path/to/leantime/app/Plugins/FocusFlow \
  --out /tmp
```

## Included Plugin

`plugins/CodexDashboard` is a Leantime 3.9.8 starter plugin with:

- native dashboard widget registration
- a plugin settings page using Leantime layout classes
- dry-run ticket-status automation listener
- documented compatibility, native UI, and automation-safety notes

Build the plugin zip:

```bash
python leantime-plugin-builder/scripts/package_leantime_plugin.py \
  plugins/CodexDashboard \
  --out plugin-builds
```

Install by copying the extracted folder to:

```text
app/Plugins/CodexDashboard
```

Then enable it in Leantime:

```bash
php ./bin/leantime plugin:list
php ./bin/leantime plugin:enable --plugin=CodexDashboard
```

## References Used

- Leantime plugin development guide: <https://docs.leantime.io/development/plugin-development>
- Leantime plugin installation guide: <https://docs.leantime.io/installation/plugin-installation>
- Leantime JSON-RPC/API docs: <https://docs.leantime.io/api/usage>
- Leantime MCP docs: <https://docs.leantime.io/installation/leantime-mcp>
- Leantime repository: <https://github.com/Leantime/leantime>

## License

MIT for this Codex skillset.
