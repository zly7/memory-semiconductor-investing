"""Idea 07 — 恒生 AH 溢价指数极值切换.

When the AH premium index is high (A trades >> H), expected forward
relative-performance favors H over A (mean reversion of the cross-listing
gap). When the index is low, expected favors A.

Falls back gracefully if the AH premium history is not in cache.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, load_macro, forward_return, setup_axes,
                    save_fig, write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    try:
        ah = load_macro("AH_PREMIUM")
    except FileNotFoundError:
        write_report("idea07", [
            "# Idea 07 — AH premium",
            "",
            "AH premium index history was not retrievable through the current",
            "akshare endpoints in this environment. Skipping idea-07 backtest;",
            "the daily live snapshot can still be obtained via the dashboard.",
        ])
        print("idea07 skipped — AH premium history unavailable")
        return

    # Pick the AH-premium scalar column heuristically.
    col = None
    for cand in ("ah_premium", "AH_index", "close", "ahindex"):
        if cand in ah.columns:
            col = cand; break
    if col is None:
        col = ah.select_dtypes(include="number").columns[0]
    s_ah = ah[col].dropna().astype(float)

    # Compare A vs H via CSI300 ETF (510300) and H-share ETF (510900)
    a_etf = "ETF510300"
    h_etf = "ETF510900"
    try:
        a = load_macro_or_price(a_etf)
        h = load_macro_or_price(h_etf)
    except Exception:
        from common import load_price as _lp
        a = _lp(a_etf); h = _lp(h_etf)

    idx = s_ah.index.intersection(a.index).intersection(h.index)
    s_ah = s_ah.loc[idx]
    a, h = a.loc[idx], h.loc[idx]

    rel = a / h   # rises when A outperforms H
    fwd60_a = forward_return(a, 60)
    fwd60_h = forward_return(h, 60)
    diff60 = fwd60_a - fwd60_h

    # bucket by AH percentile
    rk = s_ah.rank(pct=True)
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ["q1 (lowest)", "q2", "q3", "q4", "q5 (highest)"]
    cat = pd.cut(rk, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd60_A": fwd60_a.groupby(cat, observed=True).mean(),
        "fwd60_H": fwd60_h.groupby(cat, observed=True).mean(),
        "A_minus_H_60d": diff60.groupby(cat, observed=True).mean(),
    }).reindex(labels)

    fig, axL = plt.subplots(figsize=(12, 5))
    s_ah.plot(ax=axL, color="tab:red", label="AH premium index", lw=0.8)
    axL.set_title("Hang Seng AH premium index")
    save_fig("idea07_ah")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd60_A", "fwd60_H", "A_minus_H_60d"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Forward 60d return by AH-premium percentile")
    save_fig("idea07_buckets")

    report = [
        "# Idea 07 — AH premium reversal",
        f"Latest AH premium ({col}): {s_ah.iloc[-1]:.2f}",
        "",
        bucket.round(4).to_markdown(),
    ]
    write_report("idea07", report)
    print(bucket.round(4))


def load_macro_or_price(key):
    from common import load_price
    return load_price(key)


if __name__ == "__main__":
    main()
