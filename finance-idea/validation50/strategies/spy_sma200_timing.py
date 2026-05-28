"""01 — SPY 200-day SMA timing: hold SPY when above SMA200, else BIL."""
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, switching_returns, cash_ret_from_bil,
    bucket_fwd_returns, classify_verdict, bucket_monotonicity,
)

META = StrategyMeta(
    id="spy_sma200_timing",
    name_cn="SPY 200日均线 趋势开关",
    family="trend",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")

    sma200 = sma(spy, 200)
    flag = (spy > sma200).astype(float)

    spy_ret = daily_returns(spy)
    cash = cash_ret_from_bil(bil, spy.index)
    strat = switching_returns(flag, spy_ret, cash)

    # Trim to the period where signal is defined
    valid = sma200.dropna().index
    strat = strat.loc[strat.index.intersection(valid)]
    bench = {
        "spy_buy_hold": spy_ret.loc[valid],
        "bil_cash": cash.loc[valid],
    }

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
        notes=f"bucket monotonicity ρ={mono:+.2f}",
    )
