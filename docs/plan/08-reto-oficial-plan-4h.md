# Plan oficial del reto (4 h): sismos, tres bloques y aprendizaje por refuerzo

Reemplaza los supuestos de `00` a `07`. Fuente de verdad: el texto oficial guardado en `docs/research/source/` (pagina del evento, leida con Playwright el 2026-10-13 06:25) y su resumen citado en `docs/research/08-enunciado-oficial.md`. Cada hecho de este documento sale de ahi o de una consulta ejecutada hoy; lo demas va marcado INFERENCIA o SUPOSICION.

## 1. Que cambio (supuestos viejos contra realidad)

| Supuesto del plan anterior | Realidad oficial (HECHO) |
|---|---|
| Amenazas naturales varias, etiqueta UNGRD | Tema unico: **sismos**, datos del **catalogo sismico del SGC** (fuente principal) |
| Modelo GBDT supervisado + red PyTorch | Avanzado exige **aprendizaje por refuerzo**, "no se aceptan sustitutos"; ademas hay que cumplir Basico (supervisado) y Medio (no supervisado) |
| 5 h, hitos H0 a H7 | Desarrollo **8:00 a 12:00**, entrega **12:00 m.** (cerrada despues); presentacion 4:10 p. m. en 315A |
| API, MLflow, tunel, web desplegada | **No se requiere API.** Basta flujo reproducible y demostracion en vivo |
| 12 requisitos genericos | Rubrica Avanzado de 100 pts (seccion 6) y requisitos habilitantes |
| Datos abiertos varios | Fuente real oficial citada (URL, fecha, filtros); **nada sintetico como fuente principal** |

Equipo: **Syntax error II** (UNAB): Nicolas Moreno, Julian Arteaga, Zabdiel Quintero. Avanzado, desarrollo en 307B, presenta 315A a las 4:10 p. m. Compiten 9 equipos en Avanzado.

## 2. Reglas que mandan (citadas del sitio oficial)

- Equipos de 2 o 3; herramientas propias; IA generativa, APIs y preentrenados **solo como apoyo**: no reemplazan el modelo de ML de la categoria.
- Datos reales de fuente oficial; **tabla unica** (fila = observacion, columna = variable); sin duplicados, faltantes tratados, unidades y fechas homogeneas.
- **Avanzado: 20 variables minimas** (las derivadas cuentan si se justifican) y **diccionario de datos** (nombre, tipo, unidad, fuente, por que).
- **Variable objetivo bien definida y que no se calcule directamente de las variables de entrada.**
- El catalogo SGC tiene **dos consultas** con columnas distintas (1993-06 a 2018-02 y 2018-03 a hoy) que hay que unificar.
- **Habilitante**: modelo funcional entrenado por el equipo y demostrado **en vivo**, tipo de modelo obligatorio, datos reales citados y minimo de variables. Si falta, no es elegible a premio.
- Desempate: primero Impacto e innovacion, luego solidez tecnica del ML.
- Presentacion: 10 min (con demo) + 3 de preguntas; **exponen los integrantes**.

## 3. Problemas encontrados y como se atacan

