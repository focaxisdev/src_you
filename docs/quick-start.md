# Five-minute quick start

This path proves the framework locally and creates a private-state scaffold
without putting personal data in the public repository.

## Before you begin

You need Python 3.10 or newer. Git is useful but optional when you download a
source archive. The validation tools use only the Python standard library and
do not upload data.

Choose a destination that is:

- outside the public `src_you` checkout;
- private and under your control;
- readable and writable by only the people and tools you authorize;
- backed up downstream only after you have reviewed its contents.

Do not put a secret, provider object ID, or sensitive person name in the folder
name or shell command.

## 1. Get and validate the framework

```bash
git clone https://github.com/focaxisdev/src_you.git
cd src_you
python scripts/run_checks.py
```

If `python` is not the Python 3 command on your system, use `python3` on many
Unix-like systems or `py -3` on Windows.

A passing repository check validates the public framework, links, encodings,
synthetic fixtures, bootstrap safety, and checkpoint tooling. It does not prove
that a future private implementation passes the behavioral acceptance tests.

## 2. Preview the private scaffold

The example below chooses a sibling directory, not a directory inside the
public checkout:

```bash
python scripts/bootstrap_private_state.py ../src_you-private --dry-run
```

The command refuses destinations inside the public framework repository and
refuses to overwrite a non-empty destination.

## 3. Create the private scaffold

```bash
python scripts/bootstrap_private_state.py ../src_you-private
```

This copies the unfilled template only. It does not ingest chats, memories,
documents, accounts, or existing vaults.

If you already have a maintained state system, stop here and use
[`../prompts/audit-existing-system.md`](../prompts/audit-existing-system.md).
The correct next step may be to adopt that system, not create another one.

## 4. Designate authority

Open `../src_you-private/00_SYSTEM_MANIFEST.md` and fill only the minimum fields
needed to establish:

1. the private authoritative L1 store;
2. its single active writer;
3. the effective date of that authority;
4. the selected adapter;
5. downstream-only backup behavior.

Then review `registry/projects.md`. For each L2 project, keep a stable logical
pointer and a high-level L1 summary. Do not copy its exact next step, question,
code cell, session handoff, or other micro-state into L1.

Remove unused sample rows or modules rather than filling files for appearance.
Start with one confirmed, non-sensitive durable record. Keep every unconfirmed
model conclusion typed as `Inference`.

## 5. Connect an adapter and test behavior

Choose a reference mapping:

- [`../adapters/chatgpt/`](../adapters/chatgpt/) for ChatGPT capabilities;
- [`../adapters/codex/`](../adapters/codex/) for local Codex project and
  instruction capabilities.

Run the fourteen scenarios in
[`../tests/acceptance-tests.md`](../tests/acceptance-tests.md) against your
implementation. Record paths, scopes, lifecycle states, and pass/fail results
without copying personal values into a public issue.

The implementation is not conforming merely because the public repository
checks pass. Conformance requires behavioral evidence that routing,
supersession, conflicts, privacy, recovery, inference handling, and portability
work in the chosen environment.

## Privacy stop conditions

Stop before sharing, committing, or backing up the private tree if you find:

- credentials, tokens, cookies, private keys, one-time codes, or payment data;
- raw health, family, legal, employment, or financial documents when a minimal
  summary or protected pointer would suffice;
- public and private state in the same Git history;
- more than one active writer for the same state item and scope;
- a backup or cache being treated as canonical because it is newer.

Read [`privacy-and-security.md`](privacy-and-security.md) before migrating real
state.
