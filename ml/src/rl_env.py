"""Gymnasium environment for municipal prioritization with budget K.

One episode = one monthly cutoff. The agent picks K distinct
municipalities (Discrete(N), masked) before seeing any outcome.
Intermediate rewards are zero; the terminal reward is the mean of
``target_actividad_m3_mes_siguiente`` over the selected set, read from
real future records only after the K-th pick.

The reward measures observed future seismic activity at selected
sites. It is NOT damage, official risk, or avoided causal impact.

Municipalities without future coverage can never be selected: a
cutoff is usable only when every eligible municipality has a known
future activity value, and ineligible units are always masked out.
"""

from typing import ClassVar

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from ml.src.data import (
    ACTIVITY_COL,
    eligible_labeled_mask,
    load_metadata,
    load_panel,
    make_preprocessor,
)

BUDGET_K = 5


def _divipola_order(zone_ids) -> list:
    """Stable municipal order by zero-padded DIVIPOLA code."""
    return sorted(str(z).zfill(5) for z in zone_ids)


def build_cutoff_data(months: list, train_months: list, budget_k: int = BUDGET_K) -> dict:
    """Build per-cutoff arrays for the environment.

    The preprocessor is fitted on train-month rows only, then applied
    to every requested month. A cutoff is kept only when all eligible
    municipalities have a known future activity value; otherwise it is
    excluded (never filled with zero activity).
    """
    panel = load_panel()
    metadata = load_metadata()
    features = [c for c in metadata["features"]]
    mask_labeled = eligible_labeled_mask(panel)
    train_rows = panel[mask_labeled & panel["month"].isin(train_months)]
    if train_rows.empty:
        raise ValueError("no train rows to fit the preprocessor")
    preprocessor = make_preprocessor().fit(train_rows[features])
    cutoffs = {}
    order = _divipola_order(panel["zone_id"].unique())
    for month in sorted(months):
        frame = panel[panel["month"] == month].copy()
        frame["zone_id"] = frame["zone_id"].astype(str).str.zfill(5)
        must_cover = frame["eligible"].astype(str).str.lower().isin(["true", "1"])
        if not bool(frame.loc[must_cover, ACTIVITY_COL].notna().all()):
            continue
        frame = frame.set_index("zone_id").reindex(order).reset_index()
        eligible = (
            frame["eligible"].astype(str).str.lower().isin(["true", "1"]).to_numpy()
            & frame[ACTIVITY_COL].notna().to_numpy()
        )
        if int(eligible.sum()) < int(budget_k):
            continue
        obs_features = preprocessor.transform(frame[features]).astype(np.float32)
        cutoffs[month] = {
            "zone_ids": order,
            "features": obs_features,
            "eligible": eligible,
            "future": frame[ACTIVITY_COL].to_numpy(dtype=float),
            "n_features": len(features),
        }
    if not cutoffs:
        raise ValueError("no usable cutoffs with full future coverage")
    return cutoffs


class SeismicPrioritizationEnv(gym.Env):
    """Select K distinct municipalities per monthly cutoff.

    Observation = [flattened cutoff features | selected mask | budget].
    Future targets never enter the observation or intermediate infos.
    """

    metadata: ClassVar[dict] = {"render_mode": None}

    def __init__(self, cutoffs: dict, budget_k: int = BUDGET_K):
        super().__init__()
        if not cutoffs:
            raise ValueError("cutoffs must not be empty")
        self.cutoffs = cutoffs
        self.cutoff_months = sorted(cutoffs)
        self.budget_k = int(budget_k)
        sample = cutoffs[self.cutoff_months[0]]
        self.zone_ids = list(sample["zone_ids"])
        self.n_municipalities = len(self.zone_ids)
        self.n_features = int(sample["n_features"])
        if self.budget_k < 1:
            raise ValueError(f"budget K must be >= 1, got {budget_k}")
        for month in self.cutoff_months:
            entry = cutoffs[month]
            if list(entry["zone_ids"]) != self.zone_ids:
                raise ValueError(f"municipal order changed at {month}")
            if int(entry["eligible"].sum()) < self.budget_k:
                raise ValueError(f"cutoff {month} has fewer eligible units than K")
        obs_dim = self.n_municipalities * self.n_features
        obs_dim += self.n_municipalities + 1
        self.action_space = spaces.Discrete(self.n_municipalities)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )
        self._month = None
        self._entry = None
        self._selected = np.zeros(self.n_municipalities, dtype=bool)

    def action_masks(self) -> np.ndarray:
        """Eligible and not-yet-selected municipalities."""
        return self._entry["eligible"] & ~self._selected

    def _observation(self) -> np.ndarray:
        budget = np.array(
            [(self.budget_k - int(self._selected.sum())) / self.budget_k],
            dtype=np.float32,
        )
        return np.concatenate(
            [self._entry["features"].ravel(), self._selected.astype(np.float32), budget]
        ).astype(np.float32)

    def reset(self, *, seed=None, options=None):
        """Start a new episode on a reproducible random cutoff."""
        super().reset(seed=seed)
        if options is not None and "cutoff" in options:
            month = options["cutoff"]
            if month not in self.cutoffs:
                raise ValueError(f"unknown cutoff {month}")
        else:
            month = self.cutoff_months[int(self.np_random.integers(len(self.cutoffs)))]
        self._month = month
        self._entry = self.cutoffs[month]
        self._selected = np.zeros(self.n_municipalities, dtype=bool)
        return self._observation(), {"cutoff": month}

    def step(self, action):
        """Apply one pick; terminal reward only after K valid picks."""
        action = int(action)
        if not self.action_space.contains(action) or not self.action_masks()[action]:
            return (
                self._observation(),
                0.0,
                False,
                False,
                {
                    "cutoff": self._month,
                    "invalid_action": True,
                },
            )
        self._selected[action] = True
        done = bool(int(self._selected.sum()) >= self.budget_k)
        reward = 0.0
        if done:
            reward = float(np.mean(self._entry["future"][self._selected]))
        return (
            self._observation(),
            reward,
            done,
            False,
            {
                "cutoff": self._month,
                "n_selected": int(self._selected.sum()),
            },
        )

    def selected_zones(self) -> list:
        """DIVIPOLA codes selected so far, in selection order of positions."""
        return [self.zone_ids[i] for i in np.flatnonzero(self._selected).tolist()]

    def current_cutoff(self) -> str:
        """Active cutoff month label."""
        return self._month
