"""Fit Medio and publish a real JSON, reproducible map and concise report."""

import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from ml.medio.model import FIT_UNTIL, aggregate_profiles, fit_clusters

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "data/panel/panel_municipio_mes.csv.gz"
OUTPUT = ROOT / "app/web/public/data/clusters.json"


def describe_groups(profiles: pd.DataFrame, result: dict) -> list[dict]:
    groups = []
    for cluster in sorted(np.unique(result["labels"])):
        mask = result["labels"] == cluster
        center = result["scaled"][mask].mean(axis=0)
        strongest = np.argsort(np.abs(center))[-3:][::-1]
        traits = [
            {
                "variable": profiles.columns[i],
                "direccion": "mayor" if center[i] > 0 else "menor",
                "desviaciones_estandar": round(float(center[i]), 3),
            }
            for i in strongest
        ]
        label = "; ".join(f"{trait['variable']} {trait['direccion']}" for trait in traits)
        groups.append(
            {
                "cluster": int(cluster),
                "etiqueta": label,
                "n_municipios": int(mask.sum()),
                "municipios": profiles.index[mask].tolist(),
                "rasgos": traits,
                "medias": profiles.loc[mask].mean().replace({np.nan: None}).to_dict(),
            }
        )
    return groups


def make_payload(panel: pd.DataFrame, profiles: pd.DataFrame, result: dict) -> dict:
    names = panel[["divipola", "municipio"]].drop_duplicates().set_index("divipola").municipio
    groups = describe_groups(profiles, result)
    labels = {group["cluster"]: group["etiqueta"] for group in groups}
    records = municipality_records(profiles, result, names, labels)
    metrics = {
        key: result[key]
        for key in [
            "k",
            "silhouette",
            "davies_bouldin",
            "stability_ari",
            "agglomerative_silhouette",
            "agglomerative_ari",
        ]
    }
    metrics["candidatos"] = [
        {key: row[key] for key in ["k", "silhouette", "davies_bouldin"]}
        for row in result["candidates"]
    ]
    return {
        "municipios": records,
        "perfiles": groups,
        "metricas": metrics,
        "metadata": {
            "fit_until": FIT_UNTIL,
            "features": profiles.columns.tolist(),
            "metodo": "KMeans",
            "ejemplo": False,
            "targets_usados": False,
            "data_sha256": hashlib.sha256(PANEL.read_bytes()).hexdigest(),
            "scope": "Medio pre-test; includes original supervised/RL validation months",
        },
    }


def municipality_records(
    profiles: pd.DataFrame, result: dict, names: pd.Series, labels: dict
) -> list:
    records = []
    for position, (code, row) in enumerate(profiles.iterrows()):
        cluster = int(result["labels"][position])
        records.append(
            {
                "divipola": code,
                "municipio": names.loc[code],
                "lat": float(row.centroid_lat),
                "lon": float(row.centroid_lon),
                "cluster": cluster,
                "etiqueta": labels[cluster],
            }
        )
    return records


def write_map(payload: dict) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    frame = pd.DataFrame(payload["municipios"])
    fig, ax = plt.subplots(figsize=(9, 8), constrained_layout=True)
    markers = ["o", "s", "^", "D", "v", "P", "X"]
    for cluster, members in frame.groupby("cluster", sort=True):
        ax.scatter(
            members.lon,
            members.lat,
            marker=markers[int(cluster)],
            s=85,
            c="#222222",
            edgecolors="white",
            linewidths=1.5,
            label=f"Group {cluster}: {len(members)} municipalities",
        )
    santos = frame.loc[frame.municipio.eq("LOS SANTOS")].iloc[0]
    ax.annotate(
        "Los Santos",
        (santos.lon, santos.lat),
        xytext=(20, 22),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "color": "#555555"},
    )
    decorate_map(ax, frame)
    output = ROOT / "docs/figures/medio-clusters.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def decorate_map(ax, frame: pd.DataFrame) -> None:
    ax.set(
        xlabel="Longitude (degrees)",
        ylabel="Latitude (degrees)",
        title=f"Unsupervised municipal profiles | fit through {FIT_UNTIL}",
    )
    ax.set_aspect(1 / np.cos(np.radians(frame.lat.mean())))
    ax.legend(loc="lower left", fontsize=8, frameon=True)
    ax.grid(alpha=0.15)


