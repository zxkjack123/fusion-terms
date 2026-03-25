from __future__ import annotations

import json
from pathlib import Path

from pipeline.extract_candidates import extract


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_ZH = REPO_ROOT / "artifacts" / "_smoke_run" / "baseline_extract_zh_head.tsv"
BASELINE_EN = REPO_ROOT / "artifacts" / "_smoke_run" / "baseline_extract_en_head.tsv"


def _run_extract(out_dir: Path) -> None:
    extract(
        source_root=Path("tests/fixtures/corpus"),
        out_dir=out_dir,
        min_zh_len=2,
        max_zh_len=8,
        max_examples=3,
        max_files_per_term=20,
        max_files=None,
        min_count_zh=None,
        min_count_en=None,
        topk_zh=None,
        topk_en=None,
        zh_stopwords=None,
        en_stopwords=None,
        en_phrases="off",
        incremental=False,
        cache_dir=None,
        exclude_globs=None,
    )


def test_extract_output_matches_baseline(tmp_path: Path) -> None:
    assert BASELINE_ZH.exists(), f"missing baseline file: {BASELINE_ZH}"
    assert BASELINE_EN.exists(), f"missing baseline file: {BASELINE_EN}"

    _run_extract(tmp_path)

    zh_head = "\n".join((tmp_path / "candidates_zh.tsv").read_text("utf-8").splitlines()[:21]) + "\n"
    en_head = "\n".join((tmp_path / "candidates_en.tsv").read_text("utf-8").splitlines()[:21]) + "\n"

    assert zh_head == BASELINE_ZH.read_text("utf-8")
    assert en_head == BASELINE_EN.read_text("utf-8")


def test_extract_stats_keys(tmp_path: Path) -> None:
    _run_extract(tmp_path)

    stats = json.loads((tmp_path / "extract_stats.json").read_text("utf-8"))

    expected_top = {
        "source_root",
        "files_scanned",
        "zh_terms",
        "en_terms",
        "en_phrase_terms",
        "cache",
        "outputs",
    }
    assert expected_top.issubset(set(stats.keys()))

    expected_cache = {
        "enabled",
        "incremental",
        "dir",
        "extractor_sig",
        "hits",
        "misses",
        "processed_files",
        "skipped_files",
        "invalidated",
    }
    assert expected_cache.issubset(set(stats["cache"].keys()))
