# Auditoría del panel municipal

Panel: `/home/hotpot/Descargas/ciai-riesgo-avanzado/data/panel/panel_municipio_mes.csv.gz`
SHA-256: `92cb622123e471487df9ef6e617023ef216a82617bd3dbc8ffbd5da3db63e400`
Filas: 8961, columnas: 45.
Municipios: 87; meses: 103 (2018-03 a 2026-09).
Duplicados (zona, mes): 0.

## Target
Conteos: {'bajo': 8466, 'medio': 242, 'alto': 166}; sin target: 87.
Elegibles: 8004; elegibles con etiqueta: 7917.
Fracción baja entre etiquetadas: 0.954.
Actividad M>=3 positiva: 408 filas.

## Features
En contrato: 32; constantes: ['frac_gt300'].
Con infinitos: ninguna.
Tipo objeto: ninguna.
Columnas de futuro en X: ninguna.
IDs o meta en X: ninguna.

## Particiones temporales
- train: 63 meses (2019-02 a 2024-04), 5481 filas, clases {'bajo': 5225, 'medio': 145, 'alto': 111}.
- val: 13 meses (2024-05 a 2025-05), 1131 filas, clases {'bajo': 1075, 'medio': 35, 'alto': 21}.
- test: 15 meses (2025-06 a 2026-08), 1305 filas, clases {'bajo': 1245, 'medio': 41, 'alto': 19}.

## Nulos por columna

- energia_log_3m: 174
- mag_max_3m: 174
- mag_std_mes: 1463
- n_eventos_12m: 957
- n_eventos_3m: 174
- n_m_ge_3_12m: 957
- n_m_ge_4_12m: 957
- prof_std_mes: 1463
- target_actividad_m3_mes_siguiente: 87
- target_clase_mes_siguiente: 87
- target_n_eventos_mes_siguiente: 87

## Notas de contrato

- poblacion: DANE CNPV2018 retrospective projection; not as-of availability.
- catalog: retrospective/revised SGC catalog; backtest, not as-of operation.
- year_context: cutoff year kept per contract; may memorize time trends.
