# Vista independiente: sismología, roles y web como presentación

Fecha: 2026-10-13. Investigación con fuentes citadas y propuesta operativa para 08:00–12:00. Escrita **sin leer** `docs/plan/10-roles-web-presentacion.md` ni `docs/research/12-brechas-e-ideas.md`; se contrastarán después, no se presentan como ideas propias. No descarga de datasets de entrenamiento, procesamiento de datos del reto ni código de producción en este bloque.

**Decisiones de Nico transmitidas por UTS:** React es producto principal; Streamlit solo respaldo; pitch en la propia web, sin diapositivas; Zabdiel experto ML, Julián web y Nico puente ML/web. El cumplimiento del [enunciado oficial](08-enunciado-oficial.md) manda: datos SGC reales + otra fuente oficial, ≥20 variables justificadas, modelos entrenados por equipo, validación temporal y demo en vivo.

## A. Sismología que cambia decisiones, no decoración

### 1. Nido de Bucaramanga: actividad no equivale a daño

**HECHOS de literatura consultada:**

- Estudio de *Scientific Reports* (2023) describe concentración intermedia en torno a **150–170 km** y subestructura con un grupo superior alrededor de 130 km. «150 km» es referencia aproximada, no profundidad exacta de cada evento [S1].
- García-Arias et al. (2026) estudian **148,910 eventos SGC, enero 1994–febrero 2024**, en ámbito del nido; reportan **b≈1.03** global y valores anuales alrededor de 1.0 sin variación significativa en su análisis [S2]. No trasladar b del estudio a cada municipio/mes.
- Tasa ilustrativa calculada sobre ese catálogo/periodo: aproximadamente **13.5 eventos/día** (`148910 / ~30.17 años /365.25`). Es promedio del dominio y umbrales de ese estudio, no tasa actual, tasa M≥4 ni total nacional. El artículo vincula crecimiento de registros pequeños a mejoras de observación; no vender incremento bruto como crecimiento físico de amenaza.
- Mecanismo de delaminación/deshidratación propuesto en S1 es interpretación científica, no causa demostrada que debamos modelar en cuatro horas.
- USGS distingue profundidad, magnitud y efectos superficiales: más distancia a la fuente tiende a reducir sacudida; profundidad/epicentro por sí solos no cuantifican daño [S3].

**INFERENCIA útil:** una policy que siempre elige municipio del nido puede capturar mucha actividad localizada sin priorizar mayor daño potencial. El nombre de salida debe ser **prioridad exploratoria de seguimiento de actividad sísmica**, con exposición separada, no «municipio seguro/peligroso».

**SUPOSICIÓN que exige gate real:** concentración de positivos por epicentro puede hacer tarea casi trivial. No afirmo aquí un porcentaje de M≥4 a profundidad concreta; eso requiere consulta, filtros, denominador y tratamiento de escalas documentados.

### 2. Mc, estaciones y dos versiones del catálogo

**HECHO oficial:** RSNC distingue junio 1993–febrero 2018 (Earthworm/SEISAN) y desde marzo 2018 (SeisComP3), con revisión manual de analistas [S4]. Es cambio de adquisición/procesamiento, no prueba aislada de cambio físico ni fecha única de cambio de estaciones.

**HECHO de estudio:** S2 observa más registros **Ml≤2.5 desde 2009**, mejora de errores/localizaciones y menciona aumento de estaciones/modelos de velocidad como explicaciones posibles. No identifica de manera causal una sola modificación como origen del cambio.

**Definición:** magnitud de completitud **Mc** = umbral sobre el que catálogo es aproximadamente completo bajo método/dominio/periodo analizados. No es «mínimo que aparece» ni valor fijo del país. Depende de red, magnitudes, profundidad, ruido y método. Mejores estaciones pueden bajar Mc y aumentar conteos sin que aumente tasa física.

**Evidencia y límite:** se leyó texto sustancial de S2, pero valores detallados de Mc en tabla/apéndice no quedaron recuperados por WebFetch. No usar números de fragmentos de buscador como umbral validado del proyecto. S5 muestra que errores de magnitud/completitud sesgan b y tasas; no hay tamaño universal de muestra que garantice estimación fiable.

