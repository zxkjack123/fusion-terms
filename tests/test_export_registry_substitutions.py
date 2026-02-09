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


def _write_min_terms_files(terms_dir: Path) -> None:
    # Needed for validator's allowlist leak check.
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("\n", encoding="utf-8")


def test_export_substitutions_tsv_is_deterministic_and_lang_prefers(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "iter\tdevice\t\tITER\tITER\tactive\n"
            "qse\tdevice\tQSE\tQSE\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\tcomment\n"
            "ITER\titer\tabbr\tpreferred\t\n"
            "国际热核聚变实验堆\titer\tzh\tpreferred\t\n"
            "Old ITER Name\titer\ten\tdeprecated\tuse ITER\n"
            "TypoITER\titer\ten\tforbidden\ttypo\n"
            "QSE\tqse\ten\tpreferred\t\n"
            "量子能量系统\tqse\tzh\tdeprecated\told zh name\n"
        ),
        evidence="iter\thttps://www.iter.org\nqse\thttps://example.invalid\n",
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
                "--substitutions",
                "--no-vale",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        return (out_dir / "terminology_substitutions.tsv").read_text("utf-8")

    first = run_once()
    second = run_once()

    assert first == second

    lines = [ln for ln in first.splitlines() if ln.strip()]
    assert lines[0].startswith("# alias\tpreferred\tstatus\tlang\tnote")

    rows = [ln for ln in lines[1:] if not ln.startswith("#")]

    # Sorted by alias (deterministic)
    aliases = [r.split("\t", 1)[0] for r in rows]
    assert aliases == sorted(aliases)

    by_alias = {r.split("\t")[0]: r.split("\t") for r in rows}

    # deprecated and forbidden only
    assert by_alias["Old ITER Name"][2] == "deprecated"
    assert by_alias["TypoITER"][2] == "forbidden"

    # en deprecated should map to en/abbr preferred; our selection prefers same-lang first.
    # For iter concept, there is no en preferred row, so it falls back to any preferred
    # with tie-breaker (lang, alias) => abbr ITER wins.
    assert by_alias["Old ITER Name"][1] == "ITER"
    assert by_alias["TypoITER"][1] == "ITER"

    # zh deprecated should map to zh preferred when available.
    # In this fixture, qse has only en preferred, so it falls back to QSE.
    assert by_alias["量子能量系统"][1] == "QSE"

    import json

    manifest = json.loads((out_dir / "registry_exports.json").read_text("utf-8"))
    assert (out_dir / "terminology_substitutions.tsv").as_posix() == manifest["terminology_substitutions"]
    assert manifest["substitution_count"] == len(rows)


def test_export_substitutions_fails_if_no_preferred(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts="x\tdevice\n",
        aliases="Old Name\tx\ten\tdeprecated\n",
        evidence="x\thttps://example.invalid\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.export_registry",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--substitutions",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode != 0


def test_export_substitutions_fails_on_alias_equal_preferred(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts="x\tdevice\n",
        aliases=(
            "SAME\tx\ten\tpreferred\n"
            "SAME\tx\ten\tdeprecated\n"
        ),
        evidence="x\thttps://example.invalid\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.export_registry",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--substitutions",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode != 0
