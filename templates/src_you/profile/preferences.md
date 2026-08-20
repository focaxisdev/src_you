# Durable preferences and constraints

Use stable IDs. When a preference changes, update its current value and preserve
the previous value as superseded history rather than adding a competing active
record.

```yaml
- id: PREF-{{DOMAIN}}-001
  type: Preference
  scope: global
  status: current
  statement: "{{CONFIRMED_DURABLE_PREFERENCE}}"
  effective_from: "{{ISO_8601_DATE}}"
  supersedes: null
  evidence: "Explicit user instruction"
```

Do not infer sensitive preferences from isolated behavior.
