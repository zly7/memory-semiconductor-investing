# Idea 01 — QDII (Nasdaq) ETF Premium as Contrarian Signal for QQQ

QDII funds used: QDII513100, QDII513300, QDII159941
Observations: 2743  range 2015-01-05 → 2026-05-25
Latest premium: 9.05% on 2026-05-25
Latest 90th-pct threshold: 4.53%   10th-pct: -1.29%

## Quintile conditional forward returns (QQQ)
| median_premium   |   fwd_5d_mean |   fwd_5d_winrate |   fwd_20d_mean |   fwd_20d_winrate |   n_samples |
|:-----------------|--------------:|-----------------:|---------------:|------------------:|------------:|
| q1 (lowest 20%)  |        0.0024 |           0.5894 |         0.0084 |            0.646  |         548 |
| q2               |        0.0025 |           0.5938 |         0.0155 |            0.7104 |         549 |
| q3               |        0.0032 |           0.5894 |         0.0149 |            0.702  |         548 |
| q4               |        0.0079 |           0.6569 |         0.0208 |            0.7161 |         548 |
| q5 (top 20%)     |        0.0038 |           0.5743 |         0.0193 |            0.6248 |         545 |

## Strategy stats (flatten when premium > rolling 90th pct)
| name                              |   n_days |   total |   cagr |   sharpe |   maxdd |
|:----------------------------------|---------:|--------:|-------:|---------:|--------:|
| QQQ buy & hold                    |     2743 |  6.0742 | 0.1969 |   0.9308 | -0.3562 |
| QQQ + QDII-premium flatten signal |     2743 |  3.0098 | 0.1361 |   0.8105 | -0.3675 |

Reading: if `fwd_5d_mean` falls as the quintile rises (q1 highest,
q5 lowest), the contrarian premise holds.