# EDA del catálogo sísmico SGC

Generado por `uv run --group reto python -m ml.eda.eda_sgc`; todas las cifras de este informe salen del script.

## Cobertura y calidad

- Filas tras deduplicación: **208,215**; duplicados exactos removidos por `(datetime_utc, lat, lon, depth_km, mag)`: **35**.
- Rango: **1993-06-01 01:32 UTC–2026-10-13 11:35 UTC**. Sistemas: old **105,728**, new **102,487**.
- Nulos por columna:

| Columna | Nulos |
|---|---|
| datetime_utc | 0 |
| lat | 0 |
| lon | 0 |
| depth_km | 0 |
| mag | 0 |
| mag_type | 0 |
| municipio | 0 |
| source_system | 0 |
| rms | 88 |
| gap | 88 |
| phases | 0 |
| source_file | 0 |

### Eventos por año y sistema

| Año | Sistema | Eventos |
|---|---|---|
| 1993 | old | 1238 |
| 1994 | old | 1771 |
| 1995 | old | 2037 |
| 1996 | old | 1483 |
| 1997 | old | 1125 |
| 1998 | old | 1564 |
| 1999 | old | 1741 |
| 2000 | old | 1913 |
| 2001 | old | 3060 |
| 2002 | old | 3523 |
| 2003 | old | 3747 |
| 2004 | old | 3786 |
| 2005 | old | 3541 |
| 2006 | old | 3075 |
| 2007 | old | 2414 |
| 2008 | old | 2560 |
| 2009 | old | 5030 |
| 2010 | old | 6730 |
| 2011 | old | 7560 |
| 2012 | old | 8547 |
| 2013 | old | 7857 |
| 2014 | old | 6981 |
| 2015 | old | 5818 |
| 2016 | old | 7964 |
| 2017 | old | 9574 |
| 2018 | new | 8966 |
| 2018 | old | 1089 |
| 2019 | new | 12738 |
| 2020 | new | 12841 |
| 2021 | new | 11773 |
| 2022 | new | 11244 |
| 2023 | new | 12250 |
| 2024 | new | 15974 |
| 2025 | new | 11641 |
| 2026 | new | 5060 |

## Distribuciones (sistema nuevo; 2018-03 en adelante)

| Cuantil | Magnitud | Profundidad (km) |
|---|---|---|
| 0% | 0.00 | -4.88 |
| 25% | 1.60 | 132.71 |
| 50% | 1.80 | 140.29 |
| 75% | 2.00 | 145.37 |
| 90% | 2.40 | 149.00 |
| 95% | 2.70 | 151.21 |
| 99% | 3.40 | 158.37 |
| 100% | 5.80 | 212.77 |

### Municipios con más eventos

Los Santos representa **55.2%** de los 102,487 registros nuevos.

| Municipio | Eventos | % del catálogo nuevo |
|---|---|---|
| LOS SANTOS | 56552 | 55.2 |
| ZAPATOCA | 13644 | 13.3 |
| VILLANUEVA | 4681 | 4.6 |
| EL CARMEN | 2492 | 2.4 |
| SAN VICENTE DE CHUCURI | 2024 | 2.0 |
| JORDAN | 1771 | 1.7 |
| RIONEGRO | 1634 | 1.6 |
| BARICHARA | 1424 | 1.4 |
| GIRON | 1281 | 1.2 |
| SANTA HELENA DEL OPON | 1228 | 1.2 |

## Completitud aproximada por año

MAXC aproximado: magnitud con mayor frecuencia en histograma de ancho 0.1; se informa como descriptor de la moda, **no como Mc validada** ni como umbral de completitud robusto. Mezcla sistemas/escalas y cortes anuales; comparar con cautela.

