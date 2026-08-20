# Related work and differentiation

`src_you` sits beside a growing ecosystem of persistent knowledge, memory, and
portable context systems. This page avoids originality claims and explains the
different design centers as observed on 2026-08-20. Capabilities can change;
follow each project for current details.

## Adjacent approaches

### Karpathy's LLM Wiki

[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
proposes that an LLM incrementally compile raw sources into a persistent,
structured, interlinked wiki instead of reconstructing knowledge from raw RAG
chunks on every question.

**Adjacency:** maintained knowledge representation and agent-driven curation.

**`src_you` focus:** governance of current personal state, including canonical
ownership, supersession, global/project boundaries, and recovery semantics.

### Open Second Brain

[Open Second Brain](https://github.com/itechmeat/open-second-brain) is an
Obsidian-native memory layer with Markdown records, auditability, and agent
integrations.

**Adjacency:** user-owned files, memory maintenance, deterministic tools, and
versionable state.

**`src_you` focus:** storage-neutral policies; Obsidian is one possible backing
store rather than the product definition.

### OpenViking

[OpenViking](https://github.com/volcengine/OpenViking) is a context database that
organizes agent memories, resources, and skills in a virtual filesystem with
tiered, on-demand loading and observable retrieval.

**Adjacency:** hierarchical context, minimal loading, and traceable retrieval.

**`src_you` focus:** personal-state authority and lifecycle. It does not provide
a database, embedding pipeline, or retrieval server.

### ai-memory

[ai-memory](https://github.com/akitaonrails/ai-memory) provides long-term memory
and handoff between coding-agent clients, with project routing, checkpoints, and
restore mechanisms.

**Adjacency:** cross-vendor portability, project separation, recovery, and
maintained memory.

**`src_you` focus:** a non-runtime reference contract that can also govern
non-coding personal domains and distinguish global durable state from project
micro-state.

### Second Brain on Cloudflare

[Second Brain on Cloudflare](https://github.com/rahilp/second-brain-cloudflare)
offers one self-hosted memory service to multiple AI clients, including current
and superseded memory behavior.

**Adjacency:** one shared source, user control, cross-client access, and memory
lifecycle.

**`src_you` focus:** an architecture and policy toolkit rather than a hosted or
self-hosted application. It can inform deployments on many storage backends.

### Soul Protocol

[Soul Protocol](https://github.com/luishg/soul-protocol) defines a portable,
human-readable structure for assistant identity, memory, and context across
models and providers.

**Adjacency:** portability, human-readable files, and separation from a single
provider.

**`src_you` focus:** state about the person using AI, not a portable simulated
assistant identity or “soul.”

## Design center

The combination emphasized by `src_you` is:

```text
canonical personal state
+ explicit supersession
+ global/project ownership boundary
+ minimal retrieval
+ scope-aware source priority
+ replaceable platform adapters
+ downstream, recoverable backups
```

These ideas overlap with adjacent projects in useful ways. The contribution is
the compact governance contract and operational prompt/template set, not a
claim that persistent memory or Markdown knowledge systems are new.
