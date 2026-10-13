# RL evaluation (test)

| policy | mean | std | min | max |
|---|---|---|---|---|
| agent | 0.4667 | 0.1578 | 0.2 | 0.8 |
| random | 0.0133 | 0.0239 | 0.0 | 0.08 |
| static | 0.4667 | 0.1578 | 0.2 | 0.8 |
| ranker | 0.3733 | 0.1436 | 0.2 | 0.6 |
| oracle_reference | 0.7867 | - | - | - |

Cutoffs: 15 (2025-06 to 2026-08); 15 with >= 1 positive municipality.
Agent minus static: 0.0 (std 0.0). A tiny gap with large spread is variability, not superiority.
Reward = terminal mean of observed future activity (target_actividad_m3_mes_siguiente); not damage or official risk.
Ranker binary check (macro-F1 0.6385, positives 60): diagnostic only; the 3-class forest (medio recall 0 in test) is never used as an activity probability.
