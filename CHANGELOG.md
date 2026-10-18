# Changelog

All notable changes to `src_you` are documented here. The project follows
[Semantic Versioning](https://semver.org/) for public releases.

## Unreleased

### Fixed

- Preserve unresolved persistence as BLOCKED after wrong-target or invalid-version
  readback, without weakening identity, version guards, or exact comparison.
- Validate checkpoint metadata before inventory verification; retain compatible
  format 0.1.0 manifests and distinguish integrity from restore authorization.

### Added

- Lightweight execution policy dependency/revision checks, explicit failure
  classifications, opt-in bounded safe-read recovery, and independent run-stage
  evidence. No scheduler, persistent job engine, or notification sender is added.
- Synthetic regressions for stale/missing entry policies, contradictory stop
  rules, partial continuation, prepared-update replay, and recovery boundaries.

### Changed

- Upgrade and adapter guidance now audits entrypoint policy drift and fresh
  execution capabilities; adopted framework policy versions are distinct from
  state schema and checkpoint format versions. No automatic migration occurs.

## 0.2.0 — 2026-10-18

This minor release adds compatible operational policy capabilities. The
L0/L1/L2 authority model and private-state layout remain unchanged; no data
migration is required.

### Added

- Operational contract with acceptance criteria for same-source guarded updates,
  concurrent-edit reconciliation, exact readback, unknown outcomes, and separate
  delivery, persistence, and checkpoint evidence.
- Standard-library reference helpers and synthetic fault-injection tests for
  version conflicts, uncertain writes, identity and type-strict readback,
  capability evidence, and source reuse boundaries.
- A deterministic synthetic memory-conflict walkthrough with captured output
  and regression tests, previously merged after v0.1.1.

### Changed

- Retrieval, update, conflict, backup, and reference-adapter guidance now link
  the operational contract while retaining existing layer semantics and all
  fourteen acceptance scenarios. External capability-check dates are unchanged.

### Validation and upgrade

- Ten repository gates cover 49 unit tests, fourteen mapped acceptance
  scenarios, and public-tree privacy checks. CI covers Linux and Windows on
  Python 3.10 and 3.14.
- Review the operational contract and independently verify each adapter's
  guarded-update and readback capabilities before enabling automated writes.
  Synthetic tests do not demonstrate provider support or model behavior.
- Examples remain fictional. Existing adopters need no private-state migration;
  periodic maintenance remains audit/catch-up, not a replacement for authorized
  same-session durable updates.

## 0.1.1 — 2026-08-20

### Added

- Safe, dependency-free private-state scaffold bootstrap with overwrite and
  public-repository isolation guards.
- Codex reference adapter and an adapter contribution contract.
- Five-minute quick start, implementation report path, evidence-driven roadmap,
  and release process.
- Two behavioral scenarios for Inference integrity and platform portability,
  bringing the acceptance contract to fourteen scenarios.
- Machine-readable acceptance fixtures, strict UTF-8 validation, and one
  aggregate local/CI check command.
- A metadata-free 1280×640 social preview and dependency-free asset validator.

### Changed

- CI now runs every repository gate on Linux and Windows with Python 3.10 and
  3.14.
- ChatGPT capability mappings now use capability descriptions instead of
  depending on a specific product UI label.
- README positioning, onboarding, privacy boundaries, and related-work
  differentiation are more explicit.

## 0.1.0 — 2026-08-20

### Added

- Initial public three-layer architecture for durable personal state.
- Normative retrieval, update, project-boundary, conflict, sensitive-data, and
  backup policies.
- Bootstrap, audit, normalize, checkpoint, restore, and upgrade prompts.
- A capability-aware ChatGPT reference adapter.
- Fictional career and learning examples.
- Twelve acceptance scenarios and standard-library validation scripts.
