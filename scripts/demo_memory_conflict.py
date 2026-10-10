#!/usr/bin/env python3
"""Run a synthetic, deterministic conflict demo. No LLM or service is called.

This deliberately narrow example trusts a hand-prepared update and a designated
canonical input. It is not a natural-language parser, authorization boundary,
complete state validator, or production storage adapter.
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "memory-conflict-demo" / "input.json"


def current_record(records: list[dict], record_id: str, scope: str) -> dict:
    """Fail closed if the designated canonical input lacks one current value."""
    matches = [
        record for record in records
        if record["id"] == record_id and record["scope"] == scope
        and record["status"] == "current"
    ]
    if len(matches) != 1:
        raise ValueError("expected exactly one current canonical record")
    return matches[0]


def apply_prepared_update(records: list[dict], update: dict) -> list[dict]:
    """Replace a confirmed durable value, preserving its supersession history."""
    if not all(update.get(flag) is True for flag in ("confirmed", "durable", "authorized")):
        raise ValueError("demo requires a confirmed, durable, authorized update")
    result = copy.deepcopy(records)
    record = current_record(result, update["id"], update["scope"])
    if record["statement"] == update["statement"]:
        return result
    previous = copy.deepcopy(record)
    previous["status"] = "superseded"
    record.update(
        statement=update["statement"],
        effective_from=update["effective_from"],
        evidence=update["evidence"],
        supersedes=previous,
    )
    return result


def run_demo() -> str:
    fixture = json.loads(INPUT.read_text(encoding="utf-8"))
    records = fixture["canonical"]
    record_id, scope = fixture["record_id"], fixture["scope"]
    before = current_record(records, record_id, scope)
    updated = apply_prepared_update(records, fixture["prepared_update"])

    # Real local write and fresh read, confined to a disposable directory.
    with tempfile.TemporaryDirectory(prefix="src-you-demo-") as directory:
        state_path = Path(directory) / "canonical.json"
        state_path.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
        reloaded = json.loads(state_path.read_text(encoding="utf-8"))
    after = current_record(reloaded, record_id, scope)
    previous = after["supersedes"]
    lines = [
        "src_you | synthetic memory-conflict demo",
        "Mode: deterministic Python; no LLM, network, or real personal data.",
        "Input: examples/memory-conflict-demo/input.json",
        "",
        f"Canonical before: {before['statement']}",
        f"Cached Memory:    {fixture['cached_memory']}",
        f"User instruction: {fixture['user_instruction']}",
        "Update: hand-prepared structured fields; no language interpretation.",
        "",
        "Applied update; wrote and reloaded temporary canonical JSON.",
        f"Canonical now:    {after['statement']}",
        f"Cached Memory:    {fixture['cached_memory']} (unchanged; not authoritative)",
        f"Selected value:   {after['statement']}",
        "Selection is a canonical record lookup, not an AI-generated answer.",
        f"Trace: {after['id']} [{after['scope']}]; stable ID retained",
        f"  {previous['effective_from']} | {previous['status']} | {previous['statement']}",
        f"  {after['effective_from']} | {after['status']} | {after['statement']}",
        f"  Evidence: {after['evidence']}",
        "",
    ]
    ambiguous = copy.deepcopy(reloaded)
    ambiguous.append(dict(copy.deepcopy(previous), status="current"))
    try:
        current_record(ambiguous, record_id, scope)
    except ValueError as error:
        lines.append(f"Negative case (two current records): REJECTED: {error}.")
    else:
        raise RuntimeError("negative case unexpectedly accepted ambiguous state")
    lines.append("Temporary state removed; repository inputs were not modified.")
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.write(run_demo())
    return 0


if __name__ == "__main__":
    sys.exit(main())
