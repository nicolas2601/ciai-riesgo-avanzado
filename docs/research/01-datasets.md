# Datasets candidatos y definición de la etiqueta

Consulta de fuentes: 2026-10-12. Investigación documental, sin descargar datos ni entrenar modelos. Los tamaños regionales y conteos de eventos todavía no están medidos.

## Decisión recomendada, condicionada

No elegir inundación, remoción en masa, incendio o delito como si fueran intercambiables. Primero confirmar enunciado, unidad espacial, horizonte y etiqueta oficial. Si no existe etiqueta oficial, seleccionar **una sola amenaza observable** y declarar exactamente qué se predice.

- **HECHO:** FIRMS ofrece observaciones de anomalías térmicas con fecha y coordenadas; COOLR reúne reportes/inventarios de deslizamientos. Lluvia, elevación y población no son etiquetas de eventos.
- **PROPUESTA:** primer candidato operativo: frecuencia futura de detecciones térmicas por celda y ventana; alternativa: eventos reportados de deslizamiento, si el inventario regional es suficiente. Ninguno equivale automáticamente a riesgo integral ni a severidad.
- **SUPOSICIÓN:** Santander es el área de interés. No hay verificación del enunciado, inventario oficial o distribución de clases.
- **NO HACER:** crear etiquetas mediante pendiente/lluvia y entrenar con esas mismas variables. El modelo aprendería la regla, no evidencia independiente de eventos.

## Comparación rápida

| Fuente | Función | Cobertura/resolución verificada | Tamaño | Licencia/acceso |
|---|---|---|---|---|
| NASA COOLR / GLC | Eventos de deslizamiento; posible target | Reportes georreferenciados e inventarios; GLC compilado desde 2007 | Conteo y bytes regionales no verificados | Export legado: licencia no especificada; revisar términos por inventario |
| CHIRPS v2 | Lluvia y acumulados antecedentes | Diario, 0.05°, 1981–casi presente, 50°S–50°N | Bytes no verificados; recortar antes de descargar | Dominio público, según proveedor |
| Copernicus DEM GLO-30 | Elevación y derivados de relieve | DSM nominal de 30 m; teselas 1° × 1° | 3,600 filas por tesela; bytes comprimidos variables | Licencia gratuita específica; atribución y términos, no asumir CC0 |
| NASA FIRMS VIIRS | Detecciones térmicas; posible target | Nominal 375 m; S-NPP desde 2012-01-20 | Filas/bytes dependen de región y fechas; no medidos | Acceso público; archivo exige Earthdata o código por correo; licencia específica no verificada |
| WorldPop Colombia 2020 | Exposición poblacional | GeoTIFF ~100 m; habitantes por celda | Archivo nacional publicado: 586.38 MB | CC BY 4.0 |

Accesible públicamente no implica que los cinco tengan una licencia abierta estandarizada verificada. COOLR y FIRMS requieren resolver términos antes de redistribuir datos.

## 1. NASA COOLR / Global Landslide Catalog

**HECHOS:** COOLR reúne Global Landslide Catalog, reportes voluntarios y otros inventarios, incluyendo inventarios ligados a eventos. El CSV legado del portal NASA es una instantánea al 2016-03-07, no el catálogo actual. GLC combina prensa, bases de desastres y reportes científicos; su cobertura refleja también el mecanismo de reporte.

**Etiqueta candidata:** presencia o conteo de **eventos reportados** por celda y ventana. Fecha, geometría, desencadenante y precisión de ubicación deben verificarse en el export elegido. Filtrar desencadenante si se quiere exclusivamente deslizamiento por lluvia.

**No etiqueta:** ausencia de registro no demuestra ausencia de deslizamiento; tamaños narrativos no son una escala clínica/operativa universal de severidad.

**Por qué sirve:** aporta observaciones independientes para aprender susceptibilidad o frecuencia de reporte; combina naturalmente con lluvia y relieve.

**Riesgos:** sesgo hacia áreas pobladas, incertidumbre espacial, duplicados, fechas incompletas y pocos positivos en Santander. Si no hay un esquema defendible de negativos o vigilancia, evaluar presencia/background como tal, no afirmar probabilidades reales de ocurrencia.

