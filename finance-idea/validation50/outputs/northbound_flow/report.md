# northbound_flow — 北向资金 20日累计 → 沪深300
family: **sentiment** · literature verdict: **mixed**

### Result: **surprise+**

strat sharpe +0.40 vs bench +0.14 (Δ=+0.27); CAGR Δ=+5.28%; bucket monotonic ok=True

## strategy stats
| metric | value |
|---|---|
| n_days | 2245
| total | 0.6529
| cagr | 0.0580
| sharpe | 0.4046
| maxdd | -0.3700

## benchmark comparison
| benchmark       |   n_days |   total |   cagr |   sharpe |   maxdd |
|:----------------|---------:|--------:|-------:|---------:|--------:|
| csi300_buy_hold |     2245 |  0.0477 | 0.0052 |   0.1355 |  -0.467 |
| cash_3m         |     2245 |  0.1662 | 0.0174 |  14.408  |   0     |

## bucket forward-return table
| bkt   |     20d |     60d |    120d |
|:------|--------:|--------:|--------:|
| q1    | -0.0117 | -0.0057 | -0.0035 |
| q2    | -0.003  | -0.0106 | -0.0132 |
| q3    |  0.0091 |  0.0367 |  0.0063 |
| q4    |  0.0047 |  0.0219 |  0.0106 |
| q5    |  0.009  | -0.0136 |  0.0008 |

---
_notes_: bucket ρ=+0.50; long CSI300 when 20d cum > 0