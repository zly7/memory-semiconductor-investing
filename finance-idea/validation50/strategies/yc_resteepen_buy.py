"""27 — Yield curve re-steepening after inversion: buy SPY for 12 months."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil, classify_verdict,
    threshold_event_fwd_returns,
)

META = StrategyMeta(
    id="yc_resteepen_buy",
    name_cn="10Y-3M 再陡峭化买入",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    spread = load_macro_value("T10Y3M")
    spy = load_price("SPY")
    bil = load_price("BIL")
    s = spread.reindex(spy.index).ffill()

    # event: spread crosses from < 0 to > 0
    prev = s.shift(1)
    event = (prev < 0) & (s > 0)
    # hold 252 trading days after event
    pos = pd.Series(0.0, index=spy.index)
    countdown = 0
    for d in spy.index:
        if bool(event.loc[d]) if d in event.index else False:
            countdown = 252
        pos.loc[d] = 1.0 if countdown > 0 else 0.0
        if countdown > 0:
            countdown -= 1

    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        event.fillna(False), spy, {"60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=s.rename("T10Y3M (pp)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"resteepen events: {int(event.sum())} | in-market days: {int(pos.sum())}",
    )
