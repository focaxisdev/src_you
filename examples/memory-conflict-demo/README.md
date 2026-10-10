# A memory conflict in 60–90 seconds

All inputs are synthetic. Python 3.10+ and its standard library are enough.
No account, model, API key, package install, network, or private state is needed.

This executable example adapts the existing
[meeting-preference supersession example](../conflict-resolution-example.md).
Both versions refer to **focused meetings**, so the update does not silently
change the preference's scope.

## Run it

From the repository root:

```bash
python scripts/demo_memory_conflict.py
```

The script reads [input.json](input.json), applies a hand-prepared structured
update, writes the resulting canonical record to a temporary JSON file, and
reloads that file before selecting the current value. The temporary directory
is removed on exit. It never modifies the repository input or real user state.
The full [output.txt](output.txt) was captured from that command, not written as
an imagined model response. Tests compare it with a fresh process run.

## Walkthrough

1. **0–20 seconds: inspect the input.** The canonical value and cached Memory
   both say afternoon. The fictional user's instruction changes focused
   meetings to morning. `prepared_update` explicitly supplies the ID, scope,
   normalized statement, date, and confirmation/durability/authorization flags.
   These fields were written by the example author, not extracted by an LLM.
2. **20–45 seconds: run the command.** Read the `Canonical now`, `Cached Memory`,
   and `Selected value` lines. The JSON round-trip retains morning while cached
   Memory is unchanged. Selection reads the canonical record; the cache is
   shown for comparison and has no authority in this code path.
3. **45–65 seconds: inspect the trace.** `PREF-MEETINGS-001` stays stable. The
   afternoon value is nested under `supersedes` with status `superseded`; morning
   is the only current value for that ID and scope. The date and synthetic
   evidence are retained. This is a local filesystem round-trip, not a live
   cross-session adapter or a sync demonstration.
4. **65–90 seconds: inspect the failure.** The script deliberately introduces a
   second current record. It prints `REJECTED` instead of picking one. This is
   an expected negative case, so the complete demonstration exits successfully.
   A real adapter would need to surface an Open Loop and ask for clarification;
   this demo does not implement that conversation.

## What was tested

```bash
python -m unittest discover -s tests -p test_memory_conflict_demo.py -v
python scripts/run_checks.py
```

The focused tests check stable identity and scope, one current value,
supersession and multi-change history, non-mutation of inputs, a repeated update,
missing/ambiguous state rejection, wrong ID/scope rejection, required update
flags, unrelated scope preservation, disk reload with stale Memory, and exact
CLI output from another working directory. The repository's aggregate command
runs these tests alongside its existing gates.

## Limits: executable policy example, not an AI benchmark

- **No LLM was run.** The output is deterministic Python text. It does not show
  an AI failing before governance or succeeding afterward; no such baseline or
  improvement has been measured.
- **The trust decisions are supplied.** The fixture designates the canonical
  input and declares the update confirmed, durable, and authorized. Boolean
  flags are not a security or consent mechanism. The demo does not verify a
  real instruction's author or infer intent, durability, scope, or record IDs.
- **The implementation is deliberately narrow.** It is not a full input schema
  validator and does not handle arbitrary malformed records, stale/out-of-order
  changes, conflicting writers, transactions, cache repair, checkpoints, or
  production privacy controls. Do not use it to process real personal state.
- **Repository tests and model conformance differ.** Existing acceptance-fixture
  checks validate declarations. These new tests execute the demo's functions;
  neither establishes behavior of a live ChatGPT/Codex adapter. Test real
  integrations using [behavioral acceptance scenarios](../../tests/acceptance-tests.md)
  and [de-identified implementation reports](../../docs/implementation-reports.md).

The relevant contracts are the
[update policy](../../policies/update-policy.md) and
[conflict-resolution policy](../../policies/conflict-resolution-policy.md).
