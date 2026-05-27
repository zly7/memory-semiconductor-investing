"""Idea 08 — 北向资金近 N 日累计净流入 → A 股短线信号.

Hypothesis: when 20-day cumulative northbound net inflow is in the highest
quintile (HK-via-Shanghai/Shenzhen Connect is buying CN A-shares), forward CSI300
returns are above average.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, load_macro, forward_return, setup_axes,
                    save_fig, write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    try:
        nf = load_macro("NORTH_FLOW")
    except FileNotFoundError:
        write_report("idea08", [
            "# Idea 08 — Northbound flow",
            "",
            "Northbound flow series was not retrievable from akshare endpoints",
            "in this environment. Skipping. The daily snapshot can be added to",
            "the dashboard via fetchers.fetch_ak_north_flow when the endpoint",
            "stabilizes.",
        ])
        print("idea08 skipped — northbound flow unavailable")
        return

    # Heuristically pick the daily net-flow scalar column
    candidates = [
        "当日成交净买额", "当日资金流入", "北向资金", "净买额", "资金净流入",
        "当日成交净买额-沪股通", "value", "net_flow",
    ]
    col = next((c for c in candidates if c in nf.columns), None)
    if col is None:
        col = nf.select_dtypes(include="number").columns[0]
    flow = nf[col].dropna().astype(float)
    # Convert to billions if it's in 1e8 元 (东方财富 default) -> visualization only
    cum20 = flow.rolling(20).sum()

    a = load_price("ETF510300").reindex(flow.index).ffill().dropna()
    idx = cum20.index.intersection(a.index)
    cum20 = cum20.loc[idx]; a = a.loc[idx]

    fwd20 = forward_return(a, 20)
    fwd60 = forward_return(a, 60)
    rk = cum20.rank(pct=True)
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ["q1 outflow", "q2", "q3", "q4", "q5 inflow"]
    cat = pd.cut(rk, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd20_mean": fwd20.groupby(cat, observed=True).mean(),
        "fwd60_mean": fwd60.groupby(cat, observed=True).mean(),
        "fwd60_win": fwd60.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    # Strategy: long 沪深300 ETF when 20d cum flow > 0; flat otherwise
    pos = (cum20 > 0).astype(float)
    daily = a.pct_change().fillna(0)
    strat = (pos.shift(1) * daily).fillna(0)
    bh = strategy_stats(daily, "510300 buy & hold")
    s = strategy_stats(strat, "510300 long when 20d north-flow positive")

    fig, axL = plt.subplots(figsize=(12, 5))
    axR = axL.twinx()
    cum20.plot(ax=axL, color="tab:purple", label="20d cumulative N-flow", lw=0.8)
    a.plot(ax=axR, color="tab:gray", label="510300", lw=0.7)
    axL.axhline(0, color="black", lw=0.5)
    axL.legend(loc="upper left"); axR.legend(loc="upper right")
    axL.set_title("Northbound 20d cumulative flow vs 沪深300ETF")
    save_fig("idea08_flow")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd20_mean", "fwd60_mean"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Forward 510300 return by 20d N-flow percentile")
    save_fig("idea08_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=s["name"])
    ax.legend(); ax.set_title("Northbound-tilt vs buy-and-hold")
    save_fig("idea08_equity")

    report = [
        "# Idea 08 — Northbound flow → 沪深300 signal",
        f"Latest 20d cumulative flow: {cum20.iloc[-1]:,.2f}",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, s]).round(4).to_markdown(index=False),
    ]
    write_report("idea08", report)
    print(bucket.round(4))


if __name__ == "__main__":
    main()
