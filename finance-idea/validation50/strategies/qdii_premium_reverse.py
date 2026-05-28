"""21 — QDII Nasdaq premium reversal: exit QQQ when median premium > 90th percentile."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats
from ._storage_helpers import load_nav
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    bucket_fwd_returns, classify_verdict, bucket_monotonicity,
)

META = StrategyMeta(
    id="qdii_premium_reverse",
    name_cn="QDII 纳指溢价反指 QQQ",
    family="sentiment",
    lit_verdict="mixed",
)

NASDAQ_QDII = ["QDII513100", "QDII513300", "QDII159941"]


@register(META.id)
def compute() -> Result:
    premiums = {}
    for key in NASDAQ_QDII:
        try:
            p = load_price(key)
            n = load_nav(key)
        except FileNotFoundError:
            continue
        df = pd.concat([p.rename("p"), n.rename("n")], axis=1).dropna()
        premiums[key] = (df["p"] - df["n"]) / df["n"] * 100

    if not premiums:
        return _empty_result()

    prem = pd.DataFrame(premiums).median(axis=1).dropna()
    qqq = load_price("QQQ").reindex(prem.index).ffill().dropna()
    bil = load_price("BIL")
    common = prem.index.intersection(qqq.index)
    prem, qqq = prem.loc[common], qqq.loc[common]

    p90 = prem.expanding(252).quantile(0.90)
    flag = (prem <= p90).astype(float)  # stay in QQQ when not at extreme

    cash = cash_ret_from_bil(bil, qqq.index)
    qqq_ret = daily_returns(qqq)
    strat = switching_returns(flag, qqq_ret, cash)

    bench = {"qqq_buy_hold": qqq_ret, "bil_cash": cash}
    buckets = bucket_fwd_returns(prem, qqq, {"5d": 5, "20d": 20, "60d": 60})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["qqq_buy_hold"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=prem.rename("median premium %"),
        asset_series=qqq, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"bucket ρ={mono:+.2f} (expect ≤ 0 for contrarian)",
    )


def _empty_result() -> Result:
    empty = pd.Series(dtype=float)
    return Result(
        meta=META, primary_series=empty, asset_series=None,
        strategy_returns=None, benchmark_returns={},
        verdict="skipped", verdict_why="QDII NAV cache empty",
        notes="data missing",
    )
