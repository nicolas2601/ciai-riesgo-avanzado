# Tres ideas diferenciadoras, con límites honestos

Propuestas al 2026-10-12. No implementadas ni validadas con usuarios. Se subordinan a enunciado, datos y contrato API. Orden recomendado: primera idea, luego tercera; segunda solo después de evaluación y serving.

## 1. Mapa que sabe cuándo no sabe

**Problema:** un color de riesgo sin soporte induce falsa precisión y oculta regiones sin datos.

**PROPUESTA:** cada municipio (DIVIPOLA) muestra clase/frecuencia prevista para mes siguiente y, separadamente, calidad de datos, horizonte y necesidad de revisión. Polígono municipal verificado o punto representativo; no ubicación puntual del evento UNGRD. Si set conformal tiene varias clases o falta soporte/OOD verificable, mostrar estado de abstención. No confundir entropía con error de medición ni convertir confianza en garantía de seguridad.

**Panel de decisión:** probabilidad de clase alta cuando esté calibrada, población estimada expuesta separada, antigüedad de datos, versión de modelo y principales factores asociados. No multiplicar población por probabilidad de una clase relativa y llamarlo daño esperado.

**Creatividad defendible:** el mapa informa no solo dónde mirar, sino dónde hace falta mejorar observación. Una zona sin reportes se marca sin reportes, no segura.

**Costo:** API debe exponer status/metadata; calibración y soporte requieren datos reservados. Diseño visual debe usar DESIGN.md y skills UI cuando se implemente; este documento no fija paleta ni crea dashboard.

**Cómo verificar:** caso sin features, set multiclase, datos antiguos y región sin soporte deben verse distintos de bajo riesgo. Medir cobertura/abstención, no afirmar que interfaz por sí sola mejora decisiones.

## 2. Escenarios what-if con semáforo de plausibilidad

**Problema:** un score aislado no permite explorar cómo cambia predicción con lluvia antecedente u otra covariable editable.

**PROPUESTA:** comparar escenario observado con escenario hipotético explícito. Modificar solo covariables definidas y mostrar origen/unidades; controlar consistencia entre acumulados de 1/3/7/30 días. Un slider independiente para cada acumulado produciría combinaciones imposibles.

**Límite central:** se trata de sensibilidad del predictor, no intervención causal ni pronóstico meteorológico. Mantener relieve estático; valores fuera de soporte activan advertencia/abstención. La coherencia multivariable requiere validaciones adicionales al rango univariado.

**Costo:** nuevas validaciones, inferencia y texto de límites. No depende de entrenar otra arquitectura, pero sí de que actual responda de forma razonable a perturbaciones válidas.

**Cómo verificar:** escenario idéntico reproduce salida; escenario inválido se rechaza; fuente observada no se sobrescribe; escenario no actualiza historial real. Verificación de plausibilidad no demuestra causalidad.

## 3. Lista de revisión según capacidad real

**Problema:** un equipo solo puede inspeccionar K zonas; mapa completo no ordena trabajo ni registra por qué se eligieron.

**PROPUESTA:** ranking de municipios para revisión por score aprendido de reportes de una amenaza, acompañado de exposición y calidad separadas. Elegir K según capacidad del equipo, registrar motivos/versiones y marcar municipios inciertos para revisión, no ocultarlos al final de una lista.

**Creatividad defendible:** reporte reproducible de qué se priorizó, cuándo y con qué datos; estados pendiente/revisado y feedback humano que nunca sobrescribe label original.

**Límites:** una alerta de modelo no es alerta oficial de emergencia. No enviar WhatsApp/SMS/correos automáticamente en hackathon; primera versión genera borrador/lista local. Publicación o notificación externa requiere autorización y destinatarios definidos.

**Costo:** ranking/budget y rastro simple; más pequeño que plataforma de alertas. No llamar al ranking optimización multiobjetivo ni utilidad esperada si no existe función de costo y evidencia.

**Cómo verificar:** recall@K/precision@K contra eventos retenidos; mismo snapshot produce misma lista; empate determinista; zona sin datos no se etiqueta segura. Feedback requiere revisión antes de convertirse en entrenamiento.

## Base de evidencia

- Clasificación, cobertura empírica y limitaciones: [protocolo de validación](03-validacion-incertidumbre.md).
- Diferencia entre eventos, covariables y exposición: [datasets y target](01-datasets.md).
- Predicción versus causalidad: [advertencia oficial SHAP](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html).
- Conformal y supuestos: [Angelopoulos y Bates](https://arxiv.org/html/2107.07511v6).
