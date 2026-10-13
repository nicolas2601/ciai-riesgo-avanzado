# Diseño RL defendible: priorización exploratoria sísmica

Consulta: 2026-10-13. **PROPUESTA**, no implementación ni resultado. Requisitos oficiales en [08-enunciado-oficial.md](08-enunciado-oficial.md). Documentación Gymnasium, SB3 y SB3-Contrib verificada con Context7; consultas `library` → `docs`, exit 0. Acceso efectivo a datasets SGC/DANE y soporte de episodios pendientes de gate.

## 1. Decisión recomendada y límites

Construir un **entorno de planificación secuencial de seguimiento territorial**: en una fecha de corte, seleccionar hasta K municipios distintos para análisis/revisión prioritaria del mes siguiente. El agente aprende a maximizar cobertura de actividad sísmica registrada futura, opcionalmente ponderada por exposición poblacional oficial.

**HECHO:** Avanzado exige agente RL entrenado y estados/acciones/recompensa; no acepta sustitutos. Exige sismicidad SGC + otra fuente oficial, ≥20 variables, orden temporal y priorización exploratoria. No exige API ni algoritmo particular.

**INFERENCIA:** esta tarea de decisión es más defendible que afirmar que RL predice cuándo ocurrirá un terremoto o que enviar inspectores reduce su magnitud. Agente prioriza seguimiento, no interviene sobre física sísmica.

**SUPOSICIÓN a confirmar:** municipio es unidad útil de análisis y K representa capacidad limitada de revisión. Usar los 87 municipios solo si catálogo/límites/joins y cobertura permiten universo completo. K=5 es parámetro inicial de demo, no capacidad real de una autoridad.

**Límite clave:** epicentro municipal, población y magnitud no miden sacudida/daño. Sismos profundos frecuentes del Nido de Bucaramanga pueden dominar actividad sin dominar impacto superficial. No llamar al score probabilidad de daño, seguridad, alerta oficial ni mapa de amenaza física validado.

## 2. Tres componentes para cumplir herencia

| Componente | Entrada | Aprendizaje / salida | Verificación |
|---|---|---|---|
| Básico | Features previas por municipio-periodo | Clasificador supervisado bajo/medio/alto de actividad futura | Matriz confusión, accuracy, macro-F1/recall y soporte |
| Medio | Descriptores sísmicos/territoriales disponibles al corte | Clustering no supervisado; comparar KMeans con otro enfoque pequeño si tiempo permite | Evaluación interna/estabilidad, interpretación de grupos y mapa reproducible |
| Avanzado | Estado del plan, features y presupuesto | Agente RL entrenado genera selección ordenada de municipios | Retorno/backtest temporal y comparación de políticas |

El clasificador puede servir como baseline/ranker; no reemplaza agente RL. Clusters no son etiquetas oficiales de riesgo. Entrenar modelos dentro de train; cluster del futuro recalculado sobre test completo es fuga si luego se usa en policy.

**Target supervisado propuesto:** máximo de magnitud registrada en **mes siguiente**: bajo si no M≥3, medio si hay M≥3 pero no M≥4, alto si hay M≥4, siguiendo ejemplo oficial adaptado a ventana mensual. No incluir magnitudes de ese mes en features. Revisar escala de magnitud/homogeneización y soporte antes de congelar; si mes da clases inviables, otra ventana justificada, sin mezclar fuentes ni fabricar positivos.

## 3. Datos y tiempo: contrato previo al entorno

- Fuente principal SGC RSN; unificar consultas antes/después de marzo 2018, unidades, zona horaria, nombres, escala de magnitud y duplicados.
- Fuente adicional mínima DANE población/vivienda con producto, año, URL y publicación verificables. Una columna sintética de población no cumple integración.
- Unidad final: municipio × fecha de corte; CSV integrado y diccionario. Geometría/centroide desde catálogo oficial, no inventados.
- Eventos pueden afectar varias zonas aunque epicentro esté fuera de Santander. Para primer proxy, declarar **actividad localizada según catálogo**; una ventana/buffer mayor necesita regla verificable y no demuestra área afectada.
- Features `X(z,t)` solo usan datos disponibles a `t`. Resultados oficiales posteriores `Y(z,t+1)` son recompensa/label, nunca observación.
- Si DANE publica producto después de `t`, no usarlo como exposición disponible en backtest de `t`: iniciar evaluación después de publicación o buscar producto histórico. No convertir población 2018 en observación de 1993.
- Último periodo sin seguimiento completo se elimina de episodios evaluables; no rellenar con cero. Ausencia de evento en catálogo completo ≠ ausencia de amenaza física.
- Catálogo revisado hoy puede contener correcciones que no estaban publicadas en fecha histórica. Si no hay snapshots originales, declarar backtest con catálogo retrospectivo/revisado, no operación as-of plenamente demostrada.

