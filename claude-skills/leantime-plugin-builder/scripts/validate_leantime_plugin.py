#!/usr/bin/env python3
"""Validate a Leantime plugin folder for structure, safety, and security guardrails."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HARD_CODED_COLOR = re.compile(r"(#[0-9a-fA-F]{3,8}|rgba?\(|hsla?\()")
MUTATION_WORDS = re.compile(r"\b(insert|update|delete|save|create|remove|archive|complete|close|move)\b", re.I)
AUTOMATION_WORDS = re.compile(r"\b(cron|webhook|hook|event|automation|listener|schedule|mcp|jsonrpc|api)\b", re.I)
SAFETY_WORDS = ["idempot", "lock", "transaction", "audit", "dry-run", "dry run", "processed"]

UNESCAPED_BLADE = re.compile(r"\{!!\s*(?!__\()")
RAW_SUPERGLOBAL = re.compile(r"\$_(GET|POST|REQUEST|COOKIE)\b")
SQL_CONCAT = re.compile(
    r"""(SELECT|INSERT|UPDATE|DELETE)\b[^;'"]{0,200}["'][^"']*["']\s*\.\s*\$""",
    re.I,
)
DANGEROUS_CALL = re.compile(r"\b(eval|exec|shell_exec|passthru|system|unserialize)\s*\(")
SECRET_ASSIGNMENT = re.compile(
    r"""(api[_-]?key|secret|token|password|passwd)\s*['"]?\s*[:=]\s*['"][A-Za-z0-9_\-\.]{12,}['"]""",
    re.I,
)
MUTATING_ROUTE = re.compile(r"Route::(post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)['\"]", re.I)
MENU_HREF = re.compile(r"'href'\s*=>\s*'/?([^'\"]+)'")
ROUTE_PATH = re.compile(r"Route::\w+\s*\(\s*['\"]/?([^'\"]+)['\"]")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_path")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    args = parser.parse_args()

    root = Path(args.plugin_path).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists() or not root.is_dir():
        errors.append(f"Plugin path is not a directory: {root}")
    composer_path = root / "composer.json"
    register_path = root / "register.php"
    routes_path = root / "routes.php"

    for required in [composer_path, register_path, root / "bootstrap.php", root / "Controllers", root / "Templates", root / "Language"]:
        if not required.exists():
            errors.append(f"Missing required path: {rel(required, root)}")
    if not routes_path.exists() and (root / "Controllers").exists():
        warnings.append("Missing routes.php: controllers have no routes registered and will not be reachable.")

    plugin_name = root.name
    if not re.match(r"^[A-Z][A-Za-z0-9]*$", plugin_name):
        warnings.append("Plugin folder should be StudlyCase, e.g. FocusFlow.")

    if composer_path.exists():
        try:
            composer = json.loads(read(composer_path))
        except json.JSONDecodeError as exc:
            errors.append(f"composer.json is invalid JSON: {exc}")
            composer = {}
        if composer.get("type") != "leantime-plugin":
            errors.append('composer.json must include "type": "leantime-plugin".')
        autoload = composer.get("autoload", {}).get("psr-4", {})
        expected_prefix = f"Leantime\\Plugins\\{plugin_name}\\"
        if expected_prefix not in autoload:
            errors.append(f"composer.json PSR-4 must include {expected_prefix!r}.")

    register_text = ""
    if register_path.exists():
        register_text = read(register_path)
        if "registerLanguageFiles" not in register_text:
            warnings.append("register.php does not register language files.")
        if "Leantime\\Core\\Events\\Registration" in register_text:
            errors.append("register.php imports the old/wrong Registration namespace; use Leantime\\Domain\\Plugins\\Services\\Registration.")
        if plugin_name not in register_text:
            warnings.append("register.php does not mention the plugin folder/id name.")
        if "<?php" not in register_text[:20]:
            errors.append("register.php must start with PHP open tag.")

    # Menu items registered in register.php should have a matching route.
    if register_text:
        route_text = read(routes_path) if routes_path.exists() else ""
        registered_paths = {m.group(1).rstrip("/") for m in ROUTE_PATH.finditer(route_text)}
        for href_match in MENU_HREF.finditer(register_text):
            href = href_match.group(1).rstrip("/")
            href_base = href.split("?")[0]
            if href_base not in registered_paths and not any(href_base.startswith(p) for p in registered_paths):
                warnings.append(f"Menu href '/{href}' in register.php has no matching route in routes.php.")

    php_files = list(root.rglob("*.php"))
    blade_files = list(root.rglob("*.blade.php"))
    css_files = list(root.rglob("*.css"))
    all_text_files = php_files + blade_files + css_files + list(root.rglob("*.js"))
    combined = "\n".join(read(path) for path in all_text_files if path.is_file())

    normalized_core = combined.replace("Leantime\\Core\\Events\\Registration", "")
    normalized_core = normalized_core.replace("Leantime\\Core\\Controller\\Controller", "")
    if "app\\Core" in normalized_core or "Leantime\\Core" in normalized_core:
        warnings.append("Plugin references Leantime Core classes. Confirm this is a documented/stable extension surface.")
    if "app\\Domain" in combined or "Leantime\\Domain" in combined:
        warnings.append("Plugin references Leantime Domain classes. Add compatibility notes for upgrade safety.")

    for blade in blade_files:
        text = read(blade)
        if "__(" not in text:
            warnings.append(f"{rel(blade, root)} does not appear to use translation helpers.")
        if HARD_CODED_COLOR.search(text):
            warnings.append(f"{rel(blade, root)} contains hard-coded color values.")
        if UNESCAPED_BLADE.search(text):
            warnings.append(f"{rel(blade, root)} uses unescaped Blade output {{!! !!}}; confirm the value is trusted, never user/external data.")

    for css in css_files:
        text = read(css)
        color_count = len(HARD_CODED_COLOR.findall(text))
        if color_count:
            warnings.append(f"{rel(css, root)} contains {color_count} hard-coded color value(s); prefer native Leantime classes/tokens.")

    for php in php_files:
        text = read(php)
        name = rel(php, root)
        if RAW_SUPERGLOBAL.search(text):
            warnings.append(f"{name} reads a raw superglobal ($_GET/$_POST/etc); use Leantime's request helpers and validate input.")
        if SQL_CONCAT.search(text):
            errors.append(f"{name} appears to build SQL by concatenating a variable into a query string; use parameter binding.")
        if DANGEROUS_CALL.search(text):
            errors.append(f"{name} calls a dangerous function (eval/exec/shell_exec/system/unserialize); review for injection risk.")
        if SECRET_ASSIGNMENT.search(text):
            errors.append(f"{name} appears to hard-code a secret/API key/token/password; move it to env vars or settings storage.")

    if routes_path.exists():
        route_text = read(routes_path)
        for match in MUTATING_ROUTE.finditer(route_text):
            verb, path = match.group(1), match.group(2)
            if not re.search(r"auth|middleware|csrf|session", route_text, re.I):
                warnings.append(
                    f"routes.php registers a mutating {verb.upper()} route for '{path}' with no visible auth/middleware/csrf reference; confirm it runs behind Leantime's normal auth."
                )

    looks_automated = bool(AUTOMATION_WORDS.search(combined) and MUTATION_WORDS.search(combined))
    if looks_automated:
        missing = [word for word in SAFETY_WORDS if word not in combined.lower()]
        if missing:
            warnings.append("Automation-like mutation code lacks visible safety terms: " + ", ".join(missing))
        if "webhook" in combined.lower() and not re.search(r"signature|hmac|secret|shared[_-]?secret", combined, re.I):
            warnings.append("Webhook-handling code has no visible signature/shared-secret verification.")

    docs = root / "Docs" / "plugin-notes.md"
    if not docs.exists():
        warnings.append("Missing Docs/plugin-notes.md with compatibility, UI, automation-safety, and security notes.")
    else:
        doc_text = read(docs).lower()
        for section in ["compatibility", "native ui", "automation safety", "security"]:
            if section not in doc_text:
                warnings.append(f"Docs/plugin-notes.md missing section: {section}")

    if errors:
        print("ERRORS:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("OK: plugin structure and guardrail checks passed.")
    elif not errors:
        print("OK with warnings.")

    if errors or (warnings and args.strict):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
