#!/usr/bin/env python3
"""Run every local src_you repository gate with the active Python interpreter."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("structure", ["scripts/validate_structure.py"]),
    ("UTF-8", ["scripts/check_utf8.py"]),
    ("internal links", ["scripts/check_internal_links.py"]),
    ("public-tree privacy patterns", ["scripts/scan_sensitive_placeholders.py"]),
    ("acceptance fixtures", ["scripts/validate_acceptance_fixtures.py"]),
    ("private-state bootstrap", ["scripts/bootstrap_private_state.py", "--self-test"]),
    ("checkpoint integrity", ["scripts/checkpoint_manifest.py", "self-test"]),
    ("public assets", ["scripts/validate_assets.py"]),
    ("deterministic memory-conflict demo",
     ["-m", "unittest", "discover", "-s", "tests", "-p", "test_memory_conflict_demo.py"]),
    ("operational contract",
     ["-m", "unittest", "discover", "-s", "tests", "-p", "test_operational_contract.py"]),
    ("execution reliability",
     ["-m", "unittest", "discover", "-s", "tests", "-p", "test_execution_reliability.py"]),
    ("checkpoint metadata",
     ["-m", "unittest", "discover", "-s", "tests", "-p", "test_checkpoint_manifest.py"]),
]


def main() -> int:
    for label, arguments in CHECKS:
        print(f"==> {label}", flush=True)
        completed = subprocess.run([sys.executable, *arguments], cwd=ROOT, check=False)
        if completed.returncode:
            print(f"Check failed: {label} (exit {completed.returncode}).")
            return completed.returncode
    print(f"All repository checks passed: {len(CHECKS)} gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