**PROPUESTA MVP:**

1. Conservar `catalog_source_period`, `magnitude_type` y soporte/calidad; comparar distribución de magnitud/conteos entre regímenes (al menos cambio 2009 y software 2018, sin asumir que sean únicos).
2. Usar conteos sobre un umbral común **provisional** con análisis de soporte/completitud en train. M≥3 del ejemplo oficial no prueba por sí mismo completitud uniforme desde 1993.
3. Comparar sensibilidad M≥3/M≥4, periodos anteriores/posteriores y profundidad; no inferir que todo crecimiento es tectónico.
4. Si no puede sostenerse completitud común, recortar periodo justificado o mantener conteo de **eventos registrados**, declarar sesgo y evitar claim de tasa real comparable.
5. Estimar Mc/b regionales con ventanas largas y muestra suficiente solo si tiempo permite; no usar un Mc global estimado viendo futuro de test para construir features pasadas.

Estación más cercana/densidad de red serían covariables útiles **solo con inventario temporal real**. No inventar fecha de apertura ni cantidad de estaciones para completar 20 variables.

### 3. Tipos de magnitud y homogeneización

**HECHOS:** consulta histórica SGC distingue Ml y Mw [S4]. USGS define ML por amplitud local y Mw por momento sísmico; Mwr y Mww son variantes de estimación de momento con métodos distintos (regional y W-phase, respectivamente) [S6]. Definición de Mwr USGS no prueba que una etiqueta idéntica tenga misma implementación SGC.

Un boletín SGC julio 2025 indexado describe MLr y Mw(mB)/Mw(Mwp), pero PDF excedió límite de lectura en esta sesión: se conserva como fuente a revisar, **no se afirma revisión íntegra de sus ecuaciones** [S7].

**PROPUESTA defendible:**

- Conservar magnitud original, tipo, agencia, fecha/versión; no renombrar toda columna a Mw.
- Preferir una escala/documentación compatible y describir pérdida de cobertura si se filtra. Si se usan valores preferidos heterogéneos del SGC, declararlos como tal y evaluar quiebres por tipo/periodo.
- Transformar ML→Mw solo con relación publicada/aplicable a región y rango, incertidumbre y validación; no copiar regresión de otro país ni ajustar con test.
- Contrastar eventos coincidentes por tiempo/localización y profundidad antes de comparar agencias; no deduplicar por magnitud exacta ni promediar agencias silenciosamente.
- No calcular b, energía/Benioff o umbrales físicos sobre mezcla de escalas como si fuera homogénea. Si no hay homogeneización defendible, posponer esos features, mantener básicos por escala con soporte y registrar límite.

### 4. Evento histórico para pitch: 10 de marzo de 2015

| Fuente | Fecha/hora | Magnitud publicada | Profundidad | Localización |
|---|---|---|---|---|
| USGS, evento reviewed `us10001ldx` | **2015-03-10 20:55:44 UTC =15:55:44 Colombia** | **Mww6.2** | **155 km** | 2 km NNW de Cepitá |
| SGC, comunicado005 de2015 | **15:55 hora local**, día10mar2015 | **6.6**, tipo no indicado en texto consultado | **161 km** | Los Santos, Santander |

**HECHOS verificables:** ficha/metadata USGS [S8] y comunicado SGC [S9]. Consultar un evento de referencia no fue descargar el dataset de entrenamiento.

**No afirmar:** «SGC6.6=USGS6.2» por conversión conocida, ni que comunicado sea preliminar/final si no está rotulado. Diferentes agencias/versiones pueden estimar valores distintos; conservar fuente/tipo/fecha de reporte. Boletín mensual SGC puede aportar otra revisión; no sustituir automáticamente una cifra por otra sin trazabilidad.

**Uso narrativo:** «Santander tiene actividad profunda frecuente; este evento de2015 ilustra por qué distinguimos registro instrumental, profundidad y consecuencias. Nuestro agente prioriza análisis con datos oficiales, no predice fecha de próximo terremoto ni emite alertas».

