"""FastAPI service. Serves the mock until a trained bundle is wired in (see docs/plan/03-contrato-api.md)."""

from datetime import date

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
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
)

DEFAULT_HAZARD: Hazard = "wildfire"
DEFAULT_RANKING_LIMIT = 20
MAX_RANKING_LIMIT = 100

app = FastAPI(title="CIAI territorial risk API", version="0.1.0")
router = APIRouter(prefix="/api/v1")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(HTTPException)
async def _http_error(_: Request, exc: HTTPException) -> JSONResponse:
    return _error(exc.status_code, str(exc.detail), str(exc.detail))


@app.exception_handler(RequestValidationError)
async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return _error(
        422,
        "validation_error",
        "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()),
    )


def _require_zone(zone_id: str) -> str:
    if zone_id not in mock.MUNICIPALITIES:
        raise HTTPException(status_code=404, detail="zone_not_found")
    return zone_id


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "model_version": mock.MODEL_VERSION, "data_version": mock.DATA_VERSION}


@router.post("/predict")
def predict(req: PredictRequest) -> Prediction:
    return mock.predict(_require_zone(req.zone_id), req.hazard, req.as_of or date.today())


def _all_predictions(hazard: Hazard) -> list[Prediction]:
    today = date.today()
    return [mock.predict(zone_id, hazard, today) for zone_id in mock.MUNICIPALITIES]


@router.get("/zones")
def zones(hazard: Hazard = DEFAULT_HAZARD, level: str | None = None) -> dict:
    features = []
    for p in _all_predictions(hazard):
        if level and p.risk_level != level:
            continue
        m = mock.MUNICIPALITIES[p.zone_id]
        props = p.model_dump(
            include={"zone_id", "municipality", "risk_score", "risk_level", "abstain"}
        )
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [m["lon"], m["lat"]]},
                "properties": props,
            }
        )
    return {"type": "FeatureCollection", "features": features}


@router.get("/zones/ranking")
def ranking(
    hazard: Hazard = DEFAULT_HAZARD, limit: int = DEFAULT_RANKING_LIMIT, level: str | None = None
) -> Ranking:
    preds = [p for p in _all_predictions(hazard) if not level or p.risk_level == level]
    preds.sort(key=lambda p: (-p.risk_score, p.zone_id))
    items = [
        RankingItem(
            rank=i,
            zone_id=p.zone_id,
            municipality=p.municipality,
            risk_score=p.risk_score,
            risk_level=p.risk_level,
            interval=p.interval,
        )
        for i, p in enumerate(preds[: min(limit, MAX_RANKING_LIMIT)], start=1)
    ]
    return Ranking(items=items, model_version=mock.MODEL_VERSION, data_version=mock.DATA_VERSION)


@router.get("/zones/{zone_id}/explain")
def explain(zone_id: str, hazard: Hazard = DEFAULT_HAZARD) -> Explanation:
    return mock.explain(_require_zone(zone_id), hazard, date.today())


@router.get("/metrics")
def metrics() -> Metrics:
    return mock.metrics()


app.include_router(router)
