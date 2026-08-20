# Roadmap

`src_you` is an early public reference implementation. The roadmap prioritizes
implementation evidence and semantic clarity over feature count. Items are
proposals, not commitments.

## Now

| Item | Why it matters | Exit signal |
|---|---|---|
| Collect implementation reports | Real storage and adapter use reveals boundary failures that prose review cannot | At least three de-identified reports from different setups |
| Strengthen conformance evidence | Repository fixtures check the contract, but adapters need behavioral traces | A small runner can record privacy-safe pass/fail evidence for all fourteen scenarios |
| Observe first-run friction | The private bootstrap is deliberately minimal; real users should determine what remains unclear | Repeated onboarding confusion is documented and resolved without expanding the core |
| Keep privacy a release gate | A public framework can still leak through examples, metadata, or history | Every release records pattern scan, semantic review, and history review |

## Next

| Item | Why it matters | Entry condition |
|---|---|---|
| Add one non-OpenAI reference adapter | A genuinely different platform is a stronger portability test than two related surfaces | A maintainer can verify current capabilities and limitations from primary sources |
| Draft an experimental state envelope | A small optional schema could improve interchange and fixture tooling | Implementation reports identify a stable shared field set |
| Publish migration guidance | Existing vault and memory users need normalization more often than greenfield setup | At least two real layouts can be described without exposing private state |
| Improve adapter conformance fixtures | Contributors need to know whether an adapter preserves semantics | The behavioral evidence format is stable enough to reuse |

Any experimental schema must remain non-mandatory. Markdown, JSON, YAML,
databases, and future stores can all conform if they preserve the semantics.

## Later

| Item | Why it matters | Constraint |
|---|---|---|
| Broader adapter ecosystem | More platforms can test portability and reveal capability gaps | Each adapter needs an owner, freshness date, limitations, and evidence |
| Interoperability profiles | Common mappings may reduce migration cost | Profiles cannot redefine canonical authority or force one storage format |
| Small implementation tooling | Repetitive validation and migration steps may deserve automation | Tooling must stay inspectable, optional, and local-first by default |

Hosted services, dashboards, authentication systems, vector databases, sync
servers, mobile apps, and telemetry are not current roadmap goals.

## Research

| Question | Why investigate it |
|---|---|
| State provenance | Authority is easier to audit when a durable claim can explain its evidence and update path |
| Temporal state | Effective periods and review conditions may model change better than a single timestamp |
| Multi-agent canonical authority | Several agents can act concurrently without becoming several canonical writers |
| Selective disclosure | Adapters need ways to reveal only the minimum state required for a task |
| Portable personal context | Logical pointers and typed lifecycle semantics may support migration without bulk copying |

Propose work through a focused issue. Include the problem, scope, acceptance
criteria, and non-goals; avoid feature lists without an implementation need.
