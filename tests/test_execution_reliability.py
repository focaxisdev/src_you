"""Synthetic execution boundaries; no scheduler or provider behavior is claimed."""

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from execution_contract import (Entry, Failure, Policy, Recovery, RunEvidence,
                                recovery_action, validate_entry)
from operational_contract import (Evidence, Identity, InvalidContent, PermissionDenied,
                                  Snapshot, Status, TransientRead, Unavailable,
                                  guarded_update, read_with_retry)
from test_operational_contract import IDENTITY, PASS, READY, SyntheticStore


RULES = {
    Failure.TRANSIENT_READ: Recovery.RETRY_READ,
    Failure.PERMISSION_DENIED: Recovery.STOP,
    Failure.INVALID_CONTENT: Recovery.STOP,
    Failure.VERSION_CONFLICT: Recovery.REFRESH_MERGE,
    Failure.UNKNOWN_WRITE: Recovery.READBACK,
}
APPROVED = {"synthetic-execution": Policy("revision-2", RULES)}


class PolicyEntryTests(unittest.TestCase):
    def test_complete_current_loaded_policy(self):
        self.assertEqual(validate_entry(Entry({"synthetic-execution": "revision-2"}),
                                        APPROVED, APPROVED), [])

    def test_omitted_reference_is_detected_even_if_other_links_work(self):
        self.assertTrue(validate_entry(Entry({}), APPROVED, APPROVED))

    def test_stale_reference_does_not_adopt_new_rules_implicitly(self):
        self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-1"}),
                                       APPROVED, APPROVED))

    def test_reference_does_not_prove_policy_loaded(self):
        self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-2"}),
                                       APPROVED, {}))

    def test_old_loaded_policy_and_false_revision_claim_fail(self):
        for revision in ("revision-1", "revision-2"):
            rules = dict(RULES, transient_read=Recovery.STOP)
            loaded = {"synthetic-execution": Policy(revision, rules)}
            self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-2"}),
                                           APPROVED, loaded))

    def test_stop_all_connector_failures_conflicts_with_common_policy(self):
        overrides = {failure: Recovery.STOP for failure in Failure}
        self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-2"}, overrides),
                                       APPROVED, APPROVED))

    def test_compatible_local_rule_passes(self):
        entry = Entry({"synthetic-execution": "revision-2"},
                      {Failure.PERMISSION_DENIED: Recovery.STOP})
        self.assertEqual(validate_entry(entry, APPROVED, APPROVED), [])

    def test_conflicting_approved_policies_require_resolution(self):
        policies = dict(APPROVED, other=Policy("revision-3", {
            Failure.TRANSIENT_READ: Recovery.STOP}))
        entry = Entry({name: policy.revision for name, policy in policies.items()})
        self.assertTrue(validate_entry(entry, policies, policies))

    def test_unapproved_loaded_or_referenced_policy_fails(self):
        entry = Entry({"synthetic-execution": "revision-2", "other": "revision-9"})
        self.assertTrue(validate_entry(entry, APPROVED, APPROVED))
        loaded = dict(APPROVED, other=Policy("revision-9", RULES))
        self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-2"}),
                                       APPROVED, loaded))

    def test_empty_or_incomplete_registry_cannot_certify_entry(self):
        self.assertTrue(validate_entry(Entry({}), {}, {}))
        incomplete = {"synthetic-execution": Policy("revision-2", {
            Failure.TRANSIENT_READ: Recovery.RETRY_READ})}
        self.assertTrue(validate_entry(Entry({"synthetic-execution": "revision-2"}),
                                       incomplete, incomplete))


