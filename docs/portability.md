# Portability

`src_you` separates the state model from platform capabilities so a person can
change AI systems without redefining their truth.

## Portable core

The following concepts must survive adapter changes:

- authoritative source and canonical owner;
- L0/L1/L2 boundaries;
- typed claims and current/superseded lifecycle;
- canonical pointers;
- minimal retrieval and scope-aware priority;
- downstream checkpoints and explicit restore;
- privacy and sensitive-data rules.

## Adapter responsibilities

An adapter documents how a platform provides—or fails to provide:

| Capability | Required mapping |
|---|---|
| Runtime guidance | Where L0 rules live and how precedence works |
| Private durable store | How L1 canonical state is read and updated |
| Project detail | How L2 state is separated and resolved |
| Memory | How cache is identified and prevented from becoming authority |
| Retrieval | How the minimum necessary state is selected |
| Write controls | How updates, supersession, and user confirmation work |
| Checkpoint/export | How downstream recovery artifacts are produced |
| Limitations | Missing features, UI-only steps, and freshness date |

Adapters must use capability descriptions before UI labels. A renamed “Library”
or “Project” should require only an adapter update, not a new core architecture.

## Pointer portability

Avoid embedding provider-only object IDs directly throughout L1. Prefer a stable
logical pointer registry:

```yaml
logical_id: project://learning/learner-state
adapter: chatgpt
locator: "private platform-specific locator"
status: current
```

The registry can be re-bound during migration while global records retain the
logical pointer.

## Migration outline

1. Freeze writes in the old adapter.
2. Export canonical L1 and pointer registry.
3. Map L2 sources without copying unnecessary detail into L1.
4. Validate claim types, lifecycle, IDs, and sensitive-data boundaries.
5. Bind logical pointers in the new adapter.
6. Run acceptance tests in the new runtime.
7. Explicitly designate the new authoritative source.
8. Retain the old system as a read-only checkpoint until recovery confidence is
   established.

Migration is not bidirectional sync. Only one side becomes the active writer.
