"""Idea 01 — QDII (Nasdaq) ETF premium vs NAV as contrarian QQQ signal."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ._base import SignalBundle, load_nav, load_price

NASDAQ_QDII = ["QDII513100", "QDII513300", "QDII159941"]


def _interpret(v: float) -> tuple[str, str]:
    if v > 5:
        return "hot", "国内QDII溢价偏高 — 短期反指做空候选"
    if v > 2:
        return "warm", "QDII溢价中高 — 警惕"
    if v < -2:
        return "cold", "QDII折价 — 短期反弹候选"
    return "neutral", "QDII溢价正常"


def compute() -> SignalBundle:
    premiums = {}
    for key in NASDAQ_QDII:
        try:
            p = load_price(key)
            n = load_nav(key)
        except FileNotFoundError:
            continue
        df = pd.concat([p.rename("p"), n.rename("n")], axis=1).dropna()
        premiums[key] = (df["p"] - df["n"]) / df["n"] * 100
    if not premiums:
        empty = pd.Series(dtype=float)
        return SignalBundle(
            id="qdii_premium", name="QDII Premium",
            name_cn="QDII纳指溢价", description="median premium across QDII Nasdaq ETFs",
            description_md="数据缺失。", unit="%",
            interpret=lambda v: ("na", "no data"),
            primary_series=empty)

    sentiment = pd.DataFrame(premiums).median(axis=1).dropna()
    qqq = load_price("QQQ").reindex(sentiment.index).ffill().dropna()
    sentiment = sentiment.loc[qqq.index]

    p90 = sentiment.expanding(252).quantile(0.90)
    p10 = sentiment.expanding(252).quantile(0.10)

    # Strategy: flat QQQ when premium > p90
    daily = qqq.pct_change().fillna(0)
    pos = pd.Series(1.0, index=sentiment.index)
    pos[sentiment > p90] = 0.0
    strat = (pos.shift(1) * daily).fillna(0)

    return SignalBundle(
        id="qdii_premium",
        name="QDII Nasdaq Premium",
        name_cn="QDII纳指溢价 反指",
        description="cross-sectional median premium across CN-listed Nasdaq QDII ETFs",
        description_md=(
            "## 思路\n"
            "国内纳指QDII ETF（513100、513300、159941 等）受QDII额度限制经常出现溢价。\n"
            "**溢价越高，越反映散户在A股内追买美股的情绪极致**，往往对应美股短期顶部。\n\n"
            "## 信号定义\n"
            "对所有纳指QDII的 `(price − NAV) / NAV × 100%` 取截面中位数，"
            "按 252 日 90/10 分位划阈值。\n\n"
            "## 回测结论\n"
            "顶部分位 q5 的 20 日前向胜率（62%）显著低于 q4（72%）；"
            "但简单的「溢价高就平仓」规则交易过于频繁，"
            "未能跑赢 buy & hold。更适合作为**二级权重信号**。"
        ),
        unit="%",
        interpret=_interpret,
        primary_series=sentiment,
        secondary_series=qqq,
        secondary_label="QQQ close",
        upper_band=p90,
        lower_band=p10,
        bucket_asset=qqq,
        bucket_horizons={"5d": 5, "20d": 20, "60d": 60},
        equity_specs=[("QQQ buy & hold", daily), ("Flatten on premium>p90", strat)],
    )
