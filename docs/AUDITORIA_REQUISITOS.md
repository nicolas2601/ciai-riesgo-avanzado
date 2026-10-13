# Auditoría de requisitos oficiales

Fecha: 2026-10-13. Fuente de los requisitos: `docs/research/source/pagina-reto-2026-10-13.txt` y `docs/research/source/pagina-lineamientos.json` (texto oficial sin editar). Cada fila cita el archivo que la respalda. Estados: CUMPLE, PARCIAL, NO CUMPLE. La auditoría es estricta: lo que funciona pero con una salvedad seria queda PARCIAL.

## 1. Requisitos habilitantes (el jurado los verifica antes de calificar)

| Requisito | Estado | Evidencia | Observación honesta |
|---|---|---|---|
| Modelo de ML funcional entrenado por el equipo | CUMPLE | `artifacts/ml/selected_model.joblib`, `ml/medio/kmeans.joblib`, `artifacts/ml/rl/ppo_policy.zip`; código en `ml/src/` | Los tres modelos los entrenó el equipo con el código del repo |
| ...demostrado en vivo | PARCIAL | Web https://ciai.nicolasmoreno.site; API https://ciai-api.nicolasmoreno.site/docs; `docs/research/17-pruebas-e2e.md` | El supervisado y el Medio se demuestran en vivo en el despliegue. **El PPO no corre en el despliegue** (`agente: false`, "Ejecutar agente" deshabilitado). Hay que demostrarlo desde el repo local |
| Tipo de modelo obligatorio de la categoría (aprendizaje por refuerzo) | CUMPLE | `ml/src/rl_env.py`, `ml/src/train_ppo.py` (MaskablePPO) | Se entrena un agente de refuerzo real. Ver la salvedad del colapso en la rúbrica |
| Datos reales de fuente oficial citada con URL, fecha y filtros | CUMPLE | `data/sgc/provenance.json`, `docs/research/14-fuente-oficial-2.md`, `docs/DOCUMENTACION.md` sección 3 | URL, fecha 2026-10-13 y filtros por archivo del SGC. Licencia no declarada por las fuentes |
| Número mínimo de variables (20) | CUMPLE | `data/panel/metadata.json`: lista `features` con 32 variables; 45 columnas en total | Contado: 32 features >= 20. Una es constante (`frac_gt300`) y una es de año (`year_context`); aun descontándolas quedan 30 |
| Objetivo no calculado directamente de las entradas | PARCIAL | `docs/data/diccionario.md` (objetivos del mes siguiente); `artifacts/ml/audit_report.md` ("Columnas de futuro en X: ninguna") | `target_*` se calcula con el catálogo del mes t+1 y las entradas son del mes t y anteriores, así que no es una función directa de ellas. Pero las entradas incluyen `n_m_ge_3_mes` y `n_m_ge_4_mes`, de la misma familia que el objetivo: hay persistencia fuerte. Defendible, y conviene decirlo antes de que lo pregunten |

## 2. Categoría Básico (el Avanzado exige cumplirlo)

