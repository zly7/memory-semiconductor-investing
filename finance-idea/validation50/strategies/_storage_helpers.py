"""Storage-bridging helpers (avoids polluting runner.py public surface)."""
from __future__ import annotations

import pandas as pd
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "finance-data-api"))
from storage import Storage  # noqa: E402

_storage = Storage()


def load_nav(key: str) -> pd.Series:
    df = _storage.load("nav", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"nav/{key}")
    return df["nav"].dropna().astype(float)


def load_macro_df(key: str) -> pd.DataFrame:
    df = _storage.load("macro", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"macro/{key}")
    return df