def write_report(payload: dict) -> None:
    metrics = payload["metricas"]
    santos = next(row for row in payload["municipios"] if row["municipio"] == "LOS SANTOS")
    lines = [
        "# Medio: perfiles territoriales no supervisados",
        "",
        "Reproducir: `uv run python -m ml.medio.run`.",
        "",
        f"HECHO: {len(payload['municipios'])} municipios, {len(payload['metadata']['features'])} variables, ajuste hasta {FIT_UNTIL}; no usa filas 2025-06+ ni targets.",
        f"HECHO: KMeans k={metrics['k']}, silhouette={metrics['silhouette']:.6f}, Davies-Bouldin={metrics['davies_bouldin']:.6f}; k elegido3..7 por silhouette/DB, n_init20, seed7.",
        f"HECHO: estabilidad ARI contra seed7 (7/21/42)={metrics['stability_ari']}.",
        f"HECHO: contraste jerárquico mismo k: silhouette={metrics['agglomerative_silhouette']:.6f}, ARI vsKMeans={metrics['agglomerative_ari']:.6f}.",
        "",
        "| Grupo | Municipios | Perfil relativo (no riesgo oficial) |",
        "|---|---:|---|",
    ]
    lines += [
        f"| {group['cluster']} | {group['n_municipios']} | {group['etiqueta']} |"
        for group in payload["perfiles"]
    ]
    lines += [
        "",
        f"HECHO: Los Santos cae en grupo{santos['cluster']}; tamaño={next(g['n_municipios'] for g in payload['perfiles'] if g['cluster'] == santos['cluster'])}.",
        "INFERENCIA: separación describe heterogeneidad de actividad registrada/exposición/geografía; no demuestra daño ni riesgo ni causalidad.",
        "SUPOSICIÓN: centroides representan municipio para visualización; no ubicaciones de terremotos ni polígonos de área afectada.",
        "Ventana de ajuste Medio incluye validación previa del supervisado/RL, NO es train original de esos modelos. Métricas internas, no desempeño fuera de muestra.",
        "Promedios de descriptores sísmicos sobre meses con eventos; máximo histórico de mag_max_mes; frecuencias sobre todos los meses cubiertos. Estandarización e imputación mediana solo sobre perfiles pre-cutoff.",
        "DANE: proyección retrospectiva CNPV2018, no población observada ni disponibilidad as-of demostrada. Escalas magnitud no homogenizadas; más registros puede reflejar instrumentación.",
        "Variables constantes/indefinidas se imputan, no garantizan relevancia; centroides/población pueden dominar grupos. Labels arbitrarios: no ordenar grupos como bajo/medio/alto.",
        "Mapa monocromo con símbolos distintos/leyenda y tabla JSON: identificación no depende de colores; los grupos pequeños/singletons se reportan sin ocultarlos.",
        "JSON: `app/web/public/data/clusters.json`; mapa: `docs/figures/medio-clusters.png`; modelo propio: `ml/medio/kmeans.joblib`.",
        "Fuentes: panel SGC+DANE y diccionario `docs/data/diccionario.md`; metadata JSON conserva SHA256. API scikit-learn verificada por Context7.",
    ]
    path = ROOT / "docs/research/16-medio-clusters.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    panel = pd.read_csv(PANEL, dtype={"divipola": str})
    profiles = aggregate_profiles(panel)
    if len(profiles) != 87:
        raise ValueError(f"Expected 87 municipalities, got {len(profiles)}")
    result = fit_clusters(profiles)
    payload = make_payload(panel, profiles, result)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    joblib.dump(
        {
            "model": result["model"],
            "imputer": result["imputer"],
            "scaler": result["scaler"],
            "features": profiles.columns.tolist(),
        },
        ROOT / "ml/medio/kmeans.joblib",
    )
    profiles.to_csv(ROOT / "ml/medio/profiles.csv")
    write_map(payload)
    write_report(payload)
    print(json.dumps(payload["metricas"], indent=2))
    print(f"JSON: {OUTPUT}; municipalities={len(profiles)}")


if __name__ == "__main__":
    main()
