# A Dual-Track Quant Survey of 28 Market-Timing & Systematic Equity Strategies (US + China A-Shares, 2026)

## TL;DR
- For a 2026 retail quant who is fee-, tax-, and complexity-aware, **only three of the 28 strategies are unambiguously robust net of costs**: (i) trend filters on broad equity indices (Faber 10-month / 200-day SMA), (ii) diversified time-series momentum à la Moskowitz–Ooi–Pedersen, and (iii) an unleveraged all-weather/Golden Butterfly-style allocation — all three are reproducible with `yfinance`+`FRED`+`akshare` only.
- The most-celebrated single-name "buy signals" (VIX>40, AAII bears>60, Santa, pre-FOMC drift) have **either decayed or are statistical artefacts** at the published thresholds — they remain useful as risk filters but should not drive sizing decisions; in particular, Kurov–Wolfe–Gilbert (2021) document that the Lucca–Moench pre-FOMC drift "essentially disappeared after 2015."
- For a China A-share investor, the **20% capital-gains framework does NOT apply to listed-share trading gains by individuals** (those are exempt per PwC 2025: "Capital gains from transfer of shares traded on the Shanghai, Shenzhen, and Beijing Stock Exchanges are generally exempt from IIT") — so high-turnover strategies (Connors RSI(2), PEAD, J-T momentum, turn-of-month) are *more* tax-viable in China than in a US taxable account; the binding constraints in CN are stamp duty (0.05% sell side, August 2023 cut from 0.10%), commissions, and T+1 settlement.

---

## Key Findings

1. **Trend filters dominate**: Faber's 10-month SMA, MOP time-series momentum, and Antonacci GEM are the only three timing strategies with both a peer-reviewed primary source AND independent positive out-of-sample re-tests through 2025.
2. **Mean-reversion edges decayed**: Connors RSI(2) on SPY, AAII >60% bears, and the turn-of-the-month effect have weakened materially after 2010 in independent re-tests.
3. **Calendar effects are largely artefacts**: Sell-in-May (Maberly–Pierce 2004 rebuttal: vanishes after dropping Oct-1987 and Aug-1998), and pre-FOMC (Kurov–Wolfe–Gilbert 2021: gone post-2015, mean 0.092% vs 0.445% pre-2016).
4. **Allocation strategies (Permanent / Golden Butterfly / All-Weather / 60-40)** lose less return than market-timers and survive both tax regimes; they are the safest defaults.
5. **A-share reproducibility**: All but two strategies (HY OAS, CNN F&G) are reproducible in China using `akshare` because A-share OHLCV, CSI 300, and CGB yield curve are all free; the missing piece is a clean PEAD earnings-surprise feed.
6. **Tax kills high-turnover strategies in US taxable accounts** (RSI(2), J-T momentum, PEAD, turn-of-month) but is *neutral* in China for listed-share gains.

---

## Details

# FAMILY A — Trend / Momentum

## 1. SPX above/below 200-day SMA (timing rule)
**Originator & source**: Popularized as a practitioner rule for decades; first rigorously tested in Brock, Lakonishok & LeBaron (1992, *Journal of Finance* "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns"), then formalized by Faber (2007). Faber paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
**Rules**: Universe = S&P 500 total return (SPY) or CSI 300 (`ak.index_zh_a_hist(symbol="000300")`). Compute 200-day simple moving average on daily close. **Long if close > 200-d SMA, else hold T-bills (FRED DGS3MO) or money-market**. Rebalance daily check, monthly trade. Cost assumption: 0.05% one-way.
**Original claim**: Faber (2007, p. 17, using 10-month SMA — the monthly analog) — S&P timing 1900–2005: CAGR 10.66% vs B&H 9.75%; volatility 17.87% vs 22.36%; max DD −50.31% vs −83.46% (in-sample).
**Out-of-sample**: Faber's 2013 update through 2012 confirmed bond-like drawdowns with equity-like returns; Gabriel-Pagani-Zarattini (2025, SSRN 5230603) re-test through March 2025 confirms drawdown reduction persists but excess return over B&H has compressed since 2009.
**Vs benchmarks**: Faber explicitly compares to SPY B&H; **vs DCA**: backtest 1990-01-01 to 2025-12-31 SPY TR vs equal-dollar monthly DCA, costs 0.05%, T-bill from FRED DGS3MO; **vs cash**: dominant since SPY TR ≫ 3M T-bill.
**Tax/cost**: US — survives 0.05% slippage but whipsaws trigger short-term gains; rough penalty 1.5–2.5%/yr in taxable accts. CN — survives entirely (listed A-share gains exempt); only stamp 0.05% + commission.
**Implementation**: SPY/VOO; CN: 510300.SH (Huatai-PB CSI 300 ETF), 510050.SH. Data: yfinance `^GSPC`, akshare `index_zh_a_hist`.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Robust as risk filter**.

## 2. Faber GTAA (10-month SMA, 5 asset classes)
**Originator**: Mebane Faber, 2007 *Journal of Wealth Management*; SSRN 962461. https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf
**Rules**: Equal-weight 5 sleeves — US equities (VTI/SPY), foreign developed (VEU/EFA), bonds (IEF/AGG), REITs (VNQ), commodities (DBC/GSG). Each sleeve held only if **price > 10-month SMA**, else that 20% goes to T-bills. Rebalance month-end. Costs ~0.05%.
**Original claim**: Faber (2007), 1973–2005 backtest: CAGR 11.27% (timing) vs 9.96% (B&H 5-asset equal-weight); volatility 6.87% vs 9.74%; Sharpe 0.79 vs 0.51; max DD −9.53% vs −38.65%.
**Out-of-sample**: Faber's 2013 update (SSRN 962461, p. 30): real-time 2006–2012 produced "equity-like returns with bond-like volatility and drawdowns." Gabriel-Pagani-Zarattini 2025 update through March 2025 (SSRN 5230603) confirms but with reduced edge post-2010.
**Vs benchmarks**: Faber benchmarks vs 5-asset B&H; **vs SPY DCA**: backtest 1990–2025 with monthly equal-dollar DCA; **vs cash**: clearly dominant historically.
**Tax/cost**: US — modest turnover (≈200%/yr aggregate when including in/out signals); harvest in tax-deferred. CN — would require A-share, CN gov bond ETF (511010), CN gold ETF (518880), and a commodity proxy.
**Availability**: All US ETFs; CN has functional equivalents.
**akshare+yfinance+FRED only?**: **Yes** (US); **Partial** for full GTAA in CN due to missing commodity ETF coverage in akshare for some series.
**Verdict**: **Robust**.

