# Contrato API (frontera ML <-> web)

Version: v0.2. Congelar en el hito H0; cualquier cambio se avisa a Zabdiel y Julian. Esta version es ejecutable: `app/api/tests/test_contract.py` verifica cada regla contra el mock (`uv run pytest app/api`). La implementacion real debe pasar los mismos tests.

Cambios respecto a v0.1, tras la revision cruzada con uts2: probabilidades por clase en lugar de un intervalo sobre un score; conjunto de prediccion conformal; ventana temporal explicita; identificador de snapshot en todas las respuestas; liveness separado de readiness; marca de mock inequivoca.

Base: `/api/v1`. JSON UTF-8. Zona = municipio por codigo DIVIPOLA (string de 5 digitos, ej. `"68001"`); 87 municipios de Santander. Nunca se usa el codigo crudo de UNGRD: se resuelve por nombre normalizado (ver `docs/research/06-datos-colombia.md`).

## Definiciones

- **Objetivo**: nivel de riesgo de la amenaza `hazard` en el mes `target_month`, derivado de conteos de emergencias reportadas (regla de `docs/research/01-datasets.md`). Es frecuencia relativa de reportes, no severidad ni alerta oficial.
- **`hazard`**: `"wildfire" | "landslide" | "flood"`. Solo se aceptan los listados en `supported_hazards` de `/ready`; los demas se rechazan.
- **`target_month`**: `"YYYY-MM"` entre `2019-01` (inicio de la serie UNGRD) y `2099-12`; fuera de ese rango, 422. Por defecto, el mes siguiente a `data_available_through`.
- **`feature_cutoff`**: ultimo dia cuyos datos pueden usarse = dia anterior al inicio de `target_month`.
- **`data_available_through`**: ultima fecha con datos realmente disponibles en el snapshot. Si es anterior a `feature_cutoff`, la API se abstiene (`abstain_reason = "stale_data"`) en lugar de predecir.
- **Snapshot**: campos `model_version`, `data_version`, `hazard`, `target_month`, `feature_cutoff`, `is_mock`. Estan en TODAS las respuestas de datos (predict, zones, ranking, explain, metrics). La web debe pedir zones, ranking y explain con el mismo `hazard` y `target_month` para que sean coherentes.

## Probabilidades, nivel y conjunto de prediccion

- `class_probabilities`: `{ "low": p, "medium": p, "high": p }`, suma 1. Probabilidades calibradas del modelo ordinal.
- `risk_level`: la clase de mayor probabilidad (argmax). No se obtiene con umbrales sobre un score.
- `risk_score`: igual a `class_probabilities.high`. SOLO para ordenar el ranking; no es el nivel.
- `prediction_set`: conjunto de clases del split conformal (puede tener 1, 2 o 3 clases) con `conformal_alpha` (0.1). Si contiene las tres clases, la API se abstiene (`abstain = true`, `abstain_reason = "wide_set"`).
- La cobertura conformal es EMPIRICA: se mide en validacion y se publica en `/metrics`; no se promete en produccion.
- `abstain_reason`: `"stale_data" | "wide_set" | "low_support" | null`. Con `stale_data`, `class_probabilities`, `risk_level` y `risk_score` son `null` y `prediction_set` es `[]`.

## Errores

`{ "error": { "code": "string", "message": "string" } }`. Codigos: `zone_not_found` (404), `validation_error` (422, incluye hazard no soportado o `target_month` mal formado), `not_ready` (503).

## Endpoints

### GET /health
Liveness: `{ "status": "ok" }`.

### GET /ready
Readiness; la web lo llama al iniciar.
```json
{
  "ready": true,
  "is_mock": true,
  "model_version": "mock",
  "data_version": "mock-data",
  "supported_hazards": ["wildfire", "landslide", "flood"],
  "target_month": "2026-10",
  "feature_cutoff": "2026-09-30",
  "data_available_through": "2026-09-30"
}
```

### POST /predict
Entrada: `{ "zone_id": "68001", "hazard": "wildfire", "target_month": "2026-10" }` (`hazard` y `target_month` opcionales).

Respuesta:
```json
{
  "model_version": "string", "data_version": "string", "hazard": "wildfire",
  "target_month": "2026-10", "feature_cutoff": "2026-09-30", "is_mock": false,
  "zone_id": "68001", "municipality": "Bucaramanga",
  "abstain": false, "abstain_reason": null,
  "class_probabilities": { "low": 0.2, "medium": 0.3, "high": 0.5 },
  "risk_level": "high", "risk_score": 0.5,
  "prediction_set": ["high", "medium"], "conformal_alpha": 0.1,
  "top_factors": [ { "feature": "rainfall_30d", "shap": 0.18, "value": 212.4 } ]
}
```

### GET /zones
Query: `hazard`, `target_month`, `level` (todos opcionales). GeoJSON `FeatureCollection` con el miembro extra `snapshot` (campos del snapshot). Cada feature: `geometry` (punto en el centroide si no hay poligonos) y `properties` con `zone_id`, `municipality`, `risk_score`, `risk_level`, `abstain`.

### GET /zones/ranking
Query: `hazard`, `target_month`, `limit` (por defecto 20, maximo 100), `level`. Respuesta: campos del snapshot + `items`: `rank`, `zone_id`, `municipality`, `risk_score`, `risk_level`, `prediction_set`. Orden descendente por `risk_score`; las zonas con `risk_score = null` no entran.

### GET /zones/{zone_id}/explain
Query: `hazard`, `target_month`. Respuesta: campos del snapshot + `zone_id`, `abstain`, `abstain_reason`, `top_factors` (SHAP) e `history`: `[ { "month": "2026-04", "risk_score": 0.4 } ]`. Misma regla de abstencion que `/predict`: con `stale_data`, `top_factors` es `[]`. `history` solo incluye meses previos con snapshot valido (desde 2019-01 y con datos disponibles a su `feature_cutoff`).

### GET /metrics
Query: `hazard`. Metricas leidas de MLflow, nunca escritas a mano. Campos del snapshot +
```json
{
  "validation": "spatial_block_cv",
  "metrics":  [ { "name": "pr_auc", "value": 0.0, "ci_lower": 0.0, "ci_upper": 0.0 } ],
  "baseline": [ { "name": "pr_auc", "value": 0.0 } ],
  "calibration": { "ece": 0.0 },
  "conformal": { "alpha": 0.1, "empirical_coverage": 0.0, "evaluation_scope": "spatial_block_cv" }
}
```

## Mock

Mientras no haya modelo, `app/api/` sirve datos sinteticos deterministas con exactamente este schema. Reglas para que no se confundan con datos reales:

1. `is_mock = true` y `model_version = "mock"` en toda respuesta.
2. La web muestra un banner inequivoco ("Datos de demostracion, no son predicciones reales") mientras `is_mock` sea `true`, y no presenta ranking ni alertas como reales.
3. En `/metrics` los valores son `null`: no se inventan cifras.
4. El mock cumple el mismo schema, asi que la web no cambia al pasar al modelo real.
