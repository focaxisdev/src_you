# Normalize project/global boundaries

Use this prompt to repair stale duplication where project detailed state has
leaked into global state. It is intentionally conservative and does not rebuild
the system.

## Prompt

```text
Perform a conservative src_you normalization focused on this failure mode:

PROJECT_DETAILED_STATE duplicated into GLOBAL_STATE.

Do not rebuild the system, create a competing manifest, change the authoritative
source, or alter unrelated content. Make reversible, minimal edits only after
confirming ownership. Never copy private content into a public location.

Required procedure:

1. Read the current manifest, project registry, routing policy, global domain
   summary, and only the relevant L2 project source.
2. Establish which source is canonical for project detail. If authority is
   ambiguous, stop and ask one focused question naming the candidates.
3. Inventory duplicated fields, including exact question/lesson/code/task step,
   session handoff, temporary misconception, micro-progress, and ephemeral next
   action.
4. Preserve those details in L2. If L2 is already current, do not rewrite it
   merely for symmetry.
5. Remove or supersede the duplicated micro-state in L1.
6. Keep in L1 only project identity, purpose, status, major phase, major
   milestone/dependency/deadline/blocker, high-level progress, cross-project
   relationship, durable decision, true cross-project open loop, and the L2
   canonical pointer.
7. Repair routing so high-level questions stop at L1 and detailed continuation
   follows L2.
8. Check other L1 domains for the same pattern using metadata or targeted
   search; do not expand into a full rewrite unless the same defect is proven.
9. Run acceptance scenarios 1, 2, 3, 10, and 12, plus a broken-pointer and
   privacy check.
10. Record a non-sensitive changelog entry and create a checkpoint only if the
    change is a meaningful durable correction.

Example defect:

- L1 says “current mock question 17.”
- L2 says “current mock question 18.”

Correct result:

- L1 says “active; phase = mock-exam preparation; detailed state = canonical
  L2 pointer.”
- L2 alone owns the exact question number and next action.

Report changed paths, removed categories, retained L1 summary, canonical L2
pointer, test results, rollback point, and any unresolved issue. Do not expose
the private micro-state contents beyond the minimum needed to describe the fix.
```
