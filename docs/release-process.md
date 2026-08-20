# Release process

Releases describe a reviewed state of the public framework. They never package
or link a maintainer's private L1/L2 state, checkpoints, exports, or locators.

## Version policy

`src_you` follows [Semantic Versioning](https://semver.org/):

- patch: documentation, tests, CI, adapters, and compatible tooling fixes;
- minor: additive policy or template capabilities that preserve established
  invariants and migration paths;
- major: incompatible changes to authority, ownership, lifecycle, routing, or
  recovery semantics.

An adapter observation changing because a provider renamed a feature is usually
a patch. A new normative state type or ownership rule requires design review
before a version is chosen.

## Maintainer checklist

1. Confirm the release scope and migration impact in the changelog.
2. Run `python scripts/run_checks.py` with a supported Python version.
3. Run `git diff --check` and review the entire diff and public Git history for
   personal data, credentials, private object IDs, and private locators.
4. Confirm that every example and fixture is synthetic or de-identified.
5. Confirm Tests 1–14 remain mapped and review behavioral evidence affected by
   the change.
6. Open a focused pull request and require all Linux/Windows CI matrix jobs to
   pass.
7. Merge without rewriting public history unless incident response requires it.
8. Tag the merge commit as `vMAJOR.MINOR.PATCH` and create release notes from
   the corresponding changelog entry.
9. Verify the tag and release resolve to the intended commit and assets.
10. Re-run the public privacy check against the released tree before promotion.

For an exported historical tree, the same scanner can be reused with
`python scripts/scan_sensitive_placeholders.py --root PATH`. Scan only a known
public export; never point the public-framework scanner at private L1/L2 state.

Do not tag from an unreviewed working tree. Do not publish a release merely to
make the README version claim true; the repository, tag, changelog, and release
notes must agree.

## Release notes structure

Keep notes factual and short:

- **Why:** the user or maintainer problem addressed;
- **Added / changed:** observable repository behavior;
- **Compatibility:** whether the core contract or private data layout changes;
- **Validation:** local checks and CI matrix result;
- **Privacy:** whether any private-state migration is required;
- **Upgrade:** the smallest safe action for existing adopters.

## Failed-release response

If a tag points to the wrong commit and no one has consumed it, remove it using
the hosting platform's documented controls and recreate it deliberately. If it
may have been consumed, do not silently reuse the version: document the error
and publish the next patch. For any possible privacy exposure, stop promotion,
follow [`SECURITY.md`](../SECURITY.md), rotate exposed credentials, and treat
history cleanup as incident response rather than routine Git hygiene.
