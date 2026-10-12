# Estado del arte geoespacial 2025-2026: que sirve en 5 horas

Consulta: 2026-10-12. Fuentes: busquedas web (resumenes secundarios, no se leyeron los papers completos) y la pagina oficial de TabPFN (leida). Complementa `02-modelos-sota.md` (fundamentos 2019-2021, arquitectura recomendada). Aqui solo lo nuevo y su veredicto.

## Veredicto

| Tecnica | Encaja con nuestro panel municipio-mes | Decision |
|---|---|---|
| GBDT (LightGBM/XGBoost/CatBoost) | Si | Modelo principal (ver 02) |
| Red residual PyTorch propia | Si | Challenger obligatorio ("modelo desde cero") |
| TabPFN | Si, el panel (~7 000 filas) cae en su zona de uso | Challenger barato; probar si hay GPU |
| AlphaEarth Foundations (embeddings) | Parcial: anual y por pixel | Solo si hay acceso a Earth Engine; feature estatica opcional |
| Prithvi-EO-2.0 (fine-tuning) | No: modelo de imagen, requiere chips y tuning | Descartado en 5 h |
| ST-GNN / TFT completo | No por falta de datos densos | Descartado (coincide con 02) |

## TabPFN (foundation model tabular)

- HECHO (pagina oficial de PriorLabs): codigo Apache-2.0; pesos de TabPFN-2.5 y 2.6 bajo licencia **no comercial**; `pip install tabpfn` (Python >= 3.10); no exige GPU pero "es lento en CPU"; hay un cliente alojado.
- HECHO (pagina oficial): la version por defecto hoy es TabPFN-3.5. No encontre como fijar 2.5 en el README.
- HECHO (arXiv 2511.08667, via busqueda): los autores reportan 100 % de victorias contra XGBoost por defecto en clasificacion de hasta 10 000 filas y 87 % hasta 100 000.
- CAUTELA: son resultados de los propios autores y con datos i.i.d. Una revision citada en la busqueda indica que arboles y redes profundas mantienen ventaja fuera del caso i.i.d. No encontre ningun estudio que compare TabPFN contra boosting bajo validacion espacial. Un articulo de 2026 de susceptibilidad a deslizamientos (Qingchuan, Sichuan) usa TabPFN con CV espacial por bloques anidada, pero el resumen no dio resultados ni version.
- RIESGO: licencia no comercial. Para un hackathon academico es aceptable; declararlo en el README.
- USO: tercer modelo en la comparacion, bajo el mismo protocolo de validacion por bloques. No se afirma que gane.

## AlphaEarth Foundations (Google DeepMind, 2025)

- HECHO (busqueda): embeddings anuales de 64 dimensiones a 10 m, 2017-2024, dataset `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` en Earth Engine, pensados para alimentar modelos clasicos (random forest, boosting, MLP).
- HECHO (busqueda): limitaciones declaradas: composites anuales (no sirven para respuesta intra-estacional) y ejes sin interpretacion fisica directa.
- HECHO (busqueda): existe un articulo de 2026 que reemplaza factores clasicos de deslizamiento por estos embeddings.
- VEREDICTO: nuestro panel es mensual; el embedding anual solo aporta como descriptor ESTATICO del municipio (cobertura, suelo, relieve latente). Requiere cuenta de Earth Engine y extraer la media por municipio. Coste 1-2 h con riesgo de acceso: no entra en la ruta critica. Como contrapunto, la explicabilidad se pierde (ejes no interpretables), lo que choca con el requisito 7.

## Lo que SI vale la pena tomar del estado del arte

1. Validacion espacial por bloques anidada, ya adoptada en `skills/ml-pipeline`.
2. Comparar contra un modelo fundacional tabular como evidencia de rigor (TabPFN), sin atarse a el.
3. Reportar la limitacion de cada tecnica en la web: un jurado premia la honestidad metodologica mas que el nombre del modelo.

## Fuentes

- [TabPFN, repositorio oficial (licencias, instalacion)](https://github.com/PriorLabs/TabPFN)
- [TabPFN-2.5, arXiv 2511.08667](https://arxiv.org/pdf/2511.08667)
- [TabPFN para susceptibilidad a deslizamientos, Qingchuan (Applied Sciences, 2026)](https://doi.org/10.3390/app16157860)
- [AlphaEarth Foundations: resumen tecnico](https://www.emergentmind.com/topics/alphaearth)
- [AlphaEarth en CARTO](https://carto.com/blog/google-alphaearth-foundations-in-carto/)
- [Prithvi-EO-2.0 y TerraTorch (resumen)](https://medium.com/@brian-curry-research/geospatial-foundation-models-for-agricultural-machine-learning-a3cd0169d256)
