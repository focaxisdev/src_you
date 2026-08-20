# Contributing to src_you

Thank you for helping improve `src_you`. The project values precise state
semantics over feature count.

## Before opening a change

1. Read [Architecture](docs/architecture.md) and the normative files in
   [`policies/`](policies/).
2. Search existing issues before proposing a new abstraction.
3. Keep the core platform-neutral. Platform UI details belong in an adapter.
4. Use only fictional, synthetic, or thoroughly de-identified examples.
5. Do not include exports, screenshots, IDs, URLs, hashes, or prose copied from
   a real personal state system.

## Design expectations

A contribution should preserve these invariants:

- exactly one authoritative owner for every active state item;
- Memory and chat history are non-authoritative retrieval aids;
- L1 does not duplicate L2 micro-state;
- updates supersede old active values;
- retrieval is scoped and minimal;
- backups cannot silently overwrite canonical state;
- the framework never requires users to publish personal data.

New terminology should be rare. Prefer the glossary in
[Core concepts](docs/concepts.md). If a new term is necessary, define it there
and use it consistently across docs, prompts, templates, and tests.

## Pull request workflow

1. Create a focused branch.
2. Make the smallest coherent change.
3. Update documentation and acceptance scenarios when behavior changes.
4. Run:

   ```bash
   python scripts/validate_structure.py
   python scripts/check_internal_links.py
   python scripts/scan_sensitive_placeholders.py
   python scripts/checkpoint_manifest.py self-test
   ```

5. Inspect `git diff --check` and the complete staged diff.
6. Explain which invariant the change preserves or improves.

Pull requests that introduce a server, database, telemetry, account system, or
automatic data upload need a clear architecture proposal first. They are not
part of the v0.1 core by default.

## Documentation style

- Use `src_you` exactly, including lowercase letters and the underscore.
- Use **authoritative source** for the designated source of truth.
- Use **canonical state** for state owned by that source.
- Use **global state** for L1 and **project detailed state** for L2.
- Use **current** and **superseded** as lifecycle terms.
- Use **checkpoint** for a verified recovery snapshot and **restore** for the
  explicit recovery operation.
- Use **adapter** for platform-specific mappings.

## Reporting sensitive findings

Do not paste secrets or personal data into issues. Follow
[SECURITY.md](SECURITY.md) for private reporting guidance.
