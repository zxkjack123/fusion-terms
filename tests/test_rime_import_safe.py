from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import pytest


def _write_dummy_importer(
    path: Path,
    *,
    state_file: Path,
    fail_on_import: bool = False,
) -> None:
    """Create a dummy rime_import_wordlist.py compatible script.

    Behavior:
    - always writes the requested --output payload
        - if --import is provided, mutates state_file
            (or exits non-zero if fail_on_import)
    """

    payload_literal = repr("PAYLOAD\n")
    imported_literal = repr("IMPORTED\n")
    code = f"""#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--import', dest='do_import', action='store_true')
parser.add_argument('--dict-name', default='rime_ice')
parser.add_argument('--rime-user-dir', default=None)
parser.add_argument('--include-non-cjk', action='store_true')
parser.add_argument('--no-restart-fcitx', action='store_true')
args = parser.parse_args()

# Always generate payload
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text({payload_literal}, encoding='utf-8')

if args.do_import:
    if {fail_on_import}:
        sys.exit(7)
    p = Path({str(state_file)!r})
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text({imported_literal}, encoding='utf-8')
"""

    path.write_text(code, encoding="utf-8")
    path.chmod(0o755)


def test_safe_import_dry_run_generates_payload_without_import(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    state_file = tmp_path / "rime" / "userdb_state.txt"
    importer = tmp_path / "dummy_importer.py"
    _write_dummy_importer(importer, state_file=state_file)

    out_payload = tmp_path / ".rime_import.txt"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_import_safe",
            "--input",
            str(wordlist),
            "--output",
            str(out_payload),
            "--rime-script",
            str(importer),
            "--dry-run",
            "--import",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    assert out_payload.exists()
    assert out_payload.read_text("utf-8") == "PAYLOAD\n"

    # No import performed.
    assert not state_file.exists()


def test_safe_import_backups_and_can_rollback(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    state_file = tmp_path / "rime" / "userdb_state.txt"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text("BEFORE\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    _write_dummy_importer(importer, state_file=state_file)

    out_payload = tmp_path / ".rime_import.txt"
    backup_root = tmp_path / "backups"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_import_safe",
            "--input",
            str(wordlist),
            "--output",
            str(out_payload),
            "--rime-script",
            str(importer),
            "--import",
            "--backup-path",
            str(state_file),
            "--backup-root",
            str(backup_root),
            "--backup-name",
            "test-backup",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    manifest = backup_root / "test-backup" / "manifest.json"
    assert manifest.exists()

    # State should be modified by import.
    assert state_file.read_text("utf-8") == "IMPORTED\n"

    # Rollback restores.
    p2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_import_safe",
            "--rollback",
            str(manifest),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p2.returncode == 0, f"stdout:\n{p2.stdout}\nstderr:\n{p2.stderr}"
    assert state_file.read_text("utf-8") == "BEFORE\n"

    # Manifest is well-formed.
    data = json.loads(manifest.read_text("utf-8"))
    assert data["schema_version"] == 1
    assert len(data["items"]) >= 1


def test_safe_import_auto_rolls_back_on_import_failure(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    state_file = tmp_path / "rime" / "userdb_state.txt"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text("BEFORE\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    _write_dummy_importer(importer, state_file=state_file, fail_on_import=True)

    out_payload = tmp_path / ".rime_import.txt"
    backup_root = tmp_path / "backups"

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.rime_import_safe",
            "--input",
            str(wordlist),
            "--output",
            str(out_payload),
            "--rime-script",
            str(importer),
            "--import",
            "--backup-path",
            str(state_file),
            "--backup-root",
            str(backup_root),
            "--backup-name",
            "fail-backup",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )

    assert p.returncode != 0

    # Should have rolled back to BEFORE.
    assert state_file.read_text("utf-8") == "BEFORE\n"


def test_rollback_handles_target_type_drift(tmp_path: Path) -> None:
    from pipeline.rime_import_safe import create_backup
    from pipeline.rime_import_safe import rollback_from_manifest

    backup_root = tmp_path / "backups"

    # Case 1: backup is a directory, current target drifts to a file.
    orig_dir = tmp_path / "target_dir"
    (orig_dir / "nested.txt").parent.mkdir(parents=True, exist_ok=True)
    (orig_dir / "nested.txt").write_text("DIR-BEFORE\n", encoding="utf-8")

    manifest_dir = create_backup(
        backup_root=backup_root,
        backup_name="dir-backup",
        paths=[orig_dir],
    )

    shutil.rmtree(orig_dir)
    orig_dir.write_text("NOW-A-FILE\n", encoding="utf-8")

    rollback_from_manifest(manifest_dir)
    assert orig_dir.is_dir()
    assert (orig_dir / "nested.txt").read_text("utf-8") == "DIR-BEFORE\n"

    # Case 2: backup is a file, current target drifts to a directory.
    orig_file = tmp_path / "target_file.txt"
    orig_file.write_text("FILE-BEFORE\n", encoding="utf-8")

    manifest_file = create_backup(
        backup_root=backup_root,
        backup_name="file-backup",
        paths=[orig_file],
    )

    orig_file.unlink()
    orig_file.mkdir(parents=True, exist_ok=True)
    (orig_file / "junk.txt").write_text("JUNK\n", encoding="utf-8")

    rollback_from_manifest(manifest_file)
    assert orig_file.is_file()
    assert orig_file.read_text("utf-8") == "FILE-BEFORE\n"


def test_rollback_rejects_paths_outside_home(tmp_path: Path) -> None:
    from pipeline.rime_import_safe import rollback_from_manifest

    snapshot_dir = tmp_path / "snap"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    backup_file = snapshot_dir / "etc_shadow.backup"
    backup_file.write_text("x\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "items": [
            {
                "original": "/etc/shadow",
                "backup": str(backup_file),
                "kind": "file",
            }
        ],
    }
    manifest_path = snapshot_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(SystemExit, match="protected system path"):
        rollback_from_manifest(manifest_path)


def test_now_backup_name_has_microseconds_and_is_unique() -> None:
    from pipeline.rime_import_safe import _now_backup_name

    n1 = _now_backup_name()
    n2 = _now_backup_name()

    assert re.fullmatch(r"\d{8}-\d{6}-\d{6}", n1), n1
    assert re.fullmatch(r"\d{8}-\d{6}-\d{6}", n2), n2
    assert n1 != n2


def test_create_backup_rejects_path_that_escapes_snapshot_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from pipeline.rime_import_safe import create_backup

    outside = tmp_path.parent / "outside.txt"
    outside.write_text("x\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    sneaky = Path("..") / "outside.txt"

    with pytest.raises(SystemExit, match="escapes snapshot directory"):
        create_backup(
            backup_root=tmp_path / "backups",
            backup_name="escape-test",
            paths=[sneaky],
        )


def test_safe_import_rolls_back_on_timeout(tmp_path: Path) -> None:
    """TimeoutExpired during import triggers rollback and non-zero exit."""
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n", encoding="utf-8")

    state_file = tmp_path / "rime" / "userdb_state.txt"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text("BEFORE\n", encoding="utf-8")

    # Create a dummy importer that sleeps forever (will be killed by timeout).
    importer = tmp_path / "dummy_importer_timeout.py"
    importer.write_text(
        "#!/usr/bin/env python3\n"
        "import argparse, time, sys\n"
        "from pathlib import Path\n"
        "parser = argparse.ArgumentParser()\n"
        "parser.add_argument('--input', required=True)\n"
        "parser.add_argument('--output', required=True)\n"
        "parser.add_argument('--import', dest='do_import', action='store_true')\n"
        "parser.add_argument('--dict-name', default='rime_ice')\n"
        "parser.add_argument('--rime-user-dir', default=None)\n"
        "parser.add_argument('--include-non-cjk', action='store_true')\n"
        "parser.add_argument('--no-restart-fcitx', action='store_true')\n"
        "args = parser.parse_args()\n"
        "Path(args.output).parent.mkdir(parents=True, exist_ok=True)\n"
        "Path(args.output).write_text('PAYLOAD\\n', encoding='utf-8')\n"
        "if args.do_import:\n"
        "    time.sleep(999)\n",
        encoding="utf-8",
    )
    importer.chmod(0o755)

    out_payload = tmp_path / ".rime_import.txt"
    backup_root = tmp_path / "backups"

    # Run with a wrapper that patches subprocess.run timeout to 1s.
    wrapper = tmp_path / "run_with_short_timeout.py"
    wrapper.write_text(
        "import sys, os, subprocess\n"
        f"sys.path.insert(0, {str(repo_root)!r})\n"
        "from unittest.mock import patch\n"
        "_orig_run = subprocess.run\n"
        "def _patched_run(*a, **kw):\n"
        "    if 'timeout' in kw:\n"
        "        kw['timeout'] = 1\n"
        "    return _orig_run(*a, **kw)\n"
        "with patch('subprocess.run', side_effect=_patched_run):\n"
        "    from pipeline.rime_import_safe import main\n"
        "    main()\n",
        encoding="utf-8",
    )

    p = subprocess.run(
        [
            sys.executable,
            str(wrapper),
            "--input",
            str(wordlist),
            "--output",
            str(out_payload),
            "--rime-script",
            str(importer),
            "--import",
            "--backup-path",
            str(state_file),
            "--backup-root",
            str(backup_root),
            "--backup-name",
            "timeout-backup",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert p.returncode != 0
    assert "timed out" in p.stderr
    # State should be rolled back to BEFORE.
    assert state_file.read_text("utf-8") == "BEFORE\n"
