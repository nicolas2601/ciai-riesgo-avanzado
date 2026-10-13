"""Temporal evaluation of the frozen RL policy against baselines.

Every policy faces the same eval cutoffs with the same budget K.
Val selects nothing here; test is evaluated once with the frozen
policy. The oracle stays a separate, non-operative reference.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.src.baselines import (
    eligible_positions,
    fit_activity_ranker,
    fit_static_topk,
    oracle_pick,
    random_pick,
    ranker_pick,
    selection_reward,
    static_pick,
)
from ml.src.data import (
    build_supervised_frame,
    dataset_sha256,
    load_metadata,
    load_panel,
    temporal_month_splits,
    usable_months,
)
from ml.src.rl_env import BUDGET_K, SeismicPrioritizationEnv, build_cutoff_data
from ml.src.train_ppo import masked_rollout

ARTIFACT_DIR = Path("artifacts") / "ml" / "rl"
RANDOM_SEEDS = [7, 11, 23, 41, 59]


def month_lists() -> tuple:
    """Train/val/test months reused from the supervised splits."""
    panel = load_panel()
    metadata = load_metadata()
    _, _, index, _ = build_supervised_frame(panel, metadata)
    splits = temporal_month_splits(usable_months(index))
    return splits["train"], splits["val"], splits["test"]


def load_policy(model_path: Path, env):
    """Load a frozen policy; no further training happens here."""
    from sb3_contrib import MaskablePPO

    return MaskablePPO.load(str(model_path), env=env)


def evaluate_cutoffs(
    agent, eval_cutoffs: dict, static_order: list, ranker: dict, budget_k: int = BUDGET_K
) -> pd.DataFrame:
    """One row per cutoff with every policy's picks and reward."""
    rows = []
    env = SeismicPrioritizationEnv(eval_cutoffs, budget_k=budget_k)
    for month in sorted(eval_cutoffs):
        entry = eval_cutoffs[month]
        eligible = eligible_positions(entry)
        future = entry["future"]
        positives = int((future[eligible] >= 0.5).sum())
        rollout = masked_rollout(agent, env, month)
        agent_reward = selection_reward(future, [env.zone_ids.index(z) for z in rollout["picks"]])
        random_rewards = []
        for seed in RANDOM_SEEDS:
            rng = np.random.default_rng(seed)
            picks = random_pick(eligible, budget_k, rng)
            random_rewards.append(selection_reward(future, picks))
        static_picks = static_pick(static_order, eligible, budget_k)
        ranker_picks = ranker_pick(ranker, entry, budget_k)
        oracle_picks = oracle_pick(future, eligible, budget_k)
        rows.append(
            {
                "cutoff": month,
                "n_eligible": len(eligible),
                "n_positive": positives,
                "agent_reward": round(agent_reward, 4),
                "agent_picks": ",".join(rollout["picks"]),
                "random_mean": round(float(np.mean(random_rewards)), 4),
                "random_std": round(float(np.std(random_rewards)), 4),
                "static_reward": round(selection_reward(future, static_picks), 4),
                "static_picks": ",".join(env.zone_ids[i] for i in static_picks),
                "ranker_reward": round(selection_reward(future, ranker_picks), 4),
                "ranker_picks": ",".join(env.zone_ids[i] for i in ranker_picks),
                "oracle_reward": round(selection_reward(future, oracle_picks), 4),
            }
        )
    return pd.DataFrame(rows)


def summarize(frame: pd.DataFrame, columns: dict) -> dict:
    """Mean, spread and support per policy over the eval cutoffs."""
    summary = {
        "n_cutoffs": len(frame),
        "cutoffs_with_positive": int((frame["n_positive"] > 0).sum()),
    }
    for policy, column in columns.items():
        values = frame[column].to_numpy(dtype=float)
        summary[policy] = {
            "mean": round(float(values.mean()), 4),
            "std": round(float(values.std()), 4),
            "min": round(float(values.min()), 4),
            "max": round(float(values.max()), 4),
        }
    diff = (frame["agent_reward"] - frame["static_reward"]).to_numpy(dtype=float)
    summary["agent_minus_static"] = {
        "mean": round(float(diff.mean()), 4),
        "std": round(float(diff.std()), 4),
    }
    summary["oracle_gap_agent"] = round(
        float(frame["oracle_reward"].mean() - frame["agent_reward"].mean()), 4
    )
    return summary


def ranker_check(ranker: dict, eval_cutoffs: dict) -> dict:
    """Binary temporal diagnostic of the ranker (not used for selection)."""
    from sklearn.metrics import f1_score

    labels, scores = [], []
    for month in sorted(eval_cutoffs):
        entry = eval_cutoffs[month]
        eligible = eligible_positions(entry)
        future = entry["future"][eligible]
        labels.extend((future >= 0.5).astype(int).tolist())
        from ml.src.baselines import ranker_scores

        proba = ranker_scores(ranker, entry["features"][eligible])
        scores.extend((proba >= 0.5).astype(int).tolist())
    labels = np.asarray(labels)
    return {
        "support_pos": int(labels.sum()),
        "n": len(labels),
        "macro_f1": round(float(f1_score(labels, scores, average="macro", zero_division=0)), 4),
    }


