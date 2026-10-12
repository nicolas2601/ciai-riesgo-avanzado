# Validación, calibración e incertidumbre

Consulta: 2026-10-12. Protocolo propuesto; no hay métricas ejecutadas. Referencias no sustituyen validar hipótesis de datos.

## Qué se quiere generalizar

**PROPUESTA:** distinguir dos preguntas antes del split:

1. Pronóstico en zonas conocidas: futuro retenido y pasado como train, con embargo suficiente para ventanas/targets solapados.
2. Transferencia territorial: bloques geográficos retenidos; si además se promete futuro en zonas nuevas, retener simultáneamente espacio y tiempo.

Un split espacial no demuestra pronóstico futuro. Uno temporal no demuestra transferencia a otra región. Reportar cuál se probó.

**HECHO:** dependencia espacial/temporal puede volver optimista CV aleatoria. Roberts et al. y blockCV sustentan separación por bloques/buffers; tamaño de bloque no se escoge para maximizar score.

## Diseño mínimo, ajustable a soporte real

- Deduplicar eventos y agrupar inventarios del mismo episodio antes del split; mantener episodio y ventanas muy correlacionadas juntos.
- Definir bloques geográficos con distancia física/estructura del fenómeno. Tamaño inicial es hipótesis; hacer sensibilidad a dos tamaños si alcanza tiempo. H3 por sí mismo no elimina correlación.
- Reservar test externo no usado para tuning. Dentro del conjunto restante, hacer CV por bloques para selección y early stopping.
- Guardar IDs de filas, zonas, fechas, episodios y folds. No basta guardar semilla.
- Para pronóstico, toda feature necesita fecha de disponibilidad; purgar train si horizonte de su etiqueta intersecta ventana retenida. Embargo depende de historial/horizonte, no es un número universal.
- Imputadores, escaladores, encoders, sampling y umbrales de target se ajustan en train de cada fold. No ejecutar SMOTE antes de dividir.
- Si faltan clases por fold, documentar inviabilidad; reducir folds con justificación o cambiar target. No escoger split aleatorio para ocultarlo.

**Tradeoff:** retener espacio y tiempo y reservar calibración reduce tamaño de entrenamiento. Con pocos eventos puede impedir una evaluación fiable; es preferible una limitación explícita a una cifra inflada.

## Separar selección, calibración y test

Modelo seleccionado con train/validación interna. Para usar calibración probabilística y conformal juntas, reservar conjuntos disjuntos:

`train/tuning → calibración probabilística → calibración conformal → test`

El calibrador probabilístico forma parte del predictor fijo antes de calcular scores conformales. No ajustar temperatura y cuantiles conformales sobre las mismas etiquetas como si fueran independientes. No optimizar `alpha`, umbrales o método mirando test.

Si no hay soporte para tantas particiones, priorizar evaluación bloqueada y probabilidades/calibración empírica. Conformal es opcional; no introducir una garantía no defendible para llenar un requisito.

## Métricas

| Objetivo | Métrica | Qué acompañarla |
|---|---|---|
| Clases desbalanceadas | Macro-F1, balanced accuracy | Soporte por clase y matriz de confusión |
| Identificar alto | Recall/precision de alto; PR-AUC one-vs-rest | Prevalencia, presupuesto de alertas; PR-AUC de scores, no labels duros |
| Orden bajo/medio/alto | Error ordinal medio y tasa alto→bajo | Mapping ordinal documentado; no distancias físicas inventadas |
| Probabilidades | Multiclass Brier, log loss, reliability | ECE con bins y soporte; no usar ECE solo |
| Priorización | Recall@K y precision@K | K fijado por capacidad operativa, no por test |
| Sets conformales | Cobertura empírica y tamaño medio | Por región/clase/tiempo; tasa de sets vacíos y abstención |

