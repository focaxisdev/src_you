# Restore from a checkpoint

Restore is a controlled recovery operation. It is never triggered solely by a
newer backup timestamp.

## Prompt

```text
Prepare and, where authorized, execute an explicit src_you restore.

Affected canonical scope: {{LOGICAL_SCOPE}}
Selected restore point: {{CHECKPOINT_ID}}
Recovery reason: {{REASON}}

Do not assume the backup is correct because it is newer. Do not merge direct
backup edits into canonical state. Do not change authority until validation is
complete and an explicit cutover is authorized.

STAGE 1 — Establish recovery intent

1. Read the active manifest and confirm the affected authoritative source.
2. Freeze or pause normal writes for the affected scope when possible.
3. Record the selected restore point and expected recovery boundary.
4. If this action would overwrite healthy canonical data or delete material not
   covered by the request, stop before mutation and request focused approval.

STAGE 2 — Verify the checkpoint

1. Read the checkpoint manifest.
2. Verify sorted inventory, file count, byte sizes, and SHA-256 hashes.
3. Confirm schema/policy compatibility and source-scope match.
4. Scan for secrets, private-scope mismatch, corrupt files, and unexpected
   content.
5. Reject an incomplete, mismatched, or untrusted checkpoint.

STAGE 3 — Compare and plan

1. Compare restored values to current values by stable ID, scope, claim type,
   and lifecycle.
2. Identify what will change, what will remain, and what post-checkpoint durable
   changes could be lost.
3. Produce a reversible restore plan and staging location.
4. Never resolve conflicts by silent merge or newest timestamp.

STAGE 4 — Stage and validate

1. Restore to staging or a new version when the platform permits.
2. Run all twelve src_you acceptance scenarios.
3. Check pointers, terminology, privacy, secrets, and project/global boundaries.
4. Verify that exactly one current value exists per record/scope.

STAGE 5 — Cut over

1. Present the exact validated cutover effect if a final destructive or
   authority-changing approval is still required.
2. Promote the staged result as authoritative only after approval and successful
   validation.
3. Retire the damaged source as historical/recovery evidence; do not leave it
   writable as a competing authority.
4. Resume writes.

STAGE 6 — Close

1. Create a post-restore checkpoint.
2. Record a non-sensitive restore log containing restore ID, point, scope,
   integrity result, test result, cutover time, and outcome.
3. Report lost or unresolved post-checkpoint changes explicitly.

If any integrity, privacy, scope, or authority check fails, stop before cutover
and return the verified partial findings. Never claim a restore completed when
only files were copied.
```
