"""Idea 05 — DXY 6m change vs EEM."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v < -5:
        return "cold", "美元 6 个月大跌 — EM 强烈顺风"
    if v > 5:
        return "hot", "美元 6 个月大涨 — EM 强力承压"
    return "neutral", "美元中性"


def compute() -> SignalBundle:
    dxy = load_price("DXY")
    eem = load_price("EEM")
    idx = dxy.index.intersection(eem.index)
    dxy, eem = dxy.loc[idx], eem.loc[idx]

    chg = (dxy / dxy.shift(126) - 1) * 100   # in %
    chg = chg.dropna()

    daily = eem.pct_change().fillna(0)
    pos = pd.Series(1.0, index=chg.index)
    pos[chg < -5] = 1.5
    pos[chg > 5] = 0.5
    tilted = (pos.shift(1) * daily.reindex(chg.index).fillna(0)).fillna(0)

    return SignalBundle(
        id="dxy_em",
        name="DXY 6m change",
        name_cn="美元指数 6 月变动 → EEM",
        description="DXY 6-month % change",
        description_md=(
            "## 思路\n"
            "强美元 → 新兴市场资金流出、外债成本上升。\n\n"
            "## 回测结论（本组里最强）\n"
            "DXY 6m < -5% → fwd-120d EEM **+11.2%**，胜率 86%。\n"
            "DXY 6m > +5% → fwd-60d EEM -1.0%。\n"
        ),
        unit="%",
        interpret=_interpret,
        primary_series=chg,
        secondary_series=eem,
        secondary_label="EEM close",
        bucket_asset=eem,
        bucket_horizons={"60d": 60, "120d": 120, "252d": 252},
        equity_specs=[("EEM buy & hold", daily), ("EEM DXY-6m tilt", tilted)],
    )
