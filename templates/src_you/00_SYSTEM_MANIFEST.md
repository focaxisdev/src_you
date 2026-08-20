# src_you system manifest

```yaml
system: src_you
schema_version: 0.1.0
status: active
authoritative_source: "{{AUTHORITATIVE_STORE}}"
active_writer: "{{ACTIVE_WRITER}}"
authority_effective_from: "{{ISO_8601_DATE}}"
default_adapter: "{{ADAPTER_NAME}}"
backup_mode: downstream_only
```

## Authority contract

- This manifest designates one authoritative source for L1 global state.
- L2 project sources are registered in
  [`registry/projects.md`](registry/projects.md).
- Memory, chat history, search indexes, and backups are non-authoritative.
- Restore or authority change requires an explicit operation.

## Routing index

| Need | Read first | Follow when needed |
|---|---|---|
| Identity or stable context | [`profile/identity.md`](profile/identity.md) | Relevant protected evidence only |
| Durable preferences | [`profile/preferences.md`](profile/preferences.md) | Domain record if scoped |
| Goals and commitments | [`goals/goals.md`](goals/goals.md) | Related domain and project pointer |
| High-level domain state | [`domains/domain-index.md`](domains/domain-index.md) | Registered L2 canonical source |
| Current open loops | [`state/open-loops.md`](state/open-loops.md) | Owning domain/project |
| Project pointer | [`registry/projects.md`](registry/projects.md) | L2 detailed state |
| Source authority | [`registry/sources.md`](registry/sources.md) | Adapter capability notes |
| Retrieval/update rules | [`policies/local-policy.md`](policies/local-policy.md) | Framework policy version |
| Recovery | [`operations/checkpoint-manifest.md`](operations/checkpoint-manifest.md) | Selected verified checkpoint |

## Runtime rules

1. Retrieve the minimum relevant modules.
2. Route detailed continuation to L2 rather than copying it into L1.
3. Use one current value per stable record ID and scope.
4. Keep Inference distinct from Fact, Decision, and Preference.
5. Reverify changeable external facts at use time.
6. Never write secrets to this state tree.
7. Keep backups downstream; never apply “newest timestamp wins.”

## Maintenance

Record durable system changes in
[`changelog/state-changelog.md`](changelog/state-changelog.md). Create a
checkpoint only after a meaningful durable change.
