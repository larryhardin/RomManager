"""Scan a MAME ROM directory (.zip files) and test the first game per letter/number."""

from __future__ import annotations

import hashlib
import logging
import zipfile
from pathlib import Path
from typing import Any

from .matcher import RomMatcher

log = logging.getLogger(__name__)

ALPHABET_AND_NUMBERS = [str(i) for i in range(1, 10)] + [chr(c) for c in range(ord("a"), ord("z") + 1)]


def _crc32_of_zip_contents(zip_path: Path) -> str | None:
    """Compute CRC32 of the concatenated contents of a .zip (simple stand-in for set matching)."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            h = hashlib.sha1()  # use SHA1 for uniqueness; CRC32 alone can collide
            for info in sorted(zf.infolist(), key=lambda i: i.filename):
                if info.is_dir():
                    continue
                h.update(zf.read(info.filename))
            return h.hexdigest().upper()
    except (zipfile.BadZipFile, OSError) as exc:
        log.warning("Could not read %s: %s", zip_path, exc)
        return None


def test_first_mame_rom_per_letter(
    rom_dir: str | Path,
    matcher: RomMatcher | None = None,
) -> list[dict[str, Any]]:
    """
    For each letter a-z and digit 1-9:
      - Find .zip files starting with that character (case-insensitive).
      - If none, log that no games start with that letter.
      - If any, take only the first one and attempt a match (if matcher provided).

    Returns a list of result dicts, one per character.
    """
    rom_dir = Path(rom_dir)
    if not rom_dir.is_dir():
        raise FileNotFoundError(f"ROM directory not found: {rom_dir}")

    zips = sorted(p for p in rom_dir.iterdir() if p.suffix.lower() == ".zip" and p.is_file())
    by_char: dict[str, list[Path]] = {c: [] for c in ALPHABET_AND_NUMBERS}

    for z in zips:
        first = z.name[0].lower() if z.name else ""
        if first in by_char:
            by_char[first].append(z)

    results: list[dict[str, Any]] = []

    for char in ALPHABET_AND_NUMBERS:
        files = by_char[char]
        if not files:
            log.info("No games start with '%s'", char)
            results.append({"char": char, "status": "no_games", "file": None, "matches": []})
            continue

        first_file = files[0]
        log.info("Testing first game for '%s': %s (of %d)", char, first_file.name, len(files))

        match_results: list[dict] = []
        if matcher is not None:
            # For a real MAME test we would extract CRCs of the ROMs inside the zip
            # and look them up. Here we use a content hash as a placeholder identifier.
            content_hash = _crc32_of_zip_contents(first_file)
            if content_hash:
                match_results = matcher.match(sha1=content_hash)

        results.append(
            {
                "char": char,
                "status": "tested",
                "file": first_file.name,
                "total_for_char": len(files),
                "matches": match_results,
            }
        )

    return results
