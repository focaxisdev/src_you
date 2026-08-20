# Codex reference adapter

This adapter maps `src_you` to current local Codex capabilities. It uses checked
or local instruction files for L0, a user-controlled filesystem location for L1,
and the current project tree or another registered source for L2. It does not
make Codex Memory authoritative.

## Mapping

| `src_you` role | Codex-oriented mapping |
|---|---|
| L0 runtime rules | Layered global and project `AGENTS.md` guidance |
| L1 global durable state | Private files outside public repositories, available only through authorized filesystem access |
| L2 project detailed state | Project-local canonical files or another registered project source |
| Memory | Local generated recall layer; useful cache, not required guidance or canonical state |
| Checkpoint / backup | Explicit filesystem or private Git checkpoint copied downstream |

Codex CLI uses its starting directory as the project context. The IDE extension
uses the selected workspace. Neither should be assumed to expose the ChatGPT
Projects view or every private location. Filesystem sandbox and approval rules
still control what Codex can read and write.

## Recommended setup

1. Create or adopt one private L1 store outside the public framework checkout.
2. Put cross-project routing behavior in private global guidance when
   appropriate; keep personal values in the private state files, not in
   `AGENTS.md`.
3. Put project-specific L0 rules near the project root. Register the L2
   canonical source and fields it owns.
4. Keep an L1 logical pointer and lossy phase summary. Do not copy the L2 next
   action, code position, handoff, or temporary blocker into L1.
5. Ensure the current sandbox can reach only the state required for the task.
6. Treat local Codex Memory and resumed chat transcripts as recall aids.
7. Checkpoint only after meaningful durable changes; restore through an
   explicit staged operation.

If a repository is public, do not check in a private manifest locator. Keep the
locator in private global guidance or another untracked, access-controlled local
configuration.

## Files

- [`runtime-instructions.md`](runtime-instructions.md) — compact L0 block for a
  private global or project instruction layer.
- [`capability-notes.md`](capability-notes.md) — verified behavior, sources, and
  limitations.

Use [`../../docs/quick-start.md`](../../docs/quick-start.md) for the framework
setup and [`../../tests/acceptance-tests.md`](../../tests/acceptance-tests.md)
for behavioral evidence.
