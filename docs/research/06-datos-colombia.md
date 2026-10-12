# Datos abiertos colombianos con etiqueta real de eventos

Consulta: 2026-10-12, directo contra la API Socrata de datos.gov.co y APIs publicas. Todo numero de este documento salio de una consulta ejecutada ese dia (HECHO), salvo lo marcado INFERENCIA o SUPOSICION. Complementa `01-datasets.md` (fuentes globales).

## Resumen ejecutivo

- HECHO: existe una etiqueta real, publica y continua 2019-2025 de eventos de emergencia por municipio: las tablas "Emergencias UNGRD". Para Santander (filtro exacto `departamento = 'SANTANDER'`) suman 2 641 registros (1 212 + 927 + 502).
- HECHO: las coordenadas de esas tablas son inutilizables (ver mas abajo). La unidad espacial viable es el **municipio** (codigo DIVIPOLA), no una celda H3.
- HECHO: meteorologia diaria por municipio se obtiene sin llave desde Open-Meteo y NASA POWER (probado). Indice ENSO desde NOAA (ONI), actualizado a 2026.
- INFERENCIA: con 87 municipios x 84 meses el panel mide ~7 300 filas y ~2 641 eventos repartidos entre amenazas: viable en CPU. El valor esta en la validacion y la incertidumbre, no en el tamano del modelo. Con tan pocos eventos por amenaza, el gate de clases por fold es una restriccion real.
- SUPOSICION: que el reto pida Santander y riesgo por amenaza natural. Sin enunciado, esto es lo mejor evidenciado.

## 1. Emergencias UNGRD (etiqueta)

Tres tablas que, juntas, cubren 2019-2025 sin huecos. Licencia CC BY 4.0 / CC BY-SA 4.0 (atribucion a UNGRD; la variante BY-SA exige compartir igual los derivados).

| ID | Periodo | Filas | Santander | Coordenadas |
|---|---|---|---|---|
| `wwkg-r6te` | 2019-01-01 a 2022-12-31 | 25 857 | 1 212 | sin columna |
| `rgre-6ak4` | 2023-01-01 a 2024-12-31 | 16 036 | 927 | columna, pero basura |
| `2343-nuqp` | 2025-01-01 a 2025-12-31 | 13 012 | 502 | columna, pero basura |

CORRECCION (2026-10-12): una primera version de este documento conto 4 958 porque filtro con `LIKE '%SANTANDER%'`, que incluye NORTE DE SANTANDER (1 415 + 398 + 504 = 2 317). Detectado por la revision cruzada con uts2 y verificado con consultas exactas. Filtrar siempre con igualdad exacta (o prefijo DIVIPOLA `68`, ver riesgo 5).

Endpoint: `https://www.datos.gov.co/resource/<ID>.json` (SoQL: `$select`, `$where`, `$group`, `$limit`; paginar con `$offset`).

Columnas utiles: `fecha`, `departamento`, `municipio`, `evento`, `divipola` (o `codificaci_n_segun_divipola`), `fallecidos`/`muertos`, `heridos`, `personas`, `familias`, `viviendas_destruidas`, `viviendas_averiadas`, `hectareas`. Los nombres de columna cambian entre tablas: armonizar.

Eventos en Santander (HECHO, conteos por tabla en orden 2019-22 / 2023-24 / 2025):

| Amenaza | 2019-22 | 2023-24 | 2025 | Total |
|---|---|---|---|---|
| Incendio de cobertura vegetal / forestal | 439 | 677 | 274 | 1 390 |
| Movimiento en masa | 235 | 47 | 80 | 362 |
| Inundacion | 187 | 58 | 34 | 279 |
| Creciente subita | 123 | 21 | 44 | 188 |
| Avenida torrencial | 29 | 9 | 10 | 48 |

El nombre del evento cambia ("INCENDIO DE COBERTURA VEGETAL" vs "INCENDIO FORESTAL"): mapear a una categoria unica antes de contar.

### Riesgos verificados de esta etiqueta

1. **Coordenadas inservibles (HECHO).** En `2343-nuqp`, 13 008 de 13 012 filas tienen `coordenadas = '0'`; en `rgre-6ak4`, 1 428 son `0` y muestras del resto vienen como `'- 0'` o texto libre (`4°56'24.6"N  W 75°12'19.2"`). No usar como punto. Consecuencia: unidad = municipio.
2. **Salto en 2022 (HECHO el numero; la causa es SUPOSICION).** Movimiento en masa en Santander: 32, 23, 24 y 156 (2019 a 2022); a nivel nacional 2022 tiene 13 665 filas contra ~4 000 de los otros anos. Dos explicaciones no excluyentes: ano muy lluvioso (La Nina) o cambio en el registro. No se puede distinguir con estos datos. Mitigacion: la validacion temporal debe incluir 2022 en test y en train en corridas distintas, y reportar la sensibilidad.
3. **Sesgo de reporte (INFERENCIA).** Un evento existe si alguien lo reporto: municipios con mas capacidad institucional reportan mas. Es un indice de "emergencias atendidas", no de amenaza fisica. Documentarlo en la web.
4. **Tres tablas, tres esquemas.** Deduplicar y validar que no haya eventos repetidos en los bordes de ano.
5. **DIVIPOLA corrupto en 2025 (HECHO).** En `2343-nuqp`, Santander tiene 198 pares codigo-municipio y solo 70 nombres distintos; hay codigos como `22269` para SUAITA, `22978` para BARRANCABERMEJA o `20696` para GIRON (cuyos codigos reales empiezan por 68). En 2019-2024 los codigos validos de Santander son 85 por tabla. Regla: unir por nombre de municipio normalizado (mayusculas, sin tildes) y departamento, y validar contra los 87 municipios de `kqut-4h4r`; descartar o revisar filas que no resuelvan.

