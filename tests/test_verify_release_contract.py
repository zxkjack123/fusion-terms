from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.generate_manifest import generate_manifest
from pipeline.verify_release_contract import verify_release_contract


def _write_manifest(
    root: Path, *, sha_files: list[str], counts_from: str | None = None
) -> None:
    m = generate_manifest(
        root=root,
        version="v2026.02.09",
        commit="a" * 40,
        generated_at="2026-02-09T00:00:00Z",
        files=sha_files,
        counts_from=counts_from,
        repo_root=None,
    )
    (root / "fusion_terms_manifest.json").write_text(
        json.dumps(m.as_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_verify_release_contract_ok(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n3D打印\n", encoding="utf-8")
    _write_manifest(root, sha_files=["domain_terms.txt"])

    # Should not raise.
    verify_release_contract(root=root)


def test_verify_release_contract_rejects_whitespace_term(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\nion source\n", encoding="utf-8")
    _write_manifest(root, sha_files=["domain_terms.txt"])

    with pytest.raises(SystemExit):
        verify_release_contract(root=root)


def test_verify_release_contract_rejects_invisible_control(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text(
        "tokamak\nzero\u200bwidth\n", encoding="utf-8"
    )
    _write_manifest(root, sha_files=["domain_terms.txt"])

    with pytest.raises(SystemExit):
        verify_release_contract(root=root)


def test_verify_release_contract_rejects_duplicate(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\ntokamak\n", encoding="utf-8")
    _write_manifest(root, sha_files=["domain_terms.txt"])

    with pytest.raises(SystemExit):
        verify_release_contract(root=root)


def test_verify_release_contract_rejects_sha256_mismatch(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n3D打印\n", encoding="utf-8")
    _write_manifest(root, sha_files=["domain_terms.txt"])

    manifest_path = root / "fusion_terms_manifest.json"
    data = json.loads(manifest_path.read_text("utf-8"))
    data["sha256"]["domain_terms.txt"] = "0" * 64
    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit):
        verify_release_contract(root=root)


def test_verify_release_contract_rejects_counts_mismatch(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n3D打印\n", encoding="utf-8")

    # force counts from build stats to be wrong
    (root / "domain_terms_build_stats.json").write_text(
        json.dumps({"counts": {"total": 123, "zh": 1, "en": 1}}, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    _write_manifest(
        root,
        sha_files=["domain_terms.txt"],
        counts_from="domain_terms_build_stats.json",
    )

    with pytest.raises(SystemExit):
        verify_release_contract(root=root)
