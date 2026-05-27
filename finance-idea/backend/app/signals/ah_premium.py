"""Idea 07 — AH premium (graceful skip if data unavailable)."""
from __future__ import annotations

import pandas as pd

from ._base import SignalBundle, load_macro


def _interpret(v: float) -> tuple[str, str]:
    if v > 140:
        return "hot", "A 显著高于 H — 考虑切换 H"
    if v < 110:
        return "cold", "A/H 价差极低 — 考虑切换 A"
    return "neutral", "价差中性"


def compute() -> SignalBundle:
    try:
        ah = load_macro("AH_PREMIUM")
        col = ah.select_dtypes(include="number").columns[0]
        ah_s = ah[col].dropna().astype(float)
    except Exception:
        ah_s = pd.Series(dtype=float)

    return SignalBundle(
        id="ah_premium",
        name="AH Premium",
        name_cn="AH 溢价指数",
        description="Hang Seng AH Premium Index",
        description_md=(
            "## 思路\n"
            "AH 溢价指数 = A 股价 / H 股价 × 100。极高时考虑切换至 H，反之亦然。\n\n"
            "## 状态\n"
            "akshare 端点在当前环境暂不可用；信号会在数据回归后自动启用。\n"
        ),
        unit="",
        interpret=_interpret,
        primary_series=ah_s,
    )
