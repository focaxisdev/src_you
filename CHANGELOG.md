# Changelog

All notable changes to `src_you` are documented here. The project follows
[Semantic Versioning](https://semver.org/) for public releases.

## Unreleased

### Added

- Operational contract with acceptance criteria for same-source guarded updates,
  concurrent-edit reconciliation, exact readback, unknown outcomes, and separate
  delivery, persistence, and checkpoint evidence.
- Standard-library reference helpers and synthetic fault-injection tests for
  version conflicts, uncertain writes, identity and type-strict readback,
  capability evidence, and source reuse boundaries.

### Changed

- Retrieval, update, conflict, backup, and reference-adapter guidance now link
  the operational contract while retaining existing layer semantics and all
  fourteen acceptance scenarios. External capability-check dates are unchanged.

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
