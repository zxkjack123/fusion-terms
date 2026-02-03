from __future__ import annotations

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


def test_extract_then_build_smoke(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "tests" / "fixtures" / "corpus"
    terms_dir = repo_root / "tests" / "fixtures" / "terms"

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
            "--max-files",
            "10",
        ],
        cwd=repo_root,
    )

    zh_tsv = out_dir / "candidates_zh.tsv"
    en_tsv = out_dir / "candidates_en.tsv"
    stats_json = out_dir / "extract_stats.json"

    assert zh_tsv.exists()
    assert en_tsv.exists()
    assert stats_json.exists()

    zh_text = zh_tsv.read_text("utf-8", errors="ignore")
    en_text = en_tsv.read_text("utf-8", errors="ignore")

    assert zh_text.splitlines()[0].startswith("term\tcount\t")
    assert en_text.splitlines()[0].startswith("term\tcount\t")

    # Chinese example term
    assert "托卡马克" in zh_text

    # English/mixed patterns covered by current extractor rules
    for expected in ["ITER", "NBI", "H-mode", "Nb3Sn", "W/Be"]:
        assert expected in en_text

    _run(
        [
            sys.executable,
            "-m",
            "pipeline.build_terms",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--output",
            "domain_terms.txt",
        ],
        cwd=repo_root,
    )

    wordlist_path = out_dir / "domain_terms.txt"
    assert wordlist_path.exists()

    terms = [ln.strip() for ln in wordlist_path.read_text("utf-8").splitlines()]
    assert all(terms)

    # ensure synonyms mapping is applied (beta_N -> β_N)
    assert "β_N" in terms
    assert "beta_N" not in terms

    # allowlisted terms present
    assert "托卡马克" in terms
    assert "ITER" in terms
    assert "NBI" in terms


def test_build_rejects_whitespace_terms(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # Minimal curated lists
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text(
        "ITER\nneutral beam\n",
        encoding="utf-8",
    )
    (terms_dir / "denylist.txt").write_text("", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("", encoding="utf-8")

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.build_terms",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode != 0
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    assert "must not contain whitespace" in combined
    assert "neutral beam" in combined
