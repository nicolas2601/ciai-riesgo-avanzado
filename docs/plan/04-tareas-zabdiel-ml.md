# Tareas de Zabdiel: ML

Lider ML. Lee antes: `docs/research/06-datos-colombia.md`, `03-validacion-incertidumbre.md`, `02-modelos-sota.md`, `skills/ml-pipeline/SKILL.md`. Entrenas en el cluster UNABIA (ver `02-entorno-dependencias.md`); lo tabular corre en CPU si el cluster falla.

## Decision que se congela en el hito H1 (primeros 30 min)

1. Amenaza principal: incendio (1 390 eventos, soporte alto) como primera opcion; deslizamiento (362) e inundacion (279) como secundarias si hay tiempo.
2. Nivel bajo/medio/alto: regla de `01-datasets.md` (cero = bajo; mediana de positivos en train separa medio de alto). Si una clase queda vacia en algun fold, caer a binario y avisar a Nico: el contrato se ajusta.
3. Horizonte: mes siguiente. Unidad: municipio x mes.

## Tareas

### 1. Datos (H1, 30 min)
- [ ] `ml/src/data/ungrd.py`: descarga paginada SoQL de `wwkg-r6te`, `rgre-6ak4`, `2343-nuqp` filtrando Santander; armoniza columnas y nombres de evento; deduplica.
- [ ] `ml/src/data/panel.py`: panel municipio (DIVIPOLA) x mes con conteo por amenaza.
- [ ] Guardar Parquet en `data/processed/` y registrar hash SHA-256 y fecha de acceso (alimenta `data_version`).
- [ ] Centroides desde `kqut-4h4r` (deduplicar por municipio).

### 2. EDA (H2)
- [ ] `ml/notebooks/01_eda.ipynb`: conteos por ano, mes y municipio; el salto de 2022 (Santander: movimiento en masa 32, 23, 24, 156); autocorrelacion espacial (Moran); desbalance; municipios sin eventos.
- [ ] Documentar el sesgo de reporte (06, riesgo 3).

### 3. Features (H2)
- [ ] Meteorologia por municipio y mes: Open-Meteo (lluvia, temperatura, ET0) y NASA POWER (`GWETROOT`); pedir por lotes, cachear en disco.
- [ ] ONI (NOAA) por mes; estacionalidad; eventos previos del municipio y de vecinos (kNN de centroides).
- [ ] Opcional: pendiente (Copernicus DEM) y poblacion (WorldPop).
- [ ] Toda feature usa solo informacion anterior al mes a predecir; test unitario de no-fuga.

### 4. Modelos (H3)
- [ ] Baseline: prior de clases + regresion logistica.
- [ ] LightGBM (principal).
- [ ] `TerritorialRiskNet` en PyTorch, desde cero (ver 02); entrenar en el cluster.
- [ ] Opcional: TabPFN como challenger (pesos no comerciales).

### 5. Validacion (H3 a H5)
- [ ] Bloques de municipios (k-means sobre centroides, ~6 a 8 bloques) y particion temporal con embargo de 1 mes. Dos corridas de sensibilidad: 2022 en train y 2022 en test.
- [ ] Metricas de `03`: PR-AUC de la clase alta, macro-F1, Brier, ECE, recall@K.
- [ ] IC por remuestreo de bloques; comparar modelos con la diferencia pareada por bloques.
- [ ] Calibracion (temperature scaling o isotonica si hay soporte); conformal solo con cobertura empirica reportada.
- [ ] SHAP para el GBDT; permutacion bloqueada para la red.

### 6. Entrega a la API (H4)
- [ ] `ml/src/serving/bundle.py`: `load_bundle(path)` y `predict(zone_id, hazard, as_of)` que devuelve el JSON de `03-contrato-api.md`.
- [ ] Bundle = preprocesador + modelo + calibrador + `model_version` + `data_version` + orden de features. Test de paridad offline vs API.
- [ ] Todas las corridas en MLflow con semilla, hash de datos y commit. La pagina `/metrics` de la web sale de ahi.

## Definition of Done

Reproducible con un comando; metricas con intervalo y comparacion contra baseline; bundle cargable por la API; limitaciones escritas (sesgo de reporte, 2022, pocos bloques).

## Si te atrasas

Recorta en este orden: TabPFN, red PyTorch con tuning, conformal, SHAP de la red. No recortes: baseline, validacion por bloques, MLflow, bundle.
