# Formulaciones candidatas (Fase 5)

## A. Selección contextual de K por corte (recomendada, la actual)

Es lo que el código ya implementa y la auditoría confirma: **bandido
combinatorio contextual**, no MDP secuencial.

- Estado: features del corte (solo pasado) + máscara + presupuesto.
- Acciones: conjunto de K municipios distintos (secuencialización en K
  pasos por compatibilidad con PPO; el orden no afecta el retorno).
- Transición: solo máscara/presupuesto dentro del episodio; cortes
  independientes entre episodios; sismicidad exógena.
- Recompensa: media observada de actividad M≥3 del mes siguiente en los
  elegidos. Sin ponderar (DANE retrospectivo), sin costes (no
  observados), sin efectos causales (no existen).
- Horizonte: 1 (un mes). Restricción: K fijo entrenado; cobertura
  futura completa o exclusión del corte.
- Fuga evitada: recompensa solo terminal; preprocesado y rankings solo
  train; política congelada antes de val/test.
- Baselines: aleatorio, top-K estático (solo train), ranker binario
  (solo train), oráculo ex post solo como cota.
- Métrica de éxito: recompensa media en cortes posteriores + pareadas
  contra el estático con IC por bloques. Supuestos reales: presupuesto
  de seguimiento limitado, decisión mensual repetida. Hipótesis: que el
  contexto pague sobre la marginal (los datos dicen que paga poco).

## B. Secuencial con presupuesto persistente (hipótesis, NO oficial)

Idea: el presupuesto de visitas persiste entre meses (p. ej. cada
municipio debe revisarse al menos cada N meses, o hay coste de
desplazamiento entre cortes consecutivos). Entonces la acción de hoy
sí condiciona el estado de mañana y el RL secuencial tendría objeto.

- Estado A + historial de visitas y presupuesto remanente global.
- Acciones: K por mes con restricción de revisita/coste.
- Recompensa: misma actividad observada menos penalización operativa
  (coste de desplazamiento) con coeficiente fijado **antes** de ver
  resultados.
- Horizonte: varios meses; validación por bloques temporales.
- Baselines nuevos exigidos: greedy con la misma restricción y oráculo
  combinatorio del mismo objetivo (no heredar el top-K aditivo).
- **Falta la restricción operativa real**: el proyecto no define
  capacidad de visitas, frecuencias obligatorias ni costes. Sin ese
  dato de autoridad, B es hipótesis de diseño, no recompensa oficial.
  **Se solicita confirmación humana** (equipo + enunciado del reto)
  antes de implementarla.

## Recomendación

Mantener A como formulación oficial (defendible, medida, honesta sobre
su techo). Probar B solo si aparece una restricción operativa real con
fuente. No llamar "RL superior" a resolver mejor el mismo objetivo
aditivo por ser más complejo: hoy el ganador honesto es el estático.
