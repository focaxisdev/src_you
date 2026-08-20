#!/usr/bin/env python3
"""Create or verify deterministic SHA-256 checkpoint inventories."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EXCLUDED_PARTS = {".git", "__pycache__", ".venv", "venv", "private-state", "local-state"}
DEFAULT_EXCLUDED_NAMES = {"checkpoint-manifest.json", ".DS_Store"}


def included_files(root: Path, manifest_path: Path | None = None) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        if path.name in DEFAULT_EXCLUDED_NAMES:
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
    records = []
    for path in included_files(root, manifest_path):
        relative = path.relative_to(root).as_posix()
        records.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})

    return {
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


def verify_manifest(root: Path, manifest: dict, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    expected = {item["path"]: item for item in manifest.get("files", [])}
    actual_paths = {
        path.relative_to(root).as_posix(): path for path in included_files(root, manifest_path)
    }

    if set(expected) != set(actual_paths):
        missing = sorted(set(expected) - set(actual_paths))
        extra = sorted(set(actual_paths) - set(expected))
        if missing:
            errors.append(f"missing files: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected files: {', '.join(extra)}")

    for relative in sorted(set(expected) & set(actual_paths)):
        path = actual_paths[relative]
        if path.stat().st_size != expected[relative].get("bytes"):
            errors.append(f"size mismatch: {relative}")
        if sha256(path) != expected[relative].get("sha256"):
            errors.append(f"hash mismatch: {relative}")

    if manifest.get("file_count") != len(expected):
        errors.append("manifest file_count does not match inventory")
    if manifest.get("total_bytes") != sum(item.get("bytes", 0) for item in expected.values()):
        errors.append("manifest total_bytes does not match inventory")
    return errors


def command_create(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    output = Path(args.output).resolve() if args.output else None
    manifest = build_manifest(root, args.label, args.scope, output)
    serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    if output:
        output.write_text(serialized, encoding="utf-8")
        print(f"Wrote {output} with {manifest['file_count']} files.")
    else:
        print(serialized, end="")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
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