## 4. ≥20 variables justificadas, no relleno

**PROPUESTA de diccionario candidato:** medir disponibilidad real antes de prometer 20. `12m` termina en cutoff; `1m` es último mes cerrado. Calidad instrumental es covariable de observación, no factor causal del sismo.

| # | Variable candidata | Fuente / unidad | Justificación y condición |
|---|---|---|---|
| 1 | count_events_1m | SGC / eventos | Actividad reciente |
| 2 | count_events_3m | SGC / eventos | Contexto corto |
| 3 | count_events_12m | SGC / eventos | Actividad histórica anual |
| 4 | count_m_ge_3_1m | SGC / eventos | Actividad relevante reciente |
| 5 | count_m_ge_3_12m | SGC / eventos | Frecuencia pasada de umbral oficial ejemplificado |
| 6 | count_m_ge_4_12m | SGC / eventos | Frecuencia pasada de mayor magnitud |
| 7 | mean_magnitude_12m | SGC / escala declarada | Centro de distribución |
| 8 | max_magnitude_12m | SGC / escala declarada | Extremo previo, NO futuro |
| 9 | std_magnitude_12m | SGC / escala declarada | Dispersión; desconocida con soporte insuficiente |
| 10 | mean_depth_12m | SGC / km | Contexto profundidad |
| 11 | std_depth_12m | SGC / km | Variación profundidad |
| 12 | share_depth_lt_70km_12m | SGC / proporción | Separar actividad superficial/intermedia; umbral convencional, no prueba de daño |
| 13 | days_since_last_event | SGC / días | Recencia/censura declarada |
| 14 | mean_rms_12m | SGC / segundos, verificar esquema | Calidad de localización; gate disponibilidad |
| 15 | median_gap_12m | SGC / grados, verificar esquema | Cobertura azimutal; gate disponibilidad |
| 16 | mean_phases_12m | SGC / fases | Soporte instrumental; gate disponibilidad |
| 17 | share_events_with_quality_12m | SGC / proporción | Cambios de observabilidad; faltantes no se ocultan |
| 18 | municipality_latitude | Catálogo oficial / grados | Localización representativa, no epicentro |
| 19 | municipality_longitude | Catálogo oficial / grados | Localización representativa, no epicentro |
| 20 | population | DANE / personas | Exposición, con año/publicación verificables |
| 21 | dwelling_count | DANE / viviendas | Exposición habitacional, no fragilidad estructural |
| 22 | municipality_area | Geometría oficial / km² | Escala territorial, CRS métrico |
| 23 | population_density | DANE + área / personas por km² | Concentración de exposición |
| 24 | dwelling_density | DANE + área / viviendas por km² | Concentración habitacional |

No afirmar todas disponibles. Si campos RMS/gap/fases o geometría/vivienda faltan, sustituir por derivadas sísmicas justificadas con fuentes reales; cerrar gate ≥20 antes de entrenar. Identificador, target, reward y máscara del entorno no inflan número de variables de datos. Estadísticas sin eventos no son cero automáticamente; imputar desde train y conservar soporte.

## 5. Entorno Gymnasium: estado, acción y transición

**PROPUESTA `SeismicPrioritizationEnv`:** un episodio por fecha histórica con datos suficientes; agente genera plan de K elecciones antes de conocer resultado del mes siguiente.

**Observación:** matriz de features `X_t` de municipios en orden DIVIPOLA fijo, máscara de municipios ya seleccionados, presupuesto restante, y cobertura del plan por grupo/provincia si realmente se usa. Estandarizador solo train; datos ausentes tienen flags y política explícita. No entregar `Y_future`, reward futuro por municipio ni `info` con labels antes de cerrar plan.

**Acción:** `Discrete(N)` = seleccionar índice municipal para seguimiento. Máscara válida: municipio no seleccionado y con datos habilitantes. No reordenar mapping entre train/inferencia. `K <=` municipios válidos.

