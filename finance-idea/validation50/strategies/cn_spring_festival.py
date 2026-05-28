"""43 — A-share spring festival window effect (10 days before to 5 after)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, switching_returns, classify_verdict,
)

META = StrategyMeta(
    id="cn_spring_festival",
    name_cn="A 股春节前后效应",
    family="seasonal",
    lit_verdict="mixed",
)

# Lunar New Year (春节) dates 2015–2026 (Gregorian)
SPRING_FESTIVAL_DAYS = {
    2015: "2015-02-19", 2016: "2016-02-08", 2017: "2017-01-28",
    2018: "2018-02-16", 2019: "2019-02-05", 2020: "2020-01-25",
    2021: "2021-02-12", 2022: "2022-02-01", 2023: "2023-01-22",
    2024: "2024-02-10", 2025: "2025-01-29", 2026: "2026-02-17",
}


def _window_flag(index: pd.DatetimeIndex, days_before=10, days_after=5) -> pd.Series:
    flag = pd.Series(False, index=index)
    for year, sf in SPRING_FESTIVAL_DAYS.items():
        sf_date = pd.Timestamp(sf)
        # use nearest trading day
        idx_year = index[(index.year == year)]
        if idx_year.empty:
            continue
        before_mask = (idx_year < sf_date) & (idx_year >= sf_date - pd.Timedelta(days=days_before * 2))
        after_mask = (idx_year >= sf_date) & (idx_year <= sf_date + pd.Timedelta(days=days_after * 2))
        before = idx_year[before_mask][-days_before:]
        after = idx_year[after_mask][:days_after]
        flag.loc[before] = True
        flag.loc[after] = True
    return flag


@register(META.id)
def compute() -> Result:
    csi = load_price("CSI300")
    pos = _window_flag(csi.index).astype(float)
    csi_ret = daily_returns(csi)
    y = load_macro_value("DGS3MO").reindex(csi.index).ffill()
    cash = (y / 100.0 / 252.0).fillna(0.0)
    strat = switching_returns(pos, csi_ret, cash)
    bench = {"csi300_buy_hold": csi_ret, "cash_3m": cash}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]))
    return Result(
        meta=META, primary_series=pos.rename("sf_window"),
        asset_series=csi, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes=f"in-market days: {int(pos.sum())}; window: 10d pre / 5d post 春节",
    )
