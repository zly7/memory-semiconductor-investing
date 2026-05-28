# csi300_drawdown_10pct — 沪深300 从 1Y 高点回撤 10% 买入
family: **mean_reversion** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.31 vs bench +0.35 (Δ=-0.04); CAGR Δ=-1.15%

## strategy stats
| metric | value |
|---|---|
| n_days | 5915
| total | 1.8852
| cagr | 0.0462
| sharpe | 0.3095
| maxdd | -0.7230

## benchmark comparison
| benchmark       |   n_days |   total |   cagr |   sharpe |   maxdd |
|:----------------|---------:|--------:|-------:|---------:|--------:|
| csi300_buy_hold |     5915 |  2.7283 | 0.0577 |   0.3511 |  -0.723 |
| cash_3m         |     5915 |  0.5052 | 0.0176 |  14.9031 |   0     |

## bucket forward-return table
|            |    20d |    60d |   120d |   252d |
|:-----------|-------:|-------:|-------:|-------:|
| flag=False | 0.0177 | 0.0585 | 0.1195 | 0.2265 |
| flag=True  | 0.0012 | 0.003  | 0.0176 | 0.0909 |

---
_notes_: trigger days: 3610