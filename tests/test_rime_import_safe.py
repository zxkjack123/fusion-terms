from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


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
