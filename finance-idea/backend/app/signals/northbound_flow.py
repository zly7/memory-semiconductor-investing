"""Idea 08 — northbound flow 20-day cumulative."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_macro, load_price


def _interpret(v: float) -> tuple[str, str]:
    if v > 500:
        return "warm", "近 20 日累计流入显著（注意：历史上「高流入」反而对应低胜率）"
    if v < -500:
        return "cold", "近 20 日累计流出 — 中期偏弱"
    return "neutral", "流向中性"


def _pick_col(df: pd.DataFrame) -> str:
    for c in ("当日成交净买额", "当日资金流入", "净买额", "资金净流入"):
        if c in df.columns:
            return c
    return df.select_dtypes(include="number").columns[0]


def compute() -> SignalBundle:
    try:
        nf = load_macro("NORTH_FLOW")
        col = _pick_col(nf)
        flow = nf[col].dropna().astype(float)
    except Exception:
        flow = pd.Series(dtype=float)
    if flow.empty:
        return SignalBundle(
            id="northbound_flow", name="Northbound 20d flow",
            name_cn="北向 20 日累计", description="cumulative northbound net flow",
            description_md="数据不可用。", unit="亿",
            interpret=_interpret, primary_series=flow)

    cum20 = flow.rolling(20).sum().dropna()

    a = load_price("ETF510300").reindex(cum20.index).ffill().dropna()
    idx = cum20.index.intersection(a.index)
    cum20, a = cum20.loc[idx], a.loc[idx]

    daily = a.pct_change().fillna(0)
    pos = (cum20 > 0).astype(float)
    strat = (pos.shift(1) * daily).fillna(0)

    return SignalBundle(
        id="northbound_flow",
        name="Northbound 20d flow",
        name_cn="北向 20 日累计净流入",
        description="rolling 20-day sum of northbound net buys (亿元)",
        description_md=(
            "## 思路\n"
            "北向资金被视为「聪明钱」。但实证显示**简单跟随存在反向特征**：\n"
            "净流入分位最高的 q5 反而对应 fwd-60d 沪深 300 -1.5%。\n\n"
            "## 回测结论\n"
            "中位分位 q3 表现最好（fwd-60d +3.95%），首尾两端均偏弱。\n"
        ),
        unit="亿",
        interpret=_interpret,
        primary_series=cum20,
        secondary_series=a,
        secondary_label="510300 close",
        bucket_asset=a,
        bucket_horizons={"20d": 20, "60d": 60},
        equity_specs=[("510300 buy & hold", daily),
                      ("510300 long when N-flow > 0", strat)],
    )