class RecoveryClassificationTests(unittest.TestCase):
    def test_transient_read_budget_is_bounded(self):
        self.assertEqual(recovery_action(Failure.TRANSIENT_READ, attempts=1, limit=2),
                         Recovery.RETRY_READ)
        self.assertEqual(recovery_action(Failure.TRANSIENT_READ, attempts=2, limit=2),
                         Recovery.STOP)

    def test_denied_and_invalid_never_retry(self):
        for failure in (Failure.PERMISSION_DENIED, Failure.INVALID_CONTENT):
            self.assertEqual(recovery_action(failure, attempts=1, limit=3), Recovery.STOP)

    def test_unknown_write_requires_readback_even_after_budget(self):
        self.assertEqual(recovery_action(Failure.UNKNOWN_WRITE, attempts=3, limit=3),
                         Recovery.READBACK)

    def test_conflict_refreshes_within_budget_only(self):
        self.assertEqual(recovery_action(Failure.VERSION_CONFLICT, attempts=1, limit=2),
                         Recovery.REFRESH_MERGE)
        self.assertEqual(recovery_action(Failure.VERSION_CONFLICT, attempts=2, limit=2),
                         Recovery.STOP)

    def test_no_implicit_error_classification_or_invalid_budget(self):
        for failure, attempts, limit in (("network", 1, 2), (Failure.TRANSIENT_READ, 0, 2),
                                         (Failure.TRANSIENT_READ, 1, True)):
            with self.assertRaises(ValueError):
                recovery_action(failure, attempts=attempts, limit=limit)


class ReadFaultStore(SyntheticStore):
    def __init__(self):
        super().__init__()
        self.read_errors = []
        self.write_error = None

    def read(self, identity):
        if self.read_errors:
            error = self.read_errors.pop(0)
            if error is not None:
                self.events.append("read")
                raise error()
        return super().read(identity)

    def guarded_update(self, identity, version, payload):
        if self.write_error:
            self.events.append("update")
            raise self.write_error()
        return super().guarded_update(identity, version, payload)


class SafeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.store = ReadFaultStore()
        self.base = self.store.read(IDENTITY)
        self.store.events.clear()

    def update(self, **kwargs):
        return guarded_update(self.store, self.base, {"preference": "Option B"}, READY, **kwargs)

    def test_temporary_read_recovers_without_manual_second_invocation(self):
        self.store.read_errors = [TransientRead]
        result = self.update(max_read_attempts=2)
        self.assertTrue(result.saved)
        self.assertEqual(self.store.events, ["read", "read", "update", "read"])

    def test_default_remains_one_read_attempt(self):
        self.store.read_errors = [TransientRead]
        self.assertEqual(self.update().status, Status.BLOCKED)
        self.assertEqual(self.store.events, ["read"])

    def test_read_budget_exhausted_without_mutation(self):
        self.store.read_errors = [TransientRead] * 5
        self.assertEqual(self.update(max_read_attempts=2).status, Status.BLOCKED)
        self.assertEqual(self.store.events, ["read", "read"])

    def test_permanent_denial_invalid_content_and_unclassified_failure_stop(self):
        for error in (PermissionDenied, InvalidContent, Unavailable):
            with self.subTest(error=error.__name__):
                self.setUp()
                self.store.read_errors = [error]
                self.assertEqual(self.update(max_read_attempts=3).status, Status.BLOCKED)
                self.assertEqual(self.store.events, ["read"])

    def test_committed_unknown_write_readback_can_retry_safe_read_only(self):
        self.store.faults = ["timeout-after"]
        self.store.read_errors = [None, TransientRead]
        self.assertTrue(self.update(max_read_attempts=2).saved)
        self.assertEqual(self.store.events, ["read", "update", "read", "read"])

    def test_readback_denial_retains_unknown_outcome_without_retry(self):
        self.store.faults = ["timeout-after"]
        self.store.read_errors = [None, PermissionDenied]
        result = self.update(max_read_attempts=3)
        self.assertEqual(result.status, Status.BLOCKED)
        self.assertIn("unverified", result.reason)
        self.assertEqual(self.store.events, ["read", "update", "read"])
        self.assertEqual(self.store.payload["preference"], "Option B")

    def test_write_denial_or_invalid_content_is_not_retried(self):
        for error, reason in ((PermissionDenied, "permission denied"),
                              (InvalidContent, "content invalid")):
            with self.subTest(error=error.__name__):
                self.setUp()
                self.store.write_error = error
                result = self.update(max_attempts=3, max_read_attempts=3)
                self.assertEqual(result.status, Status.BLOCKED)
                self.assertIn(reason, result.reason)
                self.assertEqual(self.store.payload["preference"], "Option A")
                self.assertEqual(self.store.events, ["read", "update"])

    def test_invalid_readback_blocks_even_when_write_committed(self):
        self.store.read_errors = [None, InvalidContent]
        result = self.update(max_read_attempts=3)
        self.assertEqual(result.status, Status.BLOCKED)
        self.assertIn("unverified", result.reason)
        self.assertEqual(self.store.payload["preference"], "Option B")
        self.assertEqual(self.store.events, ["read", "update", "read"])

    def test_wrong_identity_readback_is_unresolved_not_definitely_failed(self):
        self.store.read_faults[3] = "wrong-id"
        result = self.update()
        self.assertEqual(result.status, Status.BLOCKED)
        self.assertIn("unresolved", result.reason)
        self.assertEqual(self.store.payload["preference"], "Option B")
        self.assertEqual(self.store.events.count("update"), 1)

    def test_partial_batch_reconciles_finished_update_then_only_writes_remainder(self):
        self.assertTrue(self.update().saved)
        self.store.faults = ["unavailable"]
        pending = {"unrelated": "Value B"}
        self.assertFalse(guarded_update(self.store, self.base, pending, READY).saved)
        self.store.events.clear()
        self.assertTrue(self.update().saved)
        self.assertNotIn("update", self.store.events)
        self.assertTrue(guarded_update(self.store, self.base, pending, READY).saved)
        self.assertEqual(self.store.events.count("update"), 1)
        self.assertEqual(self.store.payload, {"preference": "Option B", "unrelated": "Value B"})

    def test_synthetic_cold_resume_from_serialized_intent_reconciles_backend(self):
        self.store.faults = ["timeout-after"]
        self.store.read_errors = [None, Unavailable]
        self.assertFalse(self.update().saved)
        journal = json.dumps({"identity": self.base.identity.__dict__,
                              "base_version": self.base.version, "base_payload": self.base.payload,
                              "changes": {"preference": "Option B"}, "outcome": "unknown"})
        # A fresh caller receives only serialized approved intent and a backend.
        state = json.loads(journal)
        resumed_base = Snapshot(Identity(**state["identity"]), state["base_version"],
                                state["base_payload"])
        self.store.events.clear()
        result = guarded_update(self.store, resumed_base, state["changes"], READY)
        self.assertTrue(result.saved)
        self.assertEqual(self.store.events, ["read"])

    def test_duplicate_trigger_uses_current_state_without_duplicate_write(self):
        self.assertTrue(self.update().saved)
        self.store.events.clear()
        self.assertTrue(self.update().saved)
        self.assertEqual(self.store.events, ["read"])

    def test_overlapping_concurrent_writer_is_not_overwritten(self):
        self.store.faults = ["overlap-race"]
        self.assertEqual(self.update().status, Status.BLOCKED)
        self.assertEqual(self.store.payload["preference"], "Option C")
        self.assertEqual(self.store.events.count("update"), 1)

    def test_invalid_read_budget_rejected_before_io(self):
        for budget in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                read_with_retry(self.store, IDENTITY, budget)
        self.assertEqual(self.store.events, [])


class StageEvidenceTests(unittest.TestCase):
    def test_schedule_acceptance_does_not_certify_run_or_delivery(self):
        result = RunEvidence(schedule_acceptance=PASS)
        self.assertEqual(result.run_started.status, Status.NOT_RUN)
        self.assertEqual(result.notification.status, Status.NOT_RUN)

    def test_source_failure_does_not_erase_run_start(self):
        result = RunEvidence(run_started=PASS, source_access=Evidence(Status.BLOCKED))
        self.assertEqual(result.run_started.status, Status.PASS)
        self.assertEqual(result.persistence.status, Status.NOT_RUN)

    def test_notification_failure_preserves_backup_evidence(self):
        before = RunEvidence(persistence=PASS, checkpoint=PASS,
                             notification=Evidence(Status.FAIL, "synthetic known-unsent receipt"))
        # Model a delivery-only continuation; this is not a notification sender.
        after = RunEvidence(persistence=before.persistence, checkpoint=before.checkpoint,
                            notification=PASS)
        self.assertEqual(after.checkpoint, before.checkpoint)
        self.assertEqual(after.persistence, before.persistence)
        self.assertEqual(after.notification.status, Status.PASS)


if __name__ == "__main__":
    unittest.main()
