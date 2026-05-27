"""Shared utilities for every idea script: loader, plot helpers, backtest stats."""
from __future__ import annotations

import pathlib
import sys
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "finance-data-api"))

from storage import Storage  # noqa: E402
from universe import UNIVERSE, by_key  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

storage = Storage()


# -----------------------------------------------------------------------------
# Loaders
# -----------------------------------------------------------------------------
def load_price(key: str, col: str = "close") -> pd.Series:
    df = storage.load("prices", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"prices/{key} not in cache")
    if col not in df.columns:
        # gracefully fall back if 'latest'/'close'
        for fallback in ("close", "adj_close", "latest"):
            if fallback in df.columns:
                col = fallback
                break
    return df[col].dropna().astype(float)


def load_nav(key: str) -> pd.Series:
    df = storage.load("nav", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"nav/{key} not in cache")
    return df["nav"].dropna().astype(float)


def load_macro(key: str) -> pd.DataFrame:
    df = storage.load("macro", key)
    if df is None:
        raise FileNotFoundError(f"macro/{key} not in cache")
    return df


# -----------------------------------------------------------------------------
# Returns & backtest helpers
# -----------------------------------------------------------------------------
def forward_return(series: pd.Series, horizon: int) -> pd.Series:
    """Forward total return over `horizon` trading days (price t+h / price t - 1)."""
    return series.shift(-horizon) / series - 1.0


def signal_summary(signal: pd.Series, fwd_ret: pd.Series, baseline: pd.Series,
                   label: str) -> dict:
    """Compare conditional forward return when `signal` is True vs unconditional.

    Returns a dict with hit-rate and mean/median return.
    """
    mask = signal.reindex(fwd_ret.index).fillna(False).astype(bool)
    sub = fwd_ret[mask].dropna()
    base = baseline.dropna()
    n = len(sub)
    if n == 0:
        return {"label": label, "n": 0, "mean": np.nan, "median": np.nan,
                "win_rate": np.nan, "base_mean": base.mean() if len(base) else np.nan}
    return {
        "label": label,
        "n": n,
        "mean": sub.mean(),
        "median": sub.median(),
        "win_rate": (sub > 0).mean(),
        "base_mean": base.mean(),
        "base_win_rate": (base > 0).mean(),
    }


def equity_curve(returns: pd.Series) -> pd.Series:
    return (1.0 + returns.fillna(0)).cumprod()


def strategy_stats(daily_ret: pd.Series, name: str) -> dict:
    daily_ret = daily_ret.dropna()
    if daily_ret.empty:
        return {"name": name, "cagr": np.nan, "sharpe": np.nan, "maxdd": np.nan,
                "total": np.nan, "n_days": 0}
    eq = equity_curve(daily_ret)
    years = len(daily_ret) / 252.0
    cagr = eq.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    sharpe = daily_ret.mean() / daily_ret.std() * np.sqrt(252) if daily_ret.std() > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    return {
        "name": name,
        "n_days": len(daily_ret),
        "total": eq.iloc[-1] - 1,
        "cagr": cagr,
        "sharpe": sharpe,
        "maxdd": dd,
    }


# -----------------------------------------------------------------------------
# Plot helper
# -----------------------------------------------------------------------------
def setup_axes(figsize=(11, 5)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "figure.figsize": figsize,
        "axes.grid": True,
        "grid.alpha": 0.3,
    })
    return plt


def save_fig(name: str) -> pathlib.Path:
    p = OUT / f"{name}.png"
    plt.tight_layout()
    plt.savefig(p, dpi=130)
    plt.close()
    return p


def write_report(idea_id: str, lines: list[str]) -> pathlib.Path:
    p = OUT / f"{idea_id}_report.md"
    p.write_text("\n".join(lines))
    return p
