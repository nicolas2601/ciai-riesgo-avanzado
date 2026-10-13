"""Tests for metrics and candidate models (no external downloads)."""

import pandas as pd

from ml.src.data import CLASS_LABELS
from ml.src.evaluate import compute_metrics, render_comparison_table
from ml.src.supervised import _smote_feasibility, candidate_models


def _toy():
    y_true = ["bajo", "bajo", "medio", "alto", "alto", "bajo"]
    y_pred = ["bajo", "medio", "medio", "alto", "bajo", "bajo"]
    return y_true, y_pred


def test_compute_metrics_reports_all_classes():
    y_true, y_pred = _toy()
    metrics = compute_metrics(y_true, y_pred)
    assert set(metrics) >= {
        "macro_f1",
        "balanced_accuracy",
        "accuracy",
        "per_class",
        "confusion_matrix",
        "high_class_ovr",
    }
    assert set(metrics["per_class"]) == set(CLASS_LABELS)
    assert metrics["confusion_matrix"]["labels"] == CLASS_LABELS
    assert len(metrics["confusion_matrix"]["matrix"]) == 3
    assert metrics["high_class_ovr"]["roc_auc"] is None


def test_compute_metrics_marks_absent_high_class():
    metrics = compute_metrics(["bajo", "bajo", "medio"], ["bajo", "bajo", "bajo"])
    assert metrics["per_class"]["alto"]["support"] == 0
    assert metrics["per_class"]["alto"]["f1"] == 0


def test_candidate_models_cover_all_five_slots():
    x = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "b": [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]})
    y = pd.Series(["bajo", "bajo", "bajo", "medio", "alto", "bajo"])
    candidates = candidate_models(x, y)
    assert [c[0] for c in candidates] == [
        "A_dummy_majority",
        "B_logreg_balanced",
        "C_ros_logreg",
        "D_smote_logreg",
        "E_rf_balanced",
    ]
    assert candidates[0][1] is not None
    assert candidates[1][1] is not None
    assert candidates[4][1] is not None


def test_smote_refuses_singleton_minority():
    x = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    y = pd.Series(["bajo", "bajo", "bajo", "alto"])
    feasible, reason = _smote_feasibility(x, y)
    assert not feasible
    assert "1" in reason or "SMOTE" in reason


def test_comparison_table_marks_skips():
    rows = [
        {
            "model": "A",
            "status": "evaluated",
            "metrics": {"macro_f1": 0.3, "balanced_accuracy": 0.4, "accuracy": 0.9},
        },
        {"model": "C", "status": "skipped", "reason": "no imblearn"},
    ]
    table = render_comparison_table(rows)
    assert "skipped: no imblearn" in table
    assert "0.3" in table
