"""Tests for the RL environment, baselines and temporal separation."""

import inspect

import numpy as np

from ml.src.baselines import (
    fit_static_topk,
    oracle_pick,
    random_pick,
    ranker_pick,
    selection_reward,
    static_pick,
)
from ml.src.data import (
    build_supervised_frame,
    load_metadata,
    load_panel,
    temporal_month_splits,
    usable_months,
)
from ml.src.rl_env import BUDGET_K, SeismicPrioritizationEnv, build_cutoff_data

ZONES = ["00006", "00001", "00003", "00005", "00002", "00004"]


def _toy_cutoffs():
    rng = np.random.default_rng(7)
    cutoffs = {}
    for month in ("2024-01", "2024-02"):
        cutoffs[month] = {
            "zone_ids": sorted(ZONES),
            "features": rng.random((6, 3)).astype(np.float32),
            "eligible": np.array([True, True, True, True, False, False]),
            "future": np.array([0.0, 1.0, 0.0, 1.0, 1.0, 999.0]),
            "n_features": 3,
        }
    return cutoffs


def test_gymnasium_api_and_truncated_semantics():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    obs, info = env.reset(seed=7)
    assert isinstance(info, dict) and "cutoff" in info
    assert env.observation_space.contains(obs)
    obs, reward, terminated, truncated, _ = env.step(int(np.flatnonzero(env.action_masks())[0]))
    assert reward == 0.0 and not terminated and truncated is False
    assert isinstance(terminated, bool) and isinstance(truncated, bool)


def test_observation_shape_dtype_and_content():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    obs, _ = env.reset(seed=7, options={"cutoff": "2024-01"})
    assert obs.shape == (6 * 3 + 6 + 1,)
    assert obs.dtype == np.float32
    entry = env._entry
    expected = np.concatenate(
        [
            entry["features"].ravel(),
            np.zeros(6, dtype=np.float32),
            np.array([1.0], dtype=np.float32),
        ]
    )
    np.testing.assert_array_equal(obs, expected)
    assert 999.0 not in obs, "future values must never enter the observation"


def test_masks_exclude_selected_and_ineligible():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    env.reset(seed=7, options={"cutoff": "2024-01"})
    first = env.action_masks()
    assert first.tolist() == [True, True, True, True, False, False]
    env.step(0)
    second = env.action_masks()
    assert second.tolist() == [False, True, True, True, False, False]


def test_repeated_and_out_of_space_actions_are_rejected():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    env.reset(seed=7, options={"cutoff": "2024-01"})
    env.step(1)
    before = env.action_masks().copy()
    _obs, reward, terminated, _, info = env.step(1)
    assert reward == 0.0 and not terminated and info.get("invalid_action") is True
    np.testing.assert_array_equal(env.action_masks(), before)
    _obs, reward, terminated, _, info = env.step(6)
    assert reward == 0.0 and not terminated and info.get("invalid_action") is True


def test_budget_exceeding_eligible_is_rejected():
    cutoffs = _toy_cutoffs()
    try:
        SeismicPrioritizationEnv(cutoffs, budget_k=6)
    except ValueError:
        return
    raise AssertionError("K above eligible count must fail")


def test_terminal_reward_is_mean_future_of_selected():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    env.reset(seed=7, options={"cutoff": "2024-01"})
    env.step(1)
    _, reward, terminated, _, _ = env.step(3)
    assert terminated is True
    assert reward == float(np.mean([1.0, 1.0])) == 1.0
    assert env.selected_zones() == ["00002", "00004"]


def test_stable_divipola_order_and_reproducibility():
    first = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    second = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    assert first.zone_ids == sorted(ZONES)
    first.reset(seed=11)
    second.reset(seed=11)
    assert first.current_cutoff() == second.current_cutoff()
    first.reset(seed=11)
    assert first.current_cutoff() == second.current_cutoff()


def test_unknown_cutoff_option_fails():
    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    try:
        env.reset(options={"cutoff": "1999-01"})
    except ValueError:
        return
    raise AssertionError("unknown cutoff must fail")


def test_build_excludes_cutoff_without_future_coverage():
    panel = load_panel()
    metadata = load_metadata()
    _, _, index, _ = build_supervised_frame(panel, metadata)
    months = usable_months(index)
    train_months = months[:10]
    try:
        build_cutoff_data(["2026-09"], train_months)
    except ValueError:
        pass
    else:
        raise AssertionError("2026-09 without future must be excluded")
    cutoffs = build_cutoff_data(["2024-01", "2024-02"], train_months)
    assert set(cutoffs) == {"2024-01", "2024-02"}
    entry = cutoffs["2024-01"]
    assert entry["zone_ids"] == sorted(entry["zone_ids"])
    assert int(entry["eligible"].sum()) == 87
    assert entry["features"].shape == (87, len(metadata["features"]))
    assert not np.isnan(entry["features"]).any()


def test_baseline_signatures_take_no_future():
    for fn in (random_pick, static_pick, ranker_pick, fit_static_topk):
        params = set(inspect.signature(fn).parameters)
        assert not (params & {"future", "target", "activity", "y_future"}), fn


def test_ranker_picks_ignore_future_values():
    cutoffs = build_cutoff_data(["2024-01"], ["2019-02", "2019-03"])
    entry = cutoffs["2024-01"]
    from ml.src.baselines import eligible_positions, fit_activity_ranker

    bundle = fit_activity_ranker(["2019-02", "2019-03"])
    honest = ranker_pick(bundle, entry, 2)
    tampered = dict(entry, future=np.zeros_like(entry["future"]))
    assert ranker_pick(bundle, tampered, 2) == honest
    assert len(set(honest)) == 2
    assert set(honest) <= set(eligible_positions(entry).tolist())


def test_static_ranking_uses_train_only_and_oracle_is_explicit():
    cutoffs = _toy_cutoffs()
    entry = cutoffs["2024-01"]
    order = fit_static_topk({"2024-01": entry})
    assert order[:2] == [5, 1], "raw ranking ignores eligibility; picks must not"
    eligible = np.flatnonzero(entry["eligible"])
    static = static_pick(order, eligible, 2)
    assert static == [1, 3], "ineligible sentinel must be skipped at pick time"
    oracle = oracle_pick(entry["future"], eligible, 2)
    assert set(oracle) == {1, 3}
    assert selection_reward(entry["future"], static) == 1.0


def test_temporal_splits_keep_train_before_eval():
    panel = load_panel()
    metadata = load_metadata()
    _, _, index, _ = build_supervised_frame(panel, metadata)
    splits = temporal_month_splits(usable_months(index))
    assert max(splits["train"]) < min(splits["val"]) < min(splits["test"])
    assert not (set(splits["train"]) & (set(splits["val"]) | set(splits["test"])))


def test_policy_save_load_roundtrip(tmp_path):
    from sb3_contrib import MaskablePPO

    env = SeismicPrioritizationEnv(_toy_cutoffs(), budget_k=2)
    agent = MaskablePPO("MlpPolicy", env, n_steps=16, seed=7, device="cpu", verbose=0)
    agent.learn(total_timesteps=64)
    obs, _ = env.reset(seed=7, options={"cutoff": "2024-01"})
    masks = env.action_masks()
    first, _ = agent.predict(obs, deterministic=True, action_masks=masks)
    path = tmp_path / "policy"
    agent.save(str(path))
    reloaded = MaskablePPO.load(str(path), env=env)
    second, _ = reloaded.predict(obs, deterministic=True, action_masks=masks)
    assert int(first) == int(second)
    assert BUDGET_K == 5
