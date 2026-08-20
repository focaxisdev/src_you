# Project boundaries

Projects need detailed state to continue accurately. Global personal state needs
to stay compact and stable. Mixing the two creates duplication and drift.

## Ownership table

| State item | L1 global | L2 project |
|---|---:|---:|
| Project identity and purpose | Yes | May repeat as metadata |
| Active / paused / completed | Yes | Yes, but L2 is detailed operational source |
| Major milestone or deadline | Yes | Yes, with detail |
| Cross-project dependency | Yes | Yes, referenced |
| High-level phase | Yes | Yes |
| Canonical project-state pointer | Yes | N/A |
| Exact next step | No | Yes |
| Current question, lesson, or code cell | No | Yes |
| Temporary misconception or blocker | No | Yes |
| Session handoff | No | Yes |
| Detailed history and evidence | No | Yes |

The allowed overlap is deliberate metadata or a lossy high-level summary—not two
independent writable copies.

## Boundary decision

Use this decision sequence:

1. Will the item matter outside this project?
2. Is it a major commitment, deadline, dependency, blocker, decision, or
   milestone?
3. Would copying it to L1 require frequent synchronization?
4. Can L1 answer the high-level question with a phase and pointer instead?

If the answer to 3 is yes and 2 is no, keep it in L2.

## Example

```text
L1 global learning state
- Certification preparation is active.
- Deadline: December.
- Phase: mock-exam preparation.
- Detailed state: project://fictional-learning/learner-state

L2 project learner state
- Current question: 17.
- Error pattern: confuses precision with recall.
- Next action: answer question 18.
```

If question 17 becomes question 18, only L2 changes. L1 remains true.

## Promotion and demotion

**Promote** an L2 item by adding an L1 summary when it becomes cross-project or
durable. Keep detailed evidence in L2 and link to it.

**Demote** duplicated micro-state by removing it from L1, repairing the pointer,
and recording the normalization in the state changelog. Demotion does not delete
the canonical L2 detail.

Use [`../prompts/normalize.md`](../prompts/normalize.md) for a conservative
boundary cleanup.
