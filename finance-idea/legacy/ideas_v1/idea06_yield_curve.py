"""Idea 06 — US 收益率曲线 (10Y - 3M) 倒挂后买入.

The 10Y-3M spread inversion has preceded every US recession since 1969.
But entering equities AT inversion is too early; the historical pattern is:
inversion → market peak some months later → recession.

We test a less obvious twist: enter SPY when the spread *re-steepens* through
zero (the un-inversion), which is closer to the actual recession bottom.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    tnx = load_price("TNX") / 10.0   # yfinance reports yields x10
    irx = load_price("IRX") / 10.0
    spy = load_price("SPY")
    idx = tnx.index.intersection(irx.index).intersection(spy.index)
    tnx, irx, spy = tnx.loc[idx], irx.loc[idx], spy.loc[idx]
    spread = tnx - irx
    spread = spread.dropna()

    # Identify inversion regimes
    inverted = spread < 0
    # Re-steepening = inverted yesterday, not inverted today
    re_steep = (inverted.shift(1).fillna(False)) & (~inverted)

    fwd60 = forward_return(spy, 60)
    fwd252 = forward_return(spy, 252)
    cond60 = fwd60[re_steep]
    cond252 = fwd252[re_steep]

    daily = spy.pct_change().fillna(0)
    # Strategy: long SPY normally; cut to 50% when inverted
    pos = pd.Series(1.0, index=spread.index)
    pos[inverted] = 0.5
    strat_def = (pos.shift(1) * daily).fillna(0)
    bh = strategy_stats(daily, "SPY buy & hold")
    s_def = strategy_stats(strat_def, "Defensive: half SPY when inverted")

    fig, axL = plt.subplots(figsize=(12, 5))
    axR = axL.twinx()
    spread.plot(ax=axL, color="tab:blue", label="10Y-3M", lw=0.8)
    axL.axhline(0, color="red", ls="--", lw=0.7)
    axL.fill_between(spread.index, spread.min(), spread.max(), where=inverted,
                     color="red", alpha=0.1, label="inverted")
    spy.plot(ax=axR, color="tab:gray", lw=0.7, label="SPY")
    axL.set_title("US 10Y-3M spread vs SPY (red shading = inversion)")
    axL.legend(loc="upper left"); axR.legend(loc="upper right")
    save_fig("idea06_curve")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat_def).plot(ax=ax, label=s_def["name"])
    ax.legend()
    ax.set_title("SPY — defensive overlay during yield-curve inversion")
    save_fig("idea06_equity")

    report = [
        "# Idea 06 — Yield curve (10Y-3M) inversion / re-steepen",
        f"Latest spread {spread.iloc[-1]:.2f}%  inverted={inverted.iloc[-1]}",
        f"Number of re-steepening events in sample: {int(re_steep.sum())}",
        f"Mean fwd60 SPY after re-steepen: {cond60.mean():.4f}  vs base {fwd60.mean():.4f}",
        f"Mean fwd252 SPY after re-steepen: {cond252.mean():.4f} vs base {fwd252.mean():.4f}",
        "",
        pd.DataFrame([bh, s_def]).round(4).to_markdown(index=False),
    ]
    write_report("idea06", report)
    print(f"Inverted={inverted.iloc[-1]}, spread={spread.iloc[-1]:.2f}")
    print(pd.DataFrame([bh, s_def]).round(4))


if __name__ == "__main__":
    main()
