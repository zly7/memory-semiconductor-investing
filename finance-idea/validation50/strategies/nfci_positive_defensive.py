"""31 — Chicago Fed NFCI > 0 (tightening conditions) → reduce SPY to 50%."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, cash_ret_from_bil, threshold_event_fwd_returns, classify_verdict,
)

META = StrategyMeta(
    id="nfci_positive_defensive",
    name_cn="芝加哥金融条件 > 0 转防御",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    nfci = load_macro_value("NFCI")
    spy = load_price("SPY")
    bil = load_price("BIL")
    daily_nfci = nfci.reindex(spy.index).ffill()
    tight = (daily_nfci > 0).astype(float)
    pos = 1.0 - 0.5 * tight
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = (pos.shift(1).fillna(1.0) * spy_ret
             + (1.0 - pos.shift(1).fillna(1.0)) * cash).astype(float)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        tight.astype(bool), spy, {"20d": 20, "60d": 60, "120d": 120},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=daily_nfci.rename("NFCI (weekly)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes="NFCI > 0 → financial conditions tighter than average",
    )
