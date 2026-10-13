"""Panel loading, schema validation and temporal splits.

Contract: ``data/panel/metadata.json`` lists the allowed features and
``docs/data/diccionario.md`` documents them. The supervised target is
``target_clase_mes_siguiente`` (bajo/medio/alto of the next month).
The binary ``target_actividad_m3_mes_siguiente`` is a different
objective (RL reward) and must never enter X.
"""

import hashlib
import json
from pathlib import Path

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
PANEL_PATH = ROOT / "data" / "panel" / "panel_municipio_mes.csv.gz"
METADATA_PATH = ROOT / "data" / "panel" / "metadata.json"

TARGET_COL = "target_clase_mes_siguiente"
ACTIVITY_COL = "target_actividad_m3_mes_siguiente"
COUNT_TARGET_COL = "target_n_eventos_mes_siguiente"
TARGET_MONTH_COL = "target_month"
CLASS_LABELS = ["bajo", "medio", "alto"]
CLASS_TO_INT = {label: i for i, label in enumerate(CLASS_LABELS)}

FUTURE_COLS = {TARGET_COL, ACTIVITY_COL, COUNT_TARGET_COL, TARGET_MONTH_COL}
ID_COLS = ["zone_id", "divipola", "municipio", "month", "feature_cutoff"]
META_COLS = ["source_system", "coverage_complete", "history_12m_complete", "eligible"]


def dataset_sha256(path: Path = PANEL_PATH) -> str:
    """Return the SHA-256 hex digest of the panel file."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_metadata(path: Path = METADATA_PATH) -> dict:
    """Load the panel contract (feature list, counts, nulls)."""
    with open(path, encoding="utf-8") as handle:
        metadata = json.load(handle)
    if not metadata.get("features"):
        raise ValueError(f"metadata at {path} lists no features")
    return metadata


def load_panel(path: Path = PANEL_PATH) -> pd.DataFrame:
    """Load the municipal-month panel exactly as published."""
    if not path.exists():
        raise FileNotFoundError(f"panel not found at {path}")
    return pd.read_csv(path, compression="gzip")


def feature_columns(metadata: dict) -> list:
    """Return the contract feature list in its frozen order."""
    features = list(metadata["features"])
    if set(features) & FUTURE_COLS:
        raise ValueError("metadata features must not contain targets")
    return features


def validate_schema(panel: pd.DataFrame, metadata: dict) -> list:
    """Check required columns; return the usable feature list.

    Raises ValueError naming the missing columns.
    """
    features = feature_columns(metadata)
    required = set(features) | set(ID_COLS) | set(META_COLS) | FUTURE_COLS
    missing = sorted(required - set(panel.columns))
    if missing:
        raise ValueError(f"panel is missing columns: {missing}")
    unknown_features = [c for c in features if c not in panel.columns]
    if unknown_features:
        raise ValueError(f"contract features absent from panel: {unknown_features}")
    leaked = [c for c in features if c.startswith("target_")]
    if leaked:
        raise ValueError(f"future columns inside feature list: {leaked}")
    return features


def eligible_labeled_mask(panel: pd.DataFrame) -> pd.Series:
    """Rows usable for supervised learning: eligible and target known."""
    eligible = panel["eligible"].astype(str).str.lower().isin(["true", "1"])
    labeled = panel[TARGET_COL].isin(CLASS_LABELS)
    return eligible & labeled


def build_supervised_frame(panel: pd.DataFrame, metadata: dict) -> tuple:
    """Filter usable rows; return X, y, index and feature names.

    Rows with missing features are kept (imputation is decided later
    and fitted on train only). Rows without a usable future target or
    failing the eligibility flags are discarded.
    """
    features = validate_schema(panel, metadata)
    mask = eligible_labeled_mask(panel)
    usable = panel.loc[mask].copy()
    if usable.empty:
        raise ValueError("no eligible labeled rows in panel")
    x = usable[features].copy()
    y = usable[TARGET_COL].astype(str).copy()
    index = usable[["zone_id", "month", "feature_cutoff"]].reset_index(drop=True)
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)
    return x, y, index, features


def usable_months(index: pd.DataFrame) -> list:
    """Sorted unique months present in the supervised frame."""
    return sorted(index["month"].unique().tolist())


def temporal_month_splits(months: list, train_frac: float = 0.70, val_frac: float = 0.15) -> dict:
    """Split a sorted month list chronologically; no month is shared."""
    ordered = sorted(months)
    n = len(ordered)
    if n < 3:
        raise ValueError(f"need at least 3 months, got {n}")
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    n_train = max(1, n_train)
    n_val = max(1, n_val)
    if n_train + n_val >= n:
        n_val = max(1, n - n_train - 1)
    splits = {
        "train": ordered[:n_train],
        "val": ordered[n_train : n_train + n_val],
        "test": ordered[n_train + n_val :],
    }
    if not splits["test"]:
        raise ValueError("empty test split; check fractions and month count")
    return splits


def split_masks(index: pd.DataFrame, splits: dict) -> dict:
    """Boolean masks per split aligned with the supervised frame."""
    return {name: index["month"].isin(months) for name, months in splits.items()}


def make_preprocessor() -> Pipeline:
    """Median imputation plus standardization (fit on train only)."""
    return Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])


def feature_type_groups(x: pd.DataFrame) -> dict:
    """Group feature names by dtype for the SMOTE feasibility check."""
    groups: dict = {"numeric": [], "boolean_like": [], "categorical": []}
    for column in x.columns:
        series = x[column]
        if series.dtype == object or str(series.dtype) == "category":
            groups["categorical"].append(column)
        elif series.dropna().nunique() <= 2:
            groups["boolean_like"].append(column)
        else:
            groups["numeric"].append(column)
    return groups
