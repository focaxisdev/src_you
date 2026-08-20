# Project integration

ChatGPT Projects can keep related chats, files, instructions, and sources
together. In `src_you`, that makes a project a natural L2 boundary—not a second
global-state store.

## Project setup contract

Each project should define:

- a stable logical project ID;
- its purpose and scope;
- its detailed canonical state file or source;
- the fields it owns;
- its session-handoff format;
- the major changes that should refresh L1;
- its sensitive-data and retention rules.

The L1 registry stores only the logical pointer, status, high-level phase, major
milestone/deadline/dependency, and cross-project relationships.

## Suggested project instruction

```text
This project is an L2 src_you scope.

Canonical detailed state: {{PROJECT_STATE_LOCATOR}}
Logical pointer: project://{{PROJECT_SLUG}}/state

Own detailed task state here, including exact next step, temporary blockers,
session handoff, evidence, question/code/lesson position, and micro-progress.

Do not copy that detail into global L1 state. Update L1 only when this project
changes active/paused/completed status, major phase, milestone, deadline,
cross-project dependency, durable decision, or blocking issue. L1 should keep a
lossy summary and this logical pointer.

When global Memory or an old chat conflicts with this project's current detailed
state, use the canonical project state and report/repair the stale source.
```

## Routing examples

| User request | Route |
|---|---|
| “What are my active projects?” | L1 project registry |
| “What is the next step in this project?” | L1 pointer then L2 state |
| “Move the deadline to October.” | Use now; update owning canonical record and related L1/L2 summaries |
| “What did an old chat say?” | Chat history as evidence, not current state |

## Avoiding project drift

- Start separate chats for distinct outcomes while keeping shared L2 files in
  the project.
- Update the canonical handoff rather than relying on the longest chat.
- Archive completed micro-state in L2; mark the L1 project status completed.
- If a Project is moved or renamed, re-bind the logical pointer in the registry.
- Run boundary tests after changing project instructions.
