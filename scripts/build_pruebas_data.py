"""Build app/web/public/data/pruebas.json from real repository artifacts.

No value is recomputed: everything is parsed from existing files.
"""
import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ML = ROOT / "artifacts" / "ml"
RL = ML / "rl_research"
OUT = ROOT / "app" / "web" / "public" / "data" / "pruebas.json"


def supervisado() -> dict:
    text = (ML / "benchmark_val.md").read_text()
    modelos = []
    for line in text.splitlines():
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) == 5 and re.match(r"^[A-E]_", cols[0]):
            modelos.append({"modelo": cols[0], "macro_f1": float(cols[1]),
                            "balanced_accuracy": float(cols[2]), "accuracy": float(cols[3])})
    sel = re.search(r"\*\*(\w+)\*\*", text).group(1)
    parts = json.loads((ML / "partitions.json").read_text())
    return {"modelos": modelos, "seleccionado": sel, "baseline_mayoritario": "A_dummy_majority",
            "particiones": parts}


def medio() -> dict:
    d = json.loads((ROOT / "app/web/public/data/clusters.json").read_text())
    m = d["metricas"]
    return {"k": m["k"], "silhouette": m["silhouette"], "davies_bouldin": m["davies_bouldin"],
            "ari_por_semilla": m["stability_ari"],
            "tamanos": [{"grupo": p["cluster"], "n_municipios": p["n_municipios"]} for p in d["perfiles"]]}


def rl() -> dict:
    filas = []
    with open(RL / "comparison_val.csv", newline="") as f:
        for r in csv.DictReader(f):
            std = r["val_seed_std"]
            filas.append({"politica": r["policy"], "val_media": float(r["val_mean_seeds"]),
                          "val_desv": float(std) if std else None,
                          "conjuntos_distintos": r["distinct_sets"]})
    s = json.loads((RL / "research_summary.json").read_text())
    return {"validacion": filas, "ganador": s["winner"], "test": s["test"],
            "test_caveat": s["test_caveat"], "presupuesto_k": s["budget_k"],
            "monitores": sorted(p.name for p in RL.glob("monitor_*.csv"))}


def count(last: str, key: str) -> int:
    m = re.search(rf"(\d+) {key}", last)
    return int(m.group(1)) if m else 0


def pruebas() -> dict:
    try:
        p = subprocess.run(["uv", "run", "--group", "reto", "pytest", "ml", "-q"], cwd=ROOT,
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {"estado": "no ejecutado", "motivo": "excedio 120 s"}
    lines = p.stdout.strip().splitlines()
    last = lines[-1] if lines else ""
    return {"estado": "ejecutado", "pasan": count(last, "passed"),
            "fallan": count(last, "failed"), "resumen": last}


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = {"supervisado": supervisado(), "medio": medio(), "rl": rl(), "pruebas": pruebas()}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"wrote {OUT}")
