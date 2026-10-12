"""Deterministic synthetic predictions so the web can be built before the model exists."""

import hashlib
import json
from datetime import date
from pathlib import Path

from app.api.schemas import Explanation, Factor, HistoryPoint, Interval, Metric, Metrics, Prediction

MODEL_VERSION = "mock"
DATA_VERSION = "mock-data"
COVERAGE = 0.9
HALF_WIDTH = 0.12
ABSTAIN_HALF_WIDTH = 0.3
ABSTAIN_ONE_IN = 12
HISTORY_MONTHS = 6
FEATURES = ("rainfall_30d", "soil_moisture", "oni", "prior_events_12m")

_DATA = Path(__file__).parent / "data" / "municipios_santander.json"
MUNICIPALITIES = {m["zone_id"]: m for m in json.loads(_DATA.read_text(encoding="utf-8"))}


def _digest(*parts: str) -> bytes:
    return hashlib.sha256("|".join(parts).encode()).digest()


def _unit(*parts: str) -> float:
    return int.from_bytes(_digest(*parts)[:4], "big") / 2**32


def level_for(score: float) -> str:
    if score < 1 / 3:
        return "low"
    return "medium" if score < 2 / 3 else "high"


def _month_key(as_of: date) -> str:
    return f"{as_of.year}-{as_of.month:02d}"


def _is_abstain(zone_id: str, hazard: str, month: str) -> bool:
    return _digest(zone_id, hazard, month, "abstain")[0] % ABSTAIN_ONE_IN == 0


def _factors(zone_id: str, hazard: str, month: str) -> list[Factor]:
    return [
        Factor(
            feature=name,
            shap=round(_unit(zone_id, hazard, month, name) * 0.4 - 0.1, 3),
            value=round(_unit(name, zone_id) * 300, 1),
        )
        for name in FEATURES
    ]


def _interval(score: float, abstain: bool) -> Interval:
    half = ABSTAIN_HALF_WIDTH if abstain else HALF_WIDTH
    return Interval(
        lower=round(max(0.0, score - half), 3),
        upper=round(min(1.0, score + half), 3),
        coverage=COVERAGE,
    )


def predict(zone_id: str, hazard: str, as_of: date) -> Prediction:
    month = _month_key(as_of)
    score = round(0.05 + 0.9 * _unit(zone_id, hazard, month), 3)
    abstain = _is_abstain(zone_id, hazard, month)
    return Prediction(
        zone_id=zone_id,
        municipality=MUNICIPALITIES[zone_id]["municipality"],
        hazard=hazard,
        abstain=abstain,
        risk_score=score,
        risk_level=level_for(score),
        interval=_interval(score, abstain),
        top_factors=_factors(zone_id, hazard, month),
        model_version=MODEL_VERSION,
        data_version=DATA_VERSION,
    )


def explain(zone_id: str, hazard: str, as_of: date) -> Explanation:
    history = []
    for back in range(HISTORY_MONTHS, 0, -1):
        total = as_of.year * 12 + as_of.month - 1 - back
        point = date(total // 12, total % 12 + 1, 1)
        history.append(
            HistoryPoint(
                date=point,
                risk_score=round(0.05 + 0.9 * _unit(zone_id, hazard, _month_key(point)), 3),
            )
        )
    return Explanation(
        zone_id=zone_id, top_factors=_factors(zone_id, hazard, _month_key(as_of)), history=history
    )


def metrics() -> Metrics:
    names = ("pr_auc", "macro_f1")
    return Metrics(
        model_version=MODEL_VERSION,
        data_version=DATA_VERSION,
        validation="spatial_block_cv",
        metrics=[Metric(name=n, value=0.0, ci_lower=0.0, ci_upper=0.0) for n in names],
        baseline=[Metric(name=n, value=0.0) for n in names],
        calibration={"ece": 0.0},
        conformal_coverage=0.0,
    )
