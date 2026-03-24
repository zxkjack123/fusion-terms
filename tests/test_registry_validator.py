from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_registry_tables(terms_dir: Path, *, concepts: str, aliases: str, evidence: str) -> None:
    reg = terms_dir / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "concepts.tsv").write_text(concepts, encoding="utf-8")
    (reg / "aliases.tsv").write_text(aliases, encoding="utf-8")
    (reg / "evidence.tsv").write_text(evidence, encoding="utf-8")


def _run_validator(repo_root: Path, terms_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.validate_registry",
            "--terms-dir",
            str(terms_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )


def test_validate_registry_ok_minimal(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # allowlists are needed for the forbidden/deprecated leak check.
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("ITER\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "iter\tdevice\t\tITER\tITER\tactive\n"
            "tokamak\tconcept\t托卡马克\ttokamak\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "ITER\titer\tabbr\tpreferred\n"
            "tokamak\ttokamak\ten\tpreferred\n"
            "托卡马克\ttokamak\tzh\tpreferred\n"
        ),
        evidence=(
            "# concept_id\tsource\n"
            "iter\thttps://www.iter.org\n"
            "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\n"
        ),
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
    assert "registry OK" in (p.stdout or "")


def test_validate_registry_rejects_invalid_concept_id(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="BadID\tdevice\n",
        aliases="ITER\tBadID\tabbr\tpreferred\n",
        evidence="BadID\thttps://www.iter.org\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "invalid concept_id" in combined


def test_validate_registry_rejects_alias_mapping_conflict(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="iter\tdevice\nother\tdevice\n",
        aliases=(
            "ITER\titer\tabbr\tpreferred\n"
            "ITER\tother\tabbr\talias\n"
        ),
        evidence="iter\thttps://www.iter.org\nother\thttps://example.com\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "maps to multiple concept_ids" in combined


def test_validate_registry_rejects_control_chars(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    # ZERO WIDTH SPACE in concept_id
    _write_registry_tables(
        terms_dir,
        concepts="tokamak\u200b\tconcept\n",
        aliases="tokamak\ttokamak\u200b\ten\tpreferred\n",
        evidence="tokamak\u200b\thttps://en.wikipedia.org/wiki/Tokamak\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "control/invisible" in combined
    assert "U+200B" in combined


def test_validate_registry_rejects_forbidden_in_allowlist(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("Figure\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="iter\tdevice\n",
        aliases=(
            "ITER\titer\tabbr\tpreferred\n"
            "Figure\titer\ten\tforbidden\n"
        ),
        evidence="iter\thttps://www.iter.org\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "forbidden/deprecated" in combined
    assert "'Figure'" in combined


def test_validate_registry_rejects_missing_evidence(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts=(
            "iter\tdevice\n"
            "tokamak\tconcept\n"
        ),
        aliases=(
            "ITER\titer\tabbr\tpreferred\n"
            "tokamak\ttokamak\ten\tpreferred\n"
        ),
        evidence="iter\thttps://www.iter.org\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "concepts without evidence rows" in combined
    assert "'tokamak'" in combined
