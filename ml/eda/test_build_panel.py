import pandas as pd

from ml.eda.build_panel import FEATURE_COLUMNS, build_panel


def sample_inputs():
    events = pd.DataFrame(
        {
            "datetime_utc": pd.to_datetime(["2024-01-05", "2024-02-03", "2024-03-02"], utc=True),
            "municipio": ["LOS SANTOS"] * 3,
            "lat": [6.8] * 3,
            "lon": [-73.1] * 3,
            "depth_km": [150, 20, 400],
            "mag": [3.5, 4.2, 2.0],
            "mag_type": ["MLr"] * 3,
            "source_system": ["new"] * 3,
            "rms": [0.2] * 3,
            "gap": [90] * 3,
            "phases": [10] * 3,
        }
    )
    municipalities = pd.DataFrame(
        {
            "zone_id": ["68418", "68001"],
            "municipality": ["Los Santos", "Bucaramanga"],
            "lat": [6.8, 7.15],
            "lon": [-73.1, -73.1],
        }
    )
    months = pd.period_range("2024-01", "2024-03", freq="M")
    return events, municipalities, months


def test_panel_has_zero_months_and_separate_future_targets():
    events, municipalities, months = sample_inputs()
    panel = build_panel(events, municipalities, months)
    assert len(panel) == 6
    assert len(FEATURE_COLUMNS) >= 20
    row = panel[(panel.zone_id == "68418") & (panel.month == "2024-01")].iloc[0]
    assert row.n_eventos_mes == 1
    assert row.target_clase_mes_siguiente == "alto"
    assert row.target_n_eventos_mes_siguiente == 1
    assert panel[panel.zone_id == "68001"].n_eventos_mes.eq(0).all()
    assert panel[panel.month == "2024-03"].target_clase_mes_siguiente.isna().all()


def test_features_do_not_change_when_future_events_are_deleted():
    events, municipalities, months = sample_inputs()
    full = build_panel(events, municipalities, months)
    past = build_panel(events[events.datetime_utc < "2024-02-01"], municipalities, months)
    cols = ["zone_id", "month", *FEATURE_COLUMNS]
    pd.testing.assert_frame_equal(
        full.loc[full.month == "2024-01", cols].reset_index(drop=True),
        past.loc[past.month == "2024-01", cols].reset_index(drop=True),
    )


def test_uncovered_calendar_gap_is_not_a_negative_target():
    events, municipalities, months = sample_inputs()
    panel = build_panel(events, municipalities, months.delete(1))
    january = panel[panel.month == "2024-01"]
    assert january.target_n_eventos_mes_siguiente.isna().all()
    assert january.target_clase_mes_siguiente.isna().all()


def test_santander_carmen_alias_is_not_a_zero_event_municipality():
    events, municipalities, months = sample_inputs()
    events["municipio"] = "EL CARMEN"
    municipalities.loc[0, "municipality"] = "El Carmen de Chucurí"
    panel = build_panel(events, municipalities, months)
    row = panel[(panel.zone_id == "68418") & (panel.month == "2024-01")].iloc[0]
    assert row.n_eventos_mes == 1
    assert row.divipola == row.zone_id


def test_detection_context_is_past_only_and_distinct_from_raw_local_count():
    events, municipalities, months = sample_inputs()
    panel = build_panel(events, municipalities, months)
    assert {"mc_maxc_12m", "n_eventos_departamento_mes"} <= set(FEATURE_COLUMNS)
    january = panel[panel.month == "2024-01"]
    assert january.n_eventos_departamento_mes.eq(1).all()


def test_population_join_uses_cutoff_year_and_not_future_projections():
    events, municipalities, months = sample_inputs()
    population = pd.DataFrame(
        {
            "divipola": ["68418", "68001", "68418", "68001"],
            "anio": [2024, 2024, 2025, 2025],
            "poblacion": [100, 200, 9999, 8888],
        }
    )
    full = build_panel(events, municipalities, months, population=population)
    past = build_panel(
        events, municipalities, months, population=population[population.anio == 2024]
    )
    pd.testing.assert_series_equal(full.poblacion, past.poblacion)
    assert full.loc[full.divipola == "68418", "poblacion"].eq(100).all()
