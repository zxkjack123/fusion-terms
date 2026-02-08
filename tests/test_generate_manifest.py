from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from pipeline.generate_manifest import generate_manifest


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def test_generate_manifest_basic(tmp_path: Path) -> None:
    root = tmp_path

    domain_terms = """\
    # comment (should be ignored)
    tokamak
    3D\u6253\u5370

    tokamak  
    \n
    \u8054\u9501\u7cfb\u7edf
    """

    (root / "domain_terms.txt").write_text(domain_terms, encoding="utf-8")
    (root / "registry_exports.json").write_text("{}\n", encoding="utf-8")

    # Note: counts-from omitted -> falls back to computing from domain_terms.txt
    m = generate_manifest(
        root=root,
        version="v2026.02.08",
        commit="a" * 40,
        generated_at="2026-02-08T03:21:00Z",
        files=["domain_terms.txt", "registry_exports.json"],
    )

    d = m.as_dict()
    assert d["schema_version"] == 1
    assert d["version"] == "v2026.02.08"
    assert d["commit"] == ("a" * 40)
    assert d["generated_at"] == "2026-02-08T03:21:00Z"

    # terms are de-duplicated + stripped; comment/blank ignored
    assert d["counts"]["total"] == 3
    assert d["counts"]["zh"] == 2
    assert d["counts"]["en"] == 1

    sha = d["sha256"]
    assert sha["domain_terms.txt"] == _sha256_bytes((root / "domain_terms.txt").read_bytes())
    assert sha["registry_exports.json"] == _sha256_bytes((root / "registry_exports.json").read_bytes())


def test_generate_manifest_normalizes_generated_at_plus00(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")

    m = generate_manifest(
        root=root,
        version="v2026.02.08",
        commit="b" * 40,
        generated_at="2026-02-08T03:21:00+00:00",
        files=["domain_terms.txt"],
    )
    assert m.generated_at.endswith("Z")


def test_generate_manifest_rejects_non_utc_generated_at(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        generate_manifest(
            root=root,
            version="v2026.02.08",
            commit="c" * 40,
            generated_at="2026-02-08T03:21:00+08:00",
            files=["domain_terms.txt"],
        )


def test_generate_manifest_rejects_escape_root(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        generate_manifest(
            root=root,
            version="v2026.02.08",
            commit="d" * 40,
            generated_at="2026-02-08T03:21:00Z",
            files=["../domain_terms.txt"],
        )


def test_generate_manifest_accepts_counts_from_build_stats(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")

    stats = {
        "counts": {
            "total": 1066,
            "zh": 881,
            "en": 185,
        }
    }
    (root / "domain_terms_build_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    m = generate_manifest(
        root=root,
        version="v2026.02.08",
        commit="e" * 40,
        generated_at="2026-02-08T03:21:00Z",
        files=["domain_terms.txt"],
    )

    assert m.counts["total"] == 1066
    assert m.counts["zh"] == 881
    assert m.counts["en"] == 185


def test_generate_manifest_fails_fast_when_file_missing(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        generate_manifest(
            root=root,
            version="v2026.02.08",
            commit="f" * 40,
            generated_at="2026-02-08T03:21:00Z",
            files=["domain_terms.txt", "nope.txt"],
        )


def test_generate_manifest_rejects_unusable_counts_from(tmp_path: Path) -> None:
    root = tmp_path
    (root / "domain_terms.txt").write_text("tokamak\n", encoding="utf-8")
    (root / "bad_stats.json").write_text("{}\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        generate_manifest(
            root=root,
            version="v2026.02.08",
            commit="0" * 40,
            generated_at="2026-02-08T03:21:00Z",
            files=["domain_terms.txt"],
            counts_from="bad_stats.json",
        )
