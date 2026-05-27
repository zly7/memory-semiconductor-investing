# 系统化策略提案

这是一份**可编码、可本地回测**的策略提案，而不是统一窗口回测报告。你要求的“规范来源 URL”我用**可点击引文**替代裸链接；这样既满足引用可追溯，也符合本环境不能直接输出原始 URL 的限制。另：我在你的清单之外，补入了两类同样经典且学术关注更高的策略——**长期反转**与**短期反转**。通用税务前提如下：美国 taxable account 中，持有**超过一年**通常属于长期资本利得，**一年及以内**为短期资本利得；中国内地个人转让沪深北交易所上市股票的**价差收益通常暂免个税**，但**股息红利一般以 20% 为名义税率并按持有期享受减免**。以下凡写“高换手税敏感”，均按此理解。citeturn14search0turn14search1turn14search5turn14search8

## 趋势与动量

**Carhart UMD 横截面动量**  
**来源**：Narasimhan Jegadeesh 与 Sheridan Titman，1993；规范来源为《Returns to Buying Winners and Selling Losers》，Carhart(1997)则把它制度化为四因子中的 UMD。citeturn31view0turn33search6  
**机械规则**：若你要**Carhart/FF 风格兼容**，最实用的写法是：全市场普通股；用**过去 12 到 2 个月**累计回报做排序，跳过最近 1 个月；月度调仓；多头买入前 10%（或前 30%），空头卖空后 10%；权重等权或按市值中性。若只做 long-only，可持有胜者分位组合。原始 J/T 文献同时测试了多种 J-K 组合。citeturn31view0turn33search3  
**原始样本**：J/T 在 1965–1989 的 CRSP 样本中写明，**最成功的零成本策略**是“过去 12 个月形成、持有 3 个月”，当形成期与持有期不留空档时月收益 **1.31%**；若中间留 1 周空档，月收益 **1.49%**。表 III 中 6/6 策略的全样本平均月度 winner-minus-loser 收益为 **0.95%**。citeturn32view0turn32view1  
**后续复核**：J/T 1999/2001 明确写道，动量利润在 **1990 年代继续存在**，说明原结果**不是简单 data-snooping**；但 Daniel 与 Moskowitz 之后指出动量存在**crash risk**，尤其在市场剧烈反弹阶段。citeturn33search0turn33search10turn33search13  
**数据可行性**：若要忠实重建 UMD，最佳是 **CRSP/Compustat**；仅用 yfinance 重建会有**存活偏差、退市收益缺失、成分股点位回填**问题。可行的折中是直接下载 Ken French 的 UMD 因子作比较基准，但这超出了你限定的 akshare+yfinance+FRED 栈。  
**实现备注**：零售落地一般做 **MTUM / PDP / QMOM** 这类 ETF 替代，或自己在 S&P 500/中证 800 当前成分股里做近似版。需要做空时，美股可借券；A 股现货基本不适合原教旨 long-short。税务上月频/季频调仓在美国 taxable account 明显税敏感。  
**文献裁决**：**稳健，但有 crash 风险；适合做择股因子，不适合无风控裸奔。** citeturn33search1turn33search13

**时间序列动量与 CTA**  
**来源**：Moskowitz, Ooi, Pedersen，2012；后续百年证据由 Hurst, Ooi, Pedersen，2017 扩展。citeturn27view0turn26view0  
**机械规则**：经典可编码版：对每个合约计算**过去 12 个月回报的符号**，正则做多、负则做空；使用过去 3 年波动率做**波动率缩放**。MOP 文中给出的单资产收益写法是 `sign(r_{t-12,t}) * 0.60% / σ_t * r_{t,t+1}`；组合层将多个市场等风险叠加，形成约 **9.3% 年化 ex-ante 波动**的组合。月度更新即可。citeturn29view0turn28view0  
**原始样本**：原论文在 58 个期货合约的 1985–2009 样本中，报告 TS-MOM 对 MSCI World、SMB、HML、UMD 回归后仍有约 **1.26%/月** 的 alpha；对跨资产 value/momentum 因子控制后仍有 **94bp/月** 的 alpha。另文中指出，58 个合约里**全部都呈现正向可预测性**，其中 **52 个**统计显著。citeturn28view0turn28view1turn28view2  
**后续复核**：Hurst/Ooi/Pedersen 把样本扩展到 **1880–2016**，写明趋势跟随在这 **137 年**里“consistent profitable”；但 Kim 等后续批评指出，部分效果与**波动率管理**密切相关。总体看，边际衰减存在，但长期多资产证据依旧强。citeturn26view0turn21search0  
**数据可行性**：严格版需要多资产期货连续合约；yfinance 能拿到部分代理（`ES=F`, `NQ=F`, `ZB=F`, `CL=F`, `GC=F`, `EURUSD=X` 等），零售足够做 ETF/futures proxy 版，但不等同原样本。  
**实现备注**：零售最小载体是 CME/ICE 期货，或用 ETF 代理；策略天然涉及**做空与杠杆/期货保证金**。CN 变体可做中证股指、国债、黄金、工业品多品种趋势，但国内期货换月和夜盘细节必须单独处理。  
**文献裁决**：**多资产里最稳健的趋势策略之一；适合作为组合层“危机阿尔法”。** citeturn26view0turn28view2

