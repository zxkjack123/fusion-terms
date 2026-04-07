"""Test B12: rollback_from_manifest skips items with missing keys instead of crashing."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest


def test_missing_original_key_skips_item(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Manifest item missing 'original' is skipped with a warning, not a KeyError."""
    from pipeline.rime_import_safe import rollback_from_manifest

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)

        # Create a valid backup file to satisfy rollback for the good item
        good_orig = td_p / "good_orig.txt"
        good_orig.write_text("original", encoding="utf-8")
        good_bak = td_p / "good_backup.txt"
        good_bak.write_text("backup-content", encoding="utf-8")

        manifest = {
            "items": [
                # Bad item: missing "original"
                {"backup": str(good_bak)},
                # Good item
                {"original": str(good_orig), "backup": str(good_bak)},
            ]
        }
        manifest_path = td_p / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        # Should NOT raise KeyError
        rollback_from_manifest(manifest_path)

        captured = capsys.readouterr()
        assert "skipping manifest item with missing key" in captured.err


def test_missing_backup_key_skips_item(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Manifest item missing 'backup' is skipped with a warning."""
    from pipeline.rime_import_safe import rollback_from_manifest

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)

        manifest = {
            "items": [
                {"original": str(td_p / "something.txt")},
            ]
        }
        manifest_path = td_p / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        rollback_from_manifest(manifest_path)

        captured = capsys.readouterr()
        assert "skipping manifest item with missing key" in captured.err
