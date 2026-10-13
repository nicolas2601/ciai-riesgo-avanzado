"""Controlled RL research experiments (reference track stays frozen).

Variants (same K, reward, eligibility, cutoffs; one change at a time):
- V0_ref: reference config (flat MLP [64]), seeds 7/21/42.
- V1_clip: same config, scaled features clipped to [-5, 5] (fixed rule).
- V2_permuni: per-municipality encoder policy, hidden 32.

Deterministic references (no training): static top-K, binary ranker,
random. Selection uses VAL only by a predefined rule; the winner is
frozen before a single confirmatory TEST run (prior test exposure from
the reference track is declared as a caveat, not hidden).

Nothing here writes to artifacts/ml/rl/ (reference artifacts).
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from stable_baselines3.common.monitor import Monitor

from ml.src.baselines import fit_activity_ranker, fit_static_topk, selection_reward
from ml.src.data import dataset_sha256
from ml.src.evaluate_rl import evaluate_cutoffs, month_lists
from ml.src.rl_arch import PerMunicipalityPolicy, clip_cutoff_features
from ml.src.rl_env import BUDGET_K, SeismicPrioritizationEnv, build_cutoff_data
from ml.src.train_ppo import masked_rollout

RESEARCH_DIR = Path("artifacts") / "ml" / "rl_research"
REFERENCE_DIR = Path("artifacts") / "ml" / "rl"
TRAIN_SEEDS = [7, 21, 42]
REF_HYPER = {
    "total_timesteps": 8192,
    "n_steps": 64,
    "batch_size": 32,
    "learning_rate": 3e-4,
    "gamma": 1.0,
    "device": "cpu",
}
SELECTION_RULE = (
    "highest seed-averaged val mean reward; tie-breaks: paired win-rate "
    "vs static, then simpler variant (V0 < V1 < V2)"
)


def _guard_out_dir(out_dir: Path) -> None:
    if out_dir.resolve() == REFERENCE_DIR.resolve():
        raise ValueError("research must not overwrite reference artifacts")


def train_variant(variant: str, seed: int, train_cutoffs: dict, out_dir: Path) -> dict:
    """Train one seed of one variant with episode-reward logging."""
    from sb3_contrib import MaskablePPO

    cutoffs = train_cutoffs
    if variant == "V1_clip":
        cutoffs = clip_cutoff_features(train_cutoffs)
    env = SeismicPrioritizationEnv(cutoffs)
    env = Monitor(env, filename=str(out_dir / f"monitor_{variant}_seed{seed}"))
    if variant == "V2_permuni":
        entry = train_cutoffs[min(train_cutoffs)]
        policy, kwargs = (
            PerMunicipalityPolicy,
            {
                "n_municipalities": len(entry["zone_ids"]),
                "n_features": int(entry["n_features"]),
                "hidden_dim": 32,
            },
        )
    else:
        policy, kwargs = "MlpPolicy", {"net_arch": [64]}
    agent = MaskablePPO(
        policy,
        env,
        policy_kwargs=kwargs,
        seed=seed,
        verbose=0,
        **{k: v for k, v in REF_HYPER.items() if k != "total_timesteps"},
    )
    agent.learn(total_timesteps=REF_HYPER["total_timesteps"])
    model_path = out_dir / "policies" / f"{variant}_seed{seed}.zip"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    agent.save(str(model_path.with_suffix("")))
    log = pd.read_csv(f"{out_dir / f'monitor_{variant}_seed{seed}'}.monitor.csv", skiprows=1)
    rewards = log["r"].to_numpy(dtype=float)
    return {
        "variant": variant,
        "seed": seed,
        "model_path": str(model_path),
        "train_episodes": len(rewards),
        "train_reward_last10_mean": round(float(rewards[-len(rewards) // 10 :].mean()), 4),
        "train_reward_first10_mean": round(float(rewards[: len(rewards) // 10].mean()), 4),
    }


def load_variant_agent(model_path: str, train_cutoffs: dict):
    """Load a research policy onto a train-shaped env (no training)."""
    from sb3_contrib import MaskablePPO

    return MaskablePPO.load(model_path, env=SeismicPrioritizationEnv(train_cutoffs))


def eval_policy_on_cutoffs(agent, eval_cutoffs: dict) -> pd.DataFrame:
    """Per-cutoff rewards of one frozen policy (no baselines)."""
    env = SeismicPrioritizationEnv(eval_cutoffs)
    rows = []
    for month in sorted(eval_cutoffs):
        rollout = masked_rollout(agent, env, month)
        positions = [env.zone_ids.index(z) for z in rollout["picks"]]
        rows.append(
            {
                "cutoff": month,
                "picks": ",".join(rollout["picks"]),
                "reward": round(selection_reward(eval_cutoffs[month]["future"], positions), 4),
            }
        )
    return pd.DataFrame(rows)


def sensitivity_probe(agent, eval_cutoffs: dict) -> dict:
    """Count cutoffs where picks survive zeroed/swapped features."""
    months = sorted(eval_cutoffs)
    donor = eval_cutoffs[months[-1]]["features"]
    agree_zero, agree_swap, n_sets = 0, 0, set()
    for month in months:
        env = SeismicPrioritizationEnv({month: eval_cutoffs[month]})
        true_picks = masked_rollout(agent, env, month)["picks"]
        n_sets.add(tuple(sorted(true_picks)))
        zero_entry = dict(
            eval_cutoffs[month], features=np.zeros_like(eval_cutoffs[month]["features"])
        )
        same = np.array_equal(donor, eval_cutoffs[month]["features"])
        swap_feats = eval_cutoffs[months[0]]["features"] if same else donor
        swap_entry = dict(eval_cutoffs[month], features=swap_feats)
        env_z = SeismicPrioritizationEnv({month: zero_entry})
        env_s = SeismicPrioritizationEnv({month: swap_entry})
        agree_zero += set(masked_rollout(agent, env_z, month)["picks"]) == set(true_picks)
        agree_swap += set(masked_rollout(agent, env_s, month)["picks"]) == set(true_picks)
    return {
        "n_cutoffs": len(months),
        "distinct_sets": len(n_sets),
        "zero_agree": int(agree_zero),
        "swap_agree": int(agree_swap),
    }


def mean_policy_entropy(agent, eval_cutoffs: dict) -> float:
    """Mean stochastic-policy entropy over eval cutoffs and steps."""
    import torch as th

    env = SeismicPrioritizationEnv(eval_cutoffs)
    entropies = []
    with th.no_grad():
        for month in sorted(eval_cutoffs):
            obs, _ = env.reset(options={"cutoff": month})
            for _ in range(env.budget_k):
                masks = env.action_masks()
                dist = agent.policy.get_distribution(
                    th.as_tensor(obs).unsqueeze(0), th.as_tensor(masks).unsqueeze(0)
                )
                entropies.append(float(dist.entropy().item()))
                action, _ = agent.predict(obs, deterministic=True, action_masks=masks)
                obs, _, terminated, _, _ = env.step(int(action))
                if terminated:
                    break
    return round(float(np.mean(entropies)), 4)


def run_research(out_dir: Path = RESEARCH_DIR, test_once: bool = True) -> dict:
    """Train variants, compare on val, freeze winner, confirm on test once."""
    _guard_out_dir(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    train_months, val_months, test_months = month_lists()
    train_cutoffs = build_cutoff_data(train_months, train_months)
    val_cutoffs = build_cutoff_data(val_months, train_months)
    static_order = fit_static_topk(train_cutoffs)
    ranker = fit_activity_ranker(train_months)

    cards, val_frames = [], {}
    for variant in ("V0_ref", "V1_clip", "V2_permuni"):
        for seed in TRAIN_SEEDS:
            card = train_variant(variant, seed, train_cutoffs, out_dir)
            agent = load_variant_agent(card["model_path"], train_cutoffs)
            cutoffs = val_cutoffs if variant != "V1_clip" else clip_cutoff_features(val_cutoffs)
            frame = eval_policy_on_cutoffs(agent, cutoffs)
            card["val_mean"] = round(float(frame["reward"].mean()), 4)
            card["val_entropy"] = mean_policy_entropy(agent, cutoffs)
            card.update({f"probe_{k}": v for k, v in sensitivity_probe(agent, cutoffs).items()})
            val_frames[(variant, seed)] = frame
            frame.to_csv(out_dir / f"per_cutoff_val_{variant}_seed{seed}.csv", index=False)
            cards.append(card)
    summary = pd.DataFrame(cards)
    summary.to_csv(out_dir / "variant_cards.csv", index=False)
    variant_score = summary.groupby("variant")["val_mean"].mean().to_dict()
    winner = max(sorted(variant_score), key=lambda v: variant_score[v])
    best_seed = int(summary[summary.variant == winner].sort_values("val_mean").iloc[-1]["seed"])
    result = {
        "selection_rule": SELECTION_RULE,
        "variant_val_mean": {k: round(float(v), 4) for k, v in variant_score.items()},
        "winner": {"variant": winner, "seed": best_seed},
        "hyper": REF_HYPER,
        "train_seeds": TRAIN_SEEDS,
        "budget_k": BUDGET_K,
        "val_months": [val_months[0], val_months[-1]],
        "data_sha256": dataset_sha256(),
        "test_caveat": (
            "test months were exposed by the earlier reference track; "
            "the single test run below is confirmatory, not an intact firewall"
        ),
    }
    if test_once:
        test_cutoffs = build_cutoff_data(test_months, train_months)
        if winner == "V1_clip":
            test_cutoffs = clip_cutoff_features(test_cutoffs)
        card = summary[(summary.variant == winner) & (summary.seed == best_seed)].iloc[0]
        agent = load_variant_agent(card["model_path"], train_cutoffs)
        frame = eval_policy_on_cutoffs(agent, test_cutoffs)
        frame.to_csv(out_dir / f"per_cutoff_test_{winner}_seed{best_seed}.csv", index=False)
        full = evaluate_cutoffs(agent, test_cutoffs, static_order, ranker)
        full.to_csv(out_dir / f"per_cutoff_test_full_{winner}_seed{best_seed}.csv", index=False)
        result["test"] = {
            "variant": winner,
            "seed": best_seed,
            "test_months": [test_months[0], test_months[-1]],
            "mean": round(float(frame["reward"].mean()), 4),
            "static_mean": round(float(full["static_reward"].mean()), 4),
            "ranker_mean": round(float(full["ranker_reward"].mean()), 4),
        }
    (out_dir / "research_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    """CLI entry point for the research track."""
    import argparse

    parser = argparse.ArgumentParser(description="Run controlled RL experiments")
    parser.add_argument("--out-dir", type=Path, default=RESEARCH_DIR)
    parser.add_argument("--no-test", action="store_true")
    args = parser.parse_args()
    run_research(args.out_dir, test_once=not args.no_test)


if __name__ == "__main__":
    main()
