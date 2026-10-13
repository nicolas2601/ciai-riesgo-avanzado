"""HTTP service for the territorial risk ranking (API v1).

Run with: uvicorn app.api.service:create_app --factory --host 0.0.0.0 --port 8000
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.ranking import Catalog, ModelNotLoaded, MonthNotFound, ZoneNotFound, file_sha256
from app.api.schemas_v1 import (
    Clasificacion,
    ClasificarRequest,
    Clusters,
    ErrorResponse,
    Health,
    Municipio,
    Panel,
    Priorizacion,
)

API_VERSION = "0.2.0"
MONTH_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"
MAX_K = 87
DEFAULT_CORS_ORIGINS = "http://localhost:5173"
ROOT = Path(__file__).resolve().parents[2]
MODEL_FILE = "selected_model.joblib"

MonthQ = Annotated[
    str, Query(pattern=MONTH_PATTERN, description="Mes YYYY-MM.", examples=["2026-09"])
]
ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    404: {"model": ErrorResponse, "description": "Mes o municipio fuera del panel."},
    422: {"model": ErrorResponse, "description": "Parametro mal formado."},
    503: {"model": ErrorResponse, "description": "Modelo o recurso no disponible."},
}

DESCRIPTION = """
API de priorizacion territorial de riesgo para Santander (87 municipios).

**Naturaleza:** priorizacion **exploratoria** sobre datos historicos (backtest). No es una
alerta oficial ni una prediccion operativa de sismos ni de danos.

**Fuentes:** catalogo de sismos del Servicio Geologico Colombiano (SGC) y proyecciones de
poblacion del DANE (CNPV 2018). Ver los documentos del proyecto para URLs y fechas de descarga.

