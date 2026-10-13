# Limitaciones del MVP de RL (resultados reales)

## Lectura honesta principal
El agente aprendió la política constante del top-K estático: en los 13
cortes de validación y los 15 de test elige siempre los mismos 5
municipios (68418, 68895, 68872, 68235, 68255) y su recompensa iguala al
baseline estático al decimal (val 0,5231; test 0,4667; diferencia 0,0).
**El RL no demuestra ventaja sobre la regla simple.** Es el escenario
del gate de degeneración previsto en el diseño: con utilidad aditiva y
sismicidad exógena, el problema equivale a un top-K contextual y el
agente converge a la constante fuerte.

## Soporte y variabilidad
- 63 cortes de entrenamiento, 13 de validación, 15 de test; K=5 fijo.
- Positivos por corte: media 4,3 (val). La recompensa media vive de
  2-7 municipios activos por mes; cada acierto mueve la media en 0,2.
- Aleatorio ≈ 0,01: el azar casi nunca acierta, así que "superar al azar"
  no es evidencia de mérito (el estático también lo supera por 0,5).
- Ranker contextual binario (macro-F1 0,64 en val y test) rinde 0,45/0,37:
  por debajo del estático. La clase media del bosque de 3 clases tuvo
  recall 0 en test y nunca se usó como probabilidad de actividad.

## Lo que la recompensa NO es
Media de actividad M>=3 observada en los elegidos. No es daño, riesgo
oficial, amenaza validada ni impacto causal evitado. Sin ponderación
poblacional (la DANE es retrospectiva). Catálogo retrospectivo:
backtest, no operación as-of.

## Estabilidad del aprendizaje
Un solo entrenamiento CPU (8.192 timesteps, 13,45 s, MLP [64],
gamma 1,0, semilla 7). Sin réplicas de semilla de entrenamiento ni
barrido: no se afirma estabilidad del aprendizaje, solo del resultado
evaluado con política congelada.

## Pendiente (no ejecutado)
Réplicas de entrenamiento, intervalos pareados por bloques, K distintos
(cada K exige política nueva), exportar priorización a la web (área de
Julián; se coordinará, no se sobrescribe nada), calibración e
incertidumbre del ranker.
