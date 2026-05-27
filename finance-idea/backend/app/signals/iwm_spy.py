"""Idea 09 — IWM/SPY relative strength."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v > 1.0:
        return "warm", "小盘相对强势（风险偏好高）"
    if v < -1.0:
        return "cold", "小盘相对弱势"
    return "neutral", "相对中性"


def compute() -> SignalBundle:
    iwm = load_price("IWM")
    spy = load_price("SPY")
    idx = iwm.index.intersection(spy.index)
    iwm, spy = iwm.loc[idx], spy.loc[idx]
    ratio = (iwm / spy)
    z = ((ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()).dropna()

    sma60 = ratio.rolling(60).mean()
    long_iwm = (ratio > sma60).astype(float)
    long_spy = 1.0 - long_iwm
    rot = (long_iwm.shift(1) * iwm.pct_change()
           + long_spy.shift(1) * spy.pct_change()).fillna(0)
    half = ((iwm.pct_change() + spy.pct_change()) / 2).fillna(0)

    return SignalBundle(
        id="iwm_spy",
        name="IWM/SPY z",
        name_cn="小盘相对强度 (IWM/SPY)",
        description="rolling-252 z of IWM/SPY ratio",
        description_md=(
            "## 思路\n"
            "IWM (Russell 2000) / SPY 反映风险偏好，比率上升 = 风险偏好升温。\n\n"
            "## 回测结论\n"
            "z 的两端都对应**前向 60d 双方上涨**（均值反转）。简单旋转策略略好于 50/50。\n"
        ),
        unit="z",
        interpret=_interpret,
        primary_series=z,
        secondary_series=ratio,
        secondary_label="IWM/SPY ratio",
        bucket_asset=spy,
        bucket_horizons={"20d": 20, "60d": 60, "120d": 120},
        equity_specs=[("50/50 SPY+IWM", half), ("Rotate by IWM/SPY momentum", rot)],
    )
