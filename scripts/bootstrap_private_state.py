#!/usr/bin/env python3
"""Copy the src_you scaffold to a private location outside this public repo."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "src_you"


class DestinationError(ValueError):
    """Raised when a destination could expose or overwrite private state."""


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_destination(raw_destination: str) -> Path:
    destination = Path(raw_destination).expanduser().resolve()
    if destination == Path(destination.anchor):
        raise DestinationError("destination cannot be a filesystem root")
    if is_within(destination, ROOT):
        raise DestinationError(
            "destination must be outside the public framework repository"
        )
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise DestinationError("destination already exists and is not an empty directory")
    return destination


def template_files() -> list[Path]:
    return sorted(path for path in TEMPLATE.rglob("*") if path.is_file())


def copy_scaffold(destination: Path) -> int:
    shutil.copytree(TEMPLATE, destination, dirs_exist_ok=True)
    return len(template_files())


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="src_you_bootstrap_") as temporary:
        destination = Path(temporary) / "private-state"
        validated = validate_destination(str(destination))
        copied = copy_scaffold(validated)
        actual = sorted(path for path in validated.rglob("*") if path.is_file())
        if copied != len(actual) or copied != len(template_files()):
            print("Bootstrap self-test failed: copied inventory is incomplete.")
            return 1
        if not (validated / "00_SYSTEM_MANIFEST.md").is_file():
            print("Bootstrap self-test failed: manifest is missing.")
            return 1

        nonempty = Path(temporary) / "nonempty"
        nonempty.mkdir()
        (nonempty / "existing.txt").write_text("synthetic", encoding="utf-8")
        try:
            validate_destination(str(nonempty))
        except DestinationError:
            pass
        else:
            print("Bootstrap self-test failed: non-empty destination was accepted.")
            return 1

    try:
        validate_destination(str(ROOT / "private-state-self-test"))
    except DestinationError:
        pass
    else:
        print("Bootstrap self-test failed: in-repository destination was accepted.")
        return 1

    try:
        validate_destination(str(Path(ROOT.anchor)))
    except DestinationError:
        pass
    else:
        print("Bootstrap self-test failed: filesystem root was accepted.")
        return 1

    print(
        "Private-state bootstrap self-test passed: complete copy, overwrite guard, "
        "root guard, and public-repo isolation."
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("destination", nargs="?", help="private destination to create")
    result.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and list the operation without writing files",
    )
    result.add_argument(
        "--self-test",
        action="store_true",
        help="run isolated copy and safety checks",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if args.self_test:
        return self_test()
    if not args.destination:
        parser().error("destination is required unless --self-test is used")

    try:
        destination = validate_destination(args.destination)
    except DestinationError as error:
        print(f"Bootstrap refused: {error}.")
        return 2

    files = template_files()
    if args.dry_run:
        print(f"Dry run: would create {destination} with {len(files)} scaffold files.")
        print("No personal data or template values were written.")
        return 0

    copied = copy_scaffold(destination)
    print(f"Created {destination} with {copied} scaffold files.")
    print("Next: keep the location private and edit 00_SYSTEM_MANIFEST.md first.")
    print("Do not commit this private state into the public framework repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