| # | Problema | Evidencia | Mitigacion |
|---|---|---|---|
| P1 | Solo 4 h de desarrollo y 3 modelos (supervisado, no supervisado, RL) | Agenda oficial | Un solo dataset compartido; los tres bloques en paralelo desde la hora 2; recortes definidos (seccion 8) |
| P2 | El enlace oficial del catalogo SGC (`http://bdrsnc...`) **no responde** | Puerto 80 cerrado: timeout desde mi PC, el navegador y el VPS | **Funciona por HTTPS**: `https://bdrsnc.sgc.gov.co/paginas1/catalogo/` (200 en 0,26 s). Aviso a todos |
| P3 | La consulta del catalogo es un formulario POST con salida HTML y boton "Generar Excel" | `consulta_sismo.php` (periodo nuevo) y `consulsismo3.php` (periodo antiguo); campos `departamento` (valor `27-Santander`), `municipio`, `inicial`, `final`, rangos de magnitud, profundidad, RMS, gap | Consultar por **meses o anios** (lo recomienda el sitio); formato de fecha por descubrir en el navegador en el minuto 1; plan B: descargar Excel por tramos desde la interfaz |
| P4 | Dos periodos con software y columnas distintos (Earthworm/SEISAN contra SeisComP3) | Texto del catalogo | Mapeo de columnas en el dia 1 del dataset; guardar la version de origen como columna |
| P5 | Volumen: el Nido Sismico de Bucaramanga genera cientos de eventos al mes | Descripcion oficial del reto | Agregar por municipio y periodo; filtrar magnitud minima si el tamano lo exige |
| P6 | "Otra fuente oficial": hay que elegir y unirla | Pagina oficial | Seccion 4 |
| P7 | Los sismos en emergencias UNGRD son casi inexistentes | 4 eventos "SISMO" en Santander 2019-2025 (verificado) | No usar UNGRD como resultado; usar el dataset de la Gobernacion y la exposicion DANE |
| P8 | RL con recompensa fabricada o con fuga del futuro | Regla "objetivo no calculado de las entradas" | Recompensa **observada** del periodo siguiente, nunca en el estado; validacion cronologica (seccion 5) |
| P9 | Magnitudes de tipos distintos (Ml, Mw...) | Columna "Tipo Mag." del catalogo | Variable `tipo_magnitud`; usar la misma escala por analisis y declararlo |
| P10 | Ambiguedad: "cumplir Basico y Medio" frente a "Medio: unicamente no supervisado" | Lectura de uts2 | Entregar los tres bloques, cada uno con su tipo de modelo; preguntar al jurado en la apertura |
| P11 | Preparar datos antes de las 8:00 puede juzgarse injusto | "El reto inicia a las 8:00" | **Antes de las 8:00 solo se planifica y se prepara el entorno; los datos se descargan y procesan desde las 8:00.** Confirmar en la ceremonia |
| P12 | La infraestructura vieja (API, Cloudflare, MLflow, contrato v0.2, web React) ya no paga | Producto minimo oficial | Queda congelada (no se borra); el codigo reutilizable es el entorno `uv` y el diagrama de flujo |
| P13 | Prototipo/visualizacion territorial exigida en Medio | Rubrica Medio | Mapa por municipio (centroides ya en el repo: `app/api/data/municipios_santander.json`) o poligonos IGAC/DANE |
| P14 | 9 equipos de Avanzado; el desempate favorece Impacto e innovacion | Pagina oficial | Cuidar la narrativa de impacto desde la hora 1 (seccion 7) |

## 4. Fuentes: opciones y decision

Fuente principal (obligatoria): **SGC catalogo sismico**, `https://bdrsnc.sgc.gov.co/paginas1/catalogo/` (por HTTPS).

Segunda fuente oficial (integracion exigida), opciones:

| Opcion | Aporta | Verificado hoy | Costo | Decision |
|---|---|---|---|---|
| A. DANE proyecciones de poblacion municipal | Exposicion (poblacion por municipio y anio; cubre 1985-2042) | Descarga directa: `https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/PPED-AreaMun-2018-2042_VP.xlsx` y los de 1985-2017 (existen en la pagina) | Media (xlsx, 4 archivos por tramos de anios, unir por municipio) | **Si: segunda fuente oficial principal** (retrospectiva, se declara) |
| B. Gobernacion de Santander, eventos por desastres (datos.gov.co `a4bc-a9tq`) | Historial de impactos: viviendas, familias, heridos, fallecidos; incluye 21 eventos SISMO con `magnitud_richter` y epicentro | 1 628 filas **solo desde 2018-05**, 89 municipios, CC BY-SA 4.0, API Socrata sin cuenta | Baja | **Opcional**: no cubre 1993-2018, asi que solo sirve como variable de 2018 en adelante o para enriquecer la prueba; no como segunda fuente principal |
| C. SGC Datos Abiertos: inventario de movimientos en masa y zonas de amenaza sismica | Variables territoriales de amenaza | FeatureServer ArcGIS publico, p. ej. `https://services1.arcgis.com/Og2nrTKe5bptW02d/arcgis/rest/services/Inventario_de_movimientos_en_masa/FeatureServer` | Media | Si hay tiempo (variables territoriales para Medio) |
| D. IGAC altitud y suelos | Variable territorial | No verificado | Alta | No, salvo que sobre tiempo |
| E. USGS ComCat | Contraste de magnitudes | API programatica OK (62 eventos en 2020 en la caja de Santander; es un catalogo mas escaso que el del SGC) | Baja | Solo para contrastar, no como fuente principal |

No hace falta cuenta en ninguna de estas fuentes. (Si algun portal la pidiera, se usa el correo personal de Nico.)

## 5. Arquitectura: un dataset, tres bloques

```
SGC catalogo (2 periodos) --> unificar columnas --> variables sismicas por municipio y periodo
DANE poblacion  ----------\
Gobernacion impactos -----+--> tabla unica (CSV) + diccionario (>= 20 variables) --> orden temporal
SGC amenaza/movimientos --/                                                       |
                                    +---------------------+-----------------------+
                                    v                     v                       v
                            BASICO supervisado     MEDIO no supervisado     AVANZADO refuerzo
                            clase bajo/medio/alto  grupos de municipios     agente que prioriza zonas
                                    \                     |                       /
                                     +--- validacion temporal + incertidumbre ---+
                                                          v
                                      demostracion en vivo (cuaderno o Streamlit/Gradio) + pitch
```

