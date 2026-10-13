# Segunda fuente oficial: población municipal DANE

Consulta y descarga: **2026-10-13, 09:02–09:07 COT**. Recurso oficial [Proyecciones de población](https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion); DANE enlaza el XLSX municipal 2018–2042.

## HECHO

- **Fuente recomendada:** [PPED-AreaMun-2018-2042_VP.xlsx](https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/PPED-AreaMun-2018-2042_VP.xlsx) (HTTPS 200, XLSX, 3,948,350 bytes). Hoja `PobMunicipalxÁrea`; columnas: `DP`, `DPNOM`, `MPIO`, `DPMP`, `AÑO`, `ÁREA GEOGRÁFICA`, `TOTAL`. Archivo indica actualización 30-jul-2025.
- **Licencia:** la página y el libro consultados no exponen licencia de datos abierta específica. Fuente oficial pública; verificar términos de reutilización/atribución DANE antes de redistribuir.
- **Cobertura extraída:** DIVIPOLA municipal `68xxx`, 2018–2026 inclusivo; **87 municipios y 783 filas** (87 × 9). CSV: `data/external/dane_poblacion_municipal.csv`, columnas `divipola, municipio, anio, poblacion, area_total_o_cabecera`. Última columna contiene `cabecera|centros_poblados_rural`.
- **Naturaleza:** proyección/estimación retrospectiva y prospectiva basada en CNPV 2018 y metodología de componentes de cohortes; no equivale a conteo censal observado para cada año. Evitar presentarla como medición anual observada.
- **Metadatos reproducibles:** `data/external/dane_poblacion_municipal.meta.json`; SHA-256 del XLSX `1ea83594ad308becff39934a3977c102919c25740f60439be95d797396d11283`.
- **Lista municipal SGC:** POST a `https://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/municipios.php`, body `id_departamento=27-Santander` (HTTP 200). Entrega **87 nombres**; copia literal en `data/external/sgc_municipios_santander.csv`.
- **Crosswalk:** `data/external/crosswalk_municipios.csv`, normalización Unicode sin tildes + mayúsculas; **87/87 municipios cruzados**. 86 nombres coinciden exactamente; alias explícito y confirmado: SGC **El Carmen** → DANE **El Carmen de Chucurí**, DIVIPOLA `68235` (`alias_confirmado`). Sin cruces pendientes.
- Artefactos compactos para integración: `data/external_pub/dane_poblacion_municipal.csv` (783 filas) y `data/external_pub/crosswalk_municipios.csv` (87 municipios). Datos pesados y fuentes originales quedan en `data/external/` fuera de git.
- Filas de ejemplo reales (`divipola, municipio, anio, poblacion, area_total_o_cabecera`): `68001, Bucaramanga, 2018, 581138, 570756|10382`; `68001, Bucaramanga, 2019, 590543, 580133|10410`; `68001, Bucaramanga, 2020, 601668, 591209|10459`.

## INFERENCIA

Población total y por área geográfica son exposición municipal estable y útil para contextualizar priorización sísmica; una feature temporal debe usar solo la proyección publicada/disponible al corte definido. Se puede derivar densidad si se integra área municipal de fuente oficial compatible, pero no se calculó aquí. Proyección poblacional no mide vulnerabilidad estructural ni riesgo sísmico por sí misma.

## SUPOSICIÓN

La pestaña geográfica refleja la delimitación y códigos DIVIPOLA vigentes al producirse esta revisión; verificar correspondencia temporal si se compara con geografía histórica.

## Fuente descartada

**UNGRD `wwkg-r6te`: descartada como feature sísmica.** Consulta 2019–2022 de Santander halló solo **3 filas “SISMO”** y campos de daños consultados en cero; catálogo débil para señal predictiva sísmica. No usar agregados no sísmicos como proxy del daño por sismo sin justificación/validación. Catálogo: [API](https://www.datos.gov.co/resource/wwkg-r6te.json) · [metadatos](https://www.datos.gov.co/api/views/wwkg-r6te). Dataset anuncia CC BY-SA 4.0; la cobertura observada no valida 87/87.
