from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_extract_writes_filtered_outputs_and_respects_min_count(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "tests" / "fixtures" / "corpus"

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
            "--max-files",
            "100",
            "--min-count-en",
            "2",
            "--min-count-zh",
            "2",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    raw_en = (out_dir / "candidates_en.tsv").read_text("utf-8", errors="ignore").splitlines()
    filt_en = (out_dir / "candidates_en.filtered.tsv").read_text("utf-8", errors="ignore").splitlines()

    assert raw_en[0].startswith("term\tcount\t")
    assert filt_en[0].startswith("term\tcount\t")

    # Filtered should be <= raw in row count (excluding header)
    assert len(filt_en) <= len(raw_en)

    # ITER appears in both sample files, so with min-count-en=2 it should survive.
    assert any(ln.startswith("ITER\t") for ln in filt_en[1:])


def test_extract_filtered_outputs_respects_stopwords(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "tests" / "fixtures" / "corpus"

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    stop = tmp_path / "en_stop.txt"
    stop.write_text("ITER\n", encoding="utf-8")

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
            "--min-count-en",
            "2",
            "--en-stopwords",
            str(stop),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    filt_en = (out_dir / "candidates_en.filtered.tsv").read_text("utf-8", errors="ignore")
    assert "ITER\t" not in filt_en


def test_extract_filtered_outputs_respects_zh_stopwords(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir(parents=True, exist_ok=True)
    (corpus_root / "a.md").write_text(
        # Put stopwords on their own so the regex extracts them exactly.
        "其中。\n"
        "例如：等离子体电流。\n"
        "所示。\n"
        "托卡马克装置。\n",
        encoding="utf-8",
    )
    (corpus_root / "b.md").write_text(
        "等离子体电流。\n",
        encoding="utf-8",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    stop = tmp_path / "zh_stop.txt"
    stop.write_text("其中\n例如\n所示\n", encoding="utf-8")

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.extract_candidates",
            "--source-root",
            str(corpus_root),
            "--out-dir",
            str(out_dir),
            "--min-count-zh",
            "1",
            "--zh-stopwords",
            str(stop),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    raw_zh = (out_dir / "candidates_zh.tsv").read_text("utf-8", errors="ignore")
    for expected in ["其中", "例如", "所示"]:
        assert f"{expected}\t" in raw_zh

    filt_zh = (out_dir / "candidates_zh.filtered.tsv").read_text(
        "utf-8",
        errors="ignore",
    )
    for banned in ["其中", "例如", "所示"]:
        assert f"{banned}\t" not in filt_zh
