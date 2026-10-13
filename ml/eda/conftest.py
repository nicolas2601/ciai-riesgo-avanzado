"""Allow both pytest entry points to find the repository namespace packages."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
