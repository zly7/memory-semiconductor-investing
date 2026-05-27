# 金融炒股 / 投研 / 量化 Agent GitHub 仓库清单

> 整理日期：2026-05-27  
> 范围：只保留“炒股 Agent / 投研 Agent / 量化研发 Agent / 交易评测 Benchmark / 金融 Agent Infra”。  
> 已按你的要求排除：纯金融数据接口类仓库，例如 yfinance、AKShare、TuShare、OpenBB、ccxt、Alpha Vantage wrapper 等。

---

## 一、最推荐优先阅读的仓库

| 优先级 | 仓库 | 链接 | 类型 | 简介 | 推荐理由 |
|---|---|---|---|---|---|
| 1 | TauricResearch / TradingAgents | https://github.com/TauricResearch/TradingAgents | 多 Agent 交易决策框架 | 模拟真实交易公司结构，用基本面、技术面、新闻、情绪、Trader、Risk Manager、Portfolio Manager 等角色协作生成交易判断。 | 最适合理解“炒股 Agent 标准架构”：多角色分工、辩论、交易提案、风控审批、决策日志。 |
| 2 | virattt / ai-hedge-fund | https://github.com/virattt/ai-hedge-fund | AI hedge fund demo | 用 Buffett、Munger、Burry、Cathie Wood、Graham 等投资风格 Agent，加上估值、情绪、基本面、技术面、风控、组合经理 Agent 做决策。 | 最适合理解“投资风格 persona + 信号聚合 + 风控/组合经理”的产品化写法。 |
| 3 | HKUDS / AI-Trader | https://github.com/HKUDS/AI-Trader | Agent-native trading platform | 让 AI agent 接入交易平台，发布 trading signal、参与讨论、copy trading、paper trading，并支持股票、crypto、forex、options、futures 等市场。 | 最近一年新建、高 star、更新活跃；更像“AI 交易平台 / agent 社区 / 信号网络”的产品形态。 |
| 4 | HKUDS / Vibe-Trading | https://github.com/HKUDS/Vibe-Trading | 个人交易研究 Agent | 一条命令给 Agent 接入交易研究能力，支持研究目标、策略分析、回测、报告、Web/API/CLI/MCP 等工作流。 | 比 AI-Trader 更适合做工程参考：像“金融研究工作台 + 回测 Agent + 报告 Agent”。 |
| 5 | AI4Finance-Foundation / FinRobot | https://github.com/AI4Finance-Foundation/FinRobot | 金融分析 Agent 平台 | 面向金融分析的 LLM Agent 平台，整合 LLM、强化学习、量化分析，用于投资研究自动化、算法交易策略、风险评估等。 | 最适合看“投研报告自动化 / 金融分析 Agent 平台”如何搭，而不是只看交易信号。 |
| 6 | microsoft / RD-Agent | https://github.com/microsoft/RD-Agent | 自动化量化研发 Agent | 微软的 R&D-Agent，Quant 版本用于自动因子挖掘、模型优化、数据驱动量化研发。 | 比“直接炒股 Agent”更靠谱的方向：让 Agent 自动提出假设、写因子、跑实验、迭代策略。 |
| 7 | microsoft / qlib | https://github.com/microsoft/qlib | AI 量化研究平台 | 微软 AI-oriented quant investment platform，覆盖数据处理、模型训练、回测、组合优化，并接入 RD-Agent 做自动研发。 | 交易 Agent 真要落地，需要这种回测、因子、组合、执行骨架；建议和 RD-Agent 一起读。 |
| 8 | AI4Finance-Foundation / FinRL-Trading | https://github.com/AI4Finance-Foundation/FinRL-Trading | FinRL-X，AI-native 交易基础设施 | 新一代 FinRL-X，强调模块化、可部署、weight-centric interface，统一数据处理、策略组合、回测和 broker execution。 | 适合理解“Agent 信号如何接到真实交易系统”：权重接口、回测一致性、paper/live execution、风控。 |

---

## 二、炒股 / 交易决策 Agent

### 1. TauricResearch / TradingAgents

