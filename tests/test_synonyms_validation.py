from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_build_fails_on_conflicting_synonyms(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # Minimal allow/deny to make build run.
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("ITER\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("", encoding="utf-8")

    # Same alias with different preferred -> should error.
    (terms_dir / "synonyms.tsv").write_text(
        "# alias\tpreferred\tlang(optional)\n"
        "Hmode\tH-mode\ten\n"
        "Hmode\tHmode\ten\n",
        encoding="utf-8",
    )

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
    assert "conflicting synonyms mapping" in combined
    assert "'Hmode'" in combined
