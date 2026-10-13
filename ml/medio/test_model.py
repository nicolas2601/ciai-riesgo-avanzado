import numpy as np
import pandas as pd

from ml.medio.model import BASE_FEATURES, aggregate_profiles, fit_clusters


def sample_panel():
    rng = np.random.default_rng(7)
    panel = pd.DataFrame({name: rng.uniform(1, 100, 87) for name in BASE_FEATURES})
    panel["divipola"] = [f"68{i:03d}" for i in range(87)]
    panel["month"] = "2025-05"
    panel["coverage_complete"] = True
    return panel


def test_aggregation_has_87_units_and_15_variables_without_targets():
    panel = sample_panel()
    panel["target_clase_mes_siguiente"] = "alto"
    profiles = aggregate_profiles(panel)
    assert profiles.shape[0] == 87
    assert profiles.shape[1] >= 15
    assert not any(name.startswith("target_") for name in profiles)


def test_future_rows_and_labels_cannot_change_profiles():
    past = sample_panel()
    future = past.assign(month="2025-06", poblacion=99999999, n_eventos_mes=100000)
    pd.testing.assert_frame_equal(
        aggregate_profiles(past), aggregate_profiles(pd.concat([past, future]))
    )


def test_clustering_is_deterministic_for_fixed_seed():
    profiles = aggregate_profiles(sample_panel())
    first = fit_clusters(profiles)
    second = fit_clusters(profiles)
    np.testing.assert_array_equal(first["labels"], second["labels"])
    assert first["k"] in range(3, 8)
    assert first["silhouette"] == second["silhouette"]
