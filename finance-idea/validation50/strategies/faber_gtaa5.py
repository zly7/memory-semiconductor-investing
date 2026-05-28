"""05 — Faber GTAA 5: equal-weight 5 ETFs vs 10-month SMA filter, monthly."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, sma, fixed_weight_portfolio, classify_verdict

META = StrategyMeta(
    id="faber_gtaa5",
    name_cn="Faber GTAA 5 资产",
    family="trend",
    lit_verdict="robust",
)

UNIVERSE = ["SPY", "EFA", "IEF", "VNQ", "DBC"]


@register(META.id)
def compute() -> Result:
    prices = {k: load_price(k) for k in UNIVERSE}
    shy = load_price("SHY")
    common = prices["SPY"].index
    for s in prices.values():
        common = common.intersection(s.index)
    common = common.intersection(shy.index)
    px = pd.DataFrame({k: v.loc[common] for k, v in prices.items()})
    shy = shy.loc[common]

    # 10-month SMA ≈ 210 trading days
    above = pd.DataFrame({k: (px[k] > sma(px[k], 210)).astype(float) for k in UNIVERSE})
    rets = px.pct_change().fillna(0.0)
    shy_ret = shy.pct_change().fillna(0.0)

    # Resample to month-end signals: 1 if above SMA at month end, else hold SHY
    month_end = above.resample("M").last()
    daily_pos = above.reindex(rets.index).ffill()
    # Each asset gets 20% if above SMA, else its 20% goes to SHY (cash proxy)
    asset_w = daily_pos * 0.2
    cash_w = (1.0 - daily_pos.sum(axis=1) * 0.2).clip(lower=0.0)

    daily_w = asset_w.copy()
    daily_w["SHY"] = cash_w
    rets_full = rets.copy()
    rets_full["SHY"] = shy_ret
    daily_w = daily_w.shift(1).fillna(0.0)
    strat = (daily_w * rets_full).sum(axis=1)

    bench = {"spy_buy_hold": rets["SPY"], "equal_weight_5": rets.mean(axis=1)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=daily_pos.sum(axis=1).rename("# assets above SMA"),
        asset_series=px["SPY"],
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes=f"5-asset GTAA, 10M SMA filter, daily rebal to target weights",
    )
