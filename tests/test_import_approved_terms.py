"""Test scripts/import_approved_terms.py with mock entries."""
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "import_approved_terms.py"


@pytest.fixture()
def mock_registry(tmp_path: Path):
    """Create a minimal registry in tmp_path for testing."""
    reg = tmp_path / "terms" / "registry"
    reg.mkdir(parents=True)

    concepts = reg / "concepts.tsv"
    concepts.write_text(
        "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\tnotes\tsource\n"
        "tokamak\tconcept\t托卡马克\ttokamak\t\tactive\t\tcorpus\n"
        "iter\tconcept\t国际热核聚变实验堆\tITER\tITER\tactive\t\tcorpus\n",
        encoding="utf-8",
    )

    aliases = reg / "aliases.tsv"
    aliases.write_text(
        "# alias\tconcept_id\tlang\tkind\tcomment\n"
        "tokamak\ttokamak\ten\tpreferred\t\n"
        "ITER\titer\tabbr\tpreferred\t\n",
        encoding="utf-8",
    )

    evidence = reg / "evidence.tsv"
    evidence.write_text(
        "# concept_id\tsource\tquote\tadded_by\tadded_at\n"
        "tokamak\thttps://example.com\t\t\t2026-01-01\n"
        "iter\thttps://iter.org\t\t\t2026-01-01\n",
        encoding="utf-8",
    )

    definitions = reg / "definitions.tsv"
    definitions.write_text(
        "# concept_id\tlang\tdefinition\tsource\n",
        encoding="utf-8",
    )

    return tmp_path


@pytest.fixture()
def mock_diff(tmp_path: Path):
    """Create a diff TSV with 3 approved, 1 rejected, 1 existing (skip)."""
    diff_path = tmp_path / "test_diff.tsv"
    diff_path.write_text(
        textwrap.dedent("""\
        # term\tstatus\tmatched_concept_id\tdefinition\tzh
        plasma\tapproved\t\tIonized gas\t等离子体
        divertor\tapproved\t\tDevice component for exhaust\t偏滤器
        blanket\tapproved\t\tShielding and breeding component\t包层
        stellarator\trejected\t\t\t仿星器
        tokamak\tapproved\ttokamak\tAlready exists\t托卡马克
        """),
        encoding="utf-8",
    )
    return diff_path


def _run_import(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd),
    )


