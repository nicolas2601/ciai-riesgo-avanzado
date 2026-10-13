# Brechas, ventajas e ideas (vista uts)

Consulta: 2026-10-13 ~07:00, hora Colombia. Cada hecho cita su fuente o una consulta ejecutada hoy; lo demas es INFERENCIA o SUPOSICION. Complementa `08` y `09` y la vista de uts2 en `11-vista-uts2-roles-y-sismologia.md`.

## 1. Hallazgo que puede romper el RL: el nido domina todo

HECHO (USGS, consulta de hoy, caja de Santander): de **1 058 eventos M >= 4,0 desde 2000, la profundidad mediana es 157 km, el 95 % esta entre 100 y 200 km y solo el 3 % es de menos de 70 km**. Los mayores eventos desde 1990 son todos del Nido de Bucaramanga: 2015-03-10 **M 6,2** a 155 km (2 km al NNO de Cepita); 2025-12-10 M 5,5 (164 km, cerca de Cepita); 2023-03-10 M 5,4 (160 km, Aratoca); y varios M 5,3 a 5,4 en 1990-2018 (Cepita, San Andres). La unica excepcion de la lista es 2022-02-23 M 5,5 a 50,7 km, lejos del nido (26 km al SO de Santa Rosa del Sur).

HECHO (literatura): el nido esta entre 150 y 170 km de profundidad, produce cerca del 60 % de los sismos que registra la RSNC y tiene un b-value estable cerca de 1,0 en tres decadas ([Perez-Forero et al. 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10754942/); [pronostico por ML en el nido, J. Seismology 2026](https://link.springer.com/article/10.1007/s10950-026-10364-w)). Sus eventos se sienten a cientos de km ([NoSAm Nest GMM, 2024](https://link.springer.com/article/10.1007/s10518-024-01898-w)).

INFERENCIA (a verificar a las 8:00 con el catalogo SGC): si el objetivo o la recompensa cuentan sismos **por municipio del epicentro**, casi toda la actividad cae en pocos municipios del nido (Los Santos, Cepita, Aratoca, San Andres y vecinos) y casi nada en el resto. El ranking de municipios seria **casi constante en el tiempo** y un agente de refuerzo aprenderia a elegir siempre los mismos: un RL trivial que el jurado detecta.

**Gate de degeneracion (nuevo, a las 8:30):** medir con el dataset cuanta variacion hay en el top-K entre cortes. Si el mismo top-K aparece en mas del 90 % de los cortes, hay que rediseñar recompensa y estado (seccion 4) antes de entrenar.

## 2. Brechas que podemos aprovechar

### 2.1 Brechas de la competencia y de la rubrica (INFERENCIA)
- La rubrica de Avanzado reparte **60 de 100 puntos fuera del modelo**: validacion e incertidumbre 10, flujo y trazabilidad 15, impacto e innovacion 20, presentacion 20 (y el desempate es impacto e innovacion). Un equipo que solo entrena un PPO sin contar la historia pierde ahi.
- Con 9 equipos en Avanzado (HECHO, pagina oficial), lo probable es ver RL envuelto sobre un clasificador. Nuestro diferencial es honestidad metodologica (validacion cronologica, lineas base, abstencion, limites declarados) y una demo viva.
- La literatura de ML sismico reconoce el **problema de fuga por particiones no secuenciales** y que las redes neuronales no superan consistentemente a ETAS ([EarthquakeNPP, 2024](https://arxiv.org/pdf/2410.08226); [Dervisi et al., 2025](https://link.springer.com/article/10.1186/s40623-025-02241-6)): decir "validamos en orden temporal y comparamos con lineas base fuertes" es exactamente lo que valora un jurado tecnico.

### 2.2 Brechas de los datos (HECHO donde se indica)
- **Completitud no estacionaria**: el catalogo SGC tiene dos periodos con software y redes distintos (Earthworm/SEISAN hasta 2018-02; SeisComP3 desde 2018-03; HECHO, pagina del catalogo). Los conteos cambian por deteccion, no solo por sismicidad: se trabaja con un **umbral de magnitud por encima de la completitud** y se prueba el cambio de 2018 como analisis de robustez.
- **Epicentro no es sacudida**: un M 4,8 a 160 km se siente en toda la region, mientras el municipio del epicentro es solo un punto. Mejor variable: **sacudida esperada por municipio** (funcion de magnitud, profundidad y distancia). Existen modelos propios del nido ([NoSAm Nest GMM](https://link.springer.com/article/10.1007/s10518-024-01898-w), [GMPE para sismos profundos de subduccion en Colombia](https://www.researchgate.net/publication/326234825)); en 4 h usamos una atenuacion simple, declarada como aproximacion.
- **Profundidad**: ">70 km" no equivale a "intermedio" (incluye profundidades mayores a 300 km). Se usan bandas.
- **Fuentes**: DANE por anio es retrospectivo; la Gobernacion solo desde 2018-05 (HECHO, verificado).

### 2.3 Brechas de la literatura (oportunidad de innovacion, con cautela)
- En nuestra busqueda de hoy hay **poco trabajo de RL aplicado a priorizar monitoreo o inspeccion sismica**: lo mas cercano es RL para riesgo de edificios bajo amenaza y para puentes envejecidos (2024), y un marco de inspeccion post-sismica como problema de orientacion multiperiodo sin RL ([TRE 2024](https://par.nsf.gov/servlets/purl/10526238)). Decirlo asi: "en nuestra revision encontramos pocos trabajos", sin afirmar que no existen.
- El **pronostico en el nido por ML** es tema vigente (J. Seismology 2026): nos posiciona en el estado del arte sin prometer predecir terremotos.

## 3. Ideas creativas, de mayor a menor valor y con su costo

| # | Idea | Por que suma | Costo en 4 h | Riesgo |
|---|---|---|---|---|
| 1 | **Maquina del tiempo** en la web: deslizador de meses que muestra que habria priorizado el agente antes del **M 6,2 de Cepita (2015-03-10)**, el M 5,4 de Aratoca (2023) y el M 5,5 de 2025, y que paso despues | Impacto e innovacion (20) y presentacion (20); es memorable y verificable con USGS | Medio (la web ya lee `priorizacion.json`) | Pocos eventos grandes: contarlo con honestidad |
| 2 | **Sacudida esperada** en vez de conteo por epicentro, ponderada por poblacion DANE | Evita el RL trivial; mas cerca de lo que importa; usa literatura reciente | Medio | Aproximacion: se declara y se hace sensibilidad |
| 3 | **Dos regimenes**: nido (profundo, frecuente, sentido a distancia) y cortical (somero, raro, local) como familias de variables y como lectura de los grupos del bloque Medio | Hace interpretable el clustering ("municipios del nido, corticales, lejanos") | Bajo | Pocos eventos corticales: soporte a verificar |
| 4 | **Robustez al cambio de red de 2018**: entrenar con un periodo, evaluar en el otro y comparar con y sin umbral de completitud | Innovacion de datos, util para trazabilidad | Bajo | Ninguno serio |
| 5 | **Incertidumbre honesta**: conjunto de semillas y bootstrap para el agente; prediccion conformal opcional en el Basico; el sistema "se abstiene" si el ranking es inestable | Validacion e incertidumbre (10) | Bajo a medio | Tiempo |
| 6 | **Presupuesto K interactivo**: la web deja mover K y el mes y recalcula comparacion contra lineas base | Demo viva, trabajo de decision | Medio | Necesita precomputar o un endpoint |
| 7 | **URL publica de la demo** (Vercel o similar, estatica) para que el jurado la abra en su celular | Impacto, factor "wow", sin riesgo de internet en sala si se lleva respaldo local | Bajo | Respaldo local obligatorio |
| 8 | **Revisita**: restriccion operativa explicita (cada zona debe revisarse al menos cada N meses) que vuelve genuinamente secuencial el RL | Da sentido al refuerzo si el ranking es casi estatico | Medio | uts2 la acepta solo con coeficiente fijado de antemano y como analisis separado |

## 4. Rediseño del RL si el gate de degeneracion falla

1. Recompensa terminal = **sacudida esperada observada** en los municipios elegidos (calculada con los eventos reales del mes siguiente) × exposicion (poblacion DANE), no conteo por epicentro.
2. Si aun asi el top-K es casi constante, el agente aprendera una politica casi constante: se **declara** y se aprovecha la idea 8 (revisita) como segundo experimento para que el aprendizaje sea realmente secuencial.
3. Ante cualquier resultado, lineas base honestas: top-K estatico por sacudida historica (que puede igualar al agente: se dice), aleatorio, ranker supervisado y oraculo.
4. La conclusion que se defiende no es "RL gana", sino "aprendimos una politica de priorizacion con datos oficiales, la validamos en orden temporal y sabemos cuando no aporta sobre una regla simple".

## 5. Presentacion como producto: la web es el pitch

No hay diapositivas: la web tiene un **modo presentacion** (ruta `/presentacion`, flechas y pantalla completa) con las secciones del pitch: problema, datos, modelos, resultados (con la maquina del tiempo), impacto, limites y equipo. Los 10 minutos se reparten entre los tres: Zabdiel explica el RL y la validacion, Nico los datos y el flujo, Julian la demo y el impacto. Respaldo: la misma web corriendo local con los JSON ya generados.

## Fuentes

- [Perez-Forero et al. 2023, Sci Rep: delaminacion litosferica en el Nido de Bucaramanga](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10754942/)
- [Hacia el pronostico de sismos en el Nido de Bucaramanga con ML, J. Seismology 2026](https://link.springer.com/article/10.1007/s10950-026-10364-w)
- [NoSAm Nest GMM, Bull. Earthquake Eng. 2024](https://link.springer.com/article/10.1007/s10518-024-01898-w)
- [GMPE para sismos profundos de subduccion en Colombia](https://www.researchgate.net/publication/326234825)
- [Dervisi et al. 2025, EPS: ML de corto plazo frente a ETAS](https://link.springer.com/article/10.1186/s40623-025-02241-6)
- [EarthquakeNPP: benchmark de procesos puntuales neuronales](https://arxiv.org/pdf/2410.08226)
- [Inspeccion post-sismica como orientacion multiperiodo, TRE 2024](https://par.nsf.gov/servlets/purl/10526238)
- USGS FDSN (consulta de 2026-10-13, caja 5,7 a 8,2 N y -74,7 a -72,4 O): https://earthquake.usgs.gov/fdsnws/event/1/
- Pagina oficial del reto y catalogo SGC: `docs/research/source/` y `docs/research/08-enunciado-oficial.md`
