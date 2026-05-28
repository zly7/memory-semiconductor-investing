# qdii_premium_reverse — QDII 纳指溢价反指 QQQ
family: **sentiment** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.86 vs bench +0.93 (Δ=-0.07); CAGR Δ=-5.91%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 2743
| total | 3.0781
| cagr | 0.1378
| sharpe | 0.8572
| maxdd | -0.3669

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| qqq_buy_hold |     2743 |  6.0742 | 0.1969 |   0.9308 | -0.3562 |
| bil_cash     |     2743 |  0.0327 | 0.003  |   0.4142 | -0.0068 |

## bucket forward-return table
| bkt   |     5d |    20d |    60d |
|:------|-------:|-------:|-------:|
| q1    | 0.0023 | 0.0082 | 0.0288 |
| q2    | 0.0027 | 0.0157 | 0.0386 |
| q3    | 0.0031 | 0.015  | 0.0376 |
| q4    | 0.0079 | 0.0208 | 0.0472 |
| q5    | 0.0039 | 0.0192 | 0.0741 |

---
_notes_: bucket ρ=+0.90 (expect ≤ 0 for contrarian)