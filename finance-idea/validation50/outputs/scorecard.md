# Scorecard

## Verdict tally
| our_verdict | count |
|---|---|
| confirmed | 13 |
| decayed | 11 |
| null | 16 |
| skipped | 5 |
| surprise+ | 3 |
| surprise- | 2 |

## Top 5 positive surprises (highest Sharpe edge over benchmark)
| id | family | lit | ours | sharpe gap | strat CAGR |
|---|---|---|---|---|---|
| `csi300_sma250_timing` | trend | mixed | **surprise+** | +0.33 | 11.51% |
| `northbound_flow` | sentiment | mixed | **surprise+** | +0.27 | 5.80% |
| `cn_spring_festival` | seasonal | mixed | **surprise+** | +0.24 | 2.20% |
| `pf_permanent` | allocation | robust | **confirmed** | +0.07 | 5.79% |
| `tsmom_proxy` | trend | robust→decay | **confirmed** | +0.07 | 5.30% |

## Top 5 negative surprises (worst Sharpe gap vs benchmark)
| id | family | lit | ours | sharpe gap | strat CAGR |
|---|---|---|---|---|---|
| `short_reversal_sectors` | mean_reversion | decayed | **confirmed** | -1.12 | -8.40% |
| `santa_rally` | seasonal | seasonal-window-only | **surprise-** | -0.73 | -0.03% |
| `sector_xsmom` | trend | mixed | **decayed** | -0.50 | 0.75% |
| `csi300_sma250_dipbuy` | trend | mixed | **decayed** | -0.46 | -2.82% |
| `spy_sma200_dipbuy` | trend | decayed | **confirmed** | -0.37 | 4.88% |

