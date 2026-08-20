# Identity and stable context

Store only identity facts with clear cross-session value. Avoid unnecessary
legal identifiers, precise location, or sensitive raw documents.

## Current records

```yaml
- id: FACT-IDENTITY-001
  type: Fact
  scope: global
  status: current
  statement: "{{MINIMAL_CONFIRMED_IDENTITY_FACT}}"
  effective_from: "{{ISO_8601_DATE}}"
  evidence: "Explicit user confirmation"
```

Remove the sample record if no identity fact is needed.
