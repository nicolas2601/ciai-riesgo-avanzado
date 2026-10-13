# RL evaluation (val)

| policy | mean | std | min | max |
|---|---|---|---|---|
| agent | 0.5231 | 0.1476 | 0.4 | 0.8 |
| random | 0.0092 | 0.0169 | 0.0 | 0.04 |
| static | 0.5231 | 0.1476 | 0.4 | 0.8 |
| ranker | 0.4462 | 0.0843 | 0.4 | 0.6 |
| oracle_reference | 0.8308 | - | - | - |

Cutoffs: 13 (2024-05 to 2025-05); 13 with >= 1 positive municipality.
Agent minus static: 0.0 (std 0.0). A tiny gap with large spread is variability, not superiority.
Reward = terminal mean of observed future activity (target_actividad_m3_mes_siguiente); not damage or official risk.
Ranker binary check (macro-F1 0.6377, positives 56): diagnostic only; the 3-class forest (medio recall 0 in test) is never used as an activity probability.
