---
name: ml-pipeline
description: Reglas para EDA, features, modelado y validacion del riesgo territorial. Usar antes de tocar ml/.
---

# ML pipeline

1. EDA primero: calidad, huecos temporales, autocorrelacion espacial (Moran), desbalance. Registrar hallazgos en el notebook.
2. Unidad espacial: municipio (codigo DIVIPOLA); las coordenadas de UNGRD son inservibles. Panel municipio x mes; unir fuentes por municipio y mes.
3. Features: espaciales (vecindad k-ring, distancias), temporales (rezagos, ventanas moviles), derivadas del dominio. Solo informacion disponible hasta `as_of` (sin fuga temporal).
4. Modelos: baseline obligatorio, GBDT, red PyTorch propia, ensamblado hibrido.
5. Validacion: CV por bloques de municipios + particion temporal con embargo. IC por remuestreo de bloques. Calibracion; conformal solo con cobertura empirica.
6. Explicabilidad: SHAP por zona y global.
7. Cada corrida en MLflow con semilla, hash de datos y commit.
8. Afirmar mejora solo con el intervalo de la diferencia pareada por bloques; si es inconcluso, preferir el modelo mas simple.
