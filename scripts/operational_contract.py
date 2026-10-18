"""Small, provider-neutral reference contracts; no storage or model integration.

Payloads represent one canonical document. A caller prepares an authorized
durable change (including any supersession history) before using this module.
The backend must provide authoritative reads and atomic compare-and-swap.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Protocol


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_RUN = "NOT_RUN"


@dataclass(frozen=True)
class Evidence:
    status: Status = Status.NOT_RUN
    reference: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.status, Status):
            raise ValueError("use a defined evidence status")
        if self.status is Status.PASS and not self.reference.strip():
            raise ValueError("PASS requires a verification reference")


@dataclass(frozen=True)
class Capabilities:
    """Task-scoped probes, not inferred from tool names or other operations."""

    read: Evidence = Evidence()
    create: Evidence = Evidence()
    guarded_update: Evidence = Evidence()
    readback: Evidence = Evidence()

    def update_ready(self) -> bool:
        return all(item.status is Status.PASS for item in
                   (self.read, self.guarded_update, self.readback))


@dataclass(frozen=True)
class Completion:
    """Independent results: producing an answer proves no durable write."""

    delivery: Evidence = Evidence()
    persistence: Evidence = Evidence()
    checkpoint: Evidence = Evidence()


@dataclass(frozen=True)
class Identity:
    source: str
    record_id: str
    scope: str


@dataclass(frozen=True)
class Snapshot:
    identity: Identity
    version: str
    payload: dict


class Conflict(Exception):
    """The atomic version guard rejected the write; nothing was written."""


class UncertainWrite(Exception):
    """A write may have committed. An authoritative read must precede retry."""


class Unavailable(Exception):
    """A read is unavailable, or a write is known not to have executed."""


class Store(Protocol):
    def read(self, identity: Identity) -> Snapshot:
        """Return a fresh authoritative snapshot or raise Unavailable."""
        ...

    def guarded_update(self, identity: Identity, version: str,
                       payload: dict) -> None:
        """Atomically replace exactly this identity iff version still matches.

        Versions must change on every mutation and must never be reused. Return
        only for an acknowledged write; use UncertainWrite for unknown outcomes.
        There is deliberately no create method in the update protocol.
        """
        ...


@dataclass(frozen=True)
class UpdateResult:
    status: Status
    reason: str
    attempts: int = 0
    snapshot: Snapshot | None = None

    @property
    def saved(self) -> bool:
        return self.status is Status.PASS


def _json_value(value: object) -> bool:
    if type(value) in (str, int, bool, type(None)):
        return True
    if type(value) is float:
        return isfinite(value)
    if type(value) is list:
        return all(_json_value(item) for item in value)
    if type(value) is dict:
        return all(type(key) is str and _json_value(item)
                   for key, item in value.items())
    return False


def _same(left: object, right: object) -> bool:
    """Type-strict JSON structure equality: True, 1, and 1.0 are distinct."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (left.keys() == right.keys() and
                all(_same(left[key], right[key]) for key in left))
    if type(left) is list:
        return (len(left) == len(right) and
                all(_same(a, b) for a, b in zip(left, right)))
    return left == right


def _valid(snapshot: Snapshot, identity: Identity) -> bool:
    return (isinstance(snapshot, Snapshot) and snapshot.identity == identity and
            all(isinstance(item, str) and item for item in
                (identity.source, identity.record_id, identity.scope)) and
            isinstance(snapshot.version, str) and bool(snapshot.version) and
            type(snapshot.payload) is dict and _json_value(snapshot.payload))


def _merge(base: dict, current: dict, changes: dict) -> dict | None:
    """Conservative top-level three-way merge; nested edits are one field.

    Only unrelated fields merge automatically. A concurrent change already
    equal to the desired value is compatible. Missing is distinct from None.
    Deletion is intentionally outside this narrow reference implementation.
    """
    missing = object()
    for key, desired in changes.items():
        old, now = base.get(key, missing), current.get(key, missing)
        if not _same(now, old) and not _same(now, desired):
            return None
    merged = deepcopy(current)
    merged.update(deepcopy(changes))
    return merged


