---
name: ml-pipeline
description: Reglas para EDA, features, modelado y validacion del riesgo territorial. Usar antes de tocar ml/.
---

# ML pipeline

1. EDA primero: calidad, huecos temporales, autocorrelacion espacial (Moran), desbalance. Registrar hallazgos en el notebook.
2. Unidad espacial: celdas H3 (resolucion en config). Unir fuentes por celda y fecha.
3. Features: espaciales (vecindad k-ring, distancias), temporales (rezagos, ventanas moviles), derivadas del dominio. Solo informacion disponible hasta `as_of` (sin fuga temporal).
4. Modelos: baseline obligatorio, GBDT, red PyTorch propia, ensamblado hibrido.
5. Validacion: CV por bloques espaciales + particion temporal. IC por bootstrap. Calibracion y conformal.
6. Explicabilidad: SHAP por zona y global.
7. Cada corrida en MLflow con semilla, hash de datos y commit.
8. Nunca afirmar mejora si los intervalos se solapan.
