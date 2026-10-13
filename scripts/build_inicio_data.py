"""Build app/web/public/data/inicio.json (home page charts) from the panel data."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "data/panel/catalogo_unificado.csv.gz"
PANEL = ROOT / "data/panel/panel_municipio_mes.csv.gz"
SALIDA = ROOT / "app/web/public/data/inicio.json"


def main() -> None:
    cat = pd.read_csv(CATALOGO, usecols=["datetime_utc", "source_system"])
    cat["anio"] = pd.to_datetime(cat["datetime_utc"], utc=True).dt.year
    por_anio = cat.groupby("anio").size()
    por_sistema = cat.groupby(["anio", "source_system"]).size().unstack(fill_value=0)
    panel = pd.read_csv(PANEL)
    clases = panel["target_clase_mes_siguiente"].value_counts()
    salida = {
        "total_eventos": int(len(cat)),
        "anio_min": int(por_anio.index.min()),
        "anio_max": int(por_anio.index.max()),
        "eventos_por_anio": [
            {
                "anio": int(a),
                "total": int(n),
                **{str(s): int(por_sistema.loc[a, s]) for s in por_sistema.columns},
            }
            for a, n in por_anio.items()
        ],
        "balance_clases": {c: int(clases.get(c, 0)) for c in ("bajo", "medio", "alto")},
        "n_variables_panel": int(panel.shape[1]),
        "n_filas_panel": int(panel.shape[0]),
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1))
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
