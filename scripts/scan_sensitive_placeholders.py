#!/usr/bin/env python3
"""Baseline secret and personal-identifier scan for the public framework tree."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCANNER_RELATIVE = Path("scripts") / "scan_sensitive_placeholders.py"

TOKEN_PATTERNS = {
    "private key block": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"gh[psour]_[A-Za-z0-9]{20,}"),
    "OpenAI-style key": re.compile(r"sk-" + r"[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack token": re.compile(r"xox[abprs]-[A-Za-z0-9-]{20,}"),
    "JWT": re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    "Google API key": re.compile(r"AIza[A-Za-z0-9_-]{30,}"),
    "npm token": re.compile(r"npm_[A-Za-z0-9]{30,}"),
    "Google Drive object URL": re.compile(
        r"https?://(?:drive|docs)\.google\.com/(?:file/d|document/d|spreadsheets/d|presentation/d)/"
        r"[A-Za-z0-9_-]{20,}"
    ),
    "session credential assignment": re.compile(
        r"\b(?:session(?:_?id)?|cookie)\s*[:=]\s*[\"'][A-Za-z0-9%._~-]{16,}[\"']",
        re.IGNORECASE,
    ),
}

EMAIL_RE = re.compile(r"(?<![\w.-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<![A-Za-z0-9])(?:\+?\d[\d .()\-]{7,}\d)(?![A-Za-z0-9])")
LONG_HEX_RE = re.compile(r"(?<![A-Fa-f0-9])[A-Fa-f0-9]{40,}(?![A-Fa-f0-9])")

ALLOWED_EMAIL_SUFFIXES = ("@example.invalid", "@users.noreply.github.com")

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml", ".svg"}
SENSITIVE_FILE_NAMES = {".env", ".npmrc", "id_rsa", "id_ed25519", "credentials.json"}


def pattern_self_test() -> list[str]:
    samples = {
        "private key block": "-----BEGIN PRIVATE KEY-----",
        "GitHub token": "gh" + "p_" + "A" * 24,
        "OpenAI-style key": "sk-" + "A" * 24,
        "AWS access key": "AKIA" + "A" * 16,
        "Slack token": "xoxb-" + "A" * 24,
        "JWT": ".".join(["eyJ" + "A" * 9, "B" * 12, "C" * 12]),
        "Google API key": "AIza" + "A" * 32,
        "npm token": "npm_" + "A" * 32,
        "Google Drive object URL": (
            "https://drive.google.com/file/d/" + "A" * 24
        ),
        "session credential assignment": 'session_id="' + "A" * 20 + '"',
    }
    return [
        label
        for label, pattern in TOKEN_PATTERNS.items()
        if not pattern.search(samples[label])
    ]


def candidates(root: Path) -> list[Path]:
    result = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() == SELF or path.relative_to(root) == SCANNER_RELATIVE:
            continue
        if path.name in SENSITIVE_FILE_NAMES:
            result.append(path)
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            result.append(path)
    return sorted(result)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="public tree to scan; defaults to the repository containing this script",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Sensitive-pattern scan failed: root is not a directory: {root}")
        return 2

    findings: list[str] = []
    scanned = candidates(root)

    failed_patterns = pattern_self_test()
    if failed_patterns:
        for label in failed_patterns:
            findings.append(f"scanner self-test did not detect synthetic {label}")

    for path in scanned:
        relative = path.relative_to(root)
        if path.name in SENSITIVE_FILE_NAMES:
            findings.append(f"sensitive filename tracked in public tree: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"strict UTF-8 decode failed in {relative}")
            continue

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
        f"{len(TOKEN_PATTERNS)} token-pattern self-tests passed. "
        "A separate semantic privacy review is still required."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
