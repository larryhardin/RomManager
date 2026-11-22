"""Executable tests for the sample match cases.

Each case in sample_matches.json is loaded into a RomMatcher and asserted to
return exactly one result when queried by its hash(es).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rommanager.matcher import RomMatcher

SAMPLE_PATH = Path(__file__).parent / "sample_matches.json"


def load_cases() -> list[dict]:
    with SAMPLE_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["cases"]


@pytest.fixture
def matcher() -> RomMatcher:
    """Build a matcher pre-populated with the sample cases."""
    m = RomMatcher()
    for case in load_cases():
        m.add_entry(
            database=case["database"],
            platform=case["platform"],
            game_name=case["game_name"],
            crc32=case.get("crc32"),
            md5=case.get("md5"),
            sha1=case.get("sha1"),
        )
    return m


def test_all_cases_return_exactly_one_match(matcher: RomMatcher) -> None:
    """Every sample case must produce exactly one match when looked up by its hashes."""
    cases = load_cases()
    assert len(cases) > 0, "No sample cases found"

    for case in cases:
        results = matcher.match(
            crc32=case.get("crc32"),
            md5=case.get("md5"),
            sha1=case.get("sha1"),
        )
        assert len(results) == case["expected_matches"], (
            f"{case['id']}: expected {case['expected_matches']} match(es), got {len(results)}"
        )
        # Confirm the returned metadata matches the case
        match = results[0]
        assert match["database"] == case["database"]
        assert match["platform"] == case["platform"]
        assert match["game_name"] == case["game_name"]


def test_unknown_hash_returns_zero(matcher: RomMatcher) -> None:
    results = matcher.match(crc32="00000000")
    assert results == []


def test_sample_file_is_valid_json() -> None:
    cases = load_cases()
    required = {"id", "database", "platform", "game_name", "expected_matches"}
    for case in cases:
        missing = required - set(case)
        assert not missing, f"{case.get('id')}: missing fields {missing}"
        assert case["expected_matches"] == 1
        # At least one hash must be present
        assert any(case.get(h) for h in ("crc32", "md5", "sha1"))
