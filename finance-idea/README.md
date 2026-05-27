# finance-idea v2

A **Futu-style market-sentiment dashboard**. 10 ideas backtested out-of-the-box,
each surfaced as a live signal you can refresh daily.

```
finance-idea/
├── finance-data-api/        # 数据治理：universe + parquet 缓存 + fetchers + refresh CLI
├── backend/                 # FastAPI 服务 — /api/dashboard、/api/ideas/{id}、/api/ticker …
│   └── app/signals/         # 10 个 idea 的纯函数计算器
├── frontend/                # Vue 3 + Vite + Tailwind + ECharts SPA
├── legacy/                  # 旧版 matplotlib + 静态 HTML pipeline（保留作存档）
├── run_all.py               # refresh → 启动 dev stack
├── run_dev.sh               # 同时启动后端 + 前端
└── requirements.txt
```

## Quick start

```bash
# 1) one-time setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt fastapi 'uvicorn[standard]'
(cd frontend && npm install)

# 2) refresh data + boot dev stack
python run_all.py

# 3) open the UI
open http://localhost:5173
```

Subsequent days:
```bash
python finance-data-api/refresh.py     # cron-friendly
./run_dev.sh                            # already-installed venv
```

## Tech stack

- **Backend**: FastAPI + pandas + akshare/yfinance + parquet
- **Frontend**: Vue 3 + Vite + TypeScript + Tailwind + Pinia + ECharts
- **Convention**: 红涨 / 绿跌 (Chinese trader convention)

## API

`http://127.0.0.1:8000/docs` for the auto-generated OpenAPI explorer.

| Endpoint | Returns |
|---|---|
| `GET /api/dashboard` | 10 signal snapshots (value, delta, level, 60-day spark) |
| `GET /api/ideas`     | summary list |
| `GET /api/ideas/{id}`| full detail: time series, threshold bands, bucket heatmap, equity curves, markdown narrative |
| `GET /api/series/{key}` | raw OHLC for any cached asset |
| `GET /api/ticker`    | top-of-page index ticker tape |
| `GET /api/meta`      | per-key cache size & last refresh |

All responses are typed via Pydantic; matching TS types live in `frontend/src/lib/api.ts`.

## Data layer (unchanged from v1)

`finance-data-api/` provides:
- `universe.py` — 46 assets across 8 classes (US/CN/HK/QDII/Commodity/Rates/FX/Crypto)
- `storage.py` — Parquet cache (`data/{prices,nav,macro}/<key>.parquet`)
- `fetchers.py` — akshare Sina+EM, yfinance, with retry/fallback
- `refresh.py` — incremental CLI

```bash
python finance-data-api/refresh.py
python finance-data-api/refresh.py --only QQQ,VIX
python finance-data-api/refresh.py --class qdii_etf
```

## The 10 ideas

| id | 中文名 | 信号 |
|---|---|---|
| `qdii_premium`    | QDII纳指溢价 反指    | 国内 QDII Nasdaq ETF 溢价中位数 |
| `qqq_ma200`       | QQQ 200日均线        | close / SMA200 比率 |
| `vix_extreme`     | VIX 极值反指         | VIX 点位 |
| `gold_copper`     | 金铜比 风险情绪      | 252d z-score |
| `dxy_em`          | 美元指数 6 月变动    | DXY 6 个月 % 变化 (EM 倾斜) |
| `yield_curve`     | 美债 10Y-3M          | 利差 pp |
| `ah_premium`      | AH 溢价              | 恒生 AH 溢价指数 (数据源待修复) |
| `northbound_flow` | 北向 20 日累计       | 净流入累计 (亿) |
| `iwm_spy`         | 小盘相对强度         | IWM/SPY z-score |
| `btc_gold`        | BTC/黄金 情绪温度    | ln(BTC/GLD) z-score |

每个 idea 的详细页包含：
1. 信号时间序列 + underlying asset 覆盖图 + 阈值带
2. 五分位 × 多 horizon 前向回报**热力图**
3. 策略 vs 基准**净值曲线** + CAGR/Sharpe/maxDD 表
4. Markdown 思路/结论说明

## Daily workflow

```bash
# 早上一行命令
python run_all.py
```

`run_all.py` 先 refresh 全部 universe，再启动 backend (FastAPI) + frontend (Vite)。
打开 `http://localhost:5173` 看新一天的信号读数。

把 refresh 放进 cron：
```cron
30 18 * * 1-5  cd /path/to/finance-idea && /path/to/.venv/bin/python finance-data-api/refresh.py
```

## Extending

- **加新资产**: 在 `finance-data-api/universe.py` 加 `Asset(...)`，下次 refresh 自动入库。
- **加新 idea**: 在 `backend/app/signals/` 增加 `<name>.py`，导出 `compute() -> SignalBundle`，注册到 `signals/__init__.py:REGISTRY`。前端会自动出现在 `/` 列表里。
- **改颜色/字体**: `frontend/src/style.css` 顶部的 CSS 变量。

## Legacy

`legacy/ideas_v1/` 保留了旧的 matplotlib 脚本 + `build_html.py` 静态 HTML 流程。
新版用浏览器交互式图表替代了所有 PNG。
