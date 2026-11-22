"""Simple hash-based ROM matcher.

In a full implementation this would load No-Intro / Redump / MAME / TOSEC DAT files
and build an index by CRC32/MD5/SHA1. For now it provides the interface used by tests.
"""

from __future__ import annotations

from typing import Any


class RomMatcher:
    """Matches ROMs against an in-memory index of hash -> metadata."""

    def __init__(self) -> None:
        # key: normalized hash (uppercase hex), value: list of match dicts
        self._index: dict[str, list[dict[str, Any]]] = {}

    def add_entry(
        self,
        *,
        database: str,
        platform: str,
        game_name: str,
        crc32: str | None = None,
        md5: str | None = None,
        sha1: str | None = None,
        **extra: Any,
    ) -> None:
        entry = {
            "database": database,
            "platform": platform,
            "game_name": game_name,
            **extra,
        }
        for h in (crc32, md5, sha1):
            if h:
                key = h.strip().upper()
                self._index.setdefault(key, []).append(entry)

    def match(
        self,
        *,
        crc32: str | None = None,
        md5: str | None = None,
        sha1: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return all matches for any of the supplied hashes. Deduplicated by game_name+database+platform."""
        seen: set[tuple] = set()
        results: list[dict[str, Any]] = []
        for h in (crc32, md5, sha1):
            if not h:
                continue
            for entry in self._index.get(h.strip().upper(), []):
                ident = (entry["database"], entry["platform"], entry["game_name"])
                if ident not in seen:
                    seen.add(ident)
                    results.append(entry)
        return results
