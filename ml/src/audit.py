"""Reproducible audit of the published municipal-month panel.

Run from the repository root::

    uv run python -m ml.src.audit

Writes ``artifacts/ml/audit_report.md`` and ``artifacts/ml/audit.json``.
Exit code is 0; findings are reported, never forced to match expectations.
"""

import argparse
import json
from pathlib import Path

import pandas as pd

from ml.src.data import (
    ACTIVITY_COL,
    CLASS_LABELS,
    FUTURE_COLS,
    ID_COLS,
    META_COLS,
    PANEL_PATH,
    TARGET_COL,
    build_supervised_frame,
    dataset_sha256,
    eligible_labeled_mask,
    feature_type_groups,
    load_metadata,
    load_panel,
    temporal_month_splits,
    usable_months,
    validate_schema,
)

ARTIFACT_DIR = Path("artifacts") / "ml"


def null_table(panel: pd.DataFrame) -> dict:
    """Count nulls per column, keeping only columns with nulls."""
    nulls = panel.isna().sum()
    return {col: int(count) for col, count in nulls.items() if count}


def target_by_month(panel: pd.DataFrame) -> dict:
    """Class frequencies per month (null targets grouped as 'sin_target')."""
    counts = (
        panel.assign(_target=panel[TARGET_COL].fillna("sin_target"))
        .groupby(["month", "_target"])
        .size()
        .unstack(fill_value=0)
    )
    return counts.astype(int).to_dict(orient="index")


def split_class_support(y: pd.Series, index: pd.DataFrame, splits: dict) -> dict:
    """Class counts inside each temporal split."""
    support = {}
    for name, months in splits.items():
        mask = index["month"].isin(months)
        counts = y[mask].value_counts()
        support[name] = {
            "months": [months[0], months[-1]],
            "n_months": len(months),
            "n_rows": int(mask.sum()),
            "classes": {label: int(counts.get(label, 0)) for label in CLASS_LABELS},
        }
    return support


def constant_columns(panel: pd.DataFrame, features: list) -> list:
    """Features with a single non-null value (unusable as signal)."""
    return [c for c in features if panel[c].dropna().nunique() <= 1]


def infinite_columns(panel: pd.DataFrame, features: list) -> list:
    """Numeric features containing +inf or -inf."""
    bad = []
    for column in features:
        series = pd.to_numeric(panel[column], errors="coerce")
        if bool((series == float("inf")).any() or (series == float("-inf")).any()):
            bad.append(column)
    return bad


def text_date_columns(panel: pd.DataFrame, features: list) -> dict:
    """Features with object dtype (text/dates that need encoding)."""
    return {c: str(panel[c].dtype) for c in features if panel[c].dtype == object}


