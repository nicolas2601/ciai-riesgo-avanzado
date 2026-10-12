"""Executable version of docs/plan/03-contrato-api.md (v0.2), run against the mock."""

import pytest
from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)
LEVELS = {"low", "medium", "high"}
HAZARDS = ("wildfire", "landslide", "flood")
TARGET = "2026-10"
SNAPSHOT_KEYS = {
    "model_version",
    "data_version",
    "hazard",
    "target_month",
    "feature_cutoff",
    "is_mock",
}


def predict(zone_id="68001", hazard="wildfire", target_month=TARGET):
    return client.post(
        "/api/v1/predict", json={"zone_id": zone_id, "hazard": hazard, "target_month": target_month}
    )


def test_health_is_liveness_only():
    assert client.get("/api/v1/health").json() == {"status": "ok"}


def test_ready_declares_mock_and_supported_hazards():
    body = client.get("/api/v1/ready").json()
    assert body["ready"] is True
    assert body["is_mock"] is True
    assert body["model_version"] == "mock"
    assert set(body["supported_hazards"]) == set(HAZARDS)
    assert {
        "data_version",
        "target_month",
        "feature_cutoff",
        "data_available_through",
    } <= body.keys()


def test_predict_matches_contract():
    body = predict().json()
    assert SNAPSHOT_KEYS <= body.keys()
    assert body["zone_id"] == "68001" and body["municipality"] == "Bucaramanga"
    assert body["target_month"] == TARGET and body["feature_cutoff"] == "2026-09-30"
    assert body["is_mock"] is True
    assert body["risk_level"] in LEVELS
    assert body["top_factors"] and {"feature", "shap", "value"} <= body["top_factors"][0].keys()


def test_class_probabilities_sum_to_one_and_drive_level_and_score():
    body = predict().json()
    probs = body["class_probabilities"]
    assert set(probs) == LEVELS
    assert sum(probs.values()) == pytest.approx(1.0, abs=1e-3)
    assert body["risk_level"] == max(probs, key=probs.get)
    assert body["risk_score"] == probs["high"]


def test_prediction_set_is_a_set_of_classes_with_alpha():
    body = predict().json()
    assert body["prediction_set"] and set(body["prediction_set"]) <= LEVELS
    assert body["risk_level"] in body["prediction_set"]
    assert body["conformal_alpha"] == 0.1
    assert "interval" not in body


def test_wide_prediction_set_triggers_abstention_with_reason():
    results = [predict(z, h).json() for z in ("68001", "68081", "68679", "68755") for h in HAZARDS]
    assert any(r["abstain"] for r in results)
    for r in results:
        assert r["abstain"] == (len(r["prediction_set"]) == 3)
        assert (r["abstain_reason"] is not None) == r["abstain"]


def test_predict_is_deterministic():
    assert predict().json() == predict().json()


def test_stale_data_abstains_instead_of_predicting():
    body = predict(target_month="2027-03").json()
    assert body["abstain"] is True and body["abstain_reason"] == "stale_data"


def test_unknown_zone_returns_error_envelope():
    res = predict(zone_id="00000")
    assert res.status_code == 404 and res.json()["error"]["code"] == "zone_not_found"


def test_invalid_hazard_returns_error_envelope():
    res = predict(hazard="earthquake")
    assert res.status_code == 422 and res.json()["error"]["code"] == "validation_error"


def test_invalid_target_month_returns_error_envelope():
    res = predict(target_month="October")
    assert res.status_code == 422 and res.json()["error"]["code"] == "validation_error"


def test_ranking_is_sorted_limited_and_snapshot_tagged():
    body = client.get(
        "/api/v1/zones/ranking", params={"limit": 5, "hazard": "flood", "target_month": TARGET}
    ).json()
    assert SNAPSHOT_KEYS <= body.keys() and body["hazard"] == "flood"
    items = body["items"]
    assert [i["rank"] for i in items] == [1, 2, 3, 4, 5]
    scores = [i["risk_score"] for i in items]
    assert scores == sorted(scores, reverse=True)


