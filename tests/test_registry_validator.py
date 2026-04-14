from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_registry_tables(
    terms_dir: Path,
    *,
    concepts: str,
    aliases: str,
    evidence: str,
    definitions: str = "",
) -> None:
    reg = terms_dir / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "concepts.tsv").write_text(concepts, encoding="utf-8")
    (reg / "aliases.tsv").write_text(aliases, encoding="utf-8")
    (reg / "evidence.tsv").write_text(evidence, encoding="utf-8")
    if definitions:
        (reg / "definitions.tsv").write_text(definitions, encoding="utf-8")


def _run_validator(
    repo_root: Path, terms_dir: Path
) -> subprocess.CompletedProcess[str]:
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
        aliases=("ITER\titer\tabbr\tpreferred\nITER\tother\tabbr\talias\n"),
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
        aliases=("ITER\titer\tabbr\tpreferred\nFigure\titer\ten\tforbidden\n"),
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
        concepts=("iter\tdevice\ntokamak\tconcept\n"),
        aliases=("ITER\titer\tabbr\tpreferred\ntokamak\ttokamak\ten\tpreferred\n"),
        evidence="iter\thttps://www.iter.org\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "concepts without evidence rows" in combined
    assert "'tokamak'" in combined
    assert ":0:" not in combined
    assert ":1:" in combined


def test_validate_registry_rejects_internal_todo_evidence(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="iter\tdevice\n",
        aliases="ITER\titer\tabbr\tpreferred\n",
        evidence="iter\tinternal:TODO:iter-source\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "placeholder evidence source not allowed" in combined


def test_validate_registry_accepts_url_evidence(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="iter\tdevice\n",
        aliases="ITER\titer\tabbr\tpreferred\n",
        evidence="iter\thttps://www.iter.org\n",
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"


def test_validate_registry_rejects_concept_without_preferred_alias(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts=("iter\tdevice\ntokamak\tconcept\n"),
        aliases=("ITER\titer\tabbr\tpreferred\ntokamak\ttokamak\ten\talias\n"),
        evidence=(
            "iter\thttps://www.iter.org\n"
            "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\n"
        ),
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "concepts without preferred alias" in combined
    assert "'tokamak'" in combined
    assert ":0:" not in combined
    assert ":1:" in combined


# ---- definitions.tsv validation tests (repo-hardening-2026-04-14) ----

_MINIMAL_CONCEPTS = (
    "iter\tdevice\t\tITER\tITER\tactive\n"
    "tokamak\tconcept\t托卡马克\ttokamak\t\tactive\n"
)
_MINIMAL_ALIASES = (
    "ITER\titer\tabbr\tpreferred\n"
    "tokamak\ttokamak\ten\tpreferred\n"
    "托卡马克\ttokamak\tzh\tpreferred\n"
)
_MINIMAL_EVIDENCE = (
    "iter\thttps://www.iter.org\n"
    "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\n"
)


def _setup_terms(tmp_path: Path) -> Path:
    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("ITER\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("", encoding="utf-8")
    return terms_dir


def test_definitions_rejects_wrong_column_count(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    _write_registry_tables(
        terms_dir,
        concepts=_MINIMAL_CONCEPTS,
        aliases=_MINIMAL_ALIASES,
        evidence=_MINIMAL_EVIDENCE,
        definitions="iter\ten\tA fusion reactor\n",  # 3 columns, missing source
    )
    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "expected 4 columns" in combined


def test_definitions_rejects_empty_source(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    _write_registry_tables(
        terms_dir,
        concepts=_MINIMAL_CONCEPTS,
        aliases=_MINIMAL_ALIASES,
        evidence=_MINIMAL_EVIDENCE,
        definitions="iter\ten\tA fusion reactor\t\n",  # empty source
    )
    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "source is empty" in combined


def test_definitions_rejects_duplicate_concept_lang(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    _write_registry_tables(
        terms_dir,
        concepts=_MINIMAL_CONCEPTS,
        aliases=_MINIMAL_ALIASES,
        evidence=_MINIMAL_EVIDENCE,
        definitions=(
            "iter\ten\tA fusion reactor\tIAEA\n"
            "iter\ten\tAnother definition\tIAEA\n"  # duplicate (iter, en)
        ),
    )
    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "duplicate definition" in combined
