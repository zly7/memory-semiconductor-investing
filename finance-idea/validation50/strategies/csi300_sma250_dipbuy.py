"""04 — CSI300 250-day SMA dip-buy."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import daily_returns, sma, classify_verdict

META = StrategyMeta(
    id="csi300_sma250_dipbuy",
    name_cn="沪深300 250日均线下方持续买入",
    family="trend",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    csi = load_price("CSI300")
    sma250 = sma(csi, 250)
    below = (csi < sma250).astype(float)
    ret = daily_returns(csi)
    y = load_macro_value("DGS3MO").reindex(csi.index).ffill()
    cash = (y / 100.0 / 252.0).fillna(0.0)

    pos = below.shift(1).fillna(0.0)
    strat = (pos * ret + (1 - pos) * cash).astype(float)
    valid = sma250.dropna().index
    strat = strat.loc[strat.index.intersection(valid)]
    bench = {"csi300_buy_hold": ret.loc[valid], "cash_3m": cash.loc[valid]}

    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]))
    return Result(
        meta=META,
        primary_series=(csi / sma250 - 1.0).dropna(),
        asset_series=csi,
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="invert of 03 — hold during downtrends only",
    )
