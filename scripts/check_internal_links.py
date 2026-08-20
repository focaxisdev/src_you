#!/usr/bin/env python3
"""Check relative Markdown links and local anchors without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def github_slug(value: str) -> str:
    value = re.sub(r"[`*_~]", "", value.strip().lower())
    value = re.sub(r"[^\w\-\s]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", "-", value)


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    found: set[str] = set()
    counts: dict[str, int] = {}
    for heading in HEADING_RE.findall(text):
        base = github_slug(heading)
        count = counts.get(base, 0)
        found.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return found


def main() -> int:
    errors: list[str] = []
    checked = 0

    for source in sorted(ROOT.rglob("*.md")):
        if ".git" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                continue
            checked += 1
            if not parsed.path:
                destination = source
            else:
                destination = (source.parent / unquote(parsed.path)).resolve()
                try:
                    destination.relative_to(ROOT)
                except ValueError:
                    errors.append(f"link escapes repository: {source.relative_to(ROOT)} -> {target}")
                    continue

            if not destination.exists():
                errors.append(f"broken link: {source.relative_to(ROOT)} -> {target}")
                continue

            if parsed.fragment and destination.is_file() and destination.suffix.lower() == ".md":
                fragment = unquote(parsed.fragment).lower()
                if fragment not in anchors(destination):
                    errors.append(
                        f"missing anchor: {source.relative_to(ROOT)} -> {target}"
                    )

    if errors:
        print("Internal link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Internal link check passed: {checked} local links verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
