# Audit an existing system

Use this prompt when a person already has a Second Brain, Obsidian vault, memory
service, project files, custom state system, or partial `src_you` implementation.
The goal is diagnosis and a minimal-change plan—not automatic reconstruction.

## Prompt

```text
Audit my existing personal-state system against the src_you v0.1 architecture.

Do not build a second system. Do not migrate, rename, delete, merge, restore, or
change authority during the audit unless I separately authorize implementation.
Read only the minimum material needed to establish topology, ownership, and
risk. Never reproduce secrets or unnecessary personal details in the report.

src_you invariants:

- one authoritative source and one active writer per state item/scope;
- Memory and chat history are cache, not authority;
- L1 contains cross-domain durable state only;
- L2 owns detailed project/domain state;
- updates use one current value plus superseded history;
- claims are typed Fact, Decision, Preference, Inference, or Open Loop;
- retrieval is minimal and scope-aware;
- backups are downstream and restore is explicit;
- personal state remains private by default;
- platform behavior belongs in adapters.

Perform these stages:

1. DISCOVER
   Inventory manifests, indexes, state stores, project sources, runtime rules,
   memory/cache layers, backup destinations, and version history. Use metadata
   first and targeted reads second.

2. MAP
   Map each component to L0, L1, L2, cache/evidence, checkpoint, backup, or
   unknown. Identify its owner, writers, read path, update path, and scope.

3. CLASSIFY RISKS
   Check for:
   - no declared authority or more than one writer;
   - duplicated active facts or preferences;
   - L2 micro-state copied into L1;
   - stale pointers or summaries;
   - inference stored as fact;
   - external current facts treated as permanent;
   - over-broad retrieval;
   - secrets, raw confidential files, or public/private mixing;
   - bidirectional backup sync or newest-timestamp recovery;
   - platform-specific rules embedded in the core.

4. VERIFY SAMPLES
   For each material risk, provide a minimal de-identified example and the
   authoritative path that supports the finding. Do not dump entire files.

5. PROPOSE MINIMUM CHANGE
   Rank findings as critical, high, medium, or low. For each, propose the
   smallest reversible correction, expected effect, rollback, and acceptance
   scenario. Prefer normalization and pointer repair over migration.

6. REPORT
   Return:
   - topology and L0/L1/L2 map;
   - authority/writer matrix;
   - duplication and staleness findings;
   - privacy and backup findings;
   - acceptance-test gaps;
   - a phased, reversible remediation plan;
   - the smallest decisions or permissions required from me.

Stop and ask one focused question only if you cannot distinguish competing
authoritative sources. Otherwise finish the read-only audit without asking me
to perform manual inventory work you can do with available tools.
```
