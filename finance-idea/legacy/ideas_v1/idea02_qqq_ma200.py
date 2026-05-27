"""Idea 02 — Buy QQQ when it closes below its 200-day moving average.

Classical mean-reversion / buy-the-dip setup. The user prompt called out the
250-day variant for A-shares; the US-equity analog people quote is the 200-day
SMA on QQQ.

Test
----
- Two strategies are simulated:
    * Naive: always hold QQQ
    * "BelowMA200": fully invested only when close[t] <= SMA200[t-1].
      Cash otherwise.
- Compare CAGR / Sharpe / max DD.
- Also bucket forward 20/60-day returns by close/SMA200 ratio.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    qqq = load_price("QQQ").asfreq("B").ffill()
    sma200 = qqq.rolling(200).mean()
    ratio = qqq / sma200

    # Strategy A: always invested
    daily = qqq.pct_change().fillna(0)
    bh = strategy_stats(daily, "QQQ buy & hold")

    # Strategy B: invested when below MA200 (mean reversion)
    pos_below = (ratio.shift(1) <= 1).astype(float)
    strat_below = (pos_below * daily).fillna(0)
    below_stats = strategy_stats(strat_below, "Long only when close ≤ SMA200")

    # Strategy C (sanity): invested when ABOVE MA200 (trend following)
    pos_above = (ratio.shift(1) > 1).astype(float)
    strat_above = (pos_above * daily).fillna(0)
    above_stats = strategy_stats(strat_above, "Long only when close > SMA200")

    fwd20 = forward_return(qqq, 20)
    fwd60 = forward_return(qqq, 60)
    bins = [-np.inf, 0.85, 0.95, 1.0, 1.05, 1.15, np.inf]
    labels = ["≤0.85", "0.85-0.95", "0.95-1.00", "1.00-1.05", "1.05-1.15", ">1.15"]
    cat = pd.cut(ratio, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd20_mean": fwd20.groupby(cat, observed=True).mean(),
        "fwd60_mean": fwd60.groupby(cat, observed=True).mean(),
        "fwd60_win": fwd60.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    # Plot price vs MA200
    fig, ax = plt.subplots(figsize=(12, 5))
    qqq.plot(ax=ax, label="QQQ close", lw=0.8)
    sma200.plot(ax=ax, label="SMA200", lw=0.8, color="tab:orange")
    below_mask = ratio <= 1
    ax.fill_between(qqq.index, qqq.min(), qqq.max(), where=below_mask,
                    color="red", alpha=0.08, label="below SMA200")
    ax.set_title("QQQ vs 200d SMA — buy-the-dip regime shaded")
    ax.legend()
    save_fig("idea02_qqq_ma200")

    # Equity curves
    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label="buy & hold")
    equity_curve(strat_below).plot(ax=ax, label="long below SMA200")
    equity_curve(strat_above).plot(ax=ax, label="long above SMA200")
    ax.set_title("QQQ — equity curves comparing regime overlays")
    ax.legend()
    save_fig("idea02_equity")

    report = [
        "# Idea 02 — Buy QQQ when below its 200-day SMA",
        "",
        f"Latest QQQ {qqq.iloc[-1]:.2f}, SMA200 {sma200.iloc[-1]:.2f}, ratio {ratio.iloc[-1]:.3f}",
        "Below-SMA regime currently active." if ratio.iloc[-1] <= 1 else "Above-SMA regime currently active.",
        "",
        "## Forward return by close/SMA200 ratio bucket",
        bucket.round(4).to_markdown(),
        "",
        "## Strategy stats",
        pd.DataFrame([bh, below_stats, above_stats]).round(4).to_markdown(index=False),
        "",
        "Read-out: buy-the-dip generally underperforms buy-and-hold over the full",
        "sample (you miss the strongest trend days), but its **per-day-invested**",
        "return is informative for tactical sizing.",
    ]
    write_report("idea02", report)
    print(bucket.round(4))
    print(pd.DataFrame([bh, below_stats, above_stats]).round(4))


if __name__ == "__main__":
    main()