**Errores:** siempre `{"error": {"code", "message"}}` con el status HTTP correcto.
"""

TAGS = [
    {"name": "Basico", "description": "Estado del servicio y catalogo de municipios."},
    {"name": "Medio", "description": "Panel mensual con variables y objetivos observados."},
    {"name": "Avanzado", "description": "Clasificacion supervisada y priorizacion (exploratorio)."},
    {"name": "Sistema", "description": "Clusters territoriales y utilidades del servicio."},
]


@dataclass(frozen=True)
class Settings:
    panel_path: Path
    municipios_path: Path
    model_path: Path
    clusters_path: Path
    cors_origins: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            panel_path=Path(
                os.environ.get("PANEL_PATH", ROOT / "data/panel/panel_municipio_mes.csv.gz")
            ),
            municipios_path=Path(
                os.environ.get("MUNICIPIOS_PATH", ROOT / "app/api/data/municipios_santander.json")
            ),
            model_path=Path(os.environ.get("MODEL_PATH", ROOT / "artifacts/ml" / MODEL_FILE)),
            clusters_path=Path(
                os.environ.get("CLUSTERS_PATH", ROOT / "app/web/public/data/clusters.json")
            ),
            cors_origins=tuple(os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")),
        )


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    catalog = Catalog.load(settings.panel_path, settings.municipios_path, settings.model_path)
    app = FastAPI(
        title="API Riesgo Sísmico Santander · Syntax error II",
        version=API_VERSION,
        description=DESCRIPTION,
        openapi_tags=TAGS,
    )
    app.state.catalog = catalog
    app.state.settings = settings
    app.state.model_version = (
        file_sha256(settings.model_path)[:12] if catalog.model_loaded else None
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
    )
    app.add_exception_handler(MonthNotFound, _month_not_found)
    app.add_exception_handler(ZoneNotFound, _zone_not_found)
    app.add_exception_handler(ModelNotLoaded, _model_not_loaded)
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(HTTPException, _http_error)
    app.include_router(_router(), prefix="/api/v1")
    return app


async def _month_not_found(_: Request, exc: MonthNotFound) -> JSONResponse:
    return _error(404, "month_not_found", f"mes fuera del panel: {exc}")


async def _zone_not_found(_: Request, exc: ZoneNotFound) -> JSONResponse:
    return _error(404, "zone_not_found", f"municipio sin fila para el mes: {exc}")


async def _model_not_loaded(_: Request, exc: ModelNotLoaded) -> JSONResponse:
    return _error(503, "model_not_loaded", str(exc))


async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    detail = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors())
    return _error(422, "validation_error", detail)


async def _http_error(_: Request, exc: HTTPException) -> JSONResponse:
    return _error(exc.status_code, str(exc.detail), str(exc.detail))


def _router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/health", tags=["Basico"], response_model=Health, summary="Liveness y modelos cargados"
    )
    def health(request: Request) -> dict[str, Any]:
        state = request.app.state
        return {
            "status": "ok",
            "modelos": {
                "clasificador": state.catalog.model_loaded,
                "agente": False,
                "clusters": state.settings.clusters_path.exists(),
            },
            "version": API_VERSION,
        }

    @router.get(
        "/municipios",
        tags=["Basico"],
        response_model=list[Municipio],
        summary="87 municipios de Santander",
    )
    def municipios(request: Request, mes: MonthQ | None = None) -> list[dict[str, Any]]:
        catalog: Catalog = request.app.state.catalog
        return catalog.municipios_with_population(mes or catalog.months[-1])

    @router.get(
        "/panel",
        tags=["Medio"],
        response_model=Panel,
        responses=ERROR_RESPONSES,
        summary="Filas del panel mensual con features y objetivos",
    )
    def panel(request: Request, mes: MonthQ) -> dict[str, Any]:
        return {"mes": mes, "filas": request.app.state.catalog.panel_rows(mes)}

    @router.post(
        "/clasificar",
        tags=["Avanzado"],
        response_model=Clasificacion,
        responses=ERROR_RESPONSES,
        summary="Clase de riesgo de un municipio con el clasificador supervisado",
    )
    def clasificar(request: Request, req: ClasificarRequest) -> dict[str, Any]:
        state = request.app.state
        result = state.catalog.classify(req.mes, req.divipola)
        return {
            **result,
            "modelo": MODEL_FILE,
            "version": state.model_version,
            "exploratorio": True,
        }

    @router.get(
        "/priorizacion",
        tags=["Avanzado"],
        response_model=Priorizacion,
        responses=ERROR_RESPONSES,
        summary="Top-k municipios por metodo (exploratorio)",
    )
    def priorizacion(
        request: Request,
        corte: MonthQ,
        k: Annotated[int, Query(ge=1, le=MAX_K, description="Municipios por metodo.")] = 5,
    ) -> dict[str, Any]:
        catalog: Catalog = request.app.state.catalog
        metodos = [
            {
                "metodo": "estatico",
                "municipios": catalog.baseline_ranking(corte, k),
                "recompensa_real": None,
            },
            {
                "metodo": "aleatorio",
                "municipios": catalog.random_ranking(corte, k),
                "recompensa_real": None,
            },
            {"metodo": "ppo", "municipios": [], "recompensa_real": None},
        ]
        return {
            "corte": corte,
            "k": k,
            "exploratorio": True,
            "nota": (
                "estatico: mayor n_eventos_3m (linea base). aleatorio: muestra determinista por mes. "
                "ppo: no disponible en este despliegue (runtime sin instalar); lista vacia."
            ),
            "metodos": metodos,
        }

    @router.get(
        "/clusters",
        tags=["Sistema"],
        response_model=Clusters,
        responses=ERROR_RESPONSES,
        summary="Clusters territoriales (pendiente de entrega)",
    )
    def clusters(request: Request) -> Any:
        path: Path = request.app.state.settings.clusters_path
        if not path.exists():
            raise HTTPException(status_code=503, detail="clusters_not_ready")
        return JSONResponse(content=json.loads(path.read_text(encoding="utf-8")))

    return router
