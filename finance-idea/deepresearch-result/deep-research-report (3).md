# 2026 年个人投资者可实施的公开系统化择时与权益策略综述

## 研究口径

这份综述只纳入两类证据：一类是原始论文、专著或可追溯到命名实践者的首要来源；另一类是后续独立复测或长期样本外更新。凡是原文并未给出 CAGR、Sharpe 或最大回撤的，我不自行“补齐”为精确数字；相反，我明确标注为“原文未披露”或“仅为事件研究/预测回归结果”。这是因为很多经典文献本质上是在研究“可预测性”或“事件窗口超额收益”，并不是为个人投资者写的同口径组合回测报告。对所有“等待信号、长时间持币”的策略，我额外用 DCA 文献提醒一个重要基线：在风险资产长期正期望收益存在时，DCA 通常比一次性投入更稳，但预期收益常低于立即投入；因此，任何因择时而显著降低资金在场率的策略，都必须用更低回撤或更高风险调整收益来“补回来”。citeturn9search1turn33search2

下文把“策略是否值得 2026 年个人投资者实现”放在三个维度上判断。第一，**证据强度**：是否有原始来源，且是否有独立样本外更新。第二，**实现摩擦**：是否只需月频 ETF、是否需要做空/杠杆/期货、是否高度税敏感。第三，**适用角色**：是“提高长期复利”的主策略，还是“降低深度回撤”的风控覆盖层。结论用四档词汇统一表述：**稳健**、**已衰减但可作风控过滤器**、**更像发表偏差产物**、**不建议落地**。citeturn21search5turn22search0turn30search1turn14search3

## 趋势与动量

**Faber 200 日均线绝对动量。**  
**来源。** Mebane Faber，2007/2013，《A Quantitative Approach to Tactical Asset Allocation》。原始来源链接：`https://papers.ssrn.com/abstract=962461`。**规则。** 以月末价格与 10 个月 SMA 比较，月末收盘高于均线则下月持有标的；低于均线则下月持有 3 个月国库券。对单一标的版本，Faber用的是 S&P 500 总回报序列；对组合版则逐资产独立判断。月频调仓，交易非常低频。citeturn21search5turn26view0  
**原始结果。** Faber 在 1901–2012 的 S&P 500 总回报样本中报告：买入持有 CAGR 为 9.32%，均线择时为 10.18%；波动率从 17.87% 降到 11.97%；Sharpe 从 0.32 升到 0.55；最大回撤从 -83.46% 改善到 -50.29%；系统正收益月份占比 75.80%，并且平均不到一年一次往返交易。citeturn3view0  
**样本外更新。** Zakamulin 采用更严格的样本外与交易成本口径后发现，传统 MA/TSMOM 文献普遍高估了表现。对 1930–2012 的 S&P Composite，买入持有月均收益为 0.90%，Sharpe 为 0.109、最大回撤 -79.18%；而 MA 规则样本外月均收益降到 0.71%，Sharpe 仅小幅升到 0.120，增长终值也低于买入持有。和 Faber 的“Sharpe 提升约 72%”相比，摩擦后的 Sharpe 提升只剩大约 10%，衰减幅度显著超过 30%。citeturn24view2turn24view1  
**三基准对照。** 对同一底层的买入持有，原始文献支持其“回撤控制显著优于持有”。对现金，Faber 明确把 3 个月 T-Bill 作为离场资产。对月度 DCA，原始文献**未给出可审计数值对照**；结合 DCA 文献，只能说凡是因为等待信号而经常持币的体系，若没有明确回撤优势，预期很难击败持续月投。citeturn3view0turn9search1turn33search2  
**税费与实现。** Faber 估计 ETF/共同基金管理费约 0.10%–0.70%，组合层面一年大约 3–4 次往返交易，组合年换手接近 70%；他引用 Gannon/Blum 的税后估计，认为把换手从 20% 提到 70%，对最高税档投资者的额外税后“发型”不到 50bp。对美国应税账户，这类策略并非“免税”；对你给定的“中国 20% 资本利得税”压力测试，若真按每次实现收益征税，长期优势会被明显侵蚀。可实现载具是 SPY/VOO 或指数基金；数据用 yfinance/FRED 即可。**结论：已衰减但可作风控过滤器。** citeturn5view0turn21search5

