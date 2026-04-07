"""Test B11: forbidden/deprecated leak check is case-insensitive."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


def test_case_insensitive_leak_detected() -> None:
    """'NBI' in allowlist + 'nbi' in forbidden → detected as leak."""
    from pipeline import validate_registry

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        reg_dir = td_p / "registry"
        reg_dir.mkdir()

        # Minimal valid registry files (no headers — _iter_tsv_rows processes all lines)
        (reg_dir / "concepts.tsv").write_text(
            "nbi-heating\theating\n", encoding="utf-8"
        )
        (reg_dir / "aliases.tsv").write_text(
            "nbi\tnbi-heating\ten\tforbidden\n"
            "NBI\tnbi-heating\ten\talias\n"
            "NBI Heating\tnbi-heating\ten\tpreferred\n",
            encoding="utf-8",
        )
        (reg_dir / "evidence.tsv").write_text(
            "nbi-heating\tmanual\ttest\n",
            encoding="utf-8",
        )

        # Allowlists: NBI in uppercase
        (td_p / "allowlist_zh.txt").write_text("", encoding="utf-8")
        (td_p / "allowlist_en.txt").write_text("NBI\n", encoding="utf-8")

        # We need to intercept the forbidden_or_deprecated set.
        # Rather than re-create the entire alias parsing, let's mock it.
        # The forbidden set comes from aliases with status in {forbidden, deprecated}.
        # The validate function builds it from aliases_rows.
        # Since we set up valid files, just let it run naturally.

        with pytest.raises(SystemExit, match="forbidden/deprecated"):
            validate_registry.validate_registry(td_p)


def test_exact_case_match_still_detected() -> None:
    """Same case in both sets is still detected (regression guard)."""
    from pipeline import validate_registry

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        reg_dir = td_p / "registry"
        reg_dir.mkdir()

        (reg_dir / "concepts.tsv").write_text(
            "test-concept\tgeneral\n", encoding="utf-8"
        )
        (reg_dir / "aliases.tsv").write_text(
            "badterm\ttest-concept\ten\tforbidden\n"
            "BadTerm Preferred\ttest-concept\ten\tpreferred\n",
            encoding="utf-8",
        )
        (reg_dir / "evidence.tsv").write_text(
            "test-concept\tmanual\ttest\n",
            encoding="utf-8",
        )

        (td_p / "allowlist_zh.txt").write_text("", encoding="utf-8")
        (td_p / "allowlist_en.txt").write_text("badterm\n", encoding="utf-8")

        with pytest.raises(SystemExit, match="forbidden/deprecated"):
            validate_registry.validate_registry(td_p)