def _data_lines(path: Path) -> list[str]:
    return [ln for ln in path.read_text("utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]


def test_import_dry_run(mock_registry: Path, mock_diff: Path):
    """Dry run should report counts but not modify files."""
    result = _run_import([
        "--diff", str(mock_diff),
        "--source", "TEST-source",
        "--evidence-url", "https://test.example.com",
        "--dry-run",
    ], cwd=mock_registry)
    assert result.returncode == 0, result.stderr
    assert "New concepts:" in result.stdout
    assert "3" in result.stdout
    assert "DRY RUN" in result.stdout

    # Files should be unmodified
    concepts_text = (mock_registry / "terms" / "registry" / "concepts.tsv").read_text()
    assert concepts_text.count("\n") == 3  # header + 2 existing + trailing


def test_import_appends_approved(mock_registry: Path, mock_diff: Path):
    """Actual import should append 3 new concepts (plasma, divertor, blanket).

    tokamak is approved but already exists → definition only.
    stellarator is rejected → skipped.
    """
    result = _run_import([
        "--diff", str(mock_diff),
        "--source", "TEST-source",
        "--evidence-url", "https://test.example.com",
    ], cwd=mock_registry)
    assert result.returncode == 0, result.stderr

    reg = mock_registry / "terms" / "registry"

    # Verify concept rows: 2 existing + 3 new = 5
    concept_lines = _data_lines(reg / "concepts.tsv")
    assert len(concept_lines) == 5

    # Verify new concepts have correct format (8 columns)
    for line in concept_lines[2:]:
        parts = line.split("\t")
        assert len(parts) == 8, f"Expected 8 columns, got {len(parts)}: {line}"
        assert parts[5] == "active"
        assert parts[7] == "TEST-source"

    # Verify aliases (2 existing + 3 en + 3 zh = 8)
    assert len(_data_lines(reg / "aliases.tsv")) == 8

    # Verify evidence (2 existing + 3 new = 5)
    assert len(_data_lines(reg / "evidence.tsv")) == 5

    # Verify definitions written for all 3 new + 1 existing-with-def = 4
    def_lines = _data_lines(reg / "definitions.tsv")
    assert len(def_lines) == 4

    # Verify no rejected entry
    assert "stellarator" not in (reg / "concepts.tsv").read_text()

    # Verify tokamak not duplicated in concepts
    assert (reg / "concepts.tsv").read_text().count("tokamak\tconcept") == 1


def test_import_skips_existing_alias(mock_registry: Path, tmp_path: Path):
    """If term matches existing concept_id, definition-only; no definition → skip."""
    diff_path = tmp_path / "diff2.tsv"
    diff_path.write_text(
        "# term\tstatus\tmatched_concept_id\tdefinition\n"
        "TOKAMAK\tapproved\t\t\n"
        "new-device\tapproved\t\tBrand new\n",
        encoding="utf-8",
    )

    result = _run_import([
        "--diff", str(diff_path),
        "--source", "TEST",
        "--evidence-url", "test",
        "--dry-run",
    ], cwd=mock_registry)
    assert result.returncode == 0, result.stderr
    assert "New concepts:" in result.stdout
    # TOKAMAK has no definition and concept_id exists → skipped
    assert "SKIP" in result.stdout


def test_import_all_with_exists(mock_registry: Path, tmp_path: Path):
    """--import-all: 'exists' entries get definitions only, 'new' get full import."""
    diff_path = tmp_path / "diff_all.tsv"
    diff_path.write_text(
        "# term\tstatus\tmatched_concept_id\tdefinition\n"
        "tokamak\texists\ttokamak\tA toroidal magnetic confinement device\n"
        "stellarator\tnew\t\tAlternative magnetic confinement\n",
        encoding="utf-8",
    )

    result = _run_import([
        "--diff", str(diff_path),
        "--source", "TEST",
        "--evidence-url", "test",
        "--import-all",
    ], cwd=mock_registry)
    assert result.returncode == 0, result.stderr

    reg = mock_registry / "terms" / "registry"

    # tokamak: exists → no new concept, just definition
    concept_lines = _data_lines(reg / "concepts.tsv")
    assert len(concept_lines) == 3  # 2 existing + 1 new (stellarator)
    assert any("stellarator" in ln for ln in concept_lines)

    # Definitions: tokamak def + stellarator def = 2
    def_lines = _data_lines(reg / "definitions.tsv")
    assert len(def_lines) == 2
    assert any("tokamak" in ln for ln in def_lines)
    assert any("stellarator" in ln for ln in def_lines)


def test_import_conflict_with_map(mock_registry: Path, tmp_path: Path):
    """--conflict-map resolves conflict entries to existing concept_ids."""
    diff_path = tmp_path / "diff_conflict.tsv"
    diff_path.write_text(
        "# term\tstatus\tmatched_concept_id\tdefinition\n"
        "Q\tconflict\tenergy-gain|safety-factor\tFusion gain ratio\n"
        "plasma\tnew\t\tIonized gas\n",
        encoding="utf-8",
    )

    # Add energy-gain to mock registry so conflict-map works
    concepts_path = mock_registry / "terms" / "registry" / "concepts.tsv"
    with open(concepts_path, "a", encoding="utf-8") as f:
        f.write("energy-gain\tconcept\t能量增益\tenergy gain\tQ\tactive\t\tcorpus\n")
    aliases_path = mock_registry / "terms" / "registry" / "aliases.tsv"
    with open(aliases_path, "a", encoding="utf-8") as f:
        f.write("energy gain\tenergy-gain\ten\tpreferred\t\n")
    evidence_path = mock_registry / "terms" / "registry" / "evidence.tsv"
    with open(evidence_path, "a", encoding="utf-8") as f:
        f.write("energy-gain\thttps://example.com\t\t\t2026-01-01\n")

    result = _run_import([
        "--diff", str(diff_path),
        "--source", "TEST",
        "--evidence-url", "test",
        "--import-all",
        "--conflict-map", "Q=energy-gain",
    ], cwd=mock_registry)
    assert result.returncode == 0, result.stderr

    reg = mock_registry / "terms" / "registry"

    # Q conflict → definition for energy-gain; plasma → new concept
    def_lines = _data_lines(reg / "definitions.tsv")
    assert any("energy-gain" in ln for ln in def_lines)
    assert any("plasma" in ln for ln in def_lines)
