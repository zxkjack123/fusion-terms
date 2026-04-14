from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import pipeline.apply_decisions as apply_mod


def _read(path: Path) -> str:
    return path.read_text("utf-8", errors="ignore")


def test_apply_decisions_dry_run_and_apply_is_idempotent(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # Seed minimal repo truth files.
    (terms_dir / "allowlist_en.txt").write_text("# header\nITER\n", encoding="utf-8")
    (terms_dir / "allowlist_zh.txt").write_text(
        "# header\n托卡马克\n", encoding="utf-8"
    )
    (terms_dir / "denylist.txt").write_text("# header\nFigure\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text(
        "# header\nHmode\tH-mode\ten\n", encoding="utf-8"
    )

    decisions = tmp_path / "decisions.tsv"
    decisions.write_text(
        "# action\tvalue\tpreferred\tlang\tcomment\n"
        "allow_en\tNBI\t\t\t\n"
        "allow_zh\t偏滤器\t\t\t\n"
        "deny\tTable\t\t\t\n"
        "synonym\tbetaN\tbeta_N\ten\t\n",
        encoding="utf-8",
    )

    # Dry-run should not modify files.
    before_allow_en = _read(terms_dir / "allowlist_en.txt")
    p0 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.apply_decisions",
            "--terms-dir",
            str(terms_dir),
            "--decisions",
            str(decisions),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p0.returncode == 0, f"stdout:\n{p0.stdout}\nstderr:\n{p0.stderr}"
    assert _read(terms_dir / "allowlist_en.txt") == before_allow_en

    # Apply should add AUTO-INBOX blocks.
    p1 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.apply_decisions",
            "--terms-dir",
            str(terms_dir),
            "--decisions",
            str(decisions),
            "--apply",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p1.returncode == 0, f"stdout:\n{p1.stdout}\nstderr:\n{p1.stderr}"

    allow_en = _read(terms_dir / "allowlist_en.txt")
    assert "AUTO-INBOX" in allow_en
    assert "NBI" in allow_en

    allow_zh = _read(terms_dir / "allowlist_zh.txt")
    assert "偏滤器" in allow_zh

    deny = _read(terms_dir / "denylist.txt")
    assert "Table" in deny

    syn = _read(terms_dir / "synonyms.tsv")
    assert "betaN\tbeta_N\ten" in syn

    # Second apply should be idempotent (byte-for-byte stable).
    snap = {
        "allow_en": allow_en,
        "allow_zh": allow_zh,
        "deny": deny,
        "syn": syn,
    }

    p2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.apply_decisions",
            "--terms-dir",
            str(terms_dir),
            "--decisions",
            str(decisions),
            "--apply",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p2.returncode == 0, f"stdout:\n{p2.stdout}\nstderr:\n{p2.stderr}"

    assert _read(terms_dir / "allowlist_en.txt") == snap["allow_en"]
    assert _read(terms_dir / "allowlist_zh.txt") == snap["allow_zh"]
    assert _read(terms_dir / "denylist.txt") == snap["deny"]
    assert _read(terms_dir / "synonyms.tsv") == snap["syn"]


def test_apply_decisions_rejects_synonyms_conflict(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("betaN\tbeta_N\n", encoding="utf-8")

    decisions = tmp_path / "decisions.tsv"
    decisions.write_text("synonym\tbetaN\tβ_N\ten\n", encoding="utf-8")

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.apply_decisions",
            "--terms-dir",
            str(terms_dir),
            "--decisions",
            str(decisions),
            "--apply",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "conflicting synonyms mapping" in combined


def test_rewrite_auto_inbox_warns_when_non_comment_content_will_be_overwritten(
    tmp_path: Path,
) -> None:
    path = tmp_path / "allowlist_en.txt"
    path.write_text(
        f"# header\n{apply_mod.AUTO_MARKER}\nmanual_legacy_term\n# comment\n",
        encoding="utf-8",
    )

    with pytest.warns(UserWarning, match="AUTO_MARKER"):
        apply_mod._rewrite_auto_inbox_list(path, {"NBI"})

    out = path.read_text("utf-8")
    assert "manual_legacy_term" not in out
    assert "NBI" in out


def test_atomic_write_failure_does_not_corrupt_original_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "allowlist_en.txt"
    original = "# header\nITER\n"
    path.write_text(original, encoding="utf-8")

    def _boom(_src: Path, _dst: Path) -> None:
        raise OSError("simulated replace failure")

    monkeypatch.setattr(apply_mod.os, "replace", _boom)

    with pytest.raises(OSError, match="replace failure"):
        apply_mod._rewrite_auto_inbox_list(path, {"NBI"})

    assert path.read_text("utf-8") == original
