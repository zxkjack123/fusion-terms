from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_extract_respects_exclude_globs(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir(parents=True, exist_ok=True)

    # Included file contains ITER.
    (corpus_root / "a.md").write_text("ITER tokamak\n", encoding="utf-8")

    # Excluded files contain a unique token that should not appear.
    (corpus_root / "b.qa_report.md").write_text(
        "ZZZ should be excluded\n",
        encoding="utf-8",
    )
    (corpus_root / "c.autofix.md").write_text(
        "YYY should be excluded\n",
        encoding="utf-8",
    )
    (corpus_root / "d_debug.md").write_text(
        "XXX should be excluded\n",
        encoding="utf-8",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
            "--exclude-glob",
            "*.qa_report.md",
            "--exclude-glob",
            "*.autofix.md",
            "--exclude-glob",
            "*_debug.md",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    stats = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats["files_scanned"] == 1

    en = (out_dir / "candidates_en.tsv").read_text("utf-8", errors="ignore")
    assert "ITER\t" in en
    assert "ZZZ\t" not in en
    assert "YYY\t" not in en
    assert "XXX\t" not in en


def test_extract_does_not_harvest_latex_macro_names_as_en_words(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir(parents=True, exist_ok=True)

    # Include a technical token (ITER) so the extractor harvests
    # lowercase words.
    # Include LaTeX macros that should not leak into EN candidates.
    (corpus_root / "a.md").write_text(
        # NOTE: PDF->MD conversion sometimes drops the leading
        # backslash, leaving bare macro names in the text
        # (e.g. 'textrm'). Those should be filtered
        # as noise as well.
        "ITER plasma $\\omega$ $\\theta$ $\\phi_{\\mathrm{0}}$ textrm M/m\n",
        encoding="utf-8",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    en = (out_dir / "candidates_en.tsv").read_text("utf-8", errors="ignore")

    # Keep meaningful lowercase words.
    assert "plasma\t" in en

    # Do not include LaTeX macro names.
    assert "omega\t" not in en
    assert "theta\t" not in en
    assert "mathrm\t" not in en
    assert "textrm\t" not in en
