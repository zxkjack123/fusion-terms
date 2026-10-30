#!/usr/bin/env python3
"""Gate: the proper-name ledger and the IME wordlist must agree (#T-5110).

Checks
------
1. ``LEDGER_MISSING_ENTRY``   -- a registry proper name (company/organization/
   facility preferred_zh/preferred_en) is not registered in the ledger.
2. ``LEDGER_UNKNOWN_ENTRY``   -- a ledger entry does not correspond to any
   registry proper name (stale/typo entry).
3. ``LEDGER_SECTION_OVERLAP`` -- the same string is both excluded and allowed.
4. ``WORDLIST_LEAK``          -- an EXCLUDE_FROM_IME string reached the built
   IME wordlist.
5. ``ALLOW_NOT_IN_ALLOWLIST`` -- an ALLOW_IN_IME exemption is not backed by
   ``terms/allowlist_{zh,en}.txt`` (dangling exemption).
6. ``ALLOW_NOT_IN_WORDLIST``  -- an ALLOW_IN_IME exemption is missing from the
   built wordlist (stale wordlist or broken exemption).

Usage
-----
    python3 scripts/check_proper_names_ledger.py
    python3 scripts/check_proper_names_ledger.py --self-test
    python3 scripts/check_proper_names_ledger.py \
        --terms-dir terms --wordlist dist/stage/v2026.10.30/domain_terms.txt

Exit codes: 0 = pass, 1 = violations, 2 = missing/unreadable input.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pipeline.proper_names import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
