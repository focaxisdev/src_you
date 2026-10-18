# Execution reliability contract

This supplement defines evidence for an adapter that runs work unattended.
It adds no scheduler, authentication, persistent job store, or background worker.
Host capabilities must be verified in the execution context that will use them.
An interactive success does not prove a later background run will succeed.

## Acceptance criteria

Use only synthetic inputs and fault injection when testing the reference.
These criteria are independent of a particular provider or user deployment.

| Fault or boundary | Required observable result |
|---|---|
| Missing, stale, or contradictory entry policy | Reject entry validation before execution; require all declared policy dependencies and their approved revisions. |
| Temporary safe read failure | Retry only within a configured attempt budget; exhausted reads block dependent work. |
| Permission denial or invalid content | Stop the dependent operation without retry, new authority, or replacement object. |
| Version conflict | Reread, preserve unrelated changes, and use a fresh atomic guard; conflicting intent remains blocked. |
| Unknown write result | Read the same target before another write; unreadable or mismatched evidence preserves uncertainty. |
| Committed write with wrong-target readback | Report persistence BLOCKED, not a definite failed write; no automatic replacement or overwrite. |
| Repeated prepared update | Verify current state and perform no duplicate mutation when the intended state is already present. |
| Partial batch or restart | Reconstruct intended operations from durable approved state, reconcile completed/unknown effects, and continue only remaining authorized work. |
| Backup complete, notification failed | Preserve backup evidence; only retry delivery when its outcome is known and its retry is safe. |
| Concurrent or duplicate run | Use operation identity and backend guards/deduplication; unsupported safety blocks the affected side effect. |
| Cold execution context | Load instructions, current policies, source bindings, capabilities, and pending-operation state without the original chat. |
| Checkpoint inventory | Reject malformed or incomplete manifest metadata; valid hashes alone do not establish authority or restore readiness. |
| Future automation | Record schedule acceptance, run start, source access, persistence, checkpoint, and delivery independently; do not infer one from another. |

The existing fourteen state-governance scenarios remain required. These
additional criteria cover execution reliability, not new authority semantics.

## Entry policy consistency

Keep an implementation-owned registry of approved policy IDs, revisions, and
required dependencies. Each live entrypoint (interactive, scheduled, or recovery)
declares its required references and local error rules. Compare those declarations
with both the approved registry and the policies actually loaded in the new
execution context. A matching title or a link that exists does not prove policy
loading, revision compatibility, or completeness of the dependency list.

The pure [`execution_contract.py`](../scripts/execution_contract.py) helper
compares structured references, loaded revisions/rules, and overrides. Missing
dependencies, stale revisions, unapproved policies, and contradictory stop/retry
rules fail validation. The approved registry is supplied independently of the
entry being checked; letting an entry approve itself defeats this check.
The caller supplies the complete required dependency set; the helper does not
discover files, expand a dependency graph, or load policy text on its own.
The helper cannot detect an unrepresented instruction in prose. Adapters must
inventory actual entry instructions and review their correspondence to the
structured declarations. Never claim arbitrary natural-language conflict
detection from this helper.

Resolve policy authority and explicitly approve any changed override before
updating the registry. Do not choose by timestamp, silently weaken a denial, or
automatically replace a governing policy. Conflicting approved policies require
resolution; only the affected execution path remains blocked.

`framework_version` identifies the adopted policy baseline, filled after the
implementation's acceptance checks pass. `schema_version` identifies stored
data shape, and checkpoint `format_version` identifies inventory serialization.
They need not equal the latest repository release. A policy upgrade does not
authorize a data migration or silently mark existing deployments compliant.

## Error classification and finite recovery

| Classification | Safe next action |
|---|---|
| Explicitly transient, side-effect-free read | Retry within an approved attempt/time budget; exhausted budget blocks dependent work. |
| Permission denial | Stop dependent action; do not reauthenticate, expand permissions, or retry automatically. |
| Invalid content or failed integrity check | Stop and report the failed check; do not treat corruption as a transient network error. |
| Version conflict with known rejected write | Fresh read and conservative merge, then atomic guarded retry within its budget. |
| Unknown mutation outcome | Same-target readback before any mutation; uncertain/readback failure remains BLOCKED. |
| Unclassified error | Stop safely and retain uncertainty; never assume it is retryable. |

