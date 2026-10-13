"""Per-municipality policy architecture for MaskablePPO.

The reference flat MLP must discover from scratch which input block
belongs to which action index. This variant bakes the correspondence
in: the observation is reshaped to (municipalities, features), a
shared encoder scores every municipality, and those scores are the
action logits. Permuting municipality blocks permutes the logits
(tested). The critic pools the shared embeddings plus the budget.

Nothing here changes reward, K, eligibility or cutoffs.
"""

import numpy as np
import torch as th
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from torch import nn


class PerMunicipalityPolicy(MaskableActorCriticPolicy):
    """Shared per-municipality encoder with explicit index correspondence."""

    def __init__(
        self,
        observation_space,
        action_space,
        lr_schedule,
        n_municipalities: int,
        n_features: int,
        hidden_dim: int = 32,
        **kwargs,
    ):
        kwargs.setdefault("net_arch", [hidden_dim])
        super().__init__(observation_space, action_space, lr_schedule, **kwargs)
        self.n_municipalities = int(n_municipalities)
        self.n_features = int(n_features)
        self.hidden_dim = int(hidden_dim)
        self.muni_encoder = nn.Sequential(
            nn.Linear(self.n_features, self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.Tanh(),
        )
        self.score_head = nn.Linear(self.hidden_dim + 1, 1)
        self.value_head = nn.Sequential(
            nn.Linear(self.hidden_dim + 1, self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim, 1),
        )

    def _structured_heads(self, obs: th.Tensor):
        batch = obs.shape[0]
        n_muni, n_feat = self.n_municipalities, self.n_features
        muni = obs[:, : n_muni * n_feat].reshape(batch, n_muni, n_feat)
        tail = obs[:, n_muni * n_feat :]
        selected = tail[:, :n_muni].unsqueeze(-1)
        budget = tail[:, n_muni:]
        embed = self.muni_encoder(muni)
        scores = self.score_head(th.cat([embed, selected], dim=-1)).squeeze(-1)
        pooled = embed.mean(dim=1)
        values = self.value_head(th.cat([pooled, budget], dim=-1))
        return scores, values

    def _distribution_from_scores(self, scores: th.Tensor, action_masks=None):
        distribution = self.action_dist.proba_distribution(action_logits=scores)
        if action_masks is not None:
            distribution.apply_masking(action_masks)
        return distribution

    def forward(self, obs, deterministic=False, action_masks=None):
        scores, values = self._structured_heads(obs)
        distribution = self._distribution_from_scores(scores, action_masks)
        actions = distribution.get_actions(deterministic=deterministic)
        log_prob = distribution.log_prob(actions)
        actions = actions.reshape((-1, *self.action_space.shape))
        return actions, values, log_prob

    def get_distribution(self, obs, action_masks=None):
        scores, _ = self._structured_heads(obs)
        return self._distribution_from_scores(scores, action_masks)

    def evaluate_actions(self, obs, actions, action_masks=None):
        scores, values = self._structured_heads(obs)
        distribution = self._distribution_from_scores(scores, action_masks)
        log_prob = distribution.log_prob(actions)
        entropy = distribution.entropy()
        return values, log_prob, entropy

    def predict_values(self, obs):
        _, values = self._structured_heads(obs)
        return values


def clip_cutoff_features(cutoffs: dict, bound: float = 5.0) -> dict:
    """Clip scaled features to [-bound, bound]; fixed rule, no fitting."""
    clipped = {}
    for month, entry in cutoffs.items():
        features = np.clip(entry["features"], -bound, bound).astype(np.float32)
        clipped[month] = dict(entry, features=features)
    return clipped
