#!/usr/bin/env python3
"""Require strict UTF-8 text without a BOM or replacement characters."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".json", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitignore", "LICENSE"}


def candidates() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES)
    )


def main() -> int:
    errors: list[str] = []
    scanned = candidates()
    for path in scanned:
        relative = path.relative_to(ROOT)
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"UTF-8 BOM is not allowed: {relative}")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"strict UTF-8 decode failed: {relative} ({error})")
            continue
        if "\ufffd" in text:
            errors.append(f"replacement character U+FFFD found: {relative}")

    if errors:
        print("UTF-8 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"UTF-8 validation passed: {len(scanned)} text files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
