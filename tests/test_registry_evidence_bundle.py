import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

import scripts.registry_evidence_bundle as bundle_module

from scripts.registry_evidence_bundle import (
    CHECKS,
    CODE_FILES,
    DATA_FILES,
    MAX_EVIDENCE_BYTES,
    make_snapshot,
    verify_regular_inventory,
    inventory,
    parse_result,
    result_key,
    sha256,
    validate_manifest,
)


def test_systemexit_text_and_w0_deferred_warning_are_preserved():
    failure = parse_result("validate_registry", 1, "", "file.tsv:2: bad", False, "w0")
    assert failure["failure_detail"] == "file.tsv:2: bad"
    audit = {
        "w0_is_clean": True,
        "is_clean": False,
        "non_zero_metrics": {"definitions.en_boilerplate": 2},
        "deferred_w1_metrics": {"definitions.en_boilerplate": 2},
    }
    result = parse_result("registry_row_audit", 0, json.dumps(audit), "", False, "w0")
    assert result["status"] == "pass"
    assert "deferred:definitions.en_boilerplate=2" in result["warnings"]


def test_real_bad_tsv_preserves_validator_systemexit_text(tmp_path: Path):
    snapshot = tmp_path / "snapshot"
    for name in DATA_FILES:
        destination = snapshot / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(name, destination)
    concepts = snapshot / "terms/registry/concepts.tsv"
    concepts.write_text(concepts.read_text().replace("concept\t", "bad\t", 1))
    result = subprocess.run(
        [
            "python3",
            "-m",
            "pipeline.validate_registry",
            "--terms-dir",
            str(snapshot / "terms"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "invalid category" in result.stderr


def test_dirty_code_in_tmp_copy_changes_inventory_without_touching_workspace(
    tmp_path: Path,
):
    source = Path("scripts/registry_evidence_bundle.py")
    copied = tmp_path / "scripts/registry_evidence_bundle.py"
    copied.parent.mkdir()
    shutil.copy2(source, copied)
    before = hashlib.sha256(copied.read_bytes()).hexdigest()
    copied.write_text(copied.read_text() + "\n# dirty copy\n")
    assert before != hashlib.sha256(copied.read_bytes()).hexdigest()


def test_missing_phase_or_tampered_evidence_cannot_reuse(tmp_path: Path):
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "schema": 3,
                "profile": "w0",
                "incomplete": False,
                "batch_status": "pass",
                "evidence": [],
            }
        )
    )
    with pytest.raises(SystemExit, match="incomplete"):
        validate_manifest(tmp_path)


def test_tampered_top_level_success_cannot_reuse(tmp_path: Path):
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    for name in DATA_FILES + CODE_FILES:
        destination = snapshot / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(name, destination)
    results = []
    evidence = []
    for phase in ("baseline", "batch"):
        phase_dir = tmp_path / phase
        phase_dir.mkdir()
        phase_results = []
        for check in CHECKS:
            stdout = (
                "file.tsv:2: broken\n"
                if check == "validate_registry"
                else json.dumps({"w0_is_clean": False, "non_zero_metrics": {"bad": 1}})
            )
            stderr = "failure\n"
            (phase_dir / f"{check}.stdout").write_text(stdout)
            (phase_dir / f"{check}.stderr").write_text(stderr)
            result = parse_result(check, 1, stdout, stderr, False, "w0")
            phase_results.append(result)
            evidence.append(
                {
                    "phase": phase,
                    "check_id": check,
                    "returncode": 1,
                    "incomplete": False,
                    "stdout_sha256": sha256(phase_dir / f"{check}.stdout"),
                    "stderr_sha256": sha256(phase_dir / f"{check}.stderr"),
                }
            )
        results.append(phase_results)
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "schema": 3,
                "profile": "w0",
                "incomplete": False,
                "batch_status": "pass",
                "snapshot_hashes": inventory(snapshot, DATA_FILES + CODE_FILES),
                "same_structured_result": True,
                "baseline": [result_key(r) for r in results[0]],
                "batch": [result_key(r) for r in results[1]],
                "evidence": evidence,
            }
        )
    )
    with pytest.raises(SystemExit, match="failed"):
        validate_manifest(tmp_path)


