"""24 — AAII bearish > 60%. DATA UNAVAILABLE (manual CSV not dropped)."""
import pandas as pd
import pathlib
from runner import StrategyMeta, Result, register, load_price, stats
from ._storage_helpers import load_macro_df
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="aaii_bearish_60",
    name_cn="AAII 散户极度看空反指",
    family="sentiment",
    lit_verdict="seasonal-window-only",
)


@register(META.id)
def compute() -> Result:
    try:
        df = load_macro_df("AAII_SENTIMENT")
    except FileNotFoundError:
        return Result(
            meta=META, primary_series=pd.Series(dtype=float),
            verdict="skipped",
            verdict_why="AAII sentiment CSV not yet dropped to validation50/data_drops/aaii_sentiment.csv",
            notes="see data_acq.py sync_aaii()",
        )

    bearish = df["Bearish"].dropna().astype(float)
    spy = load_price("SPY")
    bil = load_price("BIL")
    # Bearish > 60% → contrarian buy SPY hold 60 days
    daily_bear = bearish.reindex(spy.index).ffill()
    trig = daily_bear > 60.0
    pos = _hold_n_after_trigger(trig.fillna(False), 60)
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        trig.fillna(False), spy, {"20d": 20, "60d": 60, "120d": 120},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=bearish.rename("AAII Bearish %"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger weeks: {int(trig.sum())}",
    )
