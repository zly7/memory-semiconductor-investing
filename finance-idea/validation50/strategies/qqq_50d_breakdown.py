"""15 — QQQ breakdown >3% below SMA50: buy, target hold 20 days."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="qqq_50d_breakdown",
    name_cn="QQQ 跌破 50日均线 3% 反弹",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    qqq = load_price("QQQ")
    bil = load_price("BIL")
    ma50 = sma(qqq, 50)
    dev = (qqq / ma50 - 1.0)
    trig = dev < -0.03

    pos = _hold_n_after_trigger(trig.fillna(False), 20)
    cash = cash_ret_from_bil(bil, qqq.index)
    qqq_ret = daily_returns(qqq)
    strat = switching_returns(pos, qqq_ret, cash)

    bench = {"qqq_buy_hold": qqq_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        flag=trig.fillna(False), asset=qqq,
        horizons={"5d": 5, "20d": 20, "60d": 60},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["qqq_buy_hold"]))
    return Result(
        meta=META, primary_series=dev.rename("dev to SMA50"),
        asset_series=qqq, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger days: {int(trig.sum())} | hold 20d post-trigger",
    )
