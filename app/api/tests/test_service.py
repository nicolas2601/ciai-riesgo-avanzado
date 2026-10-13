"""Service tests (API v1) on the real panel and model. The no-model case points at a missing file."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.service import Settings, create_app

ROOT = Path(__file__).resolve().parents[3]
PREFIX = "/api/v1"


def _client(model_path: Path) -> TestClient:
    settings = Settings(
        panel_path=ROOT / "data/panel/panel_municipio_mes.csv.gz",
        municipios_path=ROOT / "app/api/data/municipios_santander.json",
        model_path=model_path,
        clusters_path=ROOT / "app/web/public/data/clusters-missing.json",
        cors_origins=("http://localhost:5173",),
    )
    return TestClient(create_app(settings))


@pytest.fixture(scope="module")
def client() -> TestClient:
    return _client(ROOT / "artifacts/ml/selected_model.joblib")


@pytest.fixture(scope="module")
def client_without_model() -> TestClient:
    return _client(ROOT / "artifacts/ml/missing.joblib")


def test_health_reports_models(client: TestClient) -> None:
    body = client.get(f"{PREFIX}/health").json()
    assert body["status"] == "ok"
    assert body["modelos"] == {"clasificador": True, "agente": False, "clusters": False}


def test_municipios_lists_87_with_population(client: TestClient) -> None:
    zones = client.get(f"{PREFIX}/municipios").json()
    assert len(zones) == 87
    assert {"divipola", "nombre", "lat", "lon", "poblacion"} <= set(zones[0])
    assert len({z["divipola"] for z in zones}) == 87


def test_panel_returns_rows_with_features_and_targets(client: TestClient) -> None:
    body = client.get(f"{PREFIX}/panel", params={"mes": "2026-09"}).json()
    assert body["mes"] == "2026-09"
    assert len(body["filas"]) == 87
    row = body["filas"][0]
    assert {
        "divipola",
        "nombre",
        "features",
        "clase_observada",
        "target_clase_mes_siguiente",
    } <= set(row)
    assert "n_eventos_3m" in row["features"]


@pytest.mark.parametrize("mes", ["2026-13", "2026-9", "abril"])
def test_malformed_month_is_422_with_error_envelope(client: TestClient, mes: str) -> None:
    response = client.get(f"{PREFIX}/panel", params={"mes": mes})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_unknown_month_is_404(client: TestClient) -> None:
    assert (
        client.get(f"{PREFIX}/panel", params={"mes": "2001-01"}).json()["error"]["code"]
        == "month_not_found"
    )


def test_clasificar_returns_normalized_probabilities(client: TestClient) -> None:
    body = client.post(f"{PREFIX}/clasificar", json={"divipola": "68001", "mes": "2026-09"}).json()
    assert body["clase"] in {"bajo", "medio", "alto"}
    assert set(body["probabilidades"]) == {"bajo", "medio", "alto"}
    assert abs(sum(body["probabilidades"].values()) - 1.0) < 1e-3
    assert body["exploratorio"] is True
    assert len(body["version"]) == 12


def test_clasificar_unknown_zone_is_404(client: TestClient) -> None:
    response = client.post(f"{PREFIX}/clasificar", json={"divipola": "99999", "mes": "2026-09"})
    assert response.json()["error"]["code"] == "zone_not_found"


def test_clasificar_without_model_is_503(client_without_model: TestClient) -> None:
    response = client_without_model.post(
        f"{PREFIX}/clasificar", json={"divipola": "68001", "mes": "2026-09"}
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "model_not_loaded"


def test_priorizacion_lists_methods_and_is_exploratory(client: TestClient) -> None:
    body = client.get(f"{PREFIX}/priorizacion", params={"corte": "2026-09", "k": 5}).json()
    assert body["exploratorio"] is True
    assert [m["metodo"] for m in body["metodos"]] == ["estatico", "aleatorio", "ppo"]
    estatico = body["metodos"][0]["municipios"]
    assert [m["rank"] for m in estatico] == [1, 2, 3, 4, 5]
    assert body["metodos"][2]["municipios"] == []


def test_priorizacion_aleatorio_is_deterministic(client: TestClient) -> None:
    params = {"corte": "2026-09", "k": 5}
    first = client.get(f"{PREFIX}/priorizacion", params=params).json()["metodos"][1]
    second = client.get(f"{PREFIX}/priorizacion", params=params).json()["metodos"][1]
    assert first == second


@pytest.mark.parametrize("k", [0, 88])
def test_priorizacion_rejects_k_out_of_range(client: TestClient, k: int) -> None:
    assert (
        client.get(f"{PREFIX}/priorizacion", params={"corte": "2026-09", "k": k}).status_code == 422
    )


def test_priorizacion_works_without_model(client_without_model: TestClient) -> None:
    response = client_without_model.get(f"{PREFIX}/priorizacion", params={"corte": "2026-09"})
    assert response.status_code == 200


def test_clusters_is_503_until_published(client: TestClient) -> None:
    assert client.get(f"{PREFIX}/clusters").status_code == 503


def test_openapi_documents_every_endpoint(client: TestClient) -> None:
    spec = client.get("/openapi.json").json()
    assert spec["info"]["title"].startswith("API Riesgo")
    assert {"Basico", "Medio", "Avanzado", "Sistema"} <= {t["name"] for t in spec["tags"]}
    assert "/api/v1/clasificar" in spec["paths"]