def test_zones_is_geojson_with_snapshot_foreign_member():
    body = client.get(
        "/api/v1/zones", params={"hazard": "landslide", "target_month": TARGET}
    ).json()
    assert body["type"] == "FeatureCollection" and len(body["features"]) == 87
    assert SNAPSHOT_KEYS <= body["snapshot"].keys() and body["snapshot"]["hazard"] == "landslide"
    props = body["features"][0]["properties"]
    assert {"zone_id", "municipality", "risk_score", "risk_level", "abstain"} <= props.keys()


def test_same_hazard_and_month_give_consistent_zones_ranking_explain():
    params = {"hazard": "flood", "target_month": TARGET}
    zones = client.get("/api/v1/zones", params=params).json()
    ranking = client.get("/api/v1/zones/ranking", params={**params, "limit": 1}).json()
    top = ranking["items"][0]
    feature = next(f for f in zones["features"] if f["properties"]["zone_id"] == top["zone_id"])
    assert feature["properties"]["risk_score"] == top["risk_score"]
    explain = client.get(f"/api/v1/zones/{top['zone_id']}/explain", params=params).json()
    assert explain["hazard"] == "flood" and explain["target_month"] == TARGET


def test_explain_has_factors_history_and_snapshot():
    body = client.get("/api/v1/zones/68001/explain", params={"target_month": TARGET}).json()
    assert SNAPSHOT_KEYS <= body.keys() and body["zone_id"] == "68001"
    assert body["top_factors"] and len(body["history"]) >= 6


@pytest.mark.parametrize(
    "path", ["/api/v1/zones/ranking", "/api/v1/zones", "/api/v1/zones/68001/explain"]
)
def test_unsupported_hazard_is_rejected_everywhere(path):
    res = client.get(path, params={"hazard": "earthquake"})
    assert res.status_code == 422 and res.json()["error"]["code"] == "validation_error"


def test_metrics_are_null_in_mock_and_never_invented():
    body = client.get("/api/v1/metrics", params={"hazard": "wildfire"}).json()
    assert body["is_mock"] is True and body["validation"] == "spatial_block_cv"
    assert body["metrics"] and all(m["value"] is None for m in body["metrics"])
    assert all(m["value"] is None for m in body["baseline"])
    assert body["conformal"] == {"alpha": 0.1, "empirical_coverage": None, "evaluation_scope": None}


def test_cors_allows_the_vite_dev_origin():
    res = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})
    assert res.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unknown_origins():
    res = client.get("/api/v1/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in res.headers


@pytest.mark.parametrize("month", ["0000-01", "0001-06", "2018-12", "2100-01", "2026-13"])
def test_out_of_range_target_month_is_rejected_at_the_edge(month):
    assert predict(target_month=month).status_code == 422
    for path in ("/api/v1/zones", "/api/v1/zones/ranking", "/api/v1/zones/68001/explain"):
        res = client.get(path, params={"target_month": month})
        assert res.status_code == 422 and res.json()["error"]["code"] == "validation_error"


def test_earliest_supported_month_does_not_crash_explain():
    res = client.get("/api/v1/zones/68001/explain", params={"target_month": "2019-01"})
    assert res.status_code == 200
    assert all(p["month"] >= "2019-01" for p in res.json()["history"])


STALE = "2026-11"


def test_explain_abstains_when_predict_abstains_for_the_same_snapshot():
    assert predict(target_month=STALE).json()["abstain_reason"] == "stale_data"
    body = client.get("/api/v1/zones/68001/explain", params={"target_month": STALE}).json()
    assert body["abstain"] is True and body["abstain_reason"] == "stale_data"
    assert body["top_factors"] == []


def test_explain_history_only_has_months_with_available_data():
    body = client.get("/api/v1/zones/68001/explain", params={"target_month": "2027-03"}).json()
    assert all(p["month"] <= "2026-10" for p in body["history"])


def test_zones_and_ranking_agree_with_predict_on_stale_target():
    zones = client.get("/api/v1/zones", params={"target_month": STALE}).json()
    assert all(
        f["properties"]["abstain"] and f["properties"]["risk_score"] is None
        for f in zones["features"]
    )
    assert client.get("/api/v1/zones/ranking", params={"target_month": STALE}).json()["items"] == []
