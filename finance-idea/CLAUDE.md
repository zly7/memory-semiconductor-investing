# finance-idea/ 工作区指引

本目录用来沉淀金融 / 量化 / 投研 Agent 相关的研究资料、原型仓库与设计调研。

## 子目录约定

- `quant_by_leancli/`：用户自己的正式量化框架（LEAN + IBKR + Qlib + 自建 ML/factor lab），是独立 git 仓库，已在父级 `.gitignore` 排除。
- `other-finance-package/`：第三方金融 / 交易 Agent 参考仓库的克隆目录。**所有子目录都已在父级 `.gitignore` 中排除**（规则 `finance-idea/other-finance-package/*/`），可放心 clone，不会污染主仓库 git 状态。
- `other-finance-package/financial_trading_agent_repos.md`：第三方仓库选型清单与推荐理由，是 `other-finance-package/` 下应有内容的权威说明。
- `other-finance-package/调研.md`：调研笔记。

## 需要拉取的第三方参考仓库（16 个）

如果 `other-finance-package/` 下缺少以下任何子目录，按下面的命令补齐。详细分类和推荐理由见 [other-finance-package/financial_trading_agent_repos.md](other-finance-package/financial_trading_agent_repos.md)。

| # | 仓库 | 类型 | URL |
|---|---|---|---|
| 1 | TradingAgents | 多 Agent 交易决策 | https://github.com/TauricResearch/TradingAgents |
| 2 | ai-hedge-fund | 投资大师 persona Agent | https://github.com/virattt/ai-hedge-fund |
| 3 | AI-Trader | Agent-native 交易平台 | https://github.com/HKUDS/AI-Trader |
| 4 | Vibe-Trading | 交易研究 Agent / SKILL 化工作台 | https://github.com/HKUDS/Vibe-Trading |
| 5 | FinRobot | 金融分析 Agent 平台（AutoGen） | https://github.com/AI4Finance-Foundation/FinRobot |
| 6 | RD-Agent | 自动量化研发 Agent | https://github.com/microsoft/RD-Agent |
| 7 | qlib | AI 量化研究平台 | https://github.com/microsoft/qlib |
| 8 | FinRL-Trading | FinRL-X 交易基础设施 | https://github.com/AI4Finance-Foundation/FinRL-Trading |
| 9 | AutoHedge | Swarm 风格自主 hedge fund | https://github.com/The-Swarm-Corporation/AutoHedge |
| 10 | FinGPT | 金融大语言模型底座 | https://github.com/AI4Finance-Foundation/FinGPT |
| 11 | FinceptTerminal | 金融智能终端（含 IBKR 实盘） | https://github.com/Fincept-Corporation/FinceptTerminal |
| 12 | FinRL | 金融强化学习经典框架 | https://github.com/AI4Finance-Foundation/FinRL |
| 13 | AgenticTrading | Agentic trading orchestration | https://github.com/Open-Finance-Lab/AgenticTrading |
| 14 | stockbench | LLM 股票交易 Benchmark | https://github.com/ChenYXxxx/stockbench |
| 15 | live-trade-bench | 实时交易 Agent 评测 | https://github.com/ulab-uiuc/live-trade-bench |
| 16 | Stockagent | 多 Agent 股票交易模拟 | https://github.com/MingyuJ666/Stockagent |

### 一键拉取（shallow clone，幂等）

在 PowerShell 中运行：

```powershell
cd "d:\ai_play\memory-semiconductor-investing\finance-idea\other-finance-package"

$repos = @(
  "TauricResearch/TradingAgents",
  "virattt/ai-hedge-fund",
  "HKUDS/AI-Trader",
  "HKUDS/Vibe-Trading",
  "AI4Finance-Foundation/FinRobot",
  "microsoft/RD-Agent",
  "microsoft/qlib",
  "AI4Finance-Foundation/FinRL-Trading",
  "The-Swarm-Corporation/AutoHedge",
  "AI4Finance-Foundation/FinGPT",
  "Fincept-Corporation/FinceptTerminal",
  "AI4Finance-Foundation/FinRL",
  "Open-Finance-Lab/AgenticTrading",
  "ChenYXxxx/stockbench",
  "ulab-uiuc/live-trade-bench",
  "MingyuJ666/Stockagent"
)

foreach ($r in $repos) {
  $name = ($r -split "/")[1]
  if (Test-Path $name) {
    Write-Host "skip $name (exists)"
  } else {
    git clone --depth=1 "https://github.com/$r.git" $name
  }
}
```

Bash 等价：

```bash
cd "d:/ai_play/memory-semiconductor-investing/finance-idea/other-finance-package"

for r in \
  TauricResearch/TradingAgents \
  virattt/ai-hedge-fund \
  HKUDS/AI-Trader \
  HKUDS/Vibe-Trading \
  AI4Finance-Foundation/FinRobot \
  microsoft/RD-Agent \
  microsoft/qlib \
  AI4Finance-Foundation/FinRL-Trading \
  The-Swarm-Corporation/AutoHedge \
  AI4Finance-Foundation/FinGPT \
  Fincept-Corporation/FinceptTerminal \
  AI4Finance-Foundation/FinRL \
  Open-Finance-Lab/AgenticTrading \
  ChenYXxxx/stockbench \
  ulab-uiuc/live-trade-bench \
  MingyuJ666/Stockagent
do
  name="${r##*/}"
  if [ -d "$name" ]; then
    echo "skip $name (exists)"
  else
    git clone --depth=1 "https://github.com/$r.git" "$name"
  fi
done
```

并行版本（更快，需要支持 `&` 后台作业的 shell）：把 `git clone` 行改为 `git clone --depth=1 ... &`，循环末尾加 `wait`。注意并行 16 路对带宽和磁盘有压力，建议分两批 8+8。

## 搜索这些子仓库内容时的注意事项

父级 `.gitignore` 排除了 `other-finance-package/*/`，**ripgrep / Grep 工具默认会跳过它们**。需要搜索时显式加 `--no-ignore`：

```bash
rg --no-ignore -i "your-pattern" other-finance-package/
```

## 设计调研结论（速查）

`other-finance-package/financial_trading_agent_repos.md` 中已经按"按你的研究目标怎么读"做了分组。简化版：

- **看决策 agent 怎么搭**：TradingAgents、ai-hedge-fund
- **看投研 / 报告 agent**：FinRobot、Vibe-Trading、FinceptTerminal
- **看量化研究闭环**：RD-Agent + Qlib + AgenticTrading
- **看 LLM 是否真会交易**：stockbench、live-trade-bench、Stockagent
- **看 LLM 信号 → 真实订单**：FinRL-Trading、AutoHedge（DeFi）、FinceptTerminal（IBKR）

**IBKR 实盘交易代码只有 FinceptTerminal 一家有**（C++ 走 Client Portal Gateway，文件 `other-finance-package/FinceptTerminal/fincept-qt/src/trading/brokers/ibkr/IBKRBroker.cpp`），其余仓库要么没接 broker，要么只用 `ib_insync` 拉数据。