**均线门控定投。**  
**来源。** 这不是一篇有公认“原始论文”的独立经典策略，而是把 Faber 的 200 日/10 月均线信号改写为**现金流版本**：只在指数位于长期均线下方时把当月新增现金投入股市，不做卖出，其他月份现金留在 T-Bill。原始信号来源仍是 Faber；而把月度现金流与 DCA/择时纳入统一分析的理论基础可参考 Kirkby 等关于 DCA 与“平均式择时”的建模论文，以及 He/Wang 对 DCA 与月度时点投入方法的比较。原始信号来源链接：`https://papers.ssrn.com/abstract=962461`；DCA 理论文献链接：`https://ssrn.com/abstract=3588099`。citeturn21search5turn9search5turn33search11  
**规则。** 每月固定投入金额 \(C\)。若月末 SPX 或 SPY 收盘低于 200 日均线，则在下一个交易日买入当月金额；若高于均线，则这笔新增现金停留在 3 个月国库券，不追投、不补仓、不卖旧仓。月频检查，10bp 单边滑点。citeturn21search5turn9search1  
**原始结果与样本外。** **公开首要文献并没有为这个“门控 DCA”变体给出可审计的原始 CAGR/Sharpe/MaxDD。** 现有 DCA 文献的共同结论，是“时间分散投资”在行为上有价值，但与立即投入或某些时点投入法相比，收益排序高度依赖现金在场率与市场单边上涨环境；He/Wang 明确就是在比较月度现金流环境下的 DCA 与若干择时变体。也就是说，这个策略更像一条**行为纪律规则**，而不是已经被充分证实的阿尔法来源。citeturn9search1turn33search11turn33search2  
**三基准对照。** 与同底层买入持有相比，它几乎必然提高现金占比；与普通月度 DCA 相比，只有在“下跌期投入获得的更低成本”足以弥补“上涨期滞留现金”的代价时，才有机会占优。公开文献能支持“DCA 是强基准”，但不能支持“本变体稳定优于 DCA”。与现金相比，它显然只是在择时地从现金转入股票。**结论：证据不足，只适合把它当作情绪管理规则，不宜当作核心 alpha 策略。** citeturn9search1turn33search2turn33search11

**GTAA 10 月均线。**  
**来源。** 同样出自 Faber 的《A Quantitative Approach to Tactical Asset Allocation》。原始来源链接：`https://papers.ssrn.com/abstract=962461`。**规则。** 五大类资产等权配置：美国股票、外国股票、美国债券、REITs、商品。月末若该资产高于其 10 个月 SMA，则保留该 20% 配置；否则该 20% 进入 T-Bill。组合月度再平衡。citeturn21search5turn4view1  
**原始结果。** Faber 对 1973–2012 的五资产等权组合写得非常明确：择时组合把波动率降到了“个位数”，最大回撤从约 46% 降到不足 10%，而且自 1973 年起只有一个年份的年度跌幅超过 -1%。这是典型的“用 time-in-market 换 drawdown”的版本。citeturn4view1  
**样本外更新。** Faber 自己把 2006–2012 定义为样本外：买入持有年化回报 3.94%，GTAA 为 6.01%；波动率 14.96% 对 7.27%；Sharpe 0.16 对 0.61；最大回撤 -46.00% 对 -9.42%。这组数字很强，但必须注意：这是**作者本人更新**，并非独立第三方完全重建。以及，它处在 2008 金融危机这类趋势跟随非常占优的窗口。citeturn3view3  
**三基准对照。** 对同底层五资产买入持有，GTAA 显著改善回撤；对现金，它把大约 30% 时间留在现金附近；对同底层月度 DCA，公开首要文献仍然**没有**给出可审计同口径。税费和实现层面，Faber 认为组合年往返约 3–4 次，交易成本小，但税务不可忽视。对个人投资者，这一策略可用 ETF 完成：SPY、VEA/IEFA、IEF/TLT、VNQ、DBC/GSG；中国投资者若只做美股 ETF，也足够。**结论：稳健，但更适合税延账户或低税账户。** citeturn5view0turn3view3turn4view1

**Dual Momentum。**  
**来源。** Gary Antonacci，2012/2013，《Risk Premia Harvesting Through Dual Momentum》。原始来源链接：`https://papers.ssrn.com/abstract=2042750`。**规则。** 先做相对动量，在模块内选过去 12 个月表现更强的风险资产；再做绝对动量，若该资产过去 12 个月未跑赢 T-Bill，则持有 T-Bill。Antonacci 在论文中用的是多个模块；个人投资者最常见的 ETF 化版本是美国股票/海外股票/T-Bill 的 GEM 框架，月频执行。citeturn26view0  
**原始结果。** Antonacci 在 1974–2011 的四模块等权复合组合上报告：年化回报 14.93%，年化波动 7.99%，Sharpe 1.07，最大回撤 -10.92%；而单独的“权益模块”Dual Momentum 为年化 15.79%、Sharpe 0.73、最大回撤 -23.01%，对应静态权益基准年化 10.35%、Sharpe 0.38、最大回撤 -44.56%。citeturn27view1  
**样本外更新。** Yao/Wang 等对 1927–2017 美国股票宇宙的 TSMOM/dual-momentum 扩展发现，双重动量的价值加权月度收益 1.74%，显著高于标准 TSMOM 的 0.76%；但作者也同时指出，交易成本会削弱而不必然完全抹去该效应。要强调的是，这个独立更新针对的是**股票横截面版本**，不等于 Antonacci 的简单 ETF 轮动版；它证明的是双重动量思想仍有生命力，而不是“ETF 版原封不动没衰减”。citeturn25view0  
**三基准对照。** 对买入持有同底层权益基准，Antonacci 的原始结果优势非常大。对现金，T-Bill 本来就是其 fallback 资产。对月度 DCA，原文仍未给出同口径，但由于该策略月频、资金在场率较高且回撤控制强，逻辑上比“高现金待机”的择时法更有机会在 DCA 面前存活。ETF 实现极其容易；税费敏感度中等；不需要做空。**结论：三类 ETF 就能做的最强公开战术框架之一，属稳健。** citeturn27view1turn25view0turn9search1

