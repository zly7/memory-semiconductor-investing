"""Idea 10 — ln(BTC/Gold) sentiment thermometer."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v > 1.5:
        return "hot", "BTC/黄金欢愉 — 警惕回调"
    if v < -1.5:
        return "cold", "BTC/黄金恐惧 — 反转候选"
    return "neutral", "中性"


def compute() -> SignalBundle:
    btc = load_price("BTC")
    gld = load_price("GLD")
    spy = load_price("SPY")
    idx = btc.index.intersection(gld.index).intersection(spy.index)
    btc, gld, spy = btc.loc[idx], gld.loc[idx], spy.loc[idx]
    log_ratio = np.log(btc / gld)
    z = ((log_ratio - log_ratio.rolling(252).mean())
         / log_ratio.rolling(252).std()).dropna()

    daily = spy.pct_change().fillna(0)
    pos = pd.Series(1.0, index=z.index)
    pos[z > 1.5] = 0.75
    pos[z < -1.5] = 1.25
    tilted = (pos.shift(1) * daily.reindex(z.index).fillna(0)).fillna(0)

    return SignalBundle(
        id="btc_gold",
        name="ln(BTC/Gold) z",
        name_cn="BTC/黄金 情绪温度",
        description="rolling-252 z of ln(BTC/Gold)",
        description_md=(
            "## 思路\n"
            "BTC 是当前最纯粹的「风险情绪资产」，黄金是「避险锚」。比率极端往往映射情绪极端。\n\n"
            "## 回测结论\n"
            "样本期内 z>1.5（欢愉）后 fwd-120d SPY +9% 胜率 95%——\n"
            "**注意**：BTC 在样本期单调上行，该结论可能受制于 BTC 自身牛市，使用需谨慎。\n"
        ),
        unit="z",
        interpret=_interpret,
        primary_series=z,
        secondary_series=log_ratio,
        secondary_label="ln(BTC/Gold)",
        bucket_asset=spy,
        bucket_horizons={"60d": 60, "120d": 120, "252d": 252},
        equity_specs=[("SPY buy & hold", daily), ("SPY BTC/Gold tilt", tilted)],
    )
