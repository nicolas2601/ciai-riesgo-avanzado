# MLOps mínimo: reproducibilidad y serving

Consulta: 2026-10-12. Documentación de MLflow, DVC, Hydra, Evidently, FastAPI y PyTorch obtenida vía Context7 (`library` → `docs`, exit 0). No se verificó instalación, cluster, servicio remoto ni export de modelo.

## Recomendación para cinco horas

**PROPUESTA:** MLflow + configuración resuelta + manifiesto de datos + artifact bundle + FastAPI. DVC si existe storage compartido; Hydra si configuración ya está lista; Evidently y ONNX después del camino end-to-end. No convertir seis herramientas en seis bloqueos.

**HECHO:** cada herramienta cubre una capa distinta. Tracking no almacena automáticamente todos los datos recuperables; versionar un hash no permite reconstruir bytes ausentes; exportar ONNX no incluye necesariamente features geoespaciales ni calibración externa.

## Roles de herramientas y costo

| Herramienta | Función respaldada por documentación | Alcance propuesto / costo |
|---|---|---|
| MLflow | Parámetros, métricas, modelos, artefactos, firma y datasets de corrida | Esencial; aprovechar servidor comunicado por equipo solo tras verificar acceso |
| DVC | Metadatos en Git y datos/modelos en cache/remote | Útil para compartir snapshots; exige storage disponible y permisos |
| Hydra | Composición de configuraciones, overrides y multirun | Útil si ya integrado; YAML validado y guardado basta para MVP pequeño |
| Evidently | Evaluación de calidad/drift y reports | Un informe offline opcional; no desplegar plataforma de monitoreo en primera entrega |
| FastAPI | Validación de entrada y lifecycle de servicio | Servir bundle una vez cargado; límites explícitos y endpoint de readiness |
| ONNX | Representación/export del grafo para runtime compatible | Opcional; gate de operadores y paridad, no asumir speedup |

## Contrato reproducible por corrida

Guardar como artefactos/tags en MLflow:

- SHA de código y estado dirty. Un SHA con modificaciones sin guardar no reproduce corrida: guardar diff sin secretos o exigir snapshot limpio autorizado.
- Fuentes, producto/versión, URL, licencia, acceso, región/fechas, CRS, tamaño y hash SHA-256 de archivos raw/processed.
- Snapshot recuperable o ruta de storage versionada. No depender de URL mutable ni endpoint NRT que reemplaza históricos.
- Configuración **resuelta**, semilla, versions/lockfile, hardware/runtime, opciones deterministas y limitaciones conocidas. Una semilla no garantiza igualdad bit a bit entre CUDA/platforms.
- Definición target municipio (DIVIPOLA) × mes, horizonte mes siguiente, mapping de clases, umbral, catálogo de 87 municipios y cobertura de reporte. Registrar filtro exacto de Santander: substring incluye Norte de Santander. Auditar join nombre normalizado + departamento contra catálogo, códigos raw corruptos y ambiguos rechazados. Sin seguimiento completo, target ausente, no cero.
- IDs de folds (clusters de centroides o provincias), municipios y episodios, features en orden, transformaciones ajustadas, hiperparámetros, historia de entrenamiento y selección. Para TabPFN opcional, paquete/checkpoint/hash/licencia y contexto de entrenamiento por fold.
- Métricas por fold/clase, tamaño/soporte, intervalos y reporte de test externo; no mezclar train/test en mismo nombre de métrica.
- Preprocesador, pesos/modelo, calibrador, cuantiles conformales si existen, firma, input example y ejemplos de paridad offline/API.

**MLflow:** manual tracking es suficiente. Autologging no reemplaza manifests geoespaciales, ventanas ni splits del proyecto. Input signature sirve para contrato técnico, no garantiza semántica causal o fecha de disponibilidad.

## DVC y alternativa mínima

**HECHO:** `.dvc`/`dvc.lock` se versionan en Git; datos grandes se conservan en cache/remote. Subir metadatos Git sin subir bytes a storage no comparte dataset.

**PROPUESTA:** usar DVC únicamente si remote ya funciona y términos permiten almacenamiento. Sin remote, mantener snapshot local compartido por canal autorizado, manifiesto y hash; describir explícitamente limitación de recuperación. No llamar a esto versionado distribuido completo.

Credenciales de storage/MLflow fuera del repo. No crear cuentas, buckets ni subir datos a servicios nuevos como parte automática de documentación.

## Configuración y pipeline

Etapas propuestas: ingest → validación → features → split → entrenamiento → calibración → evaluación → bundle → smoke API.

Hydra permite sweeps, pero guardar interpolaciones evaluadas: valores basados en hora/entorno pueden cambiar al repetir. Paths absolutos/controlados y salida por run evitan que cambios de cwd alteren lectura/escritura. Lockfile fija dependencias; configuración sola no las fija.

