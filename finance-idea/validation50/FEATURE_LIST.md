# 50 Strategy Validation — Feature List

Pulled from 4 deep-research reports (76 candidates → curated to 50).
Each row gets:
- a Python module under `validation50/strategies/<id>.py` exporting `compute()`
- a chart + bucket table + stats under `validation50/outputs/<id>/`
- a single-line verdict in the master scorecard.

## Status legend

| col | meaning |
|---|---|
| `status` | `todo` / `data-needed` / `wip` / `done` / `skipped` |
| `lit_verdict` | what the literature/originator's own claim suggests we'll find: `robust` / `decayed` / `seasonal-window-only` / `mixed` |
| `our_verdict` | filled after backtest — `confirmed` / `decayed` / `surprise+` / `surprise-` / `null` / `skipped` |

`surprise+` = better than literature said; `surprise-` = worse / opposite sign.

## Data acquisition prerequisites

These series need to be added to the cache before some rows can run:

| series | source | needed by |
|---|---|---|
| FRED `T10Y3M`, `T10Y2Y`, `BAMLH0A0HYM2`, `NFCI`, `CFNAI`, `DGS3MO`, `DTWEXBGS` | FRED CSV/API (no key for CSV) | macro rows 26–35 |
| AAII bearish % weekly | manual CSV from aaii.com | row 18 |
| CBOE total / equity put/call | CBOE public CSV | row 19 |
| ETFs: `VEU EFA IEF VNQ DBC BIL BND AGG SHY USMV QUAL MTUM VLUE SPLV VBR IJS GLDM` | yfinance (already in our fetcher) | trend + allocation rows |
| Shiller CAPE | quandl `MULTPL/SHILLER_PE_RATIO_MONTH` or scrape `multpl.com` | rows 30, 49 |
| 国债到期收益率（中债 10Y） | akshare `bond_china_yield` (fix the broken fetcher) | rows 34, 35 |

A new file `validation50/data_acq.py` will pull these on demand and merge into the storage cache (`prices/` or `macro/`).

---

## The 50 strategies

### Family A — Trend / Momentum (10)

| # | id | name_cn | rule (one line) | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 01 | `spy_sma200_timing` | SPY 200日均线 趋势开关 | SPY close > 200d SMA 持仓，否则现金（BIL） | SPY, BIL | robust | tbd | todo |
| 02 | `spy_sma200_dipbuy` | SPY 200日均线下方持续买入 | SPY 跌破 SMA200 期间 DCA，平时持有 | SPY, BIL | decayed | tbd | todo |
| 03 | `csi300_sma250_timing` | 沪深300 250日均线 开关 | CSI300 close > 250d SMA 持仓，否则现金 | CSI300, DGS3MO | mixed | tbd | todo |
| 04 | `csi300_sma250_dipbuy` | 沪深300 250日均线下方持续买入 | CSI300 跌破 SMA250 期间 DCA | CSI300 | mixed | tbd | todo |
| 05 | `faber_gtaa5` | Faber GTAA 5 资产 | 月末判断 SPY/EFA/IEF/VNQ/DBC vs 10M SMA，每个20%权重 | 5 ETFs + SHY | robust | tbd | todo |
| 06 | `antonacci_gem` | Antonacci GEM 双动量 | 12M return SPY vs VEU vs AGG，月度切换 | SPY VEU AGG BIL | robust→decay | tbd | todo |
| 07 | `tsmom_proxy` | 多资产时间序列动量（ETF代理） | 6 个 ETF：12M return > 0 多头，否则现金，月度 | SPY, EFA, EEM, AGG, GLD, DBC | robust→decay | tbd | todo |
| 08 | `sector_xsmom` | 美股 11 行业横截面动量 | 11 个 SPDR 行业 12-1 月动量，长前3短后3，月度 | XLK XLF XLE XLY XLP XLV XLI XLU XLB XLRE XLC | mixed | tbd | data-needed |
| 09 | `qdii_basket_mom` | A 股 QDII 篮子动量 | 7 只 QDII：12M return 排序，长前 3，月度 | QDII513100…7 只 | mixed | tbd | todo |
| 10 | `ma_gate_dca` | 200日 SMA 门控定投 | 每月新现金仅在 SPY < SMA200 时投入 | SPY, BIL | decayed | tbd | todo |

