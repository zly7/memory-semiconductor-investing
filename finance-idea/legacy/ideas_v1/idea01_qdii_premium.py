"""Idea 01 — 国内 QDII ETF 溢价率作为美股情绪反指.

Hypothesis
----------
When CN-listed QDII ETFs (Nasdaq/S&P trackers like 513100, 513500, 159941) trade
at a *large* premium over their NAV, it reflects retail FOMO toward US equities
and is often a SHORT-term contrarian signal: forward QQQ returns over the next
1–4 weeks are below average. Symmetric: when premium is unusually low/negative,
it tends to mark short-term capitulation lows.

Test
----
1. For each QDII ETF: premium_pct[t] = (close[t] - nav[t]) / nav[t] * 100
2. Take the cross-sectional median premium across all Nasdaq trackers — call it
   the "QDII Nasdaq premium" sentiment index.
3. Bucket the index by percentile, look at forward 5/20-day QQQ returns.
4. Plot premium time series and conditional-return chart.
5. Simulate a tactical strategy: stay long QQQ, but flatten when premium is
   above the 90th percentile (reset on close); compare vs buy-and-hold.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, load_nav, forward_return, setup_axes,
                    save_fig, write_report, signal_summary, strategy_stats,
                    equity_curve)

NASDAQ_QDII = ["QDII513100", "QDII513300", "QDII159941"]


def build_premium() -> pd.DataFrame:
    rows = {}
    for key in NASDAQ_QDII:
        try:
            price = load_price(key)
            nav = load_nav(key)
        except FileNotFoundError:
            continue
        df = pd.concat([price.rename("price"), nav.rename("nav")], axis=1).dropna()
        # NAV is published EOD; align by date — premium is closing premium.
        df["premium"] = (df["price"] - df["nav"]) / df["nav"] * 100
        rows[key] = df["premium"]
    premium_df = pd.DataFrame(rows)
    premium_df["median_premium"] = premium_df.median(axis=1)
    return premium_df


def main():
    plt = setup_axes()
    premium_df = build_premium()
    qqq = load_price("QQQ")
    # Align onto QDII trading calendar (CN business days)
    sentiment = premium_df["median_premium"].dropna()
    # QQQ aligned to following trading day (since the CN premium today reflects
    # yesterday's US close + today's CN frenzy → forward signal):
    qqq_resampled = qqq.reindex(sentiment.index, method="nearest")

    fwd5 = forward_return(qqq_resampled, 5).dropna()
    fwd20 = forward_return(qqq_resampled, 20).dropna()

    base5 = forward_return(qqq, 5).dropna()
    base20 = forward_return(qqq, 20).dropna()

    # Percentile buckets
    rank = sentiment.rank(pct=True)
    buckets = pd.cut(rank, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                     labels=["q1 (lowest 20%)", "q2", "q3", "q4", "q5 (top 20%)"])
    bucket_table = pd.DataFrame({
        "fwd_5d_mean": fwd5.groupby(buckets, observed=True).mean(),
        "fwd_5d_winrate": fwd5.groupby(buckets, observed=True).apply(lambda x: (x > 0).mean()),
        "fwd_20d_mean": fwd20.groupby(buckets, observed=True).mean(),
        "fwd_20d_winrate": fwd20.groupby(buckets, observed=True).apply(lambda x: (x > 0).mean()),
        "n_samples": fwd5.groupby(buckets, observed=True).size(),
    })

    # Strategy: flatten QQQ when premium > 90th percentile rolling
    p90 = sentiment.expanding(252).quantile(0.90)
    p10 = sentiment.expanding(252).quantile(0.10)
    risk_off = (sentiment > p90).astype(int)
    risk_on = (sentiment < p10).astype(int)
    # Position: -1 risk-off (cash), +1 normal; on top of buy-and-hold
    pos = pd.Series(1.0, index=sentiment.index)
    pos[risk_off == 1] = 0.0
    qqq_aligned = qqq.reindex(sentiment.index).ffill()
    daily_ret = qqq_aligned.pct_change().fillna(0)
    strat_ret = (pos.shift(1) * daily_ret).fillna(0)

    bh = strategy_stats(daily_ret, "QQQ buy & hold")
    strat = strategy_stats(strat_ret, "QQQ + QDII-premium flatten signal")

    # ---- Plot 1: premium time series with QQQ overlay
    fig, axL = plt.subplots(figsize=(12, 6))
    axR = axL.twinx()
    sentiment.plot(ax=axL, label="QDII Nasdaq median premium %", color="tab:red", lw=1.0)
    p90.plot(ax=axL, color="tab:red", ls=":", lw=0.8, label="rolling 90th pct")
    p10.plot(ax=axL, color="tab:blue", ls=":", lw=0.8, label="rolling 10th pct")
    qqq_aligned.plot(ax=axR, color="tab:gray", lw=0.8, label="QQQ close (rhs)")
    axL.axhline(0, color="black", lw=0.5)
    axL.set_ylabel("Premium %")
    axR.set_ylabel("QQQ")
    axL.set_title("QDII Nasdaq ETF premium vs QQQ")
    axL.legend(loc="upper left", fontsize=8)
    axR.legend(loc="upper right", fontsize=8)
    save_fig("idea01_premium_vs_qqq")

    # ---- Plot 2: bucket forward returns
    fig, ax = plt.subplots(figsize=(9, 5))
    bucket_table[["fwd_5d_mean", "fwd_20d_mean"]].plot.bar(ax=ax)
    ax.set_title("Mean forward QQQ return by QDII-premium quintile")
    ax.set_ylabel("Forward return")
    ax.axhline(0, color="black", lw=0.5)
    save_fig("idea01_buckets")

    # ---- Plot 3: equity curve
    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily_ret).plot(ax=ax, label=bh["name"])
    equity_curve(strat_ret).plot(ax=ax, label=strat["name"])
    ax.set_title("Equity curves: buy-and-hold vs premium-flatten")
    ax.legend()
    save_fig("idea01_equity")

    report = [
        "# Idea 01 — QDII (Nasdaq) ETF Premium as Contrarian Signal for QQQ",
        "",
        f"QDII funds used: {', '.join(NASDAQ_QDII)}",
        f"Observations: {len(sentiment)}  range {sentiment.index.min().date()} → {sentiment.index.max().date()}",
        f"Latest premium: {sentiment.iloc[-1]:.2f}% on {sentiment.index[-1].date()}",
        f"Latest 90th-pct threshold: {p90.iloc[-1]:.2f}%   10th-pct: {p10.iloc[-1]:.2f}%",
        "",
        "## Quintile conditional forward returns (QQQ)",
        bucket_table.round(4).to_markdown(),
        "",
        "## Strategy stats (flatten when premium > rolling 90th pct)",
        pd.DataFrame([bh, strat]).round(4).to_markdown(index=False),
        "",
        "Reading: if `fwd_5d_mean` falls as the quintile rises (q1 highest,",
        "q5 lowest), the contrarian premise holds.",
    ]
    write_report("idea01", report)
    print("idea01 done.")
    print(bucket_table.round(4))
    print(pd.DataFrame([bh, strat]).round(4))


if __name__ == "__main__":
    main()