## 2. Unidad espacial: municipios (DIVIPOLA)

- HECHO: `kqut-4h4r` lista 87 municipios de Santander (departamento 68). En 2019-2022 y 2023-2024 aparecen 85 codigos DIVIPOLA distintos de Santander por tabla; en 2025 el codigo no es confiable (riesgo 5).
- HECHO: `kqut-4h4r` (Directorio Georreferenciado DIVIPOLA) trae `divipola_municipio`, `latitud_municipio`, `longitud_municipio`: sirve para centroides. Tiene una fila por entidad; deduplicar por municipio.
- PENDIENTE: poligonos municipales para el mapa coropletico (fuente por verificar: DANE MGN). Plan B ya valido: puntos (centroides) con circulo proporcional al score.

## 3. Covariables sin llave de API (HECHO: probadas hoy)

| Fuente | Que da | Prueba | Nota |
|---|---|---|---|
| Open-Meteo Archive (ERA5) | lluvia, temperatura, evapotranspiracion diaria por lat/lon | respuesta valida para (7.12, -73.12) | uso no comercial; limite de tasa: pedir por lotes |
| NASA POWER (API diaria) | `PRECTOTCORR`, `T2M`, `GWETROOT` (humedad de suelo de raiz) | respuesta valida | humedad de suelo es util para incendios |
| IDEAM Precipitacion `s54a-sgyg` | lluvia cada 10 min por estacion con lat/lon | muestra valida, actualizada 2026-10-12 | CC BY-SA 4.0; tabla enorme: el conteo total agoto el tiempo; filtrar por departamento y fecha |
| NOAA ONI | indice ENSO trimestral | archivo de 23 KB, ultima fila JAS 2026 = +2.16 | exogeno global, mismo valor para todo el pais |

IDEAM tambien publica el Catalogo Nacional de Estaciones (`hp9r-jxuu`) y viento, presion y temperatura, no explorados a fondo.

Seria util sumar DEM y pendiente por municipio (Copernicus GLO-30, ver 01-datasets) y poblacion (WorldPop), ambos ya documentados.

## 4. Hallazgo de contexto: ENSO

- HECHO: ONI del trimestre JAS 2026 = +2.16 (El Nino fuerte, umbral de El Nino >= +0.5).
- HIPOTESIS (no verificada): 2023-24, ano de El Nino, concentra 677 incendios en Santander (el mayor bloque), y 2022 concentra los movimientos en masa. Si se confirma con el modelo, "El Nino sube el riesgo de incendio, La Nina el de inundacion y deslizamiento" es un mensaje claro y defendible.
- RIESGO: el valor actual de ONI puede quedar fuera del rango visto en entrenamiento. Marcar extrapolacion en la API.

## 5. Definicion de target recomendada

Un modelo por amenaza o un target multiclase por amenaza, nunca una mezcla opaca:

1. Panel `municipio x mes` (87 x 84 ~ 7 300 filas) con conteo de eventos de la amenaza en el MES SIGUIENTE.
2. Nivel por la regla de `01-datasets.md` (cero = bajo; mediana de positivos en train = medio/alto). Con incendios hay soporte; con movimientos en masa (362 eventos) puede faltar soporte en alguna clase: aplicar el gate de la regla y caer a binario si falla.
3. Features solo del pasado: lluvia y humedad rezagadas, ONI, estacionalidad, eventos previos del municipio y vecinos, pendiente y poblacion.

## 6. Gate para H1 (30 min)

- Descargar las tres tablas de Santander (igualdad exacta), armonizar columnas y resolver municipio por nombre normalizado: 15 min.
- Panel municipio-mes con conteo por amenaza y por clase: 10 min.
- Decision: amenaza principal y si el nivel es ternario o binario: 5 min.

## Fuentes

- [Emergencias UNGRD 2019-2022 (wwkg-r6te)](https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Emergencias-UNGRD-/wwkg-r6te)
- [Emergencias UNGRD 2023-2024 (rgre-6ak4)](https://www.datos.gov.co/resource/rgre-6ak4.json)
- [Emergencias UNGRD V2, 2025 (2343-nuqp)](https://www.datos.gov.co/resource/2343-nuqp.json)
- [Directorio georreferenciado DIVIPOLA (kqut-4h4r)](https://www.datos.gov.co/resource/kqut-4h4r.json)
- [IDEAM Precipitacion (s54a-sgyg)](https://www.datos.gov.co/resource/s54a-sgyg.json)
- [Catalogo Nacional de Estaciones IDEAM (hp9r-jxuu)](https://www.datos.gov.co/resource/hp9r-jxuu.json)
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [NASA POWER API](https://power.larc.nasa.gov/docs/services/api/)
- [NOAA CPC ONI](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt)
