from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _write_registry_tables(
    terms_dir: Path, *, concepts: str, aliases: str, evidence: str
) -> None:
    reg = terms_dir / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "concepts.tsv").write_text(concepts, encoding="utf-8")
    (reg / "aliases.tsv").write_text(aliases, encoding="utf-8")
    (reg / "evidence.tsv").write_text(evidence, encoding="utf-8")


def test_export_tag_rules_jsonl_is_deterministic_and_coalesces_kinds(tmp_path: Path) -> None:
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
            "Foo\titer\ten\talias\n"
            "Foo\titer\ten\tforbidden\n"
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
                "--tag-rules",
                "--no-vale",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        return (out_dir / "tag_rules.jsonl").read_text("utf-8")

    first = run_once()
    second = run_once()

    # No timestamps; should be byte-for-byte deterministic.
    assert first == second

    lines = [ln for ln in first.splitlines() if ln.strip()]
    parsed = [json.loads(ln) for ln in lines]

    # Sorted by alias.
    assert [r["alias"] for r in parsed] == sorted(r["alias"] for r in parsed)

    by_alias = {r["alias"]: r for r in parsed}

    assert by_alias["ITER"]["concept_id"] == "iter"
    assert by_alias["ITER"]["category"] == "device"
    assert by_alias["ITER"]["kind"] == "preferred"

    # Same alias appears twice; forbidden should win.
    assert by_alias["Foo"]["kind"] == "forbidden"

    manifest = json.loads((out_dir / "registry_exports.json").read_text("utf-8"))
    assert (out_dir / "tag_rules.jsonl").as_posix() == manifest["tag_rules"]
    assert manifest["tag_rule_count"] == len(parsed)
