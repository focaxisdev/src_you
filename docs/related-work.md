# Related work and differentiation

`src_you` sits beside active work on persistent knowledge, agent memory,
context infrastructure, second brains, and portable assistant state. This page
does not claim those ideas are new. It identifies the narrower contract this
repository is trying to make testable.

Descriptions were checked against primary project sources on **2026-08-20**.
Capabilities and positioning can change; follow each linked project for current
details.

## Comparison dimensions

The projects below are not interchangeable products. This compact view compares
their stated design centers, not every capability.

| Project | Primary artifact or runtime | Stated design center | Boundary with `src_you` |
|---|---|---|---|
| [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Compiled wiki plus raw sources | Incrementally maintained, interlinked knowledge | `src_you` specifies who owns current personal state when sources conflict |
| [Open Second Brain](https://github.com/itechmeat/open-second-brain) | Obsidian-native Markdown memory with tools | User-owned, inspectable agent memory and maintenance | `src_you` is storage-neutral and makes global/project ownership normative |
| [OpenViking](https://github.com/volcengine/OpenViking) | Context database / service | Hierarchical resources, memories, skills, and on-demand context | `src_you` supplies governance semantics, not a retrieval database |
| [ai-memory](https://github.com/akitaonrails/ai-memory) | Coding-agent memory runtime | Markdown source of truth, derived index, handoffs, supersession, checkpoints | Close operational overlap; `src_you` is a broader, non-runtime reference contract |
| [Second Brain on Cloudflare](https://github.com/rahilp/second-brain-cloudflare) | Self-hosted shared memory service | Cross-client memory access, lifecycle, import/export, and search | `src_you` does not prescribe a service, account, or vector store |
| [Soul Protocol](https://github.com/luishg/soul-protocol) | Portable human-readable specification | Assistant identity, memory, and context across providers | `src_you` governs state about the user and their work, not a simulated assistant identity |
| [Mem0](https://github.com/mem0ai/mem0) | Agent-memory platform and APIs | Extracting and serving long-term memory to AI applications | `src_you` defines authority, scope, and recovery independently of memory extraction |
| [Letta](https://github.com/letta-ai/letta) | Stateful-agent platform | Agents that manage persistent memory and context | `src_you` is not an agent runtime and does not require self-editing agent memory |

## Where the overlap is real

### Maintained knowledge and user-owned files

LLM Wiki and Open Second Brain both value state that can be inspected and
maintained instead of reconstructed from an opaque conversation history.
`src_you` shares that preference. Its additional concern is lifecycle: which
record is `current`, which is `superseded`, and which source is authorized to
change the value.

### Context routing and minimal retrieval

OpenViking and memory platforms such as Mem0 address how useful context is
organized and delivered. `src_you` complements those mechanisms with a routing
constraint: choose the relevant scope before retrieval, then load the minimum
canonical state needed for the task. Similarity or recency alone does not make
a record authoritative.

### Cross-agent continuity and recovery

ai-memory has the closest visible operational overlap: a Markdown source of
truth, derived index, project routing, supersession, handoffs, checkpoints, and
restore. `src_you` should not obscure that overlap. The present distinction is
scope and form: ai-memory is an executable tool centered on coding agents;
`src_you` is a platform-neutral policy, template, prompt, and acceptance-test
contract intended to cover personal and project domains without requiring a
particular runtime.

### Shared services and stateful agents

Second Brain on Cloudflare, Mem0, and Letta provide software that stores or
serves memory. A private implementation could use one of those classes of
systems as a backing capability. Conformance would still require one canonical
owner per item and scope, explicit supersession, L1/L2 separation, minimal
retrieval, and controlled recovery. The presence of an API, vector index, or
persistent agent does not prove those properties.

### Portable assistant identity

Soul Protocol addresses portability of an assistant's identity and context.
`src_you` deliberately centers the human's durable state, commitments,
preferences, decisions, and project boundaries. A future integration could map
between the two, but neither should silently become the other's authority.

## The narrow wedge

The combination emphasized by `src_you` is:

```text
canonical personal state
+ explicit supersession
+ global/project ownership boundary
+ minimal retrieval
+ scope-aware source priority
+ replaceable platform adapters
+ downstream, recoverable backups
+ executable behavioral acceptance contract
```

The wedge is therefore not “AI can remember” or “Markdown can be a database.”
It is a compact governance contract for deciding which maintained personal
state wins, where it belongs, how an old value stops being active, and how the
same semantics survive a change of platform or storage.

## What would falsify the differentiation

The distinction is only useful if independent implementations can preserve the
contract. Evidence that would weaken or disprove the current wedge includes:

- adopters cannot apply L1/L2 ownership without duplicating state;
- adapters require provider-specific semantics in the core;
- two different stores cannot pass the same fourteen behavioral scenarios;
- a simpler established project already provides the same platform-neutral
  contract, evidence model, and non-coding scope;
- implementation reports show that supersession or recovery rules create more
  ambiguity than they remove.

That is why the next milestone is de-identified implementation evidence, not a
larger feature list. See the [roadmap](roadmap.md) and
[implementation report guide](implementation-reports.md).
