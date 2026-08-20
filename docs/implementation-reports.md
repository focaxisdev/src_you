# Implementation reports

Early `src_you` development needs evidence from real setups more than star
counts. An implementation report explains what happened when someone mapped the
contract to an actual private store and AI platform.

Use the GitHub **Implementation report** issue form, but keep the report fully
de-identified. Never attach a state tree, screenshot, export, backup manifest,
private locator, or transcript.

## Report template

```text
src_you version:
Storage class: local files / private Git / document store / database / other
AI platform or agent:
Adapter used or created:

Setup attempted:
-

What worked:
-

What broke or required a workaround:
-

What was confusing:
-

Acceptance scenarios exercised:
-

Privacy-safe evidence:
- paths expressed as logical scopes only
- pass/fail outcomes
- no personal values, IDs, screenshots, or raw documents

One improvement with the highest value:
-
```

## What maintainers look for

- Was one canonical owner clear for every active state item and scope?
- Did L1 stay free of L2 micro-state?
- Could a durable update supersede the previous value cleanly?
- Did cache, old chat, and backup remain non-authoritative?
- Was retrieval minimal in practice?
- Did the adapter expose a capability gap or platform-specific assumption?
- Could the person keep framework and personal state separate?

Reports may describe a failed implementation. A precise failure and its
conditions are useful evidence.
