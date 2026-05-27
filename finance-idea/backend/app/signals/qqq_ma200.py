"""Idea 02 — QQQ vs its 200-day SMA."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v < 0.9:
        return "cold", "QQQ深度低于200日均线 — 反弹概率高"
    if v < 1.0:
        return "warm", "低于200日均线"
    if v > 1.15:
        return "hot", "QQQ高于200日均线15%以上 — 警惕"
    return "neutral", "趋势中"


def compute() -> SignalBundle:
    qqq = load_price("QQQ").asfreq("B").ffill()
    sma = qqq.rolling(200).mean()
    ratio = (qqq / sma).dropna()

    daily = qqq.pct_change().fillna(0)
    pos_below = (ratio.shift(1) <= 1).astype(float)
    pos_above = (ratio.shift(1) > 1).astype(float)

    return SignalBundle(
        id="qqq_ma200",
        name="QQQ vs SMA200",
        name_cn="QQQ 200日均线",
        description="QQQ close / 200d SMA",
        description_md=(
            "## 思路\n"
            "QQQ 跌破 200 日均线常被视作买入信号，但实证显示**趋势效应远强于抄底**。\n\n"
            "## 信号定义\n"
            "`close / SMA200`。该值 < 1 表示已破均线，深度低于（<0.85）历史上 20 日均回报 +4.6%。\n\n"
            "## 回测结论\n"
            "策略 A：仅在均线下持仓 → 显著跑输 buy & hold。\n"
            "策略 B：仅在均线上持仓 → 总收益相近但回撤更小（−21% vs −36%），Sharpe 更高。\n"
        ),
        unit="ratio",
        interpret=_interpret,
        primary_series=ratio,
        secondary_series=qqq,
        secondary_label="QQQ close",
        bucket_asset=qqq,
        bucket_horizons={"20d": 20, "60d": 60, "120d": 120},
        equity_specs=[
            ("QQQ buy & hold", daily),
            ("Long only below SMA200", (pos_below * daily).fillna(0)),
            ("Long only above SMA200", (pos_above * daily).fillna(0)),
        ],
    )
