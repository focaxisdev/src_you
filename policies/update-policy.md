# Update policy

Status: normative for `src_you` v0.1.0.

## Objective

Keep canonical state current without turning every conversation into permanent
data or creating duplicate active claims.

## Durability gate

Persist only confirmed information with cross-session value, such as a durable
goal, preference, constraint, decision, commitment, deadline, major milestone,
high-level project status, cross-project relationship, or true unresolved open
loop.

Do not persist solely because information is recent, detailed, emotional, or
mentioned more than once. Exclude transient steps, casual queries, unconfirmed
guesses, and session-only instructions.

## Required procedure

1. Confirm the information or keep it as a labeled Inference.
2. Classify it as Fact, Decision, Preference, Inference, or Open Loop.
3. Determine whether L1 or L2 owns the claim.
4. Search for the existing stable ID and active record.
5. Update in place when the meaning changes.
6. Mark the previous value `superseded` with an effective date and evidence.
7. Ensure only one value remains `current` for the record and scope.
8. Repair indexes, high-level summaries, and pointers.
9. Run project-boundary, conflict, and sensitive-data checks.
10. Create a checkpoint only if the durable change is meaningful enough to
    justify a restore point.

## Explicit user changes

An explicit current instruction applies immediately. If language or context
shows a durable change (“from now on,” “I decided,” “this deadline changed”),
update the canonical state during the same work session when possible. Do not
leave the change only in chat.

## Inference promotion

Inference becomes Fact, Decision, or Preference only after supporting evidence
or explicit confirmation. Record the promotion and preserve provenance.

## External observations

When an external current fact supports a durable decision, store the decision
and its criteria. If the observation must also be stored, include `observed_at`,
source, and a revalidation condition. Never imply indefinite validity.

## Prohibited behavior

- creating a new active record every time wording changes;
- leaving old and new values active together;
- copying L2 micro-state into L1 during every project update;
- storing secrets or raw sensitive documents;
- treating model confidence as user confirmation;
- checkpointing every conversational turn.

Tests 3, 4, 6, 7, 11, 12, and 13 cover this policy.
