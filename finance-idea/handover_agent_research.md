# finance-idea · Agent 调研 + quant_by_leancli 接手文档

> 最后更新: 2026-05-28 · 接手人 10 分钟内能上手为目标
>
> 跟 [handover.md](handover.md) 是不同主题：那篇是 validation50 / dashboard 项目；本篇是**第三方 agent 仓库调研**和 **quant_by_leancli 跑模拟的阻塞分析**。

---

## 0. 路径约定（跨平台）

本文档曾在 Windows 上写就，现仓库落在 macOS。同一个 `finance-idea/` 工作区两个平台的根路径：

| 平台 | `finance-idea/` 根路径 |
|---|---|
| **macOS（本机）** | `/Users/bytedance/Desktop/stock/finance-idea` |
| **Windows（原机）** | `d:\ai_play\memory-semiconductor-investing\finance-idea` |

约定：

- 文档内的 markdown 链接一律用**相对 `finance-idea/` 的相对路径**（如 [quant_by_leancli/](quant_by_leancli/)、[other-finance-package/](other-finance-package/)），两个平台都能点开。
- `quant_by_leancli/` 在**本机位于 `finance-idea/` 内部**（独立 git repo），不是父级 sibling——早期版本里的 `../quant_by_leancli/` 链接已修正。
- 需要敲命令时（如 §9），bash / PowerShell 两个版本都给出，把上表的根路径填进 `cd` 即可。

---

## 1. 这次 session 在做什么

两件事，互相独立：

1. **金融 Agent 设计调研**：拉了 16 个第三方"炒股 / 投研 / 量化 Agent"仓库到 [other-finance-package/](other-finance-package/)，做了 design pattern 横向对比，回答"我自己的 quant_by_leancli 接下来可以怎么 LLM 化"。
2. **quant_by_leancli 跑模拟的可行性诊断**：用户问"现在能跑模拟吗"，答案是**不能开箱跑**，缺 Docker / LEAN CLI / venv / 数据，已经列出 3 条路径。

---

## 2. 当前状态

| 模块 | 状态 | 说明 |
|---|---|---|
| 16 个第三方仓库克隆 | ✅ 完成 | 全部 shallow clone 在 [other-finance-package/](other-finance-package/) |
| [other-finance-package/financial_trading_agent_repos.md](other-finance-package/financial_trading_agent_repos.md) | ✅ 已存在（用户原作） | 16 个仓库的选型清单和推荐理由 |
| [CLAUDE.md](CLAUDE.md) | ✅ 本次新写 | 含 16 个仓库的一键拉取 PowerShell + Bash 脚本（幂等） |
| Agent 设计 design pattern 调研 | ✅ 完成 | 4 流派 §4；**7 维度横向对比已落地为自洽表格 §4.1**，记忆专题 §4.2 |
| IBKR 实盘集成调研 | ✅ 完成 | 结论：**只有 FinceptTerminal 一家**有真 IBKR 下单 |
| 对 quant_by_leancli 的设计建议 | ✅ 完成 | §6 七条(A–G) + **§6.1 完整论证（已核对本机真实文件，自洽）** |
| quant_by_leancli 跑模拟 | ❌ 阻塞 | 缺 Docker、LEAN CLI、venv、数据；3 条路径见 §7 |

---

## 3. 第三方仓库清单（速查）

