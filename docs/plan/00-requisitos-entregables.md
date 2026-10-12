# Requisitos AVANZADO -> entregable verificable

Fuente: enunciado de la categoria AVANZADO del CIAI. Cada requisito tiene un entregable concreto y una evidencia que se puede mostrar al jurado.

## Supuestos (HECHO vs SUPOSICION)

- HECHO: el ML es obligatorio; no se acepta solucion conceptual, visual ni basada en reglas fijas. La categoria no cambia una vez iniciado el reto.
- HECHO: salida esperada = nivel de riesgo (bajo/medio/alto) por punto o zona, priorizando zonas.
- SUPOSICION: no tenemos el enunciado del fenomeno ni dataset oficial. Se disena agnostico al fenomeno y se concreta cuando exista dato. Si la organizacion entrega dataset, se usa ese (ver 01-roles-cronograma, hito H1).
- SUPOSICION: dominio por defecto = riesgo por amenaza natural en Santander con datos abiertos.
- HECHO (docs/research/06): existe etiqueta real 2019-2025 (UNGRD, 2 641 eventos en Santander) pero sus coordenadas son inservibles y el DIVIPOLA de 2025 esta corrupto; la unidad espacial es el MUNICIPIO (87, resueltos por nombre normalizado), no una celda H3. Panel municipio x mes (~7 300 filas).

## Definicion del target (riesgo de la etiqueta)

Riesgo de fondo: fabricar bajo/medio/alto sin una definicion defendible. Reglas:

1. La etiqueta sale de eventos historicos reales o de un indice con fuente citada, nunca de umbrales arbitrarios sobre las mismas features que el modelo usa (eso es fuga y reduce el ML a reglas).
2. No se mezclan amenazas distintas en un solo target sin declararlo.
3. La discretizacion a bajo/medio/alto (por ejemplo cuantiles de frecuencia o severidad por celda y ventana) se decide en `docs/research/01-datasets.md` y se congela en H1.
4. El modelo predice primero una cantidad continua o probabilidad; el nivel se deriva por umbrales calibrados.

## Matriz

| # | Requisito | Entregable | Evidencia |
|---|---|---|---|
| 1 | Solucion integral de gestion y evaluacion del riesgo | Pipeline datos -> modelo -> API -> web | Demo end-to-end en URL publica |
| 2 | Priorizar zonas de riesgo | Ranking de zonas con score y nivel; mapa | Endpoint `/zones/ranking` + vista de mapa |
| 3 | Multiples fuentes o series temporales/geoespaciales | >= 3 fuentes unidas por municipio (DIVIPOLA) y mes: UNGRD, Open-Meteo/NASA POWER, ONI, relieve y poblacion | Tabla de fuentes con licencia y cobertura |
| 4 | Ingenieria de caracteristicas | Features espaciales (vecindad, distancias), temporales (rezagos, ventanas), derivadas | Notebook de FE + lista de features con importancia |
| 5 | Modelos avanzados o hibridos | GBDT principal + red residual PyTorch propia (desde cero) + TabPFN opcional; ensamblado solo si mejora medida | Comparacion de modelos en MLflow |
| 6 | Validacion rigurosa | CV por bloques de municipios + particion temporal con embargo; baseline; IC por remuestreo de bloques y diferencia pareada | Reporte de metricas con intervalos |
| 7 | Incertidumbre o explicabilidad | SHAP + calibracion probabilistica; conformal con cobertura EMPIRICA (sin prometer garantia espacial) y abstencion | Intervalos en API y grafico SHAP en web |
| 8 | API / servicio / prototipo funcional | FastAPI + web (bun) desplegados | URL Cloudflare + OpenAPI |
| 9 | ML obligatorio | Modelo entrenado, versionado y servido | Run en MLflow + artefacto del modelo |
| 10 | Solidez metodologica | Protocolo de validacion escrito antes de entrenar | `docs/research/03-validacion-incertidumbre.md` |
| 11 | Escalabilidad | Servicio sin estado, bundle inmutable, predicciones precalculadas, ONNX opcional, docker-compose | Prueba de carga simple (latencia p95) |
| 12 | Trazabilidad | DVC o hash de datos + MLflow + semillas + commit en cada run | Cada prediccion devuelve `model_version` y `data_version` |

## Definition of Done

- Pipeline reproducible con un comando desde datos crudos hasta modelo.
- Metricas con intervalos de confianza, incluida la comparacion contra baseline.
- API documentada (OpenAPI) respondiendo con score, nivel, intervalo y explicacion.
- Web desplegada con mapa, ranking, explicacion y pagina de metricas/uso.
- README con instrucciones de uso y limites conocidos.

## Pre-mortem (asumamos que fallo en 1 dia)

| Causa probable | Mitigacion |
|---|---|
| No hay dataset del dominio y se pierde tiempo eligiendo | Hito H1 a los 30 min: congelar dataset; fallback a datos abiertos ya listados |
| Fuga espacial infla metricas | CV por bloques de municipios desde el primer experimento |
| Cluster GPU ocupado o con permisos NFS | Entrenar modelos tabulares en CPU; PyTorch pequeno corre en CPU; fallback Colab/Kaggle |
| Web bloqueada esperando al modelo | Contrato API + mock desde la hora 0 |
| Despliegue falla al final | Desplegar esqueleto en la hora 2, no en la 5 |
| Claims no verificables en la presentacion | Cada cifra sale de un run de MLflow, no se transcribe a mano |