## 3. Antonacci Dual Momentum (GEM)
**Originator**: Gary Antonacci, *Dual Momentum Investing* (McGraw-Hill, 2014); SSRN 2042750 "Risk Premia Harvesting Through Dual Momentum". https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750
**Rules**: Monthly: compute 12-month total return of S&P 500, MSCI ACWI ex-US, and T-bill. If best of (US, ex-US) > T-bill, hold the better; else hold Barclays US Aggregate. Hold 100% of one asset, rebalance monthly.
**Original claim**: Antonacci ("Risk Premia Harvesting") 1974–2011: GEM CAGR 17.43% vs MSCI World 8.85%; Sharpe 0.87 vs 0.30; max DD −22.7% vs −54.0%.
**Out-of-sample**: Antonacci Medium post (through ~2017) shows ≈14% CAGR; Newfound Research "Fragility Case Study: Dual Momentum GEM" (Hoffstein, blog.thinknewfound.com) shows the strategy is highly sensitive to lookback choice. Live AllocateSmartly tracking 2013–2024 shows ≈8–9% live CAGR — **>30% gap vs in-sample claim, flag**.
**Vs benchmarks**: Antonacci compares vs MSCI World and 60/40; **vs SPY DCA 1990–2025**: backtest at monthly frequency, T-bill DGS3MO.
**Tax/cost**: US — switches infrequent (≈1-2/yr) so LT-gain treatment achievable. CN — A-share listed-share gains exempt; would have to substitute CSI 300 for SPX and ACWI proxy via QDII ETF (513100 NASDAQ, 513500 S&P).
**Availability**: SPY, VEU, BIL, BND. CN: 510300, QDII funds (limited).
**akshare+yfinance+FRED only?**: **Yes** for US; **Partial** for CN (QDII NAV via akshare `fund_etf_hist_em`).
**Verdict**: **Decayed but usable as risk filter**.

## 4. Time-Series Momentum (CTA-style)
**Originator**: Moskowitz, Ooi, Pedersen, "Time Series Momentum," *Journal of Financial Economics* 104 (2012), 228–250. https://www.sciencedirect.com/science/article/pii/S0304405X11002613 (PDF: http://docs.lhpedersen.com/TimeSeriesMomentum.pdf)
**Rules**: 58 futures (equity indices, FX, commodities, bonds). For each: sign(past 12m excess return); volatility-scale each position to target 40% annualized vol; equal-weight across instruments; monthly rebal.
**Original claim**: 1985–2009: diversified TSMOM gross Sharpe ≈ 1.58 (Table 4, MOP 2012); alpha 17.8% annualized vs Fama-French + AMP factors.
**Out-of-sample**: Hurst, Ooi & Pedersen (2017, *Journal of Portfolio Management* 44(1), pp. 15–29) "A Century of Evidence on Trend Following" extended 1880–2016: a 20% allocation to time-series momentum **"improved Sharpe ratios from 0.39 to 0.55 while reducing maximum drawdowns from −62.3% to −50.2%"** (figures are gross of fee, gross of cost). Huang, Li, Wang, Zhou (2020, *JFE* "Time-Series Momentum: Is It There?") show that excluding the 1980s, the edge is statistically marginal for many sub-asset classes — material decay vs original Sharpe 1.58, flag.
**Vs benchmarks**: MOP do not benchmark vs SPY/DCA; backtest 1990–2025 of diversified futures TSMOM portfolio vs SPY TR DCA, T-bill DGS3MO.
**Tax/cost**: US — futures get 60/40 §1256 treatment (favorable). CN — retail futures access restricted (need 500k RMB).
**Availability**: Retail proxy via DBMF, KMLM ETFs.
**akshare+yfinance+FRED only?**: **Partial** — equity-only single-index TSMOM yes via yfinance; full 58-instrument basket needs paid futures data.
**Verdict**: **Robust at portfolio level, decayed at single-asset**.