| # | 仓库 | 路径 | 类型 |
|---|---|---|---|
| 1 | TradingAgents | [other-finance-package/TradingAgents/](other-finance-package/TradingAgents/) | LangGraph debate-driven 多 agent |
| 2 | ai-hedge-fund | [other-finance-package/ai-hedge-fund/](other-finance-package/ai-hedge-fund/) | 16 投资大师 persona |
| 3 | AI-Trader | [other-finance-package/AI-Trader/](other-finance-package/AI-Trader/) | FastAPI 交易平台 |
| 4 | Vibe-Trading | [other-finance-package/Vibe-Trading/](other-finance-package/Vibe-Trading/) | ReAct + SKILL.md 工作台 |
| 5 | FinRobot | [other-finance-package/FinRobot/](other-finance-package/FinRobot/) | AutoGen Group Chat + Leader |
| 6 | RD-Agent | [other-finance-package/RD-Agent/](other-finance-package/RD-Agent/) | Hypothesis-code-run-feedback loop |
| 7 | qlib | [other-finance-package/qlib/](other-finance-package/qlib/) | AI 量化平台（weight-centric）|
| 8 | FinRL-Trading | [other-finance-package/FinRL-Trading/](other-finance-package/FinRL-Trading/) | FinRL-X 工业级执行 |
| 9 | AutoHedge | [other-finance-package/AutoHedge/](other-finance-package/AutoHedge/) | Swarms + Jupiter Solana 实盘 |
| 10 | FinGPT | [other-finance-package/FinGPT/](other-finance-package/FinGPT/) | 金融 LLM 微调底座 |
| 11 | FinceptTerminal | [other-finance-package/FinceptTerminal/](other-finance-package/FinceptTerminal/) | C++ Qt 终端，**唯一有 IBKR 实盘** |
| 12 | FinRL | [other-finance-package/FinRL/](other-finance-package/FinRL/) | 经典 DRL trading |
| 13 | AgenticTrading | [other-finance-package/AgenticTrading/](other-finance-package/AgenticTrading/) | DAG orchestrator + Memory agent |
| 14 | stockbench | [other-finance-package/stockbench/](other-finance-package/stockbench/) | LLM 单 agent 连续决策 benchmark |
| 15 | live-trade-bench | [other-finance-package/live-trade-bench/](other-finance-package/live-trade-bench/) | 实时市场 agent 评测 |
| 16 | Stockagent | [other-finance-package/Stockagent/](other-finance-package/Stockagent/) | 多 agent 模拟市场（合成数据）|

**重要**：父级 `.gitignore` 排除 `other-finance-package/*/`，ripgrep/Grep 工具会跳过这些目录。搜索时必须显式加 `--no-ignore`：

```bash
rg --no-ignore -i "your-pattern" other-finance-package/
```

详细分类和推荐阅读顺序见 [CLAUDE.md](CLAUDE.md) 的"设计调研结论"部分 + [other-finance-package/financial_trading_agent_repos.md](other-finance-package/financial_trading_agent_repos.md) 原始选型表。

---

## 4. Agent 设计 4 大流派（调研结论）

| 流派 | 代表仓库 | 编排框架 | 核心抽象 |
|---|---|---|---|
| **机构团队模拟（debate）** | TradingAgents | LangGraph StateGraph | 角色分工 + 多阶段辩论（Bull/Bear → 3-way Risk → PM）|
| **Persona 并发聚合** | ai-hedge-fund | LangGraph StateGraph | 16 大师 parallel → confidence-weighted aggregate |
| **量化研发闭环** | RD-Agent + Qlib + AgenticTrading | 自研 RDLoop / DAG | Hypothesis → Code → Run → Feedback + CoSTEER 知识库 |
| **Skill / ReAct 工作台** | Vibe-Trading / FinceptTerminal | 自研 ReAct loop / dual-path | skill = SKILL.md + signal_engine.py，按 goal 动态加载 |

### 4.1 横向维度对比（7 维度，已落地为自洽内容）

> 下面把 8 个代表仓库按 7 个设计维度拆开对比。每格尽量给关键文件路径，接手人无需再翻仓库。
> 选这 8 个是因为它们覆盖了 §4 的 4 大流派；其余 8 个仓库（AI-Trader / FinRobot / FinRL / FinRL-Trading / AutoHedge / FinGPT / live-trade-bench / Stockagent）在设计模式上是这 8 个的变体或子集。

**表 A — 角色拆分 / Prompt / 输出 Schema**

