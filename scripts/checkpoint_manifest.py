#!/usr/bin/env python3
"""Create or verify SHA-256 inventories; integrity is not authority or restore approval."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EXCLUDED_PARTS = {".git", "__pycache__", ".venv", "venv", "private-state", "local-state"}
DEFAULT_EXCLUDED_NAMES = {"checkpoint-manifest.json", ".DS_Store"}


def safe_relative_path(value: object) -> bool:
    """Accept unambiguous relative paths portable across common filesystems."""
    if not isinstance(value, str) or not value:
        return False
    for part in value.split("/"):
        if (part in {"", ".", ".."} or part.endswith((".", " "))
                or any(ord(char) < 32 or ord(char) == 127 or char in '<>:"\\|?*' for char in part)
                or re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])", part.split(".")[0])):
            return False
    return True


def validate_manifest(manifest: object) -> list[str]:
    """Validate metadata without inspecting the filesystem."""
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    errors = []
    for field, expected in (("format", "src_you-checkpoint-manifest"),
                            ("format_version", "0.1.0"), ("hash_algorithm", "sha256")):
        if manifest.get(field) != expected:
            errors.append(f"unsupported or missing manifest {field}")
    for field in ("label", "scope"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"manifest {field} must be a nonempty string")
    created_at = manifest.get("created_at")
    try:
        if (not isinstance(created_at, str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)", created_at)
                or datetime.fromisoformat(created_at.replace("Z", "+00:00")).utcoffset() is None):
            raise ValueError
    except ValueError:
        errors.append("manifest created_at must be a timezone-aware ISO datetime")
    for field in ("file_count", "total_bytes"):
        value = manifest.get(field)
        if type(value) is not int or value < 0:
            errors.append(f"manifest {field} must be a nonnegative integer")
    excluded = manifest.get("excluded")
    if not isinstance(excluded, list) or any(
            not isinstance(item, str) or not item.strip() for item in excluded):
        errors.append("manifest excluded must be a list of nonempty strings")
    files = manifest.get("files")
    if not isinstance(files, list):
        return errors + ["manifest files must be a list"]
    seen = set()
    total_bytes = 0
    valid_sizes = True
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            errors.append(f"manifest files[{index}] must be an object")
            valid_sizes = False
            continue
        relative = item.get("path")
        if not safe_relative_path(relative):
            errors.append(f"manifest files[{index}] has an unsafe relative path")
        elif relative in seen:
            errors.append(f"duplicate manifest path: {relative}")
        else:
            seen.add(relative)
        size = item.get("bytes")
        if type(size) is not int or size < 0:
            errors.append(f"manifest files[{index}] bytes must be a nonnegative integer")
            valid_sizes = False
        else:
            total_bytes += size
        digest = item.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"manifest files[{index}] sha256 must be 64 lowercase hex digits")
    if type(manifest.get("file_count")) is int and manifest["file_count"] != len(files):
        errors.append("manifest file_count does not match inventory")
    if valid_sizes and type(manifest.get("total_bytes")) is int and manifest["total_bytes"] != total_bytes:
        errors.append("manifest total_bytes does not match inventory")
    return errors


def included_files(root: Path, manifest_path: Path | None = None) -> list[Path]:
    if not root.is_dir():
        raise ValueError("checkpoint root must be an existing directory")
    resolved_root = root.resolve()
    files = []
    for path in root.rglob("*"):
        if any(part in DEFAULT_EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        if path.name in DEFAULT_EXCLUDED_NAMES:
            continue
        if path.is_symlink() and not path.resolve(strict=True).is_relative_to(resolved_root):
            raise ValueError("checkpoint contains a symlink outside its root")
        if not path.is_file():
            continue
        if manifest_path and path.resolve() == manifest_path.resolve():
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, label: str, scope: str, manifest_path: Path | None = None) -> dict:
    for field, value in (("label", label), ("scope", scope)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"manifest {field} must be a nonempty string")
    files = included_files(root, manifest_path)
    if any(not safe_relative_path(path.relative_to(root).as_posix()) for path in files):
        raise ValueError("checkpoint contains an unsafe or nonportable relative path")
    records = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        records.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})

    manifest = {
        "format": "src_you-checkpoint-manifest",
        "format_version": "0.1.0",
        "label": label,
        "scope": scope,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hash_algorithm": "sha256",
        "file_count": len(records),
        "total_bytes": sum(item["bytes"] for item in records),
        "excluded": sorted(DEFAULT_EXCLUDED_PARTS | DEFAULT_EXCLUDED_NAMES),
        "files": records,
    }
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def verify_manifest(root: Path, manifest: dict, manifest_path: Path) -> list[str]:
    errors = validate_manifest(manifest)
    if errors:
        return errors
    expected = {item["path"]: item for item in manifest["files"]}
    try:
        actual_paths = {
            path.relative_to(root).as_posix(): path for path in included_files(root, manifest_path)
        }
    except (OSError, ValueError, RuntimeError):
        return ["checkpoint root is unavailable, invalid, or contains an unsafe symlink"]

    if set(expected) != set(actual_paths):
        missing = sorted(set(expected) - set(actual_paths))
        extra = sorted(set(actual_paths) - set(expected))
        if missing:
            errors.append(f"missing files: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected files: {', '.join(extra)}")

    for relative in sorted(set(expected) & set(actual_paths)):
        path = actual_paths[relative]
        try:
            if path.stat().st_size != expected[relative]["bytes"]:
                errors.append(f"size mismatch: {relative}")
            if sha256(path) != expected[relative]["sha256"]:
                errors.append(f"hash mismatch: {relative}")
        except OSError:
            errors.append(f"unable to read checkpoint file: {relative}")
    return errors


def command_create(args: argparse.Namespace) -> int:
    try:
        root = Path(args.root).resolve()
        output = Path(args.output).resolve() if args.output else None
        manifest = build_manifest(root, args.label, args.scope, output)
        serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        if output:
            output.write_text(serialized, encoding="utf-8")
            print(f"Wrote {output} with {manifest['file_count']} files.")
        else:
            print(serialized, end="")
    except (OSError, ValueError, RuntimeError):
        print("Checkpoint creation failed: invalid metadata, unsafe paths, or unavailable files.")
        return 1
    return 0


def command_verify(args: argparse.Namespace) -> int:
    try:
        root = Path(args.root).resolve()
        manifest_path = Path(args.manifest).resolve()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, RuntimeError):
        print("Checkpoint verification failed: unable to read a valid JSON manifest.")
        return 1
    errors = verify_manifest(root, manifest, manifest_path)
    if errors:
        print("Checkpoint verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Checkpoint verified: {manifest['file_count']} files, "
        f"{manifest['total_bytes']} bytes, SHA-256."
    )
    print("Integrity only; authority and restore approval are not established.")
    return 0


def command_self_test(_: argparse.Namespace) -> int:
    with tempfile.TemporaryDirectory(prefix="src_you_checkpoint_") as temp:
        root = Path(temp)
        (root / "one.md").write_text("one\n", encoding="utf-8")
        (root / "nested").mkdir()
        (root / "nested" / "two.md").write_text("two\n", encoding="utf-8")
        manifest_path = root / "checkpoint-manifest.json"
        manifest = build_manifest(root, "self-test", "fixture://self-test", manifest_path)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        errors = verify_manifest(root, manifest, manifest_path)
        if errors:
            print("Checkpoint self-test failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        (root / "one.md").write_text("changed\n", encoding="utf-8")
        if not verify_manifest(root, manifest, manifest_path):
            print("Checkpoint self-test failed to detect tampering.")
            return 1
    print("Checkpoint manifest self-test passed, including tamper detection.")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create a deterministic manifest")
    create.add_argument("root")
    create.add_argument("--label", required=True)
    create.add_argument("--scope", required=True)
    create.add_argument("--output")
    create.set_defaults(func=command_create)

    verify = sub.add_parser("verify", help="verify a manifest against a tree")
    verify.add_argument("root")
    verify.add_argument("manifest")
    verify.set_defaults(func=command_verify)

    self_test = sub.add_parser("self-test", help="run an isolated integrity test")
    self_test.set_defaults(func=command_self_test)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
