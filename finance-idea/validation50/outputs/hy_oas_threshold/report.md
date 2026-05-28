# hy_oas_threshold — 高收益 OAS > 500bp 转防御
family: **macro** · literature verdict: **mixed**

### Result: **decayed**

strat sharpe +0.50 vs bench +0.73 (Δ=-0.23); CAGR Δ=-7.64%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 0.6381
| cagr | 0.0444
| sharpe | 0.4990
| maxdd | -0.2448

## benchmark comparison
| benchmark    |   n_days |   total |    cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|--------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 |  0.1207 |   0.7319 | -0.341  |
| ief_buy_hold |     2865 | -0.115  | -0.0107 |  -0.1292 | -0.2772 |

## bucket forward-return table
| bkt   |     20d |     60d |   120d |
|:------|--------:|--------:|-------:|
| q1    | -0.0041 | -0.0171 | 0.0195 |
| q2    |  0.0111 |  0.0321 | 0.042  |
| q3    |  0.0144 |  0.0525 | 0.1002 |
| q4    |  0.0303 |  0.0758 | 0.1249 |
| q5    |  0.0226 |  0.0604 | 0.1418 |

---
_notes_: BAMLH0A0HYM2 series: only 785 obs in cache (FRED truncates)