def run_evaluation(split: str = "val", out_dir: Path = ARTIFACT_DIR) -> dict:
    """Evaluate the frozen policy and baselines on one split's cutoffs."""
    train_months, val_months, test_months = month_lists()
    eval_months = val_months if split == "val" else test_months
    train_cutoffs = build_cutoff_data(train_months, train_months)
    eval_cutoffs = build_cutoff_data(eval_months, train_months)
    static_order = fit_static_topk(train_cutoffs)
    ranker = fit_activity_ranker(train_months)
    train_env = SeismicPrioritizationEnv(train_cutoffs)
    agent = load_policy(out_dir / "ppo_policy.zip", train_env)
    frame = evaluate_cutoffs(agent, eval_cutoffs, static_order, ranker)
    columns = {
        "agent": "agent_reward",
        "random": "random_mean",
        "static": "static_reward",
        "ranker": "ranker_reward",
    }
    summary = summarize(frame, columns)
    summary.update(
        {
            "split": split,
            "eval_months": [eval_months[0], eval_months[-1]],
            "budget_k": BUDGET_K,
            "random_seeds": RANDOM_SEEDS,
            "data_sha256": dataset_sha256(),
            "ranker_binary_check": ranker_check(ranker, eval_cutoffs),
            "ranker_train_support": ranker["train_support"],
            "oracle_note": "retrospective reference only; not an operative policy",
            "reward_note": "terminal mean of observed future activity; not damage",
        }
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out_dir / f"per_cutoff_{split}.csv", index=False)
    rows = [{"policy": policy, **summary[policy]} for policy in columns]
    rows.append(
        {
            "policy": "oracle_reference",
            "mean": round(float(frame["oracle_reward"].mean()), 4),
            "std": None,
            "min": None,
            "max": None,
        }
    )
    pd.DataFrame(rows).to_csv(out_dir / f"comparison_{split}.csv", index=False)
    (out_dir / f"metrics_rl_{split}.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (out_dir / f"comparison_{split}.md").write_text(
        render_comparison(frame, summary, split), encoding="utf-8"
    )
    print(
        f"split={split} n={len(frame)} agent={summary['agent']['mean']} "
        f"static={summary['static']['mean']} ranker={summary['ranker']['mean']} "
        f"random={summary['random']['mean']} oracle_gap={summary['oracle_gap_agent']}"
    )
    return summary


def _para(*parts: str) -> str:
    """Join message parts without implicit string concatenation."""
    return "".join(parts)


def render_comparison(frame: pd.DataFrame, summary: dict, split: str) -> str:
    """Markdown comparison with limits and honest reading guidance."""
    lines = [
        f"# RL evaluation ({split})",
        "",
        "| policy | mean | std | min | max |",
        "|---|---|---|---|---|",
    ]
    for policy in ("agent", "random", "static", "ranker"):
        s = summary[policy]
        lines.append(f"| {policy} | {s['mean']} | {s['std']} | {s['min']} | {s['max']} |")
    lines.append(f"| oracle_reference | {frame['oracle_reward'].mean():.4f} | - | - | - |")
    lines += [
        "",
        _para(
            f"Cutoffs: {summary['n_cutoffs']} ",
            f"({summary['eval_months'][0]} to {summary['eval_months'][1]}); ",
            f"{summary['cutoffs_with_positive']} with >= 1 positive municipality.",
        ),
        _para(
            f"Agent minus static: {summary['agent_minus_static']['mean']} ",
            f"(std {summary['agent_minus_static']['std']}). ",
            "A tiny gap with large spread is variability, not superiority.",
        ),
        _para(
            "Reward = terminal mean of observed future activity ",
            "(target_actividad_m3_mes_siguiente); not damage or official risk.",
        ),
        _para(
            "Ranker binary check ",
            f"(macro-F1 {summary['ranker_binary_check']['macro_f1']}, ",
            f"positives {summary['ranker_binary_check']['support_pos']}): ",
            "diagnostic only; the 3-class forest (medio recall 0 in test) ",
            "is never used as an activity probability.",
        ),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """CLI entry point for the RL evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate the frozen RL policy")
    parser.add_argument("--split", choices=["val", "test"], default="val")
    parser.add_argument("--out-dir", type=Path, default=ARTIFACT_DIR)
    args = parser.parse_args()
    run_evaluation(args.split, args.out_dir)


if __name__ == "__main__":
    main()
