"""18 — CSI300 drawdown >10% from 1Y high: hold 6 months."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, switching_returns, threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="csi300_drawdown_10pct",
    name_cn="沪深300 从 1Y 高点回撤 10% 买入",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    csi = load_price("CSI300")
    high_1y = csi.rolling(252, min_periods=60).max()
    dd = csi / high_1y - 1.0
    trig = dd < -0.10
    pos = _hold_n_after_trigger(trig.fillna(False), 120)
    y = load_macro_value("DGS3MO").reindex(csi.index).ffill()
    cash = (y / 100.0 / 252.0).fillna(0.0)
    csi_ret = daily_returns(csi)
    strat = switching_returns(pos, csi_ret, cash)
    bench = {"csi300_buy_hold": csi_ret, "cash_3m": cash}

    buckets = threshold_event_fwd_returns(
        flag=trig.fillna(False), asset=csi,
        horizons={"20d": 20, "60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]))
    return Result(
        meta=META, primary_series=dd.rename("drawdown from 1Y high"),
        asset_series=csi, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger days: {int(trig.sum())}",
    )