**Time-Series Momentum / CTA。**  
**来源。** Moskowitz、Ooi、Pedersen，2012，《Time Series Momentum》。原始来源链接：`https://doi.org/10.1016/j.jfineco.2011.11.003`。**规则。** 在 58 个流动性很高的股指、债券、商品、外汇期货上，按照过去 12 个月收益符号决定下月多空方向，通常再做波动率目标化。典型 CTA 实现会做多也会做空，并且使用期货。citeturn29view0turn28view0  
**原始结果。** MOP 原文的核心主张是：58 个期货工具都存在显著 time-series momentum；一个跨资产类别分散的 TSMOM 组合能提供“可观的 abnormal returns”，且对标准资产定价因子暴露很低，并在极端市场中表现最好。原始摘要并未在公开 HTML 中给出单一 CAGR/MaxDD 表格。citeturn28view0turn29view0  
**样本外更新。** AQR 的《A Century of Evidence on Trend-Following Investing》把该类策略往前延展到 1880，并报告“自 1880 以来每个十年 trend following 平均收益都为正”。但它也提供了一个重要衰减事实：2000–2009 年该策略平均年化总回报 9.2%，而 2010–2018 只有 1.6%；AQR 将原因部分归因为 2007 年后跨市场相关性上升、可供独立获利的趋势减少。也就是说，**风格没死，但后危机时代风险调整收益确实下降了很多**。citeturn30search1turn30search8  
**三基准对照。** 这类策略不是拿 SPY 与 T-Bill 二选一；它本身是一组跨资产趋势因子。因此对“同底层买入持有”和“同底层 DCA”的简单比较在原始文献里并不存在。对个人投资者，真正的问题是**实现门槛**：若不用期货/做空/杠杆，只用 ETF 做“长/现金”的简化版，策略特性会明显变形。**结论：机构和专业账户稳健，普通零售若无期货条件，不宜原教旨主义落地。** citeturn28view0turn30search1turn30search12

## 均值回归与逆向情绪

**Bollinger 下轨反转。**  
**来源。** John Bollinger 在 1980 年代提出 Bollinger Bands，2001 年出版《Bollinger on Bollinger Bands》。原始来源链接：`https://www.amazon.com/Bollinger-Bands-John/dp/0071373683`。**规则。** 最常见的机械版是：20 日 SMA 为中轨，上下轨为 ±2 个标准差；收盘跌破下轨时买入，回到中轨或固定持有天数后卖出。个人投资者可直接在 SPY、QQQ、单个大票上执行，日频即可。citeturn11search10turn11search16turn20news20  
**原始结果。** 作为指标发明文献，Bollinger 本人的公开可访问来源更多是在定义与用法，而不是给一个统一的长样本绩效表。因此，**原始来源没有一个可直接摘录的“官方 CAGR/Sharpe/MaxDD”**。citeturn11search10turn11search16  
**样本外更新。** Fang/Jacobsen 的“Popularity versus Profitability: Evidence from Bollinger Bands”对 14 个主要股指的研究，说明“广为使用”并不自动等于“稳健赚钱”；2020 年有关 Bollinger Bands 盈利性的综述也延续了一个结论：只有在加入趋势过滤、止损或二次确认时，效果才更接近可交易，而“单独下轨买入”更像是一种情境工具。换句话说，**边际存在，但很依赖过滤器**。citeturn20search2turn20search0turn20news20  
**三基准对照。** 对买入持有同一标的，Bollinger 策略更偏“短打库存管理”；对 DCA，不是同一问题；对现金，只有在短窗口内才有比较意义。税费上，这是典型高短持期策略，对美国短线税和你给定的中国 20% 压力测试都不友好。**结论：已衰减且高度依赖过滤器，不宜裸用。** citeturn20news20turn20search2

**短期反转。**  
**来源。** Bruce Lehmann，1990，《Fads, Martingales, and Market Efficiency》。原始来源链接：`https://www.nber.org/system/files/working_papers/w2533/w2533.pdf`。**规则。** 学术标准版是横截面 long-short：按前一周或前一个月收益把股票排序，买最差分组、卖最好分组，持有一周或一个月后再平衡。个人投资者若没有 CRSP 级别点时数据，几乎无法无偏重建。citeturn11search14  
**原始结果。** Lehmann 在摘要中指出，两种一周期策略都能从“许多相对较小、但可预测的价格反转”中获利，而且这些策略并不依赖于持有流动性特别差的小票；但他同时警告，组合每周可能产生两千多次往返交易，交易成本可能吞噬经济意义。也就是说，原始文献从第一天起就内含了“纸面 alpha 与可实现 alpha 不同”的问题。citeturn11search14  
**样本外更新。** 近年的文献把短期反转更多解释为行业 lead-lag 和流动性提供收益，而非简单“市场犯错”。2024 年相关论文仍然显示短期反转存在，但机制更接近微观结构；Hameed 等的研究也把行业内反转与流动性抽干联系起来。**这意味着：现象仍在，但免费数据 + 零售交易条件下很难净赚。** citeturn11search5turn11search8  
**三基准对照。** 它不是拿 SPY 做 long/cash 的大众策略，和买入持有、DCA、现金的直接同底层比较在原始文献里并不存在。对零售实现而言，成本、滑点和税是核心约束。**结论：学术上真实，零售上基本不建议。** citeturn11search14turn11search5

