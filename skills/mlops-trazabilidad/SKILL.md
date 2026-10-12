---
name: mlops-trazabilidad
description: Trazabilidad de datos, corridas y modelos; despliegue reproducible. Usar al versionar datos, registrar corridas o servir el modelo.
---

# MLOps y trazabilidad

1. Datos: hash o DVC por version; `data_version` viaja hasta la API.
2. Corridas: MLflow con parametros, metricas, artefactos, semilla y commit.
3. Modelo servido: ONNX + metadatos; la API devuelve `model_version` en cada respuesta.
4. Config: Hydra/YAML, nada hardcodeado.
5. Despliegue: docker compose, healthcheck, tunel Cloudflare; verificar la URL final con curl.
6. Monitoreo minimo: latencia p95 y distribucion de scores (drift simple).
