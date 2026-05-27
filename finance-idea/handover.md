# finance-idea · 交接文档

> 最后更新: 2026-05-27 · 接手人 5 分钟内能上手为目标

---

## 1. 这个项目在做什么

一个**市场情绪信号验证平台**。两件事：

1. **日度 dashboard**: 国内 QDII 纳指 ETF 溢价、VIX、DXY、北向资金等 10 个信号的当日读数，每天 refresh 一次给出"今天市场在何种情绪状态"。
2. **回测验证**: 把"X 信号触发后买入/卖出"这类民间策略放进系统化框架去验证，看哪些是真有效 / 哪些是统计幻觉。

最终形态: Futu 风格的 SPA（红涨绿跌）+ FastAPI 后端 + 本地 parquet 缓存。

---

## 2. 当前状态

| 模块 | 状态 | 说明 |
|---|---|---|
| 数据层 (`finance-data-api/`)        | ✅ 完成 | 99 个 series 缓存，最近 refresh 2026-05-27 |
| 后端 (`backend/`)                    | ✅ 完成 | FastAPI，10 个 idea 的 signals 接口跑通 |
| 前端 (`frontend/`)                   | ✅ 完成 | Vue 3 + Vite + ECharts，dashboard + idea detail 两个页面都跑通 |
| 50 策略验证 (`validation50/`)       | 🚧 **进行中** | 框架 + feature list 完成，50 个策略**未实现** |
| Deep-research 输入 (`deepresearch-result/`) | ✅ 已归档 | 4 份调研报告，76 个候选策略已抽取 |

**🚧 in flight 的活**: validation50 已有 [FEATURE_LIST.md](validation50/FEATURE_LIST.md) 的 50 行清单 + 数据采集脚本 + 跑批 runner，但 `validation50/strategies/` 是空的——50 个 `compute()` 函数还没写。

---

## 3. 5 分钟跑起来

```bash
cd /Users/bytedance/Desktop/stock/finance-idea

# 一次性环境
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt fastapi 'uvicorn[standard]'
(cd frontend && npm install)

# 启动（前后端并行）
./run_dev.sh
# → backend  http://127.0.0.1:8000/docs
# → frontend http://localhost:5173
```

每天用:
```bash
python finance-data-api/refresh.py    # 拉新数据
# 浏览器刷新 localhost:5173
```

---

## 4. 三层架构（必读）

```
┌─────────────────────────────────────────────────┐
│ frontend/  Vue 3 SPA  红涨绿跌 / ECharts        │
│   ↓ /api/dashboard、/api/ideas/{id}             │
├─────────────────────────────────────────────────┤
│ backend/   FastAPI  signals/ 是纯函数          │
│   ↓ 直接 import storage / fetchers              │
├─────────────────────────────────────────────────┤
│ finance-data-api/  parquet 缓存 + akshare/yf    │
│   data/prices/   data/nav/   data/macro/       │
└─────────────────────────────────────────────────┘
```

**核心抽象**: 每个 idea 是 `backend/app/signals/<id>.py` 里一个 `compute() -> SignalBundle`。SignalBundle 在 [_base.py](backend/app/signals/_base.py) 定义，自带 `snapshot()` 和 `detail()` 两个序列化方法，前端两个页面直接消费。

**新增 idea 三步走**:
1. 在 `backend/app/signals/<new_id>.py` 写 `compute()` 返回 SignalBundle
2. 注册到 `backend/app/signals/__init__.py` 的 `REGISTRY` 字典
3. 前端无需改动——dashboard 自动多一张卡

---

## 5. 数据层细节

`finance-data-api/`:
- [universe.py](finance-data-api/universe.py) — 46 资产 × 8 类（US / CN / HK / QDII / 商品 / 利率 / FX / Crypto），声明式
- [storage.py](finance-data-api/storage.py) — parquet 增量 upsert，路径 `data/{prices,nav,macro}/<key>.parquet`
- [fetchers.py](finance-data-api/fetchers.py) — akshare（Sina 主 + EM 回退）+ yfinance
- [refresh.py](finance-data-api/refresh.py) — CLI: `--only KEY1,KEY2`、`--class qdii_etf`、`--sources ak_etf`

**当前缓存** (99 series):
- prices: 35+ ETF/index series（A 股 / 美股 / HK / QDII / 商品 / FX / Crypto），加上 18 个新 ETF（IEF, VEU, EFA, USMV, QUAL, MTUM, 11 个 SPDR 行业 ETF 等）
- nav: 14 QDII / 国内 ETF 的日 NAV
- macro: 13 个 FRED 序列（T10Y3M、T10Y2Y、BAMLH0A0HYM2、NFCI、CFNAI、DGS3MO 等）+ 北向资金

