"""39 — Sell in May: hold SPY Nov 1 → Apr 30, BIL cash May 1 → Oct 31."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil, classify_verdict,
)

META = StrategyMeta(
    id="sell_in_may",
    name_cn="Sell in May 季节性",
    family="seasonal",
    lit_verdict="seasonal-window-only",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)

    # Winter months (Nov..Apr) = in market; summer (May..Oct) = cash
    month = pd.Series(spy.index.month, index=spy.index)
    pos = ((month >= 11) | (month <= 4)).astype(float)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    # Bucket: avg fwd-21d return by calendar month
    fwd21 = spy.pct_change(21).shift(-21)
    df = pd.concat([month.rename("m"), fwd21.rename("ret")], axis=1).dropna()
    by_month = df.groupby("m")["ret"].mean().to_frame("fwd_21d_ret")

    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=pos.rename("in_market"),
        asset_series=spy,
        strategy_returns=strat,
        benchmark_returns=bench,
        buckets=by_month,
        verdict=verdict,
        verdict_why=why,
        notes="winter Nov-Apr in market, summer in cash",
    )
