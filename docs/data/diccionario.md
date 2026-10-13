# Diccionario del panel SGC

Generado por `python -m ml.eda.build_panel`; no editar cifras a mano.
HECHO: 8,961 filas, 45 columnas, 32 features SGC/DIVIPOLA/DANE; catálogo unificado 208,215 eventos.
HECHO: municipios sin cruce: {}.

| Feature | Tipo | Unidad / ventana / fuente | Justificación |
|---|---|---|---|
| n_eventos_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_eventos_3m | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_eventos_12m | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| mag_max_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| mag_max_3m | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| mag_media_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| mag_std_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_m_ge_3_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_m_ge_3_12m | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_m_ge_4_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_m_ge_4_12m | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| energia_log_3m | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| prof_media_mes | float64 | km; mes; SGC | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| prof_std_mes | float64 | km; mes; SGC | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| frac_prof_lt30 | float64 | proporción; mes; SGC; bandas[0,30),[30,70),[70,300],(300,+inf) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| frac_30_70 | float64 | proporción; mes; SGC; bandas[0,30),[30,70),[70,300],(300,+inf) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| frac_70_300 | float64 | proporción; mes; SGC; bandas[0,30),[30,70),[70,300],(300,+inf) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| frac_gt300 | float64 | proporción; mes; SGC; bandas[0,30),[30,70),[70,300],(300,+inf) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| rms_media_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| gap_media_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| fases_media_mes | float64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| dias_desde_ultimo_evento | float64 | días desde último registrado hasta fin de mes; -1=censurado; SGC | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| dias_desde_ultimo_m3 | float64 | días desde último registrado hasta fin de mes; -1=censurado; SGC | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_eventos_vecinos_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| centroid_lat | float64 | grados; snapshot directorio DIVIPOLA oficial en repo | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| centroid_lon | float64 | grados; snapshot directorio DIVIPOLA oficial en repo | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| hay_eventos_mes | int64 | magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| mc_maxc_12m | float64 | magnitud; MAXC histograma0.1, SOLO12meses anteriores/incluidoactual; SGC | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_m_ge_mc_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| n_eventos_departamento_mes | float64 | eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio) | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| year_context | int64 | año calendario del corte; contexto, NO medición de estaciones | Actividad/recencia/profundidad/calidad/contexto; solo pasado |
| poblacion | int64 | personas; DANE CNPV2018 proyección/estimación del año del corte, retrospectiva | Actividad/recencia/profundidad/calidad/contexto; solo pasado |

`energia_log_3m`=ln(1+sum(10^(1.5*M))) de3meses: índice relativo de magnitudes reportadas, NO joules ni homogeneización Mw.
Estadísticas de meses cubiertos sin eventos usan0 como sentinel junto a hay_eventos_mes; historia incompleta y estadísticas indefinidas quedan nulas.
Panel principal usa solo sistema nuevo desde2018-03. Catálogo antiguo incluido en archivo unificado, NO en conteos del panel comparable.
Targets separados: siguiente mes calendario completo; alto siM>=4, medio siM>=3sinM>=4, bajo sinM>=3. Último/gap sin seguimiento: target nulo.
Imputación/escalado corresponden a entrenamiento, nunca rellenar con futuro. Población DANE es proyección/estimación retrospectiva CNPV2018, NO observación ni disponibilidad histórica as-of demostrada.
Alias exacto auditado dentro de Santander y confirmado por crosswalk DANE: EL CARMEN→EL CARMEN DE CHUCURI, DIVIPOLA68235; municipio_sgc conserva nombre previo.
Cruce DANE: 87/87 municipios; 0 filas sin población. area_total_o_cabecera NO es km²: no se inventa densidad.
Más detecciones no prueba más sismicidad. Mc MAXC es aproximación regional, puede subestimar completitud; conteos M3/M4 fijos y contexto mensual/año permiten sensibilidad, no garantizan corrección de instrumentación.
Reward recomendado: target_actividad_m3_mes_siguiente, NO conteo crudo sin declarar sesgo; escoger umbral fijo Mc SOLO con train. Mc por año completo es EDA, no feature as-of.

## Balance real de target mensual
| Clase | Filas |
|---|---|
| bajo | 8466 |
| medio | 242 |
| alto | 166 |
| nan | 87 |

## Tres filas reales
```text
zone_id divipola   municipio   month feature_cutoff source_system  coverage_complete  history_12m_complete  eligible  n_eventos_mes  n_eventos_3m  n_eventos_12m  mag_max_mes  mag_max_3m  mag_media_mes  mag_std_mes  n_m_ge_3_mes  n_m_ge_3_12m  n_m_ge_4_mes  n_m_ge_4_12m  energia_log_3m  prof_media_mes  prof_std_mes  frac_prof_lt30  frac_30_70  frac_70_300  frac_gt300  rms_media_mes  gap_media_mes  fases_media_mes  dias_desde_ultimo_evento  dias_desde_ultimo_m3  n_eventos_vecinos_mes  centroid_lat  centroid_lon  hay_eventos_mes  mc_maxc_12m  n_m_ge_mc_mes  n_eventos_departamento_mes  year_context  poblacion  target_n_eventos_mes_siguiente target_clase_mes_siguiente  target_actividad_m3_mes_siguiente target_month
  68001    68001 BUCARAMANGA 2018-03     2018-03-31           new               True                 False     False            1.0           NaN            NaN          1.5         NaN            1.5          NaN           0.0           NaN           0.0           NaN             NaN          141.49           NaN             0.0         0.0          1.0         0.0            0.4          205.0             16.0                      19.0                  -1.0                  694.0      7.155475    -73.111332                1          1.7            0.0                       891.0          2018     581138                             0.0                       bajo                                0.0      2018-04
  68001    68001 BUCARAMANGA 2018-04     2018-04-30           new               True                 False     False            0.0           NaN            NaN          0.0         NaN            0.0          0.0           0.0           NaN           0.0           NaN             NaN            0.00           0.0             0.0         0.0          0.0         0.0            0.0            0.0              0.0                      49.0                  -1.0                  733.0      7.155475    -73.111332                0          1.7            0.0                       947.0          2018     581138                             0.0                       bajo                                0.0      2018-05
  68001    68001 BUCARAMANGA 2018-05     2018-05-31           new               True                 False     False            0.0           1.0            NaN          0.0         1.5            0.0          0.0           0.0           NaN           0.0           NaN        5.186424            0.00           0.0             0.0         0.0          0.0         0.0            0.0            0.0              0.0                      80.0                  -1.0                  707.0      7.155475    -73.111332                0          1.7            0.0                       883.0          2018     581138                             1.0                       bajo                                0.0      2018-06
```
