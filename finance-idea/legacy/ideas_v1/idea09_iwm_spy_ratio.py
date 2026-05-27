"""Idea 09 — IWM/SPY 小盘相对强度作为风险偏好指标.

When IWM/SPY ratio breaks DOWN (small caps underperform), risk appetite is
deteriorating. We test whether reduced equity exposure during these regimes
improves drawdown without giving up too much return; and whether ratio
contraction extremes precede mean-reverting outperformance.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    iwm = load_price("IWM")
    spy = load_price("SPY")
    idx = iwm.index.intersection(spy.index)
    iwm, spy = iwm.loc[idx], spy.loc[idx]
    ratio = iwm / spy
    # z-score 252d
    z = (ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()

    fwd60_iwm = forward_return(iwm, 60)
    fwd60_spy = forward_return(spy, 60)
    diff60 = fwd60_iwm - fwd60_spy

    bins = [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf]
    labels = ["z<-1.5", "-1.5..-0.5", "-0.5..0.5", "0.5..1.5", "z>1.5"]
    cat = pd.cut(z, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd60_IWM": fwd60_iwm.groupby(cat, observed=True).mean(),
        "fwd60_SPY": fwd60_spy.groupby(cat, observed=True).mean(),
        "IWM_minus_SPY_60d": diff60.groupby(cat, observed=True).mean(),
    }).reindex(labels)

    # Strategy: rotate SPY/IWM by ratio momentum (12w SMA crossover)
    sma12w = ratio.rolling(60).mean()
    long_iwm = (ratio > sma12w).astype(float)   # small leads → ride IWM
    long_spy = 1.0 - long_iwm
    daily_iwm = iwm.pct_change().fillna(0)
    daily_spy = spy.pct_change().fillna(0)
    strat = (long_iwm.shift(1) * daily_iwm + long_spy.shift(1) * daily_spy).fillna(0)
    bh = strategy_stats((daily_iwm + daily_spy) / 2, "50/50 SPY+IWM")
    s = strategy_stats(strat, "Rotate SPY/IWM by IWM/SPY momentum")

    fig, ax = plt.subplots(figsize=(12, 5))
    ratio.plot(ax=ax, color="teal", lw=0.8)
    sma12w.plot(ax=ax, color="tab:orange", lw=0.7, label="60d SMA")
    ax.set_title("IWM/SPY ratio")
    ax.legend()
    save_fig("idea09_ratio")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd60_IWM", "fwd60_SPY", "IWM_minus_SPY_60d"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Forward 60d return by IWM/SPY z-bucket")
    save_fig("idea09_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve((daily_iwm + daily_spy) / 2).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=s["name"])
    ax.legend()
    ax.set_title("IWM/SPY rotation vs 50/50")
    save_fig("idea09_equity")

    report = [
        "# Idea 09 — IWM/SPY relative strength",
        f"Latest ratio {ratio.iloc[-1]:.4f}, z={z.iloc[-1]:.2f}",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, s]).round(4).to_markdown(index=False),
    ]
    write_report("idea09", report)
    print(bucket.round(4))


if __name__ == "__main__":
    main()
