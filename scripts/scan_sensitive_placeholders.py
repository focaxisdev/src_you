#!/usr/bin/env python3
"""Baseline secret and personal-identifier scan for the public framework tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

TOKEN_PATTERNS = {
    "private key block": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"gh[psour]_[A-Za-z0-9]{20,}"),
    "OpenAI-style key": re.compile(r"sk-" + r"[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack token": re.compile(r"xox[abprs]-[A-Za-z0-9-]{20,}"),
    "JWT": re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
}

EMAIL_RE = re.compile(r"(?<![\w.-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<![A-Za-z0-9])(?:\+?\d[\d .()\-]{7,}\d)(?![A-Za-z0-9])")
LONG_HEX_RE = re.compile(r"(?<![A-Fa-f0-9])[A-Fa-f0-9]{40,}(?![A-Fa-f0-9])")

ALLOWED_EMAIL_SUFFIXES = ("@example.invalid", "@users.noreply.github.com")

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}


def candidates() -> list[Path]:
    result = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path == SELF:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            result.append(path)
    return sorted(result)


def main() -> int:
    findings: list[str] = []
    scanned = candidates()

    for path in scanned:
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(ROOT)

        for label, pattern in TOKEN_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label} pattern in {relative}")

        for match in EMAIL_RE.findall(text):
            if not match.lower().endswith(ALLOWED_EMAIL_SUFFIXES):
                findings.append(f"non-reserved email address in {relative}")

        # Long numeric sequences are reviewed as possible phones. ISO dates and
        # short fictional identifiers do not match this conservative pattern.
        for match in PHONE_RE.findall(text):
            digits = re.sub(r"\D", "", match)
            if 9 <= len(digits) <= 15:
                findings.append(f"possible phone number in {relative}")

        if LONG_HEX_RE.search(text):
            findings.append(f"long hash-like identifier in {relative}")

    if findings:
        print("Sensitive-pattern scan failed:")
        for finding in sorted(set(findings)):
            print(f"- {finding}")
        print("Review semantically; never print suspected secret values.")
        return 1

    print(
        f"Sensitive-pattern scan passed: {len(scanned)} public text files checked. "
        "A separate semantic privacy review is still required."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
