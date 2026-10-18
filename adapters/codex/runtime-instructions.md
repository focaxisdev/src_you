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

For ordinary tasks without an established-state dependency, retrieve no personal
state. Reuse a verified relevant read during uninterrupted task continuity;
refresh on resume, known source/version change, conflict, or before a write.

Apply the src_you operational contract (docs/operational-contract.md): bind each
update to the same canonical source identity, stable record ID, and scope;
freshly read and use an atomic version guard. After a conflict, reread and
three-way merge unrelated edits; block overlapping changes. Verify exact
same-target readback before saying saved. An unknown mutation outcome requires
a read before any retry; never create as fallback for failed update.

Read, create, guarded update, and readback need independent evidence. Report
delivery, canonical persistence, and checkpoint separately as PASS, FAIL,
BLOCKED, or NOT_RUN. Missing access or capabilities block only dependent work;
identify the exact missing scope or operation without inventing state or
substituting Memory. Keep authorized durable changes in the same work session
when possible; periodic maintenance is audit/catch-up only.

For unattended work, validate entry policy revisions and required dependencies
under docs/execution-reliability.md. Classify errors before bounded safe-read
retries; permanent denial stops dependent work. Reconcile unknown effects and
completed operations on resume. Keep schedule acceptance, run start, source
access, persistence, backup, and notification evidence separate. Do not infer
future automation reliability from an interactive success.
```

Codex discovers layered `AGENTS.md` files from global scope through the project
path. Keep this block small enough to remain durable guidance; the actual state
belongs in the private canonical files it points to.

The [operational contract](../../docs/operational-contract.md) defines these
requirements; it does not establish provider capabilities.
