# erp_dividend_yield — 股票风险溢价 (12M ret - 10Y) 极值
family: **macro** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.69 vs bench +0.73 (Δ=-0.04); CAGR Δ=-2.29%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.8887
| cagr | 0.0978
| sharpe | 0.6912
| maxdd | -0.3024

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |

## bucket forward-return table
| bkt   |    60d |   120d |   252d |
|:------|-------:|-------:|-------:|
| q1    | 0.0559 | 0.0864 | 0.2061 |
| q2    | 0.0426 | 0.0839 | 0.1639 |
| q3    | 0.0291 | 0.0572 | 0.1362 |
| q4    | 0.028  | 0.072  | 0.1515 |
| q5    | 0.0056 | 0.0226 | 0.0369 |

---
_notes_: ERP proxy = 12M SPY total return − DGS10/100