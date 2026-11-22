"""Build checks from mameRomList.txt: one representative ROM per letter/number."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .matcher import RomMatcher

log = logging.getLogger(__name__)

# Digits 1-9 then a-z (lowercase)
CHARS = [str(i) for i in range(1, 10)] + [chr(c) for c in range(ord("a"), ord("z") + 1)]

DEFAULT_LIST = Path(__file__).resolve().parents[2] / "mameRomList.txt"


def load_rom_list(path: str | Path | None = None) -> list[str]:
    """Load ROM filenames from mameRomList.txt (one .zip per line)."""
    path = Path(path) if path else DEFAULT_LIST
    if not path.is_file():
        raise FileNotFoundError(f"ROM list not found: {path}")
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and ln.strip().lower().endswith(".zip")]


def first_rom_per_character(rom_names: list[str]) -> dict[str, list[str]]:
    """Group ROM names by first character (case-insensitive) and return only those in CHARS."""
    by_char: dict[str, list[str]] = {c: [] for c in CHARS}
    for name in sorted(rom_names, key=str.lower):
        if not name:
            continue
        first = name[0].lower()
        if first in by_char:
            by_char[first].append(name)
    return by_char


def build_letter_checks(
    list_path: str | Path | None = None,
    matcher: RomMatcher | None = None,
) -> list[dict[str, Any]]:
    """
    For each letter a-z and digit 1-9:
      - If no ROMs start with that character, log it.
      - Otherwise select only the first one (sorted) and optionally match it.

    Returns a list of result dicts.
    """
    names = load_rom_list(list_path)
    by_char = first_rom_per_character(names)

    results: list[dict[str, Any]] = []

    for char in CHARS:
        files = by_char[char]
        if not files:
            log.info("No games start with '%s'", char)
            results.append(
                {"char": char, "status": "no_games", "file": None, "total_for_char": 0, "matches": []}
            )
            continue

        first = files[0]
        log.info("Selected first game for '%s': %s (of %d)", char, first, len(files))

        matches: list[dict] = []
        if matcher is not None:
            # Placeholder: real MAME matching would extract internal ROM CRCs from the zip.
            # For now we treat the filename (without .zip) as a set name lookup if desired.
            set_name = Path(first).stem
            # Future: matcher.match_set(set_name) or similar
            matches = matcher.match(sha1=set_name)  # no-op unless index has it

        results.append(
            {
                "char": char,
                "status": "selected",
                "file": first,
                "total_for_char": len(files),
                "matches": matches,
            }
        )

    return results