**VIX 过 30 的逆向买入。**  
**来源。** 这是一条**实践者阈值策略**，不是一篇经典期刊文章。公开可访问、且最接近“原始框架”的权威说明来自 Schroders 对“VIX fear gauge surges”的历史分桶研究。原始实践来源链接：`https://www.schroders.com/en-us/us/individual/insights/how-does-the-stock-market-perform-when-the-vix-fear-gauge-surges/`。**规则。** 当 VIX 收盘高于 30 或约 32.9（Schroders 使用的高恐慌门槛）时，次日买入 S&P 500 指数基金，持有固定窗口；如果要做完全机械化，最干净的是“单次触发后持有 12 个月，信号重叠则忽略”。citeturn18search7turn18search11  
**原始结果。** Schroders 报告，当 VIX 升破 32.9 时，S&P 500 随后 12 个月的平均回报超过 25%。这是一组**事件研究收益**，不是连续复利组合回测。citeturn18search7  
**样本外更新。** 2026 年的《Financial Times》再次做了相同方向的事件复盘：当 VIX 收盘高于 30 时，买入 S&P 500 在后续区间内取得正收益的概率大约为 70%–83%，平均收益为两位数。说明“高恐慌后的正向期望收益”并未消失。citeturn8search12  
**三基准对照。** 与买入持有相比，这不是一条“永续替代策略”，而是仓位追加/战术加仓规则；与月度 DCA 相比，它只在极端恐慌窗口触发，因此更适合叠加到 DCA 之上，而非替代 DCA；与现金相比，它本质上是在利用 VIX 高位时把现金再风险化。实现极其简单：数据用 FRED 的 VIXCLS，载具用 SPY/VOO。税务上，若持有期按 12 个月定义，税敏感度中等。**结论：适合做极端情形加仓器，而不是独立主策略。** citeturn18search7turn18search11turn9search1

**VIX 过 40 的逆向买入。**  
**来源。** “40”是更强烈的实践者洗盘阈值。Hartford Funds 把 40+ 定义为“极高波动”，而 Jeffrey Gundlach 在 2026 年公开表示，若 VIX 上破 40，那“也许就是洗干净了、可以考虑买”的信号。原始实践来源链接：`https://www.hartfordfunds.com/practice-management/client-conversations/managing-volatility/when-fear-runs-high-time-to-buy.html`。citeturn17search1turn17news39  
**规则。** 当 VIX 收盘 > 40 时，次日买入 SPY，持有固定 3、6 或 12 个月；若要避免重叠，则在持有期内忽略新信号。对个人投资者，这比日内“抄底”更可执行。citeturn17search1turn17news39  
**原始结果。** 公开可审计的权威文献**没有为“40 这个精确阈值”提供一套统一的连续策略 CAGR/Sharpe/MaxDD**；能确定的是 40+ 被主流机构视作极端恐慌区，而更宽的 32.9+ 桶历史上对应很高的后续 12 个月回报。citeturn17search1turn18search7  
**样本外更新。** Gundlach 的最新公开表态说明“40 阈值”在 2026 仍被一线宏观投资者当作有效洗盘线；但这还是经验规则，不是点时点资产配置模型。和 VIX>30 相比，它信号更少、均值回归力度可能更强，但统计样本也更小。月度 DCA 对照在公开首要来源中同样缺失，因此更合理的做法是把它作为“危机加仓授权”而不是替代 DCA 的全仓策略。**结论：可用，但属于低频战术按钮，不宜神化。** citeturn17news39turn18search7

## 宏观状态

**10Y–2Y 倒挂并再陡峭化。**  
**来源。** Estrella 与 Mishkin 关于收益率曲线预测衰退的系列研究。原始来源链接：`https://www.nber.org/system/files/working_papers/w5379/w5379.pdf`。**规则。** 一个可回测的个人投资者版是：当 10Y–2Y 利差转负，股权仓降到 0%–50%；当利差重新转正并维持一个月后恢复风险仓。月频执行。citeturn12search12turn12search0  
**原始结果。** Estrella/Mishkin 的核心结果不是“年化回报”，而是**衰退预测能力**：在预测 2 个季度以上的衰退时，收益率曲线斜率是最清晰的领先变量，并且往往能在样本外优于其他候选指标。citeturn12search12  
**样本外更新。** Fed 2006 的进一步工作指出，使用利差加联邦基金利率水平的模型，其样本内拟合和样本外预测都优于只看 term spread 的模型。这意味着“只看倒挂”是可用的，但“倒挂 + 货币政策状态”更好。citeturn12search8  
**三基准对照。** 对买入持有，它更像“回撤前的风险减载器”；对 DCA，它不适合作为每月机械暂停器，因为倒挂到真正下跌之间的时滞长且不稳定；对现金，它当然是把风险资产切回现金。数据完全公开，FRED 即可。**结论：稳健的宏观风控信号，但不是精确的进出场器。** citeturn12search12turn12search8

