# Quick start: run, verify, then choose a store

Start with synthetic data. The first two steps run the public demo and checks;
creating a scaffold is optional. None of these commands starts an agent,
background worker, sync service, or scheduled task.

## Before you begin

You need Git for the clone commands and Python 3.10 or newer. There are no
third-party Python dependencies, package installation steps, or API keys.
If your Python 3 command is `python3` (macOS/Linux) or `py -3` (Windows), use
that in place of `python` throughout. The command blocks work in a Unix shell
or Windows PowerShell; forward slashes in the relative paths work with Python
on both platforms. Quotes preserve paths containing spaces.

Cloning needs network access. The demo, checks, and scaffold commands run locally
without network calls. If you download a source archive instead, extract it and
open a terminal in the extracted repository root, where `README.md` and
`scripts/` are visible; skip the clone and `cd` commands.

## 1. Run the synthetic example

Start in a parent folder where you want the public checkout:

```bash
git clone https://github.com/focaxisdev/src_you.git
cd src_you
python --version
python scripts/demo_memory_conflict.py
```

Check that `python --version` reports 3.10 or newer before running the demo.
**Stay in this `src_you` root for every remaining command.** If you already
have this checkout, open its root rather than cloning into it again.

Expected output includes this excerpt:

```text
Canonical now:    Prefer focused meetings in the morning.
Cached Memory:    Prefer focused meetings in the afternoon. (unchanged; not authoritative)
Selected value:   Prefer focused meetings in the morning.
```

Later, the output ends with:

```text
Negative case (two current records): REJECTED: expected exactly one current canonical record.
Temporary state removed; repository inputs were not modified.
```

The trace includes additional lines. `REJECTED` is intentional; the complete
command exits with code 0. A prepared update replaces afternoon with morning,
saves temporary JSON, and reloads it. Cached Memory remains afternoon. This is
a deterministic state example, not an AI performance comparison or a live
adapter test. See the [full walkthrough](../examples/memory-conflict-demo/README.md).

## 2. Verify the public reference

From the same checkout root:

```bash
python scripts/run_checks.py
```

Expect several validation messages and unittest summaries, ending with:

```text
All repository checks passed: 12 gates.
```

The gates include 105 unit tests plus structure, links, encoding, privacy-pattern,
fixture, scaffold, and checkpoint checks. Success does not certify a private
store or prove that an agent follows the policies. You can stop here after
exploring the example without creating any persistent personal-state files.

## 3. Choose whether to create a scaffold

**Already have a maintained store?** Use the
[existing-system audit](../prompts/audit-existing-system.md) before creating
anything else. You may be able to adopt that store without a second authority.

For a new setup, choose an empty or absent destination outside the public
checkout. The example below uses a sibling folder named `src_you-private`.
Use a location under your control; do not put sensitive names or identifiers
in shell commands. The bootstrap copies templates but does not configure OS
permissions or encryption. Review access controls before adding real data.

Preview from the checkout root:

```bash
python scripts/bootstrap_private_state.py "../src_you-private" --dry-run
```

Expected output (the absolute path varies by machine):

```text
Dry run: would create <absolute destination> with 14 scaffold files.
No personal data or template values were written.
```

No destination is created by this preview. If you want the empty scaffold,
run from the same directory:

```bash
python scripts/bootstrap_private_state.py "../src_you-private"
```

Expected output:

```text
Created <absolute destination> with 14 scaffold files.
Next: keep the location private and edit 00_SYSTEM_MANIFEST.md first.
Do not commit this private state into the public framework repository.
```

Check the result without filling any private values:

```bash
python -c "from pathlib import Path; p = Path('../src_you-private'); print('Manifest exists:', (p / '00_SYSTEM_MANIFEST.md').is_file()); print('Scaffold files:', sum(f.is_file() for f in p.rglob('*')))"
```

Expected: `Manifest exists: True` and `Scaffold files: 14`. This is an unfilled
scaffold, not a configured assistant. It imports no chats, memories, accounts,
or existing vaults. If this was only a trial, you may remove the newly created
folder after confirming you have not added anything you need.

## Safe refusals and common setup problems

- Repeating creation on the populated destination exits with code 2 and prints
  `Bootstrap refused: destination already exists and is not an empty directory.`
  Inspect it or choose another empty destination; do not delete existing state
  to make the command succeed.
- A destination inside this checkout exits with code 2 and prints
  `Bootstrap refused: destination must be outside the public framework repository.`
- `can't open file` usually means the terminal is not in the checkout root.
- If Python is missing or older than 3.10, install a supported Python interpreter
  before continuing. `npm install` and `pip install` are not setup steps here.
- If a gate fails, retain its error and fix that issue before adopting the
  scaffold. A passing demo alone does not replace the full checks.

## 4. Configure and verify your actual integration

Open `../src_you-private/00_SYSTEM_MANIFEST.md` and identify the authoritative
private global store (L1), its single active writer, effective date, adapter,
and downstream-only backups. In `../src_you-private/registry/projects.md`,
register logical pointers to project state (L2). Detailed next steps and session
handoffs stay in the project; keep only the useful summary and pointer globally.

Remove unused sample rows. Start with one confirmed, non-sensitive durable
record, and keep unconfirmed model conclusions typed as `Inference`.

Choose the [ChatGPT](../adapters/chatgpt/) or [Codex](../adapters/codex/) reference
mapping and verify the capabilities in your own execution context. These are
instructions and mappings, not automatic installation or connection commands.
Run the [fourteen behavioral scenarios](../tests/acceptance-tests.md) against
that integration. Unattended work also needs the
[execution reliability checks](execution-reliability.md), including real
fresh-context evidence. Public unit tests cannot supply that evidence for you.

Keep real personal state out of public commits and reports. Read
[privacy and security](privacy-and-security.md) before adding it; backups are
recovery copies and never become authoritative just because they are newer.
