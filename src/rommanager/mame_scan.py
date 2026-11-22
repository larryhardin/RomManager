"""Scan a MAME ROM directory and look up each set name in a MAME DAT/XML.

Produces mame.log with:
  Filename, GameName, description, year

Set name is the zip filename without the extension (and without a leading dot if any).
Suffixes such as j, a, b, w are left intact — MAME treats them as separate sets (clones/regions).
"""

from __future__ import annotations

import argparse
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


def load_mame_dat(dat_path: str | Path) -> dict[str, dict[str, Any]]:
    """Load a MAME listxml-style DAT and return a dict keyed by machine name."""
    dat_path = Path(dat_path)
    tree = ET.parse(dat_path)
    root = tree.getroot()

    machines: dict[str, dict[str, Any]] = {}
    for machine in root.findall("machine"):
        name = machine.get("name")
        if not name:
            continue
        desc_el = machine.find("description")
        year_el = machine.find("year")
        machines[name] = {
            "description": desc_el.text if desc_el is not None and desc_el.text else "",
            "year": year_el.text if year_el is not None and year_el.text else "",
            "sourcefile": machine.get("sourcefile", ""),
            "cloneof": machine.get("cloneof", ""),
        }
    return machines


def set_name_from_filename(filename: str) -> str:
    """Return the MAME set name from a .zip filename."""
    p = Path(filename)
    return p.stem  # removes .zip; keeps j/a/b/w suffixes


def scan_mame_directory(
    rom_dir: str | Path,
    dat_path: str | Path,
    log_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """
    Scan .zip files in rom_dir, look up each set name in the DAT, and write mame.log.

    Returns the list of result records.
    """
    rom_dir = Path(rom_dir)
    if not rom_dir.is_dir():
        raise FileNotFoundError(f"ROM directory not found: {rom_dir}")

    machines = load_mame_dat(dat_path)
    log.info("Loaded %d machines from DAT", len(machines))

    zips = sorted(
        p for p in rom_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".zip"
    )

    results: list[dict[str, Any]] = []
    for z in zips:
        set_name = set_name_from_filename(z.name)
        info = machines.get(set_name)
        record = {
            "filename": z.name,
            "game_name": set_name,
            "description": info["description"] if info else "NOT FOUND",
            "year": info["year"] if info else "",
        }
        results.append(record)

    # Write log
    out = Path(log_path) if log_path else rom_dir / "mame.log"
    with out.open("w", encoding="utf-8") as f:
        f.write("Filename, GameName, description, year\n")
        for r in results:
            # Escape commas in description for simple CSV-like output
            desc = r["description"].replace(",", ";")
            f.write(f"{r['filename']}, {r['game_name']}, {desc}, {r['year']}\n")

    log.info("Wrote %d entries to %s", len(results), out)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan MAME ROM directory against a DAT")
    parser.add_argument("rom_dir", help="Path to directory containing .zip ROM sets")
    parser.add_argument("dat", help="Path to MAME listxml DAT/XML file")
    parser.add_argument("--log", help="Output log path (default: <rom_dir>/mame.log)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    scan_mame_directory(args.rom_dir, args.dat, args.log)


if __name__ == "__main__":
    main()
