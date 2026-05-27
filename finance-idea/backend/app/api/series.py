"""GET /api/series/{key} — raw OHLC for a cached asset."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..deps import get_storage
from ..schemas import OhlcPoint

router = APIRouter()


@router.get("/series/{key}", response_model=list[OhlcPoint])
def get_series(key: str, limit: int = 4000) -> list[OhlcPoint]:
    s = get_storage()
    df = s.load("prices", key)
    if df is None or df.empty:
        raise HTTPException(404, detail=f"prices/{key} missing")
    if limit and len(df) > limit:
        df = df.iloc[-limit:]
    cols = df.columns
    out = []
    for idx, row in df.iterrows():
        out.append(OhlcPoint(
            date=str(idx.date()),
            open=float(row["open"]) if "open" in cols else float(row["close"]),
            high=float(row["high"]) if "high" in cols else float(row["close"]),
            low=float(row["low"]) if "low" in cols else float(row["close"]),
            close=float(row["close"]),
            volume=float(row["volume"]) if "volume" in cols else None,
        ))
    return out
