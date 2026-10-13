# Roles, web React y presentacion (vista uts)

Version simple: **Zabdiel hace los modelos, Julian hace la web, Nico hace los datos y une todo.** Nadie lidera el mismo codigo que otro. La web **es** la presentacion: no hay diapositivas. Streamlit es solo respaldo si falta tiempo.

## 1. Quien hace que (una frase cada uno)

| Persona | Rol | Dueno de | Entrega |
|---|---|---|---|
| **Zabdiel** | Cabeza de ML | Modelo supervisado (Basico), agente de refuerzo (Avanzado), lineas base, validacion cronologica e incertidumbre | Carpeta `ml/` + los JSON `priorizacion.json` y `metricas.json` |
| **Julian** | Cabeza de la web | Web React: mapa, priorizacion, grupos, metricas, datos y **modo presentacion** | App en `app/web/` y URL de la demo |
| **Nico** | Datos, integracion y pruebas (apoya a los dos lados) | Descarga y union de datos, tabla unica y diccionario, modelo no supervisado (Medio), exportar los JSON de la web, repo reproducible, entregables y coordinacion | `data/`, `dataset.csv`, `diccionario`, `README` con un comando |

Regla de apoyo: Nico toma el bloque que se atrase (ML o web), pero **solo con aviso**, para no pisar el codigo de otro. Los que presentan son los tres.

## 2. Linea de tiempo por persona (hora Colombia), unificada con la vista de uts2

| Hora | Nico (datos e integracion) | Zabdiel (ML) | Julian (web) |
|---|---|---|---|
| Antes de las 8:00 | Planificacion, entorno listo, ceremonia | Leer `08`, `09`, `12`; esqueleto del entorno de RL con datos de forma **marcados NO oficiales** | Estructura de la web con la plantilla y el contrato de datos (seccion 4), sin datos oficiales |
| 8:00 a 8:10 | **Export minimo real del SGC** por HTTPS (URL, filtros, version); valida columnas y tiempos | Contrato de objetivo, horizonte y K; **DANE** si Nico sigue con el SGC | React local, estructura y banner "datos de ejemplo" |
| 8:10 a 8:30 | Descarga por tramos, une los dos periodos, une DANE, deduplica, registra procedencia | Entorno y politica sobre datos de forma marcados; lineas base y pruebas de mascara y recompensa | UI con datos de forma, nunca metricas que parezcan reales |
| **8:30** | **Handoff: dataset parcial de un periodo completo** (con version y cobertura) | Recibe y corre la primera vez | Valida lectura de JSON |
| 8:30 a 8:45 | Panel completo, >= 20 variables y diccionario; cortes y uniones validados | **Gate de clases, degeneracion y completitud**; congela ventanas y particiones con solo entrenamiento | Estados sin datos y errores |
| 8:45 a 9:15 | Pruebas temporales y de procedencia; exporta muestras reales; **Medio (grupos)** con las definiciones de Zabdiel | Basico supervisado y **primer agente entrenado** (o bloqueo concreto) | Mapa y grupos con datos reales |
| 9:15 a 10:00 | Integra las salidas al repositorio y a la web | Entrena y evalua el RL en validacion; semillas, configuracion, curvas; congela candidato | Modo presentacion: problema, fuentes, metodo, limites |
| **10:00** | **Primer flujo completo fuente a modelo a web, aunque el desempeno sea pobre** | | |
| 10:00 a 10:45 | Prueba de punta a punta con el mismo orden de variables | **Prueba final una sola vez** con la politica congelada; comparacion pareada y limites | Metricas y recorrido del agente; ningun numero a mano |
| 10:45 a 11:15 | **Decision del respaldo:** si React no funciona, Streamlit con los mismos JSON (30 min); si funciona, nada | Revisa retorno, soportes y mascaras; explica decisiones | Ensayo del pitch con los tres |
| 11:15 a 11:45 | Congela CSV, diccionario, codigo, modelos y paquete | Congela checkpoints y metricas | Congela build y modo presentacion; prueba local |
| **11:45** | **Entrega anticipada verificable** (quedan 15 min para fallos reales) | | |
| 11:45 a 12:00 | Confirma recepcion; **no se agregan funciones** | Verifica que el checkpoint corre | Prueba navegacion y respaldo local |
| 12:00 a 14:00 | Ensayo del pitch (10 min) | Ensayo | Ensayo y arreglos |

Reparto del Medio (diferencia entre las dos vistas, resuelta): uts2 propone que Zabdiel haga los tres bloques; uts propone que Nico haga el Medio. Se adopta que **Nico implementa el Medio bajo las definiciones de Zabdiel** (objetivo, particiones, escala) y Zabdiel lo revisa, **solo si el SGC, el panel y la exportacion ya pasaron su gate (8:45)**; si no, Zabdiel hace una version simple (KMeans) y Nico sigue con integracion. El codigo del Medio vive en `ml/medio/` (Nico, con revision de Zabdiel); no hay dos cabezas sobre `ml/` ni dos generadores del mismo JSON.

## 3. Cuellos de botella y plan B

