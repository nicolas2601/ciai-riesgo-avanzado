#!/usr/bin/env bash
# Publish model artifacts as a GitHub release. Usage: scripts/publish_release.sh v0.1.0
set -euo pipefail
tag="${1:?usage: publish_release.sh <tag>}"
files=(artifacts/ml/selected_model.joblib artifacts/ml/rl/ppo_policy.zip artifacts/ml/metrics.json)
for f in "${files[@]}"; do
  size=$(stat -c %s "$f")
  if (( size > 100 * 1024 * 1024 )); then echo "too large: $f" >&2; exit 1; fi
done
sums=$(sha256sum "${files[@]}")
gh release create "$tag" "${files[@]}" --title "$tag" --notes "SHA-256:
\`\`\`
$sums
\`\`\`"