**Faber GTAA 与 Ivy 十月均线**  
**来源**：Meb Faber，2006/2007，后在 2013 年更新。citeturn17view0  
**机械规则**：五资产等权：美国股票、海外股票、美国 10Y 国债、REIT、商品。月末若资产价格**高于其 10 个月简单均线**则持有，否则切到 **90 天 T-bill**；组合月度再平衡。只用**总回报/复权价格**，表现才接近论文。citeturn17view0turn19view0turn19view3  
**原始样本**：Faber 对单资产和五资产都给了核心结果。对 S&P 500 的 1901–2012 样本，Figure 7 报告 buy-and-hold 的 CAGR **9.32%**、波动 **17.87%**、Sharpe **0.32**、MaxDD **-83.46%**；10 个月均线 timing 为 CAGR **10.18%**、波动 **11.97%**、Sharpe **0.55**、MaxDD **-50.29%**。对 GTAA 五资产，文中写道 1973–2012 期间**回撤由 46% 降到低于 10%**。citeturn19view1turn20view0turn20view1  
**后续复核**：Faber 自己在 2006 之后的 **2006–2012**“实时外样本”里写到 timing **每年仍高出 2 个百分点以上**、波动与回撤更低；但 Zakamulin 2014 指出，很多移动均线择时论文对真实世界表现存在**data-mining bias**和**摩擦低估**。citeturn20view2turn21search0turn21search4  
**数据可行性**：完全可用 yfinance+FRED 近似：`SPY`/`VEU`/`IEF`或`TLT`/`VNQ`/`DBC`，现金用 `DTB3` 或 `BIL`。  
**实现备注**：ETF 即可，不必杠杆、不必做空；月频换手较低。CN 变体可做 510300 + 国债 ETF + 黄金 ETF + 海外股票 QDII，但国内“商品 ETF 层”可替代性较弱。  
**文献裁决**：**作为风险滤波器很强；作为纯 alpha 来源，真实世界要下修预期。** citeturn17view0turn21search0

**S&P 500 上穿二百日均线择时**  
**来源**：学术根基可追到 Brock–Lakonishok–LeBaron 的移动平均规则研究；现代实践层最常用的单资产版本，可直接用 Faber 的月度 10 个月均线结果做近似规范来源。citeturn17view0turn19view1  
**机械规则**：你完全可以写两个 `compute()` 版本。`long_only_filter`：若 `SPY Adj Close > SMA200`，持有 SPY；否则持有 `BIL/SHY`。`full_timing`：若低于 SMA200，现金化或切短债；高于 SMA200，再回到 SPY。日频判定用 Adjusted Close；也可只在**月末确认**以减少 whipsaw，这更接近 Faber。citeturn19view0turn20view2  
**原始样本**：在可直接引用的规范来源里，最接近“200 日均线单资产择时”的是 Faber 对 S&P 500 的长期 timing 结果：1901–2012 的 timing CAGR **10.18%** 对比 buy-and-hold **9.32%**；MaxDD 从 **-83.46%** 降至 **-50.29%**。这些数字本质上就是“日线 200 日均线的月末近似版”所追求的目标画像。citeturn19view1turn18view2  
**后续复核**：Zakamulin 2014/2018 的核心结论是：移动均线择时**并没有很多宣传材料写得那么好**，外样本一加入摩擦与参数不确定性后，超额收益会明显缩水；但它作为**降低回撤的机制**依旧成立。citeturn21search0turn21search15  
**数据可行性**：完全可复现：`SPY` 或 `^GSPC`，日频复权价即可；现金腿可用 `BIL` 或 FRED `DTB3`。  
**实现备注**：最小零售工具就是 SPY；无需做空。CN 版非常直接：可以做“**沪深300/中证500/创业板 ETF 的 200/250 日均线过滤**”。  
**文献裁决**：**更适合当回撤控制器，而不是全仓赌超额收益。** citeturn21search0turn19view1

**Antonacci 双重动量 GEM 与 Composite**  
**来源**：Gary Antonacci，2012/2013，《Risk Premia Harvesting Through Dual Momentum》。citeturn23view0turn25search16  
**机械规则**：原论文是**四个模块**的 composite dual momentum；零售版最常做 **GEM**。代码上建议月末：先比较 `VTI` 与 `VEU` 的过去 12 个月总回报，取相对更强者；再检查该胜者是否**跑赢 T-bill/BIL**，若没有，则切到 `IEF`/`BIL`。月度再平衡。论文中的通用范式是：先做**relative momentum**，再用 T-bill 作为**absolute momentum hurdle rate**。citeturn23view0turn24view1  
**原始样本**：Antonacci 在 Table 14 的 1974–2011 复合组合里给出：No Momentum 年化 **9.93%**、Sharpe **0.50**、MaxDD **-27.00%**；Dual Momentum 年化 **14.90%**、Sharpe **1.07**、MaxDD **-10.92%**。citeturn24view1  
**后续复核**：后续独立 ETF 样本研究发现，含“flight-to-safety”机制的 dual momentum 在**风险调整后**通常优于被动指数，但优势较原始宣传数字更温和；Antonacci 自身的 GEM 扩展回测也显示样本外仍然成立。citeturn25search19turn25search4  
**数据可行性**：完全可以用 yfinance 近似：`VTI`、`VEU`、`IEF`、`BIL`。  
**实现备注**：ETF 即可，不要求做空；月频税负中等。CN 变体可做“沪深300 vs 海外中国/亚太权益+国债ETF”的双动量，但国内现货市场可交易“避险腿”选择没有美国市场那么丰富。  
**文献裁决**：**简单、可执行、组合层很有吸引力；但别把书里的全部收益数字当未来可得。** citeturn24view1turn25search19

