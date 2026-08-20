# Capability notes

Checked: **2026-08-20**. These are external product observations, not permanent
truth. Verify current official OpenAI documentation before relying on them.

## Capability probe

Before bootstrap, determine which surface and tools are actually available:

| Probe | Why it matters |
|---|---|
| Can the agent read and update persistent private files? | Required for an agent-maintained L1 store |
| Is ChatGPT Library available to this account/surface? | Candidate persistent store; availability is not universal |
| Can files be organized and found reliably? | Needed for manifest and module routing |
| Are ChatGPT Projects available? | Candidate L2 boundary |
| Can project instructions and sources be maintained? | Needed for L2 runtime rules |
| Is Memory enabled? | Determines available cache behavior, not authority |
| Can the environment create/export files and use connected stores? | Determines checkpoint automation |
| Which actions require UI confirmation or OAuth? | Defines the manual boundary |

## Current observations

### Memory

Official documentation describes Memory as a way to carry useful context across
chats and advises keeping required guidance in instructions or checked-in
documentation. The adapter therefore treats Memory as a helpful cache, never the
only authority.

Source: [Memories](https://learn.chatgpt.com/docs/customization/memories).

### Custom and project instructions

Custom instructions can carry cross-chat preferences and runtime guidance.
Project instructions apply within a project. Use them for L0 behavior and L2
scope rules, not as a bulk personal database.

Sources: [Personalize ChatGPT](https://learn.chatgpt.com/docs/personalize) and
[Projects and chats](https://learn.chatgpt.com/docs/projects).

### Projects

Projects group related chats, files, instructions, and connected sources. This
fits the L2 project boundary, but project availability and behavior may vary by
surface. Do not assume a ChatGPT Project is a filesystem or universally exposed
to CLI/IDE clients.

Source: [Projects and chats](https://learn.chatgpt.com/docs/projects).

### File Library

OpenAI's plugin reference describes the ChatGPT file library as optional and
requires capability detection for file selection. A bootstrap must therefore
offer another private canonical store when Library is unavailable.

Source: [File APIs](https://developers.openai.com/plugins/reference#file-apis).

## Known limitations

- UI names, availability, and write capabilities can change.
- Memory updates may not be immediate or fully inspectable on every surface.
- A project and a local code directory are different concepts on some clients.
- No platform feature automatically enforces `src_you` authority; the manifest,
  policies, adapter rules, and acceptance tests provide that governance.
- OAuth, repository creation, connector installation, and some sharing changes
  may require explicit user interaction.

When a capability is missing, preserve the core invariants and document the
degraded path. Do not invent a feature or silently replace authority.
