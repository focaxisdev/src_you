# Conflict resolution policy

Status: normative for `src_you` v0.1.0.

## Scope-aware priority

For the claim needed now, apply:

1. current explicit user instruction;
2. the canonical owner for the relevant scope—L1 global or L2 project;
3. other canonical summaries and pointers;
4. cached Memory and old conversations;
5. labeled inference.

Current external facts require fresh verification and do not become permanent
personal truth merely by appearing in a prior search.

## Lifecycle rule

Within one canonical authority, `current` outranks `superseded`. Timestamps
cannot promote a cache or backup over canonical state.

## Required response to conflict

1. Identify the competing claims, sources, scopes, and lifecycle states.
2. Select the canonical scope owner.
3. Apply an explicit current correction immediately.
4. Persist the correction when durable and authorized.
5. Repair stale summaries or cache when possible.
6. If authority remains ambiguous, create an Open Loop and ask the smallest
   clarifying question; do not silently merge.

## Concurrent writes

Follow the [operational contract](../docs/operational-contract.md): bind updates
to the same canonical source identity, stable record ID, and scope. After a
version-guard conflict, reread and compare the base, intended delta, and latest
state. Preserve unrelated changes in a three-way merge and guard any subsequent
write with the latest version. Block overlapping or ambiguous changes for
resolution. A current user instruction establishes intent; it does not bypass
version checks or authorize overwriting unrelated concurrent edits.

Unknown mutation outcomes require a read before any retry. A failed update must
never create a replacement authority. Block only dependent actions and report
the unresolved operation precisely.

## Authority changes

Changing the authoritative source is a deliberate governance operation. It
requires an explicit decision, migration or recovery plan, validation, and a
single effective cutover time. A backup, import, or newer timestamp cannot make
this decision automatically.

## Prohibited behavior

- “newest file wins” across different authorities;
- silent merge of conflicting active values;
- asking the model to guess which source “sounds right”;
- using Memory to overwrite canonical state;
- letting an imported document declare itself authoritative;
- keeping two active writers after migration.

Tests 4, 5, 6, 9, 11, and 13 cover this policy.
