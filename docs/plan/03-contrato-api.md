# Contrato API (frontera ML <-> web)

Version: v0.1 (propuesta). Congelar en el hito H0. Cualquier cambio se avisa a Zabdiel y Julian. La implementacion real debe pasar la validacion contra OpenAPI generado por FastAPI.

Base: `/api/v1`. JSON UTF-8. Zonas identificadas por indice H3 (resolucion configurable, por defecto 8).

## Convenciones

- `risk_level`: `"low" | "medium" | "high"`.
- `risk_score`: numero en [0, 1], probabilidad calibrada de riesgo alto.
- `interval`: `{ "lower": n, "upper": n, "coverage": 0.9 }` (conformal).
- Toda respuesta incluye `model_version` y `data_version` (trazabilidad).
- Errores: `{ "error": { "code": "string", "message": "string" } }` con HTTP 4xx/5xx.

## Endpoints

### GET /health
Respuesta: `{ "status": "ok", "model_version": "string", "data_version": "string" }`

### POST /predict
Entrada:
```json
{ "lat": 7.1193, "lon": -73.1227, "as_of": "2026-10-12" }
```
`as_of` opcional (por defecto hoy).

Respuesta:
```json
{
  "zone_id": "88a8e0a1b3fffff",
  "risk_score": 0.74,
  "risk_level": "high",
  "interval": { "lower": 0.61, "upper": 0.85, "coverage": 0.9 },
  "top_factors": [
    { "feature": "rainfall_30d", "shap": 0.18, "value": 212.4 }
  ],
  "model_version": "string",
  "data_version": "string"
}
```

### GET /zones
Query: `bbox=minLon,minLat,maxLon,maxLat`, `level` opcional.
Respuesta: GeoJSON FeatureCollection; cada feature con `zone_id`, `risk_score`, `risk_level`.

### GET /zones/ranking
Query: `limit` (por defecto 20), `level` opcional.
Respuesta: `{ "items": [ { "rank": 1, "zone_id": "...", "risk_score": 0.91, "risk_level": "high", "interval": {...} } ], "model_version": "...", "data_version": "..." }`

### GET /zones/{zone_id}/explain
Respuesta: `top_factors` completo (SHAP) mas serie temporal reciente: `{ "zone_id": "...", "top_factors": [...], "history": [ { "date": "2026-09-01", "risk_score": 0.5 } ] }`

### GET /metrics
Metricas reales del modelo vigente leidas de MLflow (nunca escritas a mano):
```json
{
  "model_version": "string",
  "data_version": "string",
  "validation": "spatial_block_cv",
  "metrics": [ { "name": "pr_auc", "value": 0.0, "ci_lower": 0.0, "ci_upper": 0.0 } ],
  "baseline": [ { "name": "pr_auc", "value": 0.0 } ],
  "calibration": { "ece": 0.0 },
  "conformal_coverage": 0.0
}
```

## Mock

Mientras el modelo no exista, `app/api/` sirve respuestas sinteticas con esta misma forma y `model_version = "mock"`. La web no debe distinguir mock de real salvo por ese campo.
