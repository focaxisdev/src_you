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
9. the date and primary sources used to verify external product behavior.

## Contribution checklist

- Start from current first-party documentation and verify the actual surface.
- Describe capabilities before provider UI labels.
- Keep private object identifiers out of examples.
- Include a compact L0 instruction block, not a copy of personal state.
- Show how the adapter routes high-level state to L1 and detail to L2.
- Treat product Memory, generated memory, and chat history as cache.
- State what the adapter cannot enforce.
- Exercise Test 14 and the other affected acceptance scenarios.
- Update the capability-check date when behavior is reverified.

Open an adapter proposal before adding a large integration, runtime, service,
or dependency. A high-quality adapter for one verified surface is more useful
than several speculative mappings.
