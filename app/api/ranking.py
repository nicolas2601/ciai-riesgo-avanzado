"""Read-only catalog: territorial panel, baselines and the supervised classifier.

No HTTP here. The service layer maps the exceptions below to error responses.
"""

import hashlib
import json
import logging
import random
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

CLASSES = ("bajo", "medio", "alto")
EXTRA_COLUMNS = ("target_clase_mes_siguiente", "target_actividad_m3_mes_siguiente")
NON_FEATURE = {
    "zone_id",
    "divipola",
    "municipio",
    "month",
    "feature_cutoff",
    "source_system",
    "coverage_complete",
    "history_12m_complete",
    "eligible",
    "target_month",
    *EXTRA_COLUMNS,
}


class MonthNotFound(LookupError):
    """The requested month is not in the panel."""


class ZoneNotFound(LookupError):
    """The zone code has no row for the requested month."""


class ModelNotLoaded(RuntimeError):
    """The supervised model is missing or failed to load."""


def normalize_name(name: str) -> str:
    stripped = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return " ".join(stripped.upper().split())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class Catalog:
    municipios: list[dict[str, Any]]
    panel: pd.DataFrame
    model: Any | None = None
    model_error: str | None = None
    months: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, panel_path: Path, municipios_path: Path, model_path: Path) -> "Catalog":
        panel = pd.read_csv(panel_path, compression="infer", dtype={"zone_id": str})
        panel = panel.sort_values(["zone_id", "month"], kind="stable")
        panel["clase_observada"] = panel.groupby("zone_id")["target_clase_mes_siguiente"].shift(1)
        municipios = json.loads(municipios_path.read_text(encoding="utf-8"))
        model, model_error = _load_model(model_path)
        if model is not None:
            _check_features(model, panel)
        return cls(
            municipios=municipios,
            panel=panel,
            model=model,
            model_error=model_error,
            months=sorted(panel["month"].unique().tolist()),
        )

    @property
    def model_loaded(self) -> bool:
        return self.model is not None

    def zone_by_name(self, name: str) -> str | None:
        key = normalize_name(name)
        return next(
            (z["zone_id"] for z in self.municipios if normalize_name(z["municipality"]) == key),
            None,
        )

    def municipios_with_population(self, month: str) -> list[dict[str, Any]]:
        pop = self._rows_for(month).set_index("zone_id")["poblacion"]
        return [
            {
                "divipola": z["zone_id"],
                "nombre": z["municipality"],
                "lat": z["lat"],
                "lon": z["lon"],
                "poblacion": _int_or_none(pop.get(z["zone_id"])),
            }
            for z in self.municipios
        ]

    def panel_rows(self, month: str) -> list[dict[str, Any]]:
        rows = self._rows_for(month)
        features = [
            c
            for c in rows.columns
            if c not in NON_FEATURE
            and c != "clase_observada"
            and pd.api.types.is_numeric_dtype(rows[c])
        ]
        return [
            {
                "divipola": r["zone_id"],
                "nombre": r["municipio"],
                "features": {c: _float_or_none(r[c]) for c in features},
                "clase_observada": _str_or_none(r["clase_observada"]),
                "target_clase_mes_siguiente": _str_or_none(r["target_clase_mes_siguiente"]),
                "target_actividad_m3": _int_or_none(r["target_actividad_m3_mes_siguiente"]),
            }
            for _, r in rows.iterrows()
        ]

    def classify(self, month: str, zone_id: str) -> dict[str, Any]:
        self._require_model()
        row = self._rows_for(month)
        row = row[row["zone_id"] == zone_id]
        if row.empty:
            raise ZoneNotFound(f"{zone_id}@{month}")
        features = list(self.model.feature_names_in_)
        proba = self.model.predict_proba(row[features])[0]
        probs = {c: round(float(p), 4) for c, p in zip(self.model.classes_, proba, strict=True)}
        return {
            "divipola": zone_id,
            "mes": month,
            "clase": max(probs, key=probs.get),
            "probabilidades": {c: probs[c] for c in CLASSES},
        }

    def baseline_ranking(self, month: str, k: int) -> list[dict[str, Any]]:
        rows = self._rows_for(month).sort_values(
            ["n_eventos_3m", "n_eventos_12m", "zone_id"], ascending=[False, False, True]
        )
        return _ranked(rows.head(k))

    def random_ranking(self, month: str, k: int) -> list[dict[str, Any]]:
        rows = self._rows_for(month)
        picked = random.Random(month).sample(range(len(rows)), k=min(k, len(rows)))
        return _ranked(rows.iloc[picked])

    def _require_model(self) -> None:
        if self.model is None:
            raise ModelNotLoaded(self.model_error or "model file not found")

    def _rows_for(self, month: str) -> pd.DataFrame:
        rows = self.panel[self.panel["month"] == month]
        if rows.empty:
            raise MonthNotFound(month)
        return rows


def _ranked(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {"divipola": r["zone_id"], "nombre": r["municipio"], "rank": i}
        for i, (_, r) in enumerate(frame.iterrows(), start=1)
    ]


def _load_model(path: Path) -> tuple[Any | None, str | None]:
    if not path.exists():
        return None, f"model file not found: {path.name}"
    try:
        return joblib.load(path), None
    except Exception as exc:
        log.exception("model failed to load")
        return None, f"model failed to load: {type(exc).__name__}"


def _check_features(model: Any, panel: pd.DataFrame) -> None:
    features = getattr(model, "feature_names_in_", None)
    if features is None:
        raise ValueError("model has no feature_names_in_")
    missing = set(features) - set(panel.columns)
    if missing:
        raise ValueError(f"panel lacks model features: {sorted(missing)}")
    if set(model.classes_) != set(CLASSES):
        raise ValueError(f"unexpected model classes: {list(model.classes_)}")


def _int_or_none(value: Any) -> int | None:
    return None if pd.isna(value) else int(value)


def _float_or_none(value: Any) -> float | None:
    return None if pd.isna(value) else float(value)


def _str_or_none(value: Any) -> str | None:
    return None if value is None or (isinstance(value, float) and np.isnan(value)) else str(value)