- 仓库链接：https://github.com/TauricResearch/TradingAgents
- 类型：多 Agent 金融交易框架
- 简介：TradingAgents 把交易决策拆成多个角色，包括基本面分析师、情绪分析师、新闻分析师、技术分析师、Trader、Risk Management Team、Portfolio Manager 等，通过协作讨论形成交易判断。
- 推荐理由：
  - 是最典型的“机构投研团队模拟”架构。
  - 非常适合学习多 Agent 的职责拆分：分析 Agent 负责信号，Trader 负责交易 proposal，Risk Manager/Portfolio Manager 负责约束。
  - 适合研究如何做结构化输出、决策日志、风控审批和多模型 provider 支持。
- 适合重点读：
  - agent 角色定义
  - debate / discussion 流程
  - risk management 和 portfolio manager 的 prompt
  - decision log / checkpoint / LangGraph 编排

---

### 2. virattt / ai-hedge-fund

- 仓库链接：https://github.com/virattt/ai-hedge-fund
- 类型：AI hedge fund proof-of-concept
- 简介：用多种投资大师风格 Agent 和工具型 Agent 协作生成投资决策。角色包括 Buffett、Munger、Graham、Burry、Cathie Wood、Peter Lynch、Druckenmiller、估值 Agent、情绪 Agent、基本面 Agent、技术面 Agent、Risk Manager、Portfolio Manager 等。
- 推荐理由：
  - 很适合理解“persona agent”怎么写。
  - 代码和概念都比较直观，适合作为多 Agent 投资 demo 学习。
  - 它把投资风格显式拆成 prompt/schema，是做“投资大师风格分析器”的好参考。
- 注意：
  - README 明确是教育和研究用途，不用于真实交易。
  - 不要把它当成可直接实盘的策略系统。
- 适合重点读：
  - 每个投资风格 Agent 的 prompt
  - signal schema
  - risk manager 和 portfolio manager
  - order generation 逻辑

---

### 3. HKUDS / AI-Trader

- 仓库链接：https://github.com/HKUDS/AI-Trader
- 类型：Agent-native trading platform
- 简介：AI-Trader 定位为给 AI agent 使用的交易平台。Agent 可以接入平台、发布交易信号、参与讨论、进行 copy trading / paper trading，并跨股票、加密、外汇、期权、期货等市场同步交易信号。
- 推荐理由：
  - 最近一年新建，star 增长非常快，且最近仍在更新。
  - 产品形态不是单纯“本地跑一个交易 Agent”，而是“AI Agent 交易社区 + 信号平台 + copy trading”。
  - 值得研究它的 agent skill、API、signal types、copy trading、paper trading、reward/ranking 设计。
- 适合重点读：
  - `skills/ai4trade/SKILL.md`
  - `docs/README_AGENT.md`
  - `docs/api/openapi.yaml`
  - signal / copytrade / tradesync API
  - paper trading 和 community signal flow

---

### 4. HKUDS / Vibe-Trading

- 仓库链接：https://github.com/HKUDS/Vibe-Trading
- 类型：个人交易研究 Agent / 交易研究工作台
- 简介：Vibe-Trading 给 Agent 提供金融研究、交易分析、策略生成、回测、报告生成等能力，支持 Web/API/CLI/MCP，并围绕 research goal 做任务生命周期管理。
- 推荐理由：
  - 更适合工程学习：它不是只输出“买/卖/持有”，而是围绕研究目标跑完整的研究工作流。
  - 适合看“Agent 如何管理长期研究任务、证据、claims、open items、报告产物”。
  - 对你如果要做“投研 Agent / 策略研究 Agent”很有参考价值。
- 适合重点读：
  - goal lifecycle
  - tools / agent 目录
  - MCP / API / CLI 入口
  - research report artifact
  - backtesting / strategy examples

---

### 5. The-Swarm-Corporation / AutoHedge

- 仓库链接：https://github.com/The-Swarm-Corporation/AutoHedge
- 类型：autonomous hedge fund demo
- 简介：AutoHedge 宣称用 swarm intelligence 和 specialized AI agents 做端到端市场分析、风险管理和交易执行；当前主要支持 Solana，后续计划扩展 Coinbase 等。
- 推荐理由：
  - 适合理解“swarm intelligence + trading agent”的产品叙事。
  - 代码较轻，可以快速看它如何组织 Director、Quant、Risk、Execution 等角色。
  - 适合作为“自主交易 Agent demo”的横向对比。
