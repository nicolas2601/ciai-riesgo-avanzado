# EDA del catálogo sísmico SGC

Generado por `uv run --group reto python -m ml.eda.eda_sgc`; cifras generadas por script.

## Cobertura y calidad

- Filas tras deduplicación: **208,215**; duplicados exactos removidos por `(datetime_utc, lat, lon, depth_km, mag)`: **35**.
- Rango: **1993-06-01 01:32 UTC–2026-10-13 11:35 UTC**. Sistemas: old **105,728**, new **102,487**.
- Nulos: datetime_utc=0; lat=0; lon=0; depth_km=0; mag=0; mag_type=0; municipio=0; source_system=0; rms=88; gap=88; phases=0; source_file=0.
### Eventos por año y sistema

| Año | Old | New |
|---|---:|---:|
| 1993 | 1,238 | 0 |
| 1994 | 1,771 | 0 |
| 1995 | 2,037 | 0 |
| 1996 | 1,483 | 0 |
| 1997 | 1,125 | 0 |
| 1998 | 1,564 | 0 |
| 1999 | 1,741 | 0 |
| 2000 | 1,913 | 0 |
| 2001 | 3,060 | 0 |
| 2002 | 3,523 | 0 |
| 2003 | 3,747 | 0 |
| 2004 | 3,786 | 0 |
| 2005 | 3,541 | 0 |
| 2006 | 3,075 | 0 |
| 2007 | 2,414 | 0 |
| 2008 | 2,560 | 0 |
| 2009 | 5,030 | 0 |
| 2010 | 6,730 | 0 |
| 2011 | 7,560 | 0 |
| 2012 | 8,547 | 0 |
| 2013 | 7,857 | 0 |
| 2014 | 6,981 | 0 |
| 2015 | 5,818 | 0 |
| 2016 | 7,964 | 0 |
| 2017 | 9,574 | 0 |
| 2018 | 1,089 | 8,966 |
| 2019 | 0 | 12,738 |
| 2020 | 0 | 12,841 |
| 2021 | 0 | 11,773 |
| 2022 | 0 | 11,244 |
| 2023 | 0 | 12,250 |
| 2024 | 0 | 15,974 |
| 2025 | 0 | 11,641 |
| 2026 | 0 | 5,060 |

## Distribuciones (new; 2018-03+)

Cuantil: 0% M=0.00, z=-4.88 km; 25% M=1.60, z=132.71 km; 50% M=1.80, z=140.29 km; 75% M=2.00, z=145.37 km; 90% M=2.40, z=149.00 km; 95% M=2.70, z=151.21 km; 99% M=3.40, z=158.37 km; 100% M=5.80, z=212.77 km.
### Municipios con más eventos

Los Santos: **55.2%** de 102,487 eventos new.

LOS SANTOS: 56,552 (55.2%); ZAPATOCA: 13,644 (13.3%); VILLANUEVA: 4,681 (4.6%); EL CARMEN: 2,492 (2.4%); SAN VICENTE DE CHUCURI: 2,024 (2.0%); JORDAN: 1,771 (1.7%); RIONEGRO: 1,634 (1.6%); BARICHARA: 1,424 (1.4%); GIRON: 1,281 (1.2%); SANTA HELENA DEL OPON: 1,228 (1.2%).

## Completitud aproximada por año

MAXC = moda anual de bins 0.1; aproximación exploratoria, no Mc validada. Escalas old/new difieren.

Año/sistema:Mc/N — 1993 o:2.8, 1994 o:3.1, 1995 o:3.0, 1996 o:3.0, 1997 o:2.9, 1998 o:2.8, 1999 o:2.7, 2000 o:3.1, 2001 o:2.5, 2002 o:2.3, 2003 o:2.3, 2004 o:2.3, 2005 o:2.2, 2006 o:2.2, 2007 o:2.3, 2008 o:2.0, 2009 o:1.8, 2010 o:1.7, 2011 o:1.7, 2012 o:1.6, 2013 o:1.7, 2014 o:1.6, 2015 o:1.7, 2016 o:1.5, 2017 o:1.4, 2018 n:1.7, 2019 n:1.7, 2020 n:1.7, 2021 n:1.7, 2022 n:1.7, 2023 n:1.7, 2024 n:1.8, 2025 n:1.8, 2026 n:1.6.

**HIPÓTESIS:** el aumento de registros entre 2008 y 2012 es consistente con mejoras/cambios de instrumentación y cobertura; el catálogo por sí solo no establece causalidad.

## Eventos de referencia del catálogo

2015-03-10 Mw old y dos mayores new; escalas no convertidas.

| Fecha UTC | M | Tipo | Prof. km | Municipio | Sistema |
|---|---|---|---|---|---|
| 2015-03-10 20:55 UTC | 6.4 | Mw | 157.7 | LOS SANTOS | old |
| 2023-03-10 09:18 UTC | 5.5 | Mw | 150.5 | LOS SANTOS | new |
| 2025-12-10 08:27 UTC | 5.8 | MLr_3 | 149.5 | LOS SANTOS | new |
| 2018-08-07 15:53 UTC | 5.6 | Mw(mB) | 150.0 | LOS SANTOS | new |

## Balance de clases por municipio

Clases observadas en t: bajo sin M≥3; medio ≥1 M3.0–3.9 y sin M≥4; alto ≥1 M≥4. New comparable desde 2018-03.

Observado t: municipio-mes **8,961**. Municipio-año completo **609**; años parciales omitidos (2018:10m, 2026:9m).

| Clase | Municipio-mes | Municipio-año |
|---|---|---|
| bajo | 8550 | 481 |
| medio | 244 | 99 |
| alto | 167 | 29 |

**Balance target entrenamiento t+1:** 8466 bajo / 242 medio / 166 alto; 87 sin siguiente mes completo (total 8,961). No confundir con clase observada en t.
**Recomendación:** usar municipio-mes para horizonte mensual. Balance target t+1 es 8466/242/166, muy desbalanceado; anual completo (609) como sensibilidad, pierde orden intranual. Comparar con baseline.

## Limitaciones

- old/new y escalas no armonizadas; MAXC exploratoria. Más detecciones no prueba cambio físico de amenaza.
