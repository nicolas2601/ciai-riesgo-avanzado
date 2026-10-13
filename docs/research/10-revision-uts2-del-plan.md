# Revisión independiente del plan UTS: tres problemas confirmados

Fecha: 2026-10-13. Alcance: `docs/plan/08-reto-oficial-plan-4h.md`, contrastado con enunciado completo y `09-rl-diseno.md`. No se entrenaron modelos, descargaron/procesaron datasets nuevos ni modificaron archivos del plan.

**Veredicto: REQUEST CHANGES. Confianza: alta** para las contradicciones y contraejemplos descritos. No es una auditoría ejecutada de código todavía inexistente; los hallazgos son del diseño documental. No se llenó cuota de ocho con riesgos ya cubiertos.

## Evidencia y versión

- Documento revisado SHA-256: `b058a5abbfd6d3b8370f9840de3f39335605e0977c843ea94bf923bb91f12325`.
- Fuente normativa: [página oficial](https://ciaiuts.com/eventos/hackaton-utsmart-2026), export íntegro en `source/pagina-reto-2026-10-13.txt` y `source/pagina-lineamientos.json`.
- Primera lectura encontró versión anterior con recompensa por paso, objetivo anual y cluster sin aislamiento. UTS corrigió mientras se revisaba; checker detectó cambio y se recargó documento completo. **Esos fallos corregidos no figuran como hallazgos actuales**.
- Checker Python stdlib, exit 0: afirmó presencia de fragmentos vigentes y reprodujo tres contraejemplos, más caso de sensibilidad de cobertura. Son casos lógicos construidos para probar diseño, no datos inventados ofrecidos como fuente del proyecto.

## Hallazgos

| # | Severidad | Defecto confirmado | Ubicación en versión revisada |
|---|---|---|---|
| 1 | P1 | Fallback anual cambia target pero no horizonte explícito del reward RL y baseline | Plan `08`:87,103,114 |
| 2 | P2 | Cuantiles no garantizan clases balanceadas con conteos repetidos/ceros | Plan `08`:88 |
| 3 | P2 | Profundidad >70 km no identifica exclusivamente sismicidad intermedia | Plan `08`:93 |

### 1. P1: fallback anual deja objetivos distintos

**HECHO leído:** línea 87 permite pasar a ventana anual si gate mensual falla; línea 103 fija resultados/recompensa del **mes siguiente**, y 114 exige ranker Básico con mismo objetivo que recompensa. No hay instrucción que propague cambio de horizonte a entorno, reward, baseline, test y demo.

**Escenario reproducible:** cutoff diciembre 2023; enero 2024 sin evento M≥3; diciembre 2024 con M4.2. Clasificador anual tiene clase alta; reward de enero para esa zona tiene actividad cero. Ordenar por probabilidad de clase anual no es el baseline alineado de utilidad mensual; una comparación puede aparentar ventaja RL por evaluar problemas diferentes.

**Arreglo mínimo:** una config común `horizon`/`window_start`/`window_end` para target, entorno, reward, baseline y evaluación. Si se cambia a año, definir si se selecciona una vez por año o usa ventana móvil anual; en este último caso purgar targets solapados y reconocer episodios correlacionados. Regenerar todas las ventanas/splits y no usar comparación cruzada de horizontes. Alternativamente mantener RL mensual, pero entrenar ranker mensual adicional y declarar que Básico anual es componente distinto.

**Test de aceptación:** para cada episodio, `target_window == reward_window == baseline_window == evaluation_window`; contraejemplo enero/diciembre debe respetar horizonte seleccionado. Ninguna label de periodo incompleto se rellena con cero (gate ya previsto en 09).

### 2. P2: «Clases balanceadas» no se sigue de cuantiles

**HECHO leído:** alternativa B vende cuantiles de conteo mensual con ventaja «Clases balanceadas». Eso es falso como garantía.

**Contraejemplo reproducido:** 100 observaciones: 90 ceros, cinco unos, cinco doses. Terciles empíricos son ambos cero. Con partición `low <= q1`, `q1 < medium <= q2`, `high > q2`, conteos resultantes son **90 / 0 / 10**, no balanceados. Cambiar algoritmo de interpolación no resuelve masa dominante de ceros. Romper empates por orden de filas crea etiquetas diferentes para mismo conteo.

**Arreglo mínimo:** decir «intento de discretización relativa, sujeto a empates/soporte»; fijar umbrales solo en train, congelarlos y aplicar gate de clases presentes por partición. Usar umbrales de magnitud oficiales ejemplificados si tienen soporte; no prometer balance ni inventar tercera clase.

**Test de aceptación:** distribución cero-inflada/empates debe disparar rechazo de discretización inviable, nunca repartir ceros arbitrariamente entre niveles.

### 3. P2: >70 km incluye eventos profundos

**HECHO leído:** lista de variables llama a «fracción de eventos con profundidad >70 km» sismicidad intermedia.

**HECHO externo verificado:** [USGS, Determining the Depth of an Earthquake](https://www.usgs.gov/programs/earthquake-hazards/determining-depth-earthquake) distingue superficial 0–70 km, intermedia 70–300 km y profunda 300–700 km. Se debe fijar convención explícita para fronteras compartidas.

**Contraejemplo:** profundidad 500 km satisface `>70` pero no intervalo intermedio `70 < depth <= 300`. Si se acepta catálogo nacional o cajas grandes, ese evento contaminaría variable mal rotulada y explicación territorial. No se afirma que haya tal evento en dataset aún no descargado.

**Arreglo mínimo:** conservar cálculo y renombrar a `share_nonshallow_events`, o separar intermedios `70 < depth <= 300` y profundos `depth > 300` con unidad km y convención de bordes. No confundir profundidad con daño/sacudida superficial.

**Test de aceptación:** casos 69,70,71,300,301,500 km quedan en bins disjuntos definidos; diccionario coincide con cálculo.

## Contraste de decisiones abiertas, no hallazgos adicionales

### A. Mensual versus anual

**Decisión recomendada:** mensual provisional para obtener más cutoffs independientes que anual, **solo si** soporte de clases, positivos, seguimiento completo y disponibilidad de covariables pasan gate. Evaluar esos conteos tras obtener datos a partir de hora autorizada, no afirmar viabilidad de antemano. Anual es fallback justificado, no equivalente gratuito: menor número efectivo de episodios, cambios de reward y splits como hallazgo 1.

### B. Cobertura por radio R

**Acepto como sensibilidad separada**, no como vía para afirmar que RL se volvió necesario. Definir utilidad de cobertura explícita y R antes de mirar test. Distancias en CRS métrico/geodésicas, conjunto cubierto visible en estado, unión sin doble conteo y mismos K/máscaras para todos los métodos. Un centroide/radio es regla de análisis, no propagación sísmica, área afectada ni beneficio causal de inspección.

**Contraejemplo evaluativo reproducido:** candidatos A y B cubren las mismas unidades `u,v`, C cubre `w`; cada unidad pesa dos. K=2: top-K por valor individual elige A+B y cubre valor cuatro; A+C cubre seis. Por eso top-K aditivo no es oracle válido para objetivo de unión.

Agregar baseline **greedy de ganancia marginal de cobertura**. Oracle debe optimizar misma unión: solución exacta cuando problema pequeño lo permita, o cota superior explícita. Un greedy sin prueba de optimalidad no se rotula oracle exacto. El objetivo es cobertura combinatoria; romper aditividad no prueba superioridad de RL frente a ese baseline.

### C. Antes de 08:00

**Acuerdo operativo conservador:** planificación, revisión y entorno; descarga/procesamiento/entrenamiento desde inicio autorizado, confirmar en ceremonia. Página dice «el reto inicia a las 8:00» pero no contiene prohibición textual detallada sobre explorar metadatos antes. Presentar esta política como interpretación preventiva del equipo, no cita oficial inexistente. No afirmar que trabajo previo automáticamente habilita o descalifica.

## Evaluación de aportes de datos UTS

Son aportes reportados con consultas por otra sesión, no descargas repetidas aquí: HTTPS SGC/formularios, proyecciones anuales DANE, Gobernación desde 2018-05, inventario ArcGIS y contraste USGS. No hay evidencia contraria en la revisión; aceptar como inputs de planificación con URL/fecha y registrar export/hash al empezar procesamiento.

Proyecciones por año resuelven el join del año de exposición, **no** la disponibilidad histórica de publicación. Plan ya declara retrospectividad: no se reporta ese punto como fallo actual. Gobernación es opcional y no cubre años previos; ausencia de cobertura debe conservarse como desconocida, no como cero. Geometrías/códigos se validan antes del join; 89 nombres reportados no prueban 89 municipios oficiales distintos.

## Recomendación de cierre

Corregir tres fragmentos sin ampliar alcance. Priorizar SGC+DANE, ≥20 variables reales con diccionario, modelos supervisado/no supervisado y MaskablePPO efectivamente entrenado, backtest temporal y demo. Mantener análisis de radio fuera de ruta crítica. No reabrir API/Cloudflare ni declarar resultados todavía no medidos.
