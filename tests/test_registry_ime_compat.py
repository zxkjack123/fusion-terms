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


def test_ime_wordlist_and_registry_exports_can_coexist_in_same_out_dir(tmp_path: Path) -> None:
    """Stage 8.4 regression: registry exports must not break IME build workflow.

    Acceptance intent:
    - build_terms output stays stable
    - export_registry can write additional artifacts into the same out_dir
      without modifying domain_terms.txt
    """

    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # IME inputs (source of truth for build_terms).
    (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("ITER\nbeta_N\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("beta_N\tβ_N\n", encoding="utf-8")

    # Registry tables are additive for other consumers.
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
        ),
        evidence="iter\thttps://www.iter.org\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    build = subprocess.run(
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
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert build.returncode == 0, f"stdout:\n{build.stdout}\nstderr:\n{build.stderr}"

    wordlist_path = out_dir / "domain_terms.txt"
    before = wordlist_path.read_text("utf-8", errors="ignore")

    export = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.export_registry",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--query-expansions",
            "--tag-rules",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert export.returncode == 0, f"stdout:\n{export.stdout}\nstderr:\n{export.stderr}"

    # Registry exports must not mutate the IME wordlist.
    after = wordlist_path.read_text("utf-8", errors="ignore")
    assert before == after

    # And should produce additional artifacts alongside it.
    assert (out_dir / "query_expansions.json").exists()
    assert (out_dir / "tag_rules.jsonl").exists()
    assert (out_dir / "registry_exports.json").exists()
