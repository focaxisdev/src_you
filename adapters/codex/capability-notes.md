# Codex capability notes

Checked: **2026-08-20**. These are external product observations and must be
reverified before changing an implementation.

## Verified capabilities

### Layered project guidance

Codex reads `AGENTS.md` guidance before work. It combines global guidance with
files discovered from the project root toward the current working directory;
closer guidance can override earlier layers. This makes `AGENTS.md` suitable for
L0 routing rules, not for bulk personal state.

Source: [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

### Local project context

Codex CLI treats the directory where it starts as the project, while the IDE
extension uses the selected folder or workspace. These surfaces do not expose
the ChatGPT Projects view. Durable project guidance should therefore remain in
checked-in or private local documentation that the current project can reach.

Source: [Projects and chats](https://learn.chatgpt.com/docs/projects).

### Local Memory

Local Codex clients can use a separate generated memory store when the feature
is enabled. Official guidance says to keep required team rules in `AGENTS.md` or
checked-in documentation and to treat memories as a helpful recall layer. This
matches `src_you`'s cache-not-authority rule.

Source: [Memories](https://learn.chatgpt.com/docs/customization/memories).

## Limitations

- A filesystem path is not readable merely because an instruction names it;
  sandbox scope and user authorization still apply.
- `AGENTS.md` is guidance, not a transactional state database or authority
  enforcement engine.
- Local Memory may be disabled, delayed, generated, or unavailable on a given
  host. The adapter cannot depend on it for current canonical state.
- Chat transcripts and resumed sessions preserve work history but do not
  establish canonical ownership.
- A public repository must not contain private L1 values or sensitive locators.
- No Codex feature automatically enforces one active writer, supersession, or
  restore safety; the manifest, files, workflow, and acceptance evidence do.

When a capability is absent, preserve the core model and document the smallest
safe fallback. Do not invent a provider feature.