def _write_passing_bundle(
    tmp_path: Path,
    *,
    profile: str = "w0",
    same: bool = True,
    fingerprint: str = "fp-good",
) -> Path:
    snapshot = tmp_path / "snapshot"
    for name in DATA_FILES + CODE_FILES:
        destination = snapshot / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(name, destination)
    if profile == "w0":
        audit = {
            "w0_is_clean": True,
            "is_clean": False,
            "non_zero_metrics": {},
            "deferred_w1_metrics": {"definitions.en_boilerplate": 2},
        }
    else:
        audit = {
            "w0_is_clean": True,
            "is_clean": True,
            "non_zero_metrics": {},
            "deferred_w1_metrics": {},
        }
    outputs = {
        "validate_registry": ("registry OK\n", ""),
        "registry_row_audit": (json.dumps(audit, sort_keys=True) + "\n", ""),
    }
    results = []
    evidence = []
    for phase in ("baseline", "batch"):
        phase_dir = tmp_path / phase
        phase_dir.mkdir()
        phase_results = []
        for check in CHECKS:
            stdout, stderr = outputs[check]
            (phase_dir / f"{check}.stdout").write_text(stdout)
            (phase_dir / f"{check}.stderr").write_text(stderr)
            result = parse_result(check, 0, stdout, stderr, False, profile)
            phase_results.append(result)
            evidence.append(
                {
                    "phase": phase,
                    "check_id": check,
                    "returncode": 0,
                    "incomplete": False,
                    "stdout_sha256": sha256(phase_dir / f"{check}.stdout"),
                    "stderr_sha256": sha256(phase_dir / f"{check}.stderr"),
                }
            )
        results.append(phase_results)
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "schema": 3,
                "profile": profile,
                "gate": "expect-clean" if profile == "w0" else "expect-clean-all",
                "execution_fingerprint": fingerprint,
                "incomplete": False,
                "batch_status": "pass" if same else "fail",
                "snapshot_hashes": inventory(snapshot, DATA_FILES + CODE_FILES),
                "same_structured_result": same,
                "baseline": [result_key(r) for r in results[0]],
                "batch": [result_key(r) for r in results[1]],
                "evidence": evidence,
            },
            sort_keys=True,
        )
    )
    return tmp_path


def test_reuse_refuses_missing_evidence_file(tmp_path: Path):
    bundle = _write_passing_bundle(tmp_path)
    (bundle / "baseline/validate_registry.stdout").unlink()
    with pytest.raises(
        SystemExit, match="missing evidence path: baseline/validate_registry.stdout"
    ):
        validate_manifest(bundle)


def test_hard_resource_limit_is_not_a_prefix_contract():
    assert MAX_EVIDENCE_BYTES > 64 * 1024
    assert set(CHECKS) == {"validate_registry", "registry_row_audit"}
    assert "pipeline/common.py" in CODE_FILES


def test_snapshot_symlink_is_rejected(tmp_path: Path):
    link = tmp_path / "terms/registry/concepts.tsv"
    link.parent.mkdir(parents=True)
    link.symlink_to((Path("terms/registry/concepts.tsv")).resolve())
    with pytest.raises(SystemExit, match="snapshot path"):
        verify_regular_inventory(tmp_path, ("terms/registry/concepts.tsv",))


def test_fingerprint_changes_on_data_and_checker_edits(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    for name in DATA_FILES + CODE_FILES:
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(name, destination)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    monkeypatch.setattr(bundle_module, "ROOT", root)
    first, _ = bundle_module.execution_fingerprint()
    snapshot_before = make_snapshot(tmp_path / "before")
    data = root / "terms/registry/concepts.tsv"
    data.write_text(data.read_text() + "\n")
    second, _ = bundle_module.execution_fingerprint()
    assert second != first
    checker = root / "scripts/registry_row_audit.py"
    checker.write_text(checker.read_text() + "\n# changed checker\n")
    third, _ = bundle_module.execution_fingerprint()
    assert third != second
    assert make_snapshot(tmp_path / "after") != snapshot_before


def test_reuse_refuses_changed_fingerprint(tmp_path: Path):
    bundle = _write_passing_bundle(tmp_path)
    validate_manifest(bundle, "fp-good")
    with pytest.raises(SystemExit, match="execution fingerprint changed"):
        validate_manifest(bundle, "fp-bad")


def test_reuse_refuses_tampered_evidence_file(tmp_path: Path):
    bundle = _write_passing_bundle(tmp_path)
    evidence = bundle / "batch/registry_row_audit.stdout"
    evidence.write_text(evidence.read_text() + "tamper")
    with pytest.raises(SystemExit, match="tampered evidence batch/registry_row_audit"):
        validate_manifest(bundle)


def test_same_audit_scope_differs_between_w0_and_all():
    audit = json.dumps(
        {
            "w0_is_clean": True,
            "is_clean": False,
            "non_zero_metrics": {"definitions.en_boilerplate": 2},
            "deferred_w1_metrics": {"definitions.en_boilerplate": 2},
        }
    )
    w0 = parse_result("registry_row_audit", 0, audit, "", False, "w0")
    assert w0["status"] == "pass"
    assert "deferred:definitions.en_boilerplate=2" in w0["warnings"]
    assert (
        parse_result("registry_row_audit", 0, audit, "", False, "all")["status"]
        == "fail"
    )


def test_failed_comparison_cannot_reuse(tmp_path: Path):
    bundle = _write_passing_bundle(tmp_path, same=False)
    with pytest.raises(SystemExit, match="comparison summary mismatch"):
        validate_manifest(bundle)
