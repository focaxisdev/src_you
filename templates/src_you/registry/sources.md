# Source registry

Record authority by logical scope, not by “newest file.” Keep provider-specific
locators private when they reveal sensitive identifiers.

| Logical scope | Role | Source | Writable | Authority effective from |
|---|---|---|---:|---|
| `src_you://global` | authoritative | `{{AUTHORITATIVE_STORE}}` | yes | `{{ISO_8601_DATE}}` |
| `backup://primary` | downstream backup | `{{PRIVATE_BACKUP_STORE}}` | checkpoint only | not applicable |

Memory, chat history, and search indexes may be listed as `cache`, never as
authoritative sources.
