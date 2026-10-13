# Informe final de investigación RL

## 1. Hallazgos demostrados

- El problema actual es un bandido combinatorio contextual, no un MDP
  secuencial (acciones sin efecto en estados futuros, recompensa
  aditiva separable, horizonte 1). `formulation_audit.md`.
- Señal contextual real pero estrecha: conteos asociados y estables;
  ranking marginal con corr train-val 0,96; 72 % del retorno del top-K
  en dos municipios casi siempre activos. `signal_audit.md` + CSVs.
- La política de referencia ignora el estado (sondas 13/13, entropía
  1,17, top-5 con 96,5 % de masa). `policy_diagnostics.md`.
- Experimentos controlados (9 entrenamientos CPU, mismos K/recompensa/
  cortes): V0 0,4974 ± 0,032 (val, 3 semillas), V1 0,4923 ± 0,027,
  V2 0,0257 ± 0,018; estático 0,5231; ranker 0,4462. V0/V1 convergen a
  la constante (train 0,05 → 0,48); V2 explora sin aprender (train
  plano, entropía ≈ máxima). `comparison_val.csv/.md`, `variant_cards.csv`.
- Ganador congelado (V0 semilla 7) en test único: 0,4667 = estático.
  **Ninguna variante supera al top-K estático en validación ni en
  test.** La diversidad de V2 no es mérito (recompensa de azar).

## 2. Hipótesis (no verificadas)

- Más timesteps/semillas podrían sacar a V0/V1 de la constante; nada lo
  sugiere (3/3 y 3/3 semillas colapsan al mismo conjunto).
- V2 podría aprender con más presupuesto, otro lr o preentrenamiento
  supervisado del encoder; con 8192 pasos no aprende nada medible.
- Una formulación secuencial con restricción operativa real (revisita,
  costes) daría objeto al RL; hoy esa restricción no existe.

## 3. Experimentos ejecutados

9 PPO (8192 pasos, CPU, semillas 7/21/42 × V0/V1/V2) con curvas de
Monitor; sondas de sensibilidad y entropía por política; bootstrap por
bloques (bloque 3, B=10000) del informe anterior; test confirmatorio
único del ganador. Referencia intacta en `artifacts/ml/rl/`.

## 4. Experimentos pendientes

Réplicas adicionales, barrido corto de lr para V2, encoder
preentrenado supervisado, ventana/orizonte alternativos (arrastran
objetivo y baselines), formulación B si llega restricción operativa.

## 5. Validación

Tabla en `comparison_val.md`. Regla de selección predefinida y
aplicada (media entre semillas → V0; mejor semilla 7 por media).
V0≈estático en la mejor semilla, por debajo en promedio (0,4974 vs
0,5231, std entre semillas 0,032).

## 6. Evaluación final

V0 semilla 7 en test: 0,4667 (estático 0,4667, ranker 0,3733). Caveat
declarado: el test ya estaba expuesto por la pista de referencia; no
se afirma firewall intacto. No se reajustó nada tras verlo.

## Limitaciones y preguntas para validación humana

- 63/13/15 cortes; target raro; un municipio activo el 100 % de los
  meses; catálogo y DANE retrospectivos (backtest, no operación).
- ¿Existe una restricción operativa real (capacidad, frecuencias,
  costes) que justifique la formulación B? (preguntar al equipo/reto).
- ¿Se acepta declarar el top-K estático como política recomendada si
  nada contextual lo supera? Es el resultado honesto actual.
- Incidente de test detectado y corregido: `proba_distribution`
  devuelve el objeto compartido mutado; leer `.logits` diferido da la
  última llamada. Era bug del test de equivarianza, no de la
  arquitectura (SB3 consume distribuciones de inmediato: entrenamiento
  y evaluación no afectados).
