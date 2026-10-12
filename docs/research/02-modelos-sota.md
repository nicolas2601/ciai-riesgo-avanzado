# Arquitecturas: evidencia y selección pragmática

Consulta: 2026-10-12. No hay benchmark propio. UNGRD municipal verificado en `01-datasets.md`; armonización y soporte de clases pendientes. Estas referencias son fundamentos relevantes, no prueba de que una arquitectura sea el estado del arte actual para Santander.

## Recomendación

**PROPUESTA:** comenzar con gradient boosting sobre features geoespaciales/temporales y compararlo con una red pequeña implementada en PyTorch, entrenada desde pesos aleatorios; TabPFN como tercer candidato opcional. Desplegar el que gane en evaluación bloqueada y calibración, no el que use más GPU. No combinar modelos sin mejora medida.

**HECHO:** estudios de tabular muestran baselines MLP/ResNet fuertes y ningún ganador universal entre deep learning y GBDT. Graph WaveNet y TFT prueban ventajas en sus tareas, no superioridad demostrada para este target territorial.

**PROPUESTA:** tabla municipio (DIVIPOLA validado contra catálogo de 87 municipios) × mes, target de reportes UNGRD del mes siguiente. ~7,300 filas es aproximación antes de armonización, lags y censura final; resolver códigos raw corruptos mediante nombre + departamento y auditar ambiguos. Si no hay suficientes etiquetas, ninguna arquitectura avanzada resuelve ese bloqueo.

## Tres opciones

| Opción | Cuándo encaja | Ventajas | Costos/riesgos | Decisión en 5 h |
|---|---|---|---|---|
| GBDT + features espaciales/temporales; red residual como challenger | Datos tabulares, relieve, lluvia antecedente y etiquetas discretas | Entrenamiento accesible, buen baseline, explicación local | Leakage de agregados; coordenadas pueden memorizar región; red exige tuning | Recomendada |
| GNN / ST-GNN | Grafo justificable de vecindad/cuencas y series por nodo | Modela dependencias espaciales y temporales | Construir grafo, missingness, partición inductiva, cambio de nodos y export; relaciones espurias | Solo con pipeline y datos ya listos |
| TFT o red temporal pequeña | Historial largo por zona y horizonte de pronóstico explícito | Separa covariables estáticas, observadas y conocidas a futuro | Secuencias densas, costo de tuning, variables futuras no disponibles; attention no prueba causalidad | Red pequeña antes que TFT completo |

### A. GBDT espacial/temporal y challenger residual

Una fila representa municipio, mes y fecha de emisión. Features: relieve agregado municipal, lluvia antecedente, estacionalidad y, si procede, historial previo de eventos. Target pertenece a mes futuro definido en `01-datasets.md`; coordenadas de centroides no son ubicaciones de eventos.

**Features a auditar:** imputación, escalado, encoding y estadísticas de vecindad se ajustan dentro de train. Agregados de eventos nunca incluyen etiquetas futuras ni regiones retenidas. Comparar con y sin coordenadas para detectar dependencia de localización.

**Baseline:** predictor de prior de clases y regresión logística; boosting como baseline fuerte/champion candidato. No llamar avanzado a un modelo solo por nombre: entregar ablations, evaluación y manejo de incertidumbre.

**TabPFN opcional:** tercer candidato de costo a medir, no garantía de barato. Ejecutar local con mismos folds espaciales/temporales; fijar paquete, checkpoint y hash. README oficial y Context7 confirman pesos 2.5/2.6 no comerciales y default actual distinto: no asumir que instalar paquete fija versión admisible. Revisar licencia exacta para uso/redistribución antes de descargar/publicar; hackathon académico no implica permiso automático. GPU/acceso a pesos pueden bloquear; omitir si afecta ruta crítica. Es preentrenado: no satisface modelo propio desde cero ni autoriza enviar datos al cliente alojado. Ver [investigación reciente](07-sota-geoespacial.md).

### B. Grafo / ST-GNN

Graph WaveNet combina adyacencia adaptativa y convoluciones temporales dilatadas. Su evidencia original es tráfico METR-LA/PEMS-BAY; transferirlo a amenazas es una hipótesis.

