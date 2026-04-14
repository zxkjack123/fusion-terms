from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


_JSON_STR_RE = r'"(?:\\.|[^"\\])*"'
_SWAP_LINE_RE = re.compile(
    rf"^\s{{2}}(?P<k>{_JSON_STR_RE})\s*:\s*(?P<v>{_JSON_STR_RE})\s*$"
)


def _write_registry_tables(
    terms_dir: Path, *, concepts: str, aliases: str, evidence: str
) -> None:
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


def _parse_swap_mapping(yml_text: str) -> dict[str, str]:
    lines = yml_text.splitlines()
    try:
        idx = lines.index("swap:")
    except ValueError as e:
        raise AssertionError("missing swap: section") from e

    mapping: dict[str, str] = {}
    for ln in lines[idx + 1 :]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if not ln.startswith("  "):
            break
        m = _SWAP_LINE_RE.match(ln)
        assert m, f"invalid swap line: {ln!r}"
        k = json.loads(m.group("k"))
        v = json.loads(m.group("v"))
        mapping[k] = v
    return mapping


def test_export_vale_substitute_yaml_is_deterministic_and_matches_tsv(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=("iter\tdevice\n"),
        aliases=(
            "ITER\titer\tabbr\tpreferred\n"
            "Old ITER Name\titer\ten\tdeprecated\n"
            "TypoITER\titer\ten\tforbidden\n"
        ),
        evidence="iter\thttps://www.iter.org\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    def run_once() -> tuple[str, str]:
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
                "--vale-substitute",
                "--no-vale",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        tsv = (out_dir / "terminology_substitutions.tsv").read_text("utf-8")
        yml = (out_dir / "vale" / "terminology_substitute.yml").read_text("utf-8")
        return tsv, yml

    first_tsv, first_yml = run_once()
    second_tsv, second_yml = run_once()

    assert first_tsv == second_tsv
    assert first_yml == second_yml

    # TSV -> mapping
    rows = [
        ln for ln in first_tsv.splitlines() if ln.strip() and not ln.startswith("#")
    ]
    tsv_map = {ln.split("\t")[0]: ln.split("\t")[1] for ln in rows}

    yml_map = _parse_swap_mapping(first_yml)
    assert yml_map == tsv_map

    # manifest contains paths
    manifest = json.loads((out_dir / "registry_exports.json").read_text("utf-8"))
    assert (out_dir / "vale" / "terminology_substitute.yml").as_posix() == manifest[
        "vale_terminology_substitute"
    ]
    assert manifest["vale_terminology_substitute_count"] == len(yml_map)


def test_export_vale_substitute_basic(tmp_path: Path) -> None:
    """Verify YAML has swap section with correct key-value pair."""
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "tok\tdevice\t托卡马克\ttokamak\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\tcomment\n"
            "tokamak\ttok\ten\tpreferred\t\n"
            "旧称\ttok\tzh\tforbidden\ttypo\n"
        ),
        evidence="tok\thttps://example.invalid\n",
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
            "--vale-substitute",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    yml_path = out_dir / "vale" / "terminology_substitute.yml"
    assert yml_path.exists()
    yml_text = yml_path.read_text("utf-8")
    assert "swap:" in yml_text
    mapping = _parse_swap_mapping(yml_text)
    assert "旧称" in mapping


def test_export_vale_substitute_yaml_direct_call(tmp_path: Path) -> None:
    """Direct in-process call to export_vale_substitute_yaml for coverage."""
    from pipeline.export_registry import export_vale_substitute_yaml

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    reg = terms_dir / "registry"
    reg.mkdir()
    (reg / "aliases.tsv").write_text(
        "# alias\tconcept_id\tlang\tkind\tcomment\n"
        "tokamak\ttok\ten\tpreferred\t\n"
        "旧称\ttok\tzh\tforbidden\ttypo\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "artifacts"
    out_dir.mkdir()

    result = export_vale_substitute_yaml(terms_dir=terms_dir, out_dir=out_dir)
    assert result["vale_terminology_substitute_count"] > 0

    yml_path = Path(result["vale_terminology_substitute"])
    assert yml_path.exists()
    yml_text = yml_path.read_text("utf-8")
    assert "swap:" in yml_text
    mapping = _parse_swap_mapping(yml_text)
    assert "旧称" in mapping
