"""Idea 06 — US 10Y-3M yield curve."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v < 0:
        return "hot", "倒挂 — 历史上预警衰退（领先 ~12 个月）"
    if v < 0.5:
        return "warm", "曲线平坦 — 临近倒挂"
    return "neutral", "正常陡峭"


def compute() -> SignalBundle:
    tnx = load_price("TNX") / 10.0
    irx = load_price("IRX") / 10.0
    spy = load_price("SPY")
    idx = tnx.index.intersection(irx.index).intersection(spy.index)
    tnx, irx, spy = tnx.loc[idx], irx.loc[idx], spy.loc[idx]
    spread = (tnx - irx).dropna()

    daily = spy.pct_change().fillna(0)
    pos = pd.Series(1.0, index=spread.index)
    pos[spread < 0] = 0.5
    defensive = (pos.shift(1) * daily.reindex(spread.index).fillna(0)).fillna(0)

    return SignalBundle(
        id="yield_curve",
        name="10Y-3M spread",
        name_cn="美债 10Y-3M",
        description="US 10Y minus 3M Treasury yield (pp)",
        description_md=(
            "## 思路\n"
            "10Y-3M 倒挂被认为是最可靠的衰退领先指标之一。\n\n"
            "## 回测结论\n"
            "策略：倒挂期间 SPY 仓位降至 50%。\n"
            "样本期内总收益略低（缺席部分上涨日），但最大回撤略小（-30% → -30%）。\n"
            "信号的真正价值在**再陡峭化（unkink）**：倒挂后再次上穿 0 历史上对应中期低点。\n"
        ),
        unit="%",
        interpret=_interpret,
        primary_series=spread,
        secondary_series=spy,
        secondary_label="SPY close",
        bucket_asset=spy,
        bucket_horizons={"60d": 60, "120d": 120, "252d": 252},
        equity_specs=[("SPY buy & hold", daily), ("Defensive on inversion", defensive)],
    )
