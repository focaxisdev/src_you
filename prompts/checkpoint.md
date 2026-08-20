# Create a checkpoint

Use this prompt after a meaningful durable change—not after every chat.

## Prompt

```text
Create a verified downstream src_you checkpoint for the meaningful durable
change I identify below.

Change summary: {{MEANINGFUL_DURABLE_CHANGE}}
Scope: {{LOGICAL_SCOPE_OR_GLOBAL}}
Destination: {{AUTHORIZED_PRIVATE_BACKUP_DESTINATION}}

This is a checkpoint operation, not a restore, migration, bidirectional sync, or
authority change. The canonical source remains authoritative.

Before writing:

1. Confirm the scope and authoritative source from the manifest.
2. Confirm the change is durable enough to justify a restore point.
3. Inspect source status and ensure no unresolved writer conflict exists.
4. Exclude secrets, credentials, caches, temporary files, raw confidential
   documents, and provider-only transient metadata.
5. If the destination is public or has broader access than the source, stop and
   report the privacy mismatch without copying data.

Create a deterministic manifest containing:

- checkpoint ID and human-readable version label;
- ISO 8601 creation time with timezone;
- schema and policy version;
- logical source identity and scope;
- sorted relative file inventory;
- byte size and SHA-256 for every included file;
- explicit exclusions;
- minimal non-sensitive change summary;
- intended restore use;
- integrity result.

Copy source -> checkpoint -> downstream backup in one direction. Do not treat
direct edits at the destination as canonical changes. Do not use newest
timestamp wins.

After copying:

1. Recalculate destination inventory and hashes.
2. Compare them to the checkpoint manifest.
3. Verify file count and total bytes.
4. Record success or exact mismatch without reproducing sensitive content.
5. Add a minimal checkpoint entry to the canonical changelog only after
   verification succeeds.

Report checkpoint ID, source scope, destination class (not a secret locator),
file count, total bytes, hash algorithm, verification result, exclusions, and
whether any manual authorization remains. Do not claim success on a partial or
unverified copy.
```
