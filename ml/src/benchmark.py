"""Bounded supervised benchmark runner (validation selects, test confirms).

Run from the repository root::

    uv run python -m ml.src.benchmark

Artifacts go to ``artifacts/ml/`` and contain only measured results.
"""

import argparse
import json
import time
from pathlib import Path

import joblib
import pandas as pd

from ml.src.data import (
    CLASS_LABELS,
    build_supervised_frame,
    dataset_sha256,
    load_metadata,
    load_panel,
    split_masks,
    temporal_month_splits,
    usable_months,
)
from ml.src.evaluate import compute_metrics, render_comparison_table
from ml.src.supervised import RANDOM_STATE, candidate_models

ARTIFACT_DIR = Path("artifacts") / "ml"
SELECTION_METRIC = "macro_f1"


def _proba_frame(estimator, x, classes) -> pd.DataFrame | None:
    if not hasattr(estimator, "predict_proba"):
        return None
    try:
        proba = estimator.predict_proba(x)
    except Exception:  # noqa: BLE001 - any estimator may lack proba; fallback None
        return None
    order = list(getattr(estimator, "classes_", classes))
    return pd.DataFrame(proba, columns=[f"proba_{c}" for c in order])


def _val_row(result: dict) -> dict:
    row = {
        "model": result["model"],
        "status": result["status"],
        "reason": result.get("reason", ""),
        "note": result.get("note", ""),
    }
    if result["status"] == "evaluated":
        for key in ("macro_f1", "balanced_accuracy", "accuracy"):
            row[key] = result["metrics"][key]
    return row


def _fit_predict(name, estimator, x_train, y_train, x_eval):
    started = time.perf_counter()
    estimator.fit(x_train, y_train)
    train_seconds = time.perf_counter() - started
    started = time.perf_counter()
    pred = estimator.predict(x_eval)
    eval_seconds = time.perf_counter() - started
    proba = _proba_frame(estimator, x_eval, CLASS_LABELS)
    return pred, proba, round(train_seconds, 2), round(eval_seconds, 2)