def run_audit(out_dir: Path = ARTIFACT_DIR) -> dict:
    """Inspect the real panel and persist a readable report."""
    panel = load_panel(PANEL_PATH)
    metadata = load_metadata()
    features = validate_schema(panel, metadata)
    x, y, index, _ = build_supervised_frame(panel, metadata)
    months = usable_months(index)
    splits = temporal_month_splits(months)

    labeled = panel[TARGET_COL].isin(CLASS_LABELS)
    summary = {
        "panel_path": str(PANEL_PATH),
        "sha256": dataset_sha256(PANEL_PATH),
        "rows": len(panel),
        "columns": len(panel.columns),
        "municipalities": int(panel["zone_id"].nunique()),
        "months_total": int(panel["month"].nunique()),
        "month_min": str(panel["month"].min()),
        "month_max": str(panel["month"].max()),
        "dtypes": {c: str(t) for c, t in panel.dtypes.items()},
        "duplicate_zone_month": int(panel.duplicated(["zone_id", "month"]).sum()),
        "nulls": null_table(panel),
        "target_counts_all": {
            k: int(v)
            for k, v in panel[TARGET_COL].value_counts(dropna=False).items()
            if str(k) != "nan"
        },
        "target_null_rows": int((~labeled).sum()),
        "eligible_rows": int(panel["eligible"].astype(str).str.lower().isin(["true", "1"]).sum()),
        "eligible_labeled_rows": int(eligible_labeled_mask(panel).sum()),
        "low_fraction_labeled": round(
            float((panel[TARGET_COL] == "bajo").sum() / max(1, int(labeled.sum()))), 4
        ),
        "activity_positives": int((panel[ACTIVITY_COL] == 1).sum()),
        "features_in_contract": len(features),
        "constant_features": constant_columns(panel, features),
        "infinite_features": infinite_columns(panel, features),
        "object_features": text_date_columns(panel, features),
        "feature_types": feature_type_groups(x),
        "future_cols_in_x": sorted(set(x.columns) & FUTURE_COLS),
        "id_or_meta_in_x": sorted(set(x.columns) & (set(ID_COLS) | set(META_COLS))),
        "target_by_month": target_by_month(panel),
        "usable_months": months,
        "splits": split_class_support(y, index, splits),
        "contract_notes": {
            "poblacion": "DANE CNPV2018 retrospective projection; not as-of availability",
            "catalog": "retrospective/revised SGC catalog; backtest, not as-of operation",
            "year_context": "cutoff year kept per contract; may memorize time trends",
        },
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "audit.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "audit_report.md").write_text(render_report(summary), encoding="utf-8")
    return summary


def _para(*parts: str) -> str:
    """Join message parts without implicit string concatenation."""
    return "".join(parts)


def render_report(summary: dict) -> str:
    """Build the human-readable markdown audit report."""
    lines = [
        "# Auditoría del panel municipal",
        "",
        f"Panel: `{summary['panel_path']}`",
        f"SHA-256: `{summary['sha256']}`",
        f"Filas: {summary['rows']}, columnas: {summary['columns']}.",
        _para(
            f"Municipios: {summary['municipalities']}; ",
            f"meses: {summary['months_total']} ",
            f"({summary['month_min']} a {summary['month_max']}).",
        ),
        f"Duplicados (zona, mes): {summary['duplicate_zone_month']}.",
        "",
        "## Target",
        _para(
            f"Conteos: {summary['target_counts_all']}; ",
            f"sin target: {summary['target_null_rows']}.",
        ),
        _para(
            f"Elegibles: {summary['eligible_rows']}; ",
            f"elegibles con etiqueta: {summary['eligible_labeled_rows']}.",
        ),
        f"Fracción baja entre etiquetadas: {summary['low_fraction_labeled']}.",
        f"Actividad M>=3 positiva: {summary['activity_positives']} filas.",
        "",
        "## Features",
        _para(
            f"En contrato: {summary['features_in_contract']}; ",
            f"constantes: {summary['constant_features'] or 'ninguna'}.",
        ),
        f"Con infinitos: {summary['infinite_features'] or 'ninguna'}.",
        f"Tipo objeto: {summary['object_features'] or 'ninguna'}.",
        f"Columnas de futuro en X: {summary['future_cols_in_x'] or 'ninguna'}.",
        f"IDs o meta en X: {summary['id_or_meta_in_x'] or 'ninguna'}.",
        "",
        "## Particiones temporales",
    ]
    for name, info in summary["splits"].items():
        lines.append(
            _para(
                f"- {name}: {info['n_months']} meses ",
                f"({info['months'][0]} a {info['months'][1]}), ",
                f"{info['n_rows']} filas, clases {info['classes']}.",
            )
        )
    lines += ["", "## Nulos por columna", ""]
    for column, count in sorted(summary["nulls"].items()):
        lines.append(f"- {column}: {count}")
    lines += ["", "## Notas de contrato", ""]
    for key, note in summary["contract_notes"].items():
        lines.append(f"- {key}: {note}.")
    return "\n".join(lines) + "\n"


def main() -> None:
    """CLI entry point for the audit."""
    parser = argparse.ArgumentParser(description="Audit the seismic panel")
    parser.add_argument("--out-dir", type=Path, default=ARTIFACT_DIR)
    args = parser.parse_args()
    summary = run_audit(args.out_dir)
    print(
        _para(
            f"rows={summary['rows']} cols={summary['columns']} ",
            f"mun={summary['municipalities']} months={summary['months_total']}",
        )
    )
    print(f"report: {args.out_dir / 'audit_report.md'}")


if __name__ == "__main__":
    main()