- 注意：
  - 它更偏 demo / startup-style repo，严肃回测和风控能力需要自己验证。
  - 不建议作为可信实盘基础。
- 适合重点读：
  - `autohedge/`
  - `example.py`
  - risk-first architecture 相关代码
  - execution 模块

---

## 三、投研 / 金融分析 / 金融 LLM Agent

### 6. AI4Finance-Foundation / FinRobot

- 仓库链接：https://github.com/AI4Finance-Foundation/FinRobot
- 类型：金融分析 Agent 平台
- 简介：FinRobot 是 AI4Finance 的金融 Agent 平台，整合 LLM、强化学习、量化分析等技术，用于投资研究自动化、算法交易策略、风险评估、股票研究报告生成等。
- 推荐理由：
  - 比“炒股 Agent”更接近真实机构可落地的方向：先做投研分析、报告生成、风险评估。
  - 适合看财报分析、估值分析、研究报告生成这类 workflow。
  - 如果你想做“金融分析 Agent 产品”，这是非常重要的参考。
- 适合重点读：
  - `finrobot/`
  - `finrobot_equity/`
  - `tutorials_beginner/`
  - `tutorials_advanced/`
  - report generation examples

---

### 7. AI4Finance-Foundation / FinGPT

- 仓库链接：https://github.com/AI4Finance-Foundation/FinGPT
- 类型：金融大语言模型 / 金融 LLM 底座
- 简介：FinGPT 是开源金融大语言模型项目，提供金融 LLM、金融数据处理、微调示例、金融情绪/预测/投顾等任务支持。
- 推荐理由：
  - 它不是完整交易 Agent，但可以作为金融 Agent 的语义理解底座。
  - 适合做新闻、公告、研报、社媒情绪、事件分类、风险识别等信号提取。
  - 如果交易 Agent 要处理非结构化金融文本，FinGPT 这类模型/数据 pipeline 很关键。
- 适合重点读：
  - LoRA fine-tuning notebooks
  - financial sentiment / forecasting use cases
  - FinGPT model / HuggingFace resources
  - `Use_Cases.md`

---

### 8. Fincept-Corporation / FinceptTerminal

- 仓库链接：https://github.com/Fincept-Corporation/FinceptTerminal
- 类型：金融智能终端 / Agent-enabled finance terminal
- 简介：FinceptTerminal 是开源金融终端，定位类似自托管金融智能终端。功能包括多资产分析、DCF、组合优化、风险指标、衍生品定价、新闻、AI agents、实时交易、broker 集成、MCP 工具等。
- 推荐理由：
  - 更像金融 Agent 的“终端级基础设施”，不是单个交易策略。
  - 有 37 个 AI agents、100+ 数据连接器、16 个 broker 集成、QuantLib Suite、Visual Workflows、MCP 工具等设计。
  - 适合研究金融 Agent 产品如何整合 UI、数据、分析、交易、workflow。
- 注意：
  - 功能面很大，建议先看架构和 agent/workflow，不要一开始陷入所有连接器细节。
- 适合重点读：
  - AI Agents 设计
  - broker integration
  - Visual workflow / MCP tool integration
  - QuantLib Suite / AI Quant Lab

---

## 四、量化研发 / 回测 / 策略基础设施

### 9. microsoft / qlib

- 仓库链接：https://github.com/microsoft/qlib
- 类型：AI-oriented 量化投资平台
- 简介：Qlib 是微软的 AI 量化研究平台，覆盖数据处理、模型训练、回测、组合优化、订单执行等模块，并与 RD-Agent 结合做自动因子挖掘和模型优化。
- 推荐理由：
  - 真正要做交易 Agent，必须有可复现的回测和量化研究底座。
  - Qlib 适合作为 Agent 的“执行/评估环境”：Agent 提出因子或策略，Qlib 负责训练、回测、评估。
  - 与 RD-Agent 结合后，很适合做“自动量化研究员”。
- 适合重点读：
  - examples
  - workflow / recorder
  - backtest 模块
  - portfolio optimization
  - RD-Agent integration