**坑 1 — 包目录名带连字符**: `finance-data-api` 不能直接 `import`，所有调用方都得 `sys.path.insert(0, "finance-data-api")` 然后裸 import `storage`。这是有意为之，别动。
**坑 2 — 东方财富对外网不稳**: akshare 的 `_em` 后缀函数容易 connection-reset，已经在 fetchers.py 里加了 Sina 回退（`fund_etf_hist_sina`、`stock_zh_index_daily`、`stock_hk_index_daily_sina`），不要回滚到纯 EM。

---

## 6. 后端 API 速查

`http://127.0.0.1:8000/docs` 有自动 OpenAPI。常用路由:

| Method/Path | 用途 |
|---|---|
| `GET /api/dashboard` | 10 个 idea 当下读数 + 60d 走势小图 |
| `GET /api/ideas/{id}` | 单 idea 全套数据（时序、bands、buckets、净值曲线、markdown） |
| `GET /api/series/{key}` | 任意资产原始 OHLC |
| `GET /api/ticker` | 顶部跑马灯（上证/沪深300/HSI/SPY/QQQ/VIX/DXY） |
| `GET /api/meta` | 各 series 缓存状态、上次刷新时间 |

**对接前端的契约**在 [backend/app/schemas.py](backend/app/schemas.py)。**前端镜像类型**在 [frontend/src/lib/api.ts](frontend/src/lib/api.ts)，**两边要同步改**。

---

## 7. 前端速查

`frontend/src/`:
- `App.vue` — 顶栏 + ticker + router-view 三段
- `views/DashboardView.vue` — `/` 路径，10 张卡 + 一张完整表
- `views/IdeaDetailView.vue` — `/idea/:id` 路径，主图 + 热力图 + 净值
- `components/` — 单一职责 Vue 组件，按 Futu 思路设计:
  - `SignalCard.vue` — 大数字 + sparkline + pill
  - `SignalChart.vue` — 主时序图（signal + asset overlay + bands）
  - `BucketHeatmap.vue` — 分位 × horizon 热力图
  - `EquityCurveChart.vue` — 策略 vs 基准
- `lib/`
  - `api.ts` — typed fetch
  - `format.ts` — `dirColor()`、`fmtPct()` 等（**CN 约定: 红涨绿跌**）
  - `echarts.ts` — 主题 token，跟 CSS 变量联动
- `style.css` — 顶部 `:root` 有完整 dark/light 调色板，深色默认；`html.light` 切浅色

**前端要改主题色**只改 `style.css` 那 20 行 CSS 变量即可，组件不需要动。

---

## 8. 进行中的活: validation50

这是接手时**最需要继续**的工作。

**目标**: 把 4 份 deep research 里提到的 50 个策略**统一框架**回测一遍，给出 "robust / decayed / surprise+ / surprise-" 的分类结论。

### 已经完成
- [validation50/FEATURE_LIST.md](validation50/FEATURE_LIST.md) — 50 行表格，分 7 类（trend / mean reversion / sentiment / macro / cross-asset / seasonal / allocation），每行带 `id`、`rule`、`data_needs`、`lit_verdict`、`status`、`our_verdict` 列
- [validation50/data_acq.py](validation50/data_acq.py) — FRED + 18 ETF 数据采集，**已跑过**，数据都在缓存里
- [validation50/runner.py](validation50/runner.py) — 跑批框架，约定每个策略导出 `compute() -> Result`，runner 负责画 4 panel PNG + 写 markdown + 汇总成 scorecard

### 还没做
- `validation50/strategies/` **空目录**。需要给 50 个 id 每个写一个 `.py`，每个文件大概 30–50 行，结构看 [backend/app/signals/qdii_premium.py](backend/app/signals/qdii_premium.py) 类似但更简单（只要回测，不要 narrative）
- `validation50/strategies/_template.py` 还没写，建议接手时先写一个模板
- `outputs/scorecard.md` 最终交付物 — 等 50 个 strategy 跑完之后聚合

### 推荐接手顺序
1. 先写 `validation50/strategies/_template.py` 一个模板
2. 实现头 5 个最容易的（`spy_sma200_timing`、`vix_above_30_buy_spy`、`vix_above_40_buy_spy`、`pf_60_40`、`sell_in_may`）验证 runner 框架是否合理
3. 调整 runner（如有问题），再写剩下 45 个
4. 跑完 `python validation50/runner.py`，看 `outputs/scorecard.md`
5. 写一段「surprise narrative」总结哪些 idea 出乎意料、为什么

### 数据约束（哪些行还跑不通）
- **AAII bearish %** — 没自动 fetch，需要从 aaii.com 手动下 CSV 丢到 `validation50/data_drops/aaii_sentiment.csv`
- **CBOE Put/Call** — 同上
- **Shiller CAPE** — `data_acq.py` 里有 scrape 代码但不一定每次都成功
- **AH 溢价指数** — akshare 端点失效，已知问题

---

## 9. 关键决策 + 为什么

