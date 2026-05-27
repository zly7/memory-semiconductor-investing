"""Shared helpers: forward returns, bucketing, equity curves, snapshot wrapper."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from ..deps import get_storage
from ..schemas import (BucketRow, EquityCurve, IdeaDetail, SeriesPoint,
                       SignalSnapshot, SparkPoint, ThresholdBand)


# ---------- data accessors ----------
def load_price(key: str, col: str = "close") -> pd.Series:
    s = get_storage()
    df = s.load("prices", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"prices/{key} missing in cache")
    if col not in df.columns:
        for fb in ("close", "adj_close", "latest"):
            if fb in df.columns:
                col = fb
                break
    return df[col].dropna().astype(float)


def load_nav(key: str) -> pd.Series:
    s = get_storage()
    df = s.load("nav", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"nav/{key} missing in cache")
    return df["nav"].dropna().astype(float)


def load_macro(key: str) -> pd.DataFrame:
    s = get_storage()
    df = s.load("macro", key)
    if df is None:
        raise FileNotFoundError(f"macro/{key} missing in cache")
    return df


# ---------- numeric helpers ----------
def forward_return(s: pd.Series, h: int) -> pd.Series:
    return s.shift(-h) / s - 1.0


def percentile_bucket(s: pd.Series, n: int = 5) -> pd.Series:
    rk = s.rank(pct=True)
    return pd.qcut(rk, n, labels=[f"q{i+1}" for i in range(n)])


def equity_curve_series(daily_ret: pd.Series) -> pd.Series:
    return (1.0 + daily_ret.fillna(0)).cumprod()


def strategy_stats(daily_ret: pd.Series) -> dict[str, Optional[float]]:
    daily_ret = daily_ret.dropna()
    if daily_ret.empty:
        return {"cagr": None, "sharpe": None, "maxdd": None,
                "total": None, "n_days": 0}
    eq = equity_curve_series(daily_ret)
    years = len(daily_ret) / 252.0
    cagr = eq.iloc[-1] ** (1 / years) - 1 if years > 0 else None
    sharpe = (daily_ret.mean() / daily_ret.std() * np.sqrt(252)
              if daily_ret.std() > 0 else None)
    dd = float((eq / eq.cummax() - 1).min())
    return {
        "n_days": int(len(daily_ret)),
        "total": float(eq.iloc[-1] - 1),
        "cagr": None if cagr is None else float(cagr),
        "sharpe": None if sharpe is None else float(sharpe),
        "maxdd": dd,
    }


# ---------- conversion to schema objects ----------
def to_series_points(s: pd.Series, max_points: int = 4000) -> list[SeriesPoint]:
    if s is None or s.empty:
        return []
    s = s.dropna()
    if len(s) > max_points:
        step = len(s) // max_points + 1
        s = s.iloc[::step]
    return [SeriesPoint(date=str(idx.date()), value=float(v))
            for idx, v in s.items() if np.isfinite(v)]


def to_spark(s: pd.Series, n: int = 60) -> list[SparkPoint]:
    s = s.dropna().tail(n)
    return [SparkPoint(date=str(idx.date()), value=float(v))
            for idx, v in s.items() if np.isfinite(v)]


def to_threshold_bands(upper: pd.Series, lower: pd.Series,
                       max_points: int = 4000) -> list[ThresholdBand]:
    df = pd.concat([upper.rename("u"), lower.rename("l")], axis=1).dropna(how="all")
    if df.empty:
        return []
    if len(df) > max_points:
        step = len(df) // max_points + 1
        df = df.iloc[::step]
    out = []
    for idx, row in df.iterrows():
        out.append(ThresholdBand(
            date=str(idx.date()),
            upper=None if pd.isna(row["u"]) else float(row["u"]),
            lower=None if pd.isna(row["l"]) else float(row["l"]),
        ))
    return out


def make_bucket_rows(signal: pd.Series, asset: pd.Series,
                     horizons: dict[str, int]) -> list[BucketRow]:
    """horizons example: {'5d': 5, '20d': 20, '60d': 60}."""
    idx = signal.index.intersection(asset.index)
    signal = signal.loc[idx]
    fwds = {label: forward_return(asset.loc[idx], h) for label, h in horizons.items()}
    cat = percentile_bucket(signal, 5)
    rows = []
    for bucket in [f"q{i+1}" for i in range(5)]:
        mask = (cat == bucket)
        n = int(mask.sum())
        means = {label: float(fwds[label][mask].mean())
                 for label in horizons if not np.isnan(fwds[label][mask].mean())}
        wins = {label: float((fwds[label][mask] > 0).mean())
                for label in horizons if mask.sum() > 0}
        rows.append(BucketRow(bucket=bucket, n=n, fwd_means=means, fwd_winrates=wins))
    return rows


def make_equity(daily_ret: pd.Series, name: str,
                max_points: int = 1500) -> EquityCurve:
    eq = equity_curve_series(daily_ret)
    return EquityCurve(
        name=name,
        points=to_series_points(eq, max_points=max_points),
        stats=strategy_stats(daily_ret),
    )


# ---------- helper: derive a delta vs N-trading-days-ago ----------
def delta(s: pd.Series, n: int) -> Optional[float]:
    s = s.dropna()
    if len(s) <= n:
        return None
    return float(s.iloc[-1] - s.iloc[-1 - n])


# ---------- bridge dataclass that each signal returns ----------
@dataclass
class SignalBundle:
    id: str
    name: str
    name_cn: str
    description: str
    description_md: str
    unit: str
    interpret: callable        # (latest_value) -> (level, text)
    primary_series: pd.Series
    secondary_series: Optional[pd.Series] = None
    secondary_label: Optional[str] = None
    upper_band: Optional[pd.Series] = None
    lower_band: Optional[pd.Series] = None
    bucket_asset: Optional[pd.Series] = None     # asset used for forward-return bucket
    bucket_horizons: dict[str, int] = None
    equity_specs: list[tuple[str, pd.Series]] = None   # list of (name, daily_ret)

    def snapshot(self) -> SignalSnapshot:
        latest = self.primary_series.dropna()
        if latest.empty:
            return SignalSnapshot(id=self.id, name=self.name, name_cn=self.name_cn,
                                  value=None, unit=self.unit, level="na",
                                  interpretation="data unavailable",
                                  delta_7d=None, delta_30d=None,
                                  spark=[], last_update=None)
        v = float(latest.iloc[-1])
        level, text = self.interpret(v)
        return SignalSnapshot(
            id=self.id, name=self.name, name_cn=self.name_cn,
            value=round(v, 4), unit=self.unit, level=level, interpretation=text,
            delta_7d=delta(latest, 5),   # ~7 calendar = 5 trading
            delta_30d=delta(latest, 21),
            spark=to_spark(latest, n=60),
            last_update=str(latest.index[-1].date()),
        )

    def detail(self) -> IdeaDetail:
        snap = self.snapshot()
        bands = None
        if self.upper_band is not None and self.lower_band is not None:
            bands = to_threshold_bands(self.upper_band, self.lower_band)
        buckets = []
        bucket_horizons = []
        if (self.bucket_asset is not None and self.bucket_horizons):
            buckets = make_bucket_rows(self.primary_series, self.bucket_asset,
                                       self.bucket_horizons)
            bucket_horizons = list(self.bucket_horizons.keys())
        equity = []
        if self.equity_specs:
            for nm, dr in self.equity_specs:
                equity.append(make_equity(dr, nm))
        return IdeaDetail(
            snapshot=snap,
            description_md=self.description_md,
            primary_series=to_series_points(self.primary_series),
            secondary_series=(to_series_points(self.secondary_series)
                              if self.secondary_series is not None else None),
            secondary_label=self.secondary_label,
            bands=bands,
            buckets=buckets,
            bucket_horizons=bucket_horizons,
            equity=equity,
        )
