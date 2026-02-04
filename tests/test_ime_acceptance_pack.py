from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_ime_acceptance_pack_detects_missing_and_writes_outputs(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    wordlist = out_dir / "domain_terms.txt"
    wordlist.write_text(
        "ITER\nEAST\nNBI\nH-mode\nq95\nβ_N\nτ_E\n托卡马克\n", encoding="utf-8"
    )

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.ime_acceptance_pack",
            "--wordlist",
            str(wordlist),
            "--out-dir",
            str(out_dir),
            "--pick-n",
            "10",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    pack_path = out_dir / "ime_acceptance_pack.json"
    terms_path = out_dir / "ime_acceptance_terms.txt"
    hints_path = out_dir / "ime_acceptance_terms_hints.tsv"
    assert pack_path.exists()
    assert terms_path.exists()
    assert hints_path.exists()

    pack = json.loads(pack_path.read_text("utf-8"))
    assert pack["schema_version"] == 1
    assert pack["wordlist"] == str(wordlist)

    # Some defaults should be missing because our synthetic wordlist is small.
    assert pack["counts"]["missing_must_have"] >= 1
    assert "CuCrZr" in pack["missing_must_have"]

    # Suggested list always includes all must-have terms; pick-n is a target
    # that will not truncate must-haves.
    assert pack["counts"]["suggested_typing_terms"] >= len(pack["must_have"])

    # Stable: checks order matches must_have list order.
    assert [c["term"] for c in pack["checks"]] == pack["must_have"]

    # The typing terms file should mirror suggested list.
    suggested = pack["suggested_typing_terms"]
    lines = [ln.strip() for ln in terms_path.read_text("utf-8").splitlines() if ln.strip()]
    assert lines == suggested

    # Symbol-heavy terms should carry typing hints (best-effort romanization).
    typing_hints = pack.get("typing_hints")
    assert isinstance(typing_hints, dict)
    assert "β_N" in typing_hints
    assert any("beta" in h.lower() for h in typing_hints["β_N"])
    assert "τ_E" in typing_hints
    assert any("tau" in h.lower() for h in typing_hints["τ_E"])

    # TSV hints file should include at least those hint rows.
    tsv_lines = [ln.rstrip("\n") for ln in hints_path.read_text("utf-8").splitlines() if ln.strip()]
    assert tsv_lines[0].split("\t")[:2] == ["term", "hints"]
    assert any(ln.startswith("β_N\t") and "beta" in ln.lower() for ln in tsv_lines[1:])
    assert any(ln.startswith("τ_E\t") and "tau" in ln.lower() for ln in tsv_lines[1:])
