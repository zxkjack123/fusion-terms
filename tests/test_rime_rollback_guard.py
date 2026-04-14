"""Test B9: rollback_from_manifest failure is caught and both errors are reported."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import pytest


def test_rollback_failure_still_exits_nonzero(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When importer fails AND rollback fails, exit code is importer's and stderr has both."""
    from pipeline import rime_import_safe

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        manifest_path = td_p / "manifest.json"
        manifest_path.write_text(json.dumps({"items": []}), encoding="utf-8")

        # Create dummy files the argparser expects to exist
        input_file = td_p / "input.txt"
        input_file.write_text("test\ttest\n", encoding="utf-8")
        script_file = td_p / "rime_script.py"
        script_file.write_text("", encoding="utf-8")

        gen_ok = subprocess.CompletedProcess(
            args=["fake"], returncode=0, stdout="", stderr=""
        )
        imp_fail = subprocess.CompletedProcess(
            args=["fake"], returncode=42, stdout="", stderr="importer exploded"
        )

        with (
            mock.patch.object(
                rime_import_safe,
                "_run_importer_v2",
                side_effect=[gen_ok, imp_fail],
            ),
            mock.patch.object(
                rime_import_safe,
                "rollback_from_manifest",
                side_effect=OSError("disk full during rollback"),
            ),
            mock.patch.object(
                rime_import_safe,
                "create_backup",
                return_value=manifest_path,
            ),
            mock.patch(
                "sys.argv",
                [
                    "rime_import_safe",
                    "--import",
                    "--input",
                    str(input_file),
                    "--output",
                    str(td_p / "output.txt"),
                    "--rime-script",
                    str(script_file),
                    "--backup-path",
                    td,
                ],
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                rime_import_safe.main()

            assert exc_info.value.code == 42

        captured = capsys.readouterr()
        assert "rollback also failed" in captured.err
        assert "disk full during rollback" in captured.err


def test_rollback_success_still_exits_nonzero(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When importer fails but rollback succeeds, exit code is still importer's."""
    from pipeline import rime_import_safe

    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        manifest_path = td_p / "manifest.json"
        manifest_path.write_text(json.dumps({"items": []}), encoding="utf-8")

        input_file = td_p / "input.txt"
        input_file.write_text("test\ttest\n", encoding="utf-8")
        script_file = td_p / "rime_script.py"
        script_file.write_text("", encoding="utf-8")

        gen_ok = subprocess.CompletedProcess(
            args=["fake"], returncode=0, stdout="", stderr=""
        )
        imp_fail = subprocess.CompletedProcess(
            args=["fake"], returncode=7, stdout="", stderr="import failed"
        )

        with (
            mock.patch.object(
                rime_import_safe,
                "_run_importer_v2",
                side_effect=[gen_ok, imp_fail],
            ),
            mock.patch.object(
                rime_import_safe,
                "rollback_from_manifest",
                return_value=None,
            ),
            mock.patch.object(
                rime_import_safe,
                "create_backup",
                return_value=manifest_path,
            ),
            mock.patch(
                "sys.argv",
                [
                    "rime_import_safe",
                    "--import",
                    "--input",
                    str(input_file),
                    "--output",
                    str(td_p / "output.txt"),
                    "--rime-script",
                    str(script_file),
                    "--backup-path",
                    td,
                ],
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                rime_import_safe.main()

            assert exc_info.value.code == 7
