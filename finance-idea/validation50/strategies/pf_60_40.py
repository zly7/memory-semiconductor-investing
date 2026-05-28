"""44 — 60/40 stock/bond portfolio, annually rebalanced (canonical benchmark)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, fixed_weight_portfolio, classify_verdict

META = StrategyMeta(
    id="pf_60_40",
    name_cn="60/40 股债组合 年度再平衡",
    family="allocation",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    agg = load_price("AGG")
    common = spy.index.intersection(agg.index)
    rets = pd.concat([
        daily_returns(spy.loc[common]).rename("SPY"),
        daily_returns(agg.loc[common]).rename("AGG"),
    ], axis=1).dropna()

    strat = fixed_weight_portfolio(rets, {"SPY": 0.6, "AGG": 0.4}, rebal="YE")
    bench = {
        "spy_buy_hold": rets["SPY"],
        "agg_buy_hold": rets["AGG"],
        "pf_50_50": fixed_weight_portfolio(rets, {"SPY": 0.5, "AGG": 0.5}, rebal="YE"),
    }
    weight_series = (rets["SPY"].rolling(252, min_periods=20).mean() * 0 + 0.6)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=weight_series.rename("SPY weight"),
        asset_series=spy.loc[common],
        strategy_returns=strat,
        benchmark_returns=bench,
        buckets=None,
        verdict=verdict,
        verdict_why=why,
        notes="annual rebal back to 60/40",
    )