**PEAD 后公告漂移**  
**来源**：Bernard & Thomas，1989/1990；综述见 Fink，2021。citeturn35search13turn35search2turn35search0  
**机械规则**：标准可编码版：美国普通股；取每次财报公告对应的**标准化盈余意外**（SUE）或近似 surprise；按当季 SUE 分成 decile/quintile；公告次日开盘或收盘建立多空，**多头买高 surprise，空头卖低 surprise**；持有 60 交易日或到下一次财报。long-only 版只持高 surprise 分组。citeturn35search0turn35search6  
**原始样本**：BT 1990 的可获取摘要写明：当前季度盈利所隐含的未来盈利信息**没有被股价充分反映**；后续四个季度的 3 日公告期收益可由当前盈利预测。后续综述文献引用 BT 的核心结果时写到，扩展漂移在随后几次公告期仍可见。citeturn35search2turn35search5turn35search3  
**后续复核**：Fink 2021 明确写 PEAD 是一个**被描述了几十年**的经典异常；但 Kettell 2022 等研究指出，其幅度**显著下降**，部分市场区间甚至接近消失。中国样本近年仍能找到 PEAD 证据。citeturn35search0turn35search10turn35search1turn35search4  
**数据可行性**：**不能**靠 akshare+yfinance+FRED 忠实复现美国版；你需要**历史公告日 + 一致预期 + 实际值**，最好是 I/B/E/S、Compustat、FactSet、Refinitiv。  
**实现备注**：高换手、事件驱动、税敏感；盘后公告与次日缺口必须精细处理。CN 变体存在，而且在散户主导市场中常更强。  
**文献裁决**：**经典但已拥挤；若没有高质量事件数据，不建议硬做。** citeturn35search0turn35search10

## 均值回归与情绪逆向

**短期反转**  
**来源**：Jegadeesh，1990；后续分解研究见 Da, Liu, Schaumburg, 2014。citeturn34search2turn34search6  
**机械规则**：最直接的 `compute()`：全市场普通股，按**过去 1 个月回报**排序；月末买入最差 decile、卖空最好 decile；持有 1 个月，月度滚动。更“论文味”的写法是按可预测回报/自相关估计分十组。citeturn34search2turn34search18  
**原始样本**：后续文献在复述 Jegadeesh(1990) 时给出最常用数字：基于前月收益、持有 1 个月的反转策略，在 1934–1987 样本里大约有 **2%/月** 利润。citeturn34search3turn34search6  
**后续复核**：Da 等指出，传统短反转只是“总效应”的一部分；剥离非基本面成分后，增强版反转的风险调整收益约为标准反转的**三倍**。中国 A 股近年的研究也继续报告短期反转存在。citeturn34search13turn34search6turn6search6  
**数据可行性**：做“学术忠实版”仍然最好用 CRSP；用 yfinance 当前成分股重建会有严重存活偏差。  
**实现备注**：高换手、交易成本敏感、卖空要求高；美国 ETF 层面可用 sector/industry losers 做低频近似，A 股现货则更适合做 long-only 跌深反弹筛选。  
**文献裁决**：**存在，但交易成本吃掉很多；更适合做增强版而不是裸 prior-month losers。** citeturn34search6turn34search13

**长期反转与过度反应**  
**来源**：De Bondt & Thaler，1985，《Does the Stock Market Overreact?》。citeturn34search0turn34search17  
**机械规则**：每年或每季度，对全市场普通股按**过去 36–60 个月累计回报**排序；买入历史 losers，卖空历史 winners；持有 36 个月左右。为减弱 size/value 混杂，可做 industry-neutral 或 beta-neutral。citeturn31view0  
**原始样本**：原始论文的核心发现是：过去 **3–5 年**的极端 loser 在随后 **3–5 年**显著跑赢 extreme winner；我在当前可检索摘要里没有拿到作者给出的统一 CAGR/Sharpe 表，因此这里写“**原文未报告统一组合层 CAGR/Sharpe**”。citeturn34search0turn34search17  
**后续复核**：国际市场后续研究继续找到与过度反应一致的长期反转证据，但其与 size、value、tax-loss selling 的纠缠一直存在；你在中国市场也能找到相关文献。citeturn34search7turn6search14  
**数据可行性**：与短反转一样，**忠实版需要 CRSP/Compustat**；yfinance 只能做幸存者偏差近似。  
**实现备注**：持有期长，税负比短反转友好；但真正的 alpha 主要来自长期 loser basket，而不是简单“跌得多就买”。CN 变体可以做 “过去 3 年极端落后行业/风格篮子”的 long-only mean reversion。  
**文献裁决**：**学术上成立，但实现层必须小心与价值因子、size 因子做区分。** citeturn34search0turn34search7

**VIX 高位逆向买入**  
**来源**：Cipollini & Manzini，2007《Can the VIX Signal Market’s Direction?》；更新可见 Ronn，2025。citeturn37view0turn36search2  
**机械规则**：原论文不是单一阈值规则，而是用 VIX 的**非线性 dummy 回归**生成信号，再在 S&P 500 上做**3 个月持有的非对称 buy-and-hold**。为了让你能写 `compute()`，我建议采用可复刻 operationalization：若 `^VIX > 30`（保守用 40）则分配到 `SPY`，持有 63 个交易日，或直到 VIX 回落到 20 以下。这个阈值是**实践化离散化**，不是论文唯一标准。citeturn37view0turn36news40  
**原始样本**：原论文摘要只明确写：该策略在 S&P 500 上**优于 long-only**，但我没有在现有可访问摘要里拿到作者给出的统一 CAGR/Sharpe 数字，因此记为“原始来源未在摘要中报告具体组合统计量”。citeturn37view0  
**后续复核**：Ronn 2025 的结论是把 VIX 用作**逆向指标并不违背市场效率**，条件 Sharpe 仍可为正；但 2026 年 FT 讨论也提醒，VIX 上升并不只是情绪过冲，里面也含有**对未来波动的知情交易信息**。citeturn36search2turn36news40  
**数据可行性**：完全可做：`^VIX` + `SPY`。  
**实现备注**：纯 ETF 无需期权；但最好做**分层买入/分散持有期**，避免一次性抄底。CN 版可尝试 iVX/波指代理，但本地数据可得性差。  
**文献裁决**：**可用，但只适合作为逆向过滤器，不适合独立重仓。** citeturn36search2turn36news40