**Gate:** export disponible, términos aceptables, fechas y coordenadas válidas y positivos suficientes en cada partición. Si falla, no rellenar con eventos sintéticos; ampliar área/horizonte solamente si el enunciado lo permite.

Fuentes:
- [COOLR oficial](https://gpm.nasa.gov/applications/landslides/coolr)
- [Export legado y licencia no especificada](https://data.nasa.gov/dataset/global-landslide-catalog-export-f07b6)
- [Guía de exportación](https://gpm.nasa.gov/landslides/guides/COOLRGuide_Exporting.pdf)
- [FeatureServer de inventarios poligonales](https://gis.earthdata.nasa.gov/portal/rest/services/Landslides/COOLR_Reports_Polygons/FeatureServer)

## 2. CHIRPS v2: precipitación

**HECHOS:** integra estaciones y estimaciones satelitales; resolución 0.05°, serie desde 1981. El proveedor declara dominio público y espera terminar producción v2 después de diciembre de 2026. Existe v3; no mezclar versiones en una corrida.

**Etiqueta:** ninguna de evento/riesgo. Precipitación extrema podría ser un target meteorológico específico, pero no debe presentarse como desastre territorial observado.

**Features propuestas:** acumulados de 1, 3, 7 y 30 días, anomalía estacional y duración de períodos secos, calculados con información disponible antes del instante de predicción. Ventanas y estacionalidad se justifican según amenaza; no todas aplican igual.

**Tamaño:** no se verificaron bytes. Recortar área y fechas. La resolución de lluvia es mucho más gruesa que 100 m: interpolar no crea observaciones locales independientes.

**Gate temporal:** CHIRPS final es válido para análisis retrospectivo; una demo prospectiva necesita versión/latencia disponibles en la fecha de emisión. Usar lluvia de la ventana que se intenta predecir sería fuga de futuro.

Fuentes:
- [Proveedor, dominio público y transición v3](https://chc.ucsb.edu/data/chirps)
- [Directorio de descargas v2](https://data.chc.ucsb.edu/products/CHIRPS-2.0/)
- [Catálogo diario v2](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY)

## 3. Copernicus DEM GLO-30

**HECHOS:** es un modelo digital de superficie (DSM), no de terreno desnudo: vegetación y edificios pueden afectar derivados. Producto nominal de 30 m; distribución pública AWS en Cloud Optimized GeoTIFF, con teselas de 1° × 1°. Disponibilidad de teselas debe verificarse para el área.

**Etiqueta:** ninguna. Pendiente/elevación son covariables, no evidencia de evento.

**Features propuestas:** elevación, pendiente y rugosidad; distancia/drenaje o HAND requieren redes/algoritmos adicionales y no están resueltos por descargar DEM. Calcular pendientes en CRS proyectado con unidades métricas, no tratar grados como metros.

**Tamaño:** 3,600 filas por tesela GLO-30 y ancho variable por latitud según distribución AWS. Bytes dependen de compresión y tesela; no medidos. Recorte y lectura por ventanas COG evitan descargar el mundo.

**Licencia:** licencia Copernicus DEM gratuita específica. Conservar aviso de atribución del producto y revisar condiciones de derivados/redistribución. No tratarla como CC0.

**Nota de evidencia:** el extracto automatizado de la página AWS devolvió unidades angulares inconsistentes con 30 m. No se usa ese extracto para afirmar resolución angular; se conserva únicamente resolución nominal confirmada por catálogo oficial.

Fuentes:
- [Catálogo oficial del producto](https://doi.org/10.5270/ESA-c5d3d65)
- [Distribución pública AWS](https://copernicus-dem-30m.s3.amazonaws.com/readme.html)
- [Catálogo GLO-30 2024_1 y términos](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30_2024_1)

## 4. NASA FIRMS VIIRS: anomalías térmicas

**HECHOS:** archivo CSV/shapefile/JSON; S-NPP desde 2012-01-20, NOAA-20 desde 2018-04-01 y NOAA-21 desde 2024-01-17. Archivo histórico excluye últimos siete días; NRT se reemplaza por producto científico estándar con retraso aproximado de cinco meses.

**Etiqueta candidata:** número de días con al menos una detección térmica admisible por celda durante una ventana futura. Una detección no equivale a incendio forestal, área quemada, víctima ni severidad: incluye otras fuentes de calor y puede omitir incendios por nubes/revisita.

**Propuesta de limpieza:** fijar un satélite/producto para evitar cambios artificiales en esfuerzo de observación; excluir detecciones no admisibles usando campos documentados; agrupar celda-día para reducir doble conteo. Sin datos de observabilidad, llamar al target frecuencia de detección, no frecuencia real de incendio.

**Tamaño/licencia:** ni conteos regionales ni bytes verificados. NASA fomenta uso y crédito; no se encontró licencia estandarizada explícita en páginas consultadas. Revisar términos del producto antes de redistribución. Archivo exige login Earthdata o código enviado por correo: no almacenar credenciales en repo.

**Por qué sirve:** target observable temporal/geográfico, con covariables de sequedad/lluvia/relieve. Es una opción de menor dependencia de prensa, no una garantía de superior cobertura territorial.

Fuentes:
- [Archivo y acceso](https://firms.modaps.eosdis.nasa.gov/download/)
- [FAQ: anomalías, limitaciones y crédito](https://www.earthdata.nasa.gov/data/tools/firms/faq)

## 5. WorldPop Colombia 2020

**HECHOS:** producto unconstrained, ~100 m, WGS84, habitantes estimados por celda, archivo nacional 586.38 MB; licencia CC BY 4.0. El extracto consultado no confirma ajuste a totales ONU: no asumirlo.

**Etiqueta:** ninguna de amenaza. Es exposición estimada y puede apoyar priorización secundaria; no mide vulnerabilidad, evacuación ni daño.

**Propuesta:** sumar población por zona para un panel de exposición separado. No sumar/resamplear conteos como si fueran valores continuos de elevación: conservar masa poblacional. No usar población 2020 para afirmar exposición exacta de otro año.

**Por qué sirve:** distingue ocurrencia del fenómeno de personas potencialmente expuestas. Una celda con baja población no es automáticamente segura.

Fuentes:
- [Metadatos, licencia y tamaño](https://hub.worldpop.org/geodata/summary?id=6349)
- [GeoTIFF Colombia 2020](https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/COL/col_ppp_2020.tif)
- [Licencia WorldPop](https://www.worldpop.org/faq/)

## Discretización defendible para un prototipo

**PROPUESTA, no requisito verificado:** una celda fija y horizonte no solapado de 30 días, sujeto a densidad real. Definir `c(z,t)` como días con detección admisible en los siguientes 30 días; para COOLR, cambiar a conteo de reportes y renombrar explícitamente el target.

1. Bajo: `c = 0`, descrito como sin detecciones/reportes, nunca como ausencia de amenaza.
2. Obtener `q` = mediana de conteos estrictamente positivos **solo en entrenamiento**. Medio: `0 < c <= q`; alto: `c > q`. Congelar `q` al evaluar y servir.
3. Si `q` coincide con máximo, alguna clase queda vacía o no hay soporte por fold, rechazar discretización: usar target binario/conteo, otra ventana justificada o etiqueta oficial. No fabricar tercera clase para cumplir presentación.
4. Tres niveles representan frecuencia relativa observada, no severidad oficial. Usar nombres de UI y documentación que no oculten esa limitación.
5. La etiqueta procede de observaciones futuras; predictores proceden del pasado. Cuantiles, sampling y transformaciones no ven validación/calibración/test.

La regla solo construye un target ordinal; **no es el predictor**. El predictor ML debe aprender sobre eventos independientes y compararse con baseline. Si reglas oficiales definen clases de riesgo, tienen prioridad sobre esta propuesta.

## Gate de datos: primeros 30 minutos

- Confirmar dominio/target, permiso de datos, área y horizonte.
- Export mínimo real, esquema y conteos por clase/espacio/tiempo; medir bytes, registrar hash y fecha de acceso.
- Revisar fechas, CRS, precisión, duplicados, latencia y observabilidad. Deduplicar antes de partir datos.
- Definir rejilla/coordenadas y una sola fuente de eventos; lluvia + DEM como mínimo multifuente si aplican.
- Elegir resolución compatible con medición y decisiones; una rejilla fina no aumenta precisión del satélite.
- Si no pasa gate, presentar pipeline/prototipo limitado con datos reales disponibles; no afirmar modelo territorial validado.
