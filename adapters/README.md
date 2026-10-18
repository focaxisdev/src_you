# Adapter contribution guide

An adapter maps the platform-neutral `src_you` contract to capabilities that a
specific AI surface actually provides. It is not a new core architecture and it
must not promise unavailable product features.

## Reference adapters

| Adapter | Design center | Status |
|---|---|---|
| [`chatgpt/`](chatgpt/) | ChatGPT instructions, projects, files/sources, and Memory | Reference |
| [`codex/`](codex/) | Local project instructions, filesystem state, and Codex Memory | Reference |

## Required capability map

Every adapter must document:

1. where L0 runtime guidance lives and how precedence works;
2. how a private L1 store is read and updated;
3. how L2 project detail remains separate;
4. which recall or history features are non-authoritative cache;
5. how minimal retrieval is achieved;
6. how writes, stable IDs, and supersession are controlled;
7. how checkpoints and explicit restore can work;
8. unavailable capabilities and manual boundaries;
9. the date and primary sources used to verify external product behavior;
10. independent read, create, guarded-update, and exact-readback evidence,
    identity/version handling, and unknown-outcome reconciliation under the
    [operational contract](../docs/operational-contract.md);
11. separate delivery, persistence, and checkpoint statuses, with only dependent
    actions blocked when a capability is missing.
12. execution entrypoints, their required policy IDs/revisions and dependencies,
    precedence and approved local overrides, and failure conditions that stop
    an entrypoint, following the [execution reliability contract](../docs/execution-reliability.md);
13. cold/scheduled-context capability evidence and future-run evidence. An
    interactive operation or schedule-acceptance response alone does not prove
    a later run succeeded.

## Contribution checklist

- Start from current first-party documentation and verify the actual surface.
- Describe capabilities before provider UI labels.
- Keep private object identifiers out of examples.
- Include a compact L0 instruction block, not a copy of personal state.
- Show how the adapter routes high-level state to L1 and detail to L2.
- Treat product Memory, generated memory, and chat history as cache.
- State what the adapter cannot enforce. Generic contract requirements and
  synthetic tests do not newly verify external capabilities or justify changing
  the capability-check date.
- Exercise Test 14 and the other affected acceptance scenarios.
- Update the capability-check date when behavior is reverified.

Open an adapter proposal before adding a large integration, runtime, service,
or dependency. A high-quality adapter for one verified surface is more useful
than several speculative mappings.