| Requisito | Estado | Evidencia | Observación honesta |
|---|---|---|---|
| Limpiar y preparar datos de la zona | CUMPLE | `ml/eda/build_panel.py`, `docs/research/13-eda-sgc.md` | 35 duplicados exactos removidos, sistemas unificados, nulos documentados. Zona: Santander completo (87 municipios) |
| Modelo supervisado de clasificación | CUMPLE | `artifacts/ml/metrics.json` (benchmark A a E), `ml/src/supervised.py`, `ml/src/benchmark.py` | Random forest balanceado, elegido en validación entre 5 modelos |
| Niveles bajo, medio, alto definidos | CUMPLE | `docs/data/diccionario.md`: alto si M>=4, medio si M 3,0-3,9, bajo si no hay M>=3, del mes siguiente | La guía oficial sugiere municipio y año; aquí es municipio y mes, y está documentado |
| 10 variables mínimas justificadas | CUMPLE | `docs/data/diccionario.md` (32 variables) | Justificación general por familia; varias filas comparten el mismo texto de justificación |
| Métricas para evaluar | CUMPLE | `artifacts/ml/metrics.json`: macro-F1, balanced accuracy, accuracy, precisión, recall, F1 por clase, matriz de confusión | Test macro-F1 0,5296 frente a 0,3255 del dummy |
| Entender en qué casos se equivoca | CUMPLE | `artifacts/ml/critical_analysis.md` | **La clase medio no se detecta en test (precisión, recall y F1 = 0 con 41 casos)**; la clase alta tiene 19 casos |
| Producto: cuaderno o interfaz con una entrada y su resultado | CUMPLE | `/basico` en la web; `POST /api/v1/clasificar`; `docs/research/17-pruebas-e2e.md` | Entrada: municipio y mes; resultado: clase y probabilidades. No acepta variables libres: usa la fila del panel |
| Exploración inicial con al menos 3 gráficas | PARCIAL | `docs/research/13-eda-sgc.md` (tablas), `app/web/public/data/inicio.json`, `docs/figures/` | Hay gráficas en la web (eventos por año, balance de clases) y un mapa; no se verificó en esta auditoría que haya histograma de magnitudes ni su explicación. Revisar |

## 3. Categoría Medio

| Requisito | Estado | Evidencia | Observación honesta |
|---|---|---|---|
| Únicamente modelo no supervisado | CUMPLE | `ml/medio/model.py` (KMeans y contraste jerárquico), `ml/medio/run.py` | No usa objetivos; la ventana de ajuste llega hasta 2025-05 y no usa filas 2025-06+ ni targets |
| 15 variables mínimas, incluidas territoriales | CUMPLE | `docs/research/16-medio-clusters.md`: 21 variables de perfil; territoriales: `centroid_lat`, `centroid_lon`, `poblacion` | Las territoriales son pocas y de tipo geográfico/demográfico |
| Comparar la zona con otras unidades territoriales mediante patrones o grupos | CUMPLE | `app/web/public/data/clusters.json`, `docs/research/16-medio-clusters.md` | 87 municipios en 3 grupos: 19, 66 y 2 |
| Evaluación y comparación de enfoques | PARCIAL | `docs/research/16-medio-clusters.md`: silhouette 0,2777, Davies-Bouldin 1,0623, jerárquico silhouette 0,2854 | Métricas bajas (silhouette 0,28). **ARI entre semillas 1,0 / 0,387 / 1,0: solución no estable.** El grupo 2 tiene solo 2 municipios. Solo se comparan KMeans y jerárquico |
| Interpretación de grupos e importancia de variables | PARCIAL | `docs/research/16-medio-clusters.md` (rasgos por grupo) | Se describen los 3 rasgos más fuertes por grupo; no hay análisis de importancia de variables como tal |
| Visualización territorial reproducible | CUMPLE | `app/web/public/data/clusters.json`, `docs/figures/medio-clusters.png`, `/medio` en la web, `python -m ml.medio.run` | Mapa con polígonos. Los polígonos son un espejo no oficial sin licencia declarada (`docs/data/geojson_santander.md`) |
| Explicación útil para estimar o clasificar el riesgo, no solo grupos | PARCIAL | `docs/research/16-medio-clusters.md` | El propio informe dice que los grupos describen heterogeneidad de actividad registrada y no demuestran daño ni riesgo. No ordenar los grupos como bajo/medio/alto |
| Arquitectura con diagrama (datos, procesamiento, modelo, visualización) | CUMPLE | `docs/flows/arquitectura-sistema.png`, `docs/flows/reto-oficial.png`, `docs/DOCUMENTACION.md` sección 8 | `arquitectura-sistema` pertenece al plan anterior congelado; revisar que no contradiga lo actual |

## 4. Categoría Avanzado

