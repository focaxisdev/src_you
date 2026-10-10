"""Executable checks for the narrow deterministic demo, not LLM conformance."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import demo_memory_conflict as demo


class MemoryConflictDemoTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(demo.INPUT.read_text(encoding="utf-8"))
        self.records = self.fixture["canonical"]
        self.update = self.fixture["prepared_update"]

    def current(self, records):
        return demo.current_record(records, self.fixture["record_id"], self.fixture["scope"])

    def test_update_preserves_id_type_scope_and_one_current_value(self):
        updated = demo.apply_prepared_update(self.records, self.update)
        record = self.current(updated)
        for key in ("id", "type", "scope"):
            self.assertEqual(record[key], self.records[0][key])
        self.assertEqual(record["statement"], self.update["statement"])
        self.assertEqual(record["effective_from"], self.update["effective_from"])
        self.assertEqual(record["evidence"], self.update["evidence"])
        self.assertEqual(len(updated), 1)
        self.assertEqual(record["status"], "current")
        self.assertEqual(record["supersedes"]["status"], "superseded")
        self.assertEqual(record["supersedes"]["statement"], self.records[0]["statement"])

    def test_input_is_not_mutated(self):
        before = copy.deepcopy(self.records)
        demo.apply_prepared_update(self.records, self.update)
        self.assertEqual(self.records, before)

    def test_repeating_same_update_does_not_duplicate_history(self):
        once = demo.apply_prepared_update(self.records, self.update)
        self.assertEqual(demo.apply_prepared_update(once, self.update), once)

    def test_second_change_keeps_prior_history(self):
        once = demo.apply_prepared_update(self.records, self.update)
        next_update = dict(self.update, statement="Prefer focused meetings at midday.",
                           effective_from="2026-09-01")
        twice = demo.apply_prepared_update(once, next_update)
        self.assertEqual(self.current(twice)["supersedes"]["supersedes"]["statement"],
                         self.records[0]["statement"])

    def test_missing_or_ambiguous_current_record_is_rejected(self):
        for records in ([], self.records * 2,
                        [*self.records, dict(self.records[0], statement="A conflicting value.")],
                        [dict(self.records[0], status="superseded")]):
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.current(records)

    def test_scope_is_not_inferred_or_crossed(self):
        update = dict(self.update, scope="project:fictional")
        with self.assertRaises(ValueError):
            demo.apply_prepared_update(self.records, update)

    def test_wrong_id_is_not_created(self):
        update = dict(self.update, id="PREF-OTHER-001")
        with self.assertRaises(ValueError):
            demo.apply_prepared_update(self.records, update)

    def test_unconfirmed_temporary_or_unauthorized_update_is_rejected(self):
        for flag in ("confirmed", "durable", "authorized"):
            for value in (False, None, "true", 1):
                with self.subTest(flag=flag, value=value), self.assertRaises(ValueError):
                    demo.apply_prepared_update(self.records, dict(self.update, **{flag: value}))

    def test_other_scope_is_unchanged(self):
        other = dict(self.records[0], scope="project:fictional")
        result = demo.apply_prepared_update([*self.records, other], self.update)
        self.assertEqual(result[1], other)

    def test_fresh_read_uses_canonical_despite_stale_memory(self):
        result = demo.apply_prepared_update(self.records, self.update)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            reloaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(self.current(reloaded)["statement"], self.update["statement"])
        self.assertNotEqual(self.current(reloaded)["statement"], self.fixture["cached_memory"])

    def test_readme_excerpt_matches_actual_output(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        excerpt = readme.split("```text\n", 1)[1].split("```", 1)[0]
        self.assertIn(excerpt, demo.run_demo())

    def test_cli_matches_captured_output_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "demo_memory_conflict.py")],
                cwd=directory, capture_output=True, text=True, check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        expected = (demo.INPUT.parent / "output.txt").read_text(encoding="utf-8")
        self.assertEqual(completed.stdout, expected)
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
