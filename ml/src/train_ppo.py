"""Bounded MaskablePPO training on CPU for the prioritization task.

Small MLP, few thousand timesteps, no GPU, no tuning. A smoke test
(short learn + masked rollout) must pass before the real run; if the
setting cannot learn stably, that is reported, not disguised.
"""

import argparse
import json
import time
from pathlib import Path

from ml.src.data import build_supervised_frame, load_metadata, load_panel, usable_months
from ml.src.rl_env import BUDGET_K, SeismicPrioritizationEnv, build_cutoff_data

ARTIFACT_DIR = Path("artifacts") / "ml" / "rl"

DEFAULT_CONFIG = {
    "seed": 7,
    "budget_k": BUDGET_K,
    "total_timesteps": 8192,
    "n_steps": 64,
    "batch_size": 32,
    "learning_rate": 3e-4,
    "net_arch": [64],
    "gamma": 1.0,
    "device": "cpu",
}


def train_month_list() -> list:
    """Chronological train months from the supervised frame (reuse)."""
    panel = load_panel()
    metadata = load_metadata()
    _, _, index, _ = build_supervised_frame(panel, metadata)
    months = usable_months(index)
    return months[: int(len(months) * 0.70)]


def make_env(train_months: list, seed: int, budget_k: int = BUDGET_K):
    """Environment over train cutoffs only (no val/test contact)."""
    cutoffs = build_cutoff_data(train_months, train_months, budget_k=budget_k)
    return SeismicPrioritizationEnv(cutoffs, budget_k=budget_k), cutoffs


def make_agent(env, config: dict):
    """MaskablePPO with a small MLP, fresh random weights, CPU."""
    from sb3_contrib import MaskablePPO

    return MaskablePPO(
        "MlpPolicy",
        env,
        policy_kwargs={"net_arch": list(config["net_arch"])},
        n_steps=int(config["n_steps"]),
        batch_size=int(config["batch_size"]),
        learning_rate=float(config["learning_rate"]),
        gamma=float(config["gamma"]),
        seed=int(config["seed"]),
        device=config["device"],
        verbose=0,
    )


def masked_rollout(agent, env, cutoff: str) -> dict:
    """Run K masked picks on one cutoff; return picks and reward."""
    obs, _ = env.reset(options={"cutoff": cutoff})
    rewards = []
    for _ in range(env.budget_k):
        action, _ = agent.predict(obs, deterministic=True, action_masks=env.action_masks())
        obs, reward, terminated, truncated, _ = env.step(int(action))
        rewards.append(float(reward))
        if terminated or truncated:
            break
    picks = env.selected_zones()
    assert len(set(picks)) == env.budget_k, "repeated municipality selected"
    return {
        "cutoff": cutoff,
        "picks": picks,
        "reward": float(rewards[-1]),
        "intermediate": [float(r) for r in rewards[:-1]],
    }


def smoke_test(config: dict | None = None) -> dict:
    """Brief learn + masked rollout; validates lifecycle, not performance."""
    config = dict(DEFAULT_CONFIG, **(config or {}))
    train_months = train_month_list()
    env, cutoffs = make_env(train_months, config["seed"], config["budget_k"])
    agent = make_agent(env, {**config, "n_steps": 32})
    agent.learn(total_timesteps=256)
    probe = min(cutoffs)
    rollout = masked_rollout(agent, env, probe)
    assert rollout["intermediate"] == [0.0] * (config["budget_k"] - 1)
    assert env.observation_space.contains(env.reset(options={"cutoff": probe})[0])
    return {"ok": True, "probe": rollout, "n_train_cutoffs": len(cutoffs)}


def train(config: dict | None = None, out_dir: Path = ARTIFACT_DIR) -> dict:
    """Smoke test first, then the bounded training run; saves the policy."""
    config = dict(DEFAULT_CONFIG, **(config or {}))
    smoke = smoke_test(config)
    train_months = train_month_list()
    env, cutoffs = make_env(train_months, config["seed"], config["budget_k"])
    agent = make_agent(env, config)
    started = time.perf_counter()
    agent.learn(total_timesteps=int(config["total_timesteps"]))
    train_seconds = round(time.perf_counter() - started, 2)
    out_dir.mkdir(parents=True, exist_ok=True)
    agent.save(str(out_dir / "ppo_policy"))
    (out_dir / "ppo_config.json").write_text(
        json.dumps(
            {
                **config,
                "train_months": [train_months[0], train_months[-1]],
                "n_train_cutoffs": len(cutoffs),
                "train_seconds": train_seconds,
                "init": "random weights (MaskablePPO default)",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "config": config,
        "smoke": smoke,
        "train_seconds": train_seconds,
        "model_path": str(out_dir / "ppo_policy.zip"),
    }


def main() -> None:
    """CLI entry point: smoke test, then bounded training."""
    parser = argparse.ArgumentParser(description="Train the MaskablePPO policy")
    parser.add_argument("--out-dir", type=Path, default=ARTIFACT_DIR)
    parser.add_argument("--total-timesteps", type=int, default=DEFAULT_CONFIG["total_timesteps"])
    args = parser.parse_args()
    info = train({"total_timesteps": args.total_timesteps}, args.out_dir)
    print(f"smoke={info['smoke']['ok']} train_s={info['train_seconds']} model={info['model_path']}")


if __name__ == "__main__":
    main()
