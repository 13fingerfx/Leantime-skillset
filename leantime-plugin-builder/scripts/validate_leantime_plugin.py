#!/usr/bin/env python3
"""Validate a Leantime plugin folder for structure and safety guardrails."""

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

    for required in [composer_path, register_path, root / "bootstrap.php", root / "Controllers", root / "Views", root / "Language"]:
        if not required.exists():
            errors.append(f"Missing required path: {rel(required, root)}")

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

    if register_path.exists():
        register = read(register_path)
        if "registerLanguageFiles" not in register:
            warnings.append("register.php does not register language files.")
        if plugin_name not in register:
            warnings.append("register.php does not mention the plugin folder/id name.")
        if "<?php" not in register[:20]:
            errors.append("register.php must start with PHP open tag.")

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

    for css in css_files:
        text = read(css)
        color_count = len(HARD_CODED_COLOR.findall(text))
        if color_count:
            warnings.append(f"{rel(css, root)} contains {color_count} hard-coded color value(s); prefer native Leantime classes/tokens.")

    looks_automated = bool(AUTOMATION_WORDS.search(combined) and MUTATION_WORDS.search(combined))
    if looks_automated:
        missing = [word for word in SAFETY_WORDS if word not in combined.lower()]
        if missing:
            warnings.append("Automation-like mutation code lacks visible safety terms: " + ", ".join(missing))

    docs = root / "Docs" / "plugin-notes.md"
    if not docs.exists():
        warnings.append("Missing Docs/plugin-notes.md with compatibility, UI, and automation-safety notes.")
    else:
        doc_text = read(docs).lower()
        for section in ["compatibility", "native ui", "automation safety"]:
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
