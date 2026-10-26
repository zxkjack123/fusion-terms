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
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\tnotes\tsource\n"
            "iter\tdevice\t\tITER\tITER\tactive\t\t\n"
            "tokamak\tconcept\t托卡马克\ttokamak\t\tactive\t\t\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "ITER\titer\tabbr\tpreferred\n"
            "tokamak\ttokamak\ten\tpreferred\n"
            "托卡马克\ttokamak\tzh\tpreferred\n"
        ),
        evidence=(
            "# concept_id\tsource\tquote\tadded_by\tadded_at\n"
            "iter\thttps://www.iter.org\t\t\t2026-02-04\n"
            "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\t\t\t2026-02-04\n"
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
        concepts="BadID\tdevice\t\t\t\tactive\t\t\n",
        aliases="ITER\tBadID\tabbr\tpreferred\n",
        evidence="BadID\thttps://www.iter.org\t\t\t2026-02-04\n",
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
        concepts="iter\tdevice\t\t\t\tactive\t\t\nother\tdevice\t\t\t\tactive\t\t\n",
        aliases=("ITER\titer\tabbr\tpreferred\nITER\tother\tabbr\talias\n"),
        evidence=(
            "iter\thttps://www.iter.org\t\t\t2026-02-04\n"
            "other\thttps://example.com\t\t\t2026-02-04\n"
        ),
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
        concepts="tokamak\u200b\tconcept\t\t\t\tactive\t\t\n",
        aliases="tokamak\ttokamak\u200b\ten\tpreferred\n",
        evidence="tokamak\u200b\thttps://en.wikipedia.org/wiki/Tokamak\t\t\t2026-02-04\n",
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
        concepts="iter\tdevice\t\t\t\tactive\t\t\n",
        aliases=("ITER\titer\tabbr\tpreferred\nFigure\titer\ten\tforbidden\n"),
        evidence="iter\thttps://www.iter.org\t\t\t2026-02-04\n",
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
            "iter\tdevice\t\t\t\tactive\t\t\ntokamak\tconcept\t\t\t\tactive\t\t\n"
        ),
        aliases=("ITER\titer\tabbr\tpreferred\ntokamak\ttokamak\ten\tpreferred\n"),
        evidence="iter\thttps://www.iter.org\t\t\t2026-02-04\n",
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
        concepts="iter\tdevice\t\t\t\tactive\t\t\n",
        aliases="ITER\titer\tabbr\tpreferred\n",
        evidence="iter\tinternal:TODO:iter-source\t\t\t2026-02-04\n",
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
        concepts="iter\tdevice\t\t\t\tactive\t\t\n",
        aliases="ITER\titer\tabbr\tpreferred\n",
        evidence="iter\thttps://www.iter.org\t\t\t2026-02-04\n",
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
        concepts=(
            "iter\tdevice\t\t\t\tactive\t\t\ntokamak\tconcept\t\t\t\tactive\t\t\n"
        ),
        aliases=("ITER\titer\tabbr\tpreferred\ntokamak\ttokamak\ten\talias\n"),
        evidence=(
            "iter\thttps://www.iter.org\t\t\t2026-02-04\n"
            "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\t\t\t2026-02-04\n"
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
    "iter\tdevice\t\tITER\tITER\tactive\t\t\n"
    "tokamak\tconcept\t托卡马克\ttokamak\t\tactive\t\t\n"
)
_MINIMAL_ALIASES = (
    "ITER\titer\tabbr\tpreferred\n"
    "tokamak\ttokamak\ten\tpreferred\n"
    "托卡马克\ttokamak\tzh\tpreferred\n"
)
_MINIMAL_EVIDENCE = (
    "iter\thttps://www.iter.org\t\t\t2026-02-04\n"
    "tokamak\thttps://en.wikipedia.org/wiki/Tokamak\t\t\t2026-02-04\n"
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


# ---- registry row-shape gate, real-corpus anchored (T4973 T0.9 / T0.10) ----
# The fixtures under tests/fixtures/registry/ hold rows copied byte-for-byte from
# the pre-fix corpus (`git show f90e903:terms/registry/concepts.tsv`), so these
# cases assert on real malformed rows rather than a hand-written lookalike.

_REGISTRY_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "registry"


def _fixture_rows(name: str) -> list[str]:
    """Read one fixture file and return its non-empty lines, verbatim."""
    path = _REGISTRY_FIXTURES_DIR / name
    rows = path.read_text(encoding="utf-8").splitlines()
    assert rows, f"fixture is missing or empty: {path}"
    return rows


def _tables_from_concept_rows(concept_rows: list[str]) -> tuple[str, str, str]:
    """Build (concepts, aliases, evidence) text around real fixture concept rows.

    The generated alias/evidence tables are syntactically canonical, so the only
    remaining defect in the registry is the malformed concepts row itself.
    """
    concept_ids = [row.split("\t")[0] for row in concept_rows]
    concepts = "".join(f"{row}\n" for row in concept_rows)
    aliases = "".join(f"{cid}\t{cid}\ten\tpreferred\n" for cid in concept_ids)
    evidence = "".join(
        f"{cid}\thttps://example.org/{cid}\t\t\t2026-02-04\n" for cid in concept_ids
    )
    return concepts, aliases, evidence


def test_validate_registry_rejects_shifted_category_row(tmp_path: Path) -> None:
    """Pre-fix rows shifted left, so the category slot holds the Chinese name."""
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    concepts, aliases, evidence = _tables_from_concept_rows(
        _fixture_rows("pre_fix_concepts_shift.tsv")
    )
    _write_registry_tables(
        terms_dir, concepts=concepts, aliases=aliases, evidence=evidence
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "invalid category" in combined
    # The offending value comes from the real corpus row, not from this test.
    assert repr("能源安全") in combined


def test_validate_registry_rejects_six_column_row(tmp_path: Path) -> None:
    """Pre-fix 6-column rows must fail on the column count, not silently pass."""
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    concepts, aliases, evidence = _tables_from_concept_rows(
        _fixture_rows("pre_fix_concepts_sixcol.tsv")
    )
    _write_registry_tables(
        terms_dir, concepts=concepts, aliases=aliases, evidence=evidence
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "expected 8 columns" in combined
    # The shape check must win over the category whitelist (6-col rows also carry
    # a non-whitelisted category value).
    assert "invalid category" not in combined


def test_validate_registry_rejects_four_column_evidence(tmp_path: Path) -> None:
    """Evidence rows must have exactly 5 columns (4-column shape pre-dates T0.8)."""
    repo_root = Path(__file__).resolve().parents[1]
    terms_dir = _setup_terms(tmp_path)
    # Drop the trailing ``added_at`` column from the canonical evidence table.
    four_col_rows = [row.rsplit("\t", 1)[0] for row in _MINIMAL_EVIDENCE.splitlines()]
    assert all(row.count("\t") == 3 for row in four_col_rows)

    _write_registry_tables(
        terms_dir,
        concepts=_MINIMAL_CONCEPTS,
        aliases=_MINIMAL_ALIASES,
        evidence="".join(f"{row}\n" for row in four_col_rows),
    )

    p = _run_validator(repo_root, terms_dir)
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "expected 5 columns" in combined
