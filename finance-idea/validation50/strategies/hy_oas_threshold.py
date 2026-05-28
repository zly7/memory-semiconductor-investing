"""28 — HY OAS > 500bp → switch from SPY to IEF (defensive)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, switching_returns, classify_verdict,
    bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="hy_oas_threshold",
    name_cn="高收益 OAS > 500bp 转防御",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    oas = load_macro_value("BAMLH0A0HYM2")  # in % terms (e.g., 4.5)
    spy = load_price("SPY")
    ief = load_price("IEF")
    common = spy.index.intersection(ief.index)
    spy, ief = spy.loc[common], ief.loc[common]
    daily_oas = oas.reindex(spy.index).ffill()

    risky = daily_oas < 5.0  # under 500 bp → risk-on (SPY); else risk-off (IEF)
    spy_ret = daily_returns(spy)
    ief_ret = daily_returns(ief)
    flag = risky.astype(float)
    strat = switching_returns(flag, spy_ret, ief_ret)
    bench = {"spy_buy_hold": spy_ret, "ief_buy_hold": ief_ret}

    buckets = bucket_fwd_returns(daily_oas.dropna(), spy,
                                 {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=daily_oas.rename("HY OAS (%)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"BAMLH0A0HYM2 series: only {len(oas)} obs in cache (FRED truncates)",
    )
