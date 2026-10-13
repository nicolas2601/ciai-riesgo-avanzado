"""Unsupervised municipal clustering from past territorial descriptors only."""

import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

FIT_UNTIL = "2025-05"
SEEDS = (7, 21, 42)
BASE_FEATURES = [
    "n_eventos_mes",
    "mag_max_mes",
    "mag_media_mes",
    "prof_media_mes",
    "frac_prof_lt30",
    "frac_30_70",
    "frac_70_300",
    "frac_gt300",
    "rms_media_mes",
    "gap_media_mes",
    "fases_media_mes",
    "energia_log_3m",
    "n_eventos_vecinos_mes",
    "poblacion",
    "centroid_lat",
    "centroid_lon",
    "n_m_ge_3_mes",
    "n_m_ge_4_mes",
]
EVENT_DESCRIPTORS = [
    "mag_media_mes",
    "prof_media_mes",
    "frac_prof_lt30",
    "frac_30_70",
    "frac_70_300",
    "frac_gt300",
    "rms_media_mes",
    "gap_media_mes",
    "fases_media_mes",
]


def aggregate_profiles(panel: pd.DataFrame, fit_until: str = FIT_UNTIL) -> pd.DataFrame:
    """Aggregate covered months through fit_until; no target column is referenced."""
    covered = panel.coverage_complete.astype(str).str.lower().isin(["true", "1"])
    past = panel.loc[covered & panel.month.le(fit_until)].copy()
    if past.empty:
        raise ValueError("No covered fitting rows before cutoff")
    past["divipola"] = past.divipola.astype(str).str.zfill(5)
    groups = past.groupby("divipola", sort=True)
    profiles = groups[BASE_FEATURES].mean()
    active = past.loc[past.n_eventos_mes.gt(0)]
    profiles[EVENT_DESCRIPTORS] = active.groupby("divipola")[EVENT_DESCRIPTORS].mean()
    profiles["mag_max_mes"] = groups.mag_max_mes.max()
    profiles["event_frequency_std"] = groups.n_eventos_mes.std()
    profiles["fraction_months_m3"] = groups.n_m_ge_3_mes.agg(lambda values: values.gt(0).mean())
    profiles["fraction_months_m4"] = groups.n_m_ge_4_mes.agg(lambda values: values.gt(0).mean())
    return profiles


def fit_clusters(profiles: pd.DataFrame, seed: int = 7) -> dict:
    """Select k by silhouette, DB tie-break; assess seed and algorithm stability."""
    if len(profiles) < 8:
        raise ValueError("Need at least eight municipal profiles for k=3..7")
    imputer = SimpleImputer(strategy="median", keep_empty_features=True)
    scaler = StandardScaler()
    values = scaler.fit_transform(imputer.fit_transform(profiles))
    candidates = []
    with threadpool_limits(limits=1):
        for k in range(3, 8):
            model = KMeans(n_clusters=k, n_init=20, random_state=seed).fit(values)
            candidates.append(
                {
                    "k": k,
                    "silhouette": float(silhouette_score(values, model.labels_)),
                    "davies_bouldin": float(davies_bouldin_score(values, model.labels_)),
                    "model": model,
                }
            )
        winner = max(
            candidates, key=lambda row: (row["silhouette"], -row["davies_bouldin"], -row["k"])
        )
        labels = winner["model"].labels_
        stability = {
            str(other): float(
                adjusted_rand_score(
                    labels,
                    KMeans(n_clusters=winner["k"], n_init=20, random_state=other).fit_predict(
                        values
                    ),
                )
            )
            for other in SEEDS
        }
        comparison = AgglomerativeClustering(n_clusters=winner["k"]).fit_predict(values)
    return {
        **winner,
        "labels": labels,
        "scaled": values,
        "imputer": imputer,
        "scaler": scaler,
        "stability_ari": stability,
        "candidates": candidates,
        "agglomerative_silhouette": float(silhouette_score(values, comparison)),
        "agglomerative_ari": float(adjusted_rand_score(labels, comparison)),
    }