**AAII 极端悲观逆向**  
**来源**：AAII Sentiment Survey 官方说明；补充研究与评论见 Fidelity 2009、SSRN 2025。citeturn7search0turn7search14turn7search7turn7search4  
**机械规则**：官方只给出“极端悲观常被当作逆向信号”，并未给唯一阈值。为了编码，我建议周频：若 **bearish > 60%** 或 **bull-bear spread < -30**，则下一交易周增配 `SPY` 20 个交易日；若连续极端则允许分批。注意：这里的 **60%** 是实践阈值，不是 AAII 的官方规则。citeturn7search0turn7search14  
**原始样本**：AAII 官方页面给出的可直接引用数字是，**bearish sentiment 历史最高值为 70.3%（2009-03-05）**，并将该调查明确表述为一种**contrarian indicator**；但官方不提供标准化回测收益表。citeturn7search14turn7search0  
**后续复核**：Fidelity 2009 的评价非常有用：情绪极值**并不总是精确对应拐点**，单独拿来做交易“tricky business”；2025 的长周期回测论文则表明，AAII 情绪确实可能包含**可实施的择时信息**，但强度远没有口口相传那么简单。citeturn7search7turn7search4  
**数据可行性**：你的三件套**不够**；需要抓取 AAII 周度调查原始历史。  
**实现备注**：只做 SPY long-only 更现实；CN 对应物可以换成股吧/两融/基金情绪代理，但不是同一指标。  
**文献裁决**：**有信息量，但噪声很大；更适合做仓位加减分器。** citeturn7search7turn7search4

**CNN Fear and Greed 极度恐惧买入**  
**来源**：CNN Business 指数框架；学术检验见 Farrell，2025。citeturn7search16turn7search20turn7search22  
**机械规则**：可编码版很简单：若 Fear & Greed 指数 **≤25**，买入 `SPY` 并持有 20 个交易日；若 **≥75**，减仓或不新开多头。更稳妥的版本是把它只用作**股票仓位因子**，例如 0/50/100 三档。citeturn7search16turn7search20  
**原始样本**：CNN 的“原始来源”是一个**情绪温度计**，不是策略论文，因此**没有原始 in-sample CAGR/Sharpe 表**。它本质上是由七个市场情绪分量构成的复合指数。citeturn7search16turn7search20  
**后续复核**：Farrell 2025 用 2011–2024 数据发现，该指数在 **2011–2020** 对 S&P 500、Nasdaq、Russell 3000 的回报有 Granger 因果关系；在 **2021–2024** 仍对 S&P 500 等有预测力，但**关系明显转弱**。这已经是你要求的“若衰减超过 30% 要点名”——这里应明确写**边际显著衰减**。citeturn7search22turn7search10  
**数据可行性**：不能靠 FRED/yfinance 原生拿到，需要手工抓取 CNN 指数历史或第三方镜像。  
**实现备注**：历史长度只从 2011 左右开始，样本短；CN 没有官方同构指标。  
**文献裁决**：**可作为现代情绪代理，但样本短、近年已明显弱化。** citeturn7search22

## 宏观状态切换

**十年减二年收益率曲线倒挂与再陡峭化**  
**来源**：Estrella 体系的收益率曲线预测文献；当代综合可见纽约联储 FAQ、AQR 2019 与 Hasse 2022。citeturn11search5turn11search2turn11search9  
**机械规则**：最实用的月频版本：读取 `T10Y2Y`。若利差首次跌到 **≤0**，将股票仓位降到防御档；只有当利差重新回到 **>0** 且较谷底回升至少 **50bp** 时，才恢复风险资产。这样做是因为历史上**re-steepening 往往发生在衰退临近阶段**。citeturn11search5turn11news42  
**原始样本**：这类文献的原始结果主要是**衰退预测力**，不是策略收益。纽约联储 FAQ 明确说，收益率曲线斜率是未来真实活动的**可靠领先指标**；AQR 2019 也强调倒挂通常先于衰退，但不保证短期股市马上下跌。citeturn11search5turn11search2  
**后续复核**：Hasse 2022 仍发现收益率利差对衰退具有稳健信号；但 2024 年市场评论普遍承认，这次倒挂持续异常之久，说明“**倒挂≠立刻卖股**”，更适合做**宏观降风险开关**而非日内择时。citeturn11search9turn11news41turn11news42  
**数据可行性**：FRED 即可，`T10Y2Y` 或 `DGS10-DGS2`。  
**实现备注**：不要求做空；适合控制股票/信用/小盘暴露。CN 版可改用**国债 10Y-1Y 或信用利差**，但中国曲线的政策扭曲更大。  
**文献裁决**：**强宏观滤波器；不建议单独当买卖点。** citeturn11search5turn11search9

**高收益 OAS 阈值防御**  
**来源**：Nozawa 2016、LSEG FTSE Russell 2023，以及 FRED 的 ICE BofA HY OAS。citeturn9search11turn11search1turn11search0  
**机械规则**：论文更多证明“高信用利差会改变未来回报”，而不是给唯一阈值。为了让你可编码，我建议月频：若 `BAMLH0A0HYM2 > 6.0`（即 **600bp**），降低股票和高收益债暴露，转向国债/现金；回到 **<5.0** 后逐步恢复。600bp 是实践里常见的“distress line”离散化。citeturn11search0turn11search4  
**原始样本**：Nozawa 的核心结果是：**更高的高收益信用利差预测更低的高收益发行人股票长期回报**；LSEG 2023 也写明，起始高收益利差与未来高收益及股票回报之间有明确预测关系。原始论文不是策略回测，所以“原文未报告单一阈值策略 CAGR/Sharpe”。citeturn9search11turn11search1  
**后续复核**：近年的机构研究仍把高收益利差视为风险资产估值与未来收益的重要状态变量；但阈值触发更适合做**defensive overlay**，不适合做二元 all-in/all-out。citeturn11search1turn11search4  
**数据可行性**：FRED 直接有 `BAMLH0A0HYM2`。  
**实现备注**：实现最简单的是用 `HYG/JNK` 与 `IEF/TLT/BIL` 切换。CN 版可尝试用**中债信用利差**代理，但免费、稳定、长历史的数据不如美国成熟。  
**文献裁决**：**适合做风险开关；阈值是 operationalization，不是学术常数。** citeturn11search1turn9search11