**Transición:** actualizar selección y presupuesto; features de contexto permanecen congeladas durante planificación. La acción modifica recursos/plan, NO crea o elimina sismos. Costos de viaje/beneficio de inspección no observados no se inventan.

**Recompensa intermedia:** cero. **Terminal:** evaluar plan contra sismicidad futura oficial, una vez completado K. Esto impide revelar actividad futura del municipio seleccionado y adaptar siguientes elecciones con información que no existía en fecha de corte.

**Terminación:** al completar presupuesto, `terminated=True`; fin natural del episodio, no truncamiento artificial. Si imposibilidad por datos, no hacer pasar fallo por episodio válido. `truncated` para límite técnico externo con semántica documentada.

**Acción inválida:** máscara en entrenamiento e inferencia; entorno también debe manejar validación de acciones sin bucle infinito. Para checker que muestrea acciones sin máscara, definir respuesta determinista segura, sin premiar repetidos ni gastar presupuesto ficticio; tests comprueban contrato. No lanzar excepción aleatoria en rollout normal ni silenciar inválidos como selección nueva.

**HECHO técnico:** Gymnasium separa reset `(obs, info)` y step `(obs, reward, terminated, truncated, info)`. `reset(seed=...)` debe usar RNG del entorno. SB3-Contrib documenta máscaras y evaluación específica para MaskablePPO; PPO base no es sustituto de esa integración.

## 6. Recompensa real: observación versus utilidad diseñada

**No hay recompensa de impacto causal observada:** no tenemos log de intervenciones, daños evitados ni resultados de inspección. Catálogo + DANE no permite afirmar esos beneficios. Diseñar utilidad sobre datos reales es válido como proxy declarado, no como outcome causal medido.

**Opción recomendada:** `y(z,t+1)=1` si catálogo registra al menos un evento M≥3 localizado en municipio durante mes siguiente, `0` si ventana completa no registra ninguno. Umbral procede del ejemplo oficial; es actividad, no daño. Si soporte de M≥3 resulta insuficiente, elegir otro objetivo justificado antes de test.

Exposición opcional en utilidad: `w(z,t)=clip(log1p(population(z,t))/c_train, 0, 1)`, donde `c_train` es escala positiva congelada de train. DANE debe existir antes del corte y join estar verificado. Esto es una **preferencia normativa de seguimiento de zonas pobladas**, no evidencia de personas afectadas.

Para conjunto seleccionado `S_K`, retorno terminal propuesto:

`R_t = (1/K) * sum[w(z,t) * y(z,t+1) for z in S_K]`

- Valores futuros salen de eventos reales, no predicción de nuestro clasificador ni sort de magnitud pasada. Pesos salen de fuente adicional real; fórmula es decisión de utilidad y se registra.
- Contar actividad significativa una vez por municipio/ventana reduce premio artificial a miles de microeventos del nido; comparar sensibilidad por profundidad/magnitud y advertir asociación con epicentro, no sacudida.
- Si población no pasa gate, usar recompensa unweighted `sum(y)/K` y fuente adicional verificada en estado; no sintetizar exposición para mantener fórmula. Si no hay segunda fuente oficial verificable, Avanzado no cumple gate.
- Publicar retorno ponderado y cobertura no ponderada para no ocultar municipios pequeños. Revisar concentración territorial y sensibilidad a pesos.
- No usar daño por incendio/inundación UNGRD como recompensa sísmica; no atribuir daños a sismos solo por coincidir mes/municipio.

**Tradeoff metodológico:** con utilidad aditiva y sin efectos de intervención, selección secuencial equivale a optimización combinatoria contextual top-K; un ranker competente puede igualar/superar RL. El agente es RL si aprende de transiciones/retornos, pero no se afirma que RL sea necesario o superior. No fabricar dinámica física ni bonificaciones decorativas para disimular esta limitación. Diversidad por provincias solo si existe objetivo operativo explícito, con coeficiente predefinido y análisis separado, no requisito inventado.

## 7. Algoritmo y costo

