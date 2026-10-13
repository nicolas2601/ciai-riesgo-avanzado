"""Tests for the research track: architecture, clipping and guards."""

import numpy as np
import torch as th

from ml.src.rl_arch import PerMunicipalityPolicy, clip_cutoff_features
from ml.src.rl_env import SeismicPrioritizationEnv
from ml.src.rl_experiments import (
    REFERENCE_DIR,
    _guard_out_dir,
    mean_policy_entropy,
    sensitivity_probe,
)


def _toy_policy():
    import gymnasium as gym
    from gymnasium import spaces

    obs_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4 * 2 + 4 + 1,), dtype=np.float32)
    return PerMunicipalityPolicy(
        obs_space,
        gym.spaces.Discrete(4),
        lambda _: 3e-4,
        n_municipalities=4,
        n_features=2,
    )


def test_permutation_of_municipalities_permutes_logits():
    policy = _toy_policy()
    rng = np.random.default_rng(3)
    obs = np.concatenate(
        [
            rng.random(8).astype(np.float32),
            np.zeros(4, dtype=np.float32),
            np.array([1.0], dtype=np.float32),
        ]
    )
    perm = [2, 0, 3, 1]
    blocks = obs[:8].reshape(4, 2)[perm].ravel()
    swapped = np.concatenate([blocks, obs[8:]])

    # NOTE: proba_distribution mutates and returns the shared action_dist
    # object, so logits must be read immediately per call, never deferred.
    def _logits(vector: np.ndarray) -> np.ndarray:
        with th.no_grad():
            dist = policy.get_distribution(th.as_tensor(vector).unsqueeze(0))
            return dist.distribution.logits.numpy().ravel()

    first = _logits(obs)
    second = _logits(swapped)
    np.testing.assert_allclose(second, first[perm], rtol=1e-5)


def test_architecture_trains_one_rollout_without_error():
    from sb3_contrib import MaskablePPO

    rng = np.random.default_rng(5)
    cutoffs = {
        m: {
            "zone_ids": [f"{i:05d}" for i in range(6)],
            "features": rng.random((6, 3)).astype(np.float32),
            "eligible": np.ones(6, dtype=bool),
            "future": rng.integers(0, 2, size=6).astype(float),
            "n_features": 3,
        }
        for m in ("2024-01", "2024-02")
    }
    env = SeismicPrioritizationEnv(cutoffs, budget_k=2)
    agent = MaskablePPO(
        PerMunicipalityPolicy,
        env,
        policy_kwargs={"n_municipalities": 6, "n_features": 3, "hidden_dim": 8},
        n_steps=16,
        seed=7,
        device="cpu",
        verbose=0,
    )
    agent.learn(total_timesteps=64)
    obs, _ = env.reset(seed=7, options={"cutoff": "2024-01"})
    action, _ = agent.predict(obs, deterministic=True, action_masks=env.action_masks())
    assert env.action_space.contains(int(action))


def test_clip_is_bounded_idempotent_and_preserves_metadata():
    rng = np.random.default_rng(9)
    entry = {
        "zone_ids": ["00001", "00002"],
        "features": (rng.random((2, 3)).astype(np.float32) - 0.5) * 40,
        "eligible": np.array([True, False]),
        "future": np.array([1.0, 0.0]),
        "n_features": 3,
    }
    once = clip_cutoff_features({"m": entry})["m"]
    twice = clip_cutoff_features({"m": once})["m"]
    assert float(np.abs(once["features"]).max()) <= 5.0
    np.testing.assert_array_equal(once["features"], twice["features"])
    assert once["zone_ids"] == ["00001", "00002"]
    np.testing.assert_array_equal(once["eligible"], entry["eligible"])
    np.testing.assert_array_equal(once["future"], entry["future"])


def test_research_guard_rejects_reference_dir():
    try:
        _guard_out_dir(REFERENCE_DIR)
    except ValueError:
        return
    raise AssertionError("research must refuse the reference artifact dir")


def test_probe_and_entropy_helpers_are_deterministic():
    from sb3_contrib import MaskablePPO

    rng = np.random.default_rng(11)
    cutoffs = {
        m: {
            "zone_ids": [f"{i:05d}" for i in range(6)],
            "features": rng.random((6, 3)).astype(np.float32),
            "eligible": np.ones(6, dtype=bool),
            "future": rng.integers(0, 2, size=6).astype(float),
            "n_features": 3,
        }
        for m in ("2024-01", "2024-02")
    }
    env = SeismicPrioritizationEnv(cutoffs, budget_k=2)
    agent = MaskablePPO("MlpPolicy", env, n_steps=16, seed=7, device="cpu", verbose=0)
    agent.learn(total_timesteps=64)
    first = sensitivity_probe(agent, cutoffs)
    second = sensitivity_probe(agent, cutoffs)
    assert first == second
    assert mean_policy_entropy(agent, cutoffs) == mean_policy_entropy(agent, cutoffs)
    assert first["n_cutoffs"] == 2
