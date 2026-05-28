"""48 — Inverse-vol risk parity across SPY/TLT/GLD/DBC."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="pf_risk_parity",
    name_cn="等风险贡献 (反波动) RP",
    family="allocation",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    keys = ["SPY", "TLT", "GLD", "DBC"]
    px = {k: load_price(k) for k in keys}
    common = px["SPY"].index
    for s in px.values():
        common = common.intersection(s.index)
    rets = pd.DataFrame({k: daily_returns(v.loc[common]) for k, v in px.items()})
    vol = rets.rolling(60, min_periods=20).std()
    inv_vol = 1.0 / vol.replace(0, np.nan)
    w = inv_vol.div(inv_vol.sum(axis=1), axis=0).ffill().fillna(0.25)

    # Monthly rebal: hold prior month's weights
    monthly = w.resample("M").last().ffill()
    daily_w = monthly.reindex(rets.index, method="ffill").fillna(0.25)
    strat = (daily_w.shift(1).fillna(0.25) * rets).sum(axis=1)
    bench = {"spy_buy_hold": rets["SPY"], "equal_weight": rets.mean(axis=1)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["equal_weight"]))
    return Result(
        meta=META, primary_series=w["SPY"].rename("SPY rp weight"),
        asset_series=px["SPY"].loc[common],
        strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="inverse 60d vol weights, monthly rebal; no leverage",
    )
