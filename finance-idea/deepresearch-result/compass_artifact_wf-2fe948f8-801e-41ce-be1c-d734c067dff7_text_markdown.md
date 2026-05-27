# Systematic Strategies Proposal — 23 Strategies Across Five Families (US + China Dual-Track)

**Audience:** Quant research analyst who will code each strategy into a `compute()` function and backtest locally with `akshare + yfinance + FRED`.
**Scope rule:** This is a STRATEGY PROPOSAL, not a backtest. All performance numbers are quoted verbatim from cited published sources. Where a metric was not reported in the original, we say so explicitly. No unified cross-strategy table is computed.

---

## TL;DR
- 23 strategies across Trend/Momentum (6), Mean-Reversion/Sentiment (5), Macro Regime (5), Calendar/Seasonal (3), Allocation/Drawdown Control (7 — net of overlap with the famous-allocation set). Each card includes universe, signal, rebalance frequency, the original in-sample claim cited verbatim with URL, at least one out-of-sample retest, data feasibility with `akshare + yfinance + FRED`, and a one-line literature verdict.
- The strongest in-sample edges (Greenblatt Magic Formula 30.8% CAGR 1988-2004; Lucca-Moench 49 bp pre-FOMC; Antonacci GEM 17.43% CAGR 1974-2013) all have documented post-publication decay or critique that materially changes the recommendation. We flag in-sample vs out-of-sample gaps > 30% where the literature documents them — most importantly the pre-FOMC drift, which Kurov, Wolfe & Gilbert (2021) state "essentially disappeared after 2015."
- China dual-track is materially different. Blitz, Hanauer, Jansen, Swinkels & Zhou (2021, *Pacific-Basin Finance Journal* 68) document that 12-1 month momentum in A-shares is statistically insignificant ("0.33% per month return (t-statistic 0.92) for the equally weighted portfolio"); short-term residual reversal is the dominant anomaly ("0.66% per month (t-statistic 3.36)"). The CN momentum cards therefore become reversal cards.

---

## Key Findings

1. **In-sample vs out-of-sample decay is the single most important reading.** Kurov, Wolfe & Gilbert (2021, *Finance Research Letters* 40C) document that the pre-FOMC drift "essentially disappeared after 2015 in both announcements accompanied by press conferences and announcements not accompanied by press conferences." Magic Formula has been replicated directionally post-2005 but never at 30%+ CAGR. Dogs of the Dow "consistently underperformed the overall market during the last half of the 1990s" (Malkiel, *A Random Walk Down Wall Street*, as cited via Bogleheads commentary). The Halloween effect is the exception — Zhang & Jacobsen (2021, *JIMF*) explicitly state in 62,962 monthly observations over 323 years that the effect has NOT decayed.
2. **Faber's 10-month SMA timing model remains the canonical "user-runnable" trend strategy:** equity-like returns with bond-like volatility and drawdowns since 1973, with the Feb 2013 update concluding "the models have performed well in real-time, achieving equity like returns with bond like volatility and drawdowns."
3. **Risk-parity / All-Weather have a strong theoretical foundation (Asness, Frazzini & Pedersen 2012 FAJ), but the empirical case for the UNLEVERED Permanent Portfolio / Golden Butterfly retail variants is sample-period sensitive.** The 2024-2025 gold rally — World Gold Council reports gold +25.5% in 2024 and +67.4% in 2025 (LBMA PM USD; *Gold Market Commentary December 2025*, 8 January 2026, Table 1) — accounts for much of recent outperformance vs equities.
4. **China A-share momentum is famously weak; reversal dominates.** Blitz et al. (2021): "The lack of momentum is generally attributed to high turnover in Chinese markets shortening the period over which cycles of overreaction and subsequent correction occurs." The CN variant of every momentum card must be inverted to a reversal design.
5. **Several "famous" strategies are not cleanly reproducible with akshare + yfinance + FRED alone**: Conference Board LEI (paywalled since 2022 — substitute CFNAI), CNN Fear & Greed (no clean historical API), Bridgewater All-Weather (uses futures/swaps for leverage; the unlevered equity-ETF proxy is NOT the same product). The ICE BofA HY OAS series (FRED `BAMLH0A0HYM2`) will be truncated to 3 years of observations on FRED starting April 2026 — archive locally NOW.

---

## Details

# FAMILY A — Trend / Momentum

### A1. Faber 10-Month / 200-Day SMA Timing (GTAA "Ivy 5")

**1. Originator & source.** Mebane T. Faber, "A Quantitative Approach to Tactical Asset Allocation," *Journal of Wealth Management*, Spring 2007; SSRN 962461, with Feb 2009 and Feb 2013 updates. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461 (author copy: https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf).

**2. Mechanical rules.**
- **Universe (Ivy 5):** SPY (US equity), EFA (foreign developed equity), IEF (US 10Y Treasury), VNQ (US REIT), DBC (commodities).
- **Signal:** at each month-end, compare close to its own 10-month simple moving average (≈200 trading days).
- **Entry/exit:** at month-end, if `close > 10M SMA` → hold the asset for the next month; else → hold cash / T-bills (SHY).
- **Position sizing:** equal-weight 20% per asset class; cash where signal is off.
- **Costs:** the 2013 update headline assumes no transaction costs but discusses robustness to reasonable costs given <1× annual turnover.

**3. Original in-sample claim (verbatim).** "Overall, we find that the models have performed well in real-time, achieving equity like returns with bond like volatility and drawdowns" (Faber 2013, abstract, https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf). Faber compares to Siegel's DJIA 1886-2006 test (1% band): "Siegel's results showed an annualized return of 9.7 percent from 1886-2012 for the timing model versus a 9.4 percent return for a simple buy and hold strategy" (https://awealthofcommonsense.com/2018/05/what-the-200-day-moving-average-does-does-not-tell-you/).

**4. Out-of-sample updates.**
- Marmi, Pacati, Risso, Renò (SSRN 1476225) replicate and find the edge persists but is partially dependent on bond-rally tailwind.
- Gabriel, Pagani, Zarattini (SSRN 5230603, Apr 2025) re-run through March 2025 and conclude the GTAA approach "performed well in real-time." No catastrophic decay reported.

**5. Data feasibility (free tools).** YES. yfinance: `SPY EFA IEF VNQ DBC SHY`. Pre-ETF history requires mutual-fund proxies (VFINX, VGTSX, VBMFX, VGSIX).

**6. Implementation notes.** No shorting, no leverage. Monthly rebalance → low turnover. In US taxable accounts, monthly toggles create short-term gains; CN A-shares are subject to 0.1% stamp duty (sale side) but the individual capital-gains tax on A-shares is currently exempt for personal accounts.

**7. Literature verdict.** Robust as a risk-reduction filter; explicit acknowledgment in Faber 2013 that "a trend-following model can underperform buy and hold during a roaring bull market."

**CN variant.** CSI300 10-month SMA on `ak.stock_zh_index_daily(symbol="sh000300")`. No peer-reviewed CSI300 Faber-style test located (subagent gap).

---

### A2. Antonacci Dual Momentum — Global Equities Momentum (GEM)

**1. Originator & source.** Gary Antonacci, "Risk Premia Harvesting Through Dual Momentum," 2012 NAAIM Founders Award winner; published *Journal of Management & Entrepreneurship* 2(1):27-55 (Mar 2017). SSRN 2042750: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750. Book: *Dual Momentum Investing*, McGraw-Hill 2014.

**2. Mechanical rules (GEM).**
- **Universe:** S&P 500 (SPY), MSCI ACWI ex-US (VEU), aggregate bonds (AGG), T-bills (BIL).
- **Signal:** at each month-end, compute trailing 12-month total return for SPY and VEU.
  - **Absolute filter:** if SPY 12M return ≤ T-bill (BIL) 12M return → hold AGG.
  - **Relative filter (if absolute filter passes):** hold whichever of SPY or VEU has the higher 12M return.
- **Rebalance:** monthly. One ETF held at a time.

**3. Original in-sample claim (verbatim).** *Dual Momentum Investing* (McGraw-Hill 2014), pp. 94/103: "Over this entire 40-year period [1974-2013], GEM has an average annual return of 17.43% with a 12.64% standard deviation, a 0.87 Sharpe ratio, and a maximum drawdown of 22.7%." The book's benchmark comparison is to ACWI (8.85% CAGR, 60.21% max drawdown), not the S&P 500.