| 仓库 | 角色拆分 | Prompt 组织 | 输出 Schema |
|---|---|---|---|
| TradingAgents | Bull/Bear 研究员 → 投资辩论(≥2 轮) → Trader → 风险辩论(保守/激进/中性) → PM，5 层；外加 4 类分析师(行情/社媒/新闻/基本面) | 内联模板写死在各 agent 函数里，把 Pydantic schema 说明追加进 prompt（`tradingagents/agents/schemas.py`）| Pydantic：`PortfolioRating`(Buy..Sell)、`TraderProposal`(action+entry+stop_loss+sizing)、`PortfolioDecision` |
| ai-hedge-fund | 16 投资大师 persona + ~6 分析师(共 19) **并行** → Risk Manager → PM（`src/utils/analysts.py`）| 内联 system+user 字符串，逐 agent 写在函数里 | Pydantic：每 persona `{signal: bullish/bearish/neutral, confidence:0-100, reasoning}`；PM 输出 `PortfolioDecision`(action buy/sell/short/cover/hold, qty, conf) |
| RD-Agent | RDLoop = Hypothesis → Code → Run → Feedback，Factor / Model 双路并行（`rdagent/components/workflow/rd_loop.py`）| **YAML 模板**(system+user)，`prompts.yaml` + Prompts 单例 | 类型化 `Hypothesis`(hypothesis/reason/concise_*) + `CoSTEERSingleFeedback`(execution/return_checking/code/final_decision) |
| Qlib | weight-centric 管道：Alpha 特征 → 模型训练 → 信号 → 组合权重 → 回测，**无假设阶段** | 不适用（无 LLM），用 YAML 配置 | `pred`(SignalRecord) + `PortAnaRecord`(positions/pnl/sharpe)（`qlib/workflow/record_temp.py`）|
| AgenticTrading | DAG 编排：LLM `DAGPlanner` 把自然语言策略拆成 `TaskNode` DAG，调度 Data/Alpha/Execution/Risk/Memory agent pool（`FinAgents/orchestrator/core/dag_planner.py`）| NaturalLanguageProcessor(LLM) → DAG，prompt 在 llm_integration.py（部分开源）| `TaskNode.result` + Signal/Portfolio/Order 对象 |
| Vibe-Trading | 多 agent swarm(29 队) + ReAct，75 个 skill 经 MCP 调用；每个 skill 一份 `SKILL.md` | prompt 嵌在各 `SKILL.md`(`agent/src/skills/`) | 信号→持仓（未强类型）；`TradeRecord`/`Position` dataclass |
| FinceptTerminal | 单 agent C++/Qt6 终端，37 个 persona(多家 LLM 封装) | 编译进二进制 / UI 配置（仓库里没有模板文件）| UI 决策(buy/sell/hold+conf) → `UnifiedOrder` struct(Market/Limit/StopLoss, side, qty, conid)（`IBKRBroker.h`）|
| stockbench | 单 agent 双段 LLM：`FundamentalFilterAgent` + `DualAgentLLM`，ReAct observe→analyze→decide | `agents/prompts/` 按版本存(`single_agent_v1.txt`/`dual_agent_v2.txt`) | **Pydantic v2** `DecisionOutput`(action increase/hold/decrease/close, target_cash_amount, cash_change, reasons[], confidence 0-1)（`stockbench/core/schemas.py`）|

**表 B — 风控 / 工具数据 / 记忆 / 执行**

