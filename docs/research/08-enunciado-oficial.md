# Enunciado oficial CIAI UTSmart 2026: requisitos y evidencia

Consulta: 2026-10-13. Fuente primaria: [página oficial completa](https://ciaiuts.com/eventos/hackaton-utsmart-2026). Se leyó el export íntegro renderizado por la sesión UTS, incluidos los nueve desplegables; no se atribuye lectura propia del navegador a esta sesión. WebFetch solo recuperó la portada; Playwright de esta sesión estaba ocupado.

## Evidencia conservada

- [Texto de portada, agenda, participantes, salas y fuentes](source/pagina-reto-2026-10-13.txt): captura `document.body.innerText`, 2026-10-13 aproximadamente 06:25 Colombia; líneas citadas abajo se refieren a este archivo, no al HTML.
- [Nueve secciones desplegadas sin editar](source/pagina-lineamientos.json): timestamp `2026-10-13T11:25:53.642Z`. Índices humanos 1–9: rúbricas Básico, Medio, Avanzado; reglas; datos; entregables; habilitantes; evaluación; guía Básico.
- [URLs efectivas de los enlaces](source/pagina-enlaces.txt).

**HECHO:** este enunciado sustituye las suposiciones del plan anterior: tema sísmico, aprendizaje por refuerzo obligatorio en Avanzado, mínimo 20 variables y desarrollo de cuatro horas. API, cinco horas y UNGRD como fuente principal no son exigencias oficiales.

## 1. Tema y producto general

**HECHOS, portada líneas 85–123:**

- Título: «Santander Inteligente: IA para analizar y clasificar el riesgo sísmico».
- Jornada presencial, datos sísmicos reales del Servicio Geológico Colombiano (SGC), zona de Santander, tres categorías.
- Contexto citado por organización: Nido Sísmico de Bucaramanga bajo Mesa de Los Santos y alta actividad sísmica intermedia. No equivale a demostrar daño superficial en cada epicentro.
- «Temática: sismos, con tema específico libre». Equipo elige primero zona y luego filtra datos. Referencia para principiantes: últimos 20 años del comportamiento sísmico de Santander; no es horizonte obligatorio universal.
- Anticipación es opcional: texto dice «si el equipo lo decide, lo anticipen».
- «El componente central es obligatorio en los tres niveles: implementar y demostrar un sistema de Machine Learning funcional, entrenado con datos reales de una fuente oficial».
- No aceptan presentación conceptual, prototipo visual sin modelo ni solución basada solo en reglas fijas.

## 2. Categorías y productos mínimos

| Categoría | Modelo que exige texto | Variables | Requisitos / mínimo | Desarrollo |
|---|---|---:|---|---|
| Básico | Supervisado de clasificación | 10 | Limpiar/preparar zona y clasificar actividad sísmica bajo/medio/alto con métricas; cuaderno ejecutable o interfaz con entrada y resultado | 302A / 302B |
| Medio | «Únicamente modelo no supervisado» | 15 | «Cumplir el reto Básico» y comparar otras unidades territoriales mediante patrones/grupos, variables territoriales y visualización; prototipo funcional y territorial reproducible | 315A |
| Avanzado | «Obligatoriamente aprendizaje por refuerzo» | 20 | «Cumplir los retos Básico y Medio» e integrar sismicidad con otra fuente oficial para priorización exploratoria de zonas de Santander y agente RL; flujo funcional/verificable con demo, «no se requiere API» | 307B |

Fuente: portada líneas 91–123 y secciones de rúbrica/habilitantes.

**INFERENCIA conservadora de cumplimiento:** entregar tres componentes diferenciados: clasificación supervisada heredada de Básico, análisis no supervisado territorial de Medio y agente RL de Avanzado. No sustituir RL por ranker supervisado ni sustituir clustering por clasificador. Texto de Medio combina «cumplir Básico» con «únicamente no supervisado»: confirmar con organización alcance exacto de herencia; mientras tanto conservar ambos bloques, claramente separados.

## 3. Rúbricas completas

**HECHO:** cada categoría suma 100 puntos; no se suman tres rúbricas para asignar 300 al equipo Avanzado. Fuente: JSON secciones 1–3 y 8.

### Básico

| Criterio | Puntos | Evidencia descrita por organización |
|---|---:|---|
| Datos: obtención y limpieza | 20 | Fuente oficial citada, dataset limpio/preparado y 10 variables justificadas |
| Presentación | 20 | Problema identificado, integrantes exponen, trabajo en equipo, manejo de tiempo/respuestas |
| Modelo supervisado | 25 | Definición bajo/medio/alto, entrenamiento, métricas básicas, comprensión |
| Demostración | 10 | Cuaderno/interfaz con entrada y clasificación |
| Impacto e innovación | 15 | Impacto potencial en Santander y, cuando sea posible, innovación |
| Análisis de datos | 10 | Exploración y explicación de metodología/resultados |

### Medio

| Criterio | Puntos | Evidencia descrita por organización |
|---|---:|---|
| Datos y preprocesamiento | 15 | 15 variables justificadas, incluidas territoriales; preparación/transformación |
| Modelo no supervisado | 25 | Selección, entrenamiento/evaluación, comparación de enfoques, interpretación de grupos/importancia de variables |
| Arquitectura utilizada | 15 | Diagrama e integración de datos, procesamiento, modelo y visualización |
| Prototipo y visualización territorial | 10 | Funcional/reproducible y compara unidades territoriales |
| Impacto e innovación | 15 | Explicación útil para estimar/clasificar riesgo, no solo grupos |
| Presentación | 20 | Problema identificado, integrantes exponen y trabajo en equipo |

### Avanzado

| Criterio | Puntos | Evidencia descrita por organización |
|---|---:|---|
| Datos e integración de fuentes | 15 | 20 variables justificadas; cómo se unió sismicidad con otra fuente oficial |
| Aprendizaje por refuerzo | 20 | «Agente entrenado por refuerzo (entorno, estados, acciones y recompensa); no se aceptan sustitutos» |
| Validación e incertidumbre | 10 | Orden temporal, evaluación del agente, incertidumbre o explicación |
| Flujo integrado y trazabilidad | 15 | Flujo funcional, verificable/reproducible, solidez metodológica/trazabilidad |
| Impacto e innovación | 20 | Utilidad para decidir en Santander; supuestos, limitaciones/extensiones |
| Presentación | 20 | Problema identificado, integrantes exponen y trabajo en equipo |

## 4. Reglas de participación

**HECHOS, JSON sección 4:**

1. Equipos de 2 o 3 personas, de misma institución o mixtos.
2. Una sola categoría por equipo, inscrita antes de iniciar; una persona solo en un equipo.
3. Inicio 08:00, tolerancia 15 minutos, tiempo perdido no se repone.
4. Herramientas propias: portátil con cargador, software y cuentas de nube/IA, incluidas pagas.
5. «Los modelos preentrenados, las APIs y la IA generativa se permiten como apoyo, pero no reemplazan el modelo de Machine Learning que exige la categoría».
6. Nada de datos personales sensibles sin autorización; modalidad presencial con acompañamiento CIAI.

No dice que usar librería RL esté prohibido ni que todo algoritmo deba reimplementarse; sí exige agente/modelo entrenado por equipo. Política inicializada sin pesos preentrenados y entrenada en entorno propio debe documentarse; confirmar cualquier interpretación con jurado, no inventar excepción.

## 5. Datos: reglas obligatorias

**HECHOS, JSON sección 5:**

- Datos reales oficiales. «No se aceptan datos inventados ni sintéticos como fuente principal».
- Fuente principal: catálogo sísmico Red Sismológica Nacional, SGC.
- Citar origen, dirección web, fecha de descarga y filtros.
- Una sola tabla: fila = observación, columna = variable. Guardar CSV final integrado; tablas intermedias no reemplazan entregable.
- Sin duplicados; faltantes tratados; unidades/fechas homogéneas; atípicos revisados.
- Mínimos 10/15/20; «las derivadas cuentan si se justifican».
- Diccionario: nombre, tipo, unidad, fuente y por qué se incluye cada variable.
- «Variable objetivo bien definida y que no se calcule directamente de las variables de entrada».
- SGC tiene dos consultas: junio 1993–febrero 2018 y desde marzo 2018; columnas distintas a unificar. Consultar por meses/años es recomendación de descarga, no requisito de ventana analítica.

**INFERENCIA metodológica:** target de actividad de periodo futuro con features anteriores evita aprender umbral de misma magnitud de entrada. Target derivado del máximo de magnitud del mismo periodo y ese máximo como predictor incumple regla explícita. No contar IDs, target o flags de simulación como sustitutos de 20 covariables justificadas.

## 6. Fuentes oficiales enlazadas

**HECHO:** enlaces extraídos de página; no prueba de que ya tengamos acceso/export/licencia de cada dataset.

| Fuente | URL efectiva | Uso descrito por página |
|---|---|---|
| SGC catálogo RSN, principal | http://bdrsnc.sgc.gov.co/paginas1/catalogo/ | Sismos desde junio 1993; fecha, coordenadas, profundidad, magnitud, fases, RMS, gap, municipio; Excel |
| SGC datos abiertos | https://datos.sgc.gov.co/ | Amenaza sísmica, mapa geológico, inventario movimientos en masa; CSV/GeoJSON/Shapefile |
| SGC sismicidad histórica | https://sish.sgc.gov.co/ | Catálogo homogeneizado Mw y fichas de eventos con daños reportados |
| USGS catálogo | https://earthquake.usgs.gov/earthquakes/search/ | Contrastar magnitudes/localizaciones |
| Datos Abiertos Colombia | https://www.datos.gov.co/ | Incluye reporte histórico de emergencias Gobernación Santander |
| «DANE e IGAC» | https://www.dane.gov.co/ | Población/vivienda municipal, límites, cartografía, altitud/suelos |

Página rotula último enlace «DANE e IGAC», pero destino efectivo es DANE; no hay URL IGAC independiente en export. Verificar recurso concreto antes de atribuir descarga a IGAC. UNGRD no equivale a catálogo SGC ni reemplaza fuente principal.

## 7. Entregables y elegibilidad

**HECHOS, JSON secciones 6–7:** a **12:00 m.**:

1. Dataset CSV limpio y diccionario con justificación de variables.
2. Fuente oficial citada: URL, fecha y filtros.
3. Código de análisis/entrenamiento, cuaderno o repo reproducible.
4. Modelo obligatorio con métricas y validación.
5. Prototipo o demostración.
6. Presentación para pitch final.

Antes de puntuar, jurado verifica modelo funcional **entrenado por equipo y demostrado en vivo**, tipo obligatorio, fuente oficial real citada y mínimo de variables. «Un proyecto que no cumpla puede presentarse, pero no es elegible para premiación». Mock, pesos externos sin entrenamiento, slides o visualización sola no habilitan.

## 8. Agenda, equipo y evaluación

**HECHOS, portada líneas 54–84, 489–499, 655–717:**

| Fecha / hora Colombia | Actividad |
|---|---|
| Martes 13-oct, 07:00–08:00 | Apertura, registro/validación, categoría, temática/reglas/rúbricas |
| 13-oct, 08:00–12:00 | Desarrollo técnico; **cuatro horas**, entrega a las 12:00 |
| 13-oct, 12:00–14:00 | Receso, entregas cerradas, revisión de habilitantes |
| 13-oct, 14:00–16:45 | Presentaciones en cuatro salas, dos jurados/sala; primero Básico, Medio y Avanzado |
| 13-oct, 16:45–18:00 | Reevaluación si corresponde |
| 13-oct, 17:30–18:00 | Deliberación, desempates/acta/fotos; agenda publicada solapa reevaluación |
| Viernes 16-oct, hora por confirmar | Premiación, un ganador por categoría |

- Sitio anuncia 39 equipos, 110 participantes, tres instituciones, ocho jurados: 20 Básico, 10 Medio, nueve Avanzado. UTS 32 equipos, UDES cuatro, UNAB tres.
- Equipo **Syntax error II**, UNAB, tres integrantes: Nicolás Santiago Moreno Monroy, Julián Andrés Arteaga Faria y Zabdiel Julián Quintero Monroy.
- Desarrollo **307B**; presentación **315A, 16:10 estimada**, no confundir ambas salas. Horas de presentación pueden ajustarse en vivo.
- Pitch/demostración 10 min, preguntas 3 min, calificación 2 min; integrantes exponen.
- Jurados por salas: 302A Carlos Pineda/Alain Pérez; 302B Indira Cassaleth/Jahir Saavedra; 315A Diego Cruz/Jaidiver Lombo; 307B Carmen Dulcey/Diego Álvarez. Sitio también enumera supervisión y apoyo logístico en export íntegro.
- Puntaje = promedio de jurados, cada rúbrica 100. Reevaluación si diferencia **mayor de 20** puntos, empate de primer lugar entre salas o dudas de requisitos; nuevos jurados de otra sala.
- Desempate: impacto/innovación, después solidez técnica ML. Un ganador por categoría; al momento de captura aún por anunciar.

Ubicación: UTS Bucaramanga, salones 302A/302B/315A/307B. Contacto publicado: `ciai@correo.uts.edu.co`. Registro enlazado: https://forms.cloud.microsoft/r/UeCZcr21Rc ; [pantalla en vivo](https://ciaiuts.com/eventos/hackaton-utsmart-2026/pantalla). Navegación, listas completas de equipos/apoyo y enlaces legales están conservados en los exports, no se reinterpretan como requisitos técnicos adicionales.

## 9. Guía oficial Básico, paso por paso

**HECHO, JSON sección 9; ejemplos/sugerencias no son reglas universales:**

1. Zona y pregunta: municipio, provincia, área metropolitana o corredor vial.
2. Catálogo SGC por departamento/municipio/rectángulo, periodo y magnitud mínima; descargar Excel y registrar URL/fecha/filtros.
3. Limpiar duplicados/filas sin coordenadas o magnitud, fechas y columnas entre periodos; ≥10 variables justificadas.
4. Ejemplo de target municipio-año: bajo sin eventos M≥3, medio M entre 3–3.9, alto al menos un M≥4. No implica que M de mismo periodo sea input válido.
5. ≥3 gráficas: eventos por año, histograma magnitudes, mapa/dispersión latitud-longitud y observaciones.
6. Separar train/test 80/20 y modelo sencillo scikit-learn: árbol, logística, KNN o random forest. En Avanzado prevalece requisito de orden temporal, no split aleatorio por defecto.
7. Exactitud y matriz confusión; precisión/recall/F1 ante desbalance; explicar errores.
8. Cuaderno o interfaz simple sugerida Streamlit/Gradio, entrada/resultados.
9. Pitch: problema/zona, fuente, variables, modelo/métricas, demo, impacto/limitaciones.

Herramientas sugeridas: Python, pandas, scikit-learn, matplotlib, Colab/Jupyter. No exige esas tecnologías ni API ni GPU ni web React.

## 10. Gate actualizado de planificación

**PROPUESTA derivada, no texto oficial:** antes de priorizar UI/API, asegurar SGC real + fuente oficial adicional + tabla/diccionario de ≥20 covariables + supervisado + no supervisado + agente RL efectivamente entrenado + backtest temporal + demo ejecutable y pitch. Diseño RL y sus límites en [09-rl-diseno.md](09-rl-diseno.md).

El plan anterior 01–07 y prompt de explicación enviado a Nico deben leerse como exploración previa, no cumplimiento del enunciado sísmico actual. No borrar evidencia histórica ni presentar trabajo aún no realizado como listo.
