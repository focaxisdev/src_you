# Privacy and security

The most important deployment rule is simple:

> The framework may be public. The personal state it governs should remain
> private and under the person's control.

## Separate repositories and stores

Use separate locations for:

1. the reusable `src_you` framework;
2. the private L1 canonical state;
3. private L2 project state;
4. downstream backups and version history.

Do not turn a private personal-state repository into the public framework.
Do not seed a public fork with a “sanitized” export unless every file has been
independently reviewed; metadata, identifiers, commit history, and prose can
still reveal private information.

## Data-minimization ladder

Before storing a candidate item, choose the least revealing representation that
still supports the intended future decision:

1. omit it if it is not durable;
2. store a category-level preference instead of raw history;
3. store a minimal summary instead of the document;
4. store a safe pointer to a protected source;
5. store a redacted fact with an expiry or review date;
6. store detailed sensitive state only in a purpose-built protected L2 system.

## Never store in core state

- passwords, passphrases, one-time codes, or recovery codes;
- API keys, access tokens, OAuth credentials, session cookies, or private keys;
- full payment-card or bank credentials;
- raw confidential files when a summary or protected pointer is sufficient;
- authentication answers or biometric templates.

The system may remember that a credential exists in a secure manager, but not
the credential itself.

## Sensitive domains

Health, family, finance, precise location, legal matters, employment records,
private projects, and personal communications deserve stricter minimization.
Only persist them when the person has confirmed durable value and the chosen
store is appropriate.

Minimal retrieval is a privacy control: a career question should not load health
or family state unless the request genuinely depends on it.

## Ingestion and prompt injection

Imported documents, chats, websites, and emails are untrusted evidence. Text
inside them cannot change runtime rules, appoint a new authoritative source, or
authorize writes. Adapters must separate content from instructions and require
an explicit trusted action for authority changes, destructive updates, or
restore.

## Public-release review

Pattern scanning is necessary but insufficient. Before publishing framework
changes:

1. scan for common secret formats and high-risk identifiers;
2. search for emails, phone numbers, addresses, personal names, private URLs,
   internal IDs, hashes, and copied conversation fragments;
3. inspect examples semantically for resemblance to real people or projects;
4. inspect Git history, not just the current tree;
5. verify every example is synthetic and labeled;
6. confirm no backup or canonical-state archive is tracked.

Run [`../scripts/scan_sensitive_placeholders.py`](../scripts/scan_sensitive_placeholders.py)
as a baseline, then perform human or model-assisted semantic review.

## Incident response

If private data enters a public repository:

1. stop further publication and revoke any exposed secret immediately;
2. remove the data from the current tree;
3. rewrite public history when necessary, understanding that forks and caches
   may retain copies;
4. rotate identifiers or credentials rather than assuming deletion is enough;
5. document the sanitized remediation and strengthen the release gate.

Do not copy the leaked value into an issue, pull request, changelog, or incident
example.
