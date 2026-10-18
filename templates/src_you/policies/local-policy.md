# Local policy overlay

The framework policies define the default contract. This file records only
implementation-specific choices that do not weaken privacy or authority rules.

```yaml
# Adopted framework policy baseline; this does not set manifest schema_version.
# Fill only after the implementation passes the target release's acceptance set.
framework_version: "{{ADOPTED_FRAMEWORK_VERSION}}"
authoritative_store: "{{AUTHORITATIVE_STORE}}"
checkpoint_destination: "{{PRIVATE_DOWNSTREAM_DESTINATION}}"
checkpoint_trigger: meaningful_durable_change
external_fact_revalidation: at_use_time
```

The manifest's `schema_version` describes the data shape. `framework_version`
records the framework policy baseline this implementation has adopted. Keep
them independent; adopting policy updates does not itself migrate the schema.

## Local decisions

- `{{LOCAL_POLICY_DECISION_WITH_DURABLE_VALUE}}`

Do not copy platform secrets or private object IDs into this file when a secure
adapter registry can hold them.