### 5. Features defendibles: prioridad y costo estadístico

| Feature | Utilidad | Gate / decisión cuatro horas |
|---|---|---|
| Conteos registrados sobre umbral, 1/3/12meses | Actividad/recencia | Alta prioridad; mismo cutoff/escala/observabilidad, ceros solo con cobertura |
| Distribución de profundidad, proporción70–300km y >300km | Separar régimen sísmico | Alta; bordes disjuntos, no equivalente daño |
| Magnitud previa máxima/media/dispersión por escala | Describir pasado | Alta; soporte y tipo preservados |
| Tiempo desde último evento sobre umbral | Recencia | Alta; censura inicial y corte temporal |
| RMS/gap/fases y missingness | Calidad de observación | Si disponibles; no factores causales ni ceros cuando faltan |
| Población/vivienda oficial con año | Exposición | Alta si join real; no daño, vulnerabilidad o publicación as-of automática |
| **b-value** en ventana | Distribución relativa pequeños/grandes | Fuera de MVP municipio-mes; opcional regional/ventana larga con Mc/muestra/IC |
| **Mc-aware counts** | Reducir sesgo de detección | Útiles como sensibilidad; no estimar Mc con meses vacíos ni garantizar completitud por umbral arbitrario |
| **Benioff strain** acumulada | Proxy energético de historia | Opcional tras escala/units coherentes; dominada por eventos grandes, no deformación medida |
| Parámetros **Omori–Utsu** | Decaimiento de una secuencia de réplicas | Fuera de MVP: requiere mainshock/aftershocks identificados y completitud postevento, no calendario arbitrario |

**b-value:** relación Gutenberg–Richter `log10 N(M≥m)=a-b*m`. Estimador Aki–Utsu corregido por bins usa `log10(e)/(mean(M)-(Mc-ΔM/2))` con eventos ≥Mc [S10]. No son 20 puntos en una gráfica ni un score directo de peligro. Tamaño, sesgo/completitud y sensibilidad dominan; «n≥50» no es garantía universal [S5,S10]. Más eventos totales del nido no significa suficientes eventos completos en cada municipio-mes.

**Benioff:** acumulado `sum(sqrt(E_i))`; si energía se aproxima proporcional a `10^(1.5*M)`, índice relativo es proporcional a `sum(10^(0.75*M))` bajo escala compatible [S11]. No llamar joules a índice sin constante/unidades verificadas ni «strain» a deformación medida. No reutilizar conversión local ML→Ms de un estudio Wenchuan para Colombia.

**Omori:** `n(t)=K/(t+c)^p` describe tasa de una secuencia de réplicas, no todos los sismos por mes. Se encontraron estudios que cuestionan secuencias Omori en el nido, pero fulltext regional no quedó accesible: no proclamar «jamás hay réplicas» como hecho. La ausencia de secuencia validada basta para excluir fitting de p del MVP; no agregarlo para inflar variables.

### 6. K, horizonte y gate de degeneración

**PROPUESTA operacional:** K es número de municipios que un equipo puede revisar en un ciclo; mes = frecuencia de revisión administrativa, **no ciclo físico comprobado de terremotos**. No tenemos capacidad real de una autoridad: K=5 es escenario de demostración declarado, no dato oficial. Mostrar sensibilidad K=3/5/10 si municipios elegibles/tiempo lo permiten, sin seleccionar K por test.

Mensual genera más cutoffs que anual, pero meses consecutivos siguen correlacionados y pueden estar casi vacíos fuera del nido. Es útil solo si target/clases/positivos tienen soporte. Fallback anual cambia target, reward, baseline, test y UI conjuntamente.

**Gate propuesto a08:30–08:45, sobre train y cobertura disponible:**