### Family B — Mean Reversion / Oversold (8)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 11 | `connors_rsi2_spy` | Larry Connors RSI(2) SPY | SPY > SMA200 且 RSI(2) < 5 买；RSI(2) > 65 卖 | SPY | decayed | tbd | todo |
| 12 | `connors_rsi2_csi300` | RSI(2) 在沪深300 | 同上但 CSI300 + SMA250 | CSI300 | mixed | tbd | todo |
| 13 | `bollinger_lower_spy` | SPY 布林下轨反弹 | close 跌破 (SMA20 − 2σ) 后买入，回到中轨平 | SPY | mixed | tbd | todo |
| 14 | `short_reversal_sectors` | 11 行业 1 月反转 | 月末按上月回报排序，长后 3 短前 3，下月持仓 | 11 SPDR sectors | decayed | tbd | data-needed |
| 15 | `qqq_50d_breakdown` | QQQ 跌破 50日均线 N% 反弹 | close 跌破 SMA50 超 3% 后买入，目标 20 日 | QQQ | mixed | tbd | todo |
| 16 | `spy_50d_breakdown` | SPY 跌破 50日 N% 反弹 | 同上 | SPY | mixed | tbd | todo |
| 17 | `spy_drawdown_10pct` | SPY 从近 1Y 高点回撤 10% 买入 | trailing-high - 10%/20% 触发 DCA | SPY | mixed | tbd | todo |
| 18 | `csi300_drawdown_10pct` | 沪深300 从 1Y 高点回撤 10% 买入 | 同上 | CSI300 | mixed | tbd | todo |

### Family C — Sentiment Contrarian (7)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 19 | `vix_above_30_buy_spy` | VIX > 30 抄底 SPY | VIX close > 30 当日买，持有 1/3/6/12M | VIX, SPY | robust | tbd | todo |
| 20 | `vix_above_40_buy_spy` | VIX > 40 抄底 SPY | VIX close > 40 强信号版本 | VIX, SPY | robust | tbd | todo |
| 21 | `qdii_premium_reverse` | QDII 纳指溢价反指 QQQ | QDII 溢价中位数 > p90 平仓 QQQ | QDII NAV + QQQ | mixed | tbd | todo |
| 22 | `northbound_flow` | 北向资金 20日累计 → 沪深300 | 20d 累计净流入 > 0 持沪深300 | 北向 + CSI300 | mixed | tbd | todo |
| 23 | `ah_premium_reversion` | AH 溢价指数反转 | 溢价 z-score 极值时切 A/H | AH index + ETF510300/510900 | mixed | tbd | data-needed |
| 24 | `aaii_bearish_60` | AAII 散户极度看空反指 | AAII Bearish > 60% 当周买 SPY | AAII weekly | seasonal-window-only | tbd | data-needed |
| 25 | `put_call_extreme` | CBOE 看跌/看涨极值 | 10d MA Put/Call > 1.10 买 SPY | CBOE PCRATIO | mixed | tbd | data-needed |

### Family D — Macro Regime (8)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 26 | `yc_inversion_defensive` | 10Y-3M 倒挂期间防御 | T10Y3M < 0 时 SPY 仓位降至 50% | TNX IRX SPY | mixed | tbd | todo |
| 27 | `yc_resteepen_buy` | 10Y-3M 再陡峭化买入 | 倒挂后再回到 > 0 时全仓 SPY 12 月 | TNX IRX SPY | mixed | tbd | todo |
| 28 | `hy_oas_threshold` | 高收益 OAS > 500bp 转防御 | BAMLH0A0HYM2 > 500 切到 IEF | HY OAS + SPY + IEF | mixed | tbd | data-needed |
| 29 | `dxy_6m_em_tilt` | DXY 6 月跌幅 → EEM 加仓 | DXY 6m < -5% EEM 加仓；> 5% 减 | DXY EEM | robust | tbd | todo |
| 30 | `cape_top_decile` | CAPE 历史最高 10% 减仓 | Shiller CAPE > 历史 90 分位时降至 50% 仓位 | CAPE | seasonal-window-only | tbd | data-needed |
| 31 | `nfci_positive_defensive` | 芝加哥金融条件 > 0 转防御 | NFCI > 0 减仓至 50% | NFCI + SPY | mixed | tbd | data-needed |
| 32 | `erp_dividend_yield` | 股票风险溢价 > 4% 加仓 | 股息率 - 10Y > 4% 加仓 SPY | SPY div + DGS10 | mixed | tbd | data-needed |
| 33 | `gold_copper_zscore` | 金铜比 z-score 极值 | z > 1.5 风险偏好下；z < -1.5 风险偏好上 | GC HG SPY | mixed | tbd | todo |

