# Operational contract

This normative supplement makes the existing L0/L1/L2 governance contract
reviewable at each operation. It adds no layer, provider integration, scheduler,
or general agent engine. The existing
[fourteen acceptance scenarios](../tests/acceptance-tests.md) remain required
and unchanged. This contract adds operational evidence to those semantics.

## Acceptance criteria

The following criteria define the behavior exercised by the synthetic
implementation in [`scripts/operational_contract.py`](../scripts/operational_contract.py)
and its tests in [`tests/test_operational_contract.py`](../tests/test_operational_contract.py).
All examples and test backends must be fictional; no private store is needed.

| Criterion | Required observable result |
|---|---|
| Identity | An update retains the canonical source identity, stable record ID, and scope; a different source or duplicate title cannot substitute. |
| Fresh guard | Every mutation checks the version of its freshly read base atomically with the write; a stale guard cannot overwrite newer state. |
| Disjoint edits | After a version conflict, reread and three-way merge retain unrelated concurrent edits, then write with the newly observed version guard. |
| Overlapping edits | Different changes to the same owned field block the mutation and report the conflict; no silent winner is selected. |
| Saved proof | A saved claim requires exact readback of the same canonical target and expected record, lifecycle, scope, and merged content. A write acknowledgment alone is insufficient. |
| Unknown outcome | A timeout or lost acknowledgment triggers a read of the same target before any further mutation. No blind retry occurs. |
| No fallback create | A failed or uncertain update never creates a replacement record, source, or document. |
| Separate capabilities | Read, create, guarded update, and readback have independent evidence. A successful create or read does not establish update capability. |
| Separate outcomes | Delivery, canonical persistence, and checkpoint each report PASS, FAIL, BLOCKED, or NOT_RUN with evidence; only dependent work stops. |
| Minimal retrieval | An ordinary task with no dependency on established state performs no personal-state retrieval. Relevant verified sources can be reused during uninterrupted continuity. |
| Refresh boundaries | Resume, source/version change, conflict, and a proposed write require fresh relevant source reads; memory or old transcripts cannot supply the missing version. |
| Existing durability | Confirmed authorized durable changes are still persisted in the same session when possible. Periodic maintenance audits or catches up explicitly pending work; it does not replace this obligation. |

The synthetic harness demonstrates these rules within its model. Passing it
does not prove a provider supports guarded updates, reliable readback, or any
other capability. Real adapters need privacy-safe evidence on their actual
surface, in addition to all fourteen existing scenarios.

### Reference implementation boundaries

The small Python module accepts a caller-prepared, authorized durable update;
it does not interpret language, grant authorization, generate supersession
history, or select an authority. Its identity envelope holds source, record ID,
and scope outside the editable payload. Payloads contain finite JSON values;
comparison is type-strict, so booleans and numbers cannot silently substitute.
Dictionary order is immaterial, but list order and every field value matter.
It merges at top-level field boundaries; nested conflicts block conservatively.
Deletion and automatic semantic document merging are outside this reference.

The backend must supply fresh authoritative (linearizable) reads and atomic
compare-and-swap with versions that change on every mutation and are never
reused. These are assumptions to verify in a real adapter, not guarantees
provided by this module. An unchanged read after a timeout only establishes
that no commit was visible as of that read. Any delayed mutation must still
enforce its original guard; it and a guarded retry cannot both commit against
the same version. Retries are bounded. Unresolved results require reconciliation
before a caller starts another attempt; do not discard an uncertain outcome.

Capability evidence is supplied by the caller from real operation probes;
the module only checks its explicit status and reference. It does not run
provider probes, create records, send deliveries, or create checkpoints.

## Identity and minimal retrieval

Resolve the manifest only when established personal or project state matters
to the task. Ordinary writing, calculations, and generic technical questions do
not require a personal-state lookup. Where state matters, follow the existing
[retrieval policy](../policies/retrieval-policy.md) and load the smallest
relevant authority.

An operation binds to `(canonical source identity, stable record ID, scope)`.
Source identity means the actual designated object, not a title, search rank,
local copy, export, cache, or newly created object with matching content. A
logical pointer may resolve to that identity; authority migration remains an
explicit governance operation. Version is separate from identity.

A verified relevant source read may be reused during an uninterrupted task
while its identity, scope, and freshness remain valid. Refresh on resumed work,
known source or version change, conflict, or before a mutation. Do not reread
unrelated state or refresh merely because another conversational turn occurred.
External observations still follow their own use-time revalidation rules.

## Guarded mutation procedure

1. Apply the durability, scope, authorization, and sensitive-data gates. Locate
   the existing canonical target and stable record before changing it.