- **Ruta critica:** los datos del SGC. Si a las 9:00 no hay tabla v0, Zabdiel y Julian siguen con datos de forma para probar codigo, pero nada de eso se entrega ni se muestra como resultado.
- **Si el SGC no se puede automatizar:** descargar el Excel por tramos desde la interfaz (la pagina oficial lo contempla). Si el sitio cae, USGS por API como respaldo de emergencia, declarado en la fuente.
- **Si el RL sale degenerado** (mismo top-K casi siempre, medido **solo con entrenamiento**): se compara contra el top-K estatico y se declara; opcionalmente se rediseña la recompensa a un proxy de sacudida estimada (`docs/research/12-brechas-e-ideas.md`, seccion 4).
- **Si se atrasa la web:** Streamlit con los mismos JSON, sin tocar el codigo de ML.

## 4. Contrato de datos de la web (sin API)

La web **lee archivos JSON** de `app/web/public/data/`. No hace falta API. Cada archivo lo genera el pipeline de Nico o de Zabdiel y los usa Julian. Los de ejemplo llevan `"ejemplo": true` y la web debe mostrar una marca visible "datos de ejemplo" mientras existan.

| Archivo | Quien lo genera | Contenido |
|---|---|---|
| `municipios.json` | Nico | `[{id, nombre, lat, lon, poblacion, cluster, nivel}]` (87 municipios; centroides ya en `app/api/data/municipios_santander.json`) |
| `serie_mensual.json` | Nico | por municipio y mes: eventos, magnitud maxima, proxy de sacudida estimada, nivel real y nivel predicho en los meses de prueba |
| `clusters.json` | Nico | perfil de cada grupo del Medio (promedios de variables clave, lectura en palabras, municipios) e importancia de variables |
| `priorizacion.json` | Zabdiel | por corte de prueba: K elegidos por el agente, por cada linea base y por el oraculo, y el resultado real (que paso despues) |
| `metricas.json` | Zabdiel | Basico (matriz de confusion, F1), curvas del RL, comparacion contra lineas base con intervalos, semillas |
| `diccionario.json` | Nico | variables: nombre, tipo, unidad, fuente, por que se incluye |
| `fuentes.json` | Nico | cada fuente con URL, fecha de descarga y filtros |

Cambiar un archivo se avisa al otro lado por Engram uts (`topic_key` `ciai/datos/contrato-json`).

## 5. Vistas de la web (React, con bun)

1. **Mapa**: municipios de Santander coloreados por nivel (Basico) o por grupo (Medio), con selector de mes; marca visible de que es priorizacion exploratoria, no alerta.
2. **Priorizacion**: K elegidos por el agente frente a las lineas base y al resultado real; control de K y de mes.
3. **Maquina del tiempo**: deslizador de meses con los sismos historicos de referencia (2015-03-10 en Cepita: M 6,2 segun USGS y M 6,6 segun el SGC, se muestran las dos; 2023 y 2025) y que habria priorizado el agente antes.
4. **Grupos**: lectura de los clusters del Medio en palabras.
5. **Metodologia y datos**: fuentes, diccionario, validacion cronologica, incertidumbre y limites, todo desde los JSON.
6. **`/presentacion`**: el pitch en modo pantalla completa, con flechas y las secciones: problema, datos, modelos, resultados, impacto, limites y equipo.

Reglas de UI: leer `skills/web-app/SKILL.md` y crear `app/web/DESIGN.md` antes de tocar estilos; el nivel nunca depende solo del color; mostrar siempre incertidumbre y limites; el mapa necesita `maplibre-gl` excluido del pre-empaquetado (ya esta en `vite.config.ts`).

## 6. Presentacion (10 min + 3 de preguntas)

| Minutos | Quien | Contenido |
|---|---|---|
| 0 a 1,5 | Julian | Problema y por que Santander (Nido de Bucaramanga, sismos recientes) |
| 1,5 a 3,5 | Nico | Datos y flujo: fuentes oficiales, union, 20+ variables, trazabilidad |
| 3,5 a 6,5 | Zabdiel | Los tres bloques y el agente: entorno, estados, acciones, recompensa y validacion cronologica |
| 6,5 a 9 | Julian (demo) con Zabdiel | Maquina del tiempo y priorizacion en vivo |
| 9 a 10 | Nico | Impacto, supuestos, limites y extensiones; cierre |

**Demo en vivo (requisito habilitante) y como se ejecuta el modelo.** Hay dos niveles y se rotulan distinto en pantalla:

1. **Reproduccion de resultados guardados**: la web lee `priorizacion.json` precalculado. Es un **replay, NO una inferencia nueva**; el boton se llama "Reproducir resultado guardado".
2. **Ejecucion en vivo del agente**: un **puente local** que corre el checkpoint propio. Opcion principal: un servicio local delgado de FastAPI (`uv run uvicorn ml.serve:app`, reutilizando la base de `app/api/`) con un endpoint que recibe un corte (y K) y devuelve los municipios elegidos y las lineas base; la web lo llama. Opcion de respaldo: una orden de consola (`uv run python -m ml.select --cutoff YYYY-MM`) que genera un paquete nuevo y la web lo importa. Se prueba **antes de las 10:45**.

K: el agente se entrena con un K fijo (por defecto K = 5). **Mover K a un valor no entrenado exige una politica nueva**; no se trunca la lista de otro K como si fuera el mismo agente.

La demo ante el jurado muestra el nivel 2 funcionando; si falla, se dice que es un replay y se muestra el nivel 1.

## 7. Que se publica

Web estatica con los JSON, desplegada en un hosting gratuito para tener una **URL publica** que el jurado pueda abrir, mas copia local como respaldo (`bun run build` y `bun run preview`). El repositorio es privado: la URL de la demo no expone el codigo.