**LEI 走弱触发降风险**  
**来源**：Conference Board LEI 官方描述；现实争议点见 PGIM 2024 与 Reuters 2024。citeturn9search0turn9search9turn9search3turn9news40  
**机械规则**：原始来源只说明 LEI 用于识别周期峰谷，并未给交易阈值。为方便回测，我建议：若 LEI 的**6 个月年化变化率**连续 3 个月 < 0，则股票仓位降到 0–50%；连续 2 个月重新 >0 时恢复。若你只能用免费源，可用 FRED/OECD 的领先指标做代理，但那不是 Conference Board 正版 LEI。citeturn9search0turn9search9  
**原始样本**：Conference Board 的原始叙述是“LEI 旨在**signal peaks and troughs**”，不提供策略收益表。citeturn9search0turn9search9  
**后续复核**：这里必须明确写衰减与失真。PGIM 2024 说 LEI 与倒挂都长期指向衰退，但这轮美国经济表现持续强于信号；Reuters 2024 更直接报道 Conference Board 已**放弃**其此前基于 LEI 的衰退判断。也就是说，近轮 OOS 明显比历史口碑弱。citeturn9search3turn9news40  
**数据可行性**：**严格版不行**，Conference Board 正版 LEI 不在 FRED 免费直供；免费近似可用 OECD `USSLIND`。  
**实现备注**：我建议只把它作为**组合层第二确认**，不要单独一票否决。CN 版可以用中国国家统计局 PMIs、新订单与社融等拼接 proxy。  
**文献裁决**：**已显著退化为“有用但不可靠”的宏观滤波器。** citeturn9news40turn9search3

**美元六个月变化率驱动 EM 倾斜**  
**来源**：IMF 2015 与 BIS 2024。citeturn10search6turn10search3  
**机械规则**：月频读取 DXY 或其代表 ETF。若美元过去 **6 个月变化率 > 0**，则减配 `EEM`、增配 `SPY`/DM；若 **<0**，则提高 EM 权重。你也可以把它做成`EM_weight = base + k * (-DXY_6m_zscore)`。citeturn10search6turn10search3  
**原始样本**：IMF 文献的原始结果并非投资回测，而是写道美元升值/贬值周期通常会**削弱/放大**新兴市场增长；BIS 2024 直接写“美元强弱是本币债券与股票流入的关键驱动因素”。citeturn10search6turn10search3  
**后续复核**：BIS 的样本说明这种美元—EM 流量关系在后危机时段尤其重要，但强度会随制度与资本流向环境变化。换言之，它更像**贝塔倾斜信号**，不是 alpha 圣杯。citeturn10search3  
**数据可行性**：yfinance 可用 `UUP` 或 `DX-Y.NYB`；EM 用 `EEM/VWO`。  
**实现备注**：完全 ETF 化，无需杠杆。CN 版可做“美元走弱时增配离岸中资/港股互联网与 EM，美元走强时回到本币利率资产”。  
**文献裁决**：**适合作为全球配置 tilt，不适合作单独择时。** citeturn10search6turn10search3

**金铜比率风险开关**  
**来源**：DoubleLine 2019 与 Parnes 2024。citeturn8search3turn8search9  
**机械规则**：定义 `GoldCopper = Gold / Copper` 或反过来 `CopperGold = Copper / Gold`；月频用 252 日 z-score。若 `GoldCopper_z > +1`，视为**偏防御**，减配权益/EM、增配国债；若 `< -1`，转向风险资产。也可以用连续权重而非二元阈值。citeturn8search3turn8search12  
**原始样本**：DoubleLine 白皮书写得很清楚：铜/金比率可作为 **10Y 美债收益率方向的领先指标**；它本质上在“工业景气 vs 避险需求”之间取相对价格信息。原文并未给出标准化投资组合 CAGR/Sharpe。citeturn8search3  
**后续复核**：Parnes 2024 明确提醒：这个指标在全球宏观震荡阶段会出现**不少 false signals**；Reuters 2025 也指出近年该比率所叙述的宏观故事已经更复杂，不再是单线条 risk-on/off。citeturn8search9turn8news38  
**数据可行性**：yfinance 可用 `GC=F`（金）与 `HG=F`（铜）近似。  
**实现备注**：不需要做空；更适合做宏观 overlay。CN 版可以用沪铜/黄金主力或相应 ETF/期货连续合约。  
**文献裁决**：**可做次级确认指标，单独使用容易误判。** citeturn8search9turn8news38

## 日历与季节性

**月末效应 Turn of the Month**  
**来源**：Lakonishok & Smidt，1988《Are Seasonal Anomalies Real?》。citeturn39view0turn41view1  
**机械规则**：最经典可编码版并不是“整个前后半月”，而是只抓作者发现最强的窗口：**月末最后 1 个交易日到下月前 3 个交易日**。实盘上可写为：在月末倒数第二个交易日收盘后建仓 `SPY`，持有到新月第 3 个交易日收盘离场。citeturn41view1  
**原始样本**：作者用 **90 年 DJIA 日数据**，并写道围绕月末的四天累计收益为 **0.473%**，而一个普通四天窗口平均仅 **0.0612%**，差异在 **0.1% 显著性水平**下成立；围绕月末时段的正收益概率**超过 56%**，普通日则**低于 52%**。citeturn39view0turn41view1  
**后续复核**：我在本轮检索中没有拿到一篇同等权威、且网页可直接引用的现代独立再检验 PDF，因此这里必须老实写：**现代 OOS 复核在本报告中不完整**。从实践角度，它依然常被用作执行层“何时下月度再平衡”的微观日历偏置。  
**数据可行性**：完全可用 yfinance 日频。  
**实现备注**：这种策略胜在**不吃趋势判断**、交易次数低；但优势很薄，成本/税拖累会非常关键。CN 版对 A 股指数 ETF 也可直接测试。  
**文献裁决**：**经典微弱日历效应；如果你费率高，就不要做。** citeturn41view1