1. Contar positivos por mes, municipio y clase; porcentaje de meses sin ninguno y número de municipios elegibles.
2. Medir concentración top1/top5 de positivos/actividad y estabilidad de ese orden entre periodos de train.
3. Comparar baseline estático histórico/población contra aleatorio y oracle de train. Si mismo municipio domina casi siempre, una policy constante puede lograr retorno alto sin resolver tarea útil.
4. Si reward/clases son constantes o casi sin soporte: ajustar ventana, territorio u objetivo **solo con train y justificación**, fijar nueva config, volver a generar splits. No cambiar objetivo después de mirar test para hacer ganar RL.
5. No esconder degeneración mediante bonos de diversidad, daños inventados, pesos ad hoc o claim de precisión sísmica. Si se mantiene, presentarla como hallazgo/limitación y medir mejora real sobre baseline constante.

No pongo un porcentaje universal de «trivialidad»: mostrar métricas y regla de decisión predefinida por equipo. Cobertura por radio es sensibilidad separada con R ex ante, unión sin doble conteo, baseline greedy marginal/oracle consistente; no cura automáticamente falta de señales predictivas.

## B. Roles: una responsabilidad clara por persona

**PROPUESTA independiente, pendiente de contraste con UTS:**

| Persona | Responsabilidad principal | Entrega que desbloquea otras áreas | Qué no hace por defecto |
|---|---|---|---|
| **Zabdiel: dueño ML** | Define features/target/reward/splits y entrena supervisado, clustering y MaskablePPO; evalúa y firma semántica de outputs | Código/artefactos de modelos, métricas, policy y selección real | No UI, túneles ni horas de scraping de portales |
| **Julián: dueño web React** | Navegación, mapa/resultados y modo presentación; integra contrato y etiqueta datos reales/fixtures | Web que explica problema→datos→tres bloques→evaluación→priorización en diez minutos | No decide reward/labels ni fabrica métricas |
| **Nico: puente datos–ML–web** | Obtiene/limpia SGC+DANE, diccionario/provenance, valida splits/contratos, exporta resultados y ejecuta integración end-to-end | Dataset real temprano para Zabdiel; bundle trazable/lectura o inferencia para Julián | No dos implementaciones simultáneas del agente ni rediseño UI completo |

Zabdiel **manda en decisiones ML**; Nico ejecuta datos/pruebas y ayuda con tareas ML delimitadas cuando se acuerden. Julián **manda en web**; Nico conecta modelo/artifact con interfaz. «Entre ambos lados» no significa que Nico sea dueño de todo ni que tenga dos rutas críticas simultáneas sin recortes.

**Ownership de escritura propuesto:** Zabdiel modelos/entorno/training; Nico ingest/features/export/validación de contrato; Julián componentes/frontend. Split/feature schema/reward compartidos se congelan y se cambian avisando; no editar mismo archivo simultáneamente. Si Nico implementa un baseline por delegación explícita, se asigna archivo separado y Zabdiel revisa antes de comparar.

### C. Hitos y handoffs por minuto

Tiempos Colombia, relativos a inicio08:00. Fechas son propuesta operativa, no hechos de trabajo completado. Preparar entorno/leer reglas antes, pero descarga/procesamiento desde inicio autorizado; confirmar ceremonia.

