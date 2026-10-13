# Auditoría de formulación matemática (Fase 1)

Referencias al código vigente en `ml/src/`. Nada de este documento
modifica la implementación de referencia.

## A. ¿MDP, bandido contextual o selección combinatoria contextual?

**Selección combinatoria contextual de un solo paso**, secuencializada
artificialmente en K pasos. Evidencia:

- `rl_env.py:142`: cada episodio muestrea un corte; `step()` solo
  actualiza `_selected` y el presupuesto. Las features del corte
  (`_entry["features"]`) quedan **congeladas** durante los K picks: la
  transición no depende del estado sísmico futuro ni la acción lo
  modifica (`docs/research/09-rl-diseno.md` lo declara: la acción no
  crea ni elimina sismos).
- `rl_env.py:164-166`: recompensa 0 en los K−1 primeros pasos y retorno
  terminal único. El orden de los picks no afecta la recompensa (media
  del conjunto). No hay preferencia temporal real (`gamma=1.0` es, de
  hecho, la parametrización correcta de un objetivo de conjunto).
- No hay dinámica entre episodios: el corte siguiente se muestrea
  independiente (`np_random.integers`), sin carry-over de presupuesto,
  estado sísmico ni coste.

Un MDP genuino exigiría que las acciones influyan en estados futuros;
aquí no ocurre ni dentro ni entre episodios. La etiqueta honesta es
**bandido combinatorio contextual** (contexto = features del corte,
brazo = conjunto de K municipios).

## B. ¿Consecuencias de las acciones sobre el estado futuro?

No, salvo consumir presupuesto dentro del episodio
(`rl_env.py:162-163`). La sismicidad es exógena; el siguiente corte es
independiente de los picks. Correcto físicamente, pero elimina la razón
de ser del RL secuencial: no hay nada que planificar en el tiempo.

## C. ¿Recompensa aditiva y separable?

Sí (`rl_env.py:166`, `baselines.py:34-36`):
`R = (1/K)·Σ y(z)`. Sin interacciones, sin cobertura geográfica
compartida, sin costes, sin rendimientos decrecientes. Cada municipio
aporta su actividad con independencia de los demás.

## D. ¿Razón matemática para que lo estático sea óptimo/competitivo?

Sí, doble:

1. Con recompensa aditiva y contexto, la política óptima es el top-K
   de `E[y(z)|contexto]`. Si el contexto aporta poca información sobre
   `y` más allá de la media marginal —y con un municipio activo el
   100 % de los 63 meses de train (68418)—, el top-K de medias
   marginales es óptimo o casi óptimo por construcción.
2. La varianza del estimador de ventaja contextual es alta (target raro,
   4,6 % de filas) mientras la constante tiene varianza baja: con 63
   cortes, la constante es el estimador favorito en sesgo-varianza.

## E. ¿Información temporal suficiente en la observación?

En principio sí: las features varían entre cortes (p. ej.
`n_eventos_mes` de 68418 con std mensual 174; recencias, conteos
departamentales). La auditoría de señal (Fase 2) cuantifica si esa
variación predice `y` del mes siguiente. Que la información exista no
implica que la arquitectura la use (ver F).

## F. ¿Puede la arquitectura representar lo contextual?

Estructuralmente sí, pero con sesgo fuerte hacia lo constante:

- Entrada plana de 87·32+87+1 = 2872 dimensiones a un MLP [64]. Para
  elegir el municipio `i` por su contexto, la red debe aprender desde
  cero la correspondencia "bloque de features [i·F,(i+1)·F) → logit i".
  Nada la impone: ni equivariancia por permutación, ni encoder
  compartido por municipio, ni atención.
- El óptimo local barato es un vector de sesgos fijos en la capa de
  logits (preferencia por 5 índices) con pesos de features ≈ 0. Con
  recompensa terminal dispersa y 5 pasos por episodio, el gradiente
  hacia ese óptimo domina al principio y PPO tiene pocos incentivos
  para salir: la constante ya rinde 0,52 en val.
- Valor estimado: el crítico comparte el MLP plano; con retornos casi
  constantes por corte, tampoco recibe señal para diferenciar estados.

## G. ¿Atribución de mérito por selección?

No. El retorno terminal idéntico se asigna a los 5 pasos (GAE con un
solo reward no nulo). Un pick brillante y uno mediocre reciben el mismo
crédito. Es el precio correcto de no filtrar futuro en pasos
intermedios, pero deja al aprendizaje sin señal por pick.

## H. ¿Cortes suficientes para las conclusiones?

Ajustado pero suficiente para lo que se afirma: 63 cortes de train
para aprender, 13+15 meses de evaluación para comparar medias con
dispersión reportada. Insuficiente para afirmar superioridad fina
(dif. agente−ranker +0,08 con std 0,13-0,17) o estabilidad entre
semillas de entrenamiento (una sola semilla entrenada). Los IC por
bloques de `final_audit.md` lo documentan.

## I. ¿Desajuste objetivo científico ↔ recompensa?

Parcial. El objetivo declarado (priorizar seguimiento combinando
actividad, exposición e impactos) se redujo —por instrucción explícita
y con razón—a media de actividad sin ponderar (DANE retrospectivo, sin
costes observados, sin efectos causales). La recompensa es defendible
como proxy, pero (a) la captura una constante, luego no mide
"capacidad contextual"; (b) ignora exposición, así que "mirar primero"
no distingue municipios grandes de pequeños. Mérito contextual real
exigiría o bien señal donde el contexto pague (Fase 2), o bien una
formulación donde lo secuencial importe (Fase 5, hipótesis).

## Distinción obligatoria

"La política ignora el estado **en este experimento**" (demostrado por
la sonda de perturbación: picks idénticos con features a cero o de
otro corte) no implica "ninguna política puede aprovechar el estado".
La Fase 4 prueba una arquitectura con correspondencia explícita
municipio→logit para decidirlo con datos, no con opiniones.
