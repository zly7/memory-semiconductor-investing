"""03 — CSI300 250-day SMA timing (A-shares trend filter)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, sma, switching_returns, classify_verdict,
    bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="csi300_sma250_timing",
    name_cn="沪深300 250日均线 趋势开关",
    family="trend",
    lit_verdict="mixed",
)


def _cn_cash_proxy(index) -> pd.Series:
    """3-month T-bill (DGS3MO) as a USD proxy; A-shares lack a clean CN cash ETF
    in our cache. Apply daily yield/252 as a rough cash return."""
    try:
        y = load_macro_value("DGS3MO").reindex(index).ffill()
    except Exception:
        return pd.Series(0.0, index=index)
    return (y / 100.0 / 252.0).fillna(0.0)


@register(META.id)
def compute() -> Result:
    csi = load_price("CSI300")
    sma250 = sma(csi, 250)
    flag = (csi > sma250).astype(float)

    csi_ret = daily_returns(csi)
    cash = _cn_cash_proxy(csi.index)
    strat = switching_returns(flag, csi_ret, cash)

    valid = sma250.dropna().index
    strat = strat.loc[strat.index.intersection(valid)]
    bench = {"csi300_buy_hold": csi_ret.loc[valid], "cash_3m": cash.loc[valid]}

    buckets = bucket_fwd_returns(
        signal=(csi / sma250 - 1.0).dropna(),
        asset=csi,
        horizons={"20d": 20, "60d": 60, "120d": 120},
    )
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]),
                                    direction_check=mono)
    return Result(
        meta=META,
        primary_series=(csi / sma250 - 1.0).dropna(),
        asset_series=csi,
        strategy_returns=strat,
        benchmark_returns=bench,
        buckets=buckets,
        verdict=verdict,
        verdict_why=why,
        notes=f"bucket monotonicity ρ={mono:+.2f}",
    )
