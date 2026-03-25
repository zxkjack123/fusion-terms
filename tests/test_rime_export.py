from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_dummy_importer(path: Path, log_path: Path) -> None:
    code = f"""#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--dict-name', default=None)
parser.add_argument('--rime-user-dir', default=None)
parser.add_argument('--include-non-cjk', action='store_true')
parser.add_argument('--no-restart-fcitx', action='store_true')
parser.add_argument('--import', dest='do_import', action='store_true')
args = parser.parse_args()

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text('ITER\tITER\t100\\n', encoding='utf-8')
Path({str(log_path)!r}).write_text(json.dumps(vars(args), ensure_ascii=False), encoding='utf-8')
"""
    path.write_text(code, encoding="utf-8")
    path.chmod(0o755)


def test_rime_export_writes_output(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    importer_log = tmp_path / "importer_log.json"
    _write_dummy_importer(importer, importer_log)

    output = tmp_path / ".rime_import.txt"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_export",
            "--input",
            str(wordlist),
            "--output",
            str(output),
            "--rime-script",
            str(importer),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )

    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
    assert output.exists()
    assert "ITER\tITER\t100" in output.read_text("utf-8")


def test_rime_export_respects_config_dict_name(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    importer_log = tmp_path / "importer_log.json"
    _write_dummy_importer(importer, importer_log)

    config = tmp_path / "config.toml"
    config.write_text(
        "\n".join(
            [
                "[rime]",
                "dict_name = \"test_dict\"",
                f"import_script = \"{importer}\"",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    output = tmp_path / ".rime_import.txt"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_export",
            "--config",
            str(config),
            "--input",
            str(wordlist),
            "--output",
            str(output),
            "--import",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )

    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
    logged = importer_log.read_text("utf-8")
    assert '"dict_name": "test_dict"' in logged


def test_rime_export_cli_overrides_config(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    importer_log = tmp_path / "importer_log.json"
    _write_dummy_importer(importer, importer_log)

    config = tmp_path / "config.toml"
    config.write_text(
        "\n".join(
            [
                "[rime]",
                "dict_name = \"test_dict\"",
                f"import_script = \"{importer}\"",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    output = tmp_path / ".rime_import.txt"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_export",
            "--config",
            str(config),
            "--input",
            str(wordlist),
            "--output",
            str(output),
            "--dict-name",
            "override_dict",
            "--import",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )

    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
    logged = importer_log.read_text("utf-8")
    assert '"dict_name": "override_dict"' in logged
