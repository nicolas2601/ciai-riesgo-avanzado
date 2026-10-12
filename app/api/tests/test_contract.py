"""Executable version of docs/plan/03-contrato-api.md, run against the mock."""

import pytest
from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)
LEVELS = {"low", "medium", "high"}


def predict(zone_id="68001", hazard="wildfire"):
    return client.post("/api/v1/predict", json={"zone_id": zone_id, "hazard": hazard})


def test_health_reports_mock_versions():
    body = client.get("/api/v1/health").json()
    assert body["status"] == "ok"
    assert body["model_version"] == "mock"
    assert body["data_version"]


def test_predict_matches_contract():
    res = predict()
    assert res.status_code == 200
    body = res.json()
    assert body["zone_id"] == "68001"
    assert body["municipality"] == "Bucaramanga"
    assert body["hazard"] == "wildfire"
    assert body["risk_level"] in LEVELS
    assert 0 <= body["risk_score"] <= 1
    interval = body["interval"]
    assert interval["lower"] <= body["risk_score"] <= interval["upper"]
    assert body["top_factors"] and {"feature", "shap", "value"} <= body["top_factors"][0].keys()
    assert body["model_version"] == "mock"


def test_predict_is_deterministic():
    assert predict().json() == predict().json()


@pytest.mark.parametrize(
    "score_level", [("68001", "wildfire"), ("68081", "landslide"), ("68679", "flood")]
)
def test_level_is_consistent_with_score(score_level):
    body = predict(*score_level).json()
    expected = (
        "low" if body["risk_score"] < 1 / 3 else "medium" if body["risk_score"] < 2 / 3 else "high"
    )
    assert body["risk_level"] == expected


def test_unknown_zone_returns_error_envelope():
    res = predict(zone_id="00000")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "zone_not_found"


def test_invalid_hazard_returns_error_envelope():
    res = predict(hazard="earthquake")
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "validation_error"


def test_ranking_is_sorted_and_limited():
    body = client.get("/api/v1/zones/ranking", params={"limit": 5}).json()
    items = body["items"]
    assert [i["rank"] for i in items] == [1, 2, 3, 4, 5]
    scores = [i["risk_score"] for i in items]
    assert scores == sorted(scores, reverse=True)
    assert body["model_version"] == "mock"


def test_zones_is_geojson_with_all_municipalities():
    body = client.get("/api/v1/zones").json()
    assert body["type"] == "FeatureCollection"
    assert len(body["features"]) == 87
    props = body["features"][0]["properties"]
    assert {"zone_id", "municipality", "risk_score", "risk_level", "abstain"} <= props.keys()


def test_explain_has_factors_and_history():
    body = client.get("/api/v1/zones/68001/explain").json()
    assert body["zone_id"] == "68001"
    assert body["top_factors"]
    assert len(body["history"]) >= 6 and {"date", "risk_score"} <= body["history"][0].keys()


def test_metrics_exposes_baseline_and_versions():
    body = client.get("/api/v1/metrics").json()
    assert body["validation"] == "spatial_block_cv"
    assert body["metrics"] and body["baseline"]
    assert body["model_version"] == "mock"
