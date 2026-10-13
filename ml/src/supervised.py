"""Supervised benchmark: dummy, weighted logistic, resampling, forest.

SMOTE and RandomOverSampler need imbalanced-learn and are skipped with
an explicit reason when it is missing or the support is insufficient.
Resampling is applied to the training split only, inside a pipeline.
"""

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.preprocessing import StandardScaler

from ml.src.data import feature_type_groups, make_preprocessor

RANDOM_STATE = 7
SMOTE_K = 5


def _try_imblearn():
    try:
        from imblearn.over_sampling import SMOTE, RandomOverSampler
        from imblearn.pipeline import Pipeline as ImbPipeline

        return RandomOverSampler, SMOTE, ImbPipeline, None
    except ImportError as exc:
        return None, None, None, f"imbalanced-learn not installed ({exc})"


def _flat_pre_steps() -> list:
    """Imputation and scaling as plain steps (imblearn forbids nested pipes)."""
    return [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]


def _smote_feasibility(x_train: pd.DataFrame, y_train: pd.Series) -> tuple:
    """Decide whether SMOTE is valid on this training split."""
    groups = feature_type_groups(x_train)
    if groups["categorical"]:
        return False, f"categorical features present: {groups['categorical']}"
    counts = y_train.value_counts()
    smallest = int(counts.min())
    if smallest < 2:
        return False, f"smallest class has {smallest} rows; SMOTE needs >= 2"
    neighbors = min(SMOTE_K, smallest - 1)
    note = (
        f"k_neighbors={neighbors} for smallest class n={smallest}; "
        f"binary-like columns {groups['boolean_like']} are interpolated "
        "without rounding (documented caveat)"
    )
    return True, note


def candidate_models(
    x_train: pd.DataFrame, y_train: pd.Series, random_state: int = RANDOM_STATE
) -> list:
    """Return (name, estimator-or-None, skip_reason-or-None, note)."""
    ros, smote_cls, imb_pipeline, imb_error = _try_imblearn()
    candidates = [
        (
            "A_dummy_majority",
            SkPipeline(
                [("pre", make_preprocessor()), ("clf", DummyClassifier(strategy="most_frequent"))]
            ),
            None,
            "no-learning baseline",
        ),
        (
            "B_logreg_balanced",
            SkPipeline(
                [
                    ("pre", make_preprocessor()),
                    (
                        "clf",
                        LogisticRegression(
                            class_weight="balanced", max_iter=2000, random_state=random_state
                        ),
                    ),
                ]
            ),
            None,
            "class_weight=balanced, no resampling",
        ),
    ]
    if ros is None:
        candidates.append(("C_ros_logreg", None, imb_error, ""))
    else:
        candidates.append(
            (
                "C_ros_logreg",
                imb_pipeline(
                    [
                        *_flat_pre_steps(),
                        ("sampler", ros(random_state=random_state)),
                        ("clf", LogisticRegression(max_iter=2000, random_state=random_state)),
                    ]
                ),
                None,
                "RandomOverSampler on train only; plain LR",
            )
        )
    feasible, note = _smote_feasibility(x_train, y_train)
    if smote_cls is None:
        candidates.append(("D_smote_logreg", None, imb_error, ""))
    elif not feasible:
        candidates.append(("D_smote_logreg", None, note, ""))
    else:
        counts = y_train.value_counts()
        neighbors = min(SMOTE_K, int(counts.min()) - 1)
        candidates.append(
            (
                "D_smote_logreg",
                imb_pipeline(
                    [
                        *_flat_pre_steps(),
                        ("sampler", smote_cls(k_neighbors=neighbors, random_state=random_state)),
                        ("clf", LogisticRegression(max_iter=2000, random_state=random_state)),
                    ]
                ),
                None,
                note + "; plain LR, never combined with class weights",
            )
        )
    candidates.append(
        (
            "E_rf_balanced",
            SkPipeline(
                [
                    ("pre", make_preprocessor()),
                    (
                        "clf",
                        RandomForestClassifier(
                            n_estimators=300,
                            min_samples_leaf=5,
                            class_weight="balanced_subsample",
                            n_jobs=-1,
                            random_state=random_state,
                        ),
                    ),
                ]
            ),
            None,
            "no tuning; reasonable default under time pressure",
        )
    )
    return candidates
