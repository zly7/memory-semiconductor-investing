"""Idea 05 — DXY 拐点 → 新兴市场反弹.

Strong-dollar regimes are headwinds for EM equities (capital flight, USD-debt
servicing cost). When DXY 6-month % change is in the lowest quartile (weakening
USD), EEM tends to outperform.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    dxy = load_price("DXY")
    eem = load_price("EEM")
    idx = dxy.index.intersection(eem.index)
    dxy, eem = dxy.loc[idx], eem.loc[idx]

    dxy_chg6m = dxy / dxy.shift(126) - 1
    fwd60 = forward_return(eem, 60)
    fwd120 = forward_return(eem, 120)

    bins = [-np.inf, -0.05, -0.02, 0.02, 0.05, np.inf]
    labels = ["<-5%", "-5..-2%", "-2..2%", "2..5%", ">5%"]
    cat = pd.cut(dxy_chg6m, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd60_mean": fwd60.groupby(cat, observed=True).mean(),
        "fwd120_mean": fwd120.groupby(cat, observed=True).mean(),
        "fwd120_win": fwd120.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    daily = eem.pct_change().fillna(0)
    pos = pd.Series(1.0, index=dxy.index)
    pos[dxy_chg6m < -0.05] = 1.5   # USD weakening fast → overweight EM
    pos[dxy_chg6m > 0.05] = 0.5    # USD strengthening fast → underweight
    strat = (pos.shift(1) * daily).fillna(0)
    bh = strategy_stats(daily, "EEM buy & hold")
    s = strategy_stats(strat, "EEM with DXY-6m tilt")

    fig, axL = plt.subplots(figsize=(12, 5))
    axR = axL.twinx()
    dxy.plot(ax=axL, color="tab:blue", label="DXY", lw=0.7)
    eem.plot(ax=axR, color="tab:orange", label="EEM", lw=0.7)
    axL.set_ylabel("DXY"); axR.set_ylabel("EEM")
    axL.set_title("DXY vs EEM")
    axL.legend(loc="upper left"); axR.legend(loc="upper right")
    save_fig("idea05_dxy_eem")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd60_mean", "fwd120_mean"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Mean forward EEM return by DXY 6-month change bucket")
    save_fig("idea05_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=s["name"])
    ax.legend(); ax.set_title("EEM tilt vs buy & hold")
    save_fig("idea05_equity")

    report = [
        "# Idea 05 — DXY 6-month change as EM tilt",
        f"Latest DXY {dxy.iloc[-1]:.2f}, 6m change {dxy_chg6m.iloc[-1]*100:.2f}%",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, s]).round(4).to_markdown(index=False),
    ]
    write_report("idea05", report)
    print(bucket.round(4))


if __name__ == "__main__":
    main()
