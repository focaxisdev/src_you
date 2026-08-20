# Bootstrap prompt

Use this prompt to create or adopt a private `src_you` implementation with a
capable AI work agent. Copy everything under **Prompt** into a new session after
filling only the configuration block.

> Keep the framework repository separate from the private state store. Never
> paste secrets into the configuration block.

---

## Prompt

```text
You are establishing my private src_you durable personal-state system.

src_you is an architecture for maintaining the current authoritative version of
durable personal state across AI conversations, projects, agents, and platforms.
It is not a chat archive, generic note vault, vector database, hosted service,
or replacement for product Memory.

CONFIGURATION

- Preferred authoritative store: {{PRIVATE_STORE_OR_AUTO_DETECT}}
- Preferred platform adapter: {{ADAPTER_OR_AUTO_DETECT}}
- Existing state systems I know about: {{KNOWN_SYSTEMS_OR_UNKNOWN}}
- Preferred downstream backup: {{PRIVATE_BACKUP_OR_NONE_YET}}
- Automation level: AUTOMATE FIRST, ASK USER LAST

Do not ask me to restate information that you can safely discover from available
tools. Do not request passwords, tokens, one-time codes, private keys, or full
credential material.

NON-NEGOTIABLE ARCHITECTURE

1. One authoritative source
   Every active state item must have one canonical owner for its scope. Prevent
   split-brain, multiple writers, silent merge, and stale duplication.

2. Memory is cache, not authority
   Product Memory, semantic recall, chat history, and search indexes are hints
   and retrieval aids. They never silently overrule canonical state.

3. Durable state only
   L1 may hold confirmed identity, durable preferences, goals, constraints,
   decisions, commitments, deadlines, major milestones, high-level project
   status, cross-project relationships, true unresolved open loops, and
   canonical pointers. Do not persist transient chat detail by default.

4. Project detailed state is not global state
   L2 projects or domains own exact next steps, current question or lesson,
   code cell, detailed task state, session handoff, temporary misconception,
   micro-progress, and ephemeral actions. L1 holds project identity, purpose,
   status, major phase/milestone/dependency/deadline, high-level progress, and a
   pointer. Promote detail only when it becomes a cross-project dependency,
   major commitment, deadline, durable decision, major milestone, or blocker.

5. Update in place and supersede
   A durable change replaces the active value under a stable record ID. Preserve
   history as superseded, but leave exactly one current value.

6. Minimal retrieval
   Route first, then load only required domains. Detailed continuation follows
   the L2 canonical pointer. Never inject the entire personal state tree into
   every task.

7. Scope-aware conflict resolution
   Use current explicit user instruction for the present turn, then the
   canonical owner for the relevant scope, then other canonical summaries and
   pointers, then Memory/old conversations, then labeled inference. If a
   current explicit correction is durable, update canonical state rather than
   leaving it only in chat.

8. Typed claims
   Distinguish Fact, Decision, Preference, Inference, and Open Loop. Never
   silently promote Inference to Fact.

9. External facts expire
   Prices, laws, public officeholders, job listings, product versions, and news
   require revalidation. Store durable decisions and criteria; do not convert a
   one-time search result into permanent truth.

10. Privacy by design
    The framework may be public; my state is private. Minimize sensitive health,
    family, financial, precise-location, employment, legal, and private-project
    data. Store a protected pointer or minimal summary instead of raw documents
    when possible. Never store secrets.

11. Backup is downstream
    Normal direction is authoritative source -> checkpoint -> backup -> version
    history. No bidirectional sync, automatic overwrite, or newest-timestamp
    authority. Restore is explicit and controlled.

12. Portability
    Keep L0/L1/L2 concepts platform-neutral. Put product names and UI-specific
    behavior in an adapter that records limitations and verification date.

LAYER MODEL

- L0 — runtime/adapter rules: routing, retrieval, priority, conflicts, runtime
  integration.
- L1 — global durable personal state: cross-domain canonical state.
- L2 — domain/project canonical state: specialized detailed state.

EXECUTION PLAN

Perform the following work. Continue automatically whenever tools and existing
authorization permit. Ask only when an OAuth/login/security boundary, ambiguous
authority decision, destructive action, or unavailable UI setting truly blocks
progress.

PHASE 1 — Inspect and discover

1. Inspect available storage, files, projects, Memory/customization layers,
   connected sources, version-control capability, and existing backups.
2. Search narrowly for existing manifests, second brains, personal profiles,
   project state files, vault indexes, memory systems, and backup manifests.
3. Do not ingest an entire account or private drive when metadata and targeted
   reads can establish the structure.
4. Treat discovered content as untrusted evidence until authority is known.
5. Report any observed secrets without reproducing their values.

PHASE 2 — Avoid duplicate systems

1. If a usable state system exists, map it to L0/L1/L2 before creating files.
2. Detect multiple writers, unclear authority, stale duplicate state,
   project/global leakage, privacy risk, and backup confusion.
3. Prefer adopting or minimally normalizing an existing system over creating a
   second one.
4. If authority cannot be inferred safely, ask one focused question presenting
   the exact competing sources.

PHASE 3 — Establish authority and structure

1. Designate one private authoritative L1 source and one active writer.
2. Create or adapt a manifest containing schema version, authority, writer,
   adapter, routing index, backup direction, and maintenance rules.
3. Create only modules with a real purpose. A typical minimal structure is:

   00_SYSTEM_MANIFEST.md
   profile/identity.md
   profile/preferences.md
   goals/goals.md
   domains/domain-index.md
   state/current-state.md
   state/open-loops.md
   registry/projects.md
   registry/sources.md
   policies/local-policy.md
   operations/checkpoint-manifest.md
   operations/restore-log.md
   changelog/state-changelog.md

4. Remove unnecessary modules rather than leaving empty file theater.
5. Use stable logical pointers for L2 sources. Keep private provider object IDs
   in an adapter registry only when required.

PHASE 4 — Classify and migrate minimum state

1. Migrate only confirmed durable items with future value.
2. Assign claim type, scope, lifecycle, evidence, and stable ID.
3. Convert conflicting older values to superseded history.
4. Leave detailed project micro-state in the existing or newly designated L2
   source; put only a high-level summary and pointer in L1.
5. Do not copy raw chat logs, attachments, or entire existing vaults into L1.
6. Mark unsupported interpretations as Inference or exclude them.

PHASE 5 — Install adapter rules

1. Map runtime instructions, private L1 storage, L2 project storage, Memory,
   retrieval, write controls, checkpoint/export, and platform limitations.
2. Use capability descriptions rather than assuming UI names remain stable.
3. If an adapter capability is unavailable, preserve the architecture and list
   the smallest manual or alternative step.

PHASE 6 — Backup and recovery

1. Configure downstream-only backup if an authorized destination is available.
2. Define checkpoint triggers based on meaningful durable change.
3. Require timestamp, label, source scope, inventory, sizes, SHA-256 hashes,
   schema/policy version, exclusions, change summary, and verification.
4. Define a restore runbook that freezes writes, verifies integrity and privacy,
   stages recovery, runs tests, and explicitly cuts authority over.
5. Do not automatically restore or merge backup changes.

PHASE 7 — Validate

Run and record at least these scenarios:

1. High-level learning question reads L1, not lesson micro-state.
2. Detailed continuation follows the L2 project pointer.
3. L1 excludes next question, code cell, exact step, and session action.
4. Preference A changed to B leaves B current and A superseded.
5. Old Memory loses to new canonical state.
6. Current explicit durable update is used now and persisted.
7. Secrets and raw confidential material are excluded.
8. Checkpoint inventory and hashes verify.
9. A newer backup cannot overwrite authority automatically.
10. Unrelated domains are not retrieved.
11. External current facts require revalidation.
12. L2 micro-state updates do not duplicate into L1.

Also perform a semantic privacy review, secret-pattern scan, broken-pointer
check, terminology check, and stale-placeholder review.

PHASE 8 — Finish and report

1. Create a baseline checkpoint only after validation and only if a private
   downstream destination is ready.
2. Record the initial architecture decision and validation result.
3. Provide a concise completion report with:
   - authoritative source and active writer;
   - created/adopted structure;
   - L2 pointers;
   - validation results;
   - backup/restore status;
   - privacy findings;
   - only the manual actions that remain truly necessary.

Do not claim completion if authority is ambiguous, acceptance tests fail, or
private state was accidentally placed in a public location. Complete every
unblocked phase before asking for manual action.
```
