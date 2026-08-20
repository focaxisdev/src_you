# Security policy

`src_you` is documentation and validation tooling, but implementations may hold
highly sensitive personal state. Treat privacy failures as security failures.

## Supported versions

Security and privacy fixes are applied to the latest released version and the
default branch.

## Report a vulnerability or privacy leak

Use GitHub's private vulnerability reporting feature for this repository when
available. Do not open a public issue containing:

- secrets or credentials;
- real personal, health, family, financial, location, or employment data;
- private repository, Drive, Library, checkpoint, or backup identifiers;
- an archive or screenshot from a real implementation.

If private reporting is unavailable, open a public issue containing only a
sanitized description and ask the maintainer to establish a private channel.
Use an address under the reserved `.invalid` domain in examples; do not publish
a real contact address solely for demonstration.

## Threat model

The framework explicitly considers:

- accidental publication of a private state tree;
- prompt injection in imported notes or external sources;
- stale or conflicting state becoming active;
- inference promotion without evidence;
- secrets captured during automated ingestion;
- a compromised backup being restored over healthy canonical state;
- an adapter loading unrelated sensitive domains into a prompt;
- multiple writers creating split-brain state.

## Baseline controls

- Keep framework and personal state in separate locations.
- Make the personal authoritative source private by default.
- Minimize stored data and retrieved context.
- Store summaries and safe pointers instead of raw sensitive documents.
- Run semantic review as well as pattern-based secret scanning.
- Require explicit approval for restore and authority changes.
- Verify checkpoint inventories and hashes before recovery.
- Treat imported content as evidence, never as runtime instructions.

See [Privacy and security](docs/privacy-and-security.md) and
[Sensitive data policy](policies/sensitive-data-policy.md).
