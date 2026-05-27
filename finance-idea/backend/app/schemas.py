"""Pydantic response schemas — also the API contract for the Vue frontend."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


SignalLevel = str  # "hot" | "warm" | "neutral" | "cold" | "na"


class SparkPoint(BaseModel):
    date: str
    value: float


class SignalSnapshot(BaseModel):
    """Lightweight current-state of a signal used by the dashboard grid."""
    id: str
    name: str
    name_cn: str
    value: Optional[float]
    unit: str = ""
    level: SignalLevel
    interpretation: str
    delta_7d: Optional[float] = None    # vs 7 trading days ago
    delta_30d: Optional[float] = None
    spark: list[SparkPoint] = Field(default_factory=list)  # last ~60 points
    last_update: Optional[str] = None


class SeriesPoint(BaseModel):
    date: str
    value: float


class OhlcPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None


class ThresholdBand(BaseModel):
    """Optional upper/lower bands plotted with the signal time series."""
    date: str
    upper: Optional[float] = None
    lower: Optional[float] = None


class BucketRow(BaseModel):
    bucket: str
    n: int
    fwd_means: dict[str, float]   # "5d" -> mean, "20d" -> mean, "60d" -> mean
    fwd_winrates: dict[str, float]


class EquityCurve(BaseModel):
    name: str
    points: list[SeriesPoint]
    stats: dict[str, Optional[float]]   # cagr, sharpe, maxdd, total, n_days


class IdeaSummary(BaseModel):
    id: str
    name: str
    name_cn: str
    description: str
    tags: list[str] = Field(default_factory=list)


class IdeaDetail(BaseModel):
    snapshot: SignalSnapshot
    description_md: str
    primary_series: list[SeriesPoint]      # the signal itself
    secondary_series: Optional[list[SeriesPoint]] = None   # underlying asset for overlay
    secondary_label: Optional[str] = None
    bands: Optional[list[ThresholdBand]] = None
    buckets: list[BucketRow] = Field(default_factory=list)
    bucket_horizons: list[str] = Field(default_factory=list)   # e.g. ["5d","20d","60d"]
    equity: list[EquityCurve] = Field(default_factory=list)


class DashboardResponse(BaseModel):
    asof: str
    signals: list[SignalSnapshot]


class IndexTick(BaseModel):
    key: str
    name: str
    value: float
    change_pct: float


class TickerResponse(BaseModel):
    asof: str
    items: list[IndexTick]


class MetaEntry(BaseModel):
    key: str
    kind: str
    rows: int
    first: Optional[str] = None
    last: Optional[str] = None


class MetaResponse(BaseModel):
    entries: list[MetaEntry]
    refreshed_at: Optional[str] = None