The adapter classifies provider errors using operation-specific evidence. A
network exception during a write is not a retryable read failure. The existing
`Unavailable` behavior remains conservative; opt in to `TransientRead` only for
safe reads. `PermissionDenied` and `InvalidContent` stop immediately. The
reference's `max_read_attempts` defaults to one for compatibility and bounds each
read phase; `max_attempts` separately bounds guarded mutation attempts. Each
mutation attempt performs at most one refresh and one readback phase, so total
read calls are bounded by twice the product of those limits. Real adapters must
also enforce wall-clock deadlines, appropriate backoff and provider limits.
`UpdateResult.attempts` counts mutation attempts, not read calls; adapters retain
read-attempt evidence separately. The helper has no timer or background retry
queue.

## Durable resume and independent stages

An adapter supporting unattended recovery retains a privacy-safe durable
operation record outside this public framework. Include logical job/operation
identity, approved intent and policy revision, canonical identity, base version,
expected change, per-operation outcome, verification evidence, and next safe
action. Protect any necessary payload as private state; never include tokens or
copy it into public logs. A chat transcript is not the only recovery source.

After a fresh start, resolve the current policies and source bindings, re-probe
relevant capabilities, and reconcile pending or unknown effects against the
authoritative target. Replaying the same prepared assignment is safe only under
the reference backend's atomic-guard and nonreused-version assumptions. Do not
recompute a relative increment as a new intent or blindly repeat a completed
external side effect. Preserve verified completed operations and resume only
unfinished authorized ones. Revalidate changed intent, policy, or authority.

Use stable operation identity and a backend's idempotency/deduplication mechanism
for duplicate runs and external effects. If the host cannot supply the required
guard, block that side effect instead of promising exactly-once execution.

Keep schedule acceptance, actual run start, source access, canonical persistence,
backup checkpoint, and notification evidence separate using PASS/FAIL/BLOCKED/
NOT_RUN. Failure to read a source does not mean the scheduler never triggered.
A successful save or manual continuation is not acceptance of future automation.
Report what was verified and which execution context produced the evidence.

A completed backup remains completed if notification fails. Retry only delivery
when it is known unsent and safe, or reconcile an unknown delivery outcome using
the provider's receipt/deduplication facility. Do not recreate the backup to send
a message. Failure reporting should name the failed stage, safe error class,
attempt count, preserved successes, unresolved effects, and next action. The
adapter must verify the notification destination/access and observable receipt;
an inaccessible notification channel cannot be reported as successful delivery.

## Checkpoint and verification limits

A backup checkpoint is a downstream state snapshot, not an execution journal.
The inventory verifier validates supported format metadata, paths, counts, and
hashes; its success does not prove source authority, semantic completeness,
restore approval, or future job reliability. A valid empty inventory is allowed;
it must not be interpreted as proof that an expected nonempty scope was backed
up. Actual scope coverage and restore decisions remain separate checks.

[`test_execution_reliability.py`](../tests/test_execution_reliability.py) covers
policy drift, classified read retries, unknown writes, prepared-update replay,
and synthetic partial/cold continuation. Cold continuation deserializes intent
in memory; it is not a real fresh hosted runtime. Notification tests separate
receipts only; they do not send messages or demonstrate provider deduplication.
[`test_checkpoint_manifest.py`](../tests/test_checkpoint_manifest.py) covers
metadata rejection, compatible manifests, and integrity faults.

For each actual platform, separately test an authorized synthetic scheduled run
in a fresh execution context: trigger, source access, bounded failure handling,
interruption/recovery, duplicate runs, and notification receipt. Record limits
or NOT_RUN evidence when a capability is absent. No provider capability, durable
journal, scheduler, automatic notifier, or future reliability guarantee is
implemented by these reference checks.
