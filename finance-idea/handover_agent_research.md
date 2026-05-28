# finance-idea · Agent 调研 + quant_by_leancli 接手文档

> 最后更新: 2026-05-28 · 接手人 10 分钟内能上手为目标
>
> 跟 [handover.md](handover.md) 是不同主题：那篇是 validation50 / dashboard 项目；本篇是**第三方 agent 仓库调研**和 **quant_by_leancli 跑模拟的阻塞分析**。

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
| Agent 设计 design pattern 调研 | ✅ 完成 | 4 个 Explore agent 并行分析，结论见 §4 |
| IBKR 实盘集成调研 | ✅ 完成 | 结论：**只有 FinceptTerminal 一家**有真 IBKR 下单 |
| 对 quant_by_leancli 的设计建议 | ✅ 完成 | 见 §6（A/B/C/D/E/F/G 七条，按 ROI 排序）|
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

横向维度对比（角色拆分 / Prompt / Schema / 风控 / 工具 / 记忆 / 执行）详见 session 的原始分析输出。本 handover 不再重复，需要时查 git log 这次会话的 assistant 回复（关键词："金融 Agent 设计思路合并报告"）。

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

**对 quant_by_leancli 的含义**：用户已经在 [quant_by_leancli/ibkr/](../quant_by_leancli/ibkr/) 自己写了 IBKR 数据层（`ib_async` + `tws_client.py` ibapi 包装），如果将来要做实盘下单，可参考 FinceptTerminal 的 BrokerCredentials + has_native_paper 切换设计，但 Python 用 `ib_async.placeOrder()` 更直接。

---

## 6. 给 quant_by_leancli 的设计建议（按 ROI 排序）

完整分析见 session 原始输出（关键词："quant_by_leancli 的设计建议"）。要点：

**用户已经做对的**：
- factor_lab + ml_engine ≈ Qlib + RD-Agent 下半层（已超出 FinRL 单一 DRL 路线）
- lean_trading_platform + lean_workspace ≈ FinRL-Trading weight-centric execution（用 LEAN 比 FinRL-X 更接近实盘）
- ibkr/providers ≈ FinRL.ibkrdownloader 完整版（仅缺下单）
- [docs/research_registry/sp500_rotation_hypotheses.csv](../quant_by_leancli/docs/research_registry/sp500_rotation_hypotheses.csv) ≈ **RD-Agent QuantTrace 雏形**（最大资产）

**核心判断**：不缺基础设施，**唯一明显缺口是"研究迭代的 LLM 化"**（项目里完全没有 LLM 模块）。

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

[../quant_by_leancli/](../quant_by_leancli/) 在本机是**全新的**（所有文件都是 2026-05-28 创建）。盘点：

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

确认本次 session 资产到位：

```bash
cd "d:/ai_play/memory-semiconductor-investing/finance-idea"

# 1. 检查 16 个仓库是否还在
ls other-finance-package/ | grep -E "^(TradingAgents|ai-hedge-fund|qlib|RD-Agent|Stockagent)$" | wc -l
# 应该输出 5

# 2. 看本次新增的 CLAUDE.md
cat CLAUDE.md | head -20

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
