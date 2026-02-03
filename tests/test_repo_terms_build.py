from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_build_from_repo_terms_is_non_empty_and_token_only(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
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
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    wordlist = (out_dir / "domain_terms.txt").read_text("utf-8", errors="ignore")
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
