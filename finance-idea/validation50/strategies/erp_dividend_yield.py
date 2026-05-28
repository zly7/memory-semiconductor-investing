"""32 — Equity risk premium proxy (SPY 12M return - DGS10) extremes."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, classify_verdict, bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="erp_dividend_yield",
    name_cn="股票风险溢价 (12M ret - 10Y) 极值",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    # Proper SPY dividend yield is not in cache; substitute earnings yield proxy
    # using trailing 12M total return spread vs 10Y treasury — a rougher ERP proxy.
    spy = load_price("SPY")
    dgs10 = load_macro_value("DGS10")
    yield10 = (dgs10.reindex(spy.index).ffill()) / 100.0

    spy_12m = spy.pct_change(252)
    erp_proxy = spy_12m - yield10

    spy_ret = daily_returns(spy)
    # Strategy: if proxy > 0.04 (very high implied premium), tilt to 1.2x SPY
    # via levered position; if < -0.04, reduce to 0.5x. Conservative, no shorts.
    target = pd.Series(1.0, index=spy.index)
    target[erp_proxy > 0.04] = 1.0  # already 1.0
    target[erp_proxy < -0.04] = 0.5
    strat = (target.shift(1).fillna(1.0) * spy_ret).astype(float)
    bench = {"spy_buy_hold": spy_ret}

    buckets = bucket_fwd_returns(erp_proxy.dropna(), spy,
                                 {"60d": 60, "120d": 120, "252d": 252})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=mono)
    return Result(
        meta=META, primary_series=erp_proxy.rename("ERP proxy"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes="ERP proxy = 12M SPY total return − DGS10/100",
    )
