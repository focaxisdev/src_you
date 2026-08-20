# Local policy overlay

The framework policies define the default contract. This file records only
implementation-specific choices that do not weaken privacy or authority rules.

```yaml
framework_version: 0.1.0
authoritative_store: "{{AUTHORITATIVE_STORE}}"
checkpoint_destination: "{{PRIVATE_DOWNSTREAM_DESTINATION}}"
checkpoint_trigger: meaningful_durable_change
external_fact_revalidation: at_use_time
```

## Local decisions

- `{{LOCAL_POLICY_DECISION_WITH_DURABLE_VALUE}}`

Do not copy platform secrets or private object IDs into this file when a secure
adapter registry can hold them.
