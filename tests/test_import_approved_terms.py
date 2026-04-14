"""Test scripts/import_approved_terms.py with mock approved entries."""
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import pytest


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
        "tokamak\thttps://example.com\t\t\t2026-01-01\n",
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


def test_import_dry_run(mock_registry: Path, mock_diff: Path, monkeypatch):
    """Dry run should report counts but not modify files."""
    monkeypatch.chdir(mock_registry)

    result = subprocess.run(
        [
            "python3", "-m", "scripts.import_approved_terms",
            "--diff", str(mock_diff),
            "--source", "TEST-source",
            "--evidence-url", "https://test.example.com",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(mock_registry),
    )
    # Script uses REGISTRY_DIR = Path("terms/registry") relative, so cwd matters
    # But we can't use -m from tmp_path. Use subprocess with explicit path instead.
    # Let's run it directly.
    script = Path(__file__).resolve().parent.parent / "scripts" / "import_approved_terms.py"
    result = subprocess.run(
        [
            "python3", str(script),
            "--diff", str(mock_diff),
            "--source", "TEST-source",
            "--evidence-url", "https://test.example.com",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(mock_registry),
    )
    assert result.returncode == 0, result.stderr
    assert "New concepts: 3" in result.stdout
    assert "DRY RUN" in result.stdout

    # Files should be unmodified
    concepts_text = (mock_registry / "terms" / "registry" / "concepts.tsv").read_text()
    assert concepts_text.count("\n") == 3  # header + 2 existing + trailing


def test_import_appends_approved(mock_registry: Path, mock_diff: Path):
    """Actual import should append 3 new concepts (plasma, divertor, blanket).

    tokamak is approved but already exists → skipped.
    stellarator is rejected → skipped.
    """
    script = Path(__file__).resolve().parent.parent / "scripts" / "import_approved_terms.py"
    result = subprocess.run(
        [
            "python3", str(script),
            "--diff", str(mock_diff),
            "--source", "TEST-source",
            "--evidence-url", "https://test.example.com",
        ],
        capture_output=True,
        text=True,
        cwd=str(mock_registry),
    )
    assert result.returncode == 0, result.stderr
    assert "New concepts: 3" in result.stdout

    concepts = (mock_registry / "terms" / "registry" / "concepts.tsv").read_text("utf-8")
    aliases = (mock_registry / "terms" / "registry" / "aliases.tsv").read_text("utf-8")
    evidence = (mock_registry / "terms" / "registry" / "evidence.tsv").read_text("utf-8")

    # Verify concept rows
    concept_lines = [ln for ln in concepts.splitlines()
                     if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(concept_lines) == 5  # 2 existing + 3 new

    # Verify new concepts have correct format (8 columns)
    new_lines = concept_lines[2:]
    for line in new_lines:
        parts = line.split("\t")
        assert len(parts) == 8, f"Expected 8 columns, got {len(parts)}: {line}"
        assert parts[5] == "active"
        assert parts[7] == "TEST-source"

    # Verify aliases (2 existing + 3 en + 3 zh = 8)
    alias_lines = [ln for ln in aliases.splitlines()
                   if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(alias_lines) == 8

    # Verify evidence (1 existing + 3 new = 4)
    evidence_lines = [ln for ln in evidence.splitlines()
                      if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(evidence_lines) == 4

    # Verify no rejected entry
    assert "stellarator" not in concepts

    # Verify tokamak not duplicated
    assert concepts.count("tokamak\tconcept") == 1


def test_import_skips_existing_alias(mock_registry: Path, tmp_path: Path):
    """If term matches an existing alias (case-insensitive), skip it."""
    diff_path = tmp_path / "diff2.tsv"
    diff_path.write_text(
        "# term\tstatus\tmatched_concept_id\tdefinition\n"
        "TOKAMAK\tapproved\t\tShould be skipped\n"
        "new-device\tapproved\t\tBrand new\n",
        encoding="utf-8",
    )

    script = Path(__file__).resolve().parent.parent / "scripts" / "import_approved_terms.py"
    result = subprocess.run(
        [
            "python3", str(script),
            "--diff", str(diff_path),
            "--source", "TEST",
            "--evidence-url", "test",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(mock_registry),
    )
    assert result.returncode == 0, result.stderr
    assert "New concepts: 1" in result.stdout
    assert "SKIP" in result.stdout
