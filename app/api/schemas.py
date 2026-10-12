"""Pydantic models mirroring docs/plan/03-contrato-api.md (v0.2)."""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

Hazard = Literal["wildfire", "landslide", "flood"]
Level = Literal["low", "medium", "high"]
AbstainReason = Literal["stale_data", "wide_set", "low_support"]
# Supported months run from the start of the UNGRD series (2019-01) to 2099-12.
TARGET_MONTH_PATTERN = r"^20(19|[2-9]\d)-(0[1-9]|1[0-2])$"
TargetMonth = Annotated[str, StringConstraints(pattern=TARGET_MONTH_PATTERN)]


class Snapshot(BaseModel):
    """Identifies exactly which model, data, hazard and month a response belongs to."""

    model_version: str
    data_version: str
    hazard: Hazard
    target_month: TargetMonth
    feature_cutoff: date
    is_mock: bool


class Ready(BaseModel):
    ready: bool
    is_mock: bool
    model_version: str
    data_version: str
    supported_hazards: list[Hazard]
    target_month: TargetMonth
    feature_cutoff: date
    data_available_through: date


class Factor(BaseModel):
    feature: str
    shap: float
    value: float


class PredictRequest(BaseModel):
    zone_id: str
    hazard: Hazard = "wildfire"
    target_month: TargetMonth | None = None


class Prediction(Snapshot):
    zone_id: str
    municipality: str
    abstain: bool
    abstain_reason: AbstainReason | None
    class_probabilities: dict[Level, float] | None
    risk_level: Level | None
    risk_score: float | None
    prediction_set: list[Level]
    conformal_alpha: float
    top_factors: list[Factor]


class RankingItem(BaseModel):
    rank: int
    zone_id: str
    municipality: str
    risk_score: float
    risk_level: Level
    prediction_set: list[Level]


class Ranking(Snapshot):
    items: list[RankingItem]


class HistoryPoint(BaseModel):
    month: str
    risk_score: float


class Explanation(Snapshot):
    zone_id: str
    abstain: bool
    abstain_reason: AbstainReason | None
    top_factors: list[Factor]
    history: list[HistoryPoint]


class Metric(BaseModel):
    name: str
    value: float | None = None
    ci_lower: float | None = None
    ci_upper: float | None = None


class Conformal(BaseModel):
    alpha: float
    empirical_coverage: float | None = None
    evaluation_scope: str | None = None


class Metrics(Snapshot):
    validation: str
    metrics: list[Metric]
    baseline: list[Metric]
    calibration: dict[str, float | None]
    conformal: Conformal
