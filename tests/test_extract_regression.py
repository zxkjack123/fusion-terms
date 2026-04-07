from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path

import pytest

from pipeline import extract_candidates as extract_mod
from pipeline.extract_candidates import extract


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_ZH = (
    REPO_ROOT / "artifacts" / "_smoke_run" / "baseline_extract_zh_head.tsv"
)
BASELINE_EN = (
    REPO_ROOT / "artifacts" / "_smoke_run" / "baseline_extract_en_head.tsv"
)


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

    zh_head = (
        "\n".join(
            (tmp_path / "candidates_zh.tsv")
            .read_text("utf-8")
            .splitlines()[:21]
        )
        + "\n"
    )
    en_head = (
        "\n".join(
            (tmp_path / "candidates_en.tsv")
            .read_text("utf-8")
            .splitlines()[:21]
        )
        + "\n"
    )

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


def test_save_cache_index_uses_atomic_replace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    index_path = cache_dir / "index.json"
    index_path.write_text(json.dumps({"version": 0}), "utf-8")

    called: list[tuple[Path, Path]] = []
    real_replace = os.replace

    def wrapped_replace(
        src: str | os.PathLike[str],
        dst: str | os.PathLike[str],
    ) -> None:
        called.append((Path(src), Path(dst)))
        real_replace(src, dst)

    monkeypatch.setattr(extract_mod.os, "replace", wrapped_replace)

    extract_mod._save_cache_index(cache_dir, {"version": 1, "files": {}})

    assert called, "expected os.replace to be used during cache index save"
    assert called[0][1] == index_path
    saved = json.loads(index_path.read_text("utf-8"))
    assert saved["version"] == 1


def test_save_cache_index_replace_failure_preserves_original(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    index_path = cache_dir / "index.json"
    original = {"version": 0, "files": {"a.md": {"mtime_ns": 1}}}
    index_path.write_text(
        json.dumps(original, ensure_ascii=False, indent=2),
        "utf-8",
    )

    def fail_replace(
        src: str | os.PathLike[str],
        dst: str | os.PathLike[str],
    ) -> None:
        raise OSError("simulated replace failure")

    monkeypatch.setattr(extract_mod.os, "replace", fail_replace)

    with pytest.raises(OSError, match="simulated replace failure"):
        extract_mod._save_cache_index(cache_dir, {"version": 1, "files": {}})

    assert json.loads(index_path.read_text("utf-8")) == original
    assert not list(cache_dir.glob("index.json.tmp.*")), (
        "tmp files should be cleaned on failure"
    )


def test_write_tsv_escapes_tab_and_newline_fields(tmp_path: Path) -> None:
    out = tmp_path / "candidates.tsv"
    counts = Counter({"termA": 1})
    examples = {"termA": ["line with\ttab", "line with\nnewline"]}
    files = {"termA": ["/tmp/a\tb.md", "/tmp/c\nd.md"]}

    extract_mod._write_tsv(
        path=out,
        counts=counts,
        examples=examples,
        files=files,
    )

    rows = out.read_text("utf-8").splitlines()
    assert len(rows) == 2
    cols = rows[1].split("\t")
    assert len(cols) == 4, f"expected 4 TSV columns, got {len(cols)}: {cols}"
