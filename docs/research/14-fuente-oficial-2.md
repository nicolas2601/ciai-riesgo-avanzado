# Segunda fuente oficial: evaluación rápida

Consulta ejecutada: **2026-10-13, 08:54–09:00 COT**. Criterio: utilidad real para enriquecer el catálogo sísmico SGC por municipio; no usar features observadas después del corte de predicción.

## HECHO

### Candidatas (máximo 3)

| Candidata y URL | Formato / cobertura | Licencia y variables potenciales sin fuga |
|---|---|---|
| **UNGRD histórico, `wwkg-r6te`**: [consulta API](https://www.datos.gov.co/resource/wwkg-r6te.json?$where=departamento%3D%27SANTANDER%27&$limit=2000) · [metadatos](https://www.datos.gov.co/api/views/wwkg-r6te) | JSON Socrata; eventos fechados 2019-01-01–2022-12-31. La consulta exacta `departamento='SANTANDER'` retorna 1.212 registros y 85 códigos distintos, pero uno es el código departamental `68`; solo 84 son DIVIPOLA municipales de cinco dígitos. | CC BY-SA 4.0 (`CC_40_BY_SA`); atribuir a UNGRD/Alcaldía de Saravena según metadatos. Agregables *hasta fecha de corte*: (1) eventos de sismo registrados, (2) eventos no sísmicos, (3) fallecidos/heridos/desaparecidos, (4) personas/familias afectadas, (5) viviendas destruidas/averiadas. Solo usar historia conocida antes del corte; no incluir evento objetivo ni reportes futuros. |
| **Inventario de movimientos en masa SGC**: [FeatureServer](https://services1.arcgis.com/Og2nrTKe5bptW02d/arcgis/rest/services/Inventario_de_movimientos_en_masa/FeatureServer) · [capa/query GeoJSON](https://services1.arcgis.com/Og2nrTKe5bptW02d/arcgis/rest/services/Inventario_de_movimientos_en_masa/FeatureServer/0/query?where=1%3D1&outFields=TIPO%2CSUBTIPO%2CCLAS_MAPA%2CETIQUETA_M%2CINV_MOVIMI&returnGeometry=true&outSR=4326&f=geojson&resultRecordCount=10) | Feature Service ArcGIS, puntos; inventario cartográfico sin campo de fecha. Cobertura espacial nacional aparente: extensión de capa incluye Colombia; cobertura municipal de Santander no cuantificada. Consulta de prueba respondió 200 y 10 features. | Registro SGC muestra `custom`; metadatos de licencia incompletos. No redistribuir antes de aclarar términos. Features posibles tras cruce espacial municipal: (1) conteo de puntos, (2) densidad por km², (3) proporción por tipo, (4) variedad de subtipos, (5) densidad por clase `CLAS_MAPA`. Sin fechas, no asegurar que inventario existiera a cortes históricos; válido solo como contexto espacial estático con limitación explícita. |
| **Eventos UNGRD 2023–2024, `rgre-6ak4`**: [consulta](https://www.datos.gov.co/resource/rgre-6ak4.json?$limit=1) · [metadatos](https://www.datos.gov.co/api/views/rgre-6ak4) | JSON Socrata; dataset descrito para 2023–2024; campos incluyen fecha, municipio, DIVIPOLA y afectaciones. Endpoint respondió 200. No se verificaron conteos/fechas por Santander. | CC BY-SA 4.0. Variables potenciales mismas de UNGRD histórico, solo con agregación temporal anterior al corte. Complementaría actualidad, pero no mezclar tablas sin armonizar esquemas/códigos. |

Verificación de enlace y respuesta: consultas HTTP 200 realizadas entre **08:54 y 09:00 COT**, 13-oct-2026. El catálogo del SGC por HTTPS también respondió 200. Consulta municipal del catálogo: `.../Consulta_Experta_Seiscomp/municipios.php?id_departamento=27-Santander` devolvió contenido HTML, pero el servidor respondió los nombres de **Amazonas**; no se pudo validar con ese endpoint la lista Santander de 87 municipios. No afirmar join completo.

Descarga local de la candidata UNGRD: `data/external/emergencias_ungrd_santander_2019_2022.json` (ignorada/no versionada). Contiene 1.212 filas; SHA-256 `8c7284498db6be207414a92bf54a0c91d5c1c164972262d75ccf0fa47efac34b`. Contiene 85 valores DIVIPOLA distintos: 84 códigos `68xxx` y un valor departamental `68`; no cubre/valida los 87 municipios completos.

## INFERENCIA

UNGRD es mejor complemento inmediato que población DANE para una narrativa de **impacto histórico observado**, porque ofrece afectación municipal y tiene cruces directos de eventos sísmicos (3 filas de “SISMO” halladas en 2019–2022 para Santander). Aun así, volumen/continuidad es débil para entrenar objetivo sísmico municipal: solo 3 registros sísmicos, y en los tres los campos de daños consultados aparecen en cero. El registro general mezcla amenazas; no tratar afectaciones de incendios/inundaciones como daño sísmico.

Inventario SGC sería más temáticamente próximo como covariable geográfica, pero su validez temporal y licencia no quedaron resueltas; además, movimientos en masa no equivalen a amenaza sísmica. Evitar `Aa` de NSR-10 como variable dinámica: es zonificación normativa estática, no catálogo de sacudida observada.

## SUPOSICIÓN

Los 87 municipios esperados corresponden al listado del reto; falta una lista DIVIPOLA oficial descargada/verificada en esta corrida. No se asume que municipios ausentes en UNGRD tengan cero eventos (ausencia de reporte no equivale a cero).

## Recomendación

Integrar **UNGRD histórico como fuente oficial complementaria**, con filtros por tipo de evento y atributos disponibles al corte; conservar `divipola` solo si cumple regex `^68[0-9]{3}$`, revisar nombres/códigos y marcar cobertura incompleta. Usarlo como contexto histórico/validación cualitativa, no como target sísmico ni fuente principal de features predictivas. Antes de afirmar cobertura 87/87, descargar DIVIPOLA oficial y medir el join. Atribuir bajo CC BY-SA 4.0 y verificar la obligación ShareAlike para derivados redistribuidos.