**HY OAS / default spread 风险过滤。**  
**来源。** Fama/French 1989《Business Conditions and Expected Returns on Stocks and Bonds》。原始来源链接：`https://www.sciencedirect.com/science/article/pii/0304405X89900950`。**规则。** 个人投资者版通常用 ICE BofA US High Yield OAS：若 OAS 高于固定阈值（例如 6%）或高于其 12 个月中位数若干标准差，则降低股票仓位；回落到阈值下方时恢复。原文本身是预测回归，不提供“6%阈值”的官方定义，所以阈值必须由实现者预先固定。citeturn12search1turn12search5  
**原始结果。** Fama/French 的重要发现是：随经济状态变化而波动的风险溢价，对低评级债更强，对股票也更强；换言之，信用利差是“坏时候风险溢价上升”的一个有效代理。citeturn12search1turn12search13  
**样本外更新。** Campbell/Thompson 的样本外股票超额收益预测研究表明，包含这类宏观/估值变量的预测回归，在加入弱符号约束后，能够在样本外略微优于历史均值模型，但 OOS \(R^2\) 很小。这类信号可以用于**慢变量减仓**，不适合做高精度交易。citeturn12search3turn12search11  
**三基准对照。** 对买入持有，这类策略的价值在于“避开信用恐慌期”；对 DCA，若机械暂停供款，很容易因为恢复过慢而损失大量 beta；对现金，它只是风险开关。实现上，FRED 有 OAS 数据，载具是 SPY/VOO 与 SGOV/BIL。**结论：已衰减为风控指标，不要当收益机器。** citeturn12search1turn12search11

**CAPE 估值时钟。**  
**来源。** Campbell/Shiller《Valuation Ratios and the Long-Run Stock Market Outlook》。原始来源链接：`https://www.nber.org/system/files/working_papers/w8221/w8221.pdf`。**规则。** 可回测的个人版必须先固定阈值；例如当 CAPE 位于历史最高十分位时，把股票权重降到 25%–50%，否则保持满配。必须按月/季执行，不得主观加仓。citeturn13search0turn13search8turn13search1  
**原始结果。** Campbell/Shiller 在更新稿中给出非常强的长周期信号：当股息-价格比低于 3.4% 时，在重新回到历史均值之前，股市真实价格**历史上总是**会下跌；并且拟合值暗示 2000 年附近市场重新回到均值时，真实对数价格需要下降超过 1.6。原文强调这些比率更擅长预测未来价格变化，而不是未来股息增长。citeturn13search0turn13search4  
**样本外更新。** 2021 年关于 CAPE/估值预测力的研究仍然支持它对中长期回报有信息，但也强调其真正擅长的是**10 年左右 horizon**，不是 6 个月或 12 个月的战术择时。这意味着 CAPE 更像“慢变量校准器”，不是“卖点计时器”。citeturn13search3turn13search7  
**三基准对照。** 对买入持有，它适合做“高估时降权重”；对 DCA，不应轻易因为高 CAPE 就停投，因为定投天然覆盖长窗口；对现金，长期全现金显然不是合理替代。数据来源极佳：Shiller 官方数据页。**结论：稳健，但只能用于慢变量配置，不用于短线择时。** citeturn13search1turn13search3

**股息率 / Equity Risk Premium 预测。**  
**来源。** Campbell/Thompson，2008，《Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?》。原始来源链接：`https://dash.harvard.edu/bitstreams/7312037c-4c39-6bd4-e053-0100007fdf3b/download`。**规则。** 用股息率、估值和利差变量做月度预测回归；若预测的下期超额收益为正则持有股票，否则持有 T-Bill。为了避免数据挖掘，回归符号和预测值要施加弱约束。citeturn12search3turn12search11  
**原始结果。** Campbell/Thompson 的结论很克制：许多经典预测变量在加入弱的经济符号限制后，样本外可以打败“历史平均超额收益”这个朴素基准；但样本外解释力仍然很小，只是对均值—方差投资者而言具有经济意义。citeturn12search11turn12search15  
**样本外更新。** 这基本已经是对 Goyal/Welch 怀疑论的直接回应，因此“更新”本身就说明该类信号**脆弱但并未归零**。对个人投资者的启示不是“每月切仓”，而是“当 ERP 明显为负时降低权益权重”。**结论：可用于低频仓位校准，不建议做满进满出。** citeturn12search11turn12search7

## 日历与季节

**Sell in May。**  
**来源。** Bouman/Jacobsen，2002，《The Halloween Indicator, “Sell in May and Go Away”》。原始来源链接：`https://www.aeaweb.org/articles?id=10.1257/000282802762024683`。**规则。** 每年 11 月至次年 4 月持有股票，5 月至 10 月持有 T-Bill，半年切换一次。citeturn14search8turn14search4  
**原始结果。** 作者在 37 个发达与新兴市场中发现，36 个市场的 11–4 月收益高于 5–10 月，是典型的跨市场季节效应。citeturn14search4turn14search8  
**样本外更新。** 2021 年综述指出，自 2002 年发表以来，这一效应引发持续争论；2023 年的再研究把“5–10 月切到 T-Bill 与买入持有”的税后影响也纳入讨论，说明在真实账户中，**税与摩擦会显著削弱纸面优势**。对 2026 的个人投资者，这一点比“季节是否仍存在”更重要。citeturn14search0turn14search12  
**三基准对照。** 对买入持有，它在原始文献中赢的是“季节性 beta 划分”；对 DCA，这种“半年停投”非常不友好，因为 DCA 的核心就是不断覆盖时间；对现金，它只是半年退到现金。**结论：有统计现象，但在应税账户里更像发表偏差边缘，不建议重仓依赖。** citeturn14search8turn14search12turn9search1

