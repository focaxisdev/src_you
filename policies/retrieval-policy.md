# Retrieval policy

Status: normative for `src_you` v0.1.0.

## Objective

Retrieve the smallest authoritative state set needed to answer or act correctly.
Minimal retrieval improves relevance, privacy, latency, and conflict detection.

## Required procedure

1. Classify the request by domain, scope, and precision.
2. If the task depends on established personal/project state, read the
   manifest/router before opening domain state. Otherwise retrieve no personal
   state.
3. Load only the relevant L1 domain summaries.
4. Follow an L2 canonical pointer only when detailed continuation or evidence is
   required.
5. Add Memory, chat history, or external sources only when they have a defined
   purpose; keep them non-authoritative.
6. Record uncertainty when the canonical owner is unavailable or stale.
7. Do not load unrelated sensitive domains “just in case.”

## Continuity and freshness

A verified relevant source may be reused during uninterrupted task continuity.
Refresh the relevant authority on resumed work, known source/version change,
conflict, or before a write. A new conversational turn alone does not require a
repeat read. Verify source identity, stable record ID, and scope; matching names
or cached excerpts cannot substitute. The
[operational contract](../docs/operational-contract.md) defines mutation guards
and evidence without requiring unrelated retrieval.

## Routing examples

| Request | Required retrieval | Excluded by default |
|---|---|---|
| “How is my learning going overall?” | L1 learning summary and milestone registry | Question number, code cell, family/health state |
| “Continue the previous Python step.” | L1 pointer, then L2 learner state | Unrelated L1 domains |
| “Which role fits my constraints?” | L1 career goals, preferences, constraints | Learning micro-state and raw chat history |
| “What is today's product price?” | Current external verification plus relevant decision criteria | Old price as permanent truth |

## Retrieval precedence

Current explicit user instruction leads for the present turn. Then use the
canonical owner for the fact's scope. L1 summaries route; L2 owns detail. Memory
and old conversations are hints. Inference is last and labeled.

## Prohibited behavior

- injecting the complete state tree into every prompt;
- reading sensitive domains unrelated to the task;
- treating search rank as authority;
- using a stale L1 summary instead of following its L2 pointer;
- presenting inference as retrieved canonical state;
- retaining retrieved private context longer than the task requires.

## Acceptance evidence

Tests 1, 2, and 10 in
[`../tests/acceptance-tests.md`](../tests/acceptance-tests.md) cover this policy.
