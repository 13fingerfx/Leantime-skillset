#!/usr/bin/env python3
"""Scaffold a conservative Leantime plugin skeleton."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


KINDS = {"ui", "automation", "api", "mcp", "dashboard", "workflow", "service"}


def studly(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    name = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not name or not name[0].isalpha():
        raise SystemExit("Plugin name must contain letters and start with a letter after normalization.")
    return name


def slug(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    return "-".join(word.lower() for word in words)


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def composer(plugin: str, vendor: str, description: str) -> str:
    data = {
        "name": f"{vendor}/{slug(plugin)}",
        "description": description,
        "version": "0.1.0",
        "type": "leantime-plugin",
        "license": "MIT",
        "autoload": {"psr-4": {f"Leantime\\Plugins\\{plugin}\\": "/"}},
    }
    return json.dumps(data, indent=2) + "\n"


def register(plugin: str, route: str, kinds: set[str]) -> str:
    menu = ""
    if kinds & {"ui", "dashboard"}:
        menu = f"""
// Register a menu item. Adjust section/position to match the target Leantime version.
$registration->addMenuItem([
    'title' => '{route}.menu.title',
    'icon' => 'fa fa-plug',
    'tooltip' => '{route}.menu.tooltip',
    'href' => '/{route}/show',
], 'personal', [10]);
"""
    automation = ""
    if kinds & {"automation", "workflow"}:
        automation = """
// Automation guardrail: register hooks only after defining idempotency, locking,
// audit logging, and replay tests. See Docs/plugin-notes.md and references/automation-safety.md.
"""
    return f"""<?php

use Leantime\\Domain\\Plugins\\Services\\Registration;

$registration = app()->makeWith(Registration::class, ['pluginId' => '{plugin}']);

$registration->registerLanguageFiles(['en-US']);
{menu}{automation}
"""


def bootstrap(plugin: str) -> str:
    return f"""<?php

// Bootstrap for {plugin}. Keep this file small; prefer explicit services/controllers.
"""


def routes(plugin: str, route: str) -> str:
    return f"""<?php

use Illuminate\\Support\\Facades\\Route;
use Leantime\\Plugins\\{plugin}\\Controllers\\{plugin}Controller;

// GET-only scaffold route. Add POST/PATCH/DELETE routes here for mutating
// actions and keep them behind Leantime's normal auth middleware -- see
// references/security.md before adding anything that changes data.
Route::get('/{route}/show', [{plugin}Controller::class, 'show'])->name('{route}.show');
"""


def controller(plugin: str, route: str) -> str:
    return f"""<?php

namespace Leantime\\Plugins\\{plugin}\\Controllers;

use Leantime\\Core\\Controller\\Controller;

class {plugin}Controller extends Controller
{{
    public function show(): void
    {{
        $this->tpl->display('{route}::show');
    }}
}}
"""


def service(plugin: str, kinds: set[str]) -> str:
    notes = []
    if "automation" in kinds or "workflow" in kinds:
        notes.append("Add idempotency keys, locks, audit logs, dry-run mode, and replay tests before mutating records.")
    if "api" in kinds or "mcp" in kinds:
        notes.append("Keep tokens out of source control and validate response shapes before mutation.")
    notes.append("Validate/escape any user- or externally-supplied value before it reaches a template or query.")
    if not notes:
        notes.append("Keep business logic here instead of in controllers.")
    body = "\n    ".join(f"// {note}" for note in notes)
    return f"""<?php

namespace Leantime\\Plugins\\{plugin}\\Services;

class {plugin}Service
{{
    {body}
}}
"""


def view(route: str, kinds: set[str]) -> str:
    dashboard = ""
    if "dashboard" in kinds:
        dashboard = """
        <div class="row">
            <div class="col-md-12">
                <p>{{ __('""" + route + """.dashboard.empty_state') }}</p>
            </div>
        </div>
"""
    return """@extends($layout)

@section('content')
    <div class="pageheader">
        <div class="pageicon"><i class="fa fa-plug"></i></div>
        <div class="pagetitle">
            <h1>{{ __('""" + route + """.headline') }}</h1>
        </div>
    </div>

    <div class="maincontent">
        <div class="maincontentinner">
            <p>{{ __('""" + route + """.intro') }}</p>""" + dashboard + """
        </div>
    </div>
@endsection
"""


def language(route: str, plugin: str, kinds: set[str]) -> str:
    lines = [
        f'{route}.menu.title = "{plugin}"',
        f'{route}.menu.tooltip = "Open {plugin}"',
        f'{route}.headline = "{plugin}"',
        f'{route}.intro = "Configure this plugin to fit your Leantime workflow."',
    ]
    if "dashboard" in kinds:
        lines.append(f'{route}.dashboard.empty_state = "No dashboard data is available yet."')
    return "\n".join(lines) + "\n"


def docs(plugin: str, kinds: set[str]) -> str:
    lines = [
        f"# {plugin}",
        "",
        "## Compatibility",
        "",
        "- Target Leantime version: TODO",
        "- Undocumented internals used: none intended",
        "- Retest after upgrade: plugin list, enable/disable, routes, templates, API/MCP calls, automations",
        "",
        "## Native UI Checks",
        "",
        "- Nearby Leantime views inspected: TODO",
        "- Existing classes/components reused: TODO",
        "- Mobile/contrast validation: TODO",
        "",
        "## Automation Safety",
        "",
    ]
    if kinds & {"automation", "workflow"}:
        lines.extend([
            "- Trigger source: TODO",
            "- Idempotency key: TODO",
            "- Processed-event storage: TODO",
            "- Lock/transaction scope: TODO",
            "- Dry-run/audit behavior: TODO",
            "- Replay/retry/concurrency tests: TODO",
        ])
    else:
        lines.append("- Not applicable unless this plugin mutates records from hooks, cron, API, MCP, or webhooks.")
    lines.extend([
        "",
        "## Security",
        "",
        "- Mutating routes require auth: TODO",
        "- Output escaping reviewed (no `{!! !!}` on external/user data): TODO",
        "- Secrets kept out of source: TODO",
        "- Webhook signature/auth check (if applicable): TODO",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Destination plugin folder, e.g. app/Plugins/FocusFlow")
    parser.add_argument("--description", default="A Leantime plugin.")
    parser.add_argument("--vendor", default="custom")
    parser.add_argument("--kind", action="append", choices=sorted(KINDS), default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    destination = Path(args.path).expanduser().resolve()
    plugin = studly(destination.name)
    route = slug(plugin).replace("-", "")
    kinds = set(args.kind or ["ui"])

    destination.mkdir(parents=True, exist_ok=True)
    write_new(destination / "composer.json", composer(plugin, args.vendor, args.description), args.force)
    write_new(destination / "register.php", register(plugin, route, kinds), args.force)
    write_new(destination / "bootstrap.php", bootstrap(plugin), args.force)
    write_new(destination / "routes.php", routes(plugin, route), args.force)
    write_new(destination / "Controllers" / f"{plugin}Controller.php", controller(plugin, route), args.force)
    write_new(destination / "Services" / f"{plugin}Service.php", service(plugin, kinds), args.force)
    write_new(destination / "Templates" / "show.blade.php", view(route, kinds), args.force)
    write_new(destination / "Language" / "en-US.ini", language(route, plugin, kinds), args.force)
    write_new(destination / "Docs" / "plugin-notes.md", docs(plugin, kinds), args.force)

    print(f"Created Leantime plugin skeleton: {destination}")
    print("Next: fill TODOs, implement behavior, then run validate_leantime_plugin.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
