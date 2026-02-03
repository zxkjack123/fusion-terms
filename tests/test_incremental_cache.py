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


def _parse_tsv_counts(path: Path) -> dict[str, int]:
    lines = path.read_text("utf-8", errors="ignore").splitlines()
    assert lines and lines[0].startswith("term\tcount\t")
    out: dict[str, int] = {}
    for ln in lines[1:]:
        if not ln.strip():
            continue
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        term = parts[0].strip()
        try:
            cnt = int(parts[1])
        except ValueError:
            continue
        if term:
            out[term] = cnt
    return out


def test_incremental_cache_skips_unchanged_and_preserves_counts(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_corpus = repo_root / "tests" / "fixtures" / "corpus"

    corpus_root = tmp_path / "corpus"
    shutil.copytree(fixture_corpus, corpus_root)

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

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
        ],
        cwd=repo_root,
    )

    stats1 = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats1["cache"]["enabled"] is True
    assert stats1["cache"]["incremental"] is True
    assert (out_dir / "extract_delta.json").exists()

    en_counts_1 = _parse_tsv_counts(out_dir / "candidates_en.tsv")
    zh_counts_1 = _parse_tsv_counts(out_dir / "candidates_zh.tsv")

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
        ],
        cwd=repo_root,
    )

    stats2 = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats2["cache"]["hits"] > 0
    assert stats2["cache"]["processed_files"] == 0
    assert stats2["cache"]["misses"] == 0

    en_counts_2 = _parse_tsv_counts(out_dir / "candidates_en.tsv")
    zh_counts_2 = _parse_tsv_counts(out_dir / "candidates_zh.tsv")

    assert en_counts_2 == en_counts_1
    assert zh_counts_2 == zh_counts_1


def test_incremental_cache_reprocesses_changed_file_and_writes_delta(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_corpus = repo_root / "tests" / "fixtures" / "corpus"

    corpus_root = tmp_path / "corpus"
    shutil.copytree(fixture_corpus, corpus_root)

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

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
        ],
        cwd=repo_root,
    )

    # Modify one file: add a new acronym token on two lines.
    target = corpus_root / "sample.md"
    assert target.exists()
    target.write_text(
        target.read_text("utf-8", errors="ignore")
        + "\nSPARC is a compact tokamak concept.\n"
        + "\nSPARC uses high-field magnets.\n",
        encoding="utf-8",
    )

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
        ],
        cwd=repo_root,
    )

    stats = json.loads((out_dir / "extract_stats.json").read_text("utf-8"))
    assert stats["cache"]["misses"] >= 1
    assert stats["cache"]["processed_files"] >= 1
    assert stats["cache"]["hits"] >= 1

    en_counts = _parse_tsv_counts(out_dir / "candidates_en.tsv")
    assert en_counts.get("SPARC") == 2

    delta = json.loads((out_dir / "extract_delta.json").read_text("utf-8"))
    added = delta["terms"]["en"]["added"]
    assert any(d.get("term") == "SPARC" and d.get("delta") == 2 for d in added)
