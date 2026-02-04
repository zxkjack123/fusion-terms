from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_registry_tables(terms_dir: Path, *, concepts: str, aliases: str, evidence: str) -> None:
    reg = terms_dir / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "concepts.tsv").write_text(concepts, encoding="utf-8")
    (reg / "aliases.tsv").write_text(aliases, encoding="utf-8")
    (reg / "evidence.tsv").write_text(evidence, encoding="utf-8")


def test_export_query_expansions_is_deterministic_and_partitioned(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # Needed for validator's allowlist leak check.
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "iter\tdevice\t\tITER\tITER\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "ITER\titer\tabbr\tpreferred\n"
            "International Thermonuclear Experimental Reactor\titer\ten\talias\n"
            "Old ITER Name\titer\ten\tdeprecated\n"
            "TypoITER\titer\ten\tforbidden\n"
        ),
        evidence="iter\thttps://www.iter.org\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    def run_once() -> str:
        p = subprocess.run(
            [
                sys.executable,
                "-m",
                "pipeline.export_registry",
                "--terms-dir",
                str(terms_dir),
                "--out-dir",
                str(out_dir),
                "--query-expansions",
                "--no-vale",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        return (out_dir / "query_expansions.json").read_text("utf-8")

    first = run_once()
    second = run_once()

    # No timestamps; should be byte-for-byte deterministic.
    assert first == second

    import json

    data = json.loads(first)
    assert data["schema_version"] == 1
    assert data["alias_index"]["ITER"] == "iter"

    concept = data["concepts"]["iter"]
    assert concept["preferred"]["abbr"] == "ITER"

    assert concept["include"] == [
        "ITER",
        "International Thermonuclear Experimental Reactor",
    ]
    assert concept["deprecated"] == ["Old ITER Name"]
    assert concept["forbidden"] == ["TypoITER"]

    # all_terms excludes forbidden
    assert "TypoITER" not in concept["all_terms"]
