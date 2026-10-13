# Diagnóstico de la política congelada (Fase 3)

Sin reentrenar la referencia. Solo inferencia sobre cortes de val y
artefactos existentes.

## Entropía y colapso de acciones

Distribución estocástica del primer paso y siguientes (máscaras
aplicadas, 13 cortes de val × 5 pasos):

- Entropía media 1,17 (máx. ln87 = 4,47; uniforme-sobre-5 = 1,61).
- Prob. media del top-1: 0,55; masa media del top-5: 96,5 %.
- Entropía por paso: 1,54 → 1,39 → 1,18 → 0,89 → 0,88 (parte de la
  caída es el enmascarado progresivo, pero el paso 0 ya concentra).
- Muestreo repetido del primer paso: 30/30 muestras dentro del mismo
  conjunto de 5 en 3 cortes (masa cero en otros 82 municipios).

Lectura: la política colapsó sobre 5 acciones. No es un artefacto de la
evaluación determinista: la propia distribución estocástica apenas
explora fuera del conjunto.

## Sensibilidad al estado

Sonda de perturbación (13 cortes de val, política congelada): picks
deterministas idénticos al conjunto constante con features reales
(13/13), con features a cero (13/13) y con features de otro corte
(13/13). Evidencia directa de que los logits no dependen del bloque de
features en este experimento.

## Selecciones por corte y recompensa de entrenamiento

- Artefactos: mismo conjunto en 28/28 cortes (val+test).
- Curva de aprendizaje de la referencia: no disponible sin reentrenar
  (prohibido en esta fase). La Fase 4 registra curvas de entropía y
  retorno con nuevas semillas de la misma configuración, como
  experimentos nuevos y separados.

Detalle por corte y paso en `policy_entropy.csv`.