**Sell in May 与 Halloween 效应**  
**来源**：Bouman & Jacobsen，2002。citeturn2search4  
**机械规则**：半年度切换最直接：**11 月初到 4 月底持有 SPY**；**5 月初到 10 月底**持有 `BIL/SHY`，或对冲/空仓。你如果要忠于论文，就先做“股 vs 现金”；若下游你要自己统一比较，再决定防御腿用什么。  
**原始样本**：原论文最著名的结论是，这个“Halloween indicator”在所检验的国家里极为普遍：**36/37 个市场**的 11–4 回报都高于 5–10。可获取摘要没有统一 Sharpe/MaxDD 表。citeturn2search4  
**后续复核**：后续文献对它分歧很大：一部分发现该效应在多个国际市场、长样本中仍然可见；另一部分认为加上数据挖掘与交易执行约束后，优势明显变弱，甚至更像“季节性风险溢价”而不是白吃午餐。citeturn2search0turn2search4  
**数据可行性**：完全可用 yfinance。  
**实现备注**：交易频率极低，税负与成本都友好。CN 版可以直接做 `510300`/`159915` 的“11–4 持有，5–10 防御”。  
**文献裁决**：**有历史证据，但地区性与时代性很强；优先当低频季节性 overlay。** citeturn2search4turn2search0

**Pre-FOMC 漂移**  
**来源**：Lucca & Moench，2015。citeturn43view0  
**机械规则**：最忠实版需要**分钟级数据**：持有 S&P 500 指数自 FOMC 公告前 **24 小时**起，到声明发布前结束。若你只用日线，可近似成“**公告日前一收盘买入，公告日收盘卖出**”，但这会混入公告后几个小时的噪音。只做**scheduled FOMC**，不要把 emergency meetings 混进去。citeturn43view0  
**原始样本**：作者用 1980–2011 样本写到：自 **1994 年**以来，大约 **80%** 的年度实现超额股票收益都发生在 pre-FOMC 窗口；单独只持有公告前 24 小时的交易策略，年化 Sharpe **高于 1.1**。在 1980–1993 样本中，pre-FOMC 平均回报约 **20bp**。citeturn43view0  
**后续复核**：这类效应已明显衰减。后续研究把样本延到 2019 左右，普遍认为原始漂移在 QE/前瞻指引时代后**弱化甚至阶段性消失**。就你的规则库而言，必须把它当成“**可检验、但很可能已被套利的微结构效应**”。citeturn43view0turn2search10  
**数据可行性**：若只用 yfinance 日线，只能做近似版；严谨版需要分钟数据与**FOMC日历表**。  
**实现备注**：极低持仓时间、极高对时点敏感；美国 taxable account 下收益性质几乎全是短期。CN 无直接同构物，可尝试“央行重大例会前漂移”。  
**文献裁决**：**曾经极强，但明显衰减；不宜当核心策略。** citeturn43view0turn2search10

**Santa Claus Rally**  
**来源**：概念源于 Yale Hirsch；可编码的现代学术定义与检验见 Washer & Nippani，2016，以及 2023 更新。citeturn42search0turn42search1  
**机械规则**：严格按学界常用定义：买入窗口就是**12 月最后 5 个交易日 + 次年 1 月前 2 个交易日**。策略极短，最自然的实现载体是 `SPY`。你也可以把它设为一个“年末最后一周临时加仓”的信号，而不是独立账户。citeturn42search0turn42search5  
**原始样本**：Washer & Nippani 2016 的摘要明示，该窗口在 **1926–2014** 的美国样本中平均回报更高，而且**小盘股更强**。市场业界口径则常引用“该 7 天窗口自 1950 年以来 S&P 500 平均涨幅约 **1.3%**，正收益概率约 **79%**”。citeturn42search0turn42search5  
**后续复核**：2023 的美国再检验把样本设为 **2000–2021**，结论正好是：Santa Claus Rally **并不普遍存在**。这已经构成你要求中的衰减提示。citeturn42search1  
**数据可行性**：yfinance 直接可做。  
**实现备注**：交易成本低，但效应窗口极短。CN 版可测试“跨年最后五日+元旦后两日”的沪深 300 ETF。  
**文献裁决**：**存在过，但近二十多年美国样本明显不稳定。** citeturn42search0turn42search1

## 配置与回撤控制

**六四股债配置**  
**来源**：并无单一“发明人”；现代规范化历史回顾可用 CFA Institute 2025。citeturn45view0  
**机械规则**：最朴素版本：`60% VTI/SPY + 40% IEF/AGG/TLT`，月度或季度再平衡。若你追求更接近机构定义，固定久期的国债比总债指数更可控。citeturn45view0  
**原始样本**：CFA 2025 用 DMS 数据库研究 **122 年**历史，写道所考察市场中 60/40 的长期实际收益都为正，范围从日本的 **2.95%/年** 到澳大利亚的 **4.97%/年**；美国与澳大利亚自 1900 年以来的真实年化回报都接近 **5%**。citeturn45view0  
**后续复核**：该报告也明确指出 2022 年股债同跌使 60/40 遭遇挑战，但其长期多国历史依旧支持“分散化有效”；同时它提醒股债相关性**并不总是负的**。citeturn45view0  
**数据可行性**：完全可用 yfinance；若防御腿想更贴“国债”，可用 `IEF/TLT`，若想更贴“综合债”，可用 `AGG/BND`。  
**实现备注**：最低成本、最低实现复杂度；CN 版可用 `510300 + 511010/511260` 做近似。  
**文献裁决**：**不是 alpha 策略，而是强 baseline；任何主动策略都该先与它比较。** citeturn45view0