def guarded_update(store: Store, base: Snapshot, changes: dict,
                   capabilities: Capabilities, *, max_attempts: int = 3
                   ) -> UpdateResult:
    """Refresh, merge, CAS and read back before reporting canonical state saved.

    No create fallback, implicit authority migration, blind retry, or logging
    of payloads. The reference trusts a conforming backend, not an LLM.
    """
    if max_attempts < 1 or not _valid(base, base.identity):
        raise ValueError("valid base and positive attempt limit required")
    if type(changes) is not dict or not changes or not _json_value(changes):
        raise ValueError("a nonempty prepared JSON field update is required")
    if not capabilities.update_ready():
        return UpdateResult(Status.BLOCKED, "required operation not verified")
    identity = base.identity
    # Defensive copies keep caller/backend aliases out of the merge baseline.
    base = deepcopy(base)
    changes = deepcopy(changes)
    for attempt in range(1, max_attempts + 1):
        try:
            fresh = deepcopy(store.read(identity))
        except Unavailable:
            return UpdateResult(Status.BLOCKED, "refresh unavailable", attempt - 1)
        if not _valid(fresh, identity):
            return UpdateResult(Status.FAIL, "refresh identity/version invalid", attempt - 1)
        merged = _merge(base.payload, fresh.payload, changes)
        if merged is None:
            return UpdateResult(Status.BLOCKED, "overlapping change needs resolution", attempt - 1)
        if _same(merged, fresh.payload):
            return UpdateResult(Status.PASS, "desired state verified; no write needed",
                                attempt - 1, fresh)
        uncertain = False
        try:
            store.guarded_update(identity, fresh.version, deepcopy(merged))
        except Conflict:
            # A rejected guard is known not to have written. Refresh on loop.
            continue
        except UncertainWrite:
            uncertain = True
        except Unavailable:
            return UpdateResult(Status.BLOCKED, "write unavailable; not executed", attempt)
        try:
            observed = deepcopy(store.read(identity))
        except Unavailable:
            return UpdateResult(Status.BLOCKED, "write outcome unverified; read before retry", attempt)
        if not _valid(observed, identity):
            return UpdateResult(Status.FAIL, "readback identity/version invalid", attempt)
        if _same(observed.payload, merged) and observed.version != fresh.version:
            return UpdateResult(Status.PASS, "exact canonical readback verified", attempt, observed)
        if (uncertain and observed.version == fresh.version and
                _same(observed.payload, fresh.payload)):
            # No commit is visible as of this authoritative read. A late write
            # must still enforce its original atomic guard; a retry cannot
            # duplicate it because versions are never reused.
            continue
        return UpdateResult(Status.BLOCKED,
                            "readback mismatch; reconcile before further writes", attempt)
    return UpdateResult(Status.BLOCKED, "attempt limit; refresh and resolve", max_attempts)


class Retrieval(str, Enum):
    SKIP = "SKIP"
    REUSE = "REUSE"
    REFRESH = "REFRESH"


def retrieval_action(*, needs_personal_state: bool, verified_source: bool = False,
                     same_task_and_scope: bool = False, resumed: bool = False,
                     changed: bool = False, conflict: bool = False,
                     writing: bool = False) -> Retrieval:
    """A decision rule, not a persistent cache or automatic source discovery.

    'changed' includes changes to authority, content, routing, access, or task.
    Verified means identity/authority/freshness were checked for this scope.
    Callers must invalidate the verification on those events; writes always
    require fresh authoritative state even if a caller mislabels relevance.
    """
    if writing:
        return Retrieval.REFRESH
    if not needs_personal_state:
        return Retrieval.SKIP
    if (verified_source and same_task_and_scope and
            not any((resumed, changed, conflict))):
        return Retrieval.REUSE
    return Retrieval.REFRESH
