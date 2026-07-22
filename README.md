# Leantime Skillset

Agent skills for building, reviewing, validating, and packaging Leantime plugins.

Two equivalent skills are included, one per agent:

- `leantime-plugin-builder/` — the original Codex skill.
- `claude-skills/leantime-plugin-builder/` — a Claude Code skill with the same
  design, plus a fourth **security** gate (secrets, unescaped output, SQL/command
  injection, webhook auth), a fix for a real gap in the Codex version (scaffolded
  plugins had no `routes.php`, so their controllers were unreachable), and a
  packaging script that validates automatically instead of only recommending it.

Both are designed for:

- Leantime plugins under `app/Plugins`
- automated workflow plugins
- visual functions, dashboard widgets, and UI tweaks
- JSON-RPC/API and MCP integrations
- upgrade-safe customization planning

This repository also includes a first plugin source under `plugins/CodexDashboard`.

## Why This Exists

Leantime plugins can install cleanly while still failing in four painful ways:

1. They depend on Leantime internals and break across upgrades.
2. They work technically but look unlike the native Leantime UI.
3. They automate record changes without idempotency, locking, audit logs, or replay tests.
4. They render external/user data unescaped, hard-code secrets, or expose a mutating route with no auth check.

Both skills make the agent check those risks before and after it creates plugin code. (The Codex skill predates the fourth check; the Claude skill adds it explicitly — see below.)

## Install

### Codex

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/13fingerfx/Leantime-skillset.git
mkdir -p ~/.codex/skills
cp -R Leantime-skillset/leantime-plugin-builder ~/.codex/skills/
```

Restart Codex or start a new task so the skill list refreshes.

### Claude Code

Copy the Claude skill folder into your personal skills directory, or into a
project's `.claude/skills/` to scope it to that repo:

```bash
git clone https://github.com/13fingerfx/Leantime-skillset.git
mkdir -p ~/.claude/skills
cp -R Leantime-skillset/claude-skills/leantime-plugin-builder ~/.claude/skills/
```

Start a new Claude Code session so the skill list refreshes, then invoke it
with `/leantime-plugin-builder` or by describing Leantime plugin work.

## Use

Ask your agent for Leantime plugin work, for example:

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

Both skills ship the same three scripts (`scripts/scaffold_leantime_plugin.py`,
`scripts/validate_leantime_plugin.py`, `scripts/package_leantime_plugin.py`)
under their own skill folder — `leantime-plugin-builder/` for Codex,
`claude-skills/leantime-plugin-builder/` for Claude Code. The examples below
use the Codex path; swap in the Claude path to run the improved versions.

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

Package a plugin (the Claude version validates automatically first and
refuses to package on hard errors unless you pass `--skip-validate`):

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
