# Fictional conflict-resolution example

> All records are synthetic.

## Starting state

```yaml
id: PREF-MEETINGS-001
type: Preference
scope: global
status: current
statement: "Prefer afternoon meetings."
effective_from: 2026-01-10
```

Cached Memory also recalls “prefers afternoon meetings.”

## Explicit change

The fictional user says:

> From now on, schedule focused meetings in the morning; my work pattern has
> changed.

## Correct result

Use the morning preference immediately and update the existing canonical ID:

```yaml
id: PREF-MEETINGS-001
type: Preference
scope: global
status: current
statement: "Prefer focused meetings in the morning."
effective_from: 2026-08-20
supersedes:
  statement: "Prefer afternoon meetings."
  effective_from: 2026-01-10
  status: superseded
evidence: "Explicit durable user instruction"
```

The stale Memory does not create a conflict in the answer. It may be repaired or
ignored, but it cannot overwrite the canonical value.

## Incorrect results

- keeping both preferences `current`;
- saying “Memory disagrees, so please choose” when the current instruction is
  explicit;
- using morning only in the current chat while leaving afternoon canonical;
- deleting all history so the change cannot be audited;
- promoting an unrelated inference about meeting duration.