| 仓库 | 风控 | 工具 / 数据 | 记忆 | 执行 |
|---|---|---|---|---|
| TradingAgents | 3 persona 风险辩论(保守/激进/中性)；无 VaR/仓位上限 | yfinance + Alpha Vantage：价格/基本面/新闻/内部人/Reddit·StockTwits 情绪 | `TradingMemoryLog`(`agents/utils/memory.py`)：**append-only markdown**，`get_past_context(ticker, n_same=5, n_cross=3)`，按时间取，**无 embedding** | 仅信号(Buy/Sell/...)，无券商 |
| ai-hedge-fund | 专职 `risk_management_agent`：波动率调仓位上限 + 相关性矩阵 + 组合 VaR 近似，PM 按 max_shares 约束 | FinancialDatasets.ai 单一 API（价格/指标/line items/市值/新闻/内部人）| **无**（每次 run 无状态）| 仅回测(`BacktestEngine`)，无券商 |
| RD-Agent | `CoSTEERSingleFeedback.final_decision` 闸门；execution/return/code 三段校验 | Qlib Alpha158/360 + LGBModel，回测走 Qlib workflow yaml | **CoSTEER 知识库 V2**（见 §4.2，本仓最强项）| **完整回测**(Qlib TopkDropoutStrategy)，非仅信号 |
| Qlib | `TopkDropoutStrategy`(top-k + n_drop 限换手)；涨跌停 9.5% + 手续费 | Alpha158(158 因子)/Alpha360(360 因子)，LGBModel/Transformer，`qlib.backtest` | **无**（MLflow 只存元数据，不学代码+反馈）| **完整回测**(pnl/sharpe/maxDD)，含费率与价格限制 |
| AgenticTrading | `risk_agent_pool` + TaskNode.status 失败追踪 | Data pool(IEX/Binance/CoinGecko) + Alpha pool + 回测引擎 + RLPolicyEngine | **Memory Agent(A2A)**：Neo4j 图(`TradingGraphMemory`) + `IntelligentMemoryIndexer`(语义检索) + StreamProcessor（`FinAgents/memory/memory_server.py`）| 可配 完整/仅信号；DAG 执行 Data→Alpha→Execution(下单/模拟)，RL 调优 |
| Vibe-Trading | **4 个组合优化器**：`mean_variance.py`(max Sharpe, scipy SLSQP, long-only)、`risk_parity.py`(等风险贡献, Newton 迭代)、`equal_volatility.py`、`max_diversification.py`（`agent/backtest/optimizers/`）| 7 源(tushare/yfinance/okx/akshare/mootdx/ccxt/futu) | Shadow Account：从交易日志提规则→回测；单次 run 无状态 | 仅回测；实盘需外部 wrapper |
| FinceptTerminal | margin + DAY/GTC + **bracket order**(`supports_bracket_order`) + **原生 paper**(`has_native_paper`, $100k) | 100+ 连接器(Polygon/Kraken/FRED/IMF/WorldBank/AkShare...) + IBKR REST | SQLite 交易历史（仅审计），无跨会话学习 | **真实下单 + paper**：IBKR Client Portal Gateway(`localhost:5000`, REST+SSO)，place/modify/cancel_order、get_positions/orders/quotes/history（`IBKRBroker.cpp`）；另有 15 家券商 |
| stockbench | 仅仓位逻辑校验(拒绝不自洽的下单)；无全局优化器/回撤/vol-target | Polygon(价)/Finnhub(新闻)/Polygon(基本面) | 逐 symbol 仓位状态，每次 run 重置；逐步无记忆 | benchmark 模拟(市价 mock fill)；`Order` struct 含 twap_slices |

### 4.2 记忆维度专题（对 quant_by_leancli 最相关）

记忆是 §6 里"研究迭代 LLM 化"的核心，单独拎出来对比三种实现深度：

| 仓库 | 记忆载体 | 检索方式 | 学的是什么 | 工程量 |
|---|---|---|---|---|
| TradingAgents | append-only markdown 文件 | 按时间取最近 `n_same=5` 同标的 + `n_cross=3` 跨标的 | 过往"决策→结果"复盘文本 | 轻（几十行）|
| RD-Agent (CoSTEER V2) | 知识单元 = 代码(`FBWorkspace`)+反馈+embedding，存进 `UndirectedGraph`(`graph.pkl`) | **embedding 距离**(`calculate_embedding_distance_between_str_list`) 取相似成功代码+错误轨迹，注入下一轮 prompt | 可复用的代码片段 + 失败原因链 | 重（`knowledge_management.py` 千行级）|
| AgenticTrading | Neo4j 图数据库 + 语义索引器 | 语义检索 + 图查询，经 A2A 协议暴露给 orchestrator | 交易决策/执行/归因的图谱 | 最重（要起 Neo4j 服务）|

**给 quant_by_leancli 的取舍**：现有 `sp500_rotation_hypotheses.csv` 已经是 TradingAgents 那一档的"文本复盘"雏形（见 §6-A）。往上升级首选 **RD-Agent CoSTEER 风格**（embedding + faiss 即可，不必上 Neo4j），因为本仓是单人批处理、横截面 quant，不需要 AgenticTrading 那种多 agent 实时图谱的重量级方案。

---

## 5. IBKR 实盘集成调研（关键结论）

**只有 FinceptTerminal 一家**有真 IBKR 下单：

- C++ Qt 实现，596 行：[other-finance-package/FinceptTerminal/fincept-qt/src/trading/brokers/ibkr/IBKRBroker.cpp](other-finance-package/FinceptTerminal/fincept-qt/src/trading/brokers/ibkr/IBKRBroker.cpp)
- 走 IBKR Client Portal Gateway（本地 `https://localhost:5000`），REST + SSO
- 完整实现 `place_order / modify_order / cancel_order / get_orders / get_positions / get_holdings / get_funds / get_quotes / get_history`
- 支持 bracket order、margin、native paper trading

