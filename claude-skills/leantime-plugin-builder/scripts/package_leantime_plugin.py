#!/usr/bin/env python3
"""Validate (by default) and package a Leantime plugin folder as a zip file."""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path


SKIP_PARTS = {".git", "__pycache__", "node_modules", "vendor"}
SKIP_SUFFIXES = {".pyc", ".DS_Store"}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_PARTS for part in path.parts):
        return True
    if path.name in SKIP_SUFFIXES:
        return True
    return False


def run_validator(root: Path) -> int:
    validator = Path(__file__).resolve().parent / "validate_leantime_plugin.py"
    result = subprocess.run([sys.executable, str(validator), str(root)])
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_path")
    parser.add_argument("--out", default=".", help="Output directory for the zip file.")
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip the automatic validation pass. Only use once the user has explicitly accepted the risk.",
    )
    args = parser.parse_args()

    root = Path(args.plugin_path).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Plugin path is not a directory: {root}")
    if not (root / "composer.json").exists():
        raise SystemExit("Refusing to package: composer.json not found at plugin root.")

    if not args.skip_validate:
        print("Running validate_leantime_plugin.py before packaging...")
        if run_validator(root) != 0:
            raise SystemExit(
                "Refusing to package: validation reported errors. Fix them or rerun with --skip-validate "
                "only if the user has explicitly accepted the risk."
            )

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{root.name}.zip"

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file() and not should_skip(path):
                zf.write(path, Path(root.name) / path.relative_to(root))

    print(f"Created {archive}")
    print(f"After extraction, composer.json should be at app/Plugins/{root.name}/composer.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
