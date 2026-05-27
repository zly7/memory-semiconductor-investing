"""Idea 04 — Gold/Copper ratio as risk-off barometer.

Hypothesis: spikes in gold/copper indicate risk-off (industrial demand fear,
flight to safety) and predict weaker forward equity returns. Mean reversion in
the ratio precedes equity rebounds.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    gold = load_price("GC")
    copper = load_price("HG")
    spy = load_price("SPY")
    idx = gold.index.intersection(copper.index).intersection(spy.index)
    g, c, s = gold.loc[idx], copper.loc[idx], spy.loc[idx]
    ratio = g / c  # gold/copper

    # Z-score (rolling 252d)
    z = (ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()

    fwd20 = forward_return(s, 20)
    fwd60 = forward_return(s, 60)

    bins = [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf]
    labels = ["z<-1.5", "-1.5..-0.5", "-0.5..0.5", "0.5..1.5", "z>1.5"]
    cat = pd.cut(z, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd20_mean": fwd20.groupby(cat, observed=True).mean(),
        "fwd60_mean": fwd60.groupby(cat, observed=True).mean(),
        "fwd60_win": fwd60.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    # Strategy: when z > 1.5 buy SPY (oversold equities), when z < -1.5 reduce
    daily = s.pct_change().fillna(0)
    pos = pd.Series(1.0, index=z.index)
    pos[z > 1.5] = 1.25
    pos[z < -1.5] = 0.75
    strat = (pos.shift(1) * daily).fillna(0)

    bh = strategy_stats(daily, "SPY buy & hold")
    st = strategy_stats(strat, "SPY with Gold/Copper tilt")

    fig, ax = plt.subplots(figsize=(12, 5))
    ratio.plot(ax=ax, color="tab:olive", lw=0.8)
    ax.set_title("Gold/Copper ratio (GC=F / HG=F)")
    save_fig("idea04_ratio")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd20_mean", "fwd60_mean"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Forward SPY return by Gold/Copper z-bucket")
    save_fig("idea04_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=st["name"])
    ax.legend()
    ax.set_title("Equity curves")
    save_fig("idea04_equity")

    report = [
        "# Idea 04 — Gold/Copper ratio risk barometer",
        f"Latest ratio: {ratio.iloc[-1]:.2f}  z-score: {z.iloc[-1]:.2f}",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, st]).round(4).to_markdown(index=False),
    ]
    write_report("idea04", report)
    print(bucket.round(4))


if __name__ == "__main__":
    main()
