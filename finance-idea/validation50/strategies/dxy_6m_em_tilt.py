"""29 — DXY 6-month change → tilt EEM allocation."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, classify_verdict,
    bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="dxy_6m_em_tilt",
    name_cn="DXY 6 月跌幅 → EEM 加仓",
    family="macro",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    dxy = load_price("DXY")
    eem = load_price("EEM")
    spy = load_price("SPY")
    common = dxy.index.intersection(eem.index).intersection(spy.index)
    dxy, eem, spy = dxy.loc[common], eem.loc[common], spy.loc[common]

    dxy_6m = dxy.pct_change(126)
    eem_ret = daily_returns(eem)
    spy_ret = daily_returns(spy)

    # When DXY 6m < -5%, full EEM; > +5%, half EEM half SPY; else equal
    pos_eem = pd.Series(0.5, index=dxy.index)
    pos_eem[dxy_6m < -0.05] = 1.0
    pos_eem[dxy_6m > 0.05] = 0.5
    pos_spy = 1.0 - pos_eem
    strat = (pos_eem.shift(1).fillna(0.5) * eem_ret
             + pos_spy.shift(1).fillna(0.5) * spy_ret).astype(float)

    bench = {"spy_buy_hold": spy_ret, "eem_buy_hold": eem_ret,
             "eq_spy_eem": 0.5 * spy_ret + 0.5 * eem_ret}
    buckets = bucket_fwd_returns(dxy_6m.dropna(), eem,
                                 {"60d": 60, "120d": 120, "252d": 252})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["eq_spy_eem"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=dxy_6m.rename("DXY 6M change"),
        asset_series=eem, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"bucket ρ={mono:+.2f} (expect negative: weak USD → strong EM)",
    )
