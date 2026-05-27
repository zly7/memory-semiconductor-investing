"""Idea 04 — Gold/Copper ratio z-score."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v > 1.5:
        return "hot", "金铜比拉高 — 风险厌恶上升"
    if v < -1.5:
        return "cold", "金铜比极低 — 风险偏好高"
    return "neutral", "中性"


def compute() -> SignalBundle:
    g = load_price("GC")
    c = load_price("HG")
    spy = load_price("SPY")
    idx = g.index.intersection(c.index).intersection(spy.index)
    g, c, spy = g.loc[idx], c.loc[idx], spy.loc[idx]

    ratio = g / c
    z = ((ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()).dropna()

    daily = spy.pct_change().fillna(0)
    pos = pd.Series(1.0, index=z.index)
    pos[z > 1.5] = 1.25
    pos[z < -1.5] = 0.75
    tilted = (pos.shift(1) * daily.reindex(z.index).fillna(0)).fillna(0)

    return SignalBundle(
        id="gold_copper",
        name="Gold/Copper z",
        name_cn="金铜比 风险情绪",
        description="rolling-252 z-score of Gold/Copper ratio",
        description_md=(
            "## 思路\n"
            "金价跌、铜价涨 → 风险偏好上升；金涨铜跌 → 风险厌恶。z-score 极值往往伴随转向。\n\n"
            "## 回测结论\n"
            "z<-1.5 和 z>1.5 两端都对应 SPY 前向 60 日正回报（+5.7% 和 +4.9%）。"
            "更适合作为**波动率/转向**信号而非方向信号。\n"
        ),
        unit="z",
        interpret=_interpret,
        primary_series=z,
        secondary_series=ratio,
        secondary_label="Gold/Copper ratio",
        bucket_asset=spy,
        bucket_horizons={"20d": 20, "60d": 60, "120d": 120},
        equity_specs=[("SPY buy & hold", daily), ("SPY Gold/Copper tilt", tilted)],
    )
