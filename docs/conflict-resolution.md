# Conflict resolution

Conflict resolution is scope-aware. A fixed linear list without scope can make
an L1 summary incorrectly overrule the L2 source that owns project detail.

## Priority model

For the fact required by the current task:

1. **Current explicit user instruction** governs the current turn unless unsafe
   or impossible.
2. **The canonical owner for that fact's scope** governs maintained state:
   L1 for cross-domain durable state; L2 for project detail.
3. **Other canonical summaries and pointers** provide routing and context but do
   not overrule the scope owner.
4. **Cached Memory and old conversations** are hints and evidence.
5. **Inference** is last and must remain labeled.

Fresh external facts are verified from appropriate current sources rather than
ranked as permanent personal state.

## Conflict algorithm

1. State the claim and required scope precisely.
2. Identify its canonical owner through the manifest or registry.
3. Compare lifecycle: `current` beats `superseded`.
4. Compare effective dates only within the same authority; never use timestamp
   alone to promote a backup or cache.
5. Apply the user's current explicit correction for the present response.
6. If the correction is durable, update the canonical record and supersede the
   old value before the session ends when possible.
7. If authority is unclear, do not guess. Mark the conflict and request the
   smallest decision needed to establish ownership.

## Example: explicit correction

```text
Cached Memory: prefers option A
Canonical L1: prefers option A
Current user instruction: "I have changed my mind; use option B from now on."
```

Use B now. Because “from now on” is a durable update, change the canonical record
to B and mark A superseded. Do not merely override A in chat while leaving stale
canonical state.

## Example: summary versus detail

```text
L1 summary: project phase = testing
L2 canonical state: project phase = released
```

L2 owns the project's detailed operational state. Use `released`, then repair
the L1 high-level summary. Do not create a third merged value.

## Unresolved conflict record

When authority cannot be established, record an Open Loop containing:

- the competing claims;
- their sources and scopes;
- why neither can be selected safely;
- the person or action needed to resolve it;
- whether work can proceed with a temporary assumption.

Temporary assumptions remain Inferences, not Facts.