Diagrama interactivo para la presentacion: `docs/flows/reto-oficial.html` (si se alcanza a generar; si no, usar el de arriba).

### Variable objetivo (opciones y decision)

| Opcion | Definicion | Ventaja | Riesgo |
|---|---|---|---|
| A (recomendada, **ventana mensual provisional**) | Nivel del municipio en el **mes siguiente** segun los umbrales de la guia oficial: bajo (sin sismos M >= 3,0), medio (3,0 a 3,9), alto (>= 4,0) | Umbrales de la propia guia; el objetivo es del futuro (no sale de las entradas); muchos mas episodios que con anios | **Gate a las 8:00**: si las clases, positivos o episodios completos no alcanzan, se pasa a ventana anual justificada (no automatico) |
| B | Cuantiles del conteo mensual de eventos | Clases balanceadas | Menos defendible que la guia |
| C | Energia liberada acumulada | Fisicamente motivada | Mas calculo y mas explicacion |

### Variables (>= 20, justificar cada una en el diccionario)

Sismicas por municipio y periodo: numero de eventos; eventos con M >= 2, >= 3, >= 4; magnitud maxima, media y desviacion; profundidad media y desviacion; fraccion de eventos con profundidad > 70 km (sismicidad intermedia); RMS medio; gap medio; fases medias; energia aproximada (suma de 10^(1,5 M)); dias desde el ultimo M >= 3; conteos de los 3, 6 y 12 meses previos; tendencia. Territoriales y de exposicion: poblacion (DANE); distancia al centroide del Nido de Bucaramanga; eventos y viviendas afectadas historicas (Gobernacion); movimientos en masa inventariados (SGC); el cluster del bloque Medio solo entra como variable si se ajusta unicamente con datos de entrenamiento (si no, es fuga y se omite). Con eso se superan las 20; las derivadas se justifican en el diccionario. Candidatos y gates detallados en `docs/research/09-rl-diseno.md` (seccion 4).

### Bloque Basico (supervisado)
Arbol, regresion logistica, KNN y random forest de scikit-learn; division **cronologica** (no aleatoria); matriz de confusion, precision, recall y F1; explicar donde se equivoca. Linea base: clase mayoritaria.

### Bloque Medio (no supervisado, unicamente)
KMeans, GMM y aglomerativo; elegir k con silueta y Davies-Bouldin; interpretar grupos con importancia de variables; mapa por municipio. Sin etiquetas en este bloque.

### Bloque Avanzado (refuerzo): decision tomada con la vista de uts2

Diseno adoptado (`docs/research/09-rl-diseno.md`, secciones 5 a 9): **un episodio = un corte de fecha**; el agente elige **K municipios distintos** (sin reemplazo, con mascara) antes de ver resultados del mes siguiente; **recompensa intermedia cero y recompensa terminal** = actividad sismica oficial observada en el mes siguiente en los municipios elegidos, ponderada por exposicion (poblacion DANE) si la union es valida, o sin ponderar si no. Algoritmo: **MaskablePPO (SB3-Contrib) en Gymnasium**, entrenado desde pesos aleatorios. Estado: variables (>= 20) de los municipios al corte, mascara de elegidos y presupuesto restante; nada del futuro en observacion ni en `info`.

Honestidad que se dice en la presentacion: con utilidad aditiva y sismicidad exogena, elegir K es optimizacion top-K contextual; el agente RL aprende una politica desde retornos, pero **no se afirma que RL sea necesario ni superior** al ranker supervisado. La salida es **priorizacion exploratoria de zonas para seguimiento**, no una alerta ni dano. Los efectos de la accion sobre la sismicidad no existen: no se inventa dinamica.

| Opcion evaluada | Estado |
|---|---|
| A. K picks por corte, recompensa terminal, MaskablePPO | **Adoptada (nucleo)** |
| B. Bandido contextual de un paso | Descartada: cuesta menos pero el jurado puede no verlo como refuerzo |
| C. Agente que recorre un mapa | Descartada: no usa bien los datos reales |
| D. Extension de **cobertura** (cada pick cubre municipios dentro de un radio R fijado de antemano; recompensa = actividad ponderada de la union, sin doble conteo) | **Solo analisis de sensibilidad separado**, si sobra tiempo; rompe la aditividad y da a RL una razon de ser, pero no se vende como area afectada ni beneficio de inspeccion |