## 5. Carhart UMD (momentum factor)
**Originator**: Mark Carhart, "On Persistence in Mutual Fund Performance," *Journal of Finance* 52 (1997), 57–82. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1997.tb03808.x
**Rules**: Sort US stocks by past 11-month return (skip most recent month); long top 30%, short bottom 30%; value-weight; monthly rebal. The "UMD" factor available on Ken French Data Library.
**Original claim**: Carhart 1963–1993: UMD ~0.82%/month (~10.3% annualized) before costs.
**Out-of-sample**: Asness, Frazzini, Israel & Moskowitz (2014, "Fact, Fiction, and Momentum Investing", https://www.aqr.com) confirm persistence globally; however Israel & Moskowitz (2013, *JFE*) and Novy-Marx (2015) show the spread has compressed and is concentrated in small caps. French data 2010–2024 UMD ≈ 2-3%/yr gross. Daniel & Moskowitz (2016, *JFE* "Momentum Crashes") document −80% momentum crashes in 1932 and 2009.
**Vs benchmarks**: Long-short factor; requires shorting. Long-only top-decile vs SPY DCA: backtest required.
**Tax/cost**: US — high turnover (≈200%/yr), short-term gains; largely unworkable in taxable acct. CN — A-share short-selling restricted; long-only momentum is workable, exempt gains.
**Availability**: MTUM ETF (long-only large-cap momentum). CN: long-only CSI momentum factor via 159939 etc.
**akshare+yfinance+FRED only?**: **Partial** — replicating from stock-level returns yes (akshare provides A-share OHLCV); Ken French series free but not via these libraries.
**Verdict**: **Decayed but usable as long-only factor sleeve**.

## 6. PEAD (post-earnings-announcement drift)
**Originator**: Bernard & Thomas, "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?", *Journal of Accounting Research* 27 (1989), 1–36. JSTOR 2491062 (named effect, building on Ball & Brown 1968).
**Rules**: Compute SUE (Standardized Unexpected Earnings) on each earnings release. Long top-decile SUE, short bottom-decile, hold 60 trading days, equal-weight, ~1 cycle per quarter.
**Original claim**: Bernard & Thomas (1989): top-minus-bottom SUE decile spread ≈ 18%/year over 60 days post-announcement, 1974–1986, robust to risk-adjustment.
**Out-of-sample**: Chordia, Goyal, Sadka, Sadka & Shivakumar (2009, *FAJ*) show PEAD persists but alphas drop by ~50% post-decimalization (2001) once trading costs are included. Fink (2021) review confirms drift exists but exploitable spread is ≈4-6% over 63 days for liquid stocks.
**Vs benchmarks**: Always benchmarked vs Fama-French model; backtest vs SPY DCA required.
**Tax/cost**: US — short-term gains kill it in taxable acct. CN — exempt, but A-share earnings calendar/SUE data is harder to clean.
**Availability**: Need earnings surprises feed (paid: I/B/E/S, Compustat). akshare `stock_yjbb_em` gives EPS history.
**akshare+yfinance+FRED only?**: **Partial** for CN; **No** for clean US implementation (need I/B/E/S consensus).
**Verdict**: **Decayed but usable; not retail-friendly**.

## 7. Jegadeesh–Titman Cross-Sectional Momentum
**Originator**: Jegadeesh & Titman, "Returns to Buying Winners and Selling Losers," *Journal of Finance* 48 (1993), 65–91. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
**Rules**: Sort universe (NYSE+AMEX) by past J-month return (J ∈ {3,6,9,12}); long top-decile, short bottom-decile; hold K months; skip 1-week to avoid microstructure.
**Original claim**: J-T (1993) 1965–1989: 6/6 strategy ≈ 0.95%/month long-short, ≈12.0% annualized.
**Out-of-sample**: Jegadeesh & Titman (2001, *JF*) confirm 1990s persistence ≈ 1.39%/month. Asness et al. (2013, *JF* "Value and Momentum Everywhere") show in 8 markets/asset classes. 2000–2010 momentum crash and ongoing decay: Daniel-Moskowitz 2016 documents −80% drawdowns; Israel-Moskowitz 2013 show large-cap momentum spread shrunk to ~3-5%/yr 1980–2011 vs >12% in J-T sample. **>30% decay, flag**.
**Vs benchmarks**: J-T do not benchmark vs B&H; long-short backtest required.
**Tax/cost**: US — short-term, kills it; long-only top-quintile MTUM survives. CN — long-only ranking on A-shares works.
**Availability**: MTUM (US); akshare gives full A-share universe.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed; long-only factor sleeve only**.

---

# FAMILY B — Mean Reversion / Sentiment Contrarian

## 8. VIX > 30/40 buy signal
**Originator**: Practitioner heuristic (Whaley 1993 introduced VIX). Most-cited modern stat is from Wells Fargo Investment Institute, quoted in Motley Fool (Geoffrey Seiler, 2026): "When the VIX climbs above 40, the S&P 500 is, on average, up more than 30% a year later. Meanwhile, since 1990, stocks are up over the next 12 months more than 90% of the time when the VIX hits this level."
**Rules**: When daily close VIX > 40 (or > 30 in softer variant), buy SPY; hold 12 months OR until VIX < 20.
**Original claim**: ~30% average 12-month forward return after VIX > 40 since 1990, ~90% positive rate (Wells Fargo / Motley Fool 2026).
**Out-of-sample**: Signal fires rarely (≈10 days since 1990 cross-40); selection bias is severe — the universe is post-crash regimes. No peer-reviewed paper documents the threshold-rule explicitly; classify as data-mined heuristic.
**Vs benchmarks vs DCA**: backtest 1990–2025 SPY TR, signal=cross above 40, vs equal-dollar monthly DCA, costs 0.05%, T-bill FRED DGS3MO; results path-dependent on a handful of fires.
**Tax/cost**: US — small N of trades means tax is minor. CN — exempt on listed-share gains.
**Availability**: yfinance `^VIX` (1990+, FRED `VIXCLS`). CN has no exchange-traded volatility index with full history; iVIX (000188.SH) was discontinued in 2018.
**akshare+yfinance+FRED only?**: **Yes** for US; **No** for CN (no equivalent live signal).
**Verdict**: **Decayed but usable as risk filter** (don't bottom-tick; average in when VIX > 30).

## 9. Connors RSI(2) Mean Reversion
**Originator**: Larry Connors & Cesar Alvarez, *Short Term Trading Strategies That Work* (TradingMarkets Publishing, 2008/2009).
**Rules**: Universe = SPY (or large-cap stocks). Trade only when price > 200-d SMA. Buy when 2-period RSI < 5 (or <10); exit when close > 5-day SMA. No stop.
**Original claim**: Connors (2008, ch. 9): stocks with 2-period RSI < 5 outperformed the benchmark by +0.13% (1d), +0.13% (2d), +0.62% (1w) on average over 1998–2008.
**Out-of-sample**: Jeff Swanson (EasyLanguageMastery, 2019 update) — strategy in drawdown since 2011 on SPX; Quantitativo (2024) shows vanilla rules now yield "0.50 payoff ratio, not good" and require parallel multi-instrument trading to remain viable. **Edge degradation post-2011, flag**.
**Vs benchmarks**: Connors benchmarks vs B&H; backtest 1990–2025 vs SPY DCA required.
**Tax/cost**: US — multi-trade/month means short-term gains; effectively unworkable in taxable acct. CN — exempt; viable.
**Availability**: yfinance/akshare daily close.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed**; usable in CN tax regime only.

## 10. AAII Bearish Sentiment > 60% (contrarian)
**Originator**: AAII Sentiment Survey (weekly since July 1987); contrarian framing in Charles Rotblut, AAII Journal, "Is the AAII Sentiment Survey a Contrarian Indicator?" https://www.aaii.com/journal/article/is-the-aaii-sentiment-survey-a-contrarian-indicator
**Rules**: When AAII weekly bearish % > 60 (or > 2σ above historical mean ≈ 30%), buy SPY at next week's close; hold 6 months.
**Original claim (verbatim, Rotblut/AAII)**: "On a six-month basis, the S&P 500 rose 60% of the time following a bearish sentiment reading more than two standard deviations above the historical mean. The average and median gains were 2.8% and 5.3%, respectively. On a 12-month basis, the S&P 500 rose 60% of the time, with an average gain of 3.1% and a median gain of 14.3%." Bears > 3σ: 6-month avg 25.8%, median 23.0%.
**Out-of-sample**: AAII (May 2022 update, https://www.aaii.com/latest/article/21781) — bears > 60 had only 4 prior occurrences (Aug 31 1990, Oct 19 1990, Oct 9 2008, Mar 5 2009). The 2022 firing was followed by a ~6-month return roughly flat-to-positive — small N, can't reject decay.
**Vs benchmarks**: AAII publishes avg vs all-period mean (6-mo SPY ≈ 3.7%); 2.8% < average, but median 5.3% > average. Best read as risk filter, not signal.
**Tax/cost**: Few fires/decade; tax neutral.
**Availability**: AAII weekly CSV (free).
**akshare+yfinance+FRED only?**: **No** — requires AAII CSV (free download but not in those libraries). Wrap with `pandas.read_html`.
**Verdict**: **Decayed but usable as risk filter** (median > mean is the real edge).

## 11. Put/Call Ratio Extremes
**Originator**: Marketed by CBOE since 1995; first academic treatment Pan & Poteshman (2006, *RFS* "The Information in Option Volume").
**Rules**: When equity-only put/call ratio > 1.0 (extreme fear) on close, buy SPY; exit on PC < 0.6.
**Original claim**: Pan-Poteshman (2006) used signed order flow and found informed signal; the *retail* put/call > 1.0 heuristic has no canonical primary-source CAGR.
**Out-of-sample**: Multiple practitioner backtests (Bespoke 2010s) show modest positive forward 1–3 month returns but high variance.
**Vs benchmarks vs DCA**: backtest 1995–2025 CBOE PCRATIO CSV vs SPY TR DCA required.
**Tax/cost**: Few signals/yr; tax-neutral.
**Availability**: CBOE put/call (free); CN has no equivalent retail series.
**akshare+yfinance+FRED only?**: **Partial** — CBOE PCRATIO not in those libs; requires CBOE CSV.
**Verdict**: **Publication-bias artefact at the retail level**.

## 12. CNN Fear & Greed Index Extremes
**Originator**: CNN Business proprietary composite (7 sub-indicators); launched 2012.
**Rules**: Buy SPY when index < 20 (extreme fear); exit > 80 (extreme greed).
**Original claim**: No peer-reviewed source. CNN does not publish backtested returns.
**Out-of-sample**: Practitioner blog backtests (e.g., on r/algotrading, Composer.trade) show modest positive 3-month forward returns from <20 readings 2012–2024 but small N.
**Vs benchmarks**: Requires backtest 2012–2025; no published numbers.
**Tax/cost**: Few trades; tax-neutral.
**Availability**: No official API; scrape `production.dataviz.cnn.io/index/fearandgreed/graphdata`.
**akshare+yfinance+FRED only?**: **No** — requires CNN scrape.
**Verdict**: **Publication-bias artefact** (composite of already-published signals).

---

# FAMILY C — Macro Regime

## 13. 10Y–2Y Yield Curve Inversion + Re-Steepen
**Originator**: Estrella & Hardouvelis (1991), and Campbell Harvey's 1986 U. Chicago dissertation (using 5Y–90D). 10Y–3M variant popularized by Estrella & Mishkin (1996) at NY Fed. 10Y–2Y series = FRED T10Y2Y.
**Rules**: Inversion = monthly avg T10Y2Y < 0 for ≥2 consecutive months. Recession follows with median ≈14 month lead time (Eco3min 2026 tracker, citing NBER + FRED). Equity-timing variant: de-risk on inversion; re-risk on first un-inversion AND positive 12m forward equity return.
**Original claim**: NY Fed FAQ (https://www.newyorkfed.org/research/capital_markets/ycfaq): negative 12-mo-ahead recession probability model.
**Out-of-sample**: 2022–2024 was the longest inversion on record and as of May 2026 has not been followed by NBER recession — first major false positive since 1976. Six-of-seven hit rate.
**Vs benchmarks**: As an equity timing signal, backtest 1976–2025 SPY de-risk on inversion required.
**Tax/cost**: Few regime changes; tax-neutral.
**Availability**: FRED `T10Y2Y`, `T10Y3M`. CN: PBoC term structure on Wind/akshare `bond_china_yield`.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed but usable as risk filter** (binary signal, long lead, with growing false-positive risk).

## 14. High-Yield OAS Thresholds
**Originator**: ICE/BofA index (formerly Merrill Lynch HY Master II). FRED `BAMLH0A0HYM2` since Dec 1996. No single seminal academic paper, but Gilchrist & Zakrajšek (2012, *AER* "Credit Spreads and Business Cycle Fluctuations") established credit-spread → activity link via the "GZ spread."
**Rules**: Common thresholds: tight < 300bp (risk-on), monitoring 300–500bp, stress > 500bp, crisis > 800bp. Equity rule: de-risk on a 100bp+ widening over 4 weeks.
**Original claim**: HY OAS peaked at 1988bp on Dec 16, 2008 and 1087bp on Mar 23, 2020 (FRED data). Post-2009 mean ≈ 490bp.
**Out-of-sample**: 2022 rate-hike cycle peak below 600bp despite aggressive Fed tightening; remains a useful but noisier signal in QE/QT regimes.
**Vs benchmarks**: As risk filter, backtest of "long SPY when OAS < 500bp & 12-wk change negative" vs DCA required.
**Tax/cost**: Few regime changes; neutral.
**Availability**: FRED `BAMLH0A0HYM2`. **FRED is sunsetting BofA index publication to 3 years of history starting April 2026** — store snapshots locally.
**akshare+yfinance+FRED only?**: **Yes** (use HYG/JNK proxies if FRED depth lost).
**Verdict**: **Robust as risk filter**.

## 15. DXY / EM Rotation
**Originator**: Practitioner rule; academic basis in Eichengreen & Gupta (2014) on EM vulnerability to dollar strength.
**Rules**: When DXY 6-month change > +5%, underweight EM equities (EEM/MCHI); reverse when DXY 6m < −5%.
**Original claim**: No single canonical CAGR; correlation of DXY-12m to MSCI EM 12m forward roughly −0.4 in 2000s.
**Out-of-sample**: Relationship weaker post-2018 as EM index composition shifted toward tech.
**Vs benchmarks**: Backtest EEM 2003–2025 vs DCA required.
**Tax/cost**: Low turnover (~1-2/yr); friendly.
**Availability**: FRED `DTWEXBGS`, yfinance `DX-Y.NYB`, EEM/MCHI. CN: `ak.fx_spot_quote` for USD/CNY.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed but usable as risk filter**.

## 16. Gold/Copper Ratio Regime
**Originator**: Practitioner indicator popularized by Jeffrey Gundlach (DoubleLine 2010s); no academic paper.
**Rules**: Gold/Copper rising = risk-off (recession proxy). Rule: when 200d trend of Au/Cu ratio rising, underweight equities.
**Original claim**: None peer-reviewed; Gundlach commentary only.
**Out-of-sample**: Correlation to 10Y yield moderately positive but weakened in 2020–2023.
**Vs benchmarks**: Backtest gold (`GC=F`) / copper (`HG=F`) 1990–2025 required.
**Availability**: yfinance. CN: SHFE futures, gold ETF 518880.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Publication-bias artefact** at retail level (no documented edge).

## 17. Credit-Cycle Indicators (composite)
**Originator**: Multiple — Bernanke-Gertler "financial accelerator"; Adrian-Brunnermeier (NY Fed) CoVaR; Chicago Fed NFCI.
**Rules**: Use NFCI (FRED `NFCI`) > 0 = tight conditions → de-risk equities.
**Original claim**: Chicago Fed: NFCI is constructed to be zero-mean unit-variance; positive readings = above-average financial stress. No CAGR claim.
**Out-of-sample**: NFCI consistently fires before 2008, 2020; weaker signal in 2022.
**Vs benchmarks**: Backtest 1990–2025 of long-SPY-when-NFCI<0 vs DCA required.
**Tax/cost**: Low turnover; friendly.
**Availability**: FRED `NFCI`, `ANFCI`. CN: PBoC Financial Conditions Index (not on FRED).
**akshare+yfinance+FRED only?**: **Yes** US; **Partial** CN.
**Verdict**: **Robust as risk filter**.

---

# FAMILY D — Calendar / Seasonal

## 18. Sell in May (Halloween Effect)
**Originator**: Bouman & Jacobsen, "The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle," *American Economic Review* 92 (2002), 1618–1635. DOI 10.1257/000282802762024683.
**Rules**: Long equities Nov–Apr; T-bills May–Oct. Swap month-end.
**Original claim**: Bouman-Jacobsen (2002): Nov–Apr returns significantly higher than May–Oct in 36 of 37 countries, 1970–1998.
**Out-of-sample**: Maberly & Pierce (2004, *Econ Journal Watch*, econjwatch.org/File+download/24/2004-04-maberlypierce-com.pdf): Halloween effect in US "disappears after an adjustment is made for the impact of outliers, in particular the large monthly declines for October 1987 and August 1998" — i.e., it's two data points. Zhang & Jacobsen (2021, *J. Int'l Money & Finance*) re-affirm with 323 years global data showing 5–8.3% Nov–Apr vs May–Oct gap in recent 50 years.
**Vs benchmarks**: Maberly-Pierce explicitly compare to B&H + T-bill swap; even with effect, transaction costs erode most edge.
**Tax/cost**: US — annual rotation = short-term gains; harsh. CN — exempt; viable.
**Availability**: yfinance, akshare.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed/contested in US; persists internationally**.

## 19. Santa Claus Rally
**Originator**: Yale Hirsch, *1972 Stock Trader's Almanac*. Definition: last 5 trading days of December + first 2 trading days of January.
**Rules**: Long SPY for 7-day window; cash otherwise.
**Original claim**: LPL Financial / Stock Trader's Almanac (Dec 24, 2025, https://www.lpl.com/research/blog/will-the-santa-claus-rally-spark-a-bullish-start-to-2026.html): "Since 1950, the S&P 500 has averaged a 1.3% return during this period, with positive results occurring 78% of the time. For comparison, the market's typical seven-day average return is just 0.3%, with a positivity rate of 58%." Hirsch's adage: "If Santa Claus should fail to call, bears may come to Broad and Wall."
**Out-of-sample**: Effect persists through 2024; statistically significant but **economically trivial after costs** (1.0% excess over 7 days = ~50bp net of taxes once a year).
**Vs benchmarks**: 1.3% Santa vs 0.3% normal 7-day → ~1.0% excess; vs DCA equivalent: negligible difference over 35-yr horizon.
**Tax/cost**: One trade/yr; tolerable.
**Availability**: yfinance, akshare. CN A-share has different Lunar New Year seasonality.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Real but trivial**; do not implement as standalone.

## 20. Turn-of-the-Month Effect
**Originator**: Ariel (1987, *JFE*); Lakonishok & Smidt, "Are Seasonal Anomalies Real? A Ninety-Year Perspective," *Review of Financial Studies* 1 (1988), 403–425.
**Rules**: Long SPY last trading day of month + first 3 trading days of next month; cash otherwise.
**Original claim**: L&S (1988): DJIA 1897–1986, 4-day TOM avg cumulative return 0.473% vs full-month 0.349% — i.e., all monthly gain in those 4 days.
**Out-of-sample**: McConnell & Xu (2008, SSRN 917884) confirm 1987–2005 persistence. Quantseeker (2024): "the classical definition of the TOM effect, measured during the [0:3] window as established by Lakonishok and Smidt (1988), has largely disappeared over the past decade, with TOM returns now indistinguishable from returns on other days." Broader [−1,+7] window survives in ETFs ≈ 5–12 bp/day.
**Vs benchmarks**: ~4% annualized excess gross historically; ≈ 0 net of round-trip costs ×12/yr.
**Tax/cost**: US — 24 trades/yr, short-term gains, crushed by costs. CN — exempt.
**Availability**: yfinance, akshare.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed in US since ~2015**.

## 21. Pre-FOMC Drift (Lucca & Moench)
**Originator**: Lucca & Moench, "The Pre-FOMC Announcement Drift," *Journal of Finance* 70 (2015), 329–371. https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12196
**Rules**: Long SPX from close of day before scheduled FOMC to close of FOMC day; cash otherwise.
**Original claim** (verbatim, NY Fed Staff Report 512, https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf): "We document that since 1994, the S&P500 index has on average increased **49 basis points in the 24 hours before scheduled FOMC announcements** … about **80% of annual realized excess stock returns since 1994 are accounted for by the pre-FOMC announcement drift**." Annualized Sharpe **1.14**, sample Sep 1994 – Mar 2011, 131 meetings.
**Out-of-sample**: Kurov, Wolfe & Gilbert (2021), *Finance Research Letters* 40, "The Disappearing Pre-FOMC Announcement Drift" (https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/): "We extend the sample to December 2019. We find that … the pre-FOMC drift **essentially disappeared after 2015**." Specifically: Apr 2011–Dec 2015 mean = 0.445% (consistent with LM); **Jan 2016–Dec 2019 mean = 0.092%** (statistically zero). **>30% decay, flag — strategy DECEASED**.
**Vs benchmarks**: 8 trades/yr × 49bp = ~3.9% in-sample, near zero post-2015.
**Tax/cost**: 8 short-term holds; survivable in IRA only.
**Availability**: yfinance, FRED FOMC calendar.
**akshare+yfinance+FRED only?**: **Yes** for US. No analog in CN (PBoC doesn't operate on FOMC-style schedule).
**Verdict**: **Do not implement** (decayed since 2015).

## 22. End-of-Quarter Window Dressing
**Originator**: Lakonishok, Shleifer, Thaler, Vishny (1991, *JFE* "Window Dressing by Pension Fund Managers"); Ng & Wang (2004, *JFE*).
**Rules**: Long winners / short losers in last 5 days of quarter; reverse first 5 days next quarter.
**Original claim**: Modest small-cap underperformance in last week of quarter; reversal in first week. Effect size ≈ 0.5–1.0%/quarter on factor mimicking portfolios.
**Out-of-sample**: Edge weakened post-2010 with rise of passive flows; mostly a small-cap phenomenon now.
**Vs benchmarks**: Long-short backtest on small-cap winner/loser portfolios required.
**Tax/cost**: 4 trades/yr; tax-tolerable.
**Availability**: yfinance for ETF proxies; full implementation needs stock-level data.
**akshare+yfinance+FRED only?**: **Yes** (use IWM proxy).
**Verdict**: **Publication-bias artefact** at retail scale.

---

# FAMILY E — Allocation / Drawdown Control

## 23. 60/40 Portfolio
**Originator**: Convention dating to Markowitz era; no single paper. Standard "balanced fund" allocation.
**Rules**: 60% SPY (or VTI), 40% AGG (or IEF). Annual rebal.
**Original claim**: Long-run (1928–2024) ≈ 8–9% CAGR, 10–12% vol, max DD −28% (2008) per multiple data providers.
**Out-of-sample**: 2022 was the worst calendar year since 1937 — per Morgan Stanley Investment Management ("Big Picture: Return of the 60/40," 2023): "The 60/40 portfolio…saw a rollercoaster ride down **−17.5% in 2022**…its worst loss since 1937." The stock-bond correlation flipped positive. Asness, Frazzini, Pedersen 2012 critique: "60% of capital ≠ 60% of risk; equities drive ~90% of variance."
**Vs benchmarks**: vs SPY: lower return, much lower DD; vs DCA into SPY: SPY DCA wins on return, 60/40 wins on Sharpe.
**Tax/cost**: Once/yr rebal; LT gains possible.
**Availability**: SPY+BND; CN: 510300 + 511010.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Robust default, but 2022 exposed bond-correlation risk**.

## 24. Permanent Portfolio (Harry Browne)
**Originator**: Harry Browne, *Fail-Safe Investing: Lifelong Financial Security in 30 Minutes* (St. Martin's Press, 1999). 25% US stocks / 25% long Treasuries / 25% cash / 25% gold; rebal when any sleeve drifts to <15% or >35%.
**Original claim**: No CAGR in book; PRPFX mutual fund (1982 inception) is benchmark.
**Out-of-sample**: OnePortfolio (2026) cites 1972–2020: CAGR 9.7%, vol 6.8%, Sharpe ~0.5; max DD ~−13%. PortfolioCharts (Tyler) maintains live tracker. Inferior to S&P over rising-rate eras (1982–2000, post-2009).
**Vs benchmarks vs DCA**: dominates on Sharpe and DD; loses on CAGR vs SPY.
**Tax/cost**: Low turnover; gold ETF (GLD) is taxed as collectible (28%) in US — flag.
**Availability**: VTI, TLT, BIL/SHV, GLD. CN: 510300, 511010, 511880, 518880.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Robust drawdown-control portfolio**.

## 25. Golden Butterfly (Tyler / Portfolio Charts)
**Originator**: "Tyler" (founder of PortfolioCharts.com), September 2015. https://portfoliocharts.com/portfolios/golden-butterfly-portfolio/
**Rules**: 20% US total stock (VTI) / 20% US small-cap value (VIOV) / 20% short-term Treasuries (SHY) / 20% long-term Treasuries (TLT) / 20% gold (GLDM). Annual rebal.
**Original claim**: PortfolioCharts (Tyler) and lazyportfolioetf.com (April 2026, https://www.lazyportfolioetf.com/allocation/golden-butterfly/): trailing 30-yr CAGR **8.05%**, std dev **7.97%**, max DD **−17.79%**, 30 months to recover.
**Out-of-sample**: 2015–2025 live: outperformed expectations especially during 2022 (gold up, TLT down) and 2025 (gold strong); confirmed by Risk Parity Radio live tracker.
**Vs benchmarks vs DCA**: lower CAGR than SPY DCA (~10.5% same window), much lower DD (−17.8% vs −55%), higher Sharpe.
**Tax/cost**: Once/yr rebal; GLDM = collectibles 28%. CN: works via 510300+159922+511010+511880+518880.
**Availability**: 5 ETFs.
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Robust drawdown-control portfolio**.

## 26. All-Weather / Risk Parity (Dalio/Bridgewater; Asness/AQR)
**Originator**: Bridgewater All-Weather, est. 1996 (Dalio/Jensen/Prince). Retail version popularized by Tony Robbins (2014) — 30% stocks / 40% long Treasuries / 15% intermediate Treasuries / 7.5% gold / 7.5% commodities. Academic foundation: Asness, Frazzini, Pedersen, "Leverage Aversion and Risk Parity," *Financial Analysts Journal* 68 (2012). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1990493
**Rules**: As above; annual rebal. Capital weights chosen to ≈ risk-balance four growth/inflation regimes.
**Original claim**: AFP 2012 — risk parity historically outperforms 60/40 on Sharpe due to low-beta anomaly; needs leverage to match equity returns.
**Out-of-sample**: 2008 — S&P 500 lost 37% total return (Institutional Investor 2020); Bridgewater's All Weather fund is widely reported to have lost only ~−3.93% (attributed to Bridgewater publications, independent confirmation limited; PortfoliosLab proxy data show All Weather's worst 2008 month was October at −8.3% and best was December at +9.1%, consistent with a roughly flat-to-small-negative annual result). State Street launched ALLW ETF March 2025; through Jan 2026 ≈ 13.9% TR (small sample, fee 0.85%). **2022 was a major drawdown** (−20%+ for unleveraged variants) as bonds+stocks fell together.
**Vs benchmarks vs DCA**: Lower CAGR than SPY DCA, much lower DD pre-2022; competitive Sharpe.
**Tax/cost**: Low turnover; commodity ETFs (PDBC avoids K-1) and TIPS choice matter.
**Availability**: VTI, TLT, IEI, GLDM, PDBC; or single-ticker ALLW (0.85%) or RPAR (0.50%).
**akshare+yfinance+FRED only?**: **Yes** US; **Partial** CN (commodity sleeve harder).
**Verdict**: **Robust** with caveat that 2022 broke the negative-correlation assumption.

## 27. Magic Formula (Joel Greenblatt)
**Originator**: Joel Greenblatt, *The Little Book That Beats the Market* (Wiley, 2005); updated 2010.
**Rules**: Rank universe (e.g., top 3500 US stocks > $50M cap) by (i) Earnings Yield = EBIT/EV and (ii) Return on Capital = EBIT/(Net WC + Net Fixed Assets). Sum ranks; buy top 30; equal-weight; hold 1 yr; rotate.
**Original claim**: Greenblatt (2005, p. 65): 1988–2004, top-30 portfolio CAGR **30.8%** vs S&P 500 **12.4%**. Top-1000 universe: 22.9%. Underperformed market in ~25% of 1-yr periods, almost never in 5-yr.
**Out-of-sample**: Reasonable Deviations (2020, https://reasonabledeviations.com/2020/06/08/greenblatt-magic-formula/): Jul 2003–Dec 2015, annualized **11.4%** — >60% decay vs in-sample 30.8%, flag. Nordic backtest (HHS, 2010s) confirms positive but reduced edge.
**Vs benchmarks**: Greenblatt vs S&P TR; vs DCA: fresh backtest using free EBIT/EV data required.
**Tax/cost**: Annual turnover ~100%; long-term capital gains possible (hold >12mo). CN: exempt; viable but Chinese accounting data quality varies.
**Availability**: Greenblatt's site magicformulainvesting.com (free screener); fundamentals via Alpha Vantage / FMP / akshare `stock_financial_em`.
**akshare+yfinance+FRED only?**: **Partial** (need fundamentals).
**Verdict**: **Decayed but usable**; expect ~3–5%/yr alpha, not 18%.

## 28. Dogs of the Dow
**Originator**: Michael O'Higgins, *Beating the Dow* (HarperCollins, 1991). Strategy first floated by John Slatter in a 1988 *Wall Street Journal* column.
**Rules**: Each Jan 1, buy equal-dollar amounts of the 10 highest dividend-yield stocks in the DJIA 30; hold 1 yr; rebalance.
**Original claim**: Per Simply Safe Dividends citing S&P Dow Jones Indices: "From 1973 to 1988 the Dogs of the Dow strategy returned **18.4% per year, almost doubling the Dow Jones Industrial Average's 10.9% annualized return**" (Slatter / O'Higgins in-sample).
**Out-of-sample**: Meb Faber (2007): "During the in-sample period the DOGS beat the DJIA in 74% of the years vs. only 36% of the years since 1992." Live tracker dogsofthedow.com: **since the turn of the century the Dogs averaged 8.7% annual total return** (direct-stock implementation, no fees). QuantifiedStrategies.com from August 1998: "A 10,000 investment in S&P 500 (SPY) is worth 60,000 compared to only 32,000 for the Dogs Of The Dow Strategy. The CAGR is **7.7% vs 5%**" (this version includes ALPS ETF fee drag) — >50% decay vs in-sample 18.4%, flag.
**Vs benchmarks**: Originally beat DJIA; in 21st century usually trails SPY because Dow itself trails S&P.
**Tax/cost**: Annual turnover; LT-gain treatment; dividends taxed (qualified rate US).
**Availability**: yfinance for Dow constituents; DOGS ETF (ALPS Sector Dividend Dogs).
**akshare+yfinance+FRED only?**: **Yes**.
**Verdict**: **Decayed**; small-cap value tilt of Magic Formula a better expression of the same idea.

---

# UNIFIED COMPARISON TABLE (1990-01-01 to 2025-12-31 where data permit)

Where the originator did NOT publish numbers over this window, the cell holds the explicit backtest methodology string a downstream backtester can execute. CAGR/Sharpe/maxDD are originator's claims unless suffixed (OOS).

| # | Strategy | CAGR | Sharpe | Max DD | Excess over monthly DCA |
|---|---|---|---|---|---|
| 1 | SPX 200-d SMA | 10.66% (Faber 1900–2005) | n/a | −50.3% | backtest 1990-2025 SPY TR timing vs monthly equal-$ DCA, costs 0.05%, T-bill FRED DGS3MO |
| 2 | Faber GTAA | 11.27% (1973–2005) | 0.79 | −9.5% | backtest 1990-2025 5-asset GTAA vs SPY monthly DCA, costs 0.05%, DGS3MO |
| 3 | Antonacci GEM | 17.43% (1974–2011) | 0.87 | −22.7% | backtest 1990-2025 GEM (SPY/VEU/BIL/AGG) monthly vs SPY DCA, DGS3MO |
| 4 | TSMOM (MOP) | Sharpe 1.58 in-sample (1985–2009); 20% TSMOM overlay lifts Sharpe 0.39→0.55 (Hurst-Ooi-Pedersen 2017) | 1.58 | DD reduced from −62.3% to −50.2% (HOP 2017) | backtest 1990-2025 diversified futures TSMOM (KMLM proxy) vs SPY DCA |
| 5 | Carhart UMD | ~10.3% gross (1963–1993) | n/a | −80% (2009) | backtest 1990-2025 Ken French UMD long-short vs SPY DCA |
| 6 | PEAD | ~18% top-bottom decile (1974–86) | n/a | n/a | backtest 1990-2025 SUE-decile spread (I/B/E/S) vs SPY DCA |
| 7 | J-T momentum | 12% (1965–1989) | n/a | −80% (2009) | backtest 1990-2025 6/6 winners-losers vs SPY DCA |
| 8 | VIX>40 buy | ~30% 12m fwd avg (1990–2024 WF/Motley Fool); 90% positive rate | n/a | n/a | backtest VIX>40 SPY entries 1990-2025 vs SPY DCA |
| 9 | Connors RSI(2) | RSI<5 1wk fwd +0.62% (1998–2008 Connors) | n/a | n/a | backtest RSI(2)<5, SPY>200dma, exit>5dSMA, 1990-2025 vs DCA |
| 10 | AAII bears>60 | 6m avg 2.8%, 12m 3.1% (Rotblut/AAII); 3σ→6m 25.8% | n/a | n/a | backtest AAII bears>60 SPY 6m hold 1987-2025 vs DCA |
| 11 | Put/Call >1 | n/a (no canonical CAGR) | n/a | n/a | backtest CBOE PCRATIO>1 SPY 1-3m hold 1995-2025 vs DCA |
| 12 | CNN F&G <20 | n/a (no published) | n/a | n/a | backtest F&G<20 SPY 3m hold 2012-2025 vs DCA |
| 13 | 2s10s timing | n/a (recession-prob model only) | n/a | n/a | backtest de-risk on T10Y2Y<0, re-risk on un-invert, 1976-2025 |
| 14 | HY OAS filter | n/a (risk filter, not CAGR strategy) | n/a | n/a | backtest long SPY when BAMLH0A0HYM2<500 & d4w<0, 1996-2025 |
| 15 | DXY-EM rotation | n/a | n/a | n/a | backtest EEM tilt on DXY 6m, 2003-2025 vs EEM DCA |
| 16 | Gold/Copper | n/a | n/a | n/a | backtest 200d Au/Cu trend SPY filter 1990-2025 |
| 17 | NFCI<0 filter | n/a | n/a | n/a | backtest long SPY when NFCI<0 1973-2025 vs DCA |
| 18 | Sell in May | Nov–Apr >> May–Oct in 36/37 (B-J 1998); US disappears w/o Oct '87 + Aug '98 (M-P 2004) | n/a | n/a | backtest Halloween swap 1990-2025 SPY vs DCA, costs |
| 19 | Santa Claus | 1.3%/7d avg since 1950, 78% positive (LPL/STA) | n/a | n/a | trivial; backtest 1990-2025 last5+first2 vs DCA |
| 20 | TOM (L&S) | 0.473%/4d (1897–1986); near-zero post-2015 (Quantseeker 2024) | n/a | n/a | backtest [-1,+3] window 1990-2025 SPY vs DCA |
| 21 | Pre-FOMC | 49bp/24h (1994–2011); **9.2bp post-2015 Kurov-Wolfe-Gilbert 2021** | 1.14 in-sample | n/a | backtest FOMC-eve entries 1994-2025 vs DCA |
| 22 | EOQ window-dressing | ~0.5–1%/qtr (LSTV 1991) | n/a | n/a | backtest small-cap last-5 vs first-5 days of qtr 1990-2025 |
| 23 | 60/40 | ~8-9% (1928–2024 indicative); **−17.5% in 2022 (MSIM)** | ~0.5 | −28% (2008); −17.5% (2022) | backtest 60% SPY/40% AGG annual rebal 1990-2025 vs DCA |
| 24 | Permanent Portfolio | 9.7% / vol 6.8% (1972–2020, OnePortfolio) | ~0.5 | ~−13% | backtest 25/25/25/25 SPY/TLT/BIL/GLD 1990-2025 vs DCA |
| 25 | Golden Butterfly | 8.05% / vol 7.97% (30y trailing to Apr 2026, lazyportfolioetf) | ~0.6 | −17.79% | backtest 20×5 1990-2025 |
| 26 | All Weather | ALLW 13.9% (Mar 2025–Jan 2026 small sample); All Weather Fund est. −3.9% in 2008 (Bridgewater attribution, independent confirmation partial) | n/a | ~−20% (2022) | backtest 30/40/15/7.5/7.5 1990-2025 |
| 27 | Magic Formula | **30.8% (1988–2004)**; **11.4% (Jul 2003–Dec 2015 OOS)** | n/a | n/a | backtest top-30 EBIT/EV+ROC 1990-2025 vs SPY DCA |
| 28 | Dogs of the Dow | **18.4% (1973–1988 Slatter/O'Higgins)** vs DJIA 10.9%; since 2000 **8.7%** direct-stock (dogsofthedow.com); **7.7% SPY vs 5% Dogs ETF since Aug 1998** (QuantifiedStrategies) | n/a | n/a | backtest top-10 yield DJIA annual 1990-2025 vs SPY DCA |

---

## Recommendations

**If you only implement 3:**

1. **Faber 10-month SMA / GTAA (Strategy 2)** — best documented timing system with three decades of out-of-sample confirmation, modest turnover (~1-2 sleeve switches/yr), and broad ETF availability in both US (VTI/VEU/AGG/VNQ/DBC) and CN (510300/QDII/511010/512200/proxy). It cut drawdown ~75% historically without sacrificing CAGR. Rebalance month-end.
   - **Threshold that would change this**: if the strategy underperforms B&H by >5%/yr for 5 consecutive years (i.e., a sustained "Faber decay"), demote to risk-filter only.

2. **Golden Butterfly (Strategy 25)** — lowest-maintenance allocation with the best risk-adjusted track record across 1970–2026 of the unleveraged "all-weather" family. The 2022 stress test (where 60/40 lost −17.5%) showed gold's diversification value vs Dalio's bond-heavy version. Annual rebal, 5 ETFs, executable in a Vanguard or Schwab account in 10 minutes/yr.
   - **Threshold that would change this**: a regime change where gold's stock correlation flips positive for >24 months (would invalidate the diversification thesis).

3. **HY OAS + 2s10s as risk filter (Strategies 13+14)** — not a standalone alpha strategy but a free, FRED-only **regime overlay**: pause additional SPY DCA purchases when (HY OAS > 500bp AND widening 4-wk) OR (T10Y2Y has uninverted from sustained inversion in the last 12 months — the historical recession trigger). This is the only signal among the 28 that flags credit stress in real time without lag.
   - **Threshold that would change this**: if 2s10s false-positive rate exceeds 50% over the next two cycles (it's at 1-in-7 today).

**Why not the others?** VIX>40 fires too rarely to drive sizing; Connors RSI/PEAD/J-T momentum get crushed by US taxes; pre-FOMC drift is dead per Kurov-Wolfe-Gilbert 2021; Sell-in-May fails after outliers; the calendar effects are economically trivial; Magic Formula and Dogs decayed >50% out of sample.

**Staged action plan for a US-based dual-track investor:**
- **Month 1**: Set up FRED + yfinance + akshare pipelines; pull `BAMLH0A0HYM2` (cache it — series is sunsetting to 3-yr depth in April 2026), `T10Y2Y`, `DGS3MO`, `VIXCLS`.
- **Month 2**: Build Golden Butterfly in a tax-deferred account (US IRA / 401(k)) to avoid the GLD 28% collectibles tax.
- **Month 3**: Layer Faber GTAA on a separate sleeve (also tax-deferred) sized at 30-50% of risk capital.
- **Month 4**: Code HY-OAS + 2s10s monitoring; pause DCA when both flags fire.
- **Month 6+**: For the China sleeve, mirror Golden Butterfly via 510300+159922+511010+511880+518880; consider adding long-only A-share momentum (top-quintile 12m return rebalanced monthly) since exempt-status makes this tax-viable in CN.

---

## Data Sources Appendix (Python wiring)

### FRED (free, no key for `pandas_datareader`; key needed for `fredapi`)
- `DGS3MO` — 3-month Treasury (cash benchmark)
- `DGS10`, `DGS2` — for 2s10s
- `T10Y2Y`, `T10Y3M` — pre-computed spreads
- `BAMLH0A0HYM2` — ICE BofA HY OAS (history truncating to 3-yr from Apr 2026 — cache locally)
- `VIXCLS` — CBOE VIX
- `NFCI`, `ANFCI` — Chicago Fed financial conditions
- `DTWEXBGS` — broad dollar index
- `DEXCHUS` — USD/CNY
- `CPIAUCSL`, `UNRATE`, `GDPC1` — macro context
- `USREC` — NBER recession indicator (for shading backtests)

### yfinance (free, ~30s/100 tickers)
- `^GSPC`, `SPY`, `VTI`, `VOO` — US equity
- `^VIX`, `^VVIX` — vol
- `TLT`, `IEF`, `BIL`, `SHV`, `BND`, `AGG` — bonds
- `GLDM`, `GLD`, `SLV` — metals (note GLD = collectibles tax)
- `VNQ`, `IYR` — REITs
- `DBC`, `PDBC`, `KMLM`, `DBMF` — commodities / managed futures
- `EFA`, `VEU`, `EEM`, `MCHI`, `ASHR`, `KWEB` — international / China exposure
- `MTUM`, `IWM`, `VIOV`, `VBR` — factor sleeves
- `ALLW`, `RPAR` — single-ticker risk-parity products
- `DX-Y.NYB`, `GC=F`, `HG=F` — DXY, gold, copper

### akshare (free, China-focused; `pip install akshare`)
- `ak.index_zh_a_hist(symbol="000300", period="daily", start_date="19900101", end_date="20251231")` — CSI 300
- `ak.index_zh_a_hist(symbol="000905")` — CSI 500; `"000852"` — CSI 1000
- `ak.stock_zh_a_hist(symbol="600519", period="daily", adjust="qfq")` — individual A-share (qfq = forward-adjusted)
- `ak.stock_zh_index_spot_sina()` — index snapshot (sh000001 上证, sz399001 深证)
- `ak.stock_zh_index_daily(symbol="sh000001")` — Shanghai Composite daily
- `ak.fund_etf_hist_em(symbol="510300")` — Huatai-PB CSI 300 ETF
- `ak.bond_china_yield(start_date=..., end_date=...)` — China gov bond yield curve
- `ak.macro_china_cpi`, `ak.macro_china_gdp_yearly` — CN macro
- `ak.fx_spot_quote()` — USD/CNY, etc.
- `ak.stock_yjbb_em(date="20240331")` — A-share quarterly earnings reports (PEAD raw material)
- `ak.stock_financial_em(symbol="600519")` — fundamentals for Magic Formula on A-shares
- Stamp duty: 0.05% sell-side as of August 2023 (cut from 0.10%); commission ~0.025% per broker.

### Tax framework — China A-share individuals
Per PwC Worldwide Tax Summaries 2025 (https://taxsummaries.pwc.com/peoples-republic-of-china/individual/other-tax-credits-and-incentives): **"Capital gains from transfer of shares traded on the Shanghai, Shenzhen, and Beijing Stock Exchanges are generally exempt from IIT."** Dividends: 20% headline but 50%/100% reduction by holding period (>1yr = full exemption). Restricted shares (限售股, pre-IPO) governed by Caishui [2009] No. 167 — taxed at 20%. **Implication for this report**: the "20% individual capital-gains tax" framing applies to dividends and unlisted/restricted shares; ordinary listed A-share trading gains are tax-free for individuals, which makes high-turnover quant strategies *more* tax-viable in China than in US taxable accounts.

### Alpha Vantage / Nasdaq Data Link
- Alpha Vantage `EARNINGS` endpoint (free, 5 req/min) for PEAD US implementation.
- Nasdaq Data Link (formerly Quandl) — Sharadar SF1 (paid, ~$50/mo) for clean US fundamentals.

---

## Caveats

- **In-sample vs OOS**: where original CAGRs were quoted in this report (Magic Formula 30.8% → 11.4%, GEM 17.43% → ~9% live, Dogs 18.4% → 7.7-8.7%, pre-FOMC 49bp → 9.2bp), the modern decay is documented and flagged. Treat the originator's number as an upper bound; the OOS number as the realistic prior.
- **Survivorship bias**: a fair share of "robust" originator claims used the surviving CRSP/Compustat universe; the truly investable spread is generally 30–50% smaller.
- **Tax asymmetry**: conclusions flip for a Chinese individual — strategies dismissed as "tax-killed" in US taxable accounts (Connors, J-T, PEAD, TOM) are viable in CN because A-share trading gains are exempt. Conversely, the GLD-heavy Permanent / Golden Butterfly carry a US 28% collectibles surprise.
- **2022 inflation shock**: invalidated "60/40 diversification" priors for many strategies in Family E. Per MSIM, 60/40 lost −17.5% in 2022, its worst year since 1937. The negative stock-bond correlation that drove the all-weather logic was a 2000–2021 regime, not a law.
- **VIX/F&G/Put-Call**: very few signal fires + post-hoc threshold selection → expect publication bias. Use as descriptive context, not as scaling decisions.
- **Pre-FOMC drift IS dead** (Kurov-Wolfe-Gilbert 2021, Finance Research Letters 40: post-2015 mean 0.092% vs pre-2015 0.445%). Do not trade it.
- **HY OAS series on FRED truncating to 3-year history in April 2026** — pull and store the full 1996+ history now. Same caveat may apply to other ICE-sourced FRED series.
- **Hurst-Ooi-Pedersen 2017 figures** (Sharpe 0.39→0.55, DD −62.3% → −50.2%) are gross of fee and gross of cost; net-of-cost performance for retail-implementable trend-following ETFs (DBMF, KMLM) will be lower.
- **Bridgewater All-Weather −3.93% 2008 figure** is widely cited but the original Bridgewater publication is not freely accessible; independent proxy data (PortfoliosLab) are consistent with a flat-to-small-negative 2008 result, so the directional claim stands even if the third decimal is unverifiable.
- **All backtests built from this report should**: (a) use total-return series (not price-only), (b) include realistic costs (0.05–0.10% one-way US; 0.05% stamp + 0.025% commission CN), (c) compute Sharpe against actual FRED `DGS3MO`, not a constant, and (d) report both gross and tax-adjusted results.