| Minuto / hora | Nico | Zabdiel | Julián | Handoff / gate |
|---|---|---|---|---|
| 0–10 /08:00–08:10 | Prueba export mínimo SGC real; URL/filtros/versión; valida tiempos/columnas | Define contrato target/horizonte/K y checks; inicia fuente adicional DANE si Nico ocupado SGC | Arranca React local, estructura y banner fixtures/pitch | Muestra real SGC y schema congelado, sin exigir dataset completo |
| 10–30 /08:10–08:30 | Ingest por tramos, unifica mínimo viable, join DANE, dedup y provenance | Implementa entorno/policy sobre fixtures explícitos; arma baselines/clustering, tests máscaras/reward | UI con fixtures de forma, nunca métricas aparentes reales | Dataset parcial **de periodo completo** para primera corrida; versión y cobertura |
| 30–45 /08:30–08:45 | Completa panel, ≥20 covariables/diccionario; corte y joins validados | Gate clases/degeneración/completitud; ajusta scope usando train y congela ventanas/splits | Valida lectura JSON y estados sin datos/fuente real | Un snapshot real utilizable; solo train para decisiones |
| 45–75 /08:45–09:15 | Tests temporales/provenance, export de contrato y muestras reales para UI | Entrena supervisado/clustering pequeños; comienza rollout/policy real sin esperar pulido | Mapa y grupos/resultados reales, estructura de relato | Artefactos Básico/Medio y primer agente entrenado o blocker concreto |
| 75–120 /09:15–10:00 | Integra salida real al bundle/web; apoya ejecución/test sin tocar policy simultáneamente | Entrena/evalúa RL en validación; registra seeds/config/curvas; congela candidata | Modo presentación con problema/fuentes/método/limitaciones | Un flujo completo de fuente→modelo→web, aunque pobre desempeño |
| 120–165 /10:00–10:45 | Smoke end-to-end, mismo snapshot/feature order; evidencia de recomputación live | Test final una vez policy congelada; comparación pareada/baselines y límites | Ordena métricas y recorrido del agente; ningún número a mano | Resultados verificables y test intacto hasta evaluación |
| 165–195 /10:45–11:15 | Verifica entrega/reproducción y prueba fallback; ejecuta selección real en vivo | Revisa retorno, soportes/máscaras y explica decisiones ML | Ensayo pitchweb10min con los tres | Si falla React: activar respaldo, no iniciar rediseño |
| 195–225 /11:15–11:45 | Congela CSV/diccionario/código/modelos/bundle; confirma canal de entrega | Congela checkpoints/métricas y documentación de limits | Congela build/assets/modopitch; navegador local probado | Entrega anticipada verificable; quedan15min para fallos reales |
| 225–240 /11:45–12:00 | Confirma recepción/acceso y rutas; no añade features | Verifica checkpoint/command ejecutable | Prueba navegación/pitch local y backup | Deadline12:00; evidencias entregadas antes de cierre |

**Ruta crítica:** SGC real → schema/cobertura → panel válido → agente entrenado → evaluación → bundle → demo. No: API nueva → túnel → diseño pulido. Zabdiel recibe tranche completa temprano; no esperar a toda extracción del catálogo para escribir entorno o iniciar primeros entrenamientos válidos.

### D. Qué pueden desarrollar sin datos oficiales

- Tests unitarios con fixtures marcados `is_fixture=true`, `source_status="not_official"`; shapes/unidades/dtype/orden y casos vacíos, no un dataset que parezca SGC ni cifras para pitch.
- Entorno/máscaras, callbacks, save/load y export; esas pruebas no satisfacen entrenamiento con datos reales.
- UI, estados loading/error/no-support y recorrido de pitch; fuentes/métricas vacías o null mientras no haya evidencia.
- Contrato propuesto: metadata/version/hash/cutoff/targetwindow/variables/provenance; clases/grupos/selección y métricas reales por separado, trace de K elecciones. **Policy logits no se muestran como probabilidad de sismo**.
- Gates obligatorios: export final rechaza fixtures como evidencia oficial; banner visible y fuente real en pantalla, ninguna «métrica» sintética se conserva al cambiar snapshot.

### E. React principal sin convertir API en nuevo requisito

**Ruta mínima propuesta:** Python genera bundle JSON de resultados/trace/metadatos reales; React lo carga y usa como modo presentación. Para **demo viva del modelo**, equipo ejecuta policy entrenada para un cutoff/K permitido y carga resultado recién generado; no es solo maqueta ni una tabla precargada rotulada «inferencia».

Si ya hay puente funcional, usar endpoint fino para policy; si no, carga de archivo generado es válida como integración y evita red/serving nuevos. Misma selección offline/web, hash/model/datos visibles y restricción de K/horizonte coherente. No reutilizar API mock de amenazas naturales como si cumpliera contrato del agente sísmico.

Julián presenta web; Zabdiel explica/ejecuta ML; Nico verifica fuentes/join y recomputación end-to-end. No nuevas diapositivas: secciones de la web hacen el relato. Recorrido sugerido diez minutos: problema/límites1min; datos/provenance2; Básico/Medio2; agente/recompensa/demo3; evaluación/impacto/limitaciones2. Cada integrante participa.

### F. Recortes y fallas

