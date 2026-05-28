"""26 — Yield curve 10Y-3M inverted: reduce SPY exposure to 50%."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, cash_ret_from_bil, threshold_event_fwd_returns, classify_verdict,
)

META = StrategyMeta(
    id="yc_inversion_defensive",
    name_cn="10Y-3M 倒挂期间防御",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    spread = load_macro_value("T10Y3M")
    spy = load_price("SPY")
    bil = load_price("BIL")
    daily_spread = spread.reindex(spy.index).ffill()

    inverted = (daily_spread < 0).astype(float)
    # Position: 1.0 when not inverted, 0.5 when inverted
    pos = (1.0 - 0.5 * inverted)
    spy_ret = daily_returns(spy)
    cash = cash_ret_from_bil(bil, spy.index)
    strat = (pos.shift(1).fillna(1.0) * spy_ret + (1.0 - pos.shift(1).fillna(1.0)) * cash).astype(float)

    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        inverted.astype(bool), spy, {"60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=daily_spread.rename("T10Y3M (pp)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"days inverted: {int(inverted.sum())}",
    )
