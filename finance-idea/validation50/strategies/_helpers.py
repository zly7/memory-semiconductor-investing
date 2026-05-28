"""Shared helpers for validation50 strategy modules.

All public functions in this module assume *daily* pandas Series/DataFrames
with a DatetimeIndex sorted ascending. Returns are simple (not log) unless
noted otherwise.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Series math
# ---------------------------------------------------------------------------
def daily_returns(price: pd.Series) -> pd.Series:
    return price.pct_change().fillna(0.0)


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def rolling_z(s: pd.Series, n: int) -> pd.Series:
    mu = s.rolling(n, min_periods=max(20, n // 4)).mean()
    sd = s.rolling(n, min_periods=max(20, n // 4)).std()
    return (s - mu) / sd


def fwd_return(price: pd.Series, h: int) -> pd.Series:
    return price.shift(-h) / price - 1.0


def align(*series: pd.Series) -> tuple[pd.Series, ...]:
    """Inner-join several series on their common DatetimeIndex."""
    df = pd.concat([s.rename(f"_s{i}") for i, s in enumerate(series)], axis=1).dropna()
    return tuple(df[f"_s{i}"] for i in range(len(series)))


# ---------------------------------------------------------------------------
# Position → return application (no look-ahead: position(t-1) * ret(t))
# ---------------------------------------------------------------------------
def apply_position(position: pd.Series, asset_ret: pd.Series) -> pd.Series:
    pos = position.reindex(asset_ret.index).ffill().fillna(0.0)
    return (pos.shift(1).fillna(0.0) * asset_ret).astype(float)


def switching_returns(
    flag_in: pd.Series,
    risky_ret: pd.Series,
    cash_ret: pd.Series | None = None,
) -> pd.Series:
    """flag_in=1 → hold risky asset; 0 → hold cash. flag is shifted by 1."""
    flag = flag_in.reindex(risky_ret.index).ffill().fillna(0.0)
    flag = flag.shift(1).fillna(0.0)
    if cash_ret is None:
        cash_ret = pd.Series(0.0, index=risky_ret.index)
    cash_ret = cash_ret.reindex(risky_ret.index).fillna(0.0)
    return flag * risky_ret + (1.0 - flag) * cash_ret


# ---------------------------------------------------------------------------
# Cash / T-bill proxy
# ---------------------------------------------------------------------------
def cash_ret_from_bil(bil_price: pd.Series, target_index: pd.DatetimeIndex) -> pd.Series:
    """Daily returns of BIL (1-3M T-bill ETF) reindexed to target_index."""
    r = bil_price.pct_change()
    return r.reindex(target_index).fillna(0.0)


def zero_cash(index: pd.DatetimeIndex) -> pd.Series:
    return pd.Series(0.0, index=index)


# ---------------------------------------------------------------------------
# Bucket / quantile forward-return table
# ---------------------------------------------------------------------------
def bucket_fwd_returns(
    signal: pd.Series,
    asset: pd.Series,
    horizons: dict[str, int],
    q: int = 5,
) -> pd.DataFrame:
    """Quintile a signal then average forward returns of the asset over horizons.

    Returns a DataFrame indexed by bucket label, columns = horizons.
    """
    signal = signal.dropna()
    asset = asset.dropna()
    common = signal.index.intersection(asset.index)
    if len(common) < max(horizons.values()) + q * 5:
        return pd.DataFrame()
    sig = signal.loc[common]
    px = asset.loc[common]

    try:
        bucket = pd.qcut(sig.rank(method="first"), q,
                         labels=[f"q{i+1}" for i in range(q)])
    except ValueError:
        return pd.DataFrame()

    out = {}
    for label, h in horizons.items():
        f = fwd_return(px, h)
        df = pd.concat([bucket.rename("bkt"), f.rename("ret")], axis=1).dropna()
        out[label] = df.groupby("bkt", observed=True)["ret"].mean()
    return pd.DataFrame(out)


def threshold_event_fwd_returns(
    flag: pd.Series,
    asset: pd.Series,
    horizons: dict[str, int],
) -> pd.DataFrame:
    """For a boolean event series, compare fwd returns when flag=True vs flag=False."""
    common = flag.index.intersection(asset.index)
    f = flag.reindex(common).fillna(False).astype(bool)
    px = asset.loc[common]
    out = {}
    for label, h in horizons.items():
        r = fwd_return(px, h)
        df = pd.concat([f.rename("flag"), r.rename("ret")], axis=1).dropna()
        if df.empty:
            continue
        out[label] = df.groupby("flag")["ret"].mean()
    res = pd.DataFrame(out)
    if not res.empty:
        res.index = ["flag=False", "flag=True"]
    return res


# ---------------------------------------------------------------------------
# Rebalance scheduling
# ---------------------------------------------------------------------------
def month_end_index(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Trading-day month-end dates within the given index."""
    s = pd.Series(index, index=index)
    return s.groupby([index.year, index.month]).last().values


