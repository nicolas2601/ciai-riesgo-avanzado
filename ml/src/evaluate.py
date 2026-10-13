"""Evaluation metrics for the imbalanced supervised benchmark."""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    roc_auc_score,
)

from ml.src.data import CLASS_LABELS

HIGH_CLASS = "alto"


def compute_metrics(y_true, y_pred, y_proba=None) -> dict:
    """Macro-F1, balanced accuracy, per-class scores and confusion matrix.

    Missing classes keep support 0 with zero_division=0; they are
    reported, never hidden. High-class OvR AUC is added only when the
    split contains both positive and negative examples.
    """
    y_true = list(y_true)
    y_pred = list(y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=CLASS_LABELS, zero_division=0
    )
    per_class = {
        label: {
            "precision": round(float(precision[i]), 4),
            "recall": round(float(recall[i]), 4),
            "f1": round(float(f1[i]), 4),
            "support": int(support[i]),
        }
        for i, label in enumerate(CLASS_LABELS)
    }
    matrix = confusion_matrix(y_true, y_pred, labels=CLASS_LABELS).tolist()
    metrics = {
        "macro_f1": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "balanced_accuracy": round(float(balanced_accuracy_score(y_true, y_pred)), 4),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "per_class": per_class,
        "confusion_matrix": {"labels": list(CLASS_LABELS), "matrix": matrix},
        "high_class_ovr": {"label": HIGH_CLASS, "roc_auc": None, "note": ""},
    }
    if y_proba is not None:
        try:
            order = list(getattr(y_proba, "columns", CLASS_LABELS))
        except AttributeError:
            order = list(CLASS_LABELS)
        binary = [1 if v == HIGH_CLASS else 0 for v in y_true]
        if len(set(binary)) == 2 and HIGH_CLASS in order:
            scores = np.asarray(y_proba)[:, order.index(HIGH_CLASS)]
            metrics["high_class_ovr"]["roc_auc"] = round(float(roc_auc_score(binary, scores)), 4)
            metrics["high_class_ovr"]["note"] = "P(alto) vs rest"
        else:
            metrics["high_class_ovr"]["note"] = (
                "AUC unavailable: high class absent from y_true or proba"
            )
    else:
        metrics["high_class_ovr"]["note"] = "no predicted probabilities"
    return metrics


def render_comparison_table(rows: list) -> str:
    """Markdown table comparing models on one split."""
    header = ("| model | macro-F1 | bal_acc | accuracy | status |", "|---|---|---|---|---|")
    lines = list(header)
    for row in rows:
        if row["status"] == "skipped":
            lines.append(f"| {row['model']} | - | - | - | skipped: {row['reason']} |")
        else:
            m = row["metrics"]
            lines.append(
                f"| {row['model']} | {m['macro_f1']} | "
                f"{m['balanced_accuracy']} | {m['accuracy']} | evaluated |"
            )
    return "\n".join(lines) + "\n"
