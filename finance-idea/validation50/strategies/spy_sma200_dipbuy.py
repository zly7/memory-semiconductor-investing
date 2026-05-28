"""02 — SPY 200-day SMA dip-buy: DCA only while below SMA200."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, cash_ret_from_bil, classify_verdict,
    bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="spy_sma200_dipbuy",
    name_cn="SPY 200日均线下方持续买入",
    family="trend",
    lit_verdict="decayed",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    sma200 = sma(spy, 200)
    below = (spy < sma200).astype(float)
    spy_ret = daily_returns(spy)
    cash = cash_ret_from_bil(bil, spy.index)

    # Strategy: 100% SPY when below SMA200, else cash
    pos = below.shift(1).fillna(0.0)
    strat = (pos * spy_ret + (1 - pos) * cash).astype(float)

    valid = sma200.dropna().index
    strat = strat.loc[strat.index.intersection(valid)]
    bench = {"spy_buy_hold": spy_ret.loc[valid], "bil_cash": cash.loc[valid]}

    buckets = bucket_fwd_returns(
        signal=(spy / sma200 - 1.0).dropna(),
        asset=spy,
        horizons={"20d": 20, "60d": 60, "120d": 120},
    )
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=mono)
    return Result(
        meta=META,
        primary_series=(spy / sma200 - 1.0).dropna(),
        asset_series=spy,
        strategy_returns=strat,
        benchmark_returns=bench,
        buckets=buckets,
        verdict=verdict,
        verdict_why=why,
        notes="invert of 01 — buy ONLY when in downtrend",
    )
