"""Idea 03 — VIX 极值 → SPY 反向信号.

When VIX > 30: panic, expected forward SPY return is positive (buy-the-fear).
When VIX < 13: complacency, forward returns more muted, larger left-tail risk.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    vix = load_price("VIX")
    spy = load_price("SPY")
    idx = spy.index.intersection(vix.index)
    vix = vix.loc[idx]
    spy = spy.loc[idx]

    fwd5 = forward_return(spy, 5)
    fwd20 = forward_return(spy, 20)
    fwd60 = forward_return(spy, 60)

    bins = [0, 13, 17, 22, 30, 200]
    labels = ["<13 (calm)", "13-17", "17-22", "22-30", ">30 (panic)"]
    cat = pd.cut(vix, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd5_mean": fwd5.groupby(cat, observed=True).mean(),
        "fwd20_mean": fwd20.groupby(cat, observed=True).mean(),
        "fwd60_mean": fwd60.groupby(cat, observed=True).mean(),
        "fwd20_win": fwd20.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    # Strategy: long SPY normally; double-leverage (cap at +1 for chart) when VIX>30; flat when VIX<13.
    pos = pd.Series(1.0, index=vix.index)
    pos[vix > 30] = 1.5
    pos[vix < 13] = 0.5
    daily = spy.pct_change().fillna(0)
    strat = (pos.shift(1) * daily).fillna(0)
    bh = strategy_stats(daily, "SPY buy & hold")
    s = strategy_stats(strat, "VIX-tilted SPY (1.5/0.5/1.0)")

    fig, ax = plt.subplots(figsize=(12, 5))
    vix.plot(ax=ax, color="tab:red", lw=0.8)
    ax.axhline(30, color="red", ls="--", lw=0.7)
    ax.axhline(13, color="blue", ls="--", lw=0.7)
    ax.set_title("VIX history (red=>30 panic, blue=<13 calm)")
    save_fig("idea03_vix")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd5_mean", "fwd20_mean", "fwd60_mean"]].plot.bar(ax=ax)
    ax.set_title("Mean forward SPY return by VIX bucket")
    ax.axhline(0, color="black", lw=0.5)
    save_fig("idea03_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=s["name"])
    ax.legend()
    ax.set_title("VIX-tilt vs buy & hold")
    save_fig("idea03_equity")

    report = [
        "# Idea 03 — VIX extremes as SPY contrarian signal",
        "",
        f"Latest VIX {vix.iloc[-1]:.2f} on {vix.index[-1].date()}",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, s]).round(4).to_markdown(index=False),
    ]
    write_report("idea03", report)
    print(bucket.round(4))
    print(pd.DataFrame([bh, s]).round(4))


if __name__ == "__main__":
    main()
