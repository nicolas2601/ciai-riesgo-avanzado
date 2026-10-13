# Medio: perfiles territoriales no supervisados

Reproducir: `uv run python -m ml.medio.run`.

HECHO: 87 municipios, 21 variables, ajuste hasta 2025-05; no usa filas 2025-06+ ni targets.
HECHO: KMeans k=3, silhouette=0.277747, Davies-Bouldin=1.062347; k elegido3..7 por silhouette/DB, n_init20, seed7.
HECHO: estabilidad ARI contra seed7 (7/21/42)={'7': 1.0, '21': 0.3869513481667637, '42': 1.0}.
HECHO: contraste jerárquico mismo k: silhouette=0.285382, ARI vsKMeans=0.679173.

| Grupo | Municipios | Perfil relativo (no riesgo oficial) |
|---|---:|---|
| 0 | 19 | frac_prof_lt30 mayor; frac_70_300 menor; gap_media_mes mayor |
| 1 | 66 | frac_prof_lt30 menor; centroid_lon menor; gap_media_mes menor |
| 2 | 2 | fraction_months_m4 mayor; n_m_ge_4_mes mayor; fraction_months_m3 mayor |

HECHO: Los Santos cae en grupo2; tamaño=2.
INFERENCIA: separación describe heterogeneidad de actividad registrada/exposición/geografía; no demuestra daño ni riesgo ni causalidad.
SUPOSICIÓN: centroides representan municipio para visualización; no ubicaciones de terremotos ni polígonos de área afectada.
Ventana de ajuste Medio incluye validación previa del supervisado/RL, NO es train original de esos modelos. Métricas internas, no desempeño fuera de muestra.
Promedios de descriptores sísmicos sobre meses con eventos; máximo histórico de mag_max_mes; frecuencias sobre todos los meses cubiertos. Estandarización e imputación mediana solo sobre perfiles pre-cutoff.
DANE: proyección retrospectiva CNPV2018, no población observada ni disponibilidad as-of demostrada. Escalas magnitud no homogenizadas; más registros puede reflejar instrumentación.
Variables constantes/indefinidas se imputan, no garantizan relevancia; centroides/población pueden dominar grupos. Labels arbitrarios: no ordenar grupos como bajo/medio/alto.
Mapa monocromo con símbolos distintos/leyenda y tabla JSON: identificación no depende de colores; los grupos pequeños/singletons se reportan sin ocultarlos.
JSON: `app/web/public/data/clusters.json`; mapa: `docs/figures/medio-clusters.png`; modelo propio: `ml/medio/kmeans.joblib`.
Fuentes: panel SGC+DANE y diccionario `docs/data/diccionario.md`; metadata JSON conserva SHA256. API scikit-learn verificada por Context7.
