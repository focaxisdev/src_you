# Core concepts

This glossary is normative for repository terminology.

## State versus memory

**State** is a maintained representation of what currently holds. It has an
owner, scope, lifecycle, and update rule.

**Memory** is recalled context derived from prior interactions or observations.
It can be useful and accurate, but it may be incomplete, delayed, or stale.

Therefore:

```text
MEMORY != STATE
CHAT_HISTORY != CURRENT_STATE
```

## Authoritative source

The designated source allowed to define current canonical state for a scope. A
system may have multiple stores, but only one active writer may claim authority
for the same state item and scope.

## Canonical state

State whose active value is owned by the authoritative source. “Canonical” does
not mean permanently true; it means the maintained version to use until valid
evidence or an explicit update changes it.

## Durable state

Information expected to matter across sessions. Durability depends on meaning,
not age. A decision made seconds ago can be durable; a week of temporary task
steps can remain transient.

Durable candidates include identity, long-lived preferences, goals,
constraints, decisions, commitments, deadlines, major milestones, cross-project
relationships, and unresolved open loops.

## Global state

L1 cross-domain durable state. It contains high-level project status and
canonical pointers, not detailed project progress.

## Project detailed state

L2 specialized state for a domain, project, course, workflow, or agent. It may
change frequently and may use a specialized schema.

```text
PROJECT_DETAILED_STATE != GLOBAL_STATE
```

## Current and superseded

`current` is the single active value for a record and scope. `superseded` is a
historical value that has been explicitly replaced.

Deletion is not required to resolve a conflict. History may remain, but it must
not be eligible as active state.

## Claim types

| Type | Meaning | Example |
|---|---|---|
| **Fact** | Supported description of the person or environment | “The user works in UTC+1.” |
| **Decision** | A chosen course that should guide later work | “Use the private repository as the canonical store.” |
| **Preference** | A durable tendency or choice, often revisable | “Prefer concise weekly summaries.” |
| **Inference** | A model-derived hypothesis not confirmed as fact | “They may prefer morning meetings.” |
| **Open Loop** | An unresolved obligation, question, dependency, or follow-up | “Choose a venue before 30 September.” |

Inferences must remain visibly typed and must not silently become Facts.

## Canonical pointer

A stable reference from L1 to the L2 source that owns detailed state. Pointers
should be resolvable inside the chosen platform without embedding secrets or
publicly exposing private identifiers.

## Checkpoint

A verified, read-only recovery snapshot of canonical state at a meaningful
point. A checkpoint includes an inventory, hashes, version label, timestamp,
and restore metadata.

## Restore

An explicit, controlled operation that reconstructs canonical state from a
selected checkpoint. Restore never occurs solely because a backup has a newer
timestamp.

## Adapter

A platform-specific mapping between L0/L1/L2 concepts and available runtime,
storage, project, memory, and backup capabilities. Adapters may change as
platforms change; the core architecture remains stable.

## Suggested record envelope

The core does not require YAML, but implementations should preserve equivalent
fields:

```yaml
id: PREF-COMMS-001
type: Preference
scope: global
status: current
statement: "Prefer a weekly written update."
effective_from: 2026-08-20
supersedes: null
evidence:
  - "Explicit user instruction"
review_after: null
```

Use stable IDs when a record changes. Update the active record rather than
creating near-duplicate IDs for every revision.

## External current facts

Prices, laws, policies, job listings, public officeholders, software versions,
and news can become stale independently of the user. Store them only when they
support a durable decision, and then include observation date, source, and a
revalidation rule. Do not turn one search result into permanent personal truth.
