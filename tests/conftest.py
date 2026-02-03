from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repository root is importable so tests can import the in-repo
# `pipeline` package when pytest's import mechanics differ across environments.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