- **SGC tarda >15min:** Nico recorta años/zona/tramos permitidos y usa export manual HTTPS oficial; no sustituye principal por USGS más incompleto sin autorización del evento. Zabdiel/Julián continúan sobre contrato/fixtures, no inventan resultados.
- **08:45 sin panel válido:** reducir scope con corte completo/covariables disponibles; preparar prueba RL mínima sobre fuentes reales. Reportar bloqueo antes de que se consuma ventana; no prometer premios si requisito no se alcanza.
- **No soporte de clases/degeneración:** Zabdiel decide cambio metodológico con Nico sobre train y lo propagan a web/export; no parchear UI para aparentar tres clases entrenadas.
- **GPU/cluster falla:** CPU, redes pequeñas y menos seeds/timesteps documentados. No sacrificar agente funcional por esperar GPU.
- **React falla a10:45–11:00:** fallback Streamlit o cuaderno ejecutable ya probado, mismos modelos/bundle/cutoff; conservar React principal hasta gate, no desarrollar dos interfaces completas en paralelo.
- **API/túnel falla:** demo local. Sitio público no es requisito; no sacrificar reproducibilidad por URL.
- **Modelo no mejora:** entregar entrenamiento y resultado honesto contra baseline; no reemplazar policy por regla sin decirlo. Cumplimiento no asegura desempeño ni premio.

**Recortar primero:** motion/pulido, mapas complejos, radio R, Omori/b municipal, modelos extra y serving remoto. **Nunca:** fuentes reales/diccionario, entrenamiento propio, validación temporal, demo viva y trazabilidad.

## Fuentes y límites de lectura

- [S1] [Scientific Reports2023: estructura/interpretación del nido](https://www.nature.com/articles/s41598-023-50159-4). Se leyó texto científico disponible mediante WebFetch tras redirect; no verificar hipótesis física por cuenta propia.
- [S2] [García-Arias etal.,2026, Towards earthquake forecasting…](https://link.springer.com/article/10.1007/s10950-026-10364-w). Texto sustancial/limitaciones leídos; tabla detallada Mc no recuperada. Su test tiene pocos eventos objetivo; no aval de pronóstico operativo.
- [S3] [USGS profundidad y sacudida](https://www.usgs.gov/faqs/what-depth-do-earthquakes-occur-what-significance-depth).
- [S4] [SGC RSNC periodos y sistemas](https://bdrsnc.sgc.gov.co/paginas1/catalogo/index.php) y [consulta histórica](https://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta/consultaexperta_2.php).
- [S5] [Impact of magnitude uncertainties on seismic catalogue properties,2018](https://academic.oup.com/gji/article/213/2/940/4819287). Secciones metodológicas/resultados accesibles leídos, no cada referencia.
- [S6] [USGS tipos de magnitud](https://www.usgs.gov/programs/earthquake-hazards/magnitude-types).
- [S7] [SGC boletín julio2025](https://www2.sgc.gov.co/Publicaciones/Boletines%20Sismicidad/Bolet%C3%ADn%20Julio%20de%202025.pdf). Solo resultado indexado; PDF demasiado grande para WebFetch.
- [S8] [USGS evento us10001ldx](https://earthquake.usgs.gov/earthquakes/eventpage/us10001ldx). Metadata reviewed verificada mediante consulta GeoJSON del evento/día/región.
- [S9] [SGC comunicado005 de2015](https://www2.sgc.gov.co/Noticias/Paginas/Comunicado%20de%20prensa%20005%20de%202015.aspx). Texto leído; no tipo de magnitud ni estado preliminar/final explícitos.
- [S10] [Aki–Utsu/binning citado en estudio2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10915173/). Fórmula localizada en búsqueda académica; no derivación comprobada con dataset propio.
- [S11] [NHESS2022 Benioff como proxy energético](https://nhess.copernicus.org/articles/22/2543/2022/). Texto leído; no transferir sus conversiones regionales a Colombia.
- Para RL, máscaras/evaluación y oficial: [09-rl-diseno.md](09-rl-diseno.md) y [08-enunciado-oficial.md](08-enunciado-oficial.md).