| Alternativa | Encaje | Tradeoff / decisión |
|---|---|---|
| **MaskablePPO SB3-Contrib, PyTorch** | Acciones discretas, máscara y actor-critic desde inicialización nueva | Recomendado para cuatro horas; menos código frágil. Necesita entorno probado, rollout/backtest y pesos realmente entrenados |
| PPO propio PyTorch | Misma tarea, implementación transparente | Más riesgo: GAE/terminales, máscaras, log-prob ratios y minibatches. Solo si ya existe implementación validada; no requerido por enunciado |
| DQN propio PyTorch | Discrete(N), replay y Q-values | Puede reutilizar muestras, pero requiere target network, exploración y máscara también en max bootstrap; complejidad sin beneficio probado. DQN base SB3 no resuelve automáticamente selección enmascarada |

Policy pequeña inicializada al azar; aprender de train histórico. SB3 usa PyTorch y no implica cargar agente preentrenado. GPU no necesaria por defecto; medir costo real. El enunciado exige entrenamiento por equipo, no inventar PPO.

**PROPUESTA inicial:** gamma=1 para objetivo terminal finito sin preferencia artificial por orden; batch/rollout/learning-rate se fijan en config y tuning usa validación temporal. Presupuesto de timesteps se limita por reloj, no se promete convergencia. Repetir misma historia 100,000 pasos no crea 100,000 periodos independientes.

**Máscaras:** usar en learn y `predict`; conservar máscaras originales para reevaluar log-probs en PPO. Evaluación/callback de `sb3_contrib.common.maskable`, no evaluación genérica que ignore máscara. Mismas restricciones de selección para baselines.

**Demostración de entrenamiento:** curva retorno train/validación, policy pesos iniciales versus finales, seed/config/timesteps/hash, selección generada por red sin regla que reordene resultado. Medir mejora, no asumirla. Checkpoint fallido no habilita llamar al mock agente.

## 8. Baselines y oracle

1. **Aleatorio sin reemplazo**, mismo K y municipios elegibles, varias seeds; distribución de retorno.
2. **Regla por magnitud previa**, top-K por máximo registrado en ventana anterior, empate determinista. Baseline explícito, nunca sustituto RL.
3. **Ranker supervisado**, entrenado solo train para actividad futura; ordenar score objetivo consistente con reward. Si hay pesos poblacionales, adaptar score de utilidad y declarar mapping; no comparar objetivos diferentes.
4. **Oracle ex post**, top-K de `w*y` observado futuro, solo cota de referencia evaluativa. Nunca feature, política desplegada ni tuning de test.

Para clasificación Básico, baseline de clase mayoritaria/prior además de métricas reales. Para clustering Medio, grupos se interpretan sin fingir que cluster 0 significa bajo riesgo oficial.

## 9. Validación temporal y del agente

- Fechas ordenadas; train temprano, validación posterior, test final intacto. Proporciones concretas dependen de disponibilidad/cambios SGC/DANE; no fijar años con datos aún no descargados.
- Walk-forward si tiempo/episodios permiten. Todos los municipios del mismo cutoff van a misma partición temporal; no partir filas aleatoriamente.
- Purga si target/horizonte train intersecta test. Features anteriores al test pueden usar pasado real conocido; no purgar arbitrariamente todo historial útil.
- Scaling, clustering, labels thresholds si aprendidos, policy, calibradores y reward scale solo train/validación autorizadas, no test.
- Recompensa de test se revela **solo tras seleccionar todo S_K**. No adaptar parámetros, plan ni stop criteria con outcomes de test.
- Test evalúa policy congelada y baselines en mismos cutoffs y constraints. Log episodio: cutoff/selecciones/budget/retorno/referencia/model hash.
- Métricas: retorno medio/mediana, precision@K de actividad, recall@K de municipios activos (indefinido cuando ninguno activo: reportar aparte), gap a oracle, cobertura poblacional proxy claramente nombrada y concentración territorial.
- Intervalos de diferencias pareadas por bloques de meses/años/episodios correlacionados, no por millones de pasos de simulación. Separar variabilidad de seed de variabilidad entre periodos; con pocos bloques reportar limitación.
- Evaluar selección de varias seeds cuando alcance tiempo. Agente estable no significa generalización; misma fecha repetida no es evidencia adicional.

**No afirmar off-policy causal evaluation:** observamos futura actividad de todos los municipios, así que es backtest full-information de proxy bajo dinámica exógena. Si quisiéramos beneficio real de intervenciones, necesitaríamos logs de acciones/recompensas/propensities y supuestos causales; no existen en este MVP.