def monthly_rebalance_weights(
    rets: pd.DataFrame,
    weights_at_month_end: dict,  # ts → {col → weight}
) -> pd.Series:
    """Given monthly target weights at month-end, compute daily portfolio returns.

    weights_at_month_end keys must be drawn from rets.index.
    Weights apply from the NEXT trading day until next rebalance.
    """
    daily_weights = pd.DataFrame(0.0, index=rets.index, columns=rets.columns)
    sorted_dates = sorted(weights_at_month_end)
    for i, d in enumerate(sorted_dates):
        w = weights_at_month_end[d]
        for c, v in w.items():
            if c in daily_weights.columns:
                daily_weights.loc[d:, c] = v
    return (daily_weights.shift(1).fillna(0.0) * rets).sum(axis=1)


def fixed_weight_portfolio(
    rets: pd.DataFrame,
    weights: dict[str, float],
    rebal: str = "YE",  # YE=year-end, ME=month-end, none=continuous
) -> pd.Series:
    """Constant-weight portfolio with periodic rebalancing back to target."""
    rets = rets.dropna(how="all")
    cols = [c for c in weights if c in rets.columns]
    rets = rets[cols].fillna(0.0)
    w_target = np.array([weights[c] for c in cols])
    w_target = w_target / w_target.sum()

    if rebal == "none":
        return (rets * w_target).sum(axis=1)

    # Resample anchor dates — use legacy aliases for pandas < 2.2 compatibility
    alias = {"ME": "M", "YE": "Y", "QE": "Q"}.get(rebal, rebal)
    anchors = rets.resample(alias).last().index

    daily_w = pd.DataFrame(0.0, index=rets.index, columns=cols)
    w = w_target.copy()
    last_idx = None
    for d in rets.index:
        if last_idx is not None:
            # drift
            w = w * (1.0 + rets.loc[d].values)
            w = w / w.sum() if w.sum() > 0 else w_target.copy()
        if d in anchors:
            w = w_target.copy()
        daily_w.loc[d] = w
        last_idx = d
    # portfolio return on day t uses weights at t-1
    daily_w = daily_w.shift(1).fillna(0.0)
    daily_w.iloc[0] = w_target  # initial
    return (daily_w * rets).sum(axis=1)


# ---------------------------------------------------------------------------
# Verdict classification
# ---------------------------------------------------------------------------
def classify_verdict(
    lit: str,
    strat_stats: dict,
    bench_stats: dict,
    direction_check: float | None = None,
) -> tuple[str, str]:
    """Map (literature claim, realized stats) → our_verdict + reason string.

    Heuristic:
      - "robust" lit → confirmed if strat Sharpe within 0.1 of bench AND
        excess CAGR not deeply negative; decayed if much worse; surprise+ if much better.
      - "decayed" lit → confirmed if strat << bench; surprise+ if strat >> bench.
      - "mixed" / "seasonal-window-only" → use excess CAGR sign with wider band.
    """
    ss = strat_stats.get("sharpe") or 0.0
    bs = bench_stats.get("sharpe") or 0.0
    sc = strat_stats.get("cagr") or 0.0
    bc = bench_stats.get("cagr") or 0.0
    sharpe_gap = ss - bs
    cagr_gap = sc - bc
    why = f"strat sharpe {ss:+.2f} vs bench {bs:+.2f} (Δ={sharpe_gap:+.2f}); CAGR Δ={cagr_gap:+.2%}"

    if direction_check is not None:
        why += f"; bucket monotonic ok={direction_check > 0}"

    if lit == "robust":
        if sharpe_gap > 0.20: return "surprise+", why
        if sharpe_gap > -0.10: return "confirmed", why
        if sharpe_gap > -0.40: return "decayed", why
        return "surprise-", why
    if lit in ("robust→decay",):
        if sharpe_gap > 0.10: return "surprise+", why
        if sharpe_gap > -0.20: return "confirmed", why
        return "decayed", why
    if lit == "decayed":
        if sharpe_gap > 0.20: return "surprise+", why
        return "confirmed", why
    if lit == "seasonal-window-only":
        if sharpe_gap > 0.10: return "confirmed", why
        if sharpe_gap > -0.20: return "null", why
        return "surprise-", why
    # mixed or unknown
    if sharpe_gap > 0.20: return "surprise+", why
    if sharpe_gap > -0.20: return "null", why
    return "decayed", why


# ---------------------------------------------------------------------------
# Monotonicity score for bucket tables (used to flag clean signal vs noise)
# ---------------------------------------------------------------------------
def bucket_monotonicity(buckets: pd.DataFrame) -> float:
    """Rank-correlation between bucket order and mean forward return (avg over horizons).
    +1 perfect monotonic up; -1 perfect monotonic down; 0 noise.
    """
    if buckets is None or buckets.empty:
        return 0.0
    means = buckets.mean(axis=1)
    if means.isna().all():
        return 0.0
    order = pd.Series(range(len(means)), index=means.index)
    return float(order.corr(means, method="spearman") or 0.0)