**其他 15 个**：
- FinRL 有 [other-finance-package/FinRL/finrl/meta/preprocessor/ibkrdownloader.py](other-finance-package/FinRL/finrl/meta/preprocessor/ibkrdownloader.py)，但**只是用 `ib_insync` 拉历史数据**，没下单
- AutoHedge 接的是 Solana DeFi（Jupiter），不是 IBKR
- 其余 13 个都没接实盘券商

**对 quant_by_leancli 的含义**：用户已经在 [quant_by_leancli/ibkr/](quant_by_leancli/ibkr/) 自己写了 IBKR 数据层（`ib_async` + `tws_client.py` ibapi 包装），如果将来要做实盘下单，可参考 FinceptTerminal 的 BrokerCredentials + has_native_paper 切换设计，但 Python 用 `ib_async.placeOrder()` 更直接。

---

## 6. 给 quant_by_leancli 的设计建议（按 ROI 排序）

> 本节已基于本机 [quant_by_leancli/](quant_by_leancli/) 实际代码核对，自洽，无需再查上个 session 输出。

**用户已经做对的（对应到真实文件）**：
- **factor_lab + ml_engine ≈ Qlib + RD-Agent 下半层**：[quant_by_leancli/strategy/factor_mining/factor_lab/alpha158_computer.py](quant_by_leancli/strategy/factor_mining/factor_lab/) 实现了 Qlib 原生 Alpha158（窗口 `[5,10,20,30,60]`，RSI `[6,12,24]`），`RotationFeatureBuilder` 又叠了 Alpha101 + 技术因子；[quant_by_leancli/ml_engine/](quant_by_leancli/ml_engine/) 的 `trainer.py` 注册了 LGBMRanker / XGBRanker(LambdaRank, `rank:ndcg`, NDCG@5) / TwoStageRanker / TorchRanker。已经超出 FinRL 单一 DRL 路线。
- **lean_trading_platform + lean_workspace ≈ FinRL-Trading weight-centric execution**：[quant_by_leancli/lean_trading_platform/](quant_by_leancli/lean_trading_platform/) 的 `research.py:run_lean_jobs_parallel()` + `cli.py`(workspace init / data export / backtest matrix / viewer run) 并行跑 LEAN 回测矩阵。用 LEAN 比 FinRL-X 更接近实盘。
- **ibkr/providers ≈ FinRL.ibkrdownloader 完整版（仅缺下单）**：[quant_by_leancli/ibkr/](quant_by_leancli/ibkr/) 的 `providers/fetcher.py`(IBKRDataFetcher, `ib_async`) + `providers/tws_client.py`(ibapi EClient/EWrapper) + `lean_export.py`(OHLCV→LEAN CSV/ZIP)，**只拉数据、不下单**（全仓搜不到 `placeOrder`/`place_order`）。
- **[quant_by_leancli/docs/research_registry/sp500_rotation_hypotheses.csv](quant_by_leancli/docs/research_registry/sp500_rotation_hypotheses.csv) ≈ RD-Agent QuantTrace 雏形（最大资产）**：9 列 `hypothesis_id | research_line | idea | status | tested_in | evidence_path | key_result | failure_reason | next_action`，16 条假设（3 active/needs_validation、4 rejected、5 superseded）。**纯文本，无 embedding / code_diff 列** —— 这正是 §6-A 要补的地方。

**核心判断**：不缺基础设施，**唯一明显缺口是"研究迭代的 LLM 化"**——全仓 grep `openai/anthropic/llm/gpt/claude/langchain/langgraph` **零命中**（除 CLAUDE.md 本身），决策全是确定性的(ML ranker + 技术因子)。

### 6.1 七条建议的完整论证

**A — hypothesis CSV 升级成 CoSTEER 风格 KB（⭐⭐⭐，~1 周）**
- 现状：`sp500_rotation_hypotheses.csv` 是 9 列纯文本，靠人肉读 `key_result`/`failure_reason` 找下一步。
- 借鉴：RD-Agent CoSTEER V2（§4.2）—— 知识单元 = 代码 + 反馈 + embedding，存进图/向量库，按 embedding 距离检索相似历史。
- 落地：给每条假设加 `code_diff`（实验脚本相对 baseline 的 diff）+ `embedding`（idea+key_result 文本向量），落一个 faiss 索引即可，**不必上 Neo4j**。检索函数返回 top-k 相似历史假设。
- 为什么最高优先级：成本最低（在已有 CSV 上加列 + 一个 faiss），却是 B/C 的前置——没有结构化 KB，后面的"经验注入 prompt"无从谈起。

