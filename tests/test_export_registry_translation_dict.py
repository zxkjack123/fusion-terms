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


def _write_min_terms_files(terms_dir: Path) -> None:
    # Needed for validator's allowlist leak checks.
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("\n", encoding="utf-8")


def _run_export_translation(repo_root: Path, terms_dir: Path, out_dir: Path) -> dict:
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "pipeline.export_registry",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--translation-dict",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
    return json.loads((out_dir / "translation_dict.json").read_text("utf-8"))


def test_translation_dict_basic(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "design\tconcept\t设计\tdesign\t\tactive\n"
            "tritium-breeding-ratio\tmetric\t氚增殖比\ttritium breeding ratio\tTBR\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "设计\tdesign\tzh\tpreferred\n"
            "design\tdesign\ten\tpreferred\n"
            "氚增殖比\ttritium-breeding-ratio\tzh\tpreferred\n"
            "tritium breeding ratio\ttritium-breeding-ratio\ten\tpreferred\n"
            "TBR\ttritium-breeding-ratio\tabbr\tpreferred\n"
        ),
        evidence=(
            "design\thttps://example.invalid/design\n"
            "tritium-breeding-ratio\thttps://example.invalid/tbr\n"
        ),
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert data["schema_version"] == 2
    assert data["zh2en"]["设计"] == "design"
    assert data["zh2en"]["氚增殖比"] == "tritium breeding ratio"
    assert data["en2zh"]["design"] == "设计"
    assert data["en2zh"]["tritium breeding ratio"] == "氚增殖比"
    assert "en2zh_short" in data
    assert "TBR" not in data["en2zh"]
    assert "TBR" in data["en2zh_short"]
    assert data["en2zh_short"]["TBR"]["zh"] == "氚增殖比"
    assert data["en2zh_short"]["TBR"]["concept_id"] == "tritium-breeding-ratio"
    assert data["metadata"]["pairs_zh2en"] == len(data["zh2en"])
    assert data["metadata"]["pairs_en2zh"] == len(data["en2zh"])


def test_translation_dict_deterministic(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "design\tconcept\t设计\tdesign\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "设计\tdesign\tzh\tpreferred\n"
            "design\tdesign\ten\tpreferred\n"
            "方案\tdesign\tzh\talias\n"
        ),
        evidence="design\thttps://example.invalid/design\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    _run_export_translation(repo_root, terms_dir, out_dir)
    first = (out_dir / "translation_dict.json").read_text("utf-8")

    _run_export_translation(repo_root, terms_dir, out_dir)
    second = (out_dir / "translation_dict.json").read_text("utf-8")

    assert first == second


def test_translation_dict_skips_forbidden_deprecated(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "safety-analysis\tmethod\t安全分析\tsafety analysis\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "安全分析\tsafety-analysis\tzh\tpreferred\n"
            "safety analysis\tsafety-analysis\ten\tpreferred\n"
            "旧安全分析\tsafety-analysis\tzh\tdeprecated\n"
            "wrong safety analysis\tsafety-analysis\ten\tforbidden\n"
        ),
        evidence="safety-analysis\thttps://example.invalid/safety\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert "旧安全分析" not in data["zh2en"]
    assert "wrong safety analysis" not in data["en2zh"]


def test_translation_dict_missing_preferred_en(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "only-zh\tconcept\t仅中文\t\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "仅中文\tonly-zh\tzh\tpreferred\n"
            "仅中\tonly-zh\tzh\talias\n"
        ),
        evidence="only-zh\thttps://example.invalid/only-zh\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert data["zh2en"] == {}


def test_translation_dict_missing_preferred_zh(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "only-en\tconcept\t\tonly en\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "only en\tonly-en\ten\tpreferred\n"
            "only\tonly-en\ten\talias\n"
        ),
        evidence="only-en\thttps://example.invalid/only-en\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert data["en2zh"] == {}


