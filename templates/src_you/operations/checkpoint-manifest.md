# Checkpoint manifest

This human-readable record accompanies a machine-generated inventory. It must
not contain secret values or publicize private locators.

```yaml
checkpoint_id: "{{CHECKPOINT_ID}}"
created_at: "{{ISO_8601_TIMESTAMP_WITH_TIMEZONE}}"
schema_version: 0.1.0
source_scope: src_you://global
change_summary: "{{MEANINGFUL_DURABLE_CHANGE}}"
inventory_file: "{{MANIFEST_FILENAME}}"
hash_algorithm: sha256
integrity_verified: true
restore_requires_explicit_approval: true
```

The downstream copy is not an active writer.
