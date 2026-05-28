"""50 — QUAL quality factor vs SPY."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="factor_quality",
    name_cn="质量因子 QUAL",
    family="allocation",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    qual = load_price("QUAL")
    spy = load_price("SPY")
    common = qual.index.intersection(spy.index)
    qual, spy = qual.loc[common], spy.loc[common]
    strat = daily_returns(qual)
    bench = {"spy_buy_hold": daily_returns(spy)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=qual.rename("QUAL close"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="long-only QUAL; benchmark = SPY",
    )
