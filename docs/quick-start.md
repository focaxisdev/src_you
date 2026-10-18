# Quick start: build and check your ChatGPT memory structure

The main path is to let ChatGPT read the public setup instructions and help you
establish private, maintained state. You do not need to run Python for this path.
The scripts later on this page are optional ways to inspect the reference locally.

## 1. Give ChatGPT the setup instructions

Open [prompts/bootstrap.md](../prompts/bootstrap.md), fill its configuration, and
paste everything under **Prompt** into a new ChatGPT conversation. Select the
ChatGPT adapter; use the prompt's auto-detect/unknown options when you do not yet
know the store or existing systems. Leave backup unset if no destination is ready.
Do not paste credentials or another person's private data.

Provide the repository URL and ask ChatGPT to read these public sources:

- the [bootstrap prompt](../prompts/bootstrap.md), which describes setup phases;
- the [private-state templates](../templates/src_you/), starting at the manifest;
- the [ChatGPT adapter](../adapters/chatgpt/), including its capability checklist
  and runtime instructions;
- the linked policies and operational requirements relevant to your setup.

If ChatGPT cannot open links, supply the needed public files by the available
file/text mechanism. Ask it to identify anything it could not read rather than
pretend it loaded the instructions. Sharing these files supplies guidance; it
does not install a background service or change account settings.

## 2. Choose a private store and establish the structure

The bootstrap first checks for an existing system to adopt. If you already have
one, use the [existing-system audit](../prompts/audit-existing-system.md) to avoid
creating a competing source. Only inspect or change private sources you authorize.

Ask ChatGPT to explain which tools can read, create, update, and read back records
in the chosen store. An available Library, Project, or connected source must be
checked for those operations in your actual session; its name alone proves none
of them. Missing write access may leave a useful draft, but not a saved system.

The expected result is a private manifest naming the authoritative store and
writer, useful modules for durable personal state, and pointers to detailed
project state. In the framework these are L0 (instructions), L1 (global state),
and L2 (project detail). Keep only modules with a purpose. This recreates the
public architecture, not any author's private account, records, or permissions.

Have ChatGPT report the created/adopted locations, verification evidence, and
blocked operations. Keep the actual records outside the public repository.

## 3. Verify each capability separately

Start with a clearly labeled synthetic test record, not personal information:
“Demo preference: focused meetings in the afternoon.” Then change it to morning.
Ask ChatGPT to read the saved record back: morning should be the single current
value, with afternoon retained as superseded history under the same record ID.

| Outcome | Evidence to request |
|---|---|
| Structure generated | Inspect the manifest, module roles, and project pointers; a draft is sufficient for this stage only. |
| State saved and updated | Actual same-target readback shows the intended value and history; generated text or a download alone is insufficient. Guarded updates require the adapter's verified protection. |
| New-conversation access | In a new conversation, provide the installed entry instructions/manifest locator and verify it reads morning from the store, not from a pasted answer. Test an authorized synthetic update and readback there too. |
| Scheduled/background work | Only if supported and wanted: verify an actual fresh-context run, storage access, persistence, and notification separately. Schedule creation alone proves no later success. |

Use the [runtime instructions](../adapters/chatgpt/runtime-instructions.md) in an
instruction location your surface supports, with the private manifest locator.
Reading this repository once does not guarantee those instructions or files will
be available in every future conversation. Report unavailable operations as
BLOCKED or NOT_RUN rather than claiming reliable long-term memory.

These checks reduce reliance on reconstructing current state from chat history;
they do not remove the need for task context or relevant retrieval. Before real
use, review [privacy](privacy-and-security.md), the
[behavioral acceptance scenarios](../tests/acceptance-tests.md), and, if offering
unattended work, the [execution reliability contract](execution-reliability.md).
The public tests do not certify your account's capabilities.

## Optional local route: demo, checks, and scaffold

This route is for inspecting the synthetic implementation or preparing template
files locally. It does not connect them to ChatGPT. None of these commands starts
an agent, background worker, sync service, or scheduled task.

### Local prerequisites

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

### A. Run the synthetic example

Start in a parent folder where you want the public checkout:

```bash
git clone https://github.com/focaxisdev/src_you.git
cd src_you
python --version
```

After confirming Python 3.10 or newer, run from the same checkout root:

```bash
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

### B. Verify the public reference

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

### C. Choose whether to create a scaffold

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

No destination is created by this preview. If you want the unfilled scaffold,
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

### Safe refusals and common setup problems

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

### D. Configure and verify your actual integration

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
