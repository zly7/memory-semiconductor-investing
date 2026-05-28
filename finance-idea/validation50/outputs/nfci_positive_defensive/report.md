# nfci_positive_defensive — 芝加哥金融条件 > 0 转防御
family: **macro** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.74 vs bench +0.73 (Δ=+0.01); CAGR Δ=-0.35%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 2.5265
| cagr | 0.1172
| sharpe | 0.7448
| maxdd | -0.2737

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |    20d |    60d |   120d |
|:-----------|-------:|-------:|-------:|
| flag=False | 0.0089 | 0.0264 | 0.0545 |
| flag=True  | 0.0916 | 0.1855 | 0.2739 |

---
_notes_: NFCI > 0 → financial conditions tighter than average