2. Freshly read the target and capture its identity, record ID, scope, content,
   lifecycle, and version. Preserve this base and describe the intended delta.
3. Prepare the proposed content, retaining superseded history and exactly one
   current value for the record and scope. Preserve unrelated fields and edits.
4. Submit the change to the same target with an atomic expected-version guard.
   A pre-write read followed by an unconditional write is not a version guard.
   If the surface lacks a demonstrated safe guard or equivalent exclusive
   write mechanism, block the automated update and report the missing ability.
5. If the guard rejects stale state, reread that same target. Compare the base,
   intended content, and latest content. Retain latest changes where the intent
   did not touch a field; apply intended changes where latest equals the base;
   accept identical changes once. Different changes to the same field,
   deletion against modification, or ambiguous record/lifecycle edits conflict.
   Block the overlapping mutation for resolution. Never use a timestamp or
   model confidence to choose a winner. Any merged retry uses the latest
   version guard; further races require another read and comparison.
6. Read back the same canonical target after acknowledgment. Compare the exact
   expected merged record, identity, scope, and lifecycle, including preserved
   unrelated content. A mismatch or unavailable readback prevents a saved
   claim, even if the mutation may have applied. Do not overwrite the new
   content merely to force the comparison to pass.
7. Report delivery, persistence, and any checkpoint independently. Create a
   checkpoint only after verified persistence and only when justified by the
   existing checkpoint policy.

Three-way comparison is at the smallest independently owned field or record
unit the implementation can safely represent. It is not permission to guess
semantic equivalence, merge arbitrary documents, or bypass an authority conflict.
A backend unable to represent a safe merge must block that dependent mutation.

## Uncertain outcomes and failure boundaries

If a mutation acknowledgment is lost, record the outcome as uncertain and read
the same canonical target first. If exact expected content is present and
verified, persistence can pass. If the base is still present with the same
version, a guarded attempt can be considered after reconciliation. If content
has changed, use the conflict procedure. If the read fails or cannot distinguish
whether the mutation applied, keep persistence BLOCKED and do not retry.

A definite denial, unavailable update operation, or uncertain update is never a
reason to create a replacement object. Create is a separate operation only for
an authorized genuinely new record or source, with its own identity,
uniqueness, and readback evidence. A successful create cannot repair failed
update evidence or appoint a new authority.

Block only work that depends on the failed operation. A persistence failure
need not prevent delivery of an independently valid answer or artifact; failed
delivery does not undo verified persistence. A failed checkpoint does not make
a verified canonical write unsaved. Report uncertainty explicitly so a later
session reads before attempting recovery.

## Evidence and result vocabulary

Keep evidence operation-specific and privacy-safe: operation, logical target,
record/scope, observed version, guard result, comparison result, and reason.
Do not publish private source locators or contents. A generic success indicator
cannot replace proof for each action.

| Capability | Evidence required independently |
|---|---|
| Read | Actual read of the relevant canonical identity and scope. |
| Create | Authorized new-object creation plus resulting identity; does not establish update capability. |
| Guarded update | Same-target mutation with demonstrated version precondition or equivalent exclusive guard. |
| Readback | Actual post-mutation read and exact expected-content comparison, not a write response echo. |

Use the following statuses separately for delivery, canonical persistence, and
checkpoint. Retain the underlying operation evidence as well.

| Status | Meaning |
|---|---|
| PASS | The action's own success criteria have been verified. |
| FAIL | Evidence establishes that the attempted action failed its criteria. |
| BLOCKED | A required permission, capability, conflict resolution, or outcome verification is missing. |
| NOT_RUN | The action was not attempted, including when it was not required. |

A failed readback comparison can be FAIL while overall persistence remains
BLOCKED because the applied state is unresolved. A lost mutation acknowledgment
is not proof of either a successful save or a definite failure. Record both the
observed error and uncertainty. For example, fictional delivery can be PASS,
persistence BLOCKED by a version conflict, and checkpoint NOT_RUN. Do not
collapse that result into a single success or stop all independent work.

## Maintenance and compatibility

The [update policy](../policies/update-policy.md) still requires same-session
persistence of confirmed authorized durable changes when possible. A periodic
audit may identify drift, repair verified summaries, or catch up a previously
reported pending update using fresh reads and the same guards. It cannot make
an unsaved change retroactively saved or postpone ordinary durable writes.
This contract creates no recurring automation.

The existing layer boundaries, typed claims, inference rules, minimal retrieval,
source ownership, supersession, privacy, and explicit restore gates all remain.
Checkpoint and backup flow stays downstream. Existing reference-adapter
capability-check dates describe earlier external observations; these generic
requirements do not newly verify any external product capability.
