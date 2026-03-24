from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from pipeline.review_pack import _resolve_under


def _write_tsv(path: Path, rows: list[tuple[str, int]]) -> None:
    lines = ["term\tcount\texamples\tfiles"]
    for term, cnt in rows:
        lines.append(f"{term}\t{cnt}\t\t")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_review_pack_diffs_and_updates_baseline(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    cur_zh = out_dir / "candidates_zh.filtered.tsv"
    cur_en = out_dir / "candidates_en.filtered.tsv"

    # Seed current candidates.
    _write_tsv(cur_zh, [("托卡马克", 5), ("偏滤器", 3)])
    _write_tsv(cur_en, [("ITER", 10), ("NBI", 4)])

    # First run: baseline missing -> treat all as new;
    # baseline gets updated by default.
    p1 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p1.returncode == 0, f"stdout:\n{p1.stdout}\nstderr:\n{p1.stderr}"

    rp_dir = out_dir / "review_pack"
    summary = json.loads((rp_dir / "summary.json").read_text("utf-8"))
    assert summary["counts"]["new_zh"] == 2
    assert summary["counts"]["new_en"] == 2
    assert summary["counts"]["removed_zh"] == 0
    assert summary["counts"]["removed_en"] == 0

    baseline_dir = out_dir / ".review_baseline"
    assert (baseline_dir / cur_zh.name).exists()
    assert (baseline_dir / cur_en.name).exists()

    # Change current: add one, remove one.
    _write_tsv(cur_zh, [("托卡马克", 5), ("位形", 1)])
    _write_tsv(cur_en, [("ITER", 11), ("ECRH", 2)])

    p2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p2.returncode == 0, f"stdout:\n{p2.stdout}\nstderr:\n{p2.stderr}"

    # Second run diffs against previous baseline.
    summary2 = json.loads((rp_dir / "summary.json").read_text("utf-8"))
    assert summary2["counts"]["new_zh"] == 1  # 位形
    assert summary2["counts"]["removed_zh"] == 1  # 偏滤器
    assert summary2["counts"]["new_en"] == 1  # ECRH
    assert summary2["counts"]["removed_en"] == 1  # NBI

    new_en_text = (rp_dir / f"new_{cur_en.name}").read_text("utf-8")
    assert "ECRH\t2" in new_en_text

    removed_en_text = (rp_dir / f"removed_{cur_en.name}").read_text("utf-8")
    assert "NBI\t4" in removed_en_text

    # Third run with no changes should be empty diffs
    # (baseline was updated on p2).
    p3 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p3.returncode == 0, f"stdout:\n{p3.stdout}\nstderr:\n{p3.stderr}"

    summary3 = json.loads((rp_dir / "summary.json").read_text("utf-8"))
    assert summary3["counts"]["new_zh"] == 0
    assert summary3["counts"]["removed_zh"] == 0
    assert summary3["counts"]["new_en"] == 0
    assert summary3["counts"]["removed_en"] == 0


def test_review_pack_can_exclude_known_allow_deny_terms(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create a minimal curated terms dir.
    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("ITER\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("偏滤器\nNBI\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("", encoding="utf-8")

    cur_zh = out_dir / "candidates_zh.filtered.tsv"
    cur_en = out_dir / "candidates_en.filtered.tsv"

    # Seed current candidates including already known allow/deny terms.
    _write_tsv(cur_zh, [("托卡马克", 5), ("偏滤器", 3), ("位形", 2)])
    _write_tsv(cur_en, [("ITER", 10), ("NBI", 4), ("ECRH", 2)])

    # Baseline missing; without exclusion everything would be new.
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.review_pack",
            "--out-dir",
            str(out_dir),
            "--exclude-known-terms",
            "--terms-dir",
            str(terms_dir),
            # Don't update baseline in a unit test unless we need to.
            "--no-update-baseline",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    rp_dir = out_dir / "review_pack"
    summary = json.loads((rp_dir / "summary.json").read_text("utf-8"))

    # Known allow/deny terms should not appear in new/removed.
    assert summary["counts"]["new_zh"] == 1  # 位形 only
    assert summary["counts"]["new_en"] == 1  # ECRH only
    assert summary["counts"]["removed_zh"] == 0
    assert summary["counts"]["removed_en"] == 0

    new_zh_text = (rp_dir / f"new_{cur_zh.name}").read_text("utf-8")
    assert "位形\t2" in new_zh_text
    assert "托卡马克\t" not in new_zh_text
    assert "偏滤器\t" not in new_zh_text

    new_en_text = (rp_dir / f"new_{cur_en.name}").read_text("utf-8")
    assert "ECRH\t2" in new_en_text
    assert "ITER\t" not in new_en_text
    assert "NBI\t" not in new_en_text


def test_resolve_under_rejects_path_traversal(tmp_path: Path) -> None:
    base = tmp_path / "artifacts"
    base.mkdir(parents=True, exist_ok=True)

    with pytest.raises(SystemExit, match="path escapes base directory"):
        _resolve_under(base, "../../etc/passwd")


def test_resolve_under_accepts_normal_relative(tmp_path: Path) -> None:
    base = tmp_path / "artifacts"
    base.mkdir(parents=True, exist_ok=True)

    out = _resolve_under(base, "sub/file.tsv")
    assert out == (base / "sub/file.tsv").resolve()

    abs_path = (tmp_path / "absolute.tsv").resolve()
    out_abs = _resolve_under(base, str(abs_path))
    assert out_abs == abs_path
