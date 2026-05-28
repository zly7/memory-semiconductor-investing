"""45 — Harry Browne Permanent Portfolio: 25% SPY / TLT / BIL / GLD."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, fixed_weight_portfolio, classify_verdict

META = StrategyMeta(
    id="pf_permanent",
    name_cn="Harry Browne 永久组合",
    family="allocation",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    keys = ["SPY", "TLT", "BIL", "GLD"]
    px = {k: load_price(k) for k in keys}
    common = px["SPY"].index
    for s in px.values():
        common = common.intersection(s.index)
    rets = pd.DataFrame({k: daily_returns(v.loc[common]) for k, v in px.items()})
    weights = {k: 0.25 for k in keys}
    strat = fixed_weight_portfolio(rets, weights, rebal="YE")
    bench = {"spy_buy_hold": rets["SPY"], "pf_60_40_local":
             fixed_weight_portfolio(rets, {"SPY": 0.6, "TLT": 0.4}, rebal="YE")}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=pd.Series(0.25, index=common, name="SPY weight"),
        asset_series=px["SPY"].loc[common],
        strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="annual rebal back to 25/25/25/25",
    )
