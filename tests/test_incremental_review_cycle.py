from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, (
        "command failed\n"
        f"cwd: {cwd}\n"
        f"cmd: {cmd!r}\n"
        f"stdout:\n{p.stdout}\n"
        f"stderr:\n{p.stderr}\n"
    )
    return p


def test_incremental_extract_plus_review_pack_makes_second_review_near_zero(
    tmp_path: Path,
) -> None:
    """Stage 3 acceptance helper:

    - incremental extract on unchanged corpus should skip all files
    - review_pack diff should be empty on second run

    This makes incremental review cost measurably small for no-change runs.
    """

    repo_root = Path(__file__).resolve().parents[1]
    fixture_corpus = repo_root / "tests" / "fixtures" / "corpus"

    corpus_root = tmp_path / "corpus"
    shutil.copytree(fixture_corpus, corpus_root)

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Run extraction with incremental + filtered outputs enabled.
    _run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
            "--incremental",
            "--min-count-en",
            "1",
            "--min-count-zh",
            "1",
        ],
        cwd=repo_root,
    )

    stats1 = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats1["cache"]["enabled"] is True
    assert stats1["cache"]["incremental"] is True
    assert (out_dir / "extract_delta.json").exists()

    # First review_pack run: baseline missing -> everything is new.
    _run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
        ],
        cwd=repo_root,
    )
    summary1 = json.loads((out_dir / "review_pack" / "summary.json").read_text("utf-8"))
    assert summary1["counts"]["new_en"] > 0
    assert summary1["counts"]["new_zh"] > 0

    # Second extraction: unchanged corpus -> should skip all files.
    _run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
            "--incremental",
            "--min-count-en",
            "1",
            "--min-count-zh",
            "1",
        ],
        cwd=repo_root,
    )

    stats2 = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats2["cache"]["processed_files"] == 0
    assert stats2["cache"]["misses"] == 0
    assert stats2["cache"]["hits"] > 0

    # Second review_pack: should be empty diffs (baseline was updated on first run).
    _run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
        ],
        cwd=repo_root,
    )
    summary2 = json.loads((out_dir / "review_pack" / "summary.json").read_text("utf-8"))
    assert summary2["counts"]["new_zh"] == 0
    assert summary2["counts"]["removed_zh"] == 0
    assert summary2["counts"]["new_en"] == 0
    assert summary2["counts"]["removed_en"] == 0
