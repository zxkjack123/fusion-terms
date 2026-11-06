from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


ALIAS = "物理溅射"
CONCEPT = "physical-sputtering"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_projection_export(out_dir: Path) -> None:
    root = _repo_root()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.export_registry",
            "--terms-dir",
            "terms",
            "--out-dir",
            str(out_dir),
            "--query-expansions",
            "--translation-dict",
            "--substitutions",
            "--no-vale",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"projection export failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )


def _physical_rows() -> list[list[str]]:
    aliases_path = _repo_root() / "terms" / "registry" / "aliases.tsv"
    return [
        line.split("\t")
        for line in aliases_path.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#") and line.split("\t")[0] == ALIAS
    ]


def test_m3_a_prime_removes_historical_alias() -> None:
    """The adjudicated 2026-11-04 A' mapping must remove the old target."""
    assert not any(row[1] == "sputtering" for row in _physical_rows())


def test_m3_a_prime_adds_exact_preferred_row() -> None:
    assert (
        sum(row[:4] == [ALIAS, CONCEPT, "zh", "preferred"] for row in _physical_rows())
        == 1
    )


def test_m3_a_prime_keeps_single_concept_ownership() -> None:
    assert len({row[1] for row in _physical_rows()}) == 1


def test_m3_a_prime_projection_values(tmp_path: Path) -> None:
    _run_projection_export(tmp_path)

    query = json.loads((tmp_path / "query_expansions.json").read_text(encoding="utf-8"))
    translation = json.loads(
        (tmp_path / "translation_dict.json").read_text(encoding="utf-8")
    )
    substitutions = (tmp_path / "terminology_substitutions.tsv").read_text(
        encoding="utf-8"
    )

    # The translation dictionary stores the concept's preferred English label;
    # alias_index is the stable concept-id projection.
    assert translation["zh2en"][ALIAS] == "physical sputtering"
    assert query["alias_index"][ALIAS] == CONCEPT
    assert ALIAS in query["concepts"][CONCEPT]["all_terms"]
    assert ALIAS not in query["concepts"]["sputtering"]["all_terms"]
    assert translation["en2zh"]["physical sputtering"] == ALIAS
    assert translation["zh2en"]["溅射"] == "sputtering"
    assert "物理溅射率\t物理溅射\t" in substitutions


def test_exporter_rejects_multi_concept_alias(tmp_path: Path) -> None:
    from pipeline.export_registry import export_query_expansions

    registry = tmp_path / "terms" / "registry"
    registry.mkdir(parents=True)
    (registry / "concepts.tsv").write_text(
        "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\tnotes\tsource\n"
        "a\tcat\t甲\talpha\t\tactive\t\tsrc\n"
        "b\tcat\t乙\tbeta\t\tactive\t\tsrc\n",
        encoding="utf-8",
    )
    (registry / "aliases.tsv").write_text(
        "# alias\tconcept_id\tlang\tkind\tcomment\n"
        "甲\ta\tzh\tpreferred\t\n"
        "乙\tb\tzh\tpreferred\t\n"
        "冲突\ta\tzh\talias\t\n"
        "冲突\tb\tzh\talias\t\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit, match="maps to multiple concepts"):
        export_query_expansions(terms_dir=tmp_path / "terms", out_dir=tmp_path / "out")
