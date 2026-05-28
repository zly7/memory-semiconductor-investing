"""25 — CBOE Put/Call 10d MA > 1.10 → contrarian buy SPY."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._storage_helpers import load_macro_df
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="put_call_extreme",
    name_cn="CBOE 看跌/看涨极值",
    family="sentiment",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    try:
        df = load_macro_df("CBOE_PCR")
    except FileNotFoundError:
        return Result(
            meta=META, primary_series=pd.Series(dtype=float),
            verdict="skipped",
            verdict_why="CBOE PCR series not cached — run data_acq.py --only pcr",
            notes="see data_acq.py sync_cboe_pcr()",
        )

    pcr_col = next((c for c in df.columns if "ratio" in c.lower() or "p/c" in c.lower()),
                   df.select_dtypes(include="number").columns[0])
    pcr = df[pcr_col].dropna().astype(float)
    pcr_ma = pcr.rolling(10).mean()

    spy = load_price("SPY")
    bil = load_price("BIL")
    daily_pcr = pcr_ma.reindex(spy.index).ffill()
    trig = daily_pcr > 1.10
    pos = _hold_n_after_trigger(trig.fillna(False), 30)
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        trig.fillna(False), spy, {"5d": 5, "20d": 20, "60d": 60},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=pcr_ma.rename("P/C 10d MA"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
