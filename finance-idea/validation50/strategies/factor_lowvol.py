"""49 — USMV low-volatility factor vs SPY."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="factor_lowvol",
    name_cn="低波因子 USMV",
    family="allocation",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    usmv = load_price("USMV")
    spy = load_price("SPY")
    common = usmv.index.intersection(spy.index)
    usmv, spy = usmv.loc[common], spy.loc[common]
    strat = daily_returns(usmv)
    bench = {"spy_buy_hold": daily_returns(spy)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=usmv.rename("USMV close"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="long-only USMV; benchmark = SPY",
    )