Lineas base y evaluacion: aleatorio sin reemplazo con varias semillas, regla por magnitud **previa** (top-K), ranker supervisado del bloque Basico (mismo objetivo que la recompensa) y oraculo ex post solo como cota de evaluacion. Validacion: entrenamiento temprano, validacion posterior y prueba final intacta, **cronologicas por corte** (nunca filas al azar); el resultado de prueba se revela solo tras elegir los K; intervalos de diferencias pareadas por bloques de meses o anios, no por pasos de simulacion. Incertidumbre: retorno fuera de muestra con intervalos, estabilidad por semillas y sensibilidad a quitar poblacion, profundidad o proxies de calidad; explicacion: importancia por permutacion sobre la politica (no reutilizar el SHAP del arbol).

Declaraciones obligatorias (uts2): DANE ofrece proyecciones por anio (1985 a 2042) pero son **retrospectivas, no publicadas "as-of"**: se declara. El catalogo SGC de hoy puede traer correcciones posteriores: backtest con catalogo retrospectivo, no operacion as-of demostrada.

## 6. Rubrica Avanzado (100 pts) y evidencia

| Criterio | Pts | Evidencia que entregamos |
|---|---|---|
| Datos e integracion de fuentes | 15 | CSV unico, diccionario de >= 20 variables, script de union SGC + DANE + Gobernacion con las cifras de cuantos municipios y periodos cruzaron |
| Aprendizaje por refuerzo | 20 | Entorno, estados, acciones y recompensa documentados; agente entrenado en vivo o con checkpoint propio; curvas de aprendizaje |
| Validacion e incertidumbre | 10 | Division cronologica, evaluacion del agente contra lineas base, IC por semillas y bootstrap, importancia de variables |
| Flujo integrado y trazabilidad | 15 | Un comando reproduce todo (cuaderno o script), fuente con URL, fecha y filtros, versiones de librerias, semillas |
| Impacto e innovacion | 20 | Narrativa para decidir en Santander (donde mirar primero), supuestos, limitaciones y extensiones; ver seccion 7 |
| Presentacion | 20 | Pitch de 10 min con demo, exponen los tres, guion ensayado |

## 7. Impacto e innovacion (lo que decide un empate)

- Pregunta que respondemos: dado un presupuesto limitado de seguimiento, **a que municipios de Santander conviene mirar primero cada mes**, combinando actividad sismica real y exposicion de poblacion e impactos pasados.
- Innovacion defendible: refuerzo con presupuesto sobre datos oficiales reales; abstencion y lectura honesta de incertidumbre; comparacion contra lineas base y oraculo.
- Supuestos y limites a decir en voz alta: actividad no es dano; el entorno es historico (los municipios no cambian por la accion); pocas ventanas de prueba.
- Extensiones: mas fuentes (IGAC suelos, zonas de amenaza SGC), mas pasos de decision, recompensa con costos reales de inspeccion.

## 8. Cronograma del reto (hora Colombia)

| Hora | Quien | Que |
|---|---|---|
| Ahora a 7:00 | Nico | Planificacion y Engram; este documento |
| 7:00 a 8:00 | Todos | Ceremonia: confirmar reglas, pregunta sobre la ambiguedad P10, confirmar P11. Preparar el entorno (`uv sync`), sin tocar datos |
| 8:00 a 8:30 | Todos | Zona y objetivo (opcion A mensual, con el gate de clases). Nico: descarga SGC por HTTPS. Zabdiel: DANE y Gobernacion. Julian: esqueleto de la demo y del mapa |
| 8:30 a 9:30 | Nico y Zabdiel | Unificar catalogos, tabla unica, diccionario, CSV. Julian: demo contra un CSV de ejemplo |
| 9:30 a 10:30 | Todos | Zabdiel: entorno Gymnasium y MaskablePPO (con las pruebas de logica de 09). Nico: Basico y Medio. Julian: demo con datos reales, visualizacion y diapositivas |
| 10:30 a 11:30 | Todos | Entrenamiento y evaluacion del agente, validacion cronologica, incertidumbre, explicacion |
| 11:30 a 12:00 | Todos | Congelar: CSV, diccionario, codigo, metricas, demo; subir y verificar |
| 12:00 a 14:00 | Todos | Receso de entregas: guion del pitch y ensayo (10 min) |
| 14:00 en adelante | Todos | Pitch en 315A a las 16:10 |

Recortes si se atrasa (en este orden): visualizacion avanzada, segunda fuente C, algoritmos extra del Medio, graficas del pitch. **Nunca**: dataset con diccionario, agente RL entrenado y demostrable, validacion cronologica, demo en vivo.

## 9. Que queda del repo

Se conserva: entorno `uv`, diagramas Archify (el de flujo se reemplaza por el de la seccion 5), Engram uts, reglas de verificacion y revision cruzada. Se congela, sin borrar: API mock, contrato v0.2, web React, tuneles. Decision pendiente de Nico: demo en **Streamlit o Gradio** (mas rapido, mismo entorno Python; recomendado) frente a la web React ya preparada por Julian.
