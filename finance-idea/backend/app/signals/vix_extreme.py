"""Idea 03 — VIX extremes vs SPY."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v > 30:
        return "hot", "恐慌区 — 历史上 fwd-60d SPY +10%"
    if v > 22:
        return "warm", "震荡升高 — 谨慎"
    if v < 13:
        return "cold", "极度平静 — 隐含波动率低位"
    return "neutral", "波动率中性"


def compute() -> SignalBundle:
    vix = load_price("VIX")
    spy = load_price("SPY")
    idx = vix.index.intersection(spy.index)
    vix, spy = vix.loc[idx], spy.loc[idx]

    daily = spy.pct_change().fillna(0)
    pos = pd.Series(1.0, index=vix.index)
    pos[vix > 30] = 1.5
    pos[vix < 13] = 0.5
    tilted = (pos.shift(1) * daily).fillna(0)

    return SignalBundle(
        id="vix_extreme",
        name="VIX",
        name_cn="VIX 极值反指",
        description="CBOE Volatility Index",
        description_md=(
            "## 思路\n"
            "VIX 是 SPX 期权隐含波动率，极端高位往往伴随恐慌性抛售，正是逆势买入区。\n\n"
            "## 回测结论\n"
            "VIX > 30 后：fwd-5d SPY +1.2%，fwd-20d +5.2%，fwd-60d +10.1%，20d 胜率 85%。\n"
            "VIX < 13 时反向走平：fwd-60d 仅 +1.4%。该信号在尾部最强。\n"
        ),
        unit="pts",
        interpret=_interpret,
        primary_series=vix,
        secondary_series=spy,
        secondary_label="SPY close",
        bucket_asset=spy,
        bucket_horizons={"5d": 5, "20d": 20, "60d": 60},
        equity_specs=[
            ("SPY buy & hold", daily),
            ("VIX tilt 1.5/1.0/0.5", tilted),
        ],
    )
