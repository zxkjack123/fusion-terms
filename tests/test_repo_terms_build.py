from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_build_from_repo_terms_is_non_empty_and_token_only(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    def run_build() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pipeline.build_terms",
                "--terms-dir",
                str(repo_root / "terms"),
                "--out-dir",
                str(out_dir),
                "--output",
                "domain_terms.txt",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )

    p1 = run_build()
    assert p1.returncode == 0, f"stdout:\n{p1.stdout}\nstderr:\n{p1.stderr}"

    wordlist_path = out_dir / "domain_terms.txt"
    stats_path = out_dir / "domain_terms_build_stats.json"

    wordlist = wordlist_path.read_text("utf-8", errors="ignore")
    terms = [ln.strip() for ln in wordlist.splitlines() if ln.strip()]

    # Sanity: after seeding, repo terms should produce a non-empty wordlist.
    assert len(terms) >= 10

    # Token-only contract: no whitespace inside a term.
    assert all((" " not in t and "\t" not in t) for t in terms)

    # Spot-check a few high-value seeds.
    for expected in ["ITER", "EAST", "NBI", "H-mode", "Nb3Sn", "q95", "β_N", "τ_E", "托卡马克"]:
        assert expected in terms

    # denylist must take effect if someone accidentally adds noise.
    assert "Figure" not in terms

    # Build stats json should exist and match the produced wordlist.
    assert stats_path.exists()
    stats_1 = json.loads(stats_path.read_text("utf-8"))
    assert stats_1["schema_version"] == 1
    assert stats_1["wordlist"] == str(wordlist_path)
    assert stats_1["stats_path"] == str(stats_path)

    counts_1 = stats_1["counts"]
    assert counts_1["total"] == len(terms)
    assert counts_1["zh"] + counts_1["en"] == counts_1["total"]
    assert isinstance(counts_1["synonyms_mapped"], int)
    assert counts_1["synonyms_mapped"] >= 0
    # First run: no previous file to diff against.
    assert counts_1["added"] == len(terms)
    assert counts_1["removed"] == 0
    assert len(stats_1["added"]) == counts_1["added"]
    assert len(stats_1["removed"]) == counts_1["removed"]

    # Second run: should be stable, and added/removed should be empty.
    p2 = run_build()
    assert p2.returncode == 0, f"stdout:\n{p2.stdout}\nstderr:\n{p2.stderr}"
    stats_2 = json.loads(stats_path.read_text("utf-8"))
    counts_2 = stats_2["counts"]
    assert counts_2["total"] == len(terms)
    assert counts_2["added"] == 0
    assert counts_2["removed"] == 0
    assert stats_2["added"] == []
    assert stats_2["removed"] == []

    # Third run: stats content should be deterministic (byte-identical).
    before = stats_path.read_bytes()
    p3 = run_build()
    assert p3.returncode == 0, f"stdout:\n{p3.stdout}\nstderr:\n{p3.stderr}"
    after = stats_path.read_bytes()
    assert after == before
