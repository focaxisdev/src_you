#!/usr/bin/env python3
"""Validate the minimum src_you repository contract using only the stdlib."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/architecture.md",
    "docs/concepts.md",
    "docs/privacy-and-security.md",
    "docs/project-boundaries.md",
    "docs/conflict-resolution.md",
    "docs/backup-and-recovery.md",
    "docs/portability.md",
    "docs/related-work.md",
    "prompts/bootstrap.md",
    "prompts/audit-existing-system.md",
    "prompts/normalize.md",
    "prompts/checkpoint.md",
    "prompts/restore.md",
    "prompts/upgrade.md",
    "policies/retrieval-policy.md",
    "policies/update-policy.md",
    "policies/project-boundary-policy.md",
    "policies/conflict-resolution-policy.md",
    "policies/sensitive-data-policy.md",
    "policies/backup-policy.md",
    "adapters/chatgpt/README.md",
    "adapters/chatgpt/runtime-instructions.md",
    "adapters/chatgpt/project-integration.md",
    "adapters/chatgpt/capability-notes.md",
    "templates/src_you/00_SYSTEM_MANIFEST.md",
    "tests/acceptance-tests.md",
]

CORE_TEXT_FILES = [
    "README.md",
    "docs/architecture.md",
    "docs/concepts.md",
    "policies/retrieval-policy.md",
    "policies/update-policy.md",
    "policies/project-boundary-policy.md",
    "policies/conflict-resolution-policy.md",
    "policies/backup-policy.md",
    "prompts/bootstrap.md",
]

REQUIRED_TERMS = [
    "authoritative source",
    "canonical state",
    "durable state",
    "project detailed state",
    "global state",
    "superseded",
    "current",
    "checkpoint",
    "restore",
    "adapter",
]


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def empty_directories() -> list[Path]:
    result = []
    for directory in sorted(path for path in ROOT.rglob("*") if path.is_dir()):
        if ".git" in directory.parts:
            continue
        if not any(directory.iterdir()):
            result.append(directory)
    return result


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
        elif path.stat().st_size < 40:
            errors.append(f"required file is effectively empty: {relative}")

    for directory in empty_directories():
        errors.append(f"empty directory: {directory.relative_to(ROOT)}")

    acceptance = (ROOT / "tests/acceptance-tests.md").read_text(encoding="utf-8")
    for number in range(1, 13):
        if not re.search(rf"^## Test {number}\s+—", acceptance, flags=re.MULTILINE):
            errors.append(f"acceptance test {number} is missing")

    combined = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8").lower()
        for relative in CORE_TEXT_FILES
        if (ROOT / relative).is_file()
    )
    for term in REQUIRED_TERMS:
        if term not in combined:
            errors.append(f"required terminology not found in core files: {term}")

    stale_marker = re.compile(r"\b(" + "TO" + r"DO|" + "TB" + r"D|" + "FIX" + r"ME|lorem ipsum)\b", re.IGNORECASE)
    for path in markdown_files():
        matches = stale_marker.findall(path.read_text(encoding="utf-8"))
        if matches:
            errors.append(
                f"stale drafting marker in {path.relative_to(ROOT)}: {', '.join(sorted(set(matches)))}"
            )

    forbidden_brand_forms = ["Src" + "You", "SRC" + "_YOU", "src" + "-you"]
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for form in forbidden_brand_forms:
            if form in text:
                errors.append(f"non-canonical brand form {form!r} in {path.relative_to(ROOT)}")

    if errors:
        print("Structure validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Structure validation passed: {len(REQUIRED_FILES)} required files, "
        f"{len(markdown_files())} Markdown files, 12 acceptance tests."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