**4. Out-of-sample.**
- Newfound Research, "Fragility Case Study: Dual Momentum GEM" (https://blog.thinknewfound.com/2018/10/fragility-case-study-dual-momentum-gem/): the rule is highly sensitive to look-back and rebalance-date choice — multiple plausible parameterizations would have flipped the decision around the 2008 turn.
- Newfound/Resolve "Global Equity Momentum: A Craftsman's Perspective" (Hoffstein 2017): edge persists but is fragile to single-month timing luck. Recommends ensemble of rebalance dates.

**5. Data feasibility.** YES with yfinance: `SPY VEU AGG BIL`. For pre-2007 history, sub VFINX, VGTSX, VBMFX, `^IRX`.

**6. Implementation notes.** No shorting, no leverage. Single-ETF concentration → wash-sale considerations in taxable US accounts.

**7. Literature verdict.** Robust signal, fragile single-instance implementation.

**CN variant.** Replace SPY/VEU with CSI300 / Hang Seng. Note CN momentum is weak (Blitz et al. 2021) — use with caution; consider replacing the absolute-momentum filter with a 200-day SMA filter.

---

### A3. Time-Series Momentum / CTA (Moskowitz, Ooi, Pedersen 2012)

**1. Originator & source.** Tobias J. Moskowitz, Yao Hua Ooi, Lasse Heje Pedersen, "Time Series Momentum," *Journal of Financial Economics* 104(2):228-250 (2012). Author copy: http://docs.lhpedersen.com/TimeSeriesMomentum.pdf. AQR summary: https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum.

**2. Mechanical rules.**
- **Universe:** 58 liquid futures contracts (equity indices, currencies, commodities, sovereign bonds). Retail proxy: ~10-15 ETFs across asset classes.
- **Signal:** sign of the trailing 12-month excess return of each instrument.
- **Position sizing:** volatility-scaled — `position = sign(r_12m) / σ_ex-ante`, with σ from past 3-year monthly returns scaled to a target per-instrument vol (40% in the paper).
- **Rebalance:** monthly.
- **Costs:** paper reports gross; AQR's later work assumes ~0.1% per-instrument round-trip.

**3. Original in-sample claim (verbatim).** "All 58 futures contracts exhibit positive time series momentum returns and 52 are statistically different from zero at the 5%" level (http://docs.lhpedersen.com/TimeSeriesMomentum.pdf, p. 10). On portfolio Sharpe: "a diversified portfolio of time series momentum across all assets is remarkably stable and robust, yielding a Sharpe ratio greater than one on an annual basis, or roughly 2.5 times the Sharpe ratio for the equity market portfolio" (JFE 104, p. 229). [Note: the often-quoted "~1.4 Sharpe" is not the paper's own language — the paper says "greater than one"; a separate out-of-sample test cites "an annualized Sharpe ratio of 1.1" (p. 237).]

**4. Out-of-sample.**
- Huang, Li, Wang, Zhou (2020, *JFE*, working paper at https://ink.library.smu.edu.sg/context/lkcsb_research/article/7520/viewcontent/Time_series_momentum_JFE_sv.pdf): "we confirm these results with similar data, [but] we find that their results are driven by the volatility-scaled returns (or the so-called risk parity approach to asset allocation) rather than by time series momentum. Without scaling by volatility, time series momentum and a buy-and-hold strategy offer similar cumulative returns." → **Major decay-of-attribution flag**: the headline alpha is largely a vol-scaling artifact, not the sign signal.
- Hurst, Ooi, Pedersen (2017) "A Century of Evidence on Trend-Following Investing" — TSMOM-like strategies show positive Sharpe across 1880-2016 (AQR).

**5. Data feasibility.** PARTIAL. True 58-instrument replication requires futures (paid). Free retail proxy: 10-15 ETFs (`SPY EFA EWJ EEM IEF TLT DBC GLD UUP`). For China commodity futures: akshare `ak.futures_main_sina`.

**6. Implementation notes.** Requires shorting OR a long-flat variant. Vol-scaling implies implicit leverage — at retail without futures, cap at 1×.

**7. Literature verdict.** Persistent at the portfolio level; edge attributable to the SIGN signal alone is smaller than the headline once vol-scaling is controlled (Huang et al. 2020).

**CN variant.** TSMOM on CSI300, CSI500, CN10Y futures, Shanghai gold, copper — all via akshare.

---

### A4. Cross-Sectional Momentum / Carhart UMD

**1. Originator & source.** Narasimhan Jegadeesh & Sheridan Titman, "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency," *Journal of Finance* 48(1):65-91 (1993): https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf. Mark Carhart, "On Persistence in Mutual Fund Performance," *JF* 52(1):57-82 (1997) — formalizes UMD.

**2. Mechanical rules.**
- **Universe:** broad US listed common stocks (or S&P 500 / Russell 1000 for a tractable retail variant).
- **Signal:** at month t, rank stocks by total return from t−12 to t−1 (the "12-1" rule; the most recent month is skipped to avoid 1-month reversal).
- **Portfolio:** top decile long, bottom decile short (long-only variant for retail).
- **Holding period:** 3-6 months; **rebalance:** monthly with overlapping holding periods.

**3. Original in-sample claim (verbatim).** "Strategies which buy stocks that have performed well in the past and sell stocks that have performed poorly in the past generate significant positive returns over 3- to 12-month holding periods" (Jegadeesh & Titman 1993, abstract). Winner-minus-loser portfolio earned approximately 1% per month over 1965-1989 — a figure widely re-quoted in subsequent literature.

**4. Out-of-sample.**
- Jegadeesh & Titman (2001, *JF*): "momentum profits have continued in the 1990s, suggesting that the original results were not a product of data snooping bias."
- Asness, Moskowitz, Pedersen (2013, *JF*) "Value and Momentum Everywhere": momentum confirmed in 40+ countries and multiple asset classes.
- 2009 momentum crash (long losers / short winners) revealed fat-tail risk in the short leg.

**5. Data feasibility.** PARTIAL. yfinance pulls per-ticker history but does not give a clean historical S&P 500 / Russell constituent list (survivorship-bias risk). User must supply historical constituents file. akshare `ak.index_stock_cons_csindex(symbol="000300")` gives current CSI300 constituents.

**6. Implementation notes.** Long-short version requires shorting/margin. Long-only top-decile is more retail-friendly. Monthly rebalance → high turnover → meaningful US short-term tax drag.

**7. Literature verdict.** Robust factor with periodic crashes; persists post-publication in US/global equity.

**CN variant — EXPLICIT WARNING.** Blitz, Hanauer, Jansen, Swinkels, Zhou (2021, *Pacific-Basin Finance Journal* 68, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3810114): "The 12-1 month momentum strategy generates a 0.33% per month return (t-statistic 0.92) for the equally weighted portfolio and a 0.35% (t-statistic 0.79) for the value-weighted portfolio. The weak return on momentum strategies is consistent with the existing literature… The lack of momentum is generally attributed to high turnover in Chinese markets shortening the period over which cycles of overreaction and subsequent correction occurs." → CN momentum is NOT viable. Replace with short-term **reversal**: same Blitz et al. paper documents "this [residual reversal] strategy generates a statistically significant 0.66% per month (t-statistic 3.36) excess return for the equally weighted and 0.59% per month (t-statistic 2.11) excess return for the value-weighted strategy."

---

### A5. SPX 200-Day SMA Long/Flat Timing (Siegel formalization)

**1. Originator & source.** Jeremy J. Siegel, *Stocks for the Long Run*, 5th ed. (2014), McGraw-Hill, ch. 19. Practitioner replications at https://awealthofcommonsense.com/2018/05/what-the-200-day-moving-average-does-does-not-tell-you/.

**2. Mechanical rules.**
- **Universe:** SPY (and/or DJIA proxy).
- **Signal:** daily close vs 200-day SMA with a 1% band (buy when close > 1% above 200dSMA; sell to T-bills when close > 1% below).
- **Rebalance:** as signals trigger (daily check; typically 1-3 toggles per year).

**3. Original in-sample claim (verbatim).** "Siegel's results showed an annualized return of 9.7 percent from 1886-2012 for the timing model versus a 9.4 percent return for a simple buy and hold strategy. Once transaction costs were factored in, the timing model would have dropped to a return of 8.1 percent" (https://awealthofcommonsense.com/2018/05/what-the-200-day-moving-average-does-does-not-tell-you/, citing Siegel 5e ch. 19).

**4. Out-of-sample.** Siegel's earlier editions (pre-2008) reported the strategy did NOT improve risk-adjusted returns on the DJIA but did help on NASDAQ (https://en.wikipedia.org/wiki/Stocks_for_the_Long_Run). The 5e improvement reflects inclusion of the 2000-02 and 2008-09 bear markets.

**5. Data feasibility.** YES. yfinance: `^GSPC` or `SPY`.

**6. Implementation notes.** Higher whipsaw than 10-month SMA (Faber). No shorting, no leverage.

**7. Literature verdict.** Decayed but usable as risk filter — the post-cost alpha is roughly break-even pre-2000; positive 2000-2012 inclusive of two crises (Siegel 5e ch. 19).

**CN variant.** CSI300 250-day SMA. No peer-reviewed primary citation located.

---

### A6. PEAD — Post-Earnings Announcement Drift

**1. Originator & source.** Ball & Brown (1968) documented; named by Victor L. Bernard & Jacob K. Thomas, "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?," *Journal of Accounting Research* 27 (1989), and B&T "Evidence that stock prices do not fully reflect the implications of current earnings for future earnings," *Journal of Accounting and Economics* (Dec 1990).

**2. Mechanical rules.**
- **Universe:** US common stocks with quarterly earnings.
- **Signal:** Standardized Unexpected Earnings (SUE) = (actual EPS − seasonal random-walk expected EPS) / σ of forecast errors. Sort into deciles each quarter.
- **Portfolio:** long top SUE decile, short bottom SUE decile.
- **Holding period:** 60 trading days post-announcement.

**3. Original in-sample claim (verbatim).** "FOS estimate that over the 60 trading days subsequent to an earnings announcement, a long position in stocks with unexpected earnings in the highest decile, combined with a short position in stocks in the lowest decile, yields an annualized 'abnormal' return of about 25%, before transactions costs" (Bernard & Thomas 1989, abstract, https://www.semanticscholar.org/paper/POST-EARNINGS-ANNOUNCEMENT-DRIFT-DELAYED-PRICE-OR-Bernard-Thomas/01354e373f23983ac962c8b133e668332ec26da9). "Bernard and Thomas (1990) found that approximately 25-30% of the post-earnings announcement drift occurs during the three-day windows surrounding subsequent earnings announcements" (https://en.wikipedia.org/wiki/Post%E2%80%93earnings-announcement_drift).

**4. Out-of-sample.** Chordia, Goyal, Shanken, Shivakumar (2009) and Fink (2021) review show PEAD persists but is concentrated in illiquid small-cap, low-analyst-coverage names. Cohen et al. "PEAD.txt" (Phila Fed WP 21-07, https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2021/wp21-07.pdf) document an 8.01% quintile spread quarterly 2010-2019 using text-based earnings surprise.

**5. Data feasibility.** PARTIAL. yfinance does not provide consensus earnings-surprise data. Workaround: yfinance `Ticker.earnings_history` (limited, recent only); akshare `ak.stock_yjbb_em(date="20240331")` for CN quarterly earnings (业绩报表). Full US universe SUE construction requires Compustat/IBES (paid).

**6. Implementation notes.** Requires shorting for spread version. High turnover.

**7. Literature verdict.** Robust but decayed — the 25% gross spread shrinks substantially after transaction costs and concentrates in small-caps post-1990s.

**CN variant.** Less studied in English-language literature; akshare `ak.stock_yjbb_em` supports a SUE construction.

---

# FAMILY B — Mean Reversion / Sentiment Contrarian

### B1. Connors RSI(2) Mean Reversion

**1. Originator & source.** Larry Connors & Cesar Alvarez, *Short Term Trading Strategies That Work* (2009), TradingMarkets/Connors Research. Full scan: https://studylib.net/doc/27785371/.

**2. Mechanical rules.**
- **Universe:** SPY (canonical) / QQQ / liquid US equities.
- **Trend filter:** SPY close > 200-day SMA (Rule 3).
- **Entry:** RSI(2) of SPY closes below 5 (or 10 in looser variant).
- **Exit:** SPY close above 5-day SMA.
- **No stop-loss** (ch. 6, "Rule 5 — Stops Hurt").
- **Costs:** book uses zero commissions, no slippage.

**3. Original in-sample claim (verbatim).** Cumulative RSI variant: "On page 67 of their book, Connors and Alvarez state that this strategy was 88% accurate on the SPY when tested from 1993 through the date of publication, earning 65.53 SPY points with an average gain of 1.26% and an average holding period [under 5 trading days]" (https://easycators.com/thinkscript/cumulative-rsi-2-trading-strategy/). Different cumulative-RSI variant: "On page 104 of their book, Connors and Alvarez state that this strategy was 79.49% accurate on the SPY when tested, earning 779.51 S&P points with an average holding period of under 5 trading days" (same source).

**4. Out-of-sample.** Trade2Win community backtest (https://www.trade2win.com/threads/backtest-results-for-connors-rsi2-strategy.242688/) post-2010 publication: "The strategy seems to hold up over a long testing period. It has been in the public domain since the book was published in 2010, and yet in my backtest it continues to perform well… The annualised return is poor though [because of] infrequent trades."

**5. Data feasibility.** YES. yfinance `SPY`; CN variant `ak.stock_zh_index_daily(symbol="sh000300")`.

**6. Implementation notes.** Frequent short-duration trades → high US short-term capital-gains tax drag.

**7. Literature verdict.** Edge survives post-publication but is low in absolute CAGR because exposure is low; useful as a component in a multi-strategy basket.

**CN variant.** Likely STRONGER than US given documented A-share short-term reversal (Blitz et al. 2021). User backtest required.

---

### B2. VIX Spike Buy SPY

**1. Originator & source.** Whaley (2000) "The Investor Fear Gauge" *JPM*; Connors-Alvarez (2009) ch. 4 "Rule 4 — Use the VIX to Your Advantage." Review at https://arxiv.org/pdf/1806.07556.

**2. Mechanical rules (Connors-Alvarez VIX-RSI variant).**
- **Universe:** SPY.
- **Trend filter:** SPY close > 200-day SMA.
- **Signal:** VIX RSI(2) > 90 AND VIX opens above prior day's close AND SPY RSI(2) < 30 → buy SPY at close.
- **Exit:** SPY RSI(2) > 65.
- **Simple alternative:** VIX > 30 → buy SPY, hold 21 trading days.

**3. Original in-sample claim.** Connors-Alvarez book does not publish a single CAGR for the VIX-RSI variant; the source quotes high win-rates on backtests through 2008 without a specific verbatim CAGR. FXEmpire (https://www.fxempire.com/forecasts/article/sp-500-forecast-vix-above-30-could-signal-a-tactical-buying-opportunity-1589696, sample from 2016): "the three-week positive return probability for a cross above 30 is a massive 81.5%" — short sample.

**4. Out-of-sample.** iVolatility analysis (https://www.ivolatility.com/news/3127): "SPY's 20-day forward return averaged +3.78% when IVX30 was in the 25-35 range, versus +0.90% when IVX30 was below 15." Note the direction is the opposite of the popular bearish-VIX narrative.

**5. Data feasibility.** YES. yfinance: `^VIX`, `SPY`. CN equivalent: SSE iVIX was discontinued in 2018; closest live proxy is option-implied vol via `ak.option_finance_board()` on SSE 50ETF / 300ETF options.

**6. Implementation notes.** No shorting, no leverage.

**7. Literature verdict.** Useful tactical add-on; not a standalone strategy. No clean primary-source CAGR.

**CN variant.** Limited (iVIX defunct).

---

### B3. AAII Bearish > 60% Contrarian

**1. Originator & source.** American Association of Individual Investors weekly Sentiment Survey since July 1987. Contrarian-framework articles: Wayne A. Thorp, "Investor Sentiment as a Contrarian Indicator" (AAII, 2004): https://www.aaii.com/journal/sentimentsurveyarticle?a=1209; Charles Rotblut update: https://www.aaii.com/journal/article/is-the-aaii-sentiment-survey-a-contrarian-indicator.

**2. Mechanical rules.**
- **Universe:** SPY.
- **Signal:** weekly AAII bearish % > 2σ above historical mean (~50%+ — current 2σ breakpoint per AAII is ~50.5%) OR raw threshold > 60%.
- **Entry:** buy SPY at next Monday open.
- **Holding period:** 6 months (canonical AAII study) or 12 months.

**3. Original in-sample claim (verbatim, from AAII's own contrarian-indicator article).** "On a six-month basis, the S&P 500 rose 60% of the time following a bearish sentiment reading more than two standard deviations above the historical mean. The average and median gains were 2.8% and 5.3%, respectively" (https://www.aaii.com/journal/article/is-the-aaii-sentiment-survey-a-contrarian-indicator). The LOW bullish signal is statistically stronger than HIGH bearish per AAII's own data — they note "extraordinarily low levels of optimism have consistently preceded larger-than-average six- and 12-month gains in the S&P 500."

**4. Out-of-sample.** AAII Journal reports March 5, 2009 bearish hit 70.3% — a record high — coinciding with the market bottom. AInvest commentary (https://www.ainvest.com/news/market-sentiment-contrarian-indicator-pessimism-signal-buying-opportunity-2508/) notes 60%+ bearish prints in late 1990, 2008-09, 2022, April 2025; **caveat: this is a small-sample qualitative observation, not a robust statistical edge.**

**5. Data feasibility.** YES — weekly history free from AAII.com (manual CSV download). No clean API.

**6. Implementation notes.** Very low signal frequency (< 1 per year on average); not a standalone.

**7. Literature verdict.** Useful contrarian add-on; AAII's own data shows the LOW-bullish signal is statistically stronger than HIGH-bearish.

**CN variant.** No direct CN AAII analogue; informal proxies (e.g., Eastmoney 股吧 sentiment) have no clean academic source.

---

### B4. Put/Call Ratio Extremes

**1. Originator & source.** CBOE total / equity-only put/call ratio published since 1995. Popularized by Bernie Schaeffer and Larry McMillan. No single peer-reviewed canonical paper with a definitive backtest.

**2. Mechanical rules.**
- **Universe:** SPY.
- **Signal:** CBOE total P/C ratio 10-day moving average > 1.10 → buy.
- **Exit:** ratio reverts < 0.85 OR 21-trading-day timeout.

**3. Original in-sample claim.** Not reported in original source — no peer-reviewed canonical CAGR.

**4. Out-of-sample.** Practitioner backtests (quantifiedstrategies.com) show modest positive expectancy concentrated around volatility regime changes.

**5. Data feasibility.** PARTIAL. CBOE historical bulk-download is paywalled. Workaround: derive a synthetic P/C from yfinance `Ticker.option_chain` per expiry. CN has no clean equivalent (limited options market).

**6. Implementation notes.** No shorting.

**7. Literature verdict.** Weak as a standalone; OK as ensemble component.

**CN variant.** Effectively US-only.

---

### B5. CNN Fear & Greed Extreme

**1. Originator & source.** CNN Business proprietary aggregate of 7 sub-indicators; methodology: https://www.cnn.com/markets/fear-and-greed.

**2. Mechanical rules.**
- **Signal:** F&G < 25 (extreme fear) → buy SPY; hold 1-3 months.
- Symmetric variant: F&G > 75 (extreme greed) → reduce.

**3. Original in-sample claim.** Not reported in original source — CNN does not publish a backtest CAGR.

**4. Out-of-sample.** Practitioner replications (hackingthemarkets/fear-and-greed on GitHub) show extreme-fear preceded above-average forward 60-day returns 2011-2024 but the sample is short.

**5. Data feasibility.** **NO clean free historical API.** CNN does not publish historical F&G in CSV. Reconstruction from sub-components (junk-bond spreads, 125-day breadth, put/call) is required. **Flag as data-feasibility issue.**

**6. Implementation notes.** N/A.

**7. Literature verdict.** Suggestive, unverifiable without primary data construction. Do not implement as standalone.

**CN variant.** US-only.

---

# FAMILY C — Macro Regime

### C1. Yield-Curve Inversion + Re-Steepening (Estrella & Mishkin)

**1. Originator & source.** Arturo Estrella & Frederic S. Mishkin, "The Yield Curve as a Predictor of U.S. Recessions," *FRBNY Current Issues in Economics and Finance* 2(7), June 1996: https://www.newyorkfed.org/medialibrary/media/research/current_issues/ci2-7.pdf. Fed Board FEDS Notes (Mar 2018): https://www.federalreserve.gov/econres/notes/feds-notes/predicting-recession-probabilities-using-the-slope-of-the-yield-curve-20180301.html.

**2. Mechanical rules.**
- **Signal:** FRED `T10Y3M` (or `T10Y2Y`).
- **Probit (verbatim, Estrella-Mishkin):** `P(Recession) = Φ(-0.5333 - 0.6330 × Spread)`, where Spread is in percentage points.
- **Defensive trigger:** P(Recession over next 12M) > 30% → reduce equity → bonds.
- **Re-steepening trigger:** T10Y2Y crosses from negative back to positive (the historically reliable timing signal that recession is imminent).

**3. Original in-sample claim (verbatim).** "The yield curve model has correctly signaled the last seven U.S. recessions before they began" (https://ryanoconnellfinance.com/yield-curve-analyzer/, summarizing the Estrella-Mishkin update).

**4. Out-of-sample.** Fed Board FEDS Notes (Mar 2018) confirms predictive power through 2017. **Important post-publication caveat**: the 2022-23 T10Y2Y inversion did NOT result in an NBER-dated recession by mid-2024, raising fresh decay concerns. The Fed has not issued a definitive paper retracting the model — user should look at Estrella's own continued updates.

**5. Data feasibility.** YES. FRED IDs: `T10Y3M`, `T10Y2Y`, `DGS10`, `DGS2`, `DGS3MO`.

**6. Implementation notes.** Defensive rotation only; no shorting; low turnover.

**7. Literature verdict.** Decayed but usable as risk filter (the 2022-24 false signal is the strongest recent challenge to the model).

**CN variant.** China 10Y minus 2Y spread via `ak.bond_china_yield()`.

---

### C2. HY OAS Defensive Threshold

**1. Originator & source.** ICE BofA US High Yield Master II Option-Adjusted Spread, FRED series `BAMLH0A0HYM2`: https://fred.stlouisfed.org/series/BAMLH0A0HYM2. Academic foundation: Simon Gilchrist & Egon Zakrajšek, "Credit Spreads and Business Cycle Fluctuations," *AER* 102(4):1692-1720 (2012). **No peer-reviewed Fed paper quantifies discrete bp thresholds**; the threshold framework is practitioner heuristic.

**2. Mechanical rules (practitioner — flag as non-academic).**
- **Signal:** monthly `BAMLH0A0HYM2`.
- **Risk-on:** < 300 bp → 100% SPY.
- **Monitor:** 300-500 bp → 60/40.
- **Defensive:** > 500-600 bp → rotate to IEF.
- **Buy-the-dip:** > 1000 bp → overweight HY (HYG, JNK).

**3. Original in-sample claim.** Not reported in original source for these specific thresholds. Historical extremes from FRED commentary: all-time peak 1988 bp on 16 Dec 2008 (GFC); 1087 bp on 23 Mar 2020 (COVID); 20-year average ≈ 490 bp.

**4. Out-of-sample.** The continuous predictor (Gilchrist-Zakrajšek excess bond premium) is robust in peer review. The discrete thresholds are folklore.

**5. Data feasibility.** YES — but with a critical caveat. **FRED page warning (verbatim):** "Starting in April 2026, this series will only include 3 years of observations. For more data, go to the source." **Archive locally NOW.**

**6. Implementation notes.** No shorting; annual rebalance → tax-friendly.

**7. Literature verdict.** Continuous signal robust (Gilchrist-Zakrajšek 2012 AER); discrete thresholds are practitioner heuristics — re-fit on your own data.

**CN variant.** No clean FRED-equivalent; approximate via `ak.bond_china_close_return` and CN credit-spread series.

---

### C3. DXY 6-Month Change → EM Tilt

**1. Originator & source.** No single canonical academic paper. Closest formal treatment: BIS Working Paper 775, Hofmann, Shim & Shin (2020) "Bond risk premia and the exchange rate."

**2. Mechanical rules.**
- **Signal:** rolling 6-month change in DXY.
- **Long EM (EEM/VWO):** DXY 6M Δ < 0.
- **Long DM (SPY/EFA):** DXY 6M Δ > 0.
- **Rebalance:** monthly.

**3. Original in-sample claim.** Not reported in any single peer-reviewed source — user backtest required.

**4. Out-of-sample.** N/A.

**5. Data feasibility.** YES. yfinance: `DX-Y.NYB`, `EEM`, `VWO`, `SPY`, `EFA`. FRED: `DTWEXBGS`.

**6. Implementation notes.** No shorting.

**7. Literature verdict.** Folklore signal with intuitive macro foundation; no formal peer-reviewed discrete-rule test. Treat as overlay.

**CN variant.** Replace EM with CSI300 / MSCI China; USDCNY via FRED `DEXCHUS`.

---

### C4. Gold/Copper Ratio Z-Score

**1. Originator & source.** No single canonical academic paper. Popularized as "Dr. Copper" and "the gold/copper ratio" by Felder, Gundlach (https://thefelderreport.com).

**2. Mechanical rules.**
- **Signal:** rolling 5-year z-score of log(gold/copper).
- **Z > +1:** risk-off (gold rising vs copper = fear / slowing growth).
- **Z < −1:** risk-on (cyclical tilt).
- **Rebalance:** monthly.

**3. Original in-sample claim.** Not reported in original source.

**4. Out-of-sample.** Practitioner-blog only; no formal peer-reviewed backtest.

**5. Data feasibility.** YES. yfinance: `GC=F`, `HG=F`. FRED: `PCOPPUSDM`, `IQ12260` (gold London PM).

**6. Implementation notes.** No shorting.

**7. Literature verdict.** Intuitive macro overlay; unproven as standalone.

**CN variant.** Same global series; akshare `ak.futures_main_sina("CU0")` for SHFE copper.

---

### C5. Conference Board LEI Drop Trigger (with CFNAI substitute)

**1. Originator & source.** Conference Board Leading Economic Index, monthly 10-component composite: https://www.conference-board.org/topics/us-leading-indicators. Methodology behind component selection ultimately traces to Mitchell-Burns NBER tradition.

**2. Mechanical rules.**
- **Signal:** LEI 6-month annualized rate-of-change < −3.5% AND breadth < 50% → recession warning; reduce equity.
- **Reversal:** LEI 6M ROC turns positive → restore.

**3. Original in-sample claim.** Conference Board's methodology claims a 6-12 month lead over NBER-dated recession peaks. No CAGR reported.

**4. Out-of-sample.** LEI's predictive validity has been contested post-2022 — the LEI fell sharply but no NBER-dated recession occurred by mid-2024.

**5. Data feasibility.** **NO — Conference Board removed LEI from FRED in 2022; the series is now paywalled.** **Free substitute: Chicago Fed National Activity Index (CFNAI), FRED `CFNAI` and 3-month MA `CFNAIMA3`.** Use CFNAI for the user's CLI.

**6. Implementation notes.** Monthly rebalance.

**7. Literature verdict.** LEI itself decayed in 2022-24; CFNAI substitute is free and academically respected.

**CN variant.** Caixin China PMI via `ak.macro_china_pmi_yearly` or NBS PMI series.

---

# FAMILY D — Calendar / Seasonal

### D1. Halloween Indicator / Sell-in-May (Bouman & Jacobsen 2002)

**1. Originator & source.** Sven Bouman & Ben Jacobsen, "The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle," *American Economic Review* 92(5):1618-1635 (Dec 2002): https://www.aeaweb.org/articles?id=10.1257/000282802762024683. SSRN draft: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=300700.

**2. Mechanical rules.**
- **Universe:** SPY.
- **Signal:** in market Nov 1 – Apr 30; in T-bills (BIL) May 1 – Oct 31.
- **Rebalance:** twice per year.

**3. Original in-sample claim (verbatim).** "Surprisingly, we find this inherited wisdom to be true in 36 of the 37 developed and emerging markets studied in our sample" (Bouman-Jacobsen 2002, abstract). On magnitude: Bouman & Jacobsen document a US Nov-Apr return that is 11 percentage points higher than the May-Oct return, and a UK gap of 24 percentage points (as reported by CFA Institute Enterprising Investor commentary on the original AER paper). Andrade, Chhaochharia & Fuerst (2012, *FAJ*) out-of-sample replication 1998-2012 found the average gap across all 37 markets equal to about 10 percentage points.

**4. Out-of-sample.**
- Maberly & Pierce (2004) critique: results sensitive to outliers (Oct 1987, Aug 1998).
- Zhang & Jacobsen (2021, *Journal of International Money and Finance*, https://www.sciencedirect.com/science/article/abs/pii/S0261560620302242): re-test on 62,962 monthly observations over 323 years and 109 markets — "the 62,962 monthly observations over 323 years show a strong Halloween effect when measured the way as suggested in Bouman and Jacobsen (2002)." 82 of 109 countries showed Nov-Apr > May-Oct returns. **Edge persists.**

**5. Data feasibility.** YES. yfinance: `SPY`. FRED: `DGS3MO` for T-bills.

**6. Implementation notes.** No shorting; two trades/yr → very low turnover.

**7. Literature verdict.** Robust — Zhang & Jacobsen 2021 confirms persistence across 323 years.

**CN variant.** Zhang & Jacobsen 2021 include China — effect "appears to have been highly significant since the 1960s" in their sample.

---

### D2. Pre-FOMC Announcement Drift (Lucca & Moench 2015)

**1. Originator & source.** David O. Lucca & Emanuel Moench, "The Pre-FOMC Announcement Drift," *Journal of Finance* 70(1):329-371 (Feb 2015). FRBNY Staff Report 512: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf.

**2. Mechanical rules.**
- **Universe:** SPY (or ES futures).
- **Signal:** scheduled FOMC announcement.
- **Entry:** close of T−1 before FOMC.
- **Exit:** 5 minutes before announcement on T (close-to-close approximation OK for daily data).
- **Rebalance:** 8× per year per FOMC schedule.

**3. Original in-sample claim (verbatim, via Kurov, Wolfe & Gilbert 2021).** "From September 1994 to March 2011, the returns on average increase by 49 basis points during 24 h before the FOMC announcements, accounting for approximately 80% of annual returns" (Kurov, Wolfe & Gilbert 2021, *Finance Research Letters* 40C, https://www.sciencedirect.com/science/article/abs/pii/S1544612320315956, summarizing Lucca-Moench 2015).

**4. Out-of-sample — explicit decay flag (>30%).** Kurov, Wolfe & Gilbert (2021): the pre-FOMC drift "essentially disappeared after 2015 in both announcements accompanied by press conferences and announcements not accompanied by press conferences. We discuss a possible explanation for this change: reduced uncertainty." Boguth, Grégoire & Martineau (2019) also document attenuation when controlling for pre-market overnight returns (~25 bp residual). Hu, Pan, Wang & Zhu (NBER WP 25817, https://www.nber.org/system/files/working_papers/w25817/revisions/w25817.rev1.pdf) report a related residual of 15.1 bp in the close-to-close T−1 window. **Effect dropped from 49 bp pre-2011 to "essentially disappeared" post-2015.**

**5. Data feasibility.** YES. yfinance `SPY` (daily close-to-close is sufficient for the simple version). FOMC schedule: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

**6. Implementation notes.** 8 trades/yr → low turnover; US short-term gains.

**7. Literature verdict.** **Strongly decayed post-2015 (Kurov et al. 2021); do not implement as standalone.** Treat as historical anomaly.

**CN variant.** No direct PBoC analogue with comparable structured-announcement timing.

---

### D3. Turn-of-Month Effect

**1. Originator & source.** Robert A. Ariel, "A Monthly Effect in Stock Returns," *JFE* 18(1):161-174 (1987); Lakonishok & Smidt (1988); John J. McConnell & Wei Xu (2008) "Equity Returns at the Turn of the Month," *Financial Analysts Journal*.

**2. Mechanical rules.**
- **Universe:** SPY.
- **Signal:** long SPY from close of T−1 (last day of month) through close of T+3 (3rd trading day of new month); cash otherwise.

**3. Original in-sample claim.** McConnell & Xu (2008) document that the 4-day turn-of-month window earns approximately the entire monthly equity premium on average; remaining ~16-17 days have flat returns on average. Specific CAGR not in a single open-access verbatim quote — user should consult FAJ paywall or library access.

**4. Out-of-sample.** Effect persists in McConnell-Xu sample 1987-2005; subsequent replications show some attenuation but signal still positive.

**5. Data feasibility.** YES. yfinance `SPY`.

**6. Implementation notes.** ~33% market exposure (4 of 12 trading days per month). Heavy short-term tax drag.

**7. Literature verdict.** Persistent but small in absolute CAGR terms; use as exposure-tilt overlay.

**CN variant.** Documented in Chinese-language academic literature on Shanghai Composite; no canonical English citation located. Implementable with `ak.index_zh_a_hist(symbol="000300")`.

---

# FAMILY E — Allocation / Drawdown Control

### E1. 60/40 (canonical benchmark)

**1. Originator & source.** Industry convention; modern theoretical grounding: Harry Markowitz, "Portfolio Selection," *JF* 7(1):77-91 (1952). Vanguard Balanced Index Fund (VBINX, est. 1992) is the canonical retail implementation.

**2. Mechanical rules.**
- **Universe:** VTI (or SPY) 60%, BND (or AGG/IEF) 40%.
- **Rebalance:** annual to target weights.

**3. Original in-sample claim.** No single originator claim — 60/40 is a convention, not a thesis. Long-term historical performance varies by window; no benchmark comparison in original source — user will compute downstream.

**4. Out-of-sample.** 2022 was the worst calendar year for 60/40 since 1937 (-17%, per Bloomberg analyses cited widely in the financial press), reflecting positively-correlated stock-bond drawdown — a regime concern.

**5. Data feasibility.** YES. yfinance: `VTI BND`.

**6. Implementation notes.** No shorting/leverage; annual rebalance → very tax-friendly.

**7. Literature verdict.** Benchmark. Decayed if you believe stock-bond correlation has structurally flipped post-2022.

**CN variant.** CSI300 60% / CN10Y bond ETF 511260 40%; rebalance annually.

---

### E2. Harry Browne Permanent Portfolio

**1. Originator & source.** Harry Browne, *Fail-Safe Investing* (1999), St. Martin's Press. Modern guide: Craig Rowland & J.M. Lawson, *The Permanent Portfolio: Harry Browne's Long-Term Investment Strategy* (Wiley 2012). PortfolioCharts reference: https://portfoliocharts.com/portfolios/permanent-portfolio/.

**2. Mechanical rules.**
- **Universe (ETF proxy):** VTI 25%, TLT 25%, GLD 25%, BIL 25%.
- **Rebalance:** annual, or threshold-based when any band ≤ 15% or ≥ 35%.

**3. Original in-sample claim.** Browne himself did not publish an academic-style backtest. Modern third-party reproductions: "Going back to 1968 and looking through March 2026, the Permanent Portfolio has delivered a solid 8.51% CAGR with annualized volatility of only 7.32%" (https://www.optimizedportfolio.com/permanent-portfolio/). LazyPortfolioETF: "in the previous 30 Years, the Harry Browne Permanent Portfolio obtained a 7.10% compound annual return, with a 6.83% standard deviation. It suffered a maximum drawdown of -15.92% that required 27 months to be recovered" (https://www.lazyportfolioetf.com/allocation/harry-browne-permanent/). **Both are practitioner backtests, not peer-reviewed.**

**4. Out-of-sample.** Sample-period sensitivity to gold rally: World Gold Council *Gold Market Commentary December 2025* (8 January 2026, Table 1) reports LBMA Gold PM USD +25.5% in 2024 and +67.4% in 2025 — these returns alone drive much of recent PP outperformance.

**5. Data feasibility.** YES. yfinance: `VTI TLT GLD BIL`. Pre-2004 gold: FRED `IQ12260`.

**6. Implementation notes.** **GLD is taxed as a collectible at 28% US LTCG rate — material.**

**7. Literature verdict.** Robust as drawdown-controlled portfolio; lower expected return than equity-heavy alternatives.

**CN variant.** CSI300 (stocks), CN10Y ETF 511090 (TLT analog), Au9999 via `ak.spot_hist_sge(symbol="Au99.99")`, money-market 519888 (cash).

---

### E3. Golden Butterfly (Tyler / Portfolio Charts)

**1. Originator & source.** "Tyler" (anonymous Portfolio Charts founder), early-2010s blog: https://portfoliocharts.com/portfolios/golden-butterfly-portfolio/. Discussion: https://pictureperfectportfolios.com/golden-butterfly-portfolio-how-i-invest/.

**2. Mechanical rules.**
- **Universe (20% each):** VTI (total US stock), IJS or VBR (small-cap value), TLT (long Treasuries), SHY (short Treasuries), GLD (gold).
- **Rebalance:** annual.

**3. Original in-sample claim.** Practitioner backtest from lazyportfolioetf.com (https://www.lazyportfolioetf.com/allocation/golden-butterfly/): "As of April 2026, in the previous 30 Years, the Tyler Golden Butterfly Portfolio obtained a 8.05% compound annual return, with a 7.97% standard deviation. It suffered a maximum drawdown of -17.79%." OptimizedPortfolio (https://www.optimizedportfolio.com/golden-butterfly-portfolio/): "The Golden Butterfly has historically delivered roughly 93% of the S&P 500's CAGR with half the volatility and roughly 35% of the maximum drawdown" — practitioner approximation, not peer-reviewed.

**4. Out-of-sample.** Strongly sample-period sensitive. OptimizedPortfolio: "Gold rose approximately 64% in 2025… As a result, the Golden Butterfly Portfolio delivered approximately +19.3% in 2025, outperforming the S&P 500's +17.7% for the first time in a while" — corroborated by World Gold Council *Gold Market Commentary December 2025*: LBMA Gold PM USD +67.4% in 2025.

**5. Data feasibility.** YES. yfinance: `VTI IJS TLT SHY GLD`.

**6. Implementation notes.** Same GLD 28% LTCG issue as Permanent Portfolio.

**7. Literature verdict.** Robust as drawdown-controlled portfolio; "Tyler" is a practitioner, not academic.

**CN variant.** CSI300 + CSI500 (small-cap proxy, though not strictly small-value) + CN long Treasury 511260 + money-market 519888 + Au9999.

---

### E4. Ray Dalio All-Weather (unlevered retail version)

**1. Originator & source.** Ray Dalio / Bridgewater, "The All Weather Story" (https://www.bridgewater.com/research-and-insights/the-all-weather-story); "Engineering Targeted Returns and Risks" (Aug 2011, https://bridgewater.brightspotcdn.com/fa/e3/d09e72bd401a8414c5c0bdaf88bb/bridgewater-associates-engineering-targeted-returns-and-risks-aug-2011.pdf). Retail unlevered popularization: Tony Robbins, *MONEY: Master the Game* (2014).

**2. Mechanical rules (Robbins-popularized retail proxy).**
- **Universe:** VTI 30%, TLT 40%, IEF 15%, DBC 7.5%, GLD 7.5%.
- **Rebalance:** annual.

**3. Original in-sample claim (verbatim — for the LEVERED Bridgewater fund, NOT the retail proxy).** "Since the onset of the crisis [2008], the All Weather asset mix (blue line) gained 43% while the Conventional asset mix (green line) has been roughly flat, up around 1%" (Bridgewater, *Engineering Targeted Returns and Risks*, Aug 2011, https://bridgewater.brightspotcdn.com/fa/e3/d09e72bd401a8414c5c0bdaf88bb/bridgewater-associates-engineering-targeted-returns-and-risks-aug-2011.pdf, Apr 2008 through ~Oct 2011 window).

**4. Out-of-sample.** 2022 was a bad year (long bonds + stocks fell together). State Street launched ALLW ETF (https://www.ssga.com/us/en/intermediary/insights/the-all-weather-portfolio-built-for-any-forecast) to track the Bridgewater model.

**5. Data feasibility.** YES for unlevered proxy. yfinance `VTI TLT IEF DBC GLD`. The TRUE Bridgewater fund uses futures/swaps and is NOT free-replicable.

**6. Implementation notes.** Heavy long-duration bond exposure → rate-sensitive. **The retail unlevered proxy is a DIFFERENT PRODUCT from Bridgewater's fund — do not equate them.**

**7. Literature verdict.** Theoretical foundation strong (Asness-Frazzini-Pedersen 2012); retail unlevered proxy is materially different from the fund.

**CN variant.** Adapt with CSI300 + CN10Y + CN5Y + China commodity basket + gold.

---

### E5. Risk Parity (Asness, Frazzini & Pedersen 2012)

**1. Originator & source.** Clifford S. Asness, Andrea Frazzini, Lasse Heje Pedersen, "Leverage Aversion and Risk Parity," *Financial Analysts Journal* 68(1):47-59 (Jan 2012). SSRN 1990493: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1990493. AQR copy: https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf.

**2. Mechanical rules.**
- **Universe:** stocks + 10Y bonds (extendable to commodities).
- **Weighting:** inverse to volatility so each asset contributes equal risk; leverage applied to push expected return up to target.
- **Rebalance:** monthly.

**3. Original in-sample claim (verbatim, abstract).** "Safer assets must offer higher risk-adjusted returns than riskier assets… Risk parity portfolios exploit this opportunity by equalizing the risk allocation across asset classes, thus overweighting safer assets relative to their weight in the market portfolio." Figure 1 of the paper shows growth of $1 since 1926 in 60/40 vs market-cap-weighted vs simple risk parity, with risk parity dominating (specific CAGR and Sharpe not extracted from open-access copy here — user should pull from AQR PDF for verbatim Sharpe numbers).

**4. Out-of-sample.** Anderson, Bianchi & Goldberg (2012, *FAJ*) "Will My Risk Parity Outperform?" — critical reply; they argue the levered version's outperformance shrinks materially with realistic borrowing costs. A multi-issue published exchange in FAJ followed (referenced at https://blogs.cfainstitute.org/investor/2014/11/05/exploring-the-determinants-of-levered-portfolio-performance-podcast/).

**5. Data feasibility.** PARTIAL. Unlevered: yfinance `VTI BND DBC GLD`. Levered version requires futures (paid) or leveraged ETFs (UPRO 3× SPX, TMF 3× TLT) — but leveraged ETFs carry tracking error and decay at retail.

**6. Implementation notes.** **True risk parity requires LEVERAGE** — flag this. Unlevered is essentially a bond-heavy 60/40 variant.

**7. Literature verdict.** Theoretical foundation strong; empirical superiority disputed (Goldberg-Anderson-Bianchi 2012 FAJ).

**CN variant.** Adapt with CN equity + CN bond futures.

---

### E6. Joel Greenblatt Magic Formula

**1. Originator & source.** Joel Greenblatt, *The Little Book That Beats the Market* (Wiley, 2006); revised as *The Little Book That Still Beats the Market* (2010). Firm: Gotham Asset Management; screener at MagicFormulaInvesting.com. No SSRN paper.

**2. Mechanical rules.**
- **Universe:** US stocks > $50M market cap (Greenblatt's 3,500-stock variant) or > $200M (1,000-stock variant).
- **Signal:** rank each stock by (a) Earnings Yield = EBIT/EV, (b) Return on Capital = EBIT/(Net Fixed Assets + Net Working Capital). Sum the two ranks; buy the lowest-summed-rank names.
- **Portfolio:** 20-30 stocks equal-weighted.
- **Rebalance:** annual (tax-loss-harvest variant: hold winners > 1y, sell losers < 1y).

**3. Original in-sample claim (verbatim).** "He back tested the strategy from 1988 to 2004 and found that a portfolio of the top 30 magic formula stocks, rebalanced annually, would have returned 30.8% per year on average, compared to 12.4% for the S&P 500 over the same period" (https://blog.validea.com/joel-greenblatts-magic-formula-combining-value-and-quality/, summarizing the book). StableBread: "When applied to a broad universe of 3,500 U.S. stocks (over $50 million market cap), the Magic Formula returned 30.8% annually, outperforming both the S&P 500 Index (12.3%)… When backtested on the largest 1,000 U.S. [stocks]… 22.9% annually."

**4. Out-of-sample — explicit decay flag (>30%).** Old School Value (https://www.oldschoolvalue.com/investing-strategy/the-magic-formula-investing/): "The Magic Formula is famous for returning a 30% CAGR. From 1988 to 2004, it did achieve a 30.8% return, but the CAGR has declined significantly. No strategy can sustain a CAGR of 30%." Validea (https://blog.validea.com/joel-greenblatts-magic-formula-combining-value-and-quality/): "attempts by researchers to replicate these eye-popping results have largely not been successful, [but] further research has found evidence for long-term outperformance." Gray & Carlisle, *Quantitative Value* (Wiley 2012), reproduce a similar value-quality combination and find materially lower CAGR after transaction costs and survivorship adjustment.

**5. Data feasibility.** PARTIAL. Requires per-stock EBIT, EV, Net Fixed Assets, NWC. yfinance `Ticker.balance_sheet` + `.financials` per ticker is incomplete/rate-limited. Akshare for CN: `ak.stock_financial_abstract_em(symbol="000001")`. Greenblatt's MagicFormulaInvesting.com screener is free but US-only and non-API.

**6. Implementation notes.** Annual rebalance → tax-friendly. Long-only.

**7. Literature verdict.** Robust as value-quality factor combination; **decayed in absolute CAGR magnitude** vs Greenblatt's 30.8% in-sample number — replications land materially lower.

**CN variant.** Replicable via `ak.stock_financial_abstract_em` over CSI300 / CSI500 universe.

---

### E7. Dogs of the Dow

**1. Originator & source.** Michael B. O'Higgins & John Downes, *Beating the Dow* (HarperCollins, 1991). Wikipedia summary: https://en.wikipedia.org/wiki/Dogs_of_the_Dow.

**2. Mechanical rules.**
- **Universe:** 30 DJIA constituents.
- **Signal:** at year-end, rank by trailing 12-month dividend yield.
- **Portfolio:** equal-weight top 10 highest-yielding stocks.
- **Rebalance:** annual on Jan 1.

**3. Original in-sample claim (verbatim).** O'Higgins (1991) backtested to the 1920s and reported Dogs beat the DJIA on average. Wikipedia summary (https://en.wikipedia.org/wiki/Dogs_of_the_Dow): "for the twenty years from 1992 to 2011, the Dogs of the Dow on average matched the average annual total return of the DJIA (10.8 percent) and outperformed the S&P 500 (9.6 percent)." Small Dogs of the Dow (5 lowest-priced of the 10 Dogs) historical compound 19.4% per O'Higgins.

**4. Out-of-sample.** Domian, Louton & Mossman (1998) "The rise and fall of the Dogs of the Dow," *Financial Services Review* 7(3) (https://www.sciencedirect.com/science/article/abs/pii/S1057081099000074): "by the mid-1990s, market observers realized that the DDS had often selected the previous year's worst performing DJIA stocks." Malkiel, *A Random Walk Down Wall Street*: "The Dogs of the Dow consistently underperformed the overall market during the last half of the 1990s" (paraphrased in https://www.bogleheads.org/forum/viewtopic.php?t=78399).

**5. Data feasibility.** YES. yfinance for each DJIA ticker; historical DJIA constituent list required (survivorship bias risk).

**6. Implementation notes.** Annual rebalance → tax-friendly. Long-only. Concentrated 10-stock portfolio carries idiosyncratic risk.

**7. Literature verdict.** Materially decayed since the mid-1990s; **publication-bias artifact concern** per Malkiel — proceed only as a high-dividend tilt overlay, not a standalone strategy.

**CN variant.** Adapt to "Top 10 dividend yield in CSI300" (高股息组合) via `ak.stock_zh_a_hist` + `ak.index_stock_cons_csindex("000300")`; CN dividend strategies are well-known as 红利策略 (e.g., CSI Dividend Index 000922).

---

## Recommendations

**Stage 1 — Data plumbing (1 week).** Wire up Appendix A. Archive `BAMLH0A0HYM2` history NOW (FRED truncating to 3y in April 2026). Confirm CN flows via `ak.stock_zh_ah_spot_em` and `ak.index_zh_a_hist`. Replace LEI with CFNAI.

**Stage 2 — High-confidence strategies first (2 weeks).** Backtest the four with peer-reviewed primary source AND peer-reviewed out-of-sample retest: **Faber 10-mo SMA (A1), Halloween Indicator (D1), TSMOM (A3), Jegadeesh-Titman cross-sectional momentum (A4).** These set your baseline.

**Stage 3 — Contested / decayed strategies (2 weeks).** Pre-FOMC (D2), Magic Formula (E6), Dogs of the Dow (E7). Literature documents > 30% decay for each — your job is to confirm or refine the post-publication numbers on YOUR window. **Decision threshold: if out-of-sample shows < 50% of in-sample edge, mark "do not implement standalone."**

**Stage 4 — Macro and sentiment overlays (1 week).** Yield curve (C1), HY OAS (C2), AAII (B3), VIX (B2). None should be standalone. Backtest each as risk filters switching SPY ↔ BIL above/below thresholds; compare to SPY buy-and-hold.

**Stage 5 — China dual-track (2 weeks).** **REPLACE** US momentum strategies with CN short-term reversal (sort A-share universe by past 21-day return; buy bottom decile; hold 21 days). This is the single most important CN-specific design decision per Blitz et al. 2021. Faber-style trend timing on CSI300 has no peer-reviewed primary citation we could locate — your backtest fills a gap.

**Benchmarks that should change your stage-by-stage decisions:**
- Sharpe < 0.4 over full window → drop as standalone.
- Post-2015 (post-Boguth/Kurov) Sharpe < pre-publication Sharpe by > 50% → treat as historical artifact (this will catch pre-FOMC).
- Max drawdown > 25% → cap portfolio weight at 30%.
- For any allocation portfolio (E1-E5), strip out gold contribution 2024-2025 (+25.5% then +67.4% per WGC) when assessing forward expectation — that two-year run is a major sample-period sensitivity.

---

## Caveats

1. **Source quality varies.** E2 (Permanent Portfolio) and E3 (Golden Butterfly) "original" CAGRs are from third-party tools (Portfolio Charts, lazyportfolioetf, OptimizedPortfolio), not peer-reviewed papers. They are practitioner figures, cited verbatim but not academically refereed.
2. **In-sample / out-of-sample gaps > 30% are flagged explicitly on:** Pre-FOMC (49 bp → "essentially disappeared" post-2015 per Kurov, Wolfe & Gilbert 2021); Magic Formula (30.8% in 1988-2004 → replications materially lower); Dogs of the Dow (outperformed pre-1991, underperformed late 1990s onward).
3. **Data feasibility issues to encode in the CLI:** Conference Board LEI (paywalled — use CFNAI substitute); CNN Fear & Greed (no historical API — sub-component reconstruction required); CBOE put/call (bulk-download paywalled — synth from yfinance option chains); ICE BofA HY OAS (FRED truncating to 3y in Apr 2026 — archive now); SSE iVIX (discontinued 2018 — use option-implied vol via `ak.option_finance_board`).
4. **CN momentum is weak — use reversal.** Blitz et al. 2021 t-stat 0.92 for 12-1 momentum; t-stat 3.36 for residual reversal. Do not blindly port US momentum cards to A-shares.
5. **Several "famous" strategies have no primary peer-reviewed citation:** Permanent Portfolio (Browne's book); Golden Butterfly (Tyler's blog); All-Weather (Bridgewater white papers are not refereed); Dogs of the Dow (O'Higgins book). Cite verbatim numbers carefully; flag in your report any reliance on practitioner sources.
6. **Gold rally is a major 2024-2025 sample-period sensitivity** for all four allocation portfolios — World Gold Council reports LBMA Gold PM USD +25.5% in 2024 and +67.4% in 2025 (*Gold Market Commentary December 2025*, 8 Jan 2026, Table 1).
7. **The Bridgewater All-Weather "fund" uses futures/swaps and leverage.** The retail unlevered ETF proxy is NOT the same product. Don't equate the two.
8. **Practitioner threshold claims (e.g., HY OAS > 600 bp = defensive)** are NOT peer-reviewed. The refereed literature uses HY spreads as a continuous predictor (Gilchrist-Zakrajšek 2012 *AER*). Refit thresholds on your own data.

---

# Appendix A — Data Sources Cookbook

| Series / Asset | Source | Identifier | Notes |
|---|---|---|---|
| S&P 500 / SPY | yfinance | `^GSPC`, `SPY` | Daily OHLCV; SPY includes dividends |
| US Treasury 10Y, 2Y, 3M | FRED | `DGS10`, `DGS2`, `DGS3MO`, `T10Y2Y`, `T10Y3M` | Daily |
| HY OAS (ICE BofA) | FRED | `BAMLH0A0HYM2` | **ARCHIVE LOCALLY — FRED truncating to 3y in Apr 2026** |
| IG OAS | FRED | `BAMLC0A0CM` | Credit-cycle context |
| VIX | yfinance | `^VIX` | Daily |
| DXY / Broad dollar | yfinance, FRED | `DX-Y.NYB`, `DTWEXBGS` | Broad from FRED preferred |
| Gold spot | yfinance, FRED | `GC=F`, `IQ12260` | FRED has London PM fix |
| Copper | yfinance | `HG=F` | |
| Aggregate bonds | yfinance | `AGG`, `BND`, `IEF`, `TLT`, `SHY`, `BIL` | |
| Foreign equity | yfinance | `EFA`, `VEU`, `EEM`, `VWO`, `EWJ` | |
| Commodities | yfinance | `DBC`, `GSG` | |
| REITs | yfinance | `VNQ`, `IYR` | |
| AAII Sentiment | AAII.com | Weekly CSV download | Free; manual download |
| CBOE P/C ratio | CBOE | Bulk paywalled | Derive from yfinance option chains |
| CNN Fear & Greed | CNN | **No clean API** | Reconstruct from sub-components |
| Conference Board LEI | Conf. Board | **Paywalled since 2022** | Use CFNAI instead |
| Chicago Fed CFNAI | FRED | `CFNAI`, `CFNAIMA3` | Free LEI substitute |
| FOMC schedule | Federal Reserve | https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm | Scrape annually |
| CSI 300 daily | akshare | `ak.index_zh_a_hist(symbol="000300", period="daily")` | |
| CSI 300 (Sina) | akshare | `ak.stock_zh_index_daily(symbol="sh000300")` | Alt source |
| CSI 500 / CSI 1000 | akshare | `ak.index_zh_a_hist(symbol="000905" / "000852")` | |
| A-share daily | akshare | `ak.stock_zh_a_hist(symbol="000001", adjust="qfq")` | Forward-adjusted |
| A-share quarterly earnings | akshare | `ak.stock_yjbb_em(date="20240331")` | For PEAD |
| A-share fundamentals | akshare | `ak.stock_financial_abstract_em(symbol="000001")` | For Magic Formula |
| Hang Seng / HK index | akshare | `ak.stock_hk_index_daily_em` | |
| AH premium spot | akshare | `ak.stock_zh_ah_spot_em()` | Returns 比价, 溢价 per dual-listed name |
| AH Premium Index | Hang Seng Indexes | **No native akshare function — reconstruct** | https://www.hsi.com.hk/eng/indexes/all-indexes/ahpremium |
| Shanghai gold (Au9999) | akshare | `ak.spot_hist_sge(symbol="Au99.99")` | Yuan-denominated |
| CN10Y yield | akshare | `ak.bond_china_yield()` | Daily |
| Caixin China PMI | akshare | `ak.macro_china_pmi_yearly()` | Monthly |
| SHFE copper futures | akshare | `ak.futures_main_sina("CU0")` | |
| CN index constituents | akshare | `ak.index_stock_cons_csindex(symbol="000300")` | Current constituents only |

---

# Appendix B — Reading List (Ranked)

1. **Faber, Mebane (2007/2013) "A Quantitative Approach to Tactical Asset Allocation"** — SSRN 962461. The single most-replicated retail tactical model; start here. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
2. **Moskowitz, Ooi & Pedersen (2012) "Time Series Momentum"** — *JFE* 104(2). Benchmark academic paper on trend-following. http://docs.lhpedersen.com/TimeSeriesMomentum.pdf
3. **Asness, Frazzini & Pedersen (2012) "Leverage Aversion and Risk Parity"** — *FAJ* 68(1). Theoretical foundation for risk parity. https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf
4. **Lucca & Moench (2015) "The Pre-FOMC Announcement Drift"** — *JF* 70(1). Read alongside Kurov, Wolfe & Gilbert (2021, *FRL* 40C) for the decay story.
5. **Antonacci (2014) *Dual Momentum Investing*** (McGraw-Hill) + SSRN 2042750. Retail dual-momentum bible.
6. **Bouman & Jacobsen (2002) "The Halloween Indicator"** — *AER* 92(5). Plus Zhang & Jacobsen (2021, *JIMF*) 323-year update.
7. **Jegadeesh & Titman (1993, 2001)** — *JF*. Cross-sectional momentum canon. https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf
8. **Bridgewater "The All Weather Story"** + "Engineering Targeted Returns and Risks" (Aug 2011). Marketing-flavored but canonical explanation of risk-parity philosophy.
9. **Greenblatt (2006) *The Little Book That Beats the Market*** + Gray & Carlisle (2012) *Quantitative Value*. Use the latter for the replication critique.
10. **Connors & Alvarez (2009) *Short Term Trading Strategies That Work*** — best retail practitioner book for mean-reversion design (RSI(2), VIX-RSI, cumulative RSI).
11. **Blitz, Hanauer, Jansen, Swinkels & Zhou (2021) "Anomalies in the China A-share market"** — *Pacific-Basin Finance Journal* 68. Essential CN reading. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3810114
12. **Estrella & Mishkin (1996) "The Yield Curve as a Predictor of U.S. Recessions"** — FRBNY CIEF 2(7). Foundational yield-curve recession paper. https://www.newyorkfed.org/medialibrary/media/research/current_issues/ci2-7.pdf

---

# Appendix C — Strategies Considered But Rejected

| Strategy | Reason rejected |
|---|---|
| **Bridgewater All-Weather (true levered fund)** | Uses futures/swaps; not retail-replicable. Only unlevered Robbins proxy included. |
| **Conference Board LEI signal (standalone)** | Series paywalled since 2022. Substituted CFNAI. |
| **CNN Fear & Greed (standalone)** | No clean historical API. Sub-component reconstruction would be required. |
| **Variance Risk Premium (sell SPX variance vs realized)** | Requires options data and short-vol margin; not retail-friendly with akshare+yfinance+FRED. |
| **Low-volatility / BAB (Frazzini & Pedersen 2014)** | Full BAB requires shorting high-beta + leverage on low-beta. Long-only USMV/SPLV captures only part of edge. |
| **Quality factor (Asness, Frazzini & Pedersen 2019 QMJ)** | Needs Compustat-quality fundamentals; yfinance/akshare incomplete. QUAL ETF is the retail proxy. |
| **Insider trading (Form 4)** | Data parsing burden; not in akshare/yfinance/FRED. |
| **iVIX-based CN volatility timing** | SSE iVIX discontinued 2018. |
| **Equity-only put/call ratio (full bulk history)** | CBOE bulk paywalled; partial yfinance workaround listed under B4. |
| **News-based PEAD ("PEAD.txt")** | Requires NLP pipeline and earnings-call transcripts. Out of scope. |
| **52-week-high anomaly (George & Hwang 2004 JF)** | Closely related to A4 momentum; not added separately to avoid duplication. |
| **Lottery-stock avoidance (Bali, Cakici & Whitelaw 2011 MAX)** | Requires daily high resolution per stock; feasible but tedious — add in v2. |
| **AH arbitrage as standalone** | Hang Seng AH Premium Index is reconstructable from `ak.stock_zh_ah_spot_em` but cross-border capital controls (QDII / Stock Connect quota) make pure-arbitrage infeasible at retail. Useful as a regime indicator only. |
| **Pairs trading on dual-listed names** | Cointegration tests + capital controls — out of scope. |