---

### 10. microsoft / RD-Agent

- 仓库链接：https://github.com/microsoft/RD-Agent
- 类型：Research & Development Agent
- 简介：RD-Agent 是微软做自动化研发的 Agent 框架，其中 RD-Agent(Q) 面向量化金融，自动做因子挖掘、模型优化、代码生成、实验执行和结果迭代。
- 推荐理由：
  - 这是我最推荐研究的“更靠谱金融 Agent 方向”：Agent 不直接喊单，而是自动做研究、写因子、跑回测、复盘迭代。
  - 适合学习任务拆解、实验闭环、代码修改、结果评估、trace 记录。
  - 和 Qlib 结合起来能形成比较完整的“量化研究 Agent”。
- 适合重点读：
  - R&D-Agent-Quant docs
  - factor mining examples
  - model optimization examples
  - experiment trace / code diff / feedback loop

---

### 11. AI4Finance-Foundation / FinRL

- 仓库链接：https://github.com/AI4Finance-Foundation/FinRL
- 类型：金融强化学习经典框架
- 简介：FinRL 是早期开源金融强化学习框架，面向 automated stock trading 的教育、benchmark 和研究原型。现在 README 也提示新架构请看 FinRL-X / FinRL-Trading。
- 推荐理由：
  - 适合补齐交易系统里的 RL 训练、环境建模、MDP、策略评估等基本概念。
  - 对理解 FinRL-X 的演进非常有帮助。
  - 如果你要研究 DRL agent trading，这是基础项目。
- 注意：
  - 新项目建议优先看 FinRL-Trading / FinRL-X。
- 适合重点读：
  - train-test-trade pipeline
  - DRL agent examples
  - MDP environment design
  - tutorials / examples

---

### 12. AI4Finance-Foundation / FinRL-Trading

- 仓库链接：https://github.com/AI4Finance-Foundation/FinRL-Trading
- 类型：FinRL-X，AI-native modular quantitative trading infrastructure
- 简介：FinRL-X 是新一代模块化量化交易基础设施，用 weight-centric interface 统一策略逻辑、回测、paper trading 和 broker execution，支持 ML stock selection、portfolio allocation、timing adjustment、risk overlay 等模块。
- 推荐理由：
  - 它解决的是“Agent 生成信号后如何进入交易系统”的问题。
  - 强调研究回测和 live execution 一致性，这是真实交易系统的关键。
  - 适合与 LLM Agent 结合：LLM 负责文本信号，FinRL-X 负责组合、风控、回测和执行。
- 适合重点读：
  - weight-centric interface
  - `src/data/`
  - `src/backtest/`
  - `src/strategies/`
  - `src/trading/`
  - pre-trade risk checks

---

### 13. Open-Finance-Lab / AgenticTrading

- 仓库链接：https://github.com/Open-Finance-Lab/AgenticTrading
- 类型：Agentic Trading orchestration framework
- 简介：AgenticTrading 尝试把传统算法交易 pipeline 映射成智能 Agent 网络，通过 memory agent、orchestrator、alpha/risk/portfolio/backtest 等模块做 Agent 化交易研究。
- 推荐理由：
  - 虽然 star 不高，但架构思想很值得看。
  - 它关注“协议化、多 Agent 协作、DAG 编排、记忆、回测、风控”的工程结构。
  - 适合你从 Agent 工程治理角度理解金融 Agent，而不是只看 prompt。
- 适合重点读：
  - FinAgents
  - orchestrator
  - memory agent
  - alpha / risk / transaction cost / portfolio modules
  - backtest examples

---

## 五、交易 Agent Benchmark / 模拟环境

### 14. ChenYXxxx / stockbench

- 仓库链接：https://github.com/ChenYXxxx/stockbench
- 类型：LLM 股票交易决策 Benchmark
- 简介：StockBench 是评估 LLM 在股票交易决策中的 benchmark 平台，模拟真实交易场景，用历史市场数据评估投资决策质量、风险管理能力和收益表现。
- 推荐理由：
  - 适合用来评估“LLM 会不会炒股”这个问题，而不是只看 demo。
  - 强调连续决策、真实市场交互、收益、风险、回撤等指标。
  - 对比不同模型、不同 agent 策略时很有价值。
