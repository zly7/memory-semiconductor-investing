"""47 — Dalio All Weather: 30 SPY / 40 TLT / 15 IEF / 7.5 GLD / 7.5 DBC."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, fixed_weight_portfolio, classify_verdict

META = StrategyMeta(
    id="pf_all_weather",
    name_cn="Dalio All Weather",
    family="allocation",
    lit_verdict="robust→decay",
)


@register(META.id)
def compute() -> Result:
    weights = {"SPY": 0.30, "TLT": 0.40, "IEF": 0.15, "GLD": 0.075, "DBC": 0.075}
    px = {k: load_price(k) for k in weights}
    common = px["SPY"].index
    for s in px.values():
        common = common.intersection(s.index)
    rets = pd.DataFrame({k: daily_returns(v.loc[common]) for k, v in px.items()})
    strat = fixed_weight_portfolio(rets, weights, rebal="YE")
    bench = {"spy_buy_hold": rets["SPY"],
             "pf_60_40_local":
             fixed_weight_portfolio(rets, {"SPY": 0.6, "TLT": 0.4}, rebal="YE")}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=pd.Series(0.30, index=common, name="SPY weight"),
        asset_series=px["SPY"].loc[common],
        strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="annual rebal; bond-heavy → expect lower CAGR vs SPY",
    )