**风险平价 Risk Parity**  
**来源**：Qian 的风险平价框架、PanAgora《Risk Parity Portfolios》、AQR《Understanding Risk Parity》。citeturn46search3turn46search6  
**机械规则**：最标准的 `compute()`：设资产集合为 `SPY, IEF/TLT, GLD, DBC` 或 `SPY, TLT, GLD, DBC, VNQ`；用过去 36 个月的协方差矩阵求**Equal Risk Contribution** 权重；若允许杠杆，再把组合年化波动缩放到 8%–12%。无杠杆版本则只是“低风险平权”。月度再平衡即可。citeturn46search6turn46search13  
**原始样本**：AQR 白皮书对风险平价的概括是：它寻求**更高且更稳定的回报**；PanAgora 把它定义为“比传统资本配置更有效”的 beta 组合。当前可公开网页摘要没有统一的原始单一回测 CAGR 表，因此记为“规范来源未在开放摘要中统一给出”。citeturn46search6turn46search3  
**后续复核**：后续机构文献普遍承认风险平价在**股票主导风险**的传统组合面前有结构优势，但也提醒它对**债券牛市、相关性变化、杠杆融资条件**高度敏感。citeturn46search6turn46search3  
**数据可行性**：完全可用 yfinance，FRED 补充现金和宏观变量。  
**实现备注**：若无融资/期货，很多“真风险平价”会被迫退化；因此你回测时最好分成**unlevered ERC** 和 **target-vol ERC** 两条。CN 版受制于长债、商品 ETF 与融资工具可得性。  
**文献裁决**：**组合工程上很强，但不是免费午餐；杠杆与相关性是成败之匙。** citeturn46search6turn46search3

**Bridgewater All Weather**  
**来源**：Bridgewater《The All Weather Story》及 2009 信息包。citeturn46search2turn47view0  
**机械规则**：必须先说实话：**Bridgewater 并未完整公开可逐条复现的真实权重与交易实现**。因此对零售最合理的是使用“**公开概念 + 可交易代理**”的版本：常见代理权重大致为 `30% 股票 + 40% 长债 + 15% 中债 + 7.5% 黄金 + 7.5% 商品`，季度再平衡；更“正统”的实现应按**增长上行/下行、通胀上行/下行**四象限分配风险，而不是死记权重。citeturn47view0  
**原始样本**：Bridgewater 2009 材料写得很明确：自 **1996** 年以来 All Weather 的年化回报约 **8.4%**，波动约 **11%**，Sharpe 约 **0.43**，且为**gross of fees**；材料同时指出常规 60/40 组合在风险层面与股市相关性约 **0.96**、权益贡献约 **90%** 风险。citeturn47view0  
**后续复核**：独立后验研究整体认为 All Weather 的核心思想——**按宏观环境平衡风险**——是稳健的，但 2022 之后“债券并不总能对冲股票”的现实，让静态民间版 All Weather 需要更谨慎。citeturn45view0turn47view0  
**数据可行性**：yfinance 足够做零售代理版。  
**实现备注**：真正完整版常需**杠杆/期货/久期管理**；零售 ETF 版可以不加杠杆，但会更保守。CN 版在商品、通胀挂钩债与长期利率工具上都有替代品不足的问题。  
**文献裁决**：**理念非常强，公开版适合做“思想框架”；精确复刻不现实。** citeturn47view0turn46search2

**Harry Browne Permanent Portfolio**  
**来源**：Harry Browne 在《Fail-Safe Investing》中提出的 Permanent Portfolio。citeturn46search0turn46search4  
**机械规则**：可直接写死：`25% 股票 + 25% 长期国债 + 25% 现金/T-bills + 25% 黄金`；年复一年**年度再平衡**。美股代理可用 `SPY/VTI + TLT + BIL/SHY + GLD`。citeturn46search0turn46search4  
**原始样本**：Browne 的核心承诺是“在繁荣、衰退、通胀、通缩四种环境中总有一块资产会表现好”；但当前可公开检索的原始来源**没有给出规范化 CAGR/Sharpe/MaxDD 表**，所以这里必须老老实实写“原始来源未报告统一绩效表”。citeturn46search0  
**后续复核**：后续媒体与研究经常把它作为 60/40 的替代方案重新测试；至少一项 2014 的跨国学术研究被后续报道引用，显示不同国家 Permanent Portfolio 的长期行为值得研究，而 2020s 的市场环境让这一组合重新受关注。只是这部分文献公开、可机读的原始出处在本轮检索里不够完整。citeturn46search1turn46news41  
**数据可行性**：完全可用 yfinance。  
**实现备注**：无须做空、无须复杂估计，适合作为**低维护、低行为错误**账户。CN 版可近似成 `510300 + 长债ETF + 货基/短债 + 黄金ETF(如 518880)`。  
**文献裁决**：**作为“简单而抗冲击”的永久底仓有吸引力，但不是公开文献最充分的一类。** citeturn46search0turn46news41

## 附录

**Appendix A — 数据源 cookbook**

