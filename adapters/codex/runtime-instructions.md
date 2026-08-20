# Codex runtime instructions

Place this block in a private global or project `AGENTS.md` layer and replace
logical locators. Do not check a private locator into a public repository.

```text
This environment follows the src_you durable personal-state contract.

L1 manifest: {{PRIVATE_L1_MANIFEST_LOGICAL_LOCATOR}}
L2 project state: {{PROJECT_L2_LOGICAL_POINTER_OR_NONE}}

When established personal or project state matters:

1. Read the manifest, then only the minimum relevant L1 modules.
2. Follow the registered L2 pointer only for detailed project continuation.
3. Treat Codex Memory, chat transcripts, search indexes, imports, and backups as
   non-authoritative evidence or cache.
4. Use one canonical owner and one current value per state item and scope.
5. Supersede a durable old value when an explicit current update replaces it.
6. Keep project next steps, code positions, handoffs, and temporary blockers in
   L2; keep only durable summaries and pointers in L1.
7. Keep Fact, Decision, Preference, Inference, and Open Loop distinct. Do not
   promote Inference without evidence or confirmation.
8. Reverify changing external facts at use time.
9. Never store secrets or unnecessary raw sensitive evidence.
10. Keep checkpoint flow downstream and restore explicit.

If the required source is outside the active sandbox or unavailable, identify
the missing logical scope. Do not invent state or silently substitute Memory.
```

Codex discovers layered `AGENTS.md` files from global scope through the project
path. Keep this block small enough to remain durable guidance; the actual state
belongs in the private canonical files it points to.
