# Comparativa de experimentos (validación, 13 cortes 2024-05…2025-05)

| policy | val media (semillas) | semillas | conjuntos distintos | train última décima |
|---|---|---|---|---|
| V0_ref (MLP plano, ref) | 0,4974 ± 0,0321 | 0,5231 / 0,4615 / 0,5077 | 1,1,1 | 0,51 / 0,48 / 0,46 |
| V1_clip (idem, clip ±5) | 0,4923 ± 0,0267 | 0,4769 / 0,4769 / 0,5231 | 1,1,1 | 0,48 / 0,48 / 0,47 |
| V2_permuni (encoder/mpio) | 0,0257 ± 0,0178 | 0,0154 / 0,0462 / 0,0154 | 11,13,13 | 0,04 / 0,06 / 0,05 |
| static_topk (solo train) | 0,5231 | — | 1 | — |
| ranker_ctx (binario) | 0,4462 | — | 12 | — |
| random (5 semillas) | 0,0092 | — | — | — |
| oracle_ref (no operativo) | 0,8308 | — | — | — |

Selección (regla predefinida: mayor media de val entre semillas;
desempates por win-rate pareado y simplicidad): **V0_ref**
(0,4974 > 0,4923 > 0,0257). Congelado: **V0_ref semilla 7**
(val 0,5231). Test confirmatorio único: **0,4667 = estático**
(ranker 0,3733). El test ya estaba expuesto por la pista de
referencia: lectura confirmatoria, no firewall intacto.

Lectura: V0/V1 aprenden (recompensa train 0,05 → 0,48) hasta la
constante; el clip no cambia nada medible. V2 explora (entropía ≈
máx., 11-13 conjuntos, sondas 0/0) pero no aprende (train plano en
0,04-0,06, val ≈ azar). Diversidad sin recompensa no es mérito.
