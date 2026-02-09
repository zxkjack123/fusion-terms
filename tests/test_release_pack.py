from __future__ import annotations

import tarfile
from pathlib import Path

import pytest

from pipeline.release_pack import build_release_pack
from pipeline.verify_release_contract import verify_release_contract


def _write_terms_dir(terms_dir: Path) -> None:
    terms_dir.mkdir(parents=True, exist_ok=True)

    (terms_dir / "allowlist_zh.txt").write_text("3D打印\n联锁系统\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("tokamak\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("# alias\tpreferred\n", encoding="utf-8")


def test_release_pack_builds_tar_and_verifies_after_extract(tmp_path: Path) -> None:
    terms_dir = tmp_path / "terms"
    _write_terms_dir(terms_dir)

    config = tmp_path / "config.toml"
    config.write_text("\n", encoding="utf-8")

    stage_dir = tmp_path / "stage"
    tar_path = tmp_path / "fusion-terms-artifacts-v2026.02.09.tar.gz"

    res = build_release_pack(
        tag="v2026.02.09",
        stage_dir=stage_dir,
        tar_path=tar_path,
        terms_dir=terms_dir,
        config=config,
        commit="a" * 40,
        generated_at="2026-02-09T00:00:00Z",
        include_terms_sources=True,
        include_registry_sources=False,
        include_registry_exports=False,
        force=False,
    )

    assert res.tar_path.exists()

    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(tar_path, mode="r:gz") as tf:
        # Use tarfile's safety filter to avoid future default changes.
        tf.extractall(path=extract_dir, filter="data")

    # Contract verify should pass in a git-less extracted directory.
    verify_release_contract(root=extract_dir)

    # Sanity: top-level expected files exist.
    assert (extract_dir / "domain_terms.txt").exists()
    assert (extract_dir / "fusion_terms_manifest.json").exists()


def test_release_pack_refuses_existing_stage_without_force(tmp_path: Path) -> None:
    terms_dir = tmp_path / "terms"
    _write_terms_dir(terms_dir)

    config = tmp_path / "config.toml"
    config.write_text("\n", encoding="utf-8")

    stage_dir = tmp_path / "stage"
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / "junk.txt").write_text("x\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        build_release_pack(
            tag="v2026.02.09",
            stage_dir=stage_dir,
            tar_path=tmp_path / "out.tar.gz",
            terms_dir=terms_dir,
            config=config,
            commit="a" * 40,
            generated_at="2026-02-09T00:00:00Z",
            include_terms_sources=False,
            include_registry_sources=False,
            include_registry_exports=False,
            force=False,
        )