Comparar modelos sobre mismos ejemplos/folds. Intervalos mediante remuestreo por bloques/episodios, no bootstrap i.i.d. por fila correlacionada. Con pocos bloques, intervalos serán inestables: reportar cantidad y no fingir precisión.

**Criterio de comparación:** solapamiento de intervalos marginales no prueba empate ni descarta diferencia. Analizar intervalo de diferencia pareada por bloques; si es inconcluso, preferir modelo más simple. No afirmar victoria estadística por dos scores puntuales.

## Calibración probabilística

**PROPUESTA:** temperature scaling para logits de red o calibrador apropiado a probabilidades de boosting, ajustado en subconjunto reservado. Comparar reliability/Brier antes y después. Isotonic con poco soporte puede sobreajustar; no adoptarlo automáticamente.

Tres clases ordinales deben conservar un contrato inequívoco de orden. Entropía alta puede señalar ambigüedad de predicción, pero baja entropía no demuestra certeza ni seguridad fuera de distribución.

## Split conformal para clasificación

**HECHO:** garantía estándar es marginal bajo intercambio estadístico apropiado entre calibración y nuevo ejemplo; no garantiza cobertura por cada barrio, clase o input. Spatial CV no crea por sí sola exchangeability.

**PROPUESTA experimental:** predictor fijo con probabilidades `p(y|x)`, score de calibración `s_i = 1 - p(y_i|x_i)` y `alpha = 0.10` predefinido, sujeto a soporte.

- Con `n` ejemplos de calibración, `k = ceil((n + 1) * (1 - alpha))`.
- Si `k <= n`, usar el score ordenado número `k` (índice matemático 1-based), no interpolación lineal.
- Si `k > n`, usar umbral infinito y devolver todas las clases; no bajar el rango artificialmente para aparentar cobertura.
- Devolver `C(x) = {y: 1 - p(y|x) <= q}`. Empates usan `<=`.
- Set de varias clases: revisión humana. Set vacío: abstenerse/señalar anomalía; no escoger una clase silenciosamente.

**Limitación central:** autocorrelación espacial, cambios de observación y shift regional/temporal pueden romper supuestos. Mostrar cobertura **empírica** en holdout y no prometer 90% en producción. Adaptaciones por bloques/ponderación requieren supuestos y validación propios; no se resuelven renombrando el split.

**Tests propuestos:** cuantiles pequeños, caso `k > n`, empates, orden de clases, set vacío, predictor congelado y ausencia de superposición entre particiones.

## Explicabilidad

**PROPUESTA:** SHAP para árboles si tiempo/costo permiten; explicación de red mediante método compatible, no llamar TreeSHAP a un MLP. Para el MVP, explicación global por ablation/permutación bloqueada es alternativa honesta.

- Background de explicación procede de train y se registra; elección de dependencia de features debe ser explícita.
- Pendiente/relieve y ventanas de lluvia pueden estar correlacionados: atribuciones pueden repartirse y no son causalidad.
- Explicaciones describen salida concreta (logit/probabilidad/clase) del modelo, no por qué ocurrió un desastre.
- No presentar simulación what-if como impacto causal de una intervención.
- No usar explicación como prueba de ausencia de leakage.

## Gates de entrega

Test externo intacto; folds guardados; métricas por clase/espacio/tiempo; calibración separada; baseline; limitaciones de cobertura/reporte; una predicción API con mismo preprocesamiento que offline. No hay garantía de seguridad territorial ni aval oficial.

## Fuentes

- [Roberts et al., 2017, DOI](https://doi.org/10.1111/ecog.02881)
- [Valavi et al., blockCV, 2019](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13107)
- [Documentación de bloques y buffers](https://search.r-project.org/CRAN/refmans/blockCV/html/cv_spatial.html)
- [Angelopoulos y Bates: conformal, texto completo v6](https://arxiv.org/html/2107.07511v6)
- [SHAP: dependencias entre features](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html)
- [SHAP: predicción no implica causalidad](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html)
