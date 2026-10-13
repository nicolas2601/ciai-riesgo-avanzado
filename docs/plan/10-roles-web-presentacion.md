# Roles, web React y presentacion (vista uts)

Version simple: **Zabdiel hace los modelos, Julian hace la web, Nico hace los datos y une todo.** Nadie lidera el mismo codigo que otro. La web **es** la presentacion: no hay diapositivas. Streamlit es solo respaldo si falta tiempo.

## 1. Quien hace que (una frase cada uno)

| Persona | Rol | Dueno de | Entrega |
|---|---|---|---|
| **Zabdiel** | Cabeza de ML | Modelo supervisado (Basico), agente de refuerzo (Avanzado), lineas base, validacion cronologica e incertidumbre | Carpeta `ml/` + los JSON `priorizacion.json` y `metricas.json` |
| **Julian** | Cabeza de la web | Web React: mapa, priorizacion, grupos, metricas, datos y **modo presentacion** | App en `app/web/` y URL de la demo |
| **Nico** | Datos, integracion y pruebas (apoya a los dos lados) | Descarga y union de datos, tabla unica y diccionario, modelo no supervisado (Medio), exportar los JSON de la web, repo reproducible, entregables y coordinacion | `data/`, `dataset.csv`, `diccionario`, `README` con un comando |

Regla de apoyo: Nico toma el bloque que se atrase (ML o web), pero **solo con aviso**, para no pisar el codigo de otro. Los que presentan son los tres.

## 2. Linea de tiempo por persona (hora Colombia)

| Hora | Nico (datos e integracion) | Zabdiel (ML) | Julian (web) |
|---|---|---|---|
| Antes de las 8:00 | Planificacion, entorno listo, ceremonia | Leer `08`, `09` y `12`; esqueleto del entorno de RL con datos de forma **marcados como NO oficiales** (solo para probar codigo) | Estructura de la web con la plantilla y el contrato de datos (seccion 4), sin datos oficiales |
| 8:00 a 9:00 | **Descarga SGC por HTTPS** y union de los dos periodos | **DANE** (xlsx) y Gobernacion (opcional); borrador del diccionario de variables | Mapa de Santander, navegacion y las vistas vacias leyendo los JSON de ejemplo |
| 9:00 a 9:30 | Tabla unica v0, gate de clases y **gate de degeneracion** | Revisa el gate con Nico; ajusta objetivo y recompensa | Vista de priorizacion y de grupos con datos de forma |
| 9:30 a 10:30 | Medio (grupos), diccionario, exporta `municipios.json` y `clusters.json` | Basico (supervisado), entorno y agente de RL, primeras corridas | Conecta los JSON reales conforme salen; vista de metricas |
| 10:30 a 11:15 | **Corte de respaldo:** si la web no tiene mapa, priorizacion y metricas con datos reales, Nico monta Streamlit con los mismos JSON (30 min) | Entrenamiento final, comparacion con lineas base, intervalos, importancia de variables; exporta `priorizacion.json` y `metricas.json` | Maquina del tiempo, modo presentacion, pulido |
| 11:15 a 11:30 | Congela datos y revisa trazabilidad | Congela modelos y metricas | Congela la web y la publica |
| 11:30 a 12:00 | **Entrega 12:00**: CSV, diccionario, fuente citada, codigo, modelos con metricas, demo | Revisa cifras contra lo que sale del codigo | Prueba la demo completa, respaldo local |
| 12:00 a 14:00 | Ensayo del pitch (10 min) | Ensayo | Ensayo; arregla lo que falle |

## 3. Cuellos de botella y plan B

- **Ruta critica:** los datos del SGC. Si a las 9:00 no hay tabla v0, Zabdiel y Julian siguen con datos de forma para probar codigo, pero nada de eso se entrega ni se muestra como resultado.
- **Si el SGC no se puede automatizar:** descargar el Excel por tramos desde la interfaz (la pagina oficial lo contempla). Si el sitio cae, USGS por API como respaldo de emergencia, declarado en la fuente.
- **Si el RL sale degenerado** (mismo top-K casi siempre): se rediseña la recompensa a sacudida esperada y/o revisita (`docs/research/12-brechas-e-ideas.md`, seccion 4).
- **Si se atrasa la web:** Streamlit con los mismos JSON, sin tocar el codigo de ML.

## 4. Contrato de datos de la web (sin API)

La web **lee archivos JSON** de `app/web/public/data/`. No hace falta API. Cada archivo lo genera el pipeline de Nico o de Zabdiel y los usa Julian. Los de ejemplo llevan `"ejemplo": true` y la web debe mostrar una marca visible "datos de ejemplo" mientras existan.

| Archivo | Quien lo genera | Contenido |
|---|---|---|
| `municipios.json` | Nico | `[{id, nombre, lat, lon, poblacion, cluster, nivel}]` (87 municipios; centroides ya en `app/api/data/municipios_santander.json`) |
| `serie_mensual.json` | Nico | por municipio y mes: eventos, magnitud maxima, sacudida esperada, nivel real y nivel predicho en los meses de prueba |
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

La demo en vivo (**requisito habilitante**) ejecuta el modelo entrenado: el boton "Ejecutar agente" corre la politica guardada (el checkpoint propio) sobre un corte elegido; respaldo: los resultados ya calculados en `priorizacion.json`.

## 7. Que se publica

Web estatica con los JSON, desplegada en un hosting gratuito para tener una **URL publica** que el jurado pueda abrir, mas copia local como respaldo (`bun run build` y `bun run preview`). El repositorio es privado: la URL de la demo no expone el codigo.
