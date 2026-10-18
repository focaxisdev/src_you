"""Pure execution-policy checks; no scheduler, network calls, or job storage."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

from operational_contract import Evidence


class Failure(str, Enum):
    TRANSIENT_READ = "transient_read"
    PERMISSION_DENIED = "permission_denied"
    INVALID_CONTENT = "invalid_content"
    VERSION_CONFLICT = "version_conflict"
    UNKNOWN_WRITE = "unknown_write"


class Recovery(str, Enum):
    RETRY_READ = "retry_read"
    STOP = "stop_dependent_operation"
    REFRESH_MERGE = "refresh_and_guarded_merge"
    READBACK = "reconcile_write_by_readback"


def recovery_action(failure: Failure, *, attempts: int, limit: int) -> Recovery:
    """Classify a failed attempt; never grants permission or retries a write.

    An unknown write needs reconciliation even after its mutation budget ends.
    Actual time limits/backoff and provider error mapping belong to the adapter.
    """
    if (type(attempts) is not int or type(limit) is not int or
            attempts < 1 or limit < 1):
        raise ValueError("positive integer attempt counts required")
    if not isinstance(failure, Failure):
        raise ValueError("explicit failure classification required")
    if failure is Failure.UNKNOWN_WRITE:
        return Recovery.READBACK
    if attempts >= limit:
        return Recovery.STOP
    if failure is Failure.TRANSIENT_READ:
        return Recovery.RETRY_READ
    if failure is Failure.VERSION_CONFLICT:
        return Recovery.REFRESH_MERGE
    return Recovery.STOP


@dataclass(frozen=True)
class Policy:
    revision: str
    rules: Mapping[Failure, Recovery]


@dataclass(frozen=True)
class Entry:
    """Declared references and structured local rules, not natural-language text."""

    references: Mapping[str, str]
    overrides: Mapping[Failure, Recovery] = field(default_factory=dict)


def validate_entry(entry: Entry, required: Mapping[str, Policy],
                   loaded: Mapping[str, Policy]) -> list[str]:
    """Compare an entry with an independently approved required-policy registry.

    The caller supplies actual loaded revisions/rules. Self-declared references
    do not prove loading. Newer timestamps never appoint a new policy authority.
    This checks structured declarations only, not arbitrary prose semantics.
    """
    errors = []
    if not required:
        return ["approved required-policy registry is empty"]
    expected_rules = {}
    for name, policy in required.items():
        if not name or not policy.revision.strip() or not policy.rules:
            errors.append("invalid approved policy declaration")
            continue
        if entry.references.get(name) != policy.revision:
            errors.append("missing or stale required policy reference")
        actual = loaded.get(name)
        if actual is None or actual != policy:
            errors.append("required policy not loaded at approved revision/content")
        for failure, action in policy.rules.items():
            if not isinstance(failure, Failure) or not isinstance(action, Recovery):
                errors.append("unrecognized approved failure rule")
                continue
            if failure in expected_rules and expected_rules[failure] != action:
                errors.append("approved policies conflict; resolve authority explicitly")
            expected_rules[failure] = action
    if set(entry.references) - set(required):
        errors.append("entry references an unapproved policy")
    if set(loaded) - set(required):
        errors.append("loaded policy is not in the approved registry")
    if set(expected_rules) != set(Failure):
        errors.append("approved policies do not classify every failure kind")
    for failure, action in entry.overrides.items():
        if (not isinstance(failure, Failure) or not isinstance(action, Recovery)
                or expected_rules.get(failure) != action):
            errors.append("local stop/retry rule conflicts with approved policies")
    return errors


@dataclass(frozen=True)
class RunEvidence:
    """A single run's evidence; no stage implies a later stage or future run.

    References belong in the adapter's durable, privacy-safe operation record.
    This data shape neither schedules work nor persists a journal.
    """

    schedule_acceptance: Evidence = Evidence()
    run_started: Evidence = Evidence()
    source_access: Evidence = Evidence()
    persistence: Evidence = Evidence()
    checkpoint: Evidence = Evidence()
    notification: Evidence = Evidence()
