"""Pydantic models mirroring docs/plan/03-contrato-api.md."""

from datetime import date
from typing import Literal

from pydantic import BaseModel

Hazard = Literal["wildfire", "landslide", "flood"]
Level = Literal["low", "medium", "high"]


class Interval(BaseModel):
    lower: float
    upper: float
    coverage: float


class Factor(BaseModel):
    feature: str
    shap: float
    value: float


class PredictRequest(BaseModel):
    zone_id: str
    hazard: Hazard = "wildfire"
    as_of: date | None = None


class Prediction(BaseModel):
    zone_id: str
    municipality: str
    hazard: Hazard
    abstain: bool
    risk_score: float
    risk_level: Level
    interval: Interval
    top_factors: list[Factor]
    model_version: str
    data_version: str


class RankingItem(BaseModel):
    rank: int
    zone_id: str
    municipality: str
    risk_score: float
    risk_level: Level
    interval: Interval


class Ranking(BaseModel):
    items: list[RankingItem]
    model_version: str
    data_version: str


class HistoryPoint(BaseModel):
    date: date
    risk_score: float


class Explanation(BaseModel):
    zone_id: str
    top_factors: list[Factor]
    history: list[HistoryPoint]


class Metric(BaseModel):
    name: str
    value: float
    ci_lower: float | None = None
    ci_upper: float | None = None


class Metrics(BaseModel):
    model_version: str
    data_version: str
    validation: str
    metrics: list[Metric]
    baseline: list[Metric]
    calibration: dict[str, float]
    conformal_coverage: float
