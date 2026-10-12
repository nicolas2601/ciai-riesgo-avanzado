# Roles y cronograma (5 h)

## Roles

| Persona | Rol | Responsable de |
|---|---|---|
| Zabdiel (zquintero246) | Lider ML | EDA, preprocesamiento, features, modelado, validacion, MLflow, export ONNX |
| Julian (Andrejulian21) | Lider web | Prototipo web con bun: mapa, ranking, explicabilidad, pagina de metricas y uso |
| Nico | Integracion y plataforma | API FastAPI, contrato, entorno, despliegue + tunel Cloudflare, apoyo en ambos lados |

Regla de apoyo: Nico toma el bloque que se atrase. Se decide en cada hito, no al final.

## Hitos

| Hito | Hora | Salida | Responsable |
|---|---|---|---|
| H0 | 0:00 | Repo, entorno, contrato API congelado | Nico |
| H1 | 0:30 | Dataset elegido y descargado; mock de API arriba | Zabdiel + Nico |
| H2 | 1:30 | EDA + features v1; esqueleto web con mock; esqueleto desplegado | Zabdiel, Julian, Nico |
| H3 | 2:30 | Baseline + modelo avanzado entrenados con CV espacial | Zabdiel |
| H4 | 3:30 | Modelo servido por API real; web consume API real; explicabilidad | Todos |
| H5 | 4:15 | Incertidumbre, pagina de metricas/uso, prueba de carga | Todos |
| H6 | 4:45 | Congelar: README, resultados, URL final | Nico |
| H7 | 5:00 | Mensaje al grupo con repo y URLs | Nico |

## Flujo por persona

### Zabdiel (ML)
1. `ml/notebooks/01_eda.ipynb`: calidad, distribucion, autocorrelacion espacial (Moran), desbalance, huecos temporales.
2. `ml/src/features/`: panel municipio-mes, vecindad entre municipios, rezagos, ventanas, estacionalidad, ONI; todo parametrizado.
3. `ml/src/models/`: baseline (prior + regresion logistica), GBDT, red residual PyTorch propia, TabPFN opcional.
4. `ml/src/eval/`: CV por bloques, particion temporal con embargo, IC por bloques, calibracion, SHAP, conformal (cobertura empirica).
5. Cada corrida a MLflow; guardar bundle (preprocesador + modelo + calibrador); ONNX opcional si hay paridad.

### Julian (web)
1. Arrancar contra el mock del contrato (`docs/plan/03-contrato-api.md`), sin esperar al modelo.
2. Vistas: mapa de riesgo por municipio, ranking de zonas, detalle con explicacion y conjunto de prediccion, pagina de metricas, pagina "como usarlo".
3. Cliente tipado generado desde OpenAPI.
4. Reglas de UI: leer `skills/web-app/SKILL.md`.

### Nico (integracion)
1. `app/api/`: endpoints del contrato, carga del modelo, versionado en cada respuesta.
2. `infra/`: Docker, docker-compose, tunel Cloudflare, healthchecks.
3. Prueba de carga y verificacion end-to-end antes del congelamiento.

## Rituales

- Sincronizacion de 5 min en cada hito: que esta hecho (con evidencia), que bloquea, que cambia.
- Un bloqueo de mas de 15 min se escala, no se sufre en silencio.
