"""08 — Cross-sectional momentum across 11 S&P sectors (long top 3, short bottom 3)."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="sector_xsmom",
    name_cn="美股 11 行业横截面动量",
    family="trend",
    lit_verdict="mixed",
)

SECTORS = ["XLK", "XLF", "XLE", "XLY", "XLP", "XLV", "XLI", "XLU", "XLB", "XLRE", "XLC"]


@register(META.id)
def compute() -> Result:
    px_dict = {}
    for s in SECTORS:
        try:
            px_dict[s] = load_price(s)
        except FileNotFoundError:
            continue
    common = None
    for s in px_dict.values():
        common = s.index if common is None else common.intersection(s.index)
    px = pd.DataFrame({k: v.loc[common] for k, v in px_dict.items()})

    # 12-1 month momentum (skip last month, look back 12 months)
    mom = px.shift(21).pct_change(231)  # 252-21
    rets = px.pct_change().fillna(0.0)

    monthly_idx = px.resample("M").last().index

    pos = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    current_pos = pd.Series(0.0, index=px.columns)
    for d in px.index:
        if d in monthly_idx:
            m = mom.loc[d].dropna()
            if len(m) >= 6:
                ranked = m.rank(ascending=False)
                current_pos = pd.Series(0.0, index=px.columns)
                top = ranked[ranked <= 3].index
                bot = ranked[ranked > len(m) - 3].index
                for t in top:
                    current_pos.loc[t] = 1.0 / 3
                for b in bot:
                    current_pos.loc[b] = -1.0 / 3
        pos.loc[d] = current_pos

    strat = (pos.shift(1).fillna(0.0) * rets).sum(axis=1)
    bench = {"equal_weight": rets.mean(axis=1), "spy_proxy": rets["XLK"]}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["equal_weight"]))
    return Result(
        meta=META,
        primary_series=mom.mean(axis=1).rename("avg 12-1 mom"),
        asset_series=px.mean(axis=1),
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="long-short equal-dollar; benchmark = equal-weight",
    )