| Requisito | Estado | Evidencia | Observación honesta |
|---|---|---|---|
| Cumplir Básico y Medio | PARCIAL | Secciones 2 y 3 de este documento | Ambos existen; ver sus PARCIAL |
| Aprendizaje por refuerzo obligatorio (agente entrenado; no se aceptan sustitutos) | PARCIAL | `ml/src/rl_env.py`, `ml/src/train_ppo.py`, `artifacts/ml/rl/ppo_policy.zip`, `ppo_config.json` | El agente PPO es real, pero **colapsa a una política constante** idéntica al top-K estático: 5 municipios fijos en los 28 cortes de val y test; sin uso del estado (`final_audit.md`). El problema es un bandido contextual, no un MDP secuencial |
| 20 variables mínimas justificadas | CUMPLE | `data/panel/metadata.json` (32), `docs/data/diccionario.md` | Ver habilitantes |
| Integrar con otra fuente oficial | PARCIAL | `docs/research/14-fuente-oficial-2.md`, `data/external_pub/dane_poblacion_municipal.csv`, `data/external_pub/crosswalk_municipios.csv` | DANE proyecciones de población, cruce 87/87. **Aporta una sola variable (`poblacion`)** al panel de 32 y es una proyección retrospectiva. La integración es real pero delgada |
| Evidencia de cómo se unió la información | CUMPLE | `data/external_pub/crosswalk_municipios.csv`, `ml/eda/build_panel.py` (alias El Carmen) | Cruce por DIVIPOLA con alias explícito confirmado |
| Priorización exploratoria de zonas de Santander | CUMPLE | `/avanzado`, `GET /api/v1/priorizacion`, `app/web/public/data/pruebas.json` | Está etiquetada como exploratoria. En el despliegue solo muestran lista el estático y el aleatorio |
| Flujo funcional y verificable con demostración (no se requiere API) | PARCIAL | `docs/DOCUMENTACION.md` secciones 4 y 12; `docs/research/17-pruebas-e2e.md` | El flujo se reproduce por comandos y la web funciona sin API para Medio y Avanzado. El PPO no corre en el despliegue; la demostración en vivo del agente depende de correrlo localmente |
| Validación que respete el orden temporal | CUMPLE | `ml/src/data.py` (`temporal_month_splits`), `artifacts/ml/partitions.json` | Train 2019-02 a 2024-04, val 2024-05 a 2025-05, test 2025-06 a 2026-08. Sin embargo entre particiones |
| Evaluación del agente | CUMPLE | `artifacts/ml/rl/metrics_rl_{val,test}.json`, `comparison_*.md`, `final_audit.md` | Comparado con estático, ranker, aleatorio y oráculo; el resultado es empate con el estático |
| Incertidumbre o explicación | PARCIAL | Bootstrap por bloques en `final_audit.md`; `artifacts/ml/critical_analysis.md` | Hay IC bootstrap para el RL. **No hay incertidumbre para el supervisado** (sin IC ni calibración; AUC de la clase alta no disponible) |
| Utilidad de la priorización, supuestos, limitaciones, extensiones | CUMPLE | `artifacts/ml/rl/limitaciones.md`, `research_report.md`, `docs/DOCUMENTACION.md` sección 10 | Las limitaciones están escritas con honestidad. La utilidad concreta es modesta: el agente no mejora la regla simple |

## 5. Rúbrica del Avanzado (100 puntos) y autoevaluación por criterio

Los puntajes máximos son los oficiales. "Estado" es nuestra lectura de cuánto del criterio está respaldado por evidencia; no es una nota.

