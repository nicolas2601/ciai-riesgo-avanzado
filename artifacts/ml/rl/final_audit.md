# Auditoría final de degeneración de la política RL

Fecha: 2026-10-13. Modelo `ppo_policy.zip` intacto (sin reentrenar, sin
cambiar hiperparámetros). Test usado una sola vez con política
congelada; nada de este informe re-selecciona ni ajusta nada.

## 1. Hallazgos comprobados (código + artefactos)

- **Observación** (`rl_env.py:125-132`): `[features(N×F) | máscara(N) |
  presupuesto(1)]`, float32, orden DIVIPOLA estable y validado por
  corte (líneas 105-110). El array `future` vive en la entrada del
  corte pero jamás se concatena ni aparece en `info` intermedio.
- **Recompensa solo terminal** (líneas 148-176): 0,0 en picks válidos
  no finales y `mean(future[seleccionados])` al completar K. Acciones
  inválidas: recompensa 0, sin gastar presupuesto, sin terminar.
  Verificado por tests y por el smoke (`intermediate == [0,0,0,0]`).
- **Sin fuga en construcción** (`build_cutoff_data`): preprocesador
  ajustado solo con filas de train; targets futuros solo en `future` y
  en el gate de cobertura (corte incompleto se excluye, nunca se
  rellena con cero; 2026-09 excluido y testeado). Nulos de clase y de
  actividad son el mismo conjunto (87 filas de 2026-09), así que el
  conjunto usable de RL coincide con el supervisado.
- **Muestreo de entrenamiento** (`train_ppo.py`, `rl_env.py:134-142`):
  corte uniforme al azar por episodio con RNG con semilla; 8192
  timesteps / 5 pasos ≈ 1638 episodios sobre 63 cortes de train
  (2019-02…2024-04, solo train). Máscaras en `learn` (MaskablePPO) y en
  `predict` durante la evaluación.
- **Top-K estático** (`baselines.py:47-59`): media de actividad por
  municipio sobre **solo** cortes de train, empates por posición
  (determinista). RL, estático, ranker y aleatorio usan K=5, la misma
  máscara de elegibilidad y la misma `selection_reward`.
- **No hay bug que invalide métricas.** Un filo real (ranking truncado
  a K antes de filtrar elegibles) lo detectó un test y se corrigió
  **antes** de entrenar y evaluar, devolviendo el orden completo.

## 2. La política constante (evidencia, no afirmación)

- El agente elige siempre `{68418, 68895, 68872, 68235, 68255}`: 1
  conjunto distinto en 13 cortes de val y 1 en 15 de test; coincide
  como **conjunto** con el top-K estático (el orden de picks difiere,
  la recompensa no). Diferencia pareada agente−estático: 0,0 en los 28
  cortes (13 empates + 15 empates).
- Frecuencia de actividad del conjunto (panel, tasa de meses activo):
  68418 = 100 % en train (63/63), val (13/13) y test (15/15); 68895 =
  89 %/77 %/47 %; resto 16-33 %. La recompensa está dominada por dos
  municipios: 68418 aporta 0,2 fijos cada mes y 68895 la mayor parte
  del resto (val 0,5231 ≈ 0,2 + 0,154 + resto).
- El ranker contextual sí varía (12 municipios distintos en val, 18 en
  test) y rinde menos (val 0,4462; test 0,3733). El oráculo (referencia
  no operativa) alcanza 0,83/0,79: hay señal futura, pero ninguna
  política operativa la captura.
- **Prueba de uso de estado** (modelo congelado, solo cortes de val,
  sin entrenar, sin tocar test): con features reales, con features a
  cero y con features de otro corte, los picks deterministas son el
  mismo conjunto en 13/13, 13/13 y 13/13. Muestreo estocástico del
  primer paso: 30/30 muestras caen dentro del conjunto en 3 cortes
  (masa cero en los otros 82 municipios). Las features sí cambian
  entre cortes (p. ej. `n_eventos_mes` de 68418 con std mensual 174),
  luego la constancia no es por estado constante: el agente aprendió
  preferencia fija por 5 índices de acción.

## 3. Robustez (descriptiva; no re-selecciona)

- Val: agente−ranker media +0,0769 (std 0,13); gana 4/13, empata 9,
  pierde 0. Test: +0,0933 (std 0,17); gana 6/15, empata 8, pierde 1.
- Bootstrap circular por bloques (bloque = 3 meses, B = 10000, semilla
  7, mismos índices para todas las series), IC 95 %:
  val agente [0,477, 0,549] = estático idéntico; ranker [0,415, 0,446];
  dif. agente−ranker [0,034, 0,106]. Test: agente [0,431, 0,479];
  ranker [0,361, 0,412]; dif. [0,029, 0,107].
- Límites: 13/15 meses no son observaciones independientes
  (autocorrelación sísmica); el bloque de 3 meses es un compromiso
  arbitrario y con tan pocos bloques el IC es orientativo. La ventaja
  sobre el ranker es pequeña frente a la dispersión y al gap al
  oráculo (0,31-0,32).

## 4. Conclusión científica

- **No existe evidencia de ventaja del RL.** El agente empata con una
  regla constante construida solo con train; la única "mejora" medible
  es sobre el ranker contextual (+0,08/+0,09 con IC que apenas excluye
  el cero en muestras de 13/15 meses) y sobre el azar (~0,01, umbral
  irrelevante). Con utilidad aditiva y sismicidad exógena, el problema
  es un top-K contextual y la política óptima aparente es casi
  constante: el PPO la encontró y ahí se quedó.
- Hipótesis no verificadas: si más timesteps/semillas saldrían de la
  constante; si features distintas (p. ej. sacudida estimada) harían
  útil lo contextual; si un K mayor o presupuestos variables cambiarían
  el cuadro. Ninguna se probó (prohibido reentrenar en esta auditoría).
- Experimento futuro que sí decidiría: replicar el entrenamiento con
  varias semillas y comparar la distribución de políticas resultantes
  contra el estático con IC pareado por bloques pre-registrado; en
  paralelo, un ranker mejorado (p. ej. con interacciones nido/corteza)
  como techo contextual honesto. Si ningún intento supera al estático
  fuera de muestra, la conclusión defendible es que el top-K estático
  es la política correcta para este target y ventana.
- Limitaciones estructurales: 91 meses usables, target raro (4,6 % de
  filas, mediana 4 municipios activos/mes), un municipio activo el
  100 % de los meses (techo de variabilidad), catálogo retrospectivo
  (backtest, no operación as-of) y población DANE retrospectiva (sin
  ponderación, por eso la recompensa es media simple).
- La recompensa mide actividad observada, no daño, riesgo oficial ni
  impacto evitado. Nada de este informe autoriza presentar la política
  como alerta ni como predicción operativa.
