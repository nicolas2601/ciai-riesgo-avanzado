# Auditoría de señal con train (Fase 2)

Todo calculado con cortes 2019-02…2024-04. Test y val solo aparecen en
una correlación de generalización del ranking (no para elegir nada).

## Prevalencia y estabilidad (por municipio)

- 87 municipios: 1 siempre activo en train (68418, 63/63), 44 nunca
  activos, resto intermitente. Positivos por corte: media 4,06,
  std 1,31, rango 1-7.
- Estabilidad de la tasa de actividad por municipio (correlación entre
  periodos): mitad1 vs mitad2 de train 0,97; train vs val 0,96; train
  vs test 0,90. **El ranking marginal generaliza**: el techo de lo
  estático es alto y persistente.
- Recompensa esperada del conjunto constante en train: 0,5206
  (≈ val observado 0,5231). Aportes: 68418 el 38 %, 68895 el 34 %,
  68872/68235/68255 entre 6 % y 11 % cada uno. Dos municipios explican
  casi tres cuartas partes del retorno.

## Features: distribución y asociación con el mes siguiente

- 32 features, todas numéricas; solo `frac_gt300` constante (0) y
  `hay_eventos_mes` binaria. Ninguna categórica: SMOTE/LR sin problema
  de tipo (ya usado en el benchmark supervisado).
- Asociación (media en filas con actividad futura − media sin ella):
  dominan conteos 12m/3m/mes, conteos M≥3/M≥4 y magnitudes máximas,
  todas con **signo estable entre mitades de train**. Señal contextual
  existe en los datos.
- Excepciones con signo inestable: `n_eventos_departamento_mes`
  (efecto global del mes, idéntico para los 87 municipios del corte:
  inútil para rankear dentro del corte), `year_context` y `poblacion`
  (tendencias temporales/retrospectivas, confusoras, no señal
  municipal). No se eliminan (contrato), pero un encoder explícito
  puede aprender a ignorarlas; el MLP plano también podría, en teoría.
- Redundancia extrema entre conteos (correlaciones 0,91-0,99:
  `n_eventos_mes/3m/12m`, `n_m_ge_3_*`, `n_m_ge_mc_mes`). La matriz de
  2872 entradas contiene ~10 grados reales de variación por municipio.
  Esto abarata una solución constante: con features casi colineales y
  premio dominado por dos municipios, ignorar el estado cuesta poco.

## Cobertura y advertencias operacionales

- Cobertura completa en train usable (gate del entorno); 2026-09 sin
  futuro se excluye, nunca se cero-rellena.
- `poblacion` es proyección retrospectiva CNPV2018 (no disponibilidad
  as-of); el catálogo es revisado (backtest). Ninguna invalida el
  experimento, pero prohíben leerlo como operación en vivo.
- Detalle en `municipality_train_diagnostics.csv` (tasas por municipio
  y periodo) y `feature_diagnostics.csv` (medias, dispersión,
  asociación y estabilidad de signo por feature).

## Lectura para la Fase 4

Hay señal contextual real y estable (conteos), pero el 72 % del retorno
del top-K viene de dos municipios casi siempre activos y el ranking
marginal persiste (corr ≥ 0,90). El margen medible de lo contextual
sobre lo estático es estrecho: cualquier variante debe demostrar
ganancia pareada en val, no solo diversidad de picks.
