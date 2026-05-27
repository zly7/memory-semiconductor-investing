"""Idea 10 — BTC/Gold ratio 作为风险情绪温度计.

BTC has matured into the canonical risk-on asset; Gold is the canonical
risk-off store of value. Their ratio is sentiment-rich:
  - rapid spikes → speculative euphoria → forward equity returns muted
  - rapid drawdowns of the ratio → flight-to-safety → potential mean revert
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import (load_price, forward_return, setup_axes, save_fig,
                    write_report, strategy_stats, equity_curve)


def main():
    plt = setup_axes()
    btc = load_price("BTC")
    gold = load_price("GLD")
    spy = load_price("SPY")
    idx = btc.index.intersection(gold.index).intersection(spy.index)
    btc, gold, spy = btc.loc[idx], gold.loc[idx], spy.loc[idx]

    ratio = btc / gold
    log_ratio = np.log(ratio)
    z = (log_ratio - log_ratio.rolling(252).mean()) / log_ratio.rolling(252).std()

    fwd60 = forward_return(spy, 60)
    fwd120 = forward_return(spy, 120)
    bins = [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf]
    labels = ["z<-1.5 fear", "-1.5..-0.5", "-0.5..0.5", "0.5..1.5", "z>1.5 euphoria"]
    cat = pd.cut(z, bins=bins, labels=labels)
    bucket = pd.DataFrame({
        "n": cat.value_counts(),
        "fwd60_SPY": fwd60.groupby(cat, observed=True).mean(),
        "fwd120_SPY": fwd120.groupby(cat, observed=True).mean(),
        "fwd120_win": fwd120.groupby(cat, observed=True).apply(lambda x: (x > 0).mean()),
    }).reindex(labels)

    # Strategy: SPY tilt when BTC/Gold euphoria/fear
    daily = spy.pct_change().fillna(0)
    pos = pd.Series(1.0, index=z.index)
    pos[z > 1.5] = 0.75
    pos[z < -1.5] = 1.25
    strat = (pos.shift(1) * daily).fillna(0)
    bh = strategy_stats(daily, "SPY buy & hold")
    s = strategy_stats(strat, "SPY with BTC/Gold z-tilt")

    fig, axL = plt.subplots(figsize=(12, 5))
    axR = axL.twinx()
    log_ratio.plot(ax=axL, color="tab:purple", lw=0.8, label="ln(BTC/GLD)")
    z.plot(ax=axR, color="tab:red", lw=0.7, label="z-score")
    axR.axhline(1.5, color="red", ls=":")
    axR.axhline(-1.5, color="blue", ls=":")
    axL.set_title("ln(BTC/Gold) and rolling z-score")
    axL.legend(loc="upper left"); axR.legend(loc="upper right")
    save_fig("idea10_btc_gold")

    fig, ax = plt.subplots(figsize=(9, 5))
    bucket[["fwd60_SPY", "fwd120_SPY"]].plot.bar(ax=ax)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Forward SPY return by BTC/Gold z-bucket")
    save_fig("idea10_buckets")

    fig, ax = plt.subplots(figsize=(11, 5))
    equity_curve(daily).plot(ax=ax, label=bh["name"])
    equity_curve(strat).plot(ax=ax, label=s["name"])
    ax.legend(); ax.set_title("SPY: BTC/Gold tilt vs buy & hold")
    save_fig("idea10_equity")

    report = [
        "# Idea 10 — BTC/Gold sentiment thermometer",
        f"Latest ln(BTC/GLD) z = {z.iloc[-1]:.2f}",
        "",
        bucket.round(4).to_markdown(),
        "",
        pd.DataFrame([bh, s]).round(4).to_markdown(index=False),
    ]
    write_report("idea10", report)
    print(bucket.round(4))


if __name__ == "__main__":
    main()
