"""Deterministic synthetic predictions so the web can be built before the model exists."""

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

from app.api.schemas import (
    Conformal,
    Explanation,
    Factor,
    HistoryPoint,
    Metric,
    Metrics,
    Prediction,
    Ready,
    Snapshot,
)

MODEL_VERSION = "mock"
DATA_VERSION = "mock-data"
SUPPORTED_HAZARDS = ("wildfire", "landslide", "flood")
DATA_AVAILABLE_THROUGH = date(2026, 9, 30)
ALPHA = 0.1
HISTORY_MONTHS = 6
LEVELS = ("low", "medium", "high")
FEATURES = ("rainfall_30d", "soil_moisture", "oni", "prior_events_12m")

_DATA = Path(__file__).parent / "data" / "municipios_santander.json"
MUNICIPALITIES = {m["zone_id"]: m for m in json.loads(_DATA.read_text(encoding="utf-8"))}


def _unit(*parts: str) -> float:
    digest = hashlib.sha256("|".join(parts).encode()).digest()
    return int.from_bytes(digest[:4], "big") / 2**32


def _shift_month(month: str, delta: int) -> str:
    total = int(month[:4]) * 12 + int(month[5:]) - 1 + delta
    return f"{total // 12}-{total % 12 + 1:02d}"


def default_target_month() -> str:
    return _shift_month(DATA_AVAILABLE_THROUGH.strftime("%Y-%m"), 1)


def feature_cutoff(target_month: str) -> date:
    return date(int(target_month[:4]), int(target_month[5:]), 1) - timedelta(days=1)


def snapshot(hazard: str, target_month: str | None) -> Snapshot:
    month = target_month or default_target_month()
    return Snapshot(
        model_version=MODEL_VERSION,
        data_version=DATA_VERSION,
        hazard=hazard,
        target_month=month,
        feature_cutoff=feature_cutoff(month),
        is_mock=True,
    )


def is_stale(snap: Snapshot) -> bool:
    return snap.feature_cutoff > DATA_AVAILABLE_THROUGH


def ready() -> Ready:
    snap = snapshot("wildfire", None)
    return Ready(
        ready=True,
        is_mock=True,
        model_version=MODEL_VERSION,
        data_version=DATA_VERSION,
        supported_hazards=list(SUPPORTED_HAZARDS),
        target_month=snap.target_month,
        feature_cutoff=snap.feature_cutoff,
        data_available_through=DATA_AVAILABLE_THROUGH,
    )


def class_probabilities(zone_id: str, hazard: str, month: str) -> dict[str, float]:
    weights = [(0.15 + _unit(zone_id, hazard, month, level)) ** 2 for level in LEVELS]
    probs = [round(w / sum(weights), 3) for w in weights]
    probs[-1] = round(1 - sum(probs[:-1]), 3)
    return dict(zip(LEVELS, probs, strict=True))


def prediction_set(probs: dict[str, float]) -> list[str]:
    chosen, total = [], 0.0
    for level, p in sorted(probs.items(), key=lambda kv: -kv[1]):
        chosen.append(level)
        total += p
        if total >= 1 - ALPHA:
            break
    return chosen


def _factors(zone_id: str, hazard: str, month: str) -> list[Factor]:
    return [
        Factor(
            feature=name,
            shap=round(_unit(zone_id, hazard, month, name) * 0.4 - 0.1, 3),
            value=round(_unit(name, zone_id) * 300, 1),
        )
        for name in FEATURES
    ]


def predict(zone_id: str, hazard: str, target_month: str | None) -> Prediction:
    snap = snapshot(hazard, target_month)
    base = {
        **snap.model_dump(),
        "zone_id": zone_id,
        "municipality": MUNICIPALITIES[zone_id]["municipality"],
        "conformal_alpha": ALPHA,
        "top_factors": _factors(zone_id, hazard, snap.target_month),
    }
    if is_stale(snap):
        return Prediction(
            **base,
            abstain=True,
            abstain_reason="stale_data",
            class_probabilities=None,
            risk_level=None,
            risk_score=None,
            prediction_set=[],
        )
    probs = class_probabilities(zone_id, hazard, snap.target_month)
    chosen = prediction_set(probs)
    wide = len(chosen) == len(LEVELS)
    return Prediction(
        **base,
        abstain=wide,
        abstain_reason="wide_set" if wide else None,
        class_probabilities=probs,
        risk_level=max(probs, key=probs.get),
        risk_score=probs["high"],
        prediction_set=chosen,
    )


def explain(zone_id: str, hazard: str, target_month: str | None) -> Explanation:
    snap = snapshot(hazard, target_month)
    history = [
        HistoryPoint(
            month=_shift_month(snap.target_month, -back),
            risk_score=class_probabilities(zone_id, hazard, _shift_month(snap.target_month, -back))[
                "high"
            ],
        )
        for back in range(HISTORY_MONTHS, 0, -1)
    ]
    return Explanation(
        **snap.model_dump(),
        zone_id=zone_id,
        history=history,
        top_factors=_factors(zone_id, hazard, snap.target_month),
    )


def metrics(hazard: str) -> Metrics:
    names = ("pr_auc", "macro_f1")
    return Metrics(
        **snapshot(hazard, None).model_dump(),
        validation="spatial_block_cv",
        metrics=[Metric(name=n) for n in names],
        baseline=[Metric(name=n) for n in names],
        calibration={"ece": None},
        conformal=Conformal(alpha=ALPHA),
    )