**Santa Claus Rally。**  
**来源。** Yale Hirsch 在 1972 年《Stock Trader’s Almanac》提出；后续学术验证见 Nippani/Washer/Johnson。原始书籍公开稳定 URL 缺失，定义可由后续权威来源核实。**规则。** 每年只持有最后 5 个交易日加次年最前 2 个交易日，其余时间持有现金/T-Bill。citeturn32search4turn32search10turn14search1  
**原始结果。** 历史统计常见表述是：该 7 个交易日窗口自 1950 年以来平均上涨约 1.3%，上涨年份占比大约 76%。但这不是复利策略，而是极短窗口事件统计。citeturn32news30  
**样本外更新。** 2016 年关于规模维度的研究指出，Santa Claus 效应在小盘股里更明显；但 2023 年对 2000–2021 美国市场的研究却发现，该效应在现代样本中并不普遍。也就是说，**如果把 1926–2014 与 2000–2021 对比，衰减已经非常明显，远超 30%**。citeturn14search17turn32search0  
**三基准对照。** 对买入持有同底层，它只是一个 7 天窗口暴露；对 DCA 完全不构成合理替代；对现金则几乎是“短暂日历下注”。税费方面，这是最不经税的策略之一。**结论：已明显衰减，不建议实盘依赖。** citeturn32news30turn32search0

**Turn-of-the-Month。**  
**来源。** Lakonishok/Smidt，1988，《Are Seasonal Anomalies Real? A Ninety-Year Perspective》。原始来源链接：`https://academic.oup.com/rfs/article-abstract/1/4/403/1566965`。**规则。** 月末最后一个交易日买入，持有到次月第三个交易日卖出（也可采用“最后一日到第三日”四交易日窗口的原始框架）。citeturn15search3  
**原始结果。** 作者在 90 年的 DJIA 日度数据中发现，围绕月末—月初的收益异常持续存在，是他们最稳固的日历异常之一。citeturn15search3turn15search0  
**样本外更新。** McConnell 等进一步把样本扩展到 1897–2005，并指出：在 109 年周期里，DJIA 的全部正收益几乎都来自 turn-of-the-month 窗口，而且这一效应在最近二十年仍然显著。这个更新是少数对日历异常相对友好的长期扩展证据。citeturn15search11  
**三基准对照。** 对买入持有，它是“极低 time-in-market”策略；对 DCA，不适合作为现金流方案；对现金，它是在极短时间内把现金暴露到股票。问题在于真实世界的滑点、税和可复制性会快于统计优势恶化。**结论：统计上仍存在，但对零售税后并不优先。** citeturn15search11turn9search1

**Pre-FOMC Drift。**  
**来源。** Lucca/Moench，《The Pre-FOMC Announcement Drift》。原始来源链接：`https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf`。**规则。** 在预定 FOMC 会议前的短窗口买入美国股票指数，在公告前/后平仓；原版是极窄事件窗口，不是日常持仓策略。citeturn14search11  
**原始结果。** 原论文最重要的事实不是“大盘长期 CAGR”，而是：美国股市相当大一部分超额收益集中在 FOMC 公告前的短窗口里，而且这种 pre-FOMC return 在收益率曲线偏平和 VIX 偏高时期更强。citeturn14search11  
**样本外更新。** Kurov 等把样本延到 2019 年，结论非常明确：这一漂移在 2015 年后基本消失，无论是伴随主席新闻发布会的会议还是普通会议都如此。这是本报告里证据最干净的“**边际已消失**”案例之一。citeturn14search3turn14search18  
**三基准对照。** 对买入持有，它原本像一个“事件窗口 alpha”；对 DCA 完全不是同一类问题；对现金，则只在极窄时段承担风险。由于信号已显著衰减，再加上交易窗口极短、税极不友好，**结论：不建议落地。** citeturn14search3turn14search11

## 配置与回撤控制

**60/40 股债平衡。**  
**来源。** 60/40 并无单一发明者；但现代研究与实践通常把它定义为 60% S&P 500 + 40% 10 年期美国国债，按月再平衡。AQR 的公开研究就使用这一标准定义。参考链接：`https://www.aqr.com/Insights/Perspectives/Risk-Parity-Is-Even-Better-Than-We-Thought`。citeturn6search15turn16search7  
**规则。** 60% 权益、40% 国债，月度或年度再平衡；无需择时。对个人投资者，这是全部系统策略的**现实基准**。citeturn6search15turn16search3  
**原始结果与样本外。** 公开文献把它当“政策基准”远多于“异常策略”，因此并不存在一个单一“原始论文绩效表”。但几乎所有风险平价/全天候研究都以它作为默认对照；也正因此，对 2026 的个人投资者，60/40 的意义是“**先把基线立住，再讨论主动覆盖层**”。税务和实现都友好，ETF 可用 VTI/VOO + IEF/TLT/BND。**结论：不是 alpha 策略，但仍是最重要的比较尺子。** citeturn6search15turn16search3

