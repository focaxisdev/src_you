#!/usr/bin/env python3
"""Validate the machine-readable fixtures for the behavioral contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
EXPECTED_TESTS = set(range(1, 15))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    acceptance = (ROOT / "tests" / "acceptance-tests.md").read_text(encoding="utf-8")
    headings = {
        int(number)
        for number in re.findall(r"^## Test (\d+)\s+—", acceptance, flags=re.MULTILINE)
    }
    require(headings == EXPECTED_TESTS, "acceptance headings must cover Tests 1-14", errors)

    fixture_paths = sorted(FIXTURES.glob("*.json"))
    fixtures: dict[str, dict] = {}
    covered: set[int] = set()
    for path in fixture_paths:
        try:
            fixture = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid fixture {path.name}: {error}")
            continue
        if not isinstance(fixture, dict):
            errors.append(f"fixture {path.name} must be a JSON object")
            continue
        fixtures[path.name] = fixture
        tests = fixture.get("tests", [])
        require(
            isinstance(tests, list) and all(isinstance(item, int) for item in tests),
            f"{path.name} must declare integer test IDs",
            errors,
        )
        if isinstance(tests, list):
            covered.update(item for item in tests if isinstance(item, int))
        require(
            "synthetic" in str(fixture.get("description", "")).lower(),
            f"{path.name} must identify itself as synthetic",
            errors,
        )

    require(covered == EXPECTED_TESTS, "fixtures must map to every Test 1-14", errors)

    durable = fixtures.get("durable-update.json", {})
    require(durable.get("expected", {}).get("active_value_count") == 1,
            "durable update must leave one active value", errors)
    require(durable.get("before", {}).get("status") == "current",
            "durable update must begin with one current value", errors)
    require(durable.get("expected", {}).get("current") == "Option B",
            "durable update must make the explicit value current", errors)
    require(durable.get("expected", {}).get("superseded") == "Option A",
            "durable update must supersede the prior value", errors)

    boundary = fixtures.get("project-boundary.json", {})
    global_state = boundary.get("global", {})
    project_state = boundary.get("project", {})
    forbidden = boundary.get("forbidden_global_fields", [])
    require(all(field not in global_state for field in forbidden),
            "project micro-state leaked into the global fixture", errors)
    require(all(field in project_state for field in forbidden),
            "project fixture must own every forbidden global field", errors)

    routing = fixtures.get("routing.json", {})
    route_tests = {case.get("test") for case in routing.get("cases", [])}
    require(route_tests == {1, 2, 10}, "routing cases must cover Tests 1, 2, and 10", errors)
    for case in routing.get("cases", []):
        require(bool(case.get("read")), f"routing Test {case.get('test')} needs a read set", errors)
        require(bool(case.get("must_not_read")),
                f"routing Test {case.get('test')} needs exclusions", errors)

    conflict = fixtures.get("conflict-resolution.json", {})
    require(conflict.get("memory_conflict", {}).get("expected_value") == "Option B",
            "canonical state must beat stale Memory", errors)
    require(conflict.get("explicit_update", {}).get("persist_if_durable") is True,
            "explicit durable updates must be persisted", errors)

    sensitive = fixtures.get("sensitive-input.json", {})
    require(sensitive.get("credential_placeholder") == "<REDACTED_SECRET>",
            "sensitive fixture must contain only a redacted credential placeholder", errors)
    require("raw_document_placeholder" not in sensitive.get("expected_storage", []),
            "raw sensitive evidence must not be expected storage", errors)

    recovery = fixtures.get("backup-recovery.json", {})
    require(recovery.get("newer_backup", {}).get("automatic_restore") is False,
            "a newer backup must not restore automatically", errors)
    require(recovery.get("restore", {}).get("explicit_operation_required") is True,
            "restore must require an explicit operation", errors)

    freshness = fixtures.get("external-freshness.json", {})
    require(freshness.get("expected", {}).get("revalidate_at_use_time") is True,
            "external observations must be revalidated at use time", errors)

    inference = fixtures.get("inference.json", {})
    require(inference.get("claim", {}).get("type") == "Inference",
            "unconfirmed model-derived claims must remain Inference", errors)
    require(inference.get("expected", {}).get("promote_without_confirmation") is False,
            "Inference must not be promoted without confirmation", errors)

    portability = fixtures.get("platform-portability.json", {})
    require(portability.get("core", {}).get("requires_provider_ui") is False,
            "the core contract must not require provider UI names", errors)
    require(len(portability.get("adapters", [])) >= 2,
            "portability fixture must map at least two replaceable adapters", errors)

    if errors:
        print("Acceptance fixture validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Acceptance fixture validation passed: Tests 1-14 mapped across "
        f"{len(fixture_paths)} synthetic fixtures."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
