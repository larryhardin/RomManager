"""Simple JSON config for RomManager.

Stores paths the UI, CLI, and API can share.
Default location: data/config.json (relative to repo root).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path("data/config.json")

DEFAULT_CONFIG: dict[str, Any] = {
    "mame": {
        "roms_directory": "",
        "xml_database": "data/MAME/XML/mame_728_0.289.xml",
        "daemon_script": "rom_daemon_threaded.sh",
    }
}


def load_config(path: Path | str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    path = Path(path)
    if not path.is_file():
        save_config(DEFAULT_CONFIG, path)
        return DEFAULT_CONFIG.copy()
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict[str, Any], path: Path | str = DEFAULT_CONFIG_PATH) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def get_mame_roms_directory(path: Path | str = DEFAULT_CONFIG_PATH) -> str:
    cfg = load_config(path)
    return cfg.get("mame", {}).get("roms_directory", "")


def get_mame_xml_database(path: Path | str = DEFAULT_CONFIG_PATH) -> str:
    cfg = load_config(path)
    return cfg.get("mame", {}).get("xml_database", "")


def get_mame_daemon_script(path: Path | str = DEFAULT_CONFIG_PATH) -> str:
    cfg = load_config(path)
    return cfg.get("mame", {}).get("daemon_script", "rom_daemon_threaded.sh")


def set_mame_roms_directory(value: str, path: Path | str = DEFAULT_CONFIG_PATH) -> None:
    cfg = load_config(path)
    cfg.setdefault("mame", {})["roms_directory"] = value
    save_config(cfg, path)


def set_mame_xml_database(value: str, path: Path | str = DEFAULT_CONFIG_PATH) -> None:
    cfg = load_config(path)
    cfg.setdefault("mame", {})["xml_database"] = value
    save_config(cfg, path)


def set_mame_daemon_script(value: str, path: Path | str = DEFAULT_CONFIG_PATH) -> None:
    cfg = load_config(path)
    cfg.setdefault("mame", {})["daemon_script"] = value
    save_config(cfg, path)