**Permanent Portfolio。**  
**来源。** Harry Browne，1999，《Fail-Safe Investing》。原书公开稳定 URL 缺失；公开可访问的实践复述明确指出该组合来自 Browne。**规则。** 25% 股票、25% 长期国债、25% 现金、25% 黄金，年度再平衡或在偏离阈值时再平衡。其思想是用四类资产覆盖繁荣、衰退、通胀、通缩四种大环境。citeturn16search4turn16search16turn16search12  
**原始结果与样本外。** Browne 的公开可访问来源强调的是“在任何经济环境下保护与增长财富”的目标，而非一个学术表格式 CAGR/Sharpe/MaxDD。后续实践者持续把它视为低复杂度、低判断依赖的防御组合。对个人投资者，它最大的优点恰恰不是“赢大盘”，而是**把深回撤分散掉**。citeturn16search16turn16search4  
**三基准对照。** 对 SPY 买入持有，它通常会在大牛市明显跑输；对 DCA 者而言，它更像持仓容器而不是入场规则；对现金，它在真实利率下降或通胀冲击环境下更有韧性。实现非常简单，但黄金与长期债的长期低相关性未必一直稳定。**结论：稳健的防守型基座，但不是收益最大化器。** citeturn16search16turn16search4

**Risk Parity / All Weather。**  
**来源。** 风险平价的经典起点常追溯到 Qian，Bridgewater 的 All Weather 则是最著名的实践版本。公开权威链接：Bridgewater《The All Weather Story》`https://www.bridgewater.com/research-and-insights/the-all-weather-story`；Qian 风险平价白皮书公开版亦可访问。citeturn16search2turn16search17  
**规则。** 不是按资金等权，而是按风险贡献近似等权配置股票、名义债、通胀敏感资产，再通过杠杆把组合波动提到目标水平。AQR 对风险平价的概念表述得很明确：它从更低的股票敞口起步，依靠真正的风险分散来争取更高、更稳定的 Sharpe。citeturn16search9turn16search2  
**原始结果。** 公开摘要中，PanAgora/Qian 的白皮书把风险平价描述为“能通过真正分散构造更高效 beta 组合”；而 AQR 2015 的样本外-ish 讨论给出了更硬的数字：模拟风险平价相对 60/40 大致有约 250bp/年的优势；即使把这一优势砍半，Sharpe 改善也发生在 86% 的滚动 10 年窗口。citeturn16search17turn6search15  
**样本外更新。** Bridgewater 的 All Weather 叙事说明了它如何在不同宏观状态中求平衡；AQR 的后续文章则提醒，风险平价的好成绩有相当一部分可能享受了长期债券牛市，因此个人投资者若**不用杠杆**、只用普通 ETF 做“伪风险平价”，结果会与机构版差不少。citeturn16search2turn6search15  
**三基准对照。** 对 60/40，它最主要的比较优势是 Sharpe 和回撤路径，而不一定是裸收益；对 DCA，它更像目标组合容器；对现金，它当然不是替代。实现难度中高：若不用期货或保证金，很难做到“真正的”风险平价。**结论：机构口径稳健，零售若无杠杆能力则只能做近似版。** citeturn6search15turn16search2turn16search9

## 统一比较与三条建议

严格按“原始文献 + 可公开核验更新 + 不伪造同口径回测”的要求，**无法**把全部 20 条策略都放进一个真正统一的 1990-01-01 至 2025-12-31 审计级数值表里。原因很简单：它们混杂了长仓 ETF 轮动、期货多空、事件研究、预测回归和配置模板；很多原文根本不报告 CAGR/MaxDD，或者采用的不是可免费复现的数据口径。所以下表只填入**文献中可直接核验**的同义指标；其余明确标为 N/A，而不是用二手博客数字去“补齐”。citeturn21search5turn22search0turn14search3turn15search11

| 策略 | CAGR/年化回报 | Sharpe | Max DD | 相对月度 DCA 超额 | 文献状态 |
|---|---:|---:|---:|---:|---|
| Faber 200 日/10 月均线 | 10.18% | 0.55 | -50.29% | N/A | 原始单资产完整表可核验。citeturn3view0 |
| 均线门控定投 | N/A | N/A | N/A | N/A | 公开首要文献不足；应视为 DCA 变体，需自行回测。citeturn9search1turn33search11 |
| GTAA 10 月均线 | 6.01%（2006–2012 OOS） | 0.61 | -9.42% | N/A | 作者给出样本外表，但独立第三方统一重建不足。citeturn3view3 |
| Dual Momentum 复合组合 | 14.93% | 1.07 | -10.92% | N/A | 原始论文给出完整统计。citeturn27view1 |
| Time-Series Momentum / CTA | N/A | N/A | N/A | N/A | 原始摘要未给统一表；长期更新显示风格仍正但 2010 后显著降速。citeturn28view0turn30search8 |
| Bollinger 下轨反转 | N/A | N/A | N/A | N/A | 原始指标书无统一绩效表。citeturn11search10 |
| 短期反转 | N/A | N/A | N/A | N/A | 原始文献是横截面长短仓，不是单资产复利策略。citeturn11search14 |
| VIX > 30 买入 | 事件收益：后 12 个月均值 >25% | N/A | N/A | 对 DCA 不同类 | 事件研究而非连续策略。citeturn18search7 |
| VIX > 40 买入 | N/A | N/A | N/A | 对 DCA 不同类 | 阈值偏实践者规则。citeturn17news39turn17search1 |
| 10Y–2Y 倒挂/再陡峭化 | N/A | N/A | N/A | N/A | 预测衰退，不是原始组合回测。citeturn12search12 |
| HY OAS / default spread | N/A | N/A | N/A | N/A | 预测回归，不是原始组合回测。citeturn12search1 |
| CAPE 估值时钟 | N/A | N/A | N/A | N/A | 适用于长周期配重，不是短线组合表。citeturn13search0 |
| 股息率/ERP 预测 | N/A | N/A | N/A | N/A | OOS \(R^2\) 小，但经济上有意义。citeturn12search11 |
| Sell in May | N/A | N/A | N/A | N/A | 原文提供季节差异，不是统一复利表。citeturn14search8 |
| Santa Claus Rally | 约 1.3%/7 交易日 | N/A | N/A | 对 DCA 不同类 | 事件窗口效应。citeturn32news30 |
| Turn-of-the-Month | N/A | N/A | N/A | N/A | 原文/更新都以窗口收益为主。citeturn15search11 |
| Pre-FOMC Drift | N/A | N/A | N/A | 对 DCA 不同类 | 事件窗口效应，且 2015 后基本消失。citeturn14search3 |
| 60/40 | N/A | N/A | N/A | N/A | 基线组合，不是异常策略。citeturn16search7turn16search3 |
| Permanent Portfolio | N/A | N/A | N/A | N/A | 公开首要来源更强调原理而非同口径表。citeturn16search16 |
| Risk Parity / All Weather | 对 60/40 约 +250bp/年 | Sharpe 改善频繁 | N/A | N/A | 相对 60/40 的优势更清楚，绝对统一表缺失。citeturn6search15 |

