"""Entirely synthetic fault-injection tests; no provider, network or user data."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from operational_contract import (  # noqa: E402
    Capabilities, Completion, Conflict, Evidence, Identity, Retrieval, Snapshot,
    Status, Unavailable, UncertainWrite, guarded_update, retrieval_action,
)


IDENTITY = Identity("synthetic-source", "SYNTHETIC-001", "global")
PASS = Evidence(Status.PASS, "synthetic probe")
READY = Capabilities(read=PASS, guarded_update=PASS, readback=PASS)


class SyntheticStore:
    """In-memory atomic backend with non-reused versions and injected faults."""

    def __init__(self):
        self.payload = {"preference": "Option A", "unrelated": "Value A"}
        self.version = 1
        self.events = []
        self.faults = []
        self.read_faults = {}
        self.read_count = 0

    def read(self, identity):
        self.events.append("read")
        self.read_count += 1
        fault = self.read_faults.get(self.read_count)
        if fault == "unavailable":
            raise Unavailable()
        if fault == "wrong-source":
            identity = Identity("other-synthetic-source", identity.record_id, identity.scope)
        if fault == "wrong-scope":
            identity = Identity(identity.source, identity.record_id, "project")
        if fault == "wrong-id":
            identity = Identity(identity.source, "SYNTHETIC-002", identity.scope)
        return Snapshot(identity, str(self.version), deepcopy(self.payload))

    def mutate(self, **changes):
        self.payload.update(changes)
        self.version += 1

    def guarded_update(self, identity, version, payload):
        self.events.append("update")
        assert identity == IDENTITY
        fault = self.faults.pop(0) if self.faults else None
        if fault == "disjoint-race":
            self.mutate(unrelated="Value B")
        if fault == "overlap-race":
            self.mutate(preference="Option C")
        if fault == "unavailable":
            raise Unavailable()
        if fault == "timeout-before":
            raise UncertainWrite()
        if version != str(self.version):
            raise Conflict()
        self.payload = deepcopy(payload)
        if fault != "unchanged-version":
            self.version += 1
        if fault == "corrupt":
            self.mutate(unrelated="unexpected synthetic mutation")
        if fault == "coerce-type":
            self.mutate(typed=1)
        if fault == "timeout-after":
            raise UncertainWrite()
        if fault == "timeout-and-race":
            self.mutate(unrelated="Value B")
            raise UncertainWrite()

    def create(self, *args):
        raise AssertionError("update must never fall back to create")


class GuardedUpdateTests(unittest.TestCase):
    def setUp(self):
        self.store = SyntheticStore()
        self.base = self.store.read(IDENTITY)
        self.store.events.clear()
        self.changes = {"preference": "Option B"}

    def run_update(self, **kwargs):
        return guarded_update(self.store, self.base, self.changes, READY, **kwargs)

    def test_exact_readback_and_identity(self):
        result = self.run_update()
        self.assertTrue(result.saved)
        self.assertEqual(result.snapshot.identity, IDENTITY)
        self.assertEqual(result.snapshot.payload, {
            "preference": "Option B", "unrelated": "Value A"})
        self.assertEqual(self.store.events, ["read", "update", "read"])

    def test_refresh_before_write_preserves_prior_unrelated_change(self):
        self.store.mutate(unrelated="Value B")
        self.assertTrue(self.run_update().saved)
        self.assertEqual(self.store.payload["unrelated"], "Value B")

    def test_race_guard_rejects_then_refresh_merge_preserves_unrelated(self):
        self.store.faults = ["disjoint-race"]
        result = self.run_update()
        self.assertTrue(result.saved)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(self.store.payload["unrelated"], "Value B")
        self.assertEqual(self.store.events, ["read", "update", "read", "update", "read"])

    def test_overlap_on_initial_refresh_blocks_without_write(self):
        self.store.mutate(preference="Option C")
        self.assertEqual(self.run_update().status, Status.BLOCKED)
        self.assertEqual(self.store.events, ["read"])

    def test_overlap_race_blocks_after_rejected_guard(self):
        self.store.faults = ["overlap-race"]
        result = self.run_update()
        self.assertFalse(result.saved)
        self.assertEqual(self.store.payload["preference"], "Option C")
        self.assertEqual(self.store.events, ["read", "update", "read"])

    def test_identical_concurrent_value_is_verified_noop(self):
        self.store.mutate(preference="Option B", unrelated="Value B")
        result = self.run_update()
        self.assertTrue(result.saved)
        self.assertEqual(result.attempts, 0)
        self.assertEqual(self.store.events, ["read"])

    def test_unknown_committed_outcome_reads_without_duplicate_write(self):
        self.store.faults = ["timeout-after"]
        self.assertTrue(self.run_update().saved)
        self.assertEqual(self.store.events, ["read", "update", "read"])

    def test_unknown_uncommitted_outcome_reads_before_retry(self):
        self.store.faults = ["timeout-before"]
        self.assertTrue(self.run_update().saved)
        self.assertEqual(self.store.events, ["read", "update", "read", "read", "update", "read"])

    def test_unknown_outcome_with_concurrent_change_stops_for_reconciliation(self):
        self.store.faults = ["timeout-and-race"]
        self.assertFalse(self.run_update().saved)
        self.assertEqual(self.store.events.count("update"), 1)

    def test_unknown_outcome_unreadable_does_not_retry(self):
        self.store.faults = ["timeout-after"]
        self.store.read_faults[3] = "unavailable"
        result = self.run_update()
        self.assertEqual(result.status, Status.BLOCKED)
        self.assertEqual(self.store.events.count("update"), 1)

    def test_acknowledgement_without_readback_is_not_saved(self):
        self.store.read_faults[3] = "unavailable"
        self.assertFalse(self.run_update().saved)

    def test_full_payload_readback_required(self):
        self.store.faults = ["corrupt"]
        self.assertFalse(self.run_update().saved)
        self.assertEqual(self.store.events.count("update"), 1)

    def test_mutation_requires_changed_version(self):
        self.store.faults = ["unchanged-version"]
        self.assertFalse(self.run_update().saved)

    def test_refresh_identity_mismatch_is_rejected(self):
        for fault in ("wrong-source", "wrong-scope", "wrong-id"):
            with self.subTest(fault=fault):
                self.setUp()
                self.store.read_faults[2] = fault
                self.assertEqual(self.run_update().status, Status.FAIL)
                self.assertNotIn("update", self.store.events)

    def test_readback_identity_mismatch_is_not_saved(self):
        for fault in ("wrong-source", "wrong-scope", "wrong-id"):
            with self.subTest(fault=fault):
                self.setUp()
                self.store.read_faults[3] = fault
                result = self.run_update()
                self.assertFalse(result.saved)
                self.assertEqual(result.status, Status.BLOCKED)
                self.assertEqual(self.store.events.count("update"), 1)

    def test_failed_update_has_no_create_fallback(self):
        self.store.faults = ["unavailable"]
        self.assertEqual(self.run_update().status, Status.BLOCKED)
        self.assertEqual(self.store.events, ["read", "update"])

    def test_refresh_unavailable_prevents_write(self):
        self.store.read_faults[2] = "unavailable"
        self.assertEqual(self.run_update().status, Status.BLOCKED)
        self.assertNotIn("update", self.store.events)

    def test_attempts_are_bounded(self):
        self.store.faults = ["timeout-before"] * 3
        self.assertEqual(self.run_update(max_attempts=2).attempts, 2)
        self.assertEqual(self.store.events.count("update"), 2)

    def test_inputs_not_mutated(self):
        base, changes = deepcopy(self.base), deepcopy(self.changes)
        self.run_update()
        self.assertEqual(self.base, base)
        self.assertEqual(self.changes, changes)

    def test_nested_overlapping_edits_are_not_silently_merged(self):
        self.store.payload["nested"] = {"left": "A", "right": "A"}
        self.base = self.store.read(IDENTITY)
        self.store.mutate(nested={"left": "A", "right": "B"})
        self.changes = {"nested": {"left": "B", "right": "A"}}
        self.assertFalse(self.run_update().saved)

    def test_missing_field_is_not_null(self):
        self.store.mutate(new_field=None)
        self.changes = {"new_field": "Option B"}
        self.assertFalse(self.run_update().saved)

    def test_invalid_request(self):
        for changes, limit in (({}, 3), (self.changes, 0)):
            with self.assertRaises(ValueError):
                guarded_update(self.store, self.base, changes, READY, max_attempts=limit)

    def test_boolean_integer_concurrent_change_is_an_overlap(self):
        self.store.payload["typed"] = 1
        self.base = self.store.read(IDENTITY)
        self.store.mutate(typed=True)
        self.changes = {"typed": 2}
        self.assertFalse(self.run_update().saved)
        self.assertIs(self.store.payload["typed"], True)

    def test_exact_readback_rejects_type_coercion(self):
        self.changes = {"typed": True}
        self.store.faults = ["coerce-type"]
        self.assertFalse(self.run_update().saved)

    def test_type_only_changes_are_not_noops_in_nested_json(self):
        for before, after in ((1, True), (1, 1.0), ([1], [True]),
                              ({"item": 1}, {"item": True})):
            with self.subTest(before=before, after=after):
                self.setUp()
                self.store.payload["typed"] = before
                self.base = self.store.read(IDENTITY)
                self.changes = {"typed": after}
                self.assertTrue(self.run_update().saved)
                self.assertEqual(self.store.events.count("update"), 1)

    def test_only_finite_json_payloads_are_accepted(self):
        for value in (float("nan"), float("inf"), (1, 2), {1: "value"}, {1, 2}):
            with self.subTest(kind=type(value).__name__), self.assertRaises(ValueError):
                guarded_update(self.store, self.base, {"typed": value}, READY)

    def test_prepared_lifecycle_history_survives_guarded_merge(self):
        old = {"statement": "Option A", "status": "current"}
        self.store.payload["record"] = old
        self.base = self.store.read(IDENTITY)
        self.store.mutate(unrelated="Value B")
        self.changes = {"record": {
            "statement": "Option B", "status": "current",
            "supersedes": dict(old, status="superseded")}}
        result = self.run_update()
        self.assertTrue(result.saved)
        self.assertEqual(result.snapshot.payload["record"], self.changes["record"])
        self.assertEqual(result.snapshot.payload["unrelated"], "Value B")


class EvidenceTests(unittest.TestCase):
    def test_create_does_not_imply_guarded_update(self):
        capabilities = Capabilities(read=PASS, create=PASS, readback=PASS)
        store = SyntheticStore()
        base = store.read(IDENTITY)
        store.events.clear()
        result = guarded_update(store, base, {"preference": "Option B"}, capabilities)
        self.assertEqual(result.status, Status.BLOCKED)
        self.assertEqual(store.events, [])

    def test_each_required_operation_must_independently_pass(self):
        for operation in ("read", "guarded_update", "readback"):
            for status in (Status.FAIL, Status.BLOCKED, Status.NOT_RUN):
                with self.subTest(operation=operation, status=status):
                    kwargs = dict(read=PASS, guarded_update=PASS, readback=PASS)
                    kwargs[operation] = Evidence(status)
                    self.assertFalse(Capabilities(**kwargs).update_ready())
        self.assertTrue(READY.update_ready())  # create is NOT_RUN

    def test_pass_requires_evidence_and_status_is_explicit(self):
        with self.assertRaises(ValueError):
            Evidence(Status.PASS)
        with self.assertRaises(ValueError):
            Evidence("success", "synthetic reference")

    def test_blocked_persistence_does_not_block_delivery(self):
        results = Completion(delivery=PASS, persistence=Evidence(Status.BLOCKED))
        self.assertEqual(results.delivery.status, Status.PASS)
        self.assertEqual(results.persistence.status, Status.BLOCKED)
        self.assertEqual(results.checkpoint.status, Status.NOT_RUN)

    def test_checkpoint_success_does_not_prove_canonical_persistence(self):
        results = Completion(checkpoint=PASS)
        self.assertEqual(results.persistence.status, Status.NOT_RUN)


class RetrievalTests(unittest.TestCase):
    def test_ordinary_task_skips_personal_sources(self):
        self.assertEqual(retrieval_action(needs_personal_state=False), Retrieval.SKIP)

    def test_verified_continuous_scope_can_reuse(self):
        self.assertEqual(retrieval_action(needs_personal_state=True,
                         verified_source=True, same_task_and_scope=True), Retrieval.REUSE)

    def test_unverified_or_different_scope_requires_refresh(self):
        for verified, same in ((False, True), (True, False), (False, False)):
            self.assertEqual(retrieval_action(needs_personal_state=True,
                             verified_source=verified, same_task_and_scope=same), Retrieval.REFRESH)

    def test_resume_change_conflict_and_write_invalidate_reuse(self):
        for event in ("resumed", "changed", "conflict", "writing"):
            with self.subTest(event=event):
                self.assertEqual(retrieval_action(needs_personal_state=True,
                                 verified_source=True, same_task_and_scope=True,
                                 **{event: True}), Retrieval.REFRESH)

    def test_write_always_requires_refresh(self):
        self.assertEqual(retrieval_action(needs_personal_state=False, writing=True), Retrieval.REFRESH)


if __name__ == "__main__":
    unittest.main()