| 决策 | 为什么这样 | 不要回滚 |
|---|---|---|
| Vue 3 + ECharts，不是 React | 用户偏好 CN 金融界主流栈，且 ECharts 对热力图/K 线原生支持好 | 别换成 Recharts / Lightweight Charts，主题适配会重写 |
| 红涨绿跌（CN 约定） | 用户明确要求 Futu 风格 | 别换 Western 约定 |
| 后端用 Python 不是 Node | 所有 signal 计算依赖 pandas | 别 rewrite 成 TS |
| `finance-data-api` 目录名带连字符 | 用户最初命名要求 | 别改成下划线，sys.path 那段是有意保留 |
| 旧版 matplotlib pipeline 归档到 `legacy/` 而非删除 | 离线 PNG 报告偶尔还有用 | 不要删 |
| FRED 用 CSV 端点而非官方 API key | 不需要注册、URL 稳定 | 别引入 fredapi 依赖 |

---

## 10. 文件地图

```
finance-idea/
├── README.md                       项目自述（公开版）
├── handover.md                     ← 本文件
├── 要做什么提示词.md                 用户最早的需求
├── 金融数据结构调研.md               数据源调研
├── run_all.py / run_dev.sh         一键启动
├── requirements.txt
│
├── finance-data-api/               数据层
│   ├── universe.py    storage.py   fetchers.py   refresh.py
│   └── data/                       parquet 缓存（不进 git）
│
├── backend/                        FastAPI 服务
│   └── app/
│       ├── main.py                 入口、CORS、SPA static mount
│       ├── deps.py                 Storage 单例 + sys.path 注入
│       ├── schemas.py              **所有 Pydantic 类型，前端契约源**
│       ├── api/                    路由 (dashboard, ideas, series, meta)
│       └── signals/                10 个 idea 的 compute() 函数
│           ├── _base.py            SignalBundle 数据类 + 公共 helpers
│           └── qdii_premium.py … 等 10 个
│
├── frontend/                       Vue 3 SPA
│   ├── package.json   vite.config.ts   tailwind.config.js
│   └── src/
│       ├── App.vue   main.ts   router.ts   style.css
│       ├── lib/api.ts           ← TS 类型必须和 schemas.py 同步
│       ├── lib/format.ts        ← CN 红涨绿跌 helpers
│       ├── lib/echarts.ts       ← ECharts 主题
│       ├── stores/              Pinia
│       ├── components/          原子组件（Sparkline、SignalCard、…）
│       └── views/               DashboardView、IdeaDetailView
│
├── validation50/                   🚧 50 策略验证（进行中）
│   ├── FEATURE_LIST.md             50 行清单，唯一真理源
│   ├── data_acq.py                 已跑过，数据已落地
│   ├── runner.py                   跑批 + 绘图 + scorecard 框架
│   ├── strategies/                 ← **空，需要填 50 个 .py**
│   └── outputs/                    每策略一个子目录
│
├── deepresearch-result/            4 份 deep research 报告
│   └── *.md (4 files, 205KB total)
│
├── legacy/ideas_v1/                旧版 matplotlib pipeline（不删）
│
└── other-finance-package/          17 个对标的开源 agent 仓库（克隆）
                                    (TradingAgents, FinRL, qlib, ai-hedge-fund, …)
```

`quant_by_leancli/` 是**平行项目**（基于 LEAN CLI 的另一套量化框架），跟当前 finance-idea 解耦，本次交接不涉及。

---

## 11. 已知问题 & 待研究

- [ ] `akshare.bond_china_yield()` 报 "No tables found"，国债收益率拉不到，FRED 的 DGS10/DGS3MO 暂时顶上
- [ ] `akshare.stock_hk_ah_premium_index()` 不存在 / 失败，AH 溢价历史信号 (idea07) 永久 fallback 到 "data unavailable"
- [ ] 前端首次加载 `/api/ideas/{id}` 比较慢（每次调用都重算 compute），可以加 LRU cache 或者 daily snapshot table。当前**未做**，对单用户场景够用
- [ ] 净值曲线起算日期不统一（不同策略的 underlying 起始日不同），scorecard 里直接比 CAGR 会失真——需要在 runner 里加 "对齐到公共起始日" 的统一处理
- [ ] CBOE / AAII / CAPE 三个 scrape 链路偶发失败，没设置告警

---

## 12. 联系点

- 数据源:
  - akshare (Sina + EM) — `pip install akshare`，无 key
  - yfinance — 无 key，但 Yahoo 偶尔限流
  - FRED — public CSV，URL: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
- 用户偏好（记忆）:
  - 中文沟通，技术内容可中英混合
  - 偏好用户优先 / Futu 风格
  - 不要无故添加 emoji
  - 验证完才说 done，不要 over-claim

---

**接手后的最小验证**:

```bash
./run_dev.sh                           # 起前后端
curl http://127.0.0.1:8000/api/dashboard | jq '.signals[0]'
# 在浏览器看 http://localhost:5173 显示 10 张信号卡
```

跑得通就说明上层完好，可以专心做 validation50 的剩余活儿。
