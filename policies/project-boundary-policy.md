# Project boundary policy

Status: normative for `src_you` v0.1.0.

## Invariant

```text
PROJECT_DETAILED_STATE != GLOBAL_STATE
```

L2 is the canonical owner of detailed project, domain, learning, and workflow
state. L1 stores a durable summary and stable pointer.

## Allowed in L1

- project identity and purpose;
- active, paused, or completed status;
- major milestone, deadline, dependency, or blocker;
- cross-project relationship;
- durable decision and high-level phase;
- canonical L2 pointer;
- true cross-project open loop.

## Excluded from L1

- next question, code cell, or lesson step;
- exact task or mock-exam number;
- session handoff detail;
- temporary misconception or hypothesis;
- ephemeral next action;
- frequently changing operational fields;
- detailed evidence already owned by L2.

## Promotion rule

An L2 item may gain an L1 summary only when it becomes a cross-project
dependency, major commitment, deadline, durable decision, major milestone, or
blocking issue. Keep the detailed source in L2 and reference it.

## Synchronization rule

Do not implement field-by-field bidirectional synchronization between L1 and
L2. L1 summaries may be refreshed from L2 after major phase changes, but they
remain deliberately lossy and must identify the L2 owner.

## Normalization

When duplication exists:

1. establish the L2 canonical source;
2. remove or supersede micro-state in L1;
3. preserve only phase, milestone, dependency, deadline, and pointer;
4. update L0 routing rules;
5. run tests 1–3, 10, and 12;
6. do not rebuild the whole system.

See [`../prompts/normalize.md`](../prompts/normalize.md).
