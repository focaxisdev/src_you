# Project registry

Each project has one detailed canonical owner. L1 stores only routing metadata
and high-level state.

| Project ID | Purpose | Status | L2 logical pointer | L2 authority | Last major update |
|---|---|---|---|---|---|
| `PROJECT-{{SLUG}}` | `{{PURPOSE}}` | active | `project://{{SLUG}}/state` | `{{PRIVATE_STORE}}` | `{{ISO_8601_DATE}}` |

If the L2 location changes, re-bind the logical pointer. Do not copy the full L2
state into this registry.
