# Santander municipal polygons

- File: app/web/public/data/santander_municipios.geojson (87 features; properties: divipola, nombre; WGS84 lon/lat).
- Origin data: DANE Marco Geoestadistico Nacional (MGN) 2018, municipal level (field MPIO_CCNCT = DIVIPOLA).
- Downloaded from: https://raw.githubusercontent.com/caticoa3/colombia_mapa/master/co_2018_MGN_MPIO_POLITICO.geojson
- Download date: 2026-10-13.
- Provenance: UNOFFICIAL third-party GitHub mirror of the DANE MGN 2018 layer; the official DANE/IGAC and datos.gov.co services were not queried (time-boxed).
- License: the mirror repository declares no license. Underlying data is DANE public geostatistical data (open data in Colombia, attribution to DANE).
- Processing: filtered DPTO_CCDGO = 68, Douglas-Peucker simplification 0.002 deg (shapely, topology preserved), names title-cased.
- Verification: 87 features, all divipola codes match data/external_pub/dane_poblacion_municipal.csv, all geometries valid.
- Caveat: 2018 boundaries and 0.002 deg simplification; for display only, not for area or legal calculations.