def run_benchmark(out_dir: Path = ARTIFACT_DIR) -> dict:
    """Train A-E, select on validation, confirm the winner on test."""
    panel = load_panel()
    metadata = load_metadata()
    x, y, index, features = build_supervised_frame(panel, metadata)
    months = usable_months(index)
    splits = temporal_month_splits(months)
    masks = split_masks(index, splits)
    data_hash = dataset_sha256()

    partitions = {}
    for name, months_part in splits.items():
        counts = y[masks[name]].value_counts()
        partitions[name] = {
            "start": months_part[0],
            "end": months_part[-1],
            "n_months": len(months_part),
            "n_rows": int(masks[name].sum()),
            "classes": {label: int(counts.get(label, 0)) for label in CLASS_LABELS},
        }

    x_train, y_train = x[masks["train"]], y[masks["train"]]
    results, frames = [], {}
    for name, estimator, skip_reason, note in candidate_models(x_train, y_train):
        if estimator is None:
            results.append(
                {"model": name, "status": "skipped", "reason": skip_reason, "note": note}
            )
            continue
        pred_val, proba_val, train_s, eval_s = _fit_predict(
            name, estimator, x_train, y_train, x[masks["val"]]
        )
        metrics = compute_metrics(y[masks["val"]], pred_val, proba_val)
        results.append(
            {
                "model": name,
                "status": "evaluated",
                "metrics": metrics,
                "train_seconds": train_s,
                "eval_seconds": eval_s,
                "note": note,
            }
        )
        frames[name] = (pred_val, proba_val)

    evaluated = [r for r in results if r["status"] == "evaluated"]
    if not evaluated:
        raise RuntimeError("no model could be evaluated")
    evaluated.sort(
        key=lambda r: (-r["metrics"][SELECTION_METRIC], -r["metrics"]["balanced_accuracy"])
    )
    winner = evaluated[0]["model"]
    estimators = {n: e for n, e, s, _ in candidate_models(x_train, y_train) if e is not None}
    best = estimators[winner]
    pred_test, proba_test, _, test_s = _fit_predict(
        winner, best, x_train, y_train, x[masks["test"]]
    )
    test_metrics = compute_metrics(y[masks["test"]], pred_test, proba_test)
    test_frames = {winner: (pred_test, proba_test)}
    test_extra = {}
    if winner != "A_dummy_majority" and "A_dummy_majority" in estimators:
        dummy = estimators["A_dummy_majority"]
        pred_d, proba_d, _, _ = _fit_predict(
            "A_dummy_majority", dummy, x_train, y_train, x[masks["test"]]
        )
        test_extra["A_dummy_majority"] = compute_metrics(y[masks["test"]], pred_d, proba_d)
        test_frames["A_dummy_majority"] = (pred_d, proba_d)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "partitions.json").write_text(
        json.dumps(partitions, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    val_rows = [_val_row(r) for r in results]
    pd.DataFrame(val_rows).to_csv(out_dir / "benchmark_val.csv", index=False)
    (out_dir / "benchmark_val.md").write_text(
        "# Benchmark (validation)\n\n"
        + render_comparison_table(results)
        + f"\nSelection: highest val {SELECTION_METRIC} -> **{winner}** "
        "(ties: balanced accuracy, then simpler model).\n",
        encoding="utf-8",
    )
    for name, (pred, proba) in frames.items():
        frame = index[masks["val"]].copy()
        frame["y_true"] = y[masks["val"]].to_numpy()
        frame["y_pred"] = list(pred)
        if proba is not None:
            for col in proba.columns:
                frame[col] = proba[col].to_numpy()
        frame.to_csv(out_dir / f"predictions_val_{name}.csv", index=False)
    for name, (pred, proba) in test_frames.items():
        frame = index[masks["test"]].copy()
        frame["y_true"] = y[masks["test"]].to_numpy()
        frame["y_pred"] = list(pred)
        if proba is not None:
            for col in proba.columns:
                frame[col] = proba[col].to_numpy()
        frame.to_csv(out_dir / f"predictions_test_{name}.csv", index=False)
    summary = {
        "data_sha256": data_hash,
        "panel_rows": len(panel),
        "supervised_rows": len(x),
        "features": features,
        "partitions": partitions,
        "seeds": {"random_state": RANDOM_STATE},
        "selection": {"metric": SELECTION_METRIC, "split": "val", "winner": winner},
        "validation": {r["model"]: r for r in results},
        "test": {
            "model": winner,
            "metrics": test_metrics,
            "eval_seconds": test_s,
            "dummy_reference": test_extra.get("A_dummy_majority"),
        },
        "caveats": [
            "DANE poblacion is a retrospective CNPV2018 projection, not as-of data.",
            "SGC catalog is retrospective/revised; results are a backtest.",
            "Not an operational forecast of earthquakes, damage or official hazard.",
        ],
    }
    (out_dir / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    joblib.dump(best, out_dir / "selected_model.joblib")
    (out_dir / "config.json").write_text(
        json.dumps(
            {
                "random_state": RANDOM_STATE,
                "selection_metric": SELECTION_METRIC,
                "models": [
                    {
                        "model": n,
                        "status": ("skipped" if e is None else "evaluated"),
                        "reason": s,
                        "note": t,
                    }
                    for n, e, s, t in candidate_models(x_train, y_train)
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"winner={winner} "
        f"val_macro_f1={evaluated[0]['metrics']['macro_f1']} "
        f"test_macro_f1={test_metrics['macro_f1']}"
    )
    print(f"artifacts: {out_dir}")
    return summary


def main() -> None:
    """CLI entry point for the benchmark."""
    parser = argparse.ArgumentParser(description="Run the supervised benchmark")
    parser.add_argument("--out-dir", type=Path, default=ARTIFACT_DIR)
    args = parser.parse_args()
    run_benchmark(args.out_dir)


if __name__ == "__main__":
    main()