## 10. Incertidumbre y explicabilidad del agente

**Ruta mínima recomendada:** intervalos del retorno fuera de muestra + explicación de objetivo/selección y sensibilidad a covariables/weights. Rúbrica acepta incertidumbre **o** explicación; no es obligatorio conformal de RL.

- Actor softmax es distribución de acciones condicionada a estado/máscara, **no** probabilidad de terremoto ni clase alta.
- Q-value/critic estima retorno bajo entorno/objetivo diseñado, no daño esperado real ni severidad física.
- Comparar frecuencia de selección por seeds y perturbaciones plausibles, con máscara/objetivo constantes; estabilidad es diagnóstica, no cobertura garantizada.
- Sensibilidad a excluir población, profundidad/epicentros y proxies de calidad ayuda detectar que agente memoriza municipios grandes o esfuerzo de registro.
- Mostrar por municipio historial previo, exposición con año y cluster territorial, separados de atribución causal. Si SHAP se aplica a policy, especificar salida y fondo; no reutilizar TreeSHAP del baseline como explicación del agente.
- Abstenerse ante features ausentes, catálogo obsoleto/no completo o zonas fuera de soporte; no emitir prioridad como segura.

## 11. Riesgos y gates antes de entrenamiento

| Falla probable | Gate / mitigación |
|---|---|
| No alcanza catálogo SGC export/unificación | Recortar años/área con filtros documentados; SGC sigue principal. Otra fuente no sustituye obligación |
| No hay ≥20 variables reales justificadas | Completar diccionario/derivadas válidas; no inventar columnas ni contar target como feature |
| RL sin transiciones/reward real | Implementar entorno/checker y tests; agente aprende retorno, no wrapper de sort |
| Reward sparse o trivially constant | Medir soporte por periodo/unidad antes de elegir ventana/K/threshold; ajustar en train, no test |
| Recompensa de daño inventada | Utilidad exploratoria de actividad/exposición, sin afirmaciones causales |
| Rewards intermedias revelan futuro | Cero hasta terminal; no future outcomes en obs/info durante planificación |
| Repetición municipal/inválidos | Máscara en policy, bootstrap/eval y invariantes del entorno |
| Agente memoriza replay | Periodos retenidos, seeds, baseline, no equiparar timesteps a datos independientes |
| Mezcla SGC, UNGRD y censos temporalmente inválida | Disponibilidad as-of, mapeo oficial y provenance; no cross-hazard reward |
| API/pulido consume ventana | Notebook o flujo mínimo reproducible y mapa; web/API opcional |

**Tests de lógica propuestos:** cutoff no incluye futuro; episodio sin seguimiento rechazado; rewards cero hasta terminal; misma seed reproduce; seleccionados no se repiten; all-zero outcomes tienen reward0; K inválido falla al borde; reward sum corresponde a rows oficiales; mapping municipal estable; checkpoint roundtrip; máscara train/eval; final natural no bootstrapea futuro.

**Artefactos mínimos:** CSV+dicionario/fuentes, módulo entorno/config/tests, modelos supervisado/no supervisado/policy entrenados, splits y curvas/métricas de validación, selección reproducible y pitch. Flujo: fuentes → tabla → Básico/Medio → entorno → agente → backtest → selección/mapa. MLflow útil si ya listo; logging local recuperable si servidor falla.

## Fuentes

- [Oficial CIAI y export completo](08-enunciado-oficial.md).
- [Gymnasium entorno propio](https://gymnasium.farama.org/introduction/create_custom_env/).
- [Gymnasium checker](https://gymnasium.farama.org/api/utils/).
- [SB3 consejos de selección/evaluación](https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html).
- [SB3 DQN](https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html).
- [MaskablePPO: masks y evaluación](https://sb3-contrib.readthedocs.io/en/master/modules/ppo_mask.html).
- [USGS: profundidad y sacudida superficial](https://www.usgs.gov/faqs/what-depth-do-earthquakes-occur-what-significance-depth).
- [USGS: magnitud versus efectos/daño](https://pubs.usgs.gov/gip/earthq1/measure.html).
- [Agarwal et al., NeurIPS2021: evaluación RL y pocos seeds](https://arxiv.org/abs/2108.13264).
- [Wang et al., 2017: off-policy contextual bandits](https://proceedings.mlr.press/v70/wang17a.html).