**PROPUESTA:** grafo de vecindad física/cuencas, mensajes espaciales y encoder temporal. No usar un grafo por latitud/longitud sin justificar conectividad del fenómeno. Una relación de vecindad útil para incendio puede ser incorrecta para inundación.

**Gate:** datos temporales por nodo, mecanismo para nodos nuevos y partición espacial sin pasar targets del holdout. Si el grafo usa features de nodos de test, declarar evaluación transductiva; no venderla como generalización inductiva a zonas nuevas.

### C. Temporal: TFT o encoder ligero

TFT utiliza covariables estáticas, entradas temporales observadas y entradas conocidas a futuro, con selección de variables, gating y atención.

**PROPUESTA mínima:** encoder Conv1D o GRU de lluvia/eventos antecedentes y rama MLP para relieve; fusionar embeddings para clasificación. Calendario puede conocerse a futuro; lluvia observada futura no. Pronósticos meteorológicos exigen fuente y fecha de emisión verificadas.

**Gate:** series regulares, suficiente historia y un backtest temporal. Si solo hay puntos estáticos, TFT no encaja. Interpretabilidad de atención no sustituye auditoría de leakage ni explicación causal.

## Modelo propio en PyTorch, sin exagerar novedad

**Significado defendible:** implementación propia de un diseño pequeño con bloques conocidos, entrenamiento desde cero y datos del proyecto. No afirmar arquitectura científicamente nueva ni superior por haber escrito una clase.

**Diseño propuesto `TerritorialRiskNet`:**

- Input tabular: features numéricas escaladas y máscaras de faltantes; embeddings de categorías solamente si existen y tienen política para desconocidos.
- Proyección a dimensión oculta y dos bloques residuales pequeños; salida de tres logits cuando el target tenga tres clases válidas.
- Variante temporal únicamente si existe historial: encoder de secuencia y fusión con embedding estático; no construir ambas variantes sin necesidad.
- Dimensión inicial 64, dropout 0.1 y límite de épocas 50 son **hiperparámetros propuestos**, no óptimos medidos. Early stopping usa validación interna, nunca test.
- Cross-entropy como pérdida inicial. Si se usan pesos de clase o muestreo, estimarlos solo en train y recalibrar sobre distribución objetivo; logits no son automáticamente probabilidades calibradas.
- Semillas múltiples cuando alcance tiempo; guardar pesos, preprocesamiento, orden de features y mapping de clases como una unidad.

**Ablations mínimas:** prior/logística → boosting → red residual → TabPFN opcional; luego quitar lluvia o relieve para medir aporte multifuente. Usar mismos folds y recursos acotados. Híbrido de probabilidades solo si pesos se seleccionan en validación y mejora justifica costo de mantener dos modelos.

## Gates y pre-mortem

1. No hay positivos/clases en folds: revisar target/datos, no complejizar red.
2. Baseline gana: desplegar baseline aprendido y reportar challenger; revisar requisito avanzado contra enunciado real, no inflar resultado.
3. GPU/cluster no disponible: entrenar boosting o red pequeña CPU; hardware comunicado por equipo todavía no está verificado en esta investigación.
4. Export o inferencia fallan: servir runtime nativo ya probado. ONNX no es requisito metodológico.
5. Scores altos solo en split aleatorio: resultado no demuestra generalización territorial; prevalece evaluación bloqueada.

## Fuentes

- [Gorishniy et al., NeurIPS 2021: modelos tabulares](https://proceedings.neurips.cc/paper/2021/file/9d86d83f925f2149e9edb0ac3b49229c-Paper.pdf)
- [Implementación y conclusiones oficiales](https://github.com/yandex-research/rtdl-revisiting-models)
- [Wu et al., Graph WaveNet, IJCAI 2019](https://www.ijcai.org/proceedings/2019/264)
- [Lim et al., TFT, 2021](https://doi.org/10.1016/j.ijforecast.2021.03.012)
- [Documentación PyTorch/ONNX consultada mediante Context7](https://github.com/pytorch/pytorch/blob/main/docs/source/onnx.md)
- [TabPFN: README oficial y licencias; documentación consultada con Context7](https://github.com/PriorLabs/TabPFN)
