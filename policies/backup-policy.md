# Backup policy

Status: normative for `src_you` v0.1.0.

## Direction

```text
AUTHORITATIVE SOURCE
    -> CHECKPOINT
    -> DOWNSTREAM BACKUP
    -> VERSION HISTORY
```

Backup is not authority. Restore is an explicit recovery operation.

## Checkpoint trigger

Create a checkpoint after meaningful durable changes, such as a schema or policy
upgrade, major decision set, migration, milestone, authority change, or recovery.
Do not checkpoint every chat or transient L2 action.

## Independent evidence

Under the [operational contract](../docs/operational-contract.md), delivery,
canonical persistence, and checkpoint each receive their own PASS, FAIL,
BLOCKED, or NOT_RUN result and evidence. Checkpoint only after exact canonical
readback verifies persistence. A failed checkpoint does not negate a verified
canonical save, and a successful checkpoint cannot prove a failed or uncertain
update saved. Periodic audits and catch-up do not defer same-session durable
writes or change recovery direction.

## Required metadata

- restore-point label and timestamp;
- source identity and scope;
- sorted inventory, size, and SHA-256 per file;
- policy/schema version;
- excluded paths;
- change summary;
- integrity-verification result.

## Restore requirements

- explicit recovery intent;
- normal writes paused for affected scope;
- selected restore point named;
- manifest and hashes verified;
- privacy and schema compatibility reviewed;
- staged validation completed;
- recovered source explicitly designated authoritative;
- post-restore checkpoint created.

## Prohibited behavior

- bidirectional sync between canonical and backup writers;
- automatic overwrite because backup is newer;
- manual backup edits silently merged into canonical state;
- restore from an unverified archive;
- publishing a backup manifest that reveals private locators or file names;
- treating version history as an alternative live database.

Tests 8 and 9 cover this policy.