## Per-strategy (sorted by family)
| id | family | name_cn | lit | ours | total | sharpe | maxdd | why |
|---|---|---|---|---|---|---|---|---|
| `factor_lowvol` | allocation | 低波因子 USMV | robust | **decayed** | 138.19% | 0.60 | -33.10% | strat sharpe +0.60 vs bench +0.73 (Δ=-0.13); CAGR Δ=-4.14% |
| `factor_quality` | allocation | 质量因子 QUAL | robust | **confirmed** | 246.71% | 0.70 | -34.06% | strat sharpe +0.70 vs bench +0.73 (Δ=-0.03); CAGR Δ=-0.52% |
| `pf_60_40` | allocation | 60/40 股债组合 年度再平衡 | robust | **confirmed** | 116.48% | 0.67 | -21.92% | strat sharpe +0.67 vs bench +0.73 (Δ=-0.06); CAGR Δ=-5.04% |
| `pf_all_weather` | allocation | Dalio All Weather | robust→decay | **decayed** | 55.29% | 0.50 | -23.97% | strat sharpe +0.50 vs bench +0.73 (Δ=-0.23); CAGR Δ=-8.12% |
| `pf_golden_butterfly` | allocation | Golden Butterfly | robust | **confirmed** | 74.66% | 0.79 | -19.75% | strat sharpe +0.79 vs bench +0.76 (Δ=+0.03); CAGR Δ=-6.42% |
| `pf_permanent` | allocation | Harry Browne 永久组合 | robust | **confirmed** | 89.57% | 0.81 | -17.61% | strat sharpe +0.81 vs bench +0.73 (Δ=+0.07); CAGR Δ=-6.29% |
| `pf_risk_parity` | allocation | 等风险贡献 (反波动) RP | mixed | **null** | 101.84% | 0.73 | -20.48% | strat sharpe +0.73 vs bench +0.77 (Δ=-0.04); CAGR Δ=-0.71% |
| `btc_gold_zscore` | cross_asset | BTC/黄金 情绪 z | mixed | **decayed** | 49.45% | 0.37 | -19.68% | strat sharpe +0.37 vs bench +0.73 (Δ=-0.36); CAGR Δ=-8.47%; bucket monotonic ok=False |
| `eem_spy_ratio` | cross_asset | EEM/SPY 相对强度 z | mixed | **null** | 167.78% | 0.56 | -32.59% | strat sharpe +0.56 vs bench +0.56 (Δ=-0.00); CAGR Δ=+0.24%; bucket monotonic ok=True |
| `gold_silver_ratio` | cross_asset | 金银比 (GLD/SLV) 极值 | mixed | **null** | 78.06% | 0.78 | -11.89% | strat sharpe +0.78 vs bench +0.73 (Δ=+0.05); CAGR Δ=-6.87%; bucket monotonic ok=True |
| `iwm_spy_zscore` | cross_asset | IWM/SPY 相对强度 z | mixed | **null** | 206.51% | 0.59 | -40.09% | strat sharpe +0.59 vs bench +0.60 (Δ=-0.01); CAGR Δ=+0.07%; bucket monotonic ok=True |
| `oil_gold_ratio` | cross_asset | 油金比 (CL/GC) z 极值 | mixed | **null** | 76.35% | 0.61 | -21.78% | strat sharpe +0.61 vs bench +0.73 (Δ=-0.13); CAGR Δ=-6.96%; bucket monotonic ok=False |
| `cape_top_decile` | macro | CAPE 历史最高 10% 减仓 | seasonal-window-only | **skipped** | 0.00% | 0.00 | 0.00% | Shiller CAPE not cached — run data_acq.py --only cape |
| `dxy_6m_em_tilt` | macro | DXY 6 月跌幅 → EEM 加仓 | robust | **confirmed** | 171.08% | 0.57 | -33.22% | strat sharpe +0.57 vs bench +0.56 (Δ=+0.01); CAGR Δ=+0.36%; bucket monotonic ok=True |
| `erp_dividend_yield` | macro | 股票风险溢价 (12M ret - 10Y) 极值 | mixed | **null** | 188.87% | 0.69 | -30.24% | strat sharpe +0.69 vs bench +0.73 (Δ=-0.04); CAGR Δ=-2.29%; bucket monotonic ok=False |
| `gold_copper_zscore` | macro | 金铜比 z-score 极值 | mixed | **null** | 64.58% | 0.65 | -19.82% | strat sharpe +0.65 vs bench +0.73 (Δ=-0.08); CAGR Δ=-7.60%; bucket monotonic ok=False |
| `hy_oas_threshold` | macro | 高收益 OAS > 500bp 转防御 | mixed | **decayed** | 63.81% | 0.50 | -24.48% | strat sharpe +0.50 vs bench +0.73 (Δ=-0.23); CAGR Δ=-7.64%; bucket monotonic ok=False |
| `nfci_positive_defensive` | macro | 芝加哥金融条件 > 0 转防御 | mixed | **null** | 252.65% | 0.74 | -27.37% | strat sharpe +0.74 vs bench +0.73 (Δ=+0.01); CAGR Δ=-0.35% |
| `yc_inversion_defensive` | macro | 10Y-3M 倒挂期间防御 | mixed | **null** | 194.56% | 0.67 | -30.00% | strat sharpe +0.67 vs bench +0.73 (Δ=-0.06); CAGR Δ=-2.10% |
| `yc_resteepen_buy` | macro | 10Y-3M 再陡峭化买入 | mixed | **decayed** | 91.83% | 0.50 | -34.10% | strat sharpe +0.50 vs bench +0.73 (Δ=-0.23); CAGR Δ=-6.17% |
| `bollinger_lower_spy` | mean_reversion | SPY 布林下轨反弹 | mixed | **decayed** | 84.97% | 0.49 | -29.78% | strat sharpe +0.49 vs bench +0.73 (Δ=-0.24); CAGR Δ=-6.51% |
| `connors_rsi2_csi300` | mean_reversion | RSI(2) 沪深300 | mixed | **null** | 161.13% | 0.37 | -49.29% | strat sharpe +0.37 vs bench +0.35 (Δ=+0.02); CAGR Δ=-1.59%; bucket monotonic ok=False |
| `connors_rsi2_spy` | mean_reversion | Larry Connors RSI(2) SPY | decayed | **confirmed** | 103.10% | 0.74 | -18.12% | strat sharpe +0.74 vs bench +0.73 (Δ=+0.01); CAGR Δ=-5.64%; bucket monotonic ok=False |
| `csi300_drawdown_10pct` | mean_reversion | 沪深300 从 1Y 高点回撤 10% 买入 | mixed | **null** | 188.52% | 0.31 | -72.30% | strat sharpe +0.31 vs bench +0.35 (Δ=-0.04); CAGR Δ=-1.15% |
| `qqq_50d_breakdown` | mean_reversion | QQQ 跌破 50日均线 3% 反弹 | mixed | **null** | 289.33% | 0.77 | -27.37% | strat sharpe +0.77 vs bench +0.90 (Δ=-0.13); CAGR Δ=-6.11% |
| `short_reversal_sectors` | mean_reversion | 11 行业 1 月反转 | decayed | **confirmed** | -50.05% | -0.49 | -60.91% | strat sharpe -0.49 vs bench +0.63 (Δ=-1.12); CAGR Δ=-18.75% |
| `spy_50d_breakdown` | mean_reversion | SPY 跌破 50日 3% 反弹 | mixed | **null** | 125.57% | 0.58 | -29.46% | strat sharpe +0.58 vs bench +0.73 (Δ=-0.15); CAGR Δ=-4.65% |
| `spy_drawdown_10pct` | mean_reversion | SPY 从近 1Y 高点回撤 10% 买入 | mixed | **null** | 168.04% | 0.65 | -28.74% | strat sharpe +0.65 vs bench +0.73 (Δ=-0.09); CAGR Δ=-3.01% |
| `cn_spring_festival` | seasonal | A 股春节前后效应 | mixed | **surprise+** | 66.81% | 0.59 | -12.27% | strat sharpe +0.59 vs bench +0.35 (Δ=+0.24); CAGR Δ=-3.56% |
| `prefomc_drift` | seasonal | Pre-FOMC 漂移 | decayed | **skipped** | 0.00% | 0.00 | 0.00% | FOMC schedule not in cache — would need calendar from Federal Reserve site |
| `santa_rally` | seasonal | Santa Claus Rally | seasonal-window-only | **surprise-** | -0.34% | 0.00 | -7.23% | strat sharpe +0.00 vs bench +0.73 (Δ=-0.73); CAGR Δ=-12.10% |
| `sell_in_may` | seasonal | Sell in May 季节性 | seasonal-window-only | **surprise-** | 75.66% | 0.42 | -34.10% | strat sharpe +0.42 vs bench +0.73 (Δ=-0.31); CAGR Δ=-6.99% |
| `turn_of_month` | seasonal | 月末效应 | seasonal-window-only | **null** | 74.96% | 0.67 | -14.64% | strat sharpe +0.67 vs bench +0.73 (Δ=-0.07); CAGR Δ=-7.03% |
| `aaii_bearish_60` | sentiment | AAII 散户极度看空反指 | seasonal-window-only | **skipped** | 0.00% | 0.00 | 0.00% | AAII sentiment CSV not yet dropped to validation50/data_drops/aaii_sentiment.csv |
| `ah_premium_reversion` | sentiment | AH 溢价指数反转 | mixed | **skipped** | 0.00% | 0.00 | 0.00% | AH premium index unavailable — akshare stock_hk_ah_premium_index endpoint broken |
| `northbound_flow` | sentiment | 北向资金 20日累计 → 沪深300 | mixed | **surprise+** | 65.29% | 0.40 | -37.00% | strat sharpe +0.40 vs bench +0.14 (Δ=+0.27); CAGR Δ=+5.28%; bucket monotonic ok=True |
| `put_call_extreme` | sentiment | CBOE 看跌/看涨极值 | mixed | **skipped** | 0.00% | 0.00 | 0.00% | CBOE PCR series not cached — run data_acq.py --only pcr |
| `qdii_premium_reverse` | sentiment | QDII 纳指溢价反指 QQQ | mixed | **null** | 307.81% | 0.86 | -36.69% | strat sharpe +0.86 vs bench +0.93 (Δ=-0.07); CAGR Δ=-5.91%; bucket monotonic ok=False |
| `vix_above_30_buy_spy` | sentiment | VIX > 30 抄底 SPY | robust | **confirmed** | 165.81% | 0.67 | -28.74% | strat sharpe +0.67 vs bench +0.73 (Δ=-0.06); CAGR Δ=-3.09% |
| `vix_above_40_buy_spy` | sentiment | VIX > 40 强抄底 SPY | robust | **decayed** | 85.03% | 0.52 | -32.18% | strat sharpe +0.52 vs bench +0.73 (Δ=-0.21); CAGR Δ=-6.51% |
| `antonacci_gem` | trend | Antonacci GEM 双动量 | robust→decay | **confirmed** | 160.78% | 0.63 | -34.10% | strat sharpe +0.63 vs bench +0.73 (Δ=-0.10); CAGR Δ=-3.28% |
| `csi300_sma250_dipbuy` | trend | 沪深300 250日均线下方持续买入 | mixed | **decayed** | -47.41% | -0.08 | -69.57% | strat sharpe -0.08 vs bench +0.38 (Δ=-0.46); CAGR Δ=-9.32% |
| `csi300_sma250_timing` | trend | 沪深300 250日均线 趋势开关 | mixed | **surprise+** | 1057.42% | 0.71 | -36.38% | strat sharpe +0.71 vs bench +0.38 (Δ=+0.33); CAGR Δ=+5.01%; bucket monotonic ok=True |
| `faber_gtaa5` | trend | Faber GTAA 5 资产 | robust | **decayed** | 32.86% | 0.44 | -10.95% | strat sharpe +0.44 vs bench +0.73 (Δ=-0.29); CAGR Δ=-9.54% |
| `ma_gate_dca` | trend | 200日 SMA 门控定投 | decayed | **confirmed** | 263.61% | 0.74 | -34.10% | strat sharpe +0.74 vs bench +0.74 (Δ=+0.00); CAGR Δ=+0.00% |
| `qdii_basket_mom` | trend | A 股 QDII 篮子动量 | mixed | **decayed** | -3.04% | 0.10 | -50.97% | strat sharpe +0.10 vs bench +0.42 (Δ=-0.32); CAGR Δ=-7.09% |
| `sector_xsmom` | trend | 美股 11 行业横截面动量 | mixed | **decayed** | 6.11% | 0.13 | -27.75% | strat sharpe +0.13 vs bench +0.63 (Δ=-0.50); CAGR Δ=-9.61% |
| `spy_sma200_dipbuy` | trend | SPY 200日均线下方持续买入 | decayed | **confirmed** | 65.58% | 0.42 | -26.29% | strat sharpe +0.42 vs bench +0.78 (Δ=-0.37); CAGR Δ=-8.31%; bucket monotonic ok=False |
| `spy_sma200_timing` | trend | SPY 200日均线 趋势开关 | robust | **confirmed** | 123.56% | 0.71 | -20.29% | strat sharpe +0.71 vs bench +0.78 (Δ=-0.07); CAGR Δ=-5.29%; bucket monotonic ok=False |
| `tsmom_proxy` | trend | 多资产时间序列动量（ETF代理） | robust→decay | **confirmed** | 79.90% | 0.80 | -12.37% | strat sharpe +0.80 vs bench +0.73 (Δ=+0.07); CAGR Δ=-6.77% |