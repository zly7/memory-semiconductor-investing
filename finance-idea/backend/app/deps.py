"""Dependency wiring: storage singleton + path bootstrap."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATA_API = ROOT / "finance-data-api"

# Make finance-data-api modules importable (hyphenated dir → manual sys.path).
sys.path.insert(0, str(DATA_API))

from storage import Storage  # noqa: E402
from universe import UNIVERSE, by_key  # noqa: E402

_storage: Storage | None = None


def get_storage() -> Storage:
    global _storage
    if _storage is None:
        _storage = Storage()
    return _storage


__all__ = ["Storage", "UNIVERSE", "by_key", "get_storage", "ROOT", "DATA_API"]