| Año | Sistema | N | Moda MAXC (M) |
|---|---|---|---|
| 1993 | old | 1238 | 2.8 |
| 1994 | old | 1771 | 3.1 |
| 1995 | old | 2037 | 3.0 |
| 1996 | old | 1483 | 3.0 |
| 1997 | old | 1125 | 2.9 |
| 1998 | old | 1564 | 2.8 |
| 1999 | old | 1741 | 2.7 |
| 2000 | old | 1913 | 3.1 |
| 2001 | old | 3060 | 2.5 |
| 2002 | old | 3523 | 2.3 |
| 2003 | old | 3747 | 2.3 |
| 2004 | old | 3786 | 2.3 |
| 2005 | old | 3541 | 2.2 |
| 2006 | old | 3075 | 2.2 |
| 2007 | old | 2414 | 2.3 |
| 2008 | old | 2560 | 2.0 |
| 2009 | old | 5030 | 1.8 |
| 2010 | old | 6730 | 1.7 |
| 2011 | old | 7560 | 1.7 |
| 2012 | old | 8547 | 1.6 |
| 2013 | old | 7857 | 1.7 |
| 2014 | old | 6981 | 1.6 |
| 2015 | old | 5818 | 1.7 |
| 2016 | old | 7964 | 1.5 |
| 2017 | old | 9574 | 1.4 |
| 2018 | new | 8966 | 1.7 |
| 2019 | new | 12738 | 1.7 |
| 2020 | new | 12841 | 1.7 |
| 2021 | new | 11773 | 1.7 |
| 2022 | new | 11244 | 1.7 |
| 2023 | new | 12250 | 1.7 |
| 2024 | new | 15974 | 1.8 |
| 2025 | new | 11641 | 1.8 |
| 2026 | new | 5060 | 1.6 |

**HIPÓTESIS:** el aumento de registros entre 2008 y 2012 es consistente con mejoras/cambios de instrumentación y cobertura; el catálogo por sí solo no establece causalidad.

## Eventos de referencia del catálogo

2015-03-10 usa la magnitud Mw disponible en el catálogo antiguo; puede diferir de estimaciones de otras agencias. Se muestran también los dos mayores eventos del sistema nuevo; no se convierten escalas.

| Fecha UTC | M | Tipo | Prof. km | Municipio | Sistema |
|---|---|---|---|---|---|
| 2015-03-10 20:55 UTC | 6.4 | Mw | 157.7 | LOS SANTOS | old |
| 2023-03-10 09:18 UTC | 5.5 | Mw | 150.5 | LOS SANTOS | new |
| 2025-12-10 08:27 UTC | 5.8 | MLr_3 | 149.5 | LOS SANTOS | new |
| 2018-08-07 15:53 UTC | 5.6 | Mw(mB) | 150.0 | LOS SANTOS | new |

## Balance de clases por municipio

Definición por período: bajo = sin M≥3; medio = al menos un M3.0–3.9 y sin M≥4; alto = al menos un M≥4. Sistema nuevo comparable desde 2018-03. Los conteos usan la cuadrícula completa de municipios observados × todos los meses y años del período; una celda sin evento catalogado queda como bajo.

Filas: municipio-mes **9,048**; municipio-año **783**.

| Clase | Municipio-mes | Municipio-año |
|---|---|---|
| bajo | 8636 | 625 |
| medio | 245 | 121 |
| alto | 167 | 37 |

**Recomendación:** usar municipio-mes para priorización temporal: hay 167 períodos altos y 245 medios (9,048 celdas; fuerte desbalance), lo que preserva resolución y permite horizonte mensual. Municipio-año reduce el número de celdas a 783 y oculta variación intranual; usarlo como sensibilidad/agregado, no como unidad primaria. Reportar desbalance y comparar con baseline.

## Limitaciones

- El salto de versión old→new alrededor de 2018 impide interpretar diferencias de conteo/magnitud sin armonización; el tipo de magnitud se conserva.
- MAXC anual con muestras y escalas mezcladas es solo exploratorio; no inferir cambio físico de amenaza desde más detecciones.
