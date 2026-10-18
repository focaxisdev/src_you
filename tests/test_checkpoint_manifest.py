"""Checkpoint validation using only synthetic files in platform temporary directories."""

import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import checkpoint_manifest as checkpoint  # noqa: E402


class CheckpointManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="checkpoint_test_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "root"
        self.root.mkdir()
        (self.root / "synthetic.txt").write_bytes(b"synthetic\n")
        self.manifest_path = self.root / "checkpoint-manifest.json"
        self.manifest = checkpoint.build_manifest(
            self.root, "synthetic", "fixture://synthetic", self.manifest_path)

    def verify(self, manifest=None, root=None):
        return checkpoint.verify_manifest(
            self.root if root is None else root,
            self.manifest if manifest is None else manifest, self.manifest_path)

    def assert_rejected_before_filesystem(self, manifest):
        with patch.object(checkpoint, "included_files") as inspect:
            self.assertTrue(checkpoint.verify_manifest(self.root, manifest, self.manifest_path))
            inspect.assert_not_called()

    def test_current_version_manifest_remains_valid(self):
        self.assertEqual(self.manifest["format_version"], "0.1.0")
        self.assertEqual(self.verify(), [])

    def test_create_rejects_invalid_metadata_without_overwriting_output(self):
        self.manifest_path.write_text("existing synthetic output", encoding="utf-8")
        for field in ("label", "scope"):
            for value in ("", "  "):
                args = argparse.Namespace(root=str(self.root), output=str(self.manifest_path),
                                          label="synthetic", scope="fixture://synthetic")
                setattr(args, field, value)
                with patch.object(checkpoint, "sha256") as hash_file, redirect_stdout(io.StringIO()):
                    self.assertEqual(checkpoint.command_create(args), 1)
                    hash_file.assert_not_called()
                self.assertEqual(self.manifest_path.read_text(encoding="utf-8"), "existing synthetic output")

    def test_create_rejects_unsafe_filename_without_hashing_or_overwriting(self):
        self.manifest_path.write_text("existing synthetic output", encoding="utf-8")
        args = argparse.Namespace(root=str(self.root), output=str(self.manifest_path),
                                  label="synthetic", scope="fixture://synthetic")
        with patch.object(checkpoint, "included_files", return_value=[self.root / "a:b.txt"]), \
                patch.object(checkpoint, "sha256") as hash_file, redirect_stdout(io.StringIO()):
            self.assertEqual(checkpoint.command_create(args), 1)
            hash_file.assert_not_called()
        self.assertEqual(self.manifest_path.read_text(encoding="utf-8"), "existing synthetic output")

    def test_cli_create_roundtrip(self):
        args = argparse.Namespace(root=str(self.root), output=str(self.manifest_path),
                                  label="synthetic", scope="fixture://synthetic")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checkpoint.command_create(args), 0)
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(self.verify(manifest), [])

    def test_each_required_field_is_required_before_filesystem_access(self):
        for field in self.manifest:
            with self.subTest(field=field):
                manifest = deepcopy(self.manifest)
                del manifest[field]
                self.assert_rejected_before_filesystem(manifest)

    def test_malformed_top_level_metadata_does_not_raise(self):
        for manifest in (None, [], "manifest", 0, True, {}, {"files": []}):
            with self.subTest(manifest=manifest):
                self.assert_rejected_before_filesystem(manifest)

    def test_metadata_values_are_validated(self):
        cases = {
            "format": (None, "other", []),
            "format_version": (None, "0.2.0", 1),
            "hash_algorithm": (None, "md5", "SHA256"),
            "label": (None, "", "  ", [], 1),
            "scope": (None, "", "\t", {}, False),
            "created_at": (None, "2026-10-18", "2026-10-18T12:00:00",
                           "2026-02-30T12:00:00+00:00", "2026-10-18T12:00:00+25:00",
                           "2026-10-18T12:00:00+00:99"),
            "file_count": (None, True, False, -1, 1.0, "1", [], 2),
            "total_bytes": (None, True, False, -1, 10.0, "10", {}, 11),
            "excluded": (None, "private-state", {}, [None], [""], [" "]),
            "files": (None, {}, "", [None], [1], [True], [[]]),
        }
        for field, values in cases.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    manifest = deepcopy(self.manifest)
                    manifest[field] = value
                    self.assert_rejected_before_filesystem(manifest)

    def test_timezone_iso_datetime_variants(self):
        for timestamp in ("2026-10-18T12:00:00Z", "2026-10-18T12:00:00.123+08:00"):
            self.manifest["created_at"] = timestamp
            self.assertEqual(self.verify(), [])

    def test_file_record_fields_are_required(self):
        for field in ("path", "bytes", "sha256"):
            manifest = deepcopy(self.manifest)
            del manifest["files"][0][field]
            self.assert_rejected_before_filesystem(manifest)

    def test_file_sizes_are_nonnegative_integers(self):
        for size in (None, True, False, -1, 1.0, "1", [], {}):
            manifest = deepcopy(self.manifest)
            manifest["files"][0]["bytes"] = size
            self.assert_rejected_before_filesystem(manifest)

    def test_digest_format(self):
        for digest in (None, [], 1, "f" * 63, "f" * 65, "x" * 64, "F" * 64):
            manifest = deepcopy(self.manifest)
            manifest["files"][0]["sha256"] = digest
            self.assert_rejected_before_filesystem(manifest)

    def test_unsafe_or_nonportable_paths(self):
        for relative in (None, [], {}, "", "/absolute", "../escape", "a/../b", "./a",
                         "a//b", "a/", "C:/a", "a\\b", "a\x00b", "a\x7fb", "a:b", "a?b",
                         "CON", "nul.txt", "a/COM1.log", "a.", "a "):
            with self.subTest(relative=relative):
                manifest = deepcopy(self.manifest)
                manifest["files"][0]["path"] = relative
                self.assert_rejected_before_filesystem(manifest)

    def test_duplicate_paths_are_rejected(self):
        self.manifest["files"].append(deepcopy(self.manifest["files"][0]))
        self.manifest["file_count"] *= 2
        self.manifest["total_bytes"] *= 2
        self.assert_rejected_before_filesystem(self.manifest)

    def test_empty_inventory_with_full_metadata_is_valid(self):
        (self.root / "synthetic.txt").unlink()
        manifest = checkpoint.build_manifest(self.root, "empty", "fixture://empty")
        self.assertEqual(self.verify(manifest), [])

    def test_missing_or_file_root_cannot_verify_as_empty(self):
        empty = deepcopy(self.manifest)
        empty.update(files=[], file_count=0, total_bytes=0)
        for root in (self.root / "missing", self.root / "synthetic.txt"):
            self.assertTrue(self.verify(empty, root))
            with self.assertRaises(ValueError):
                checkpoint.build_manifest(root, "empty", "fixture://empty")

    def test_same_size_tampering_is_detected(self):
        (self.root / "synthetic.txt").write_bytes(b"tampered!\n")
        self.assertIn("hash mismatch: synthetic.txt", self.verify())

    def test_missing_and_extra_files_are_detected(self):
        (self.root / "synthetic.txt").unlink()
        (self.root / "extra.txt").write_text("extra", encoding="utf-8")
        errors = self.verify()
        self.assertIn("missing files: synthetic.txt", errors)
        self.assertIn("unexpected files: extra.txt", errors)

    def make_symlink(self, path, target):
        try:
            path.symlink_to(target)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"symlink creation unavailable: {error}")

    def test_external_symlink_is_not_hashed(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("synthetic external file", encoding="utf-8")
        self.make_symlink(self.root / "linked.txt", outside)
        with patch.object(checkpoint, "sha256") as hash_file:
            self.assertTrue(self.verify())
            hash_file.assert_not_called()

    def test_looping_symlink_fails_safely(self):
        loop = self.root / "loop"
        self.make_symlink(loop, loop.name)
        with patch.object(checkpoint, "sha256") as hash_file:
            self.assertTrue(self.verify())
            hash_file.assert_not_called()
        create = argparse.Namespace(root=str(self.root), output=str(self.manifest_path),
                                    label="synthetic", scope="fixture://synthetic")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checkpoint.command_create(create), 1)
        self.assertFalse(self.manifest_path.exists())
        for args in (argparse.Namespace(root=str(loop), manifest=str(self.manifest_path)),
                     argparse.Namespace(root=str(self.root), manifest=str(loop))):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(checkpoint.command_verify(args), 1)

    def test_broken_symlink_fails_before_hashing(self):
        self.make_symlink(self.root / "broken", "missing")
        with patch.object(checkpoint, "sha256") as hash_file:
            self.assertTrue(self.verify())
            hash_file.assert_not_called()

    def test_loop_rejected_when_nonstrict_resolve_returns_unresolved_path(self):
        loop = self.root / "loop"
        self.make_symlink(loop, loop.name)
        resolve = Path.resolve

        def modern_resolve(path, strict=False):
            # Python 3.13+ non-strict resolution preserves unresolved loops.
            if path == loop and not strict:
                return path
            return resolve(path, strict=strict)

        with patch.object(Path, "resolve", modern_resolve), \
                patch.object(checkpoint, "sha256") as hash_file:
            self.assertTrue(self.verify())
            hash_file.assert_not_called()

    def test_file_read_error_fails_safely(self):
        with patch.object(checkpoint, "sha256", side_effect=PermissionError):
            self.assertIn("unable to read checkpoint file: synthetic.txt", self.verify())

    def test_cli_invalid_json_encoding_missing_or_unreadable_manifest(self):
        args = argparse.Namespace(root=str(self.root), manifest=str(self.manifest_path))
        for payload in (b"{", b"\xff", b"null", b"{}", b"[" * 2000):
            self.manifest_path.write_bytes(payload)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(checkpoint.command_verify(args), 1)
        self.manifest_path.unlink()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checkpoint.command_verify(args), 1)
        with patch.object(Path, "read_text", side_effect=PermissionError), redirect_stdout(io.StringIO()):
            self.assertEqual(checkpoint.command_verify(args), 1)

    def test_cli_integrity_success_does_not_claim_authority(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        output = io.StringIO()
        args = argparse.Namespace(root=str(self.root), manifest=str(self.manifest_path))
        with redirect_stdout(output):
            self.assertEqual(checkpoint.command_verify(args), 0)
        self.assertIn("Integrity only; authority and restore approval are not established.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
