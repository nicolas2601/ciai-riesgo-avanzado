"""FastAPI service. Serves the mock until a trained bundle is wired in (see docs/plan/03-contrato-api.md)."""

import os
from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import mock
from app.api.schemas import (
    Explanation,
    Hazard,
    Metrics,
    Prediction,
    PredictRequest,
    Ranking,
    RankingItem,
    Ready,
)

DEFAULT_HAZARD: Hazard = "wildfire"
DEFAULT_RANKING_LIMIT = 20
MAX_RANKING_LIMIT = 100
DEFAULT_CORS_ORIGINS = "http://localhost:5173"
MONTH_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"

HazardQ = Annotated[Hazard, Query()]
MonthQ = Annotated[str | None, Query(pattern=MONTH_PATTERN)]

app = FastAPI(title="CIAI territorial risk API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)
router = APIRouter(prefix="/api/v1")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(HTTPException)
async def _http_error(_: Request, exc: HTTPException) -> JSONResponse:
    return _error(exc.status_code, str(exc.detail), str(exc.detail))


@app.exception_handler(RequestValidationError)
async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    detail = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors())
    return _error(422, "validation_error", detail)


def _require_zone(zone_id: str) -> str:
    if zone_id not in mock.MUNICIPALITIES:
        raise HTTPException(status_code=404, detail="zone_not_found")
    return zone_id


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> Ready:
    return mock.ready()


@router.post("/predict")
def predict(req: PredictRequest) -> Prediction:
    return mock.predict(_require_zone(req.zone_id), req.hazard, req.target_month)


def _all_predictions(hazard: Hazard, month: str | None) -> list[Prediction]:
    return [mock.predict(zone_id, hazard, month) for zone_id in mock.MUNICIPALITIES]


@router.get("/zones")
def zones(
    hazard: HazardQ = DEFAULT_HAZARD, target_month: MonthQ = None, level: str | None = None
) -> dict:
    features = []
    for p in _all_predictions(hazard, target_month):
        if level and p.risk_level != level:
            continue
        m = mock.MUNICIPALITIES[p.zone_id]
        props = p.model_dump(
            include={"zone_id", "municipality", "risk_score", "risk_level", "abstain"}
        )
        point = {"type": "Point", "coordinates": [m["lon"], m["lat"]]}
        features.append({"type": "Feature", "geometry": point, "properties": props})
    snap = mock.snapshot(hazard, target_month).model_dump(mode="json")
    return {"type": "FeatureCollection", "snapshot": snap, "features": features}


@router.get("/zones/ranking")
def ranking(
    hazard: HazardQ = DEFAULT_HAZARD,
    target_month: MonthQ = None,
    limit: int = DEFAULT_RANKING_LIMIT,
    level: str | None = None,
) -> Ranking:
    preds = [p for p in _all_predictions(hazard, target_month) if p.risk_score is not None]
    preds = [p for p in preds if not level or p.risk_level == level]
    preds.sort(key=lambda p: (-p.risk_score, p.zone_id))
    items = [
        RankingItem(
            rank=i,
            zone_id=p.zone_id,
            municipality=p.municipality,
            risk_score=p.risk_score,
            risk_level=p.risk_level,
            prediction_set=p.prediction_set,
        )
        for i, p in enumerate(preds[: min(limit, MAX_RANKING_LIMIT)], start=1)
    ]
    return Ranking(**mock.snapshot(hazard, target_month).model_dump(), items=items)


@router.get("/zones/{zone_id}/explain")
def explain(
    zone_id: str, hazard: HazardQ = DEFAULT_HAZARD, target_month: MonthQ = None
) -> Explanation:
    return mock.explain(_require_zone(zone_id), hazard, target_month)


@router.get("/metrics")
def metrics(hazard: HazardQ = DEFAULT_HAZARD) -> Metrics:
    return mock.metrics(hazard)


app.include_router(router)
