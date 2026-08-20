# Upgrade an implementation

Use this prompt when adopting a newer framework, schema, policy, or adapter
version.

## Prompt

```text
Upgrade my existing src_you implementation from {{CURRENT_VERSION}} to
{{TARGET_VERSION}} using the smallest reversible change.

Do not rebuild the personal state, change the authoritative source, duplicate
L1/L2 content, or copy private data into the public framework repository.

1. Read the current manifest, local policy overlay, adapter notes, changelog,
   and target release notes.
2. Produce a compatibility matrix covering schema, terminology, record
   lifecycle, pointers, routing, backup manifests, restore behavior, and
   acceptance scenarios.
3. Identify required, optional, and incompatible changes. Treat product UI
   capability updates as adapter changes unless a core invariant genuinely
   changed.
4. Create and verify a pre-upgrade checkpoint.
5. Apply required changes in place, preserving stable IDs and superseded
   history.
6. Do not promote transient L2 detail into L1 during migration.
7. Re-bind logical pointers rather than spreading new provider IDs through
   global state.
8. Run all twelve acceptance scenarios plus privacy, secret, terminology,
   pointer, and checkpoint-integrity checks.
9. Update manifest version and changelog only after validation succeeds.
10. Create a post-upgrade checkpoint and report rollback instructions.

If the target requires a new authority model, destructive conversion, or
broader data exposure, stop and request an explicit decision before applying
that portion. Complete every safe, independent validation step first.
```