def test_translation_dict_abbr_aliases(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "cfetr\tdevice\t中国聚变工程试验堆\tCFETR\tCFETR\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "中国聚变工程试验堆\tcfetr\tzh\tpreferred\n"
            "CFETR\tcfetr\tabbr\tpreferred\n"
            "CFETR reactor\tcfetr\ten\talias\n"
        ),
        evidence="cfetr\thttps://example.invalid/cfetr\n",
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert data["zh2en"]["CFETR"] == "CFETR"
    assert "CFETR" not in data["en2zh"]
    assert data["en2zh_short"]["CFETR"]["zh"] == "中国聚变工程试验堆"
    assert data["en2zh_short"]["CFETR"]["concept_id"] == "cfetr"


def test_translation_dict_short_en_keys_segregated(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "deuterium\tmaterial\t氘\tdeuterium\tD\tactive\n"
            "central-solenoid\tcomponent\t中心螺管\tcentral solenoid\tCS\tactive\n"
            "tritium-breeding-ratio\tmetric\t氚增殖比\ttritium breeding ratio\tTBR\tactive\n"
            "beta\tmetric\t比压\tbeta\tβ\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "氘\tdeuterium\tzh\tpreferred\n"
            "deuterium\tdeuterium\ten\tpreferred\n"
            "D\tdeuterium\tabbr\tpreferred\n"
            "中心螺管\tcentral-solenoid\tzh\tpreferred\n"
            "central solenoid\tcentral-solenoid\ten\tpreferred\n"
            "CS\tcentral-solenoid\tabbr\tpreferred\n"
            "氚增殖比\ttritium-breeding-ratio\tzh\tpreferred\n"
            "tritium breeding ratio\ttritium-breeding-ratio\ten\tpreferred\n"
            "TBR\ttritium-breeding-ratio\tabbr\tpreferred\n"
            "比压\tbeta\tzh\tpreferred\n"
            "beta\tbeta\ten\tpreferred\n"
            "β\tbeta\tabbr\tpreferred\n"
        ),
        evidence=(
            "deuterium\thttps://example.invalid/deuterium\n"
            "central-solenoid\thttps://example.invalid/cs\n"
            "tritium-breeding-ratio\thttps://example.invalid/tbr\n"
            "beta\thttps://example.invalid/beta\n"
        ),
    )

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = _run_export_translation(repo_root, terms_dir, out_dir)

    assert data["schema_version"] == 2

    assert "D" not in data["en2zh"]
    assert "CS" not in data["en2zh"]
    assert "D" in data["en2zh_short"]
    assert "CS" in data["en2zh_short"]

    assert "TBR" not in data["en2zh"]
    assert "TBR" in data["en2zh_short"]
    assert data["en2zh_short"]["TBR"]["concept_id"] == "tritium-breeding-ratio"

    assert "β" in data["en2zh"]
    assert "β" not in data["en2zh_short"]

    assert data["en2zh_short"]["D"]["zh"] == "氘"
    assert data["en2zh_short"]["D"]["concept_id"] == "deuterium"
    assert data["metadata"]["pairs_en2zh_short"] == len(data["en2zh_short"])


def test_translation_dict_cli_flag(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    _write_min_terms_files(terms_dir)

    _write_registry_tables(
        terms_dir,
        concepts=(
            "# concept_id\tcategory\tpreferred_zh\tpreferred_en\tpreferred_abbr\tstatus\n"
            "design\tconcept\t设计\tdesign\t\tactive\n"
        ),
        aliases=(
            "# alias\tconcept_id\tlang\tkind\n"
            "设计\tdesign\tzh\tpreferred\n"
            "design\tdesign\ten\tpreferred\n"
        ),
        evidence="design\thttps://example.invalid/design\n",
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
            "--translation-dict",
            "--no-vale",
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    out_path = out_dir / "translation_dict.json"
    assert out_path.exists()

    data = json.loads(out_path.read_text("utf-8"))
    assert data["schema_version"] == 2
    assert "zh2en" in data and "en2zh" in data
    assert "en2zh_short" in data

    manifest = json.loads((out_dir / "registry_exports.json").read_text("utf-8"))
    assert manifest["translation_dict"] == out_path.as_posix()