- 适合重点读：
  - benchmark design
  - evaluation metrics
  - data contamination control
  - portfolio → analysis → trade workflow

---

### 15. ulab-uiuc / live-trade-bench

- 仓库链接：https://github.com/ulab-uiuc/live-trade-bench
- 类型：实时交易 Agent 评测平台
- 简介：Live Trade Bench 用于在实时市场环境中评估 LLM-based trading agents，支持运行、监控、benchmark 多个交易 Agent，目标是避免传统回测过拟合。
- 推荐理由：
  - 比静态 benchmark 更接近真实世界：实时市场、多 Agent、多市场、持续评估。
  - 很适合研究“交易 Agent 的线上评测系统”如何搭。
  - 对做 paper trading / live evaluation 平台很有参考价值。
- 适合重点读：
  - backend FastAPI
  - frontend monitoring
  - agent evaluation loop
  - real-time market benchmark design
  - anti-backtest-overfitting 设计

---

### 16. MingyuJ666 / Stockagent

- 仓库链接：https://github.com/MingyuJ666/Stockagent
- 类型：LLM-based stock trading simulation
- 简介：StockAgent 是一个由 LLM 驱动的多 Agent 股票交易模拟系统，用于模拟投资者面对宏观、政策、公司基本面、全球事件等外部因素时的交易行为。
- 推荐理由：
  - 适合看“多 Agent 投资者行为模拟”而不是单个策略收益。
  - 特别关注 test set leakage / 真实环境模拟的问题。
  - 可以作为研究型 trading agent benchmark 的补充。
- 适合重点读：
  - `agent.py`
  - `secretary.py`
  - prompts
  - simulation setup
  - leakage avoidance design

---

## 六、按你的研究目标怎么读

### 目标 A：理解“炒股 Agent 怎么做决策”

优先读：

1. TradingAgents
2. ai-hedge-fund
3. AI-Trader
4. AutoHedge

重点关注：

- 分析 Agent 如何拆分
- Trader Agent 如何生成 proposal
- Risk Manager 如何约束仓位
- Portfolio Manager 如何做最终决策
- 输出是否结构化
- 是否有交易理由、证据和风险标记

---

### 目标 B：理解“投研 Agent 怎么落地”

优先读：

1. FinRobot
2. Vibe-Trading
3. FinceptTerminal
4. FinGPT

重点关注：

- 财报 / 新闻 / 公告 / 研报处理
- research goal 管理
- 证据链和 claims 管理
- 报告生成
- 金融文本信号提取
- UI / workflow / MCP 工具整合

---

### 目标 C：理解“量化研究 Agent 怎么做闭环”

优先读：

1. RD-Agent
2. Qlib
3. FinRL-Trading
4. FinRL
5. AgenticTrading

重点关注：

- Agent 如何提出因子假设
- 如何写因子代码
- 如何跑回测
- 如何根据结果迭代
- 如何避免未来函数和数据泄漏
- 如何把信号转成 portfolio weights
- 如何接 paper/live execution

---

### 目标 D：评估 Agent 是否真的会交易

优先读：

1. StockBench
2. LiveTradeBench
3. StockAgent

重点关注：

- 连续决策设置
- 训练数据污染 / 数据泄漏控制
- cumulative return
- max drawdown
- Sharpe / Sortino
- turnover
- transaction cost
- benchmark baseline，比如 buy-and-hold / index / random policy

---

## 七、总览表

