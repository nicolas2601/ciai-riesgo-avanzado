"""Critical analysis of the supervised benchmark (answers 8 questions).

Run from the repository root after the benchmark::

    uv run python -m ml.src.analyze

Reads ``artifacts/ml/metrics.json`` and writes
``artifacts/ml/critical_analysis.md``. No new training happens here.
"""

import argparse
import json
from pathlib import Path

ARTIFACT_DIR = Path("artifacts") / "ml"


def _fmt(value) -> str:
    return "no medido" if value is None else str(value)


def _delta_text(winner: float, dummy: float) -> str:
    return f"{winner - dummy:+.4f}"


def _para(*parts: str) -> str:
    """Join message parts without implicit string concatenation."""
    return "".join(parts)


def build_analysis(summary: dict) -> str:
    """Answer the eight required questions with measured numbers."""
    val = summary["validation"]
    test = summary["test"]
    winner = summary["selection"]["winner"]
    dummy = val["A_dummy_majority"]["metrics"]
    best_val = val[winner]["metrics"]
    best_test = test["metrics"]
    dummy_test = test.get("dummy_reference")
    smote = val.get("D_smote_logreg", {})
    lines = ["# Análisis crítico del benchmark supervisado", ""]
    lines.append(
        _para(
            f"Modelo seleccionado en validación: **{winner}** ",
            f"(macro-F1 val {best_val['macro_f1']}). ",
            "Test confirma una sola vez, sin re-selección.",
        )
    )
    lines += [
        "",
        "## 1. Baseline sin aprendizaje",
        _para(
            f"A_dummy_majority en validación: macro-F1 {dummy['macro_f1']}, ",
            f"balanced accuracy {dummy['balanced_accuracy']}, ",
            f"accuracy {dummy['accuracy']}. Predice siempre la clase baja; ",
            "su accuracy alta solo refleja el desbalance.",
        ),
    ]
    lines += ["", "## 2. Mejora del modelo ponderado"]
    b_model = val["B_logreg_balanced"]
    if b_model["status"] == "evaluated":
        b = b_model["metrics"]
        lines.append(
            _para(
                f"B_logreg_balanced en validación: macro-F1 {b['macro_f1']} ",
                f"(delta {_delta_text(b['macro_f1'], dummy['macro_f1'])} vs dummy).",
            )
        )
    else:
        lines.append("B_logreg_balanced no evaluado; sin mejora medible.")
    if smote.get("status") == "evaluated":
        s = smote["metrics"]
        b = val["B_logreg_balanced"]["metrics"]
        verdict = (
            "SMOTE NO mejora; se reporta como resultado negativo."
            if s["macro_f1"] < b["macro_f1"]
            else "SMOTE mejora en validación; falta confirmar en test."
        )
        lines += [
            "",
            "## 3. SMOTE en validación",
            _para(
                f"D_smote_logreg: macro-F1 {s['macro_f1']} ",
                f"(B: {b['macro_f1']}, ",
                f"delta {_delta_text(s['macro_f1'], b['macro_f1'])}), ",
                f"balanced accuracy {s['balanced_accuracy']} ",
                f"(B: {b['balanced_accuracy']}). ",
                verdict,
            ),
        ]
    else:
        lines += [
            "",
            "## 3. SMOTE en validación",
            _para(
                f"D_smote_logreg omitido: {smote.get('reason', 'sin información')}. ",
                "No se fuerza el experimento; ",
                "el benchmark compara ponderación de clases.",
            ),
        ]
    for label in ("medio", "alto"):
        w = best_val["per_class"][label]
        d = dummy["per_class"][label]
        lines += [
            "",
            f"## 4. Clase {label} (precisión/recall)",
            _para(
                f"Validación {winner}: precisión {w['precision']}, ",
                f"recall {w['recall']}, ",
                f"F1 {w['f1']}, soporte {w['support']}. ",
                f"Dummy: precisión {d['precision']}, recall {d['recall']}, ",
                f"F1 {d['f1']}, soporte {d['support']}.",
            ),
        ]
    lines += [
        "",
        "## 5. Sobreajuste y degradación temporal",
        _para(
            f"{winner} val macro-F1 {best_val['macro_f1']} ",
            f"vs test {best_test['macro_f1']} ",
            f"(delta {_delta_text(best_test['macro_f1'], best_val['macro_f1'])}). ",
            "Sin métricas de entrenamiento no se afirma sobreajuste clásico; ",
            "la comparación val->test mide degradación temporal.",
        ),
    ]
    for label in ("medio", "alto"):
        wv = best_val["per_class"][label]
        wt = best_test["per_class"][label]
        lines += [
            (
                f"- {label}: recall val {wv['recall']} "
                f"(n={wv['support']}) vs "
                f"test {wt['recall']} (n={wt['support']})."
            )
        ]
    lines += [
        "",
        "## 6. Estabilidad de la clase alta",
        _para(
            f"Soportes: val {best_val['per_class']['alto']['support']}, ",
            f"test {best_test['per_class']['alto']['support']}. ",
            "Con decenas de ejemplos, cada acierto/error mueve el recall en puntos; ",
            "las métricas de clase alta son orientativas, no estables.",
        ),
    ]
    if dummy_test is not None:
        lines += [
            "",
            "## 7. La mejora se mantiene en test",
            _para(
                f"{winner} test macro-F1 {best_test['macro_f1']} vs ",
                f"dummy test {dummy_test['macro_f1']} ",
                f"(delta {_delta_text(best_test['macro_f1'], dummy_test['macro_f1'])}).",
            ),
        ]
    else:
        lines += [
            "",
            "## 7. La mejora se mantiene en test",
            "Sin referencia dummy en test; comparar val->test del ganador.",
        ]
    lines += [
        "",
        "## 8. Límites para uso operativo",
        _para(
            "- El modelo clasifica actividad municipal del mes siguiente; ",
            "NO predice cuándo ocurrirá un terremoto.",
        ),
        _para(
            "- No estima daños, ni produce probabilidades oficiales de amenaza, ",
            "ni demuestra reducción de pérdidas.",
        ),
        "- El catálogo SGC es retrospectivo/revisado: backtest, no operación as-of.",
        "- La población DANE es proyección retrospectiva CNPV2018.",
        _para(
            "- La clase alta tiene soporte mínimo; ",
            "cualquier despliegue requeriría ",
            "validación, incertidumbre y revisión de Zabdiel.",
        ),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """CLI entry point for the critical analysis."""
    parser = argparse.ArgumentParser(description="Write the critical analysis")
    parser.add_argument("--out-dir", type=Path, default=ARTIFACT_DIR)
    args = parser.parse_args()
    summary = json.loads((args.out_dir / "metrics.json").read_text(encoding="utf-8"))
    (args.out_dir / "critical_analysis.md").write_text(build_analysis(summary), encoding="utf-8")
    print(f"analysis: {args.out_dir / 'critical_analysis.md'}")


if __name__ == "__main__":
    main()