**B — 跨实验经验注入下次假设 prompt（⭐⭐⭐，配合 A，1 周）**
- 借鉴：TradingAgents `memory.py` 的 `get_past_context(n_same=5, n_cross=3)`（§4.2）——取同主线 5 条 + 跨主线 3 条历史复盘喂给下一步。
- 落地：用 A 建好的 KB，在生成新假设时按 `research_line` 取 `n_same=5` 同主线 + `n_cross=3` 跨主线的历史 `key_result/failure_reason`，拼进 prompt 上下文。
- 为什么配合 A：B 是 A 的直接消费者；A 落地后 B 几乎是顺手的事。

**C — 半自动 hypothesis-generator agent（⭐⭐，1-2 个月）**
- 借鉴：RD-Agent RDLoop（Hypothesis → Code → Run → Feedback，`rd_loop.py`）。
- 落地：LLM 读 KB(A) + 注入经验(B) → 提新假设 → 生成实验脚本 diff → 跑 `run_lean_jobs_parallel` → 把 `key_result` 回写 CSV，形成闭环。
- 为什么不是最高：跨度 1-2 月，且依赖 A/B 先就位；先做 A/B 拿到价值再考虑闭环自动化。

**D — FeatureInput v1 schema 标准化（⭐⭐，配合 E）**
- 借鉴：stockbench `FeatureInput`/`DecisionOutput` Pydantic v2（§4.1 表 A）——观测输入强类型化（tech/news/fund/market_ctx/position_state）。
- 落地：把 factor_lab 喂给 ranker 的特征封成 Pydantic `FeatureInput`，带 `schema_version="v1"`，方便版本演进和跨实验对齐。

**E — signal_exporter 后加多优化器层（⭐⭐，短期价值高）**
- 现状：[quant_by_leancli/strategy/market_wide/signal_pipeline/signal_exporter.py](quant_by_leancli/strategy/market_wide/signal_pipeline/) 的 `SignalExporter` 把模型分数转成 `monthly_weights.json`，只有 `equal` / `score_weighted` 两种加权 + `max_weight` 上限。
- 借鉴：Vibe-Trading 4 个优化器（`mean_variance.py` / `risk_parity.py` / `equal_volatility.py` / `max_diversification.py`，`agent/backtest/optimizers/`）。
- 落地：在 score→weight 之间插一层优化器（mean-variance / risk-parity / vol-target），压回撤。
- 为什么短期价值高：当前最优策略 **XGBRanker top2_5d = +255.14% net / Sharpe 2.127 / 但回撤 37.1%**（来自 hypothesis CSV）——回撤明显偏高，优化器层能直接吃掉这块痛点。

**F — 策略目录 SKILL.md 化（⭐，可选）**
- 借鉴：Vibe-Trading 每个 skill 一份 SKILL.md，按 goal 动态加载。
- 落地：给 4 个 LEAN 项目(NBISLab / NBIS5mLab / OUPair5mLab / GoldKCSqueezeLab)各写一份 SKILL.md 描述触发条件与参数。锦上添花，不紧急。

**G — IBKR 实盘下单层（⭐，长期）**
- 现状：ibkr/ 只读数据，不下单（见上）。
- 借鉴：FinceptTerminal `IBKRBroker.cpp`（place/modify/cancel_order + bracket + `has_native_paper`，§4.1 表 B）。
- 落地：Python 用 `ib_async.placeOrder()` 直接下单比照搬 C++ 更省事；务必先 paper → live，并加 pre-trade risk gate。长期目标，回测体系稳定前不碰。

**建议优先级**：