### Family E — Cross-Asset Ratios (5)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 34 | `iwm_spy_zscore` | IWM/SPY 相对强度 z | z 极值时旋转大小盘 | IWM SPY | mixed | tbd | todo |
| 35 | `btc_gold_zscore` | BTC/黄金 情绪 z | ln(BTC/GLD) z 极值后 SPY 前向 | BTC GLD SPY | mixed | tbd | todo |
| 36 | `gold_silver_ratio` | 金银比极值 | GC/SI > 90 风险厌恶；< 50 风险偏好 | GC SLV SPY | mixed | tbd | todo |
| 37 | `oil_gold_ratio` | 油金比 | CL/GC 极值与 SPY 关系 | CL GC SPY | mixed | tbd | todo |
| 38 | `eem_spy_ratio` | EEM/SPY 相对强度 | 比值 z 极值后转向 | EEM SPY | mixed | tbd | todo |

### Family F — Seasonal / Calendar (5)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 39 | `sell_in_may` | Sell in May | 11/1 入 SPY，4/30 出，余 6 月持现金 | SPY BIL | seasonal-window-only | tbd | todo |
| 40 | `santa_rally` | Santa Claus Rally | 12 月末 5 + 1 月初 2 共 7 日持仓 | SPY | seasonal-window-only | tbd | todo |
| 41 | `turn_of_month` | 月末效应 | 每月末倒数 1 至次月正 3 共 4 日持仓 | SPY | seasonal-window-only | tbd | todo |
| 42 | `prefomc_drift` | Pre-FOMC 漂移 | FOMC 日前 24 小时持仓 SPY | SPY + FOMC schedule | decayed | tbd | data-needed |
| 43 | `cn_spring_festival` | A 股春节前后效应 | 春节前后 N 个交易日持沪深300 | CSI300 | mixed | tbd | todo |

### Family G — Allocation Portfolios (7)

| # | id | name_cn | rule | data | lit_verdict | our_verdict | status |
|---|---|---|---|---|---|---|---|
| 44 | `pf_60_40` | 60/40 股债组合 | 60% SPY + 40% AGG，年度 rebal | SPY AGG | robust (benchmark) | tbd | todo |
| 45 | `pf_permanent` | Harry Browne 永久组合 | 25% SPY + 25% TLT + 25% BIL + 25% GLD | SPY TLT BIL GLD | robust | tbd | todo |
| 46 | `pf_golden_butterfly` | Golden Butterfly | 20% × {SPY, IJS, SHY, TLT, GLDM} | SPY IJS SHY TLT GLD | robust | tbd | todo |
| 47 | `pf_all_weather` | Dalio All Weather | 30% SPY + 40% TLT + 15% IEF + 7.5% GLD + 7.5% DBC | SPY TLT IEF GLD DBC | robust→decay | tbd | todo |
| 48 | `pf_risk_parity` | 等风险贡献 RP | 反向波动率加权 SPY/TLT/GLD/DBC | SPY TLT GLD DBC | mixed | tbd | todo |
| 49 | `factor_lowvol` | 低波因子 USMV | 长 USMV 与 SPY 对比 | USMV SPY | robust | tbd | todo |
| 50 | `factor_quality` | 质量因子 QUAL | 长 QUAL vs SPY | QUAL SPY | robust | tbd | todo |

---

## Validation pipeline per strategy

Each `compute()` returns:

```python
{
    "id": "...",
    "name_cn": "...",
    "family": "...",
    "primary_series": pd.Series,       # the signal value over time
    "asset_series": pd.Series,         # the underlying we trade
    "strategy_returns": pd.Series,     # daily P&L when applying rule
    "benchmark_returns": dict[str, pd.Series],  # {"buy_hold": ..., "dca": ..., "tbill": ...}
    "buckets": pd.DataFrame,           # quintile fwd-return table
    "stats": {"cagr", "sharpe", "maxdd", "total"},
    "vs_dca_excess_cagr": float,
    "verdict": "confirmed" | "decayed" | "surprise+" | "surprise-" | "null",
    "verdict_why": "...",
}
```

A driver script `validation50/run_all.py` iterates the 50, writes one PNG + one .md per id under `outputs/<id>/`, and produces a final `outputs/scorecard.md` with:
- count by `our_verdict`
- top-5 biggest "surprise" cases ranked by gap between literature claim and our result
- short-form narrative explaining the surprises

## Order of operations

1. **Now** — feature list (this file) committed. ✓
2. **Step 1** — implement `validation50/data_acq.py` to fetch FRED + AAII + missing ETFs.
3. **Step 2** — implement `validation50/runner.py` framework (computes benchmarks, stats, plot helpers) + 1 reference strategy (`spy_sma200_timing`) end-to-end.
4. **Step 3** — fan out to remaining 49 strategies (one Python module each, ~30–50 LoC each).
5. **Step 4** — generate scorecard + surprise narrative.

This document is the source of truth — every row's `status` and `our_verdict` field is updated as we go.
