"""Parquet-based local cache.

Layout (relative to the package directory):

    data/
        prices/<key>.parquet         # OHLCV (Date index, columns: open/high/low/close/volume)
        nav/<key>.parquet            # NAV daily series for QDII ETFs
        macro/<key>.parquet          # macro / sentiment / yield series
        meta.json                    # per-key last-update timestamp

Everything is stored on a Date index in ISO format, sorted ascending, deduped.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Optional

import pandas as pd


PKG_DIR = Path(__file__).resolve().parent
DATA_DIR = PKG_DIR / "data"


@dataclass
class Storage:
    root: Path = DATA_DIR

    def __post_init__(self) -> None:
        for sub in ("prices", "nav", "macro"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    # ----- paths -----
    def _path(self, kind: str, key: str) -> Path:
        return self.root / kind / f"{key}.parquet"

    def meta_path(self) -> Path:
        return self.root / "meta.json"

    # ----- read -----
    def load(self, kind: str, key: str) -> Optional[pd.DataFrame]:
        p = self._path(kind, key)
        if not p.exists():
            return None
        df = pd.read_parquet(p)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
        df.index = pd.to_datetime(df.index)
        return df.sort_index()

    def last_date(self, kind: str, key: str) -> Optional[date]:
        df = self.load(kind, key)
        if df is None or df.empty:
            return None
        return df.index.max().date()

    # ----- write -----
    def upsert(self, kind: str, key: str, df: pd.DataFrame) -> int:
        """Merge `df` (must have DatetimeIndex) into existing series, dedupe by index."""
        if df is None or df.empty:
            return 0
        df = df.copy()
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df[~df.index.duplicated(keep="last")]

        existing = self.load(kind, key)
        if existing is not None:
            combined = pd.concat([existing, df])
            combined = combined[~combined.index.duplicated(keep="last")].sort_index()
        else:
            combined = df
        out = self._path(kind, key)
        combined.reset_index().rename(columns={"index": "date"}).to_parquet(out)
        self._touch_meta(key, kind, len(combined))
        return len(df)

    def _touch_meta(self, key: str, kind: str, rows: int) -> None:
        meta = self._read_meta()
        meta[f"{kind}/{key}"] = {
            "rows": rows,
            "refreshed_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.meta_path().write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    def _read_meta(self) -> dict:
        p = self.meta_path()
        if not p.exists():
            return {}
        return json.loads(p.read_text())

    # ----- introspection -----
    def list_keys(self, kind: str) -> list[str]:
        return sorted(p.stem for p in (self.root / kind).glob("*.parquet"))

    def summary(self) -> pd.DataFrame:
        rows = []
        for kind in ("prices", "nav", "macro"):
            for key in self.list_keys(kind):
                df = self.load(kind, key)
                if df is None or df.empty:
                    rows.append({"kind": kind, "key": key, "rows": 0,
                                 "first": None, "last": None})
                    continue
                rows.append({
                    "kind": kind, "key": key, "rows": len(df),
                    "first": df.index.min().date(),
                    "last": df.index.max().date(),
                })
        return pd.DataFrame(rows)


if __name__ == "__main__":
    s = Storage()
    print(s.summary().to_string(index=False))