| # | 建议 | 借鉴自 | 优先级 |
|---|---|---|---|
| A | 把 hypothesis CSV 升级成 CoSTEER 风格 KB（含 code_diff + embeddings + faiss）| RD-Agent | ⭐⭐⭐ 最高，~ 1 周 |
| B | 跨实验经验注入下次假设 prompt（n_same=5 同主线 + n_cross=3 跨主线） | TradingAgents memory.py | ⭐⭐⭐ 配合 A，1 周 |
| C | 半自动 hypothesis-generator agent（LLM 提假设 → 生成实验脚本 diff → 回写 CSV） | RD-Agent RDLoop | ⭐⭐ 1-2 个月 |
| D | FeatureInput v1 schema 标准化（Pydantic, schema_version="v1"） | StockBench | ⭐⭐ 配合 E 一起做 |
| E | 在 signal_exporter 后加多优化器层（mean-variance / risk-parity / vol-target 压回撤）| Vibe-Trading optimizers | ⭐⭐ 短期价值高，当前 top2 回撤 37% 偏高 |
| F | 策略目录 SKILL.md 化 | Vibe-Trading | ⭐ 可选 |
| G | IBKR 实盘下单层（paper → live + pre-trade risk gate） | FinceptTerminal | ⭐ 长期 |

**不建议做的事**：
1. 不要 LLM 直接喊单（ML ranker 已经 Sharpe 2.1，LLM 接管会退化）
2. 不要照搬 persona agent（S&P500 横截面 quant，persona 没价值）
3. 不要 AutoHedge sequential handoff（单人 batch 不需要 agent 协作）
4. 不要重写 Qlib / LEAN
5. 不要早期上 multi-agent debate（token 成本太高）

---

## 7. quant_by_leancli 现状诊断 + 跑模拟阻塞

### 现状

[quant_by_leancli/](quant_by_leancli/)（位于 `finance-idea/` 内部，是独立 git repo）盘点：

| 项目 | 状态 |
|---|---|
| Python 3.12.9 | ✅ 已有 |
| 项目代码（4 个 LEAN 项目：NBISLab / NBIS5mLab / OUPair5mLab / GoldKCSqueezeLab） | ✅ 完整 |
| `.venv312` Python 虚拟环境 | ❌ 不存在 |
| `pip install -r requirements.txt` | ❌ 没装 |
| **LEAN CLI** | ❌ `lean` 命令找不到 |
| **Docker Desktop** | ❌ `docker` 命令找不到 |
| LEAN workspace 初始化（`lean_workspace/lean.json`）| ❌ 不存在 |
| 行情数据（`lean_workspace/data/`、`data/raw/`）| ❌ 完全空 |
| 历史回测结果（`lean_workspace/results/`）| ❌ 不存在 |

### 核心阻塞

**LEAN 引擎只能在 Docker 里跑**，所以阻塞链是：

```
Docker Desktop (没装)
  ↓
LEAN CLI (没装)
  ↓
.venv312 (没建)
  ↓
依赖 (没 pip install)
  ↓
数据 (空)
  ↓
回测 (不可能)
```

连 walk-forward 这种"看着像 Python 脚本"的入口也是依赖 `lean_trading_platform.research.run_lean_jobs_parallel`，**绕不开 LEAN/Docker**。

### 三条路径

| 路径 | 描述 | 时间 | 阻塞 |
|---|---|---|---|
| **A** | 装 Docker + venv + LEAN CLI + 用 LEAN 自带免费 SPY 数据跑 NBISLab baseline（symbol 覆写成 SPY，纯 smoke test） | ≥ 1 小时 | **需要装 Docker Desktop（admin、WSL2、重启）** |
| **B** | 装 Docker + IBKR TWS 登录 + `data export` 真 NBIS 数据 + matrix backtest | 数小时 | 同 A，外加 IBKR 账号 + TWS 配置 |
| **C** | 不装 Docker，先 `scripts/fetch_sp500_fundamentals.py` 跑 yfinance 数据下载 + 跑 factor_lab 计算 Alpha158（纯 Python） | 30 分钟 | 不是回测，看不到曲线 |

**等用户确认**：本机有没有 Docker Desktop / 愿不愿意装。在用户回答前，**不要替他装 Docker**。

### 替代选项

如果用户只是想"看 LLM agent 跑起来长什么样"而不是真的要 quant_by_leancli 回测：

- 切到 [other-finance-package/Stockagent/](other-finance-package/Stockagent/) — 完全合成数据，6 个 pip 包，只要 `OPENAI_API_KEY`，30 分钟出结果
- 烧钱预警：50 agent × 264 天默认是数千次 LLM call，**先把天数砍到 5-10 试跑**