| 仓库 | 链接 | 类型 | 简介 | 推荐理由 |
|---|---|---|---|---|
| TradingAgents | https://github.com/TauricResearch/TradingAgents | 多 Agent 交易决策 | 模拟真实交易团队，分析师、Trader、Risk、PM 协作决策 | 最标准的炒股 Agent 架构参考 |
| ai-hedge-fund | https://github.com/virattt/ai-hedge-fund | AI hedge fund demo | 投资大师 persona + 工具 Agent + 风控/组合经理 | 最适合学习 persona agent 和信号聚合 |
| AI-Trader | https://github.com/HKUDS/AI-Trader | Agent 交易平台 | Agent 发布信号、copy trading、paper trading、社区协作 | 近期最火的 Agent-native trading 产品形态 |
| Vibe-Trading | https://github.com/HKUDS/Vibe-Trading | 交易研究 Agent | 研究目标、策略分析、回测、报告、MCP/API/CLI | 工程参考价值高，适合做投研/策略工作台 |
| AutoHedge | https://github.com/The-Swarm-Corporation/AutoHedge | 自主 hedge fund demo | Swarm intelligence + market analysis + risk + execution | 适合看 swarm-style 交易 Agent demo |
| FinRobot | https://github.com/AI4Finance-Foundation/FinRobot | 金融分析 Agent 平台 | 投资研究自动化、算法策略、风险评估、报告生成 | 更接近真实机构可落地的投研 Agent |
| FinGPT | https://github.com/AI4Finance-Foundation/FinGPT | 金融 LLM 底座 | 金融大模型、微调、情绪/预测/投顾任务 | 适合作为交易 Agent 的文本信号模块 |
| FinceptTerminal | https://github.com/Fincept-Corporation/FinceptTerminal | 金融智能终端 | AI agents、broker、MCP、数据连接器、终端 UI | 看金融 Agent 产品和基础设施集成 |
| Qlib | https://github.com/microsoft/qlib | AI 量化平台 | 数据、模型、回测、组合优化、执行 | 交易 Agent 落地需要的量化研究底座 |
| RD-Agent | https://github.com/microsoft/RD-Agent | 自动量化研发 Agent | 自动因子挖掘、模型优化、代码生成、实验迭代 | 最值得研究的“Agent 做量化研发”方向 |
| FinRL | https://github.com/AI4Finance-Foundation/FinRL | 金融强化学习框架 | 经典 DRL automated trading 教育/研究框架 | 补齐 RL trading 基础概念 |
| FinRL-Trading | https://github.com/AI4Finance-Foundation/FinRL-Trading | FinRL-X 交易基础设施 | weight-centric、回测、paper/live execution、风控 | 适合把 LLM 信号接到真实交易系统 |
| AgenticTrading | https://github.com/Open-Finance-Lab/AgenticTrading | Agentic trading orchestration | 把算法交易 pipeline 映射成 Agent 网络 | 架构思想好，适合看协议化 Agent 协作 |
| StockBench | https://github.com/ChenYXxxx/stockbench | LLM 股票交易 Benchmark | 连续股票交易决策评测 | 评估 LLM 是否真的会交易 |
| live-trade-bench | https://github.com/ulab-uiuc/live-trade-bench | 实时交易 Agent Benchmark | 实时市场环境中评估 LLM trading agents | 避免单纯历史回测过拟合 |
| StockAgent | https://github.com/MingyuJ666/Stockagent | 股票交易模拟 Agent | 多 Agent 模拟投资者交易行为 | 适合研究真实环境模拟和数据泄漏问题 |

---

## 八、我建议的阅读顺序

如果只读 6 个：

1. TradingAgents  
2. ai-hedge-fund  
3. AI-Trader  
4. Vibe-Trading  
5. RD-Agent + Qlib  
6. StockBench / LiveTradeBench  

如果你要做一个自己的项目，我建议路线是：

```text
FinGPT / 新闻公告处理
        ↓
TradingAgents / Vibe-Trading 的多 Agent 分析结构
        ↓
Qlib / FinRL-Trading 的回测与执行环境
        ↓
StockBench / LiveTradeBench 的评估体系
        ↓
AI-Trader 的 signal / community / copy trading 产品形态
```

---

## 九、不要直接照搬的点

1. 不要让 LLM 直接输出“买卖多少股”就算完成。
2. 不要只看收益率，必须看最大回撤、交易成本、换手、Sharpe、Sortino、基准比较。
3. 不要跳过数据泄漏检查，尤其是 LLM 预训练可能看过历史事件。
4. 不要把网页抓取数据和实盘交易直接连起来，中间必须有缓存、校验、风控和异常处理。
5. 不要忽略 broker execution、滑点、成交失败、限价单、流动性这些工程问题。
6. 不要把 persona prompt 当成投资能力，真正价值在数据、回测、风控、执行闭环。