如果只实施 3 条，我会按“个人投资者 2026 年可执行 + 证据最硬 + 税费后仍有意义”来排序。

**第一条：60/40 作为基线，而不是作为幻想中的 alpha。** 它最大的价值，是给你一个低摩擦、低判断依赖、可持续持有的政策组合；后面的主动规则都应该是覆盖在这个基线上，而不是取代纪律本身。citeturn16search7turn16search3

**第二条：Faber 200 日/10 月均线，只把它当“风控覆盖层”。** 它最强的证据不在于长期永久跑赢股市，而在于回撤管理极具可验证性；但 Zakamulin 已经说明，真实世界 Sharpe 提升远比宣传材料小。所以最合理的用法，是给你的核心权益仓加一个月频刹车，而不是把全部财富押成“我能靠均线打败市场”。citeturn3view0turn24view2turn24view1

**第三条：Dual Momentum 作为最像“个人投资者可复制的强战术模型”的选项。** 它比单一 200 日均线更主动，比期货版 CTA 更容易落地，原始论文给出了完整的年化回报、Sharpe 和最大回撤，而且只需少数 ETF、月频轮动。对于能接受 tracking error、愿意每月执行一次规则的人，它是本报告里最值得认真测试的一条。citeturn27view1turn25view0

反过来说，我不会把 VIX 过阈值、Santa、Pre-FOMC 这类事件型策略放进前三。原因不是它们“统计上完全不存在”，而是它们要么样本太少、要么边际已明显衰减、要么税后不友好。宏观变量如 CAPE、利差和 OAS，我更愿意把它们看作**仓位刻度盘**，而不是“开/关仓按钮”。citeturn14search3turn32search0turn13search3turn12search11

## 数据源附录与局限

**可直接接入 Python 的公开数据源。**  
价格与总回报：`yfinance` 取 SPY、VOO、VTI、VEA、VNQ、IEF、TLT、GLD、DBC 等；若想做中国 ETF，可用 `akshare` 拉取沪深 ETF、指数与利率近似数据。宏观与利率：FRED 取 `VIXCLS`、`TB3MS`、`DGS10`、`DGS2`、`T10Y2Y`、以及高收益利差系列。估值数据：Robert Shiller 官方数据页提供月度价格、股息、盈利和 CPI。FOMC 日历可从 Federal Reserve 官网导入；VIX 历史也可直接从 Cboe/FRED 获得。citeturn18search11turn13search1turn17search4

**建议的最小可实现载具。**  
月频趋势/动量：SPY、VEA/IEFA、BIL/SGOV 即可做简易 Dual Momentum 与 200 日过滤。GTAA 需要再加 REIT 与商品 ETF。宏观信号只需要给股票仓加一个风险开关。日历与事件类策略都只要 SPY，但因为持有期短、税和滑点敏感，现实吸引力远低于回测吸引力。真正的 TSMOM/CTA 与 Risk Parity 如果要保留原策略灵魂，通常需要期货、保证金或至少 leverage-aware 的组合载具；纯 ETF 近似品会改变收益源。citeturn29view0turn16search9turn16search2

**局限。**  
本报告刻意**不**用第三方博客回测去“补齐”那些原始文献没有提供的 CAGR/Sharpe/MaxDD，因此统一表里存在大量 N/A。书籍来源如 Browne、Hirsch、Connors 的不少细节并无稳定开放 URL；我在这些地方优先引用了可公开访问的权威复述或后续学术验证，而不是拿不透明二手摘要硬凑数字。最后，文中对“美国短线税/中国 20% 税”只做**压力测试**使用，不应视为现行税法意见；真正落地前，必须按你的法域、账户类型和券商结算规则重算税后收益。citeturn14search1turn16search16turn9search1