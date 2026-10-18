# Upgrade an implementation

Use this prompt when adopting a newer framework, schema, policy, or adapter
version.

## Prompt

```text
Upgrade my existing src_you implementation from {{CURRENT_VERSION}} to
{{TARGET_VERSION}} using the smallest reversible change.

Do not rebuild the personal state, change the authoritative source, duplicate
L1/L2 content, or copy private data into the public framework repository.

1. Read the current manifest, local policy overlay, every active runtime
   entrypoint, adapter notes, all required framework policies, changelog, and
   target release notes. Inventory entrypoints that can start work, including
   scheduled/cold-context entrypoints, and record each one's policy references,
   policy IDs/revisions, and declared dependencies.
2. Verify every active entrypoint includes its applicable required policies at
   their adopted revisions, including the operational contract and, for entries
   offering unattended work, the execution reliability contract.
   Revalidate actual scheduled/cold-context capabilities. Do not claim unattended
   execution accepted until an actual fresh-context run supplies evidence;
   an interactive success or schedule-creation acknowledgment is insufficient.
   Unsupported paths remain unaccepted without blocking independent work.
   Stop the affected entrypoint if a
   required policy is missing, stale, contradictory, or cannot be verified.
3. Produce a compatibility matrix covering schema, policy baseline, entrypoint
   dependencies and precedence, terminology, record lifecycle, pointers,
   routing, backup manifests, restore behavior, and acceptance scenarios.
4. Resolve conflicts by normative framework policy first, then compatible
   adapter requirements, then local policy choices. Explicit local overrides
   must be documented and approved, may strengthen requirements or fill in
   platform details, and may not weaken framework safeguards. Version dates or
   timestamps never decide authority. Stop when a conflict cannot be resolved
   under this order.
5. Identify required, optional, and incompatible changes. Treat product UI
   capability updates as adapter changes unless a core invariant genuinely
   changed.
6. Create and verify a pre-upgrade checkpoint.
7. Apply required changes in place, preserving stable IDs and superseded
   history.
8. Do not promote transient L2 detail into L1 during migration.
9. Re-bind logical pointers rather than spreading new provider IDs through
   global state.
10. Run all fourteen state-governance scenarios, applicable execution-reliability
    acceptance criteria, and privacy, secret, terminology, pointer, and
    checkpoint-integrity checks. Checkpoint metadata checks validate shape,
    format, and version only; separately verify source identity and authority,
    restore approval, and any execution journal.
11. Update `framework_version` only after the target policy baseline's full
    acceptance set passes. Keep manifest `schema_version` unchanged unless a
    schema migration is separately required and validated. Update the changelog
    only after validation succeeds.
12. Create a post-upgrade checkpoint and report rollback instructions.

If the target requires a new authority model, destructive conversion, or
broader data exposure, stop and request an explicit decision before applying
that portion. Complete every safe, independent validation step first.
```

See the [operational contract](../docs/operational-contract.md) and
[execution reliability contract](../docs/execution-reliability.md) for the
applicable criteria and explicit platform boundaries.