| Criterio (máx.) | Estado | Evidencia | Observación honesta |
|---|---|---|---|
| Datos e integración de fuentes (15): 20 variables justificadas; evidencia de unión con otra fuente oficial | PARCIAL | `data/panel/metadata.json`, `docs/data/diccionario.md`, `docs/research/14-fuente-oficial-2.md` | 32 variables y cruce 87/87 con DANE. La fuente segunda aporta 1 variable; la justificación del diccionario es genérica por familia |
| Aprendizaje por refuerzo (20): entorno, estados, acciones y recompensa; no se aceptan sustitutos | PARCIAL | `ml/src/rl_env.py`, `artifacts/ml/rl/final_audit.md`, `rl_research/research_report.md` | Entorno, estados, acciones y recompensa están definidos y documentados con tests. El agente entrenado converge a la constante y no supera al estático |
| Validación e incertidumbre (10): orden temporal; evaluación del agente; incertidumbre o explicación | PARCIAL | `artifacts/ml/partitions.json`, `final_audit.md`, `critical_analysis.md` | Orden temporal y evaluación del agente sólidos. Faltan IC y calibración del supervisado; el test del RL ya estaba expuesto por la pista de referencia |
| Flujo integrado y trazabilidad (15): funcional, verificable, reproducible | PARCIAL | `data/sgc/provenance.json`, hash del panel en `metrics.json`, `docs/DOCUMENTACION.md` sección 12 | Hashes, semilla y proveniencia por archivo. Huecos: no hay script versionado para el XLSX del DANE; `data/raw` y `data/external` están fuera de git; el README sigue describiendo un estado anterior (ver abajo) |
| Impacto e innovación (20): utilidad para decidir en Santander; supuestos, limitaciones, extensiones | PARCIAL | `docs/DOCUMENTACION.md` secciones 2 y 10; `docs/research/12-brechas-e-ideas.md` | Planteamiento honesto y bien acotado; el valor práctico queda limitado porque el RL no aporta frente a la regla simple. Lo innovador: gate de degeneración, auditoría del colapso, trazabilidad por hash |
| Presentación (20): problema, integrantes que exponen, trabajo en equipo | PARCIAL | `/presentacion` en la web, `docs/plan/10-roles-web-presentacion.md` | El pitch está en la web. Falta confirmar guion, reparto de turnos entre los tres y ensayo cronometrado (10 min + 3 de preguntas) |

## 6. Qué hacer antes de la presentación

1. **Decidir cómo demostrar el PPO en vivo.** No corre en el despliegue. Dejar un comando local listo (`ml.src.evaluate_rl --split val`) y ensayar el discurso: "el agente aprende la política constante y empata con el top-K estático".
2. **No sobrevender el RL.** Preparar la respuesta a "¿qué aporta el agente?": nada medible sobre el estático; la contribución es el entorno, el gate de degeneración y la auditoría.
3. **Preparar la respuesta sobre la clase medio** (F1 0 en test) y sobre el desbalance (bajo 95%). Mostrar macro-F1 y por qué no accuracy.
4. **Actualizar el README.** La sección "Estado" dice que datos, modelos y métricas "NO hechos" y que la web es andamiaje; la etiqueta real descrita en "Decisiones clave" (emergencias UNGRD) fue descartada. Un jurado que lo lea verá lo contrario de lo demostrado.
5. **Cerrar el hueco de trazabilidad del DANE:** versionar el script o los pasos de descarga del XLSX (hoy solo existe el CSV compacto y los metadatos).
6. **Agregar incertidumbre al supervisado** (IC por bootstrap de bloques de meses sobre macro-F1) o declarar explícitamente que no existe.
7. **Verificar las tres gráficas de exploración** que pide la guía (sismos por año, histograma de magnitudes, mapa o dispersión) y tenerlas a mano.
8. **Aclarar la licencia:** los polígonos son un espejo no oficial sin licencia; declararlo en la presentación o reemplazarlos por la capa oficial DANE/IGAC si hay tiempo.
9. **Repartir los turnos de exposición** entre Nicolás, Julián y Zabdiel (el reto exige que expongan los integrantes) y cronometrar 10 minutos.
10. **Correr `uv run pytest -q` y el build de la web** el mismo día para llegar con CI y despliegue verificados.
11. **Medio:** tener lista la explicación de por qué ARI 0,387 con la semilla 21 no invalida los grupos, y de por qué el grupo 2 tiene solo 2 municipios (incluye Los Santos).
