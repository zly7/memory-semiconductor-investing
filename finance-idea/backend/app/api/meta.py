"""GET /api/meta and /api/ticker (top-of-page index ticker)."""
from __future__ import annotations

import datetime as dt
import json

from fastapi import APIRouter

from ..deps import get_storage, DATA_API
from ..schemas import (IndexTick, MetaEntry, MetaResponse, TickerResponse)

router = APIRouter()


TICKER_KEYS = [
    ("SHCOMP", "上证综指"),
    ("CSI300", "沪深300"),
    ("CHINEXT", "创业板指"),
    ("HSI", "恒生指数"),
    ("SPY", "S&P 500"),
    ("QQQ", "Nasdaq 100"),
    ("VIX", "VIX"),
    ("DXY", "美元指数"),
]


@router.get("/meta", response_model=MetaResponse)
def get_meta() -> MetaResponse:
    s = get_storage()
    summary = s.summary()
    entries = []
    for row in summary.to_dict("records"):
        entries.append(MetaEntry(
            key=row["key"], kind=row["kind"], rows=row["rows"],
            first=str(row["first"]) if row["first"] else None,
            last=str(row["last"]) if row["last"] else None,
        ))
    refreshed_at = None
    meta_p = DATA_API / "data" / "meta.json"
    if meta_p.exists():
        try:
            data = json.loads(meta_p.read_text())
            ts = [v.get("refreshed_at") for v in data.values() if v.get("refreshed_at")]
            refreshed_at = max(ts) if ts else None
        except Exception:
            pass
    return MetaResponse(entries=entries, refreshed_at=refreshed_at)


@router.get("/ticker", response_model=TickerResponse)
def get_ticker() -> TickerResponse:
    s = get_storage()
    items = []
    for key, label in TICKER_KEYS:
        df = s.load("prices", key)
        if df is None or df.empty or "close" not in df.columns:
            continue
        close = df["close"].dropna().astype(float)
        if len(close) < 2:
            continue
        items.append(IndexTick(
            key=key, name=label,
            value=float(close.iloc[-1]),
            change_pct=float((close.iloc[-1] / close.iloc[-2] - 1) * 100),
        ))
    return TickerResponse(asof=dt.datetime.now().isoformat(timespec="seconds"),
                          items=items)
