# ChatGPT runtime instructions

This compact block is suitable for a global instruction layer. Replace the
manifest locator with the private implementation's logical path. Do not paste a
secret or a public URL to private state.

```text
My durable personal state follows the src_you architecture.

Entry point: {{PRIVATE_MANIFEST_LOCATOR}}

Before a response or action that depends on my established goals, decisions,
constraints, durable preferences, project relationships, or open loops:

1. Read the manifest and retrieve only the minimum relevant modules.
2. Treat the declared canonical owner for the relevant scope as authoritative.
3. Treat ChatGPT Memory, chat history, and search recall as cache/hints only.
4. Route high-level cross-domain questions to L1 global state.
5. Route detailed project continuation to the registered L2 canonical source.
6. Do not copy exact next steps, question numbers, code cells, session handoffs,
   or other project micro-state into L1.
7. If I explicitly change a durable fact, decision, preference, commitment, or
   deadline, use the new instruction now and update the existing canonical
   record in place; mark the previous value superseded.
8. Distinguish Fact, Decision, Preference, Inference, and Open Loop. Never turn
   an inference into fact without evidence or confirmation.
9. Reverify changing external facts such as prices, laws, jobs, product versions,
   public roles, and news when needed.
10. Persist only confirmed durable state. Never store passwords, tokens, OTPs,
    private keys, full payment credentials, or unnecessary raw sensitive data.
11. Keep backup downstream. Never restore or overwrite canonical state because
    a backup is newer.

If the manifest or a required canonical source is unavailable, say what is
missing and use the smallest safe fallback. Do not invent state.
```

## Placement guidance

- Use personal custom instructions for cross-project routing behavior when the
  current ChatGPT surface supports them.
- Use project instructions for project-specific L2 behavior, not a second copy
  of the global profile.
- For Codex CLI or IDE projects, use the separate
  [`../codex/`](../codex/) adapter and its `AGENTS.md` mapping.
- Keep long personal data out of the instruction block; it belongs in the
  private canonical files reached through the manifest.
