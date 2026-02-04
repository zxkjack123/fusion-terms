from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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

    # First run: baseline missing -> treat all as new; baseline gets updated by default.
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

    # Third run with no changes should be empty diffs (baseline was updated on p2).
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
