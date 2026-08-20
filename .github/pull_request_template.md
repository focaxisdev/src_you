## Summary

Describe the focused change and the state-governance problem it addresses.

## Invariants

- [ ] One authoritative owner remains defined per active state item and scope.
- [ ] Memory and chat history remain non-authoritative.
- [ ] L1 does not duplicate L2 project micro-state.
- [ ] Current/superseded lifecycle remains unambiguous.
- [ ] Retrieval remains minimal and scope-aware.
- [ ] Backup remains downstream and restore explicit.
- [ ] Core architecture remains platform-neutral, or the change is isolated to an adapter.

## Privacy

- [ ] All examples and fixtures are fictional, synthetic, or fully de-identified.
- [ ] No secrets, personal data, private IDs, raw state exports, or private repository links are included.

## Validation

- [ ] `python scripts/validate_structure.py`
- [ ] `python scripts/check_internal_links.py`
- [ ] `python scripts/scan_sensitive_placeholders.py`
- [ ] `python scripts/checkpoint_manifest.py self-test`
- [ ] Relevant acceptance scenarios were reviewed or updated.
