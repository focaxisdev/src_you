# Acceptance tests

These behavior-level tests define the minimum `src_you` v0.1 conformance
contract. Run them against an implementation after bootstrap, normalization,
adapter changes, upgrade, or restore. Record evidence without exposing private
state contents.

## Test 1 — High-level routing

**Prompt:** “What is my learning currently focused on overall?”

**Expected:** Read the L1 learning summary and major milestones. Do not load the
exact lesson, question, or code-step state unless the high-level record is
insufficient for a stated reason.

**Pass evidence:** Retrieved paths/scopes and a high-level answer.

## Test 2 — Detailed project routing

**Prompt:** “Continue the previous Python step.”

**Expected:** Read the L1 project pointer, then route to the L2 project canonical
state. Do not infer the step from global state or old chat history.

**Pass evidence:** Resolved logical pointer and current L2 state version.

## Test 3 — Micro-state exclusion

**Setup:** L2 contains an exact question, code cell, lesson step, and session
action.

**Expected:** L1 contains none of those fields. It may contain status, major
phase, milestone, deadline, blocker, and L2 pointer.

**Pass evidence:** Field inventory for L1 and L2.

## Test 4 — Durable update

**Setup:** Stable preference record says A is current. The user explicitly
changes the durable preference to B.

**Expected:** The same stable ID has B current; A is superseded history. No
second active record exists.

**Pass evidence:** Lifecycle and uniqueness check.

## Test 5 — Memory conflict

**Setup:** Cached Memory contains old value A; canonical state contains current
value B.

**Expected:** Use B. Identify Memory as stale cache; never overwrite B from
Memory.

**Pass evidence:** Answer and conflict trace.

## Test 6 — Explicit user update

**Setup:** Current explicit instruction conflicts with canonical durable state.

**Expected:** Follow the explicit instruction for the current turn. If the change
is durable, update canonical state and supersede the old value. If transience is
clear, do not persist it.

**Pass evidence:** Immediate behavior plus durability decision.

## Test 7 — Sensitive data

**Setup:** Input contains a placeholder representing a secret, a raw confidential
file, and a useful non-secret durable summary.

**Expected:** Exclude secret and unnecessary raw file. Persist only the minimum
safe summary or protected pointer when justified. Never echo the secret.

**Pass evidence:** Redacted handling report and stored-field inventory.

## Test 8 — Backup integrity

**Setup:** Create a checkpoint from a known fixture set.

**Expected:** Manifest contains sorted paths, sizes, SHA-256 hashes, schema,
timestamp, scope, label, exclusions, and verification. Recalculation matches.

**Pass evidence:** Successful manifest verification.

## Test 9 — Restore safety

**Setup:** A downstream backup is newer than the authoritative source but no
restore has been declared.

**Expected:** No overwrite or merge occurs. Request an explicit recovery intent
and complete integrity, privacy, comparison, staging, and cutover steps.

**Pass evidence:** Blocked automatic restore and generated recovery plan.

## Test 10 — Minimal retrieval

**Setup:** Several unrelated domains exist, including a sensitive domain.

**Prompt:** Ask a question that requires only one non-sensitive domain.

**Expected:** Retrieve the manifest/router and that domain only. Do not load the
unrelated or sensitive domains.

**Pass evidence:** Retrieval trace with rationale.

## Test 11 — External fact staleness

**Setup:** State includes a dated observation about a price, policy, public role,
job, or software version.

**Expected:** Treat it as an observation with date/source and reverify before a
current answer. Do not present it as indefinitely true.

**Pass evidence:** Freshness check and current source or explicit uncertainty.

## Test 12 — Project boundary

**Setup:** Update an L2 project's exact next step and session handoff.

**Expected:** L2 changes. L1 does not copy the new micro-state. L1 changes only
if status, major phase, milestone, deadline, dependency, decision, or blocker
changed.

**Pass evidence:** Before/after scoped diff.

## Release gate

An implementation passes v0.1 conformance when all twelve tests pass, no
unresolved authority conflict exists, pointers resolve, sensitive-data review
passes, and checkpoint/restore behavior is one-directional and explicit.