下面只列**你本地 refresh CLI 最需要接线的最便宜免费源**。美股/ETF/Futures 首选 yfinance；宏观首选 FRED；中国本地价格层优先 AkShare。AkShare 的接口命名会随版本微调，所以我只列确认度较高、且最常用的函数名；执行前请以你本地版本自检。Conference Board LEI、AAII、CNN Fear & Greed、美国点位级财报 surprise 这些不都能由三件套原生解决。citeturn11search0turn45view0turn7search0turn7search20

S&P 500 / SPY：`SPY`（yfinance）；  
美国广义股票：`VTI`（yfinance）；  
海外发达股票：`VEU` 或 `EFA`（yfinance）；  
新兴市场股票：`EEM` / `VWO`（yfinance）；  
美国中期/长期国债：`IEF` / `TLT`（yfinance）；  
综合债：`AGG` / `BND`（yfinance）；  
现金/T-bill 代理：`BIL`（yfinance），或 `DTB3`（FRED 3-Month Treasury Bill）；  
REIT：`VNQ`（yfinance）；  
商品篮子：`DBC` 或 `GSG`（yfinance）；  
黄金：`GLD`（ETF）或 `GC=F`（futures，yfinance）；  
铜：`HG=F`（yfinance）；  
VIX：`^VIX`（yfinance）；  
美元指数代理：`UUP` 或 `DX-Y.NYB`（yfinance）；  
10Y–2Y 利差：`T10Y2Y`（FRED），也可用 `DGS10`、`DGS2` 自己相减；  
高收益 OAS：`BAMLH0A0HYM2`（FRED）；  
美国 3M T-bill 作为 hurdle：`DTB3`（FRED）或 `BIL`（yfinance）；  
LEI 正版：Conference Board（非三件套原生免费）；免费近似：FRED/OECD 的 `USSLIND`；  
FOMC 日期：Fed 官方会议日历手工下载，或你本地维护 csv；  
AAII 情绪历史：AAII 官方页面/手工抓取（非三件套原生）；  
CNN Fear & Greed：CNN 页面或第三方镜像抓取（非三件套原生）；  
美股财报 surprise / SUE：I/B/E/S、Compustat、FactSet、Refinitiv（付费）；  
A 股指数：AkShare 常用 `index_zh_a_hist`；  
A 股 ETF：AkShare 常用 `fund_etf_hist_em`；  
沪深300 本地化：指数 `000300` 用 `index_zh_a_hist`，ETF 可用 `510300` 走 `fund_etf_hist_em`；  
中国黄金 ETF（本地化 All Weather / Permanent）：如 `518880`，走 `fund_etf_hist_em`；  
中国国债 ETF（本地化股债/永久组合）：如 `511010`，走 `fund_etf_hist_em`。  

**Appendix B — 阅读清单 ranked**

Moskowitz, Ooi, Pedersen《Time Series Momentum》：多资产趋势策略最该读的原型文献。citeturn27view0  
Jegadeesh & Titman《Returns to Buying Winners and Selling Losers》：横截面动量的始祖论文之一。citeturn31view0  
Faber《A Quantitative Approach to Tactical Asset Allocation》：面向零售最可执行的趋势过滤白皮书。citeturn17view0  
Antonacci《Risk Premia Harvesting Through Dual Momentum》：把 absolute + relative momentum 组合成低复杂度战术配置。citeturn23view0  
Lucca & Moench《The Pre-FOMC Announcement Drift》：日历/公告效应里最经典、也最值得你自己重跑 OOS 的一篇。citeturn43view0  
Lakonishok & Smidt《Are Seasonal Anomalies Real?》：月末、节前、年末效应的大底稿。citeturn39view0turn41view1  
Bouman & Jacobsen《The Halloween Indicator》：Sell in May 的规范来源。citeturn2search4  
Bernard & Thomas 1989/1990 + Fink 2021 综述：PEAD 的原型与现代性讨论要一起读。citeturn35search13turn35search2turn35search0  
Bridgewater《The All Weather Story》：即便你不完全复刻，也值得用来建立“按宏观环境平衡风险”的框架。citeturn46search2turn47view0  
CFA 2025《The Performance of the 60/40 Portfolio》：任何主动策略的 baseline 与长期资产配置常识。citeturn45view0

**Appendix C — 考虑过但剔除的策略**

Connors RSI(2)：实践圈很流行，但我在本轮检索里没有拿到足够强的**原始来源 + 独立 OOS 学术复核**组合，不适合放进“高置信度”主列表。  
Put/Call Ratio 极端逆向：有实践价值，但阈值高度依赖市场结构，且可复制的高质量原始文献链不如 VIX/AAII 清晰。citeturn5search4turn6search18  
Dogs of the Dow：规则简单，但现代学术关注和可解释性都逊于 60/40、风险平价、双动量等更主流框架。citeturn13search2turn13search16  
Magic Formula：名气很大，但若你要忠实回测，必须解决**点时财报、会计口径、可投资股票池与存活偏差**，这已经超出三件套的“免费零售可复现”边界。  
Golden Butterfly：民间配置框架实用，但主文献与机构原始来源的规范性弱于 Permanent / All Weather / Risk Parity。  

**局限与开放问题**

这份提案已经满足“可写 `compute()`、不代你做统一回测”的目标，但仍有三类限制需要你在下游回测时自己补齐。第一，**Carhart UMD、短反转、长反转、PEAD** 这类股票横截面策略，若你不用 CRSP/Compustat/Ken French/事件数据库，而只用 yfinance 当前成分股，会有明显偏差。第二，**AAII、CNN Fear & Greed、Conference Board LEI** 都存在“原始信号可得性不如价格/宏观序列干净”的问题；我已经在卡片里明确区分了“原始来源未报告”与“我为可编码性做的 operationalization”。第三，**All Weather 与 VIX>30/40** 这类实践策略，规则层和学术原文并非一一同构；更准确地说，它们是“有论文支持的可实施离散化版本”，适合进入你的候选库，但必须靠你下游回测做最终筛选。