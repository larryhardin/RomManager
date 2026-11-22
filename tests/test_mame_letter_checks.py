"""Tests for building one-check-per-letter from mameRomList.txt."""

from __future__ import annotations

import pytest

from rommanager.mame_letter_test import build_letter_checks, load_rom_list


def test_load_rom_list_exists() -> None:
    names = load_rom_list()
    assert len(names) > 1000, "Expected a large MAME ROM list"
    assert all(n.lower().endswith(".zip") for n in names[:100])


def test_build_letter_checks_covers_alphabet_and_numbers() -> None:
    results = build_letter_checks()
    chars = [r["char"] for r in results]
    assert set(chars) == set("123456789" + "abcdefghijklmnopqrstuvwxyz")

    selected = [r for r in results if r["status"] == "selected"]
    no_games = [r for r in results if r["status"] == "no_games"]

    # We expect most letters to have at least one game
    assert len(selected) >= 20
    # Digits 1-9 should mostly have entries (MAME has numbered sets)
    digit_selected = [r for r in selected if r["char"].isdigit()]
    assert len(digit_selected) >= 5

    for r in selected:
        assert r["file"] is not None
        assert r["file"].lower().startswith(r["char"])
        assert r["total_for_char"] >= 1

    for r in no_games:
        assert r["file"] is None
        assert r["total_for_char"] == 0
