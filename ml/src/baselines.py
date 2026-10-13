"""Operative baselines and the non-operative oracle for the RL task.

- random: uniform picks without replacement (recorded seeds).
- static top-K: mean train activity per municipality, train cutoffs only.
- contextual ranker: binary P(activity M>=3) trained on train rows only.
  The 3-class supervised model is NOT reused as an activity probability;
  binary activity is a different objective with its own temporal check.
- oracle: ex post top-K on observed future, reference only, never operative.

Pick functions never receive future values, except the oracle whose
signature makes the future input explicit.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from ml.src.data import (
    ACTIVITY_COL,
    eligible_labeled_mask,
    load_metadata,
    load_panel,
    make_preprocessor,
)

RANDOM_STATE = 7


def eligible_positions(entry: dict) -> np.ndarray:
    """Positions selectable under the mask, in stable DIVIPOLA order."""
    return np.flatnonzero(entry["eligible"])


def selection_reward(future: np.ndarray, positions: list) -> float:
    """Mean future activity over the selected positions."""
    return float(np.mean(np.asarray(future, dtype=float)[list(positions)]))


def random_pick(eligible: np.ndarray, k: int, rng: np.random.Generator) -> list:
    """Uniform picks without replacement."""
    eligible = list(eligible)
    if k > len(eligible):
        raise ValueError(f"K={k} exceeds {len(eligible)} eligible units")
    return [int(i) for i in rng.choice(eligible, size=k, replace=False)]


def fit_static_topk(train_cutoffs: dict) -> list:
    """Rank all municipalities by mean observed train activity (train only).

    The full order is returned; truncation to K happens at pick time so
    ineligible units can be skipped without losing coverage.
    """
    months = sorted(train_cutoffs)
    if not months:
        raise ValueError("no train cutoffs to build the static ranking")
    stacked = np.stack([train_cutoffs[m]["future"] for m in months])
    mean_activity = np.where(np.isnan(stacked).all(axis=0), -1.0, np.nanmean(stacked, axis=0))
    order = sorted(range(len(mean_activity)), key=lambda i: (-mean_activity[i], i))
    return [int(i) for i in order]


def static_pick(static_order: list, eligible: np.ndarray, k: int) -> list:
    """First K static-ranked positions that are eligible at this cutoff."""
    allowed = {int(i) for i in eligible}
    picks = [i for i in static_order if i in allowed][:k]
    if len(picks) < k:
        raise ValueError("static ranking covers fewer eligible units than K")
    return picks


def fit_activity_ranker(train_months: list, random_state: int = RANDOM_STATE) -> dict:
    """Train binary P(activity M>=3) on train rows only.

    Returns the preprocessor fitted on train, the classifier, the
    feature list and the train class support for the feasibility log.
    """
    panel = load_panel()
    metadata = load_metadata()
    features = list(metadata["features"])
    usable = panel[eligible_labeled_mask(panel) & panel["month"].isin(train_months)]
    usable = usable[usable[ACTIVITY_COL].notna()].copy()
    if usable.empty:
        raise ValueError("no train rows with known activity for the ranker")
    y = (usable[ACTIVITY_COL].to_numpy(dtype=float) >= 0.5).astype(int)
    preprocessor = make_preprocessor().fit(usable[features])
    clf = LogisticRegression(class_weight="balanced", max_iter=2000, random_state=random_state)
    clf.fit(preprocessor.transform(usable[features]), y)
    counts = pd.Series(y).value_counts()
    return {
        "preprocessor": preprocessor,
        "clf": clf,
        "features": features,
        "train_support": {str(k): int(v) for k, v in counts.items()},
        "train_months": sorted(train_months),
    }


def ranker_scores(bundle: dict, features_row: np.ndarray) -> np.ndarray:
    """P(activity) per municipality from past-only features (no future)."""
    proba = bundle["clf"].predict_proba(features_row)
    classes = list(bundle["clf"].classes_)
    return np.asarray(proba)[:, classes.index(1)]


def ranker_pick(bundle: dict, entry: dict, k: int) -> list:
    """Top-K eligible positions by contextual activity score."""
    scores = ranker_scores(bundle, entry["features"])
    eligible = {int(i) for i in eligible_positions(entry)}
    order = sorted(eligible, key=lambda i: (-scores[i], i))
    return [int(i) for i in order[:k]]


def oracle_pick(future: np.ndarray, eligible: np.ndarray, k: int) -> list:
    """Ex post top-K on observed future. Reference only, NOT operative."""
    values = np.asarray(future, dtype=float)
    order = sorted((int(i) for i in eligible), key=lambda i: (-values[i], i))
    return [int(i) for i in order[:k]]