**Gate:** repetir comando desde ambiente limpio autorizado recupera mismas fuentes/splits y resultados dentro de tolerancia documentada; no prometer reproducibilidad bit a bit sin comprobarla.

## Serving FastAPI

**HECHO:** documentación recomienda cargar recursos con `lifespan`; pruebas con context manager disparan startup/shutdown.

**PROPUESTA de diseño, subordinada al contrato del equipo:**

- Cargar bundle verificado una vez en startup; readiness falla si faltan pesos/preprocesador o mapping compatible.
- API pública recibe municipio/DIVIPOLA y fecha; resolver features a partir de snapshot municipal precomputado. No inferir ubicación puntual de eventos UNGRD desde centroides ni descargar rasters/entrenar dentro de cada petición.
- Separar inferencia de construcción de features y documentar si API solo acepta features precalculadas, en vez de prometer resolución territorial inexistente.
- Validar CRS, rangos, fechas, unidades, valores finitos y límites de lote/body. Número máximo se fija con prueba real, no se inventa throughput.
- Respuesta incluye versión/hash de modelo, snapshot, horizonte, probabilidades calibradas cuando lo estén, target, clase y motivo de abstención cuando aplique.
- Timeout, errores tipados, logs estructurados sin información sensible. No devolver una clase por defecto ante fallo del modelo.
- Restricciones de acceso, CORS específico y límites antes de exposición pública; túnel no equivale a autenticación.

CPU como primera ruta de inferencia para modelo pequeño; medir latencia y memoria. Multiplicar workers también duplica modelos y puede agotar VRAM. GPU se justifica por benchmark, no por disponibilidad.

## ONNX: gate de compatibilidad

PyTorch documenta export y verificación contra ejecución nativa. Export exitoso no prueba que pipeline completo sea idéntico.

**PROPUESTA:** fijar opset/runtime compatibles; comprobar batch 1 y batch máximo, faltantes procesados, features en orden y salidas de borde. Comparar scores con tolerancia predefinida y labels/sets en proximidad de umbrales. Mantener preprocesamiento/calibración idénticos.

Si paridad falla o export consume ventana de entrega, servir runtime nativo ya verificado y documentar export pendiente. No afirmar reducción de latencia sin medir ambos.

## Drift y operación

Evidently compara distribuciones/quality; drift sin etiquetas no demuestra pérdida de precisión. **PROPUESTA:** registrar missingness, out-of-range, tasa de abstención, versión/edad de fuente, latencia y distribución de predicciones por región/tiempo. Cuando lleguen labels, medir desempeño/calibración retardados.

Estacionalidad y cambios de satélite pueden producir drift esperado o artefactual. No reentrenar automáticamente por una alerta. Revisar fuente y soporte con responsable humano.

## Escalabilidad y rollback

- Recortar COG por ventanas y cachear agregados; tabla procesada particionada por región/fecha si volumen lo exige. No cargar raster global para consulta puntual.
- Precalcular predicciones municipales para mapa; evitar inferencia por cada píxel visible. Mostrar polígonos verificados o puntos representativos, no heatmap puntual de eventos inexistentes.
- Bundle inmutable: cambiar versión mediante publicación controlada; preservar versión previa y endpoint de versión.
- Falla cluster: entrenamiento pequeño local y tracking local pendiente de sincronización.
- Falla fuente/túnel: mostrar snapshot y su antigüedad; no decir tiempo real. Demo local como fallback, sin inventar disponibilidad pública.

**Pre-mortem:** bytes perdidos, target cambió, API recibió features distintas, dependencia CUDA incompatibile o fuente nueva rompió observabilidad. Manifiesto, bundle conjunto, validación de contrato y rollback abordan esas fallas antes que más infraestructura.

## Fuentes

- [MLflow tracking](https://github.com/mlflow/mlflow/blob/master/docs/docs/classic-ml/tracking/tracking-api/index.mdx)
- [MLflow datasets](https://github.com/mlflow/mlflow/blob/master/docs/docs/classic-ml/dataset/index.mdx)
- [MLflow signature](https://github.com/mlflow/mlflow/blob/master/docs/docs/classic-ml/model/signatures/index.mdx)
- [DVC remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage)
- [DVC push](https://dvc.org/doc/command-reference/push)
- [Hydra configuración/sweeps](https://hydra.cc/docs/patterns/configuring_experiments)
- [Hydra advertencias de rerun e interpolación](https://hydra.cc/docs/experimental/rerun)
- [Evidently](https://github.com/evidentlyai/evidently)
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/)
- [Pruebas de lifecycle](https://fastapi.tiangolo.com/advanced/testing-events/)
- [PyTorch ONNX](https://github.com/pytorch/pytorch/blob/main/docs/source/onnx.md)
- [PyTorch verificación ONNX](https://github.com/pytorch/pytorch/blob/main/docs/source/onnx_verification.md)