---

## 8. 文件地图（本 session 关心的）

```
finance-idea/
├── handover.md                          ← validation50 / dashboard 项目交接（已有）
├── handover_agent_research.md           ← 本文件（agent 调研 + quant_by_leancli 诊断）
├── CLAUDE.md                            ← 本次新写：16 仓库拉取脚本 + 调研速查
│
├── other-finance-package/               ← 16 个克隆仓库（已在 .gitignore 排除）
│   ├── financial_trading_agent_repos.md ← 16 仓库选型清单（用户原作）
│   ├── 调研.md                          ← 用户原调研笔记
│   ├── TradingAgents/                   ← LangGraph 多 agent 决策
│   ├── ai-hedge-fund/                   ← 16 大师 persona
│   ├── AI-Trader/                       ← FastAPI 交易平台
│   ├── Vibe-Trading/                    ← ReAct + SKILL
│   ├── FinRobot/                        ← AutoGen Group Chat
│   ├── RD-Agent/                        ← Hypothesis loop
│   ├── qlib/                            ← Microsoft 量化平台
│   ├── FinRL-Trading/                   ← FinRL-X 执行
│   ├── AutoHedge/                       ← Swarms + Solana
│   ├── FinGPT/                          ← 金融 LLM 微调
│   ├── FinceptTerminal/                 ← C++ 终端，IBKR 实盘 ⭐
│   ├── FinRL/                           ← DRL trading
│   ├── AgenticTrading/                  ← DAG orchestrator
│   ├── stockbench/                      ← LLM benchmark
│   ├── live-trade-bench/                ← 实时 agent 评测
│   └── Stockagent/                      ← 多 agent 模拟（合成数据）
│
└── quant_by_leancli/                    ← 用户自己的量化框架（独立 git repo）
                                         ← 现状：全新未初始化，跑模拟有硬阻塞
                                         ← 设计建议见 §6
```

---

## 9. 接手后的最小验证

确认本次 session 资产到位。先 `cd` 到 `finance-idea/`（两种平台的根路径见 §0 路径约定），再执行：

**macOS / Linux (bash)**：

```bash
cd /Users/bytedance/Desktop/stock/finance-idea   # 本机 Mac 根路径

# 1. 检查 16 个仓库是否还在
ls other-finance-package/ | grep -E "^(TradingAgents|ai-hedge-fund|qlib|RD-Agent|Stockagent)$" | wc -l
# 应该输出 5

# 2. 看本次新增的 CLAUDE.md
head -20 CLAUDE.md

# 3. 如果有仓库丢了，按 CLAUDE.md 里的一键脚本补
```

**Windows (PowerShell)**：

```powershell
cd "d:\ai_play\memory-semiconductor-investing\finance-idea"   # 原 Windows 根路径

# 1. 检查 16 个仓库是否还在（应输出 5）
(Get-ChildItem other-finance-package -Directory | Where-Object {
  $_.Name -match '^(TradingAgents|ai-hedge-fund|qlib|RD-Agent|Stockagent)$'
}).Count

# 2. 看本次新增的 CLAUDE.md
Get-Content CLAUDE.md -TotalCount 20

# 3. 如果有仓库丢了，按 CLAUDE.md 里的一键脚本补
```

---

## 10. 下一步该问用户什么

按优先级：

1. **本机有没有 Docker Desktop / 愿不愿意装？** — 决定 quant_by_leancli 能不能进 §7 路径 A
2. **真正想要的是"跑通 LEAN 回测看曲线"还是"给项目加 LLM agent 层"？** — 前者走 §7 路径 A，后者走 §6 建议 A+B
3. **当前要不要先跑 [Stockagent](other-finance-package/Stockagent/) 看 LLM agent 长什么样？** — 30 分钟出结果，跟 quant_by_leancli 解耦

---

## 11. 用户偏好（本 session 观察到的）

- 中文沟通，路径用 markdown clickable link
- 偏好"先盘点现状再给建议"，不喜欢空对空
- 反感"30 分钟跑起来"那种过度乐观估算 — 要诚实标阻塞
- 对工程细节耐心（愿意看长报告），但要结构化
- 已有项目（quant_by_leancli）工程层很扎实，不要建议他做基础设施层重写
