from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_proper_names_ledger.py"

LEDGER_TEMPLATE = """# fixture ledger
# --- EXCLUDE_FROM_IME ---
ENN\tregistry:enn:preferred_en (organization)
EUROfusion	registry:eurofusion:preferred_en (organization)
欧洲聚变能组织\tregistry:eurofusion:preferred_zh (organization)
# --- ALLOW_IN_IME ---
新奥\tretained Chinese organization name
"""


def _run(args: list[str], *, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )


def _write_terms_dir(root: Path, *, ledger: str | None = LEDGER_TEMPLATE) -> Path:
    terms_dir = root / "terms"
    registry = terms_dir / "registry"
    registry.mkdir(parents=True)

    (terms_dir / "allowlist_zh.txt").write_text("新奥\n托卡马克\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text(
        "ENN\nEUROfusion\nITER\n", encoding="utf-8"
    )
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text(
        "# alias\tpreferred\nENN\tENN\n", encoding="utf-8"
    )
    (registry / "concepts.tsv").write_text(
        "# concept_id\tcategory\tpreferred_zh\tpreferred_en\n"
        "enn\torganization\t新奥\tENN\n"
        "eurofusion\torganization\t欧洲聚变能组织\tEUROfusion\n",
        encoding="utf-8",
    )
    if ledger is not None:
        (terms_dir / "proper_names.txt").write_text(ledger, encoding="utf-8")
    return terms_dir


def _build(
    terms_dir: Path, out_dir: Path, *extra: str
) -> subprocess.CompletedProcess[str]:
    return _run(
        [
            "-m",
            "pipeline.build_terms",
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(out_dir),
            "--output",
            "domain_terms.txt",
            *extra,
        ]
    )


def _wordlist(out_dir: Path) -> list[str]:
    return [
        line.strip()
        for line in (out_dir / "domain_terms.txt").read_text("utf-8").splitlines()
        if line.strip()
    ]


def test_build_terms_applies_proper_name_ledger(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(tmp_path)
    out_dir = tmp_path / "out"

    proc = _build(terms_dir, out_dir)
    assert proc.returncode == 0, proc.stderr

    terms = _wordlist(out_dir)
    assert "新奥" in terms
    assert "ITER" in terms
    assert "ENN" not in terms
    assert "EUROfusion" not in terms

    stats = json.loads((out_dir / "domain_terms_build_stats.json").read_text("utf-8"))
    assert stats["proper_name_exclude_file"] == str(terms_dir / "proper_names.txt")
    assert stats["counts"]["proper_name_excluded"] == 2
    assert stats["proper_name_excluded_terms"] == ["ENN", "EUROfusion"]


def test_build_terms_can_disable_ledger(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(tmp_path)
    out_dir = tmp_path / "out"

    proc = _build(terms_dir, out_dir, "--no-exclude-file")
    assert proc.returncode == 0, proc.stderr
    terms = _wordlist(out_dir)
    assert "ENN" in terms
    assert "EUROfusion" in terms

    stats = json.loads((out_dir / "domain_terms_build_stats.json").read_text("utf-8"))
    assert stats["proper_name_exclude_file"] is None
    assert stats["counts"]["proper_name_excluded"] == 0


def test_build_terms_excludes_synonym_target(tmp_path: Path) -> None:
    """An alias must not smuggle an excluded preferred form into the wordlist."""

    terms_dir = _write_terms_dir(
        tmp_path,
        ledger=(
            "# fixture ledger\n"
            "# --- EXCLUDE_FROM_IME ---\n"
            "新奥能源\tregistry:enn:preferred_zh (organization)\n"
            "# --- ALLOW_IN_IME ---\n"
            "新奥\tretained Chinese organization name\n"
        ),
    )
    (terms_dir / "synonyms.tsv").write_text(
        "# alias\tpreferred\nENN\t新奥能源\n", encoding="utf-8"
    )
    out_dir = tmp_path / "out"

    proc = _build(terms_dir, out_dir)
    assert proc.returncode == 0, proc.stderr
    terms = _wordlist(out_dir)
    assert "新奥能源" not in terms
    assert "ENN" not in terms
    assert "新奥" in terms


def test_build_terms_rejects_missing_explicit_exclude_file(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(tmp_path)
    out_dir = tmp_path / "out"

    proc = _build(terms_dir, out_dir, "--exclude-file", str(tmp_path / "nope.txt"))
    assert proc.returncode != 0
    assert "--exclude-file not found" in proc.stderr


def test_checker_self_test_passes() -> None:
    proc = _run([str(CHECKER), "--self-test"])
    assert proc.returncode == 0, proc.stderr


def test_checker_fails_on_wordlist_leak(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(tmp_path)
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("新奥\nENN\n", encoding="utf-8")

    proc = _run(
        [str(CHECKER), "--terms-dir", str(terms_dir), "--wordlist", str(wordlist)]
    )
    assert proc.returncode == 1
    assert "WORDLIST_LEAK" in proc.stderr


def test_checker_fails_on_missing_ledger_entry(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(
        tmp_path,
        ledger=(
            "# fixture ledger\n"
            "# --- EXCLUDE_FROM_IME ---\n"
            "ENN\tregistry:enn:preferred_en (organization)\n"
            "# --- ALLOW_IN_IME ---\n"
            "新奥\tretained Chinese organization name\n"
        ),
    )
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("新奥\n", encoding="utf-8")

    proc = _run(
        [str(CHECKER), "--terms-dir", str(terms_dir), "--wordlist", str(wordlist)]
    )
    assert proc.returncode == 1
    assert "LEDGER_MISSING_ENTRY" in proc.stderr


def test_checker_fails_on_unknown_ledger_entry(tmp_path: Path) -> None:
    terms_dir = _write_terms_dir(
        tmp_path,
        ledger=(
            "# fixture ledger\n"
            "# --- EXCLUDE_FROM_IME ---\n"
            "ENN\tregistry:enn:preferred_en (organization)\n"
            "EUROfusion\tregistry:eurofusion:preferred_en (organization)\n"
            "Bogus Name\tregistry:nope:preferred_en (company)\n"
            "# --- ALLOW_IN_IME ---\n"
            "新奥\tretained Chinese organization name\n"
        ),
    )
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("新奥\n", encoding="utf-8")

    proc = _run(
        [str(CHECKER), "--terms-dir", str(terms_dir), "--wordlist", str(wordlist)]
    )
    assert proc.returncode == 1
    assert "LEDGER_UNKNOWN_ENTRY" in proc.stderr


def test_repo_ledger_matches_repo_registry_and_wordlist(tmp_path: Path) -> None:
    """Repo-level guard: the shipped ledger must cover the shipped registry."""

    out_dir = tmp_path / "out"
    proc = _build(REPO_ROOT / "terms", out_dir)
    assert proc.returncode == 0, proc.stderr

    terms = _wordlist(out_dir)
    for latin in ("ENN", "EUROfusion", "ICRP"):
        assert latin not in terms
    for retained in (
        "新奥",
        "欧洲聚变能组织",
        "聚变能源机构",
        "等离子体物理研究所",
        "联邦聚变系统",
        "通用原子能",
        "国际原子能机构",
        "马克斯·普朗克等离子体物理研究所",
        "核工业西南物理研究院",
    ):
        assert retained in terms

    check = _run(
        [
            str(CHECKER),
            "--terms-dir",
            str(REPO_ROOT / "terms"),
            "--wordlist",
            str(out_dir / "domain_terms.txt"),
        ]
    )
    assert check.returncode == 0, check.stderr


def _write_release_fixture(
    tmp_path: Path, *, ledger: str | None
) -> tuple[Path, Path, Path, Path]:
    terms_dir = _write_terms_dir(tmp_path, ledger=ledger)
    config = tmp_path / "config.toml"
    config.write_text("\n", encoding="utf-8")
    return terms_dir, config, tmp_path / "stage", tmp_path / "out.tar.gz"


def test_release_pack_runs_ledger_gate(tmp_path: Path) -> None:
    from pipeline.release_pack import build_release_pack

    terms_dir, config, stage_dir, tar_path = _write_release_fixture(
        tmp_path, ledger=LEDGER_TEMPLATE
    )
    res = build_release_pack(
        tag="v2026.10.30",
        stage_dir=stage_dir,
        tar_path=tar_path,
        terms_dir=terms_dir,
        config=config,
        commit="a" * 40,
        generated_at="2026-10-30T00:00:00Z",
        include_terms_sources=True,
        force=False,
    )
    assert res.tar_path.exists()
    staged = (stage_dir / "domain_terms.txt").read_text("utf-8")
    assert "ENN" not in staged.splitlines()
    assert (stage_dir / "terms" / "proper_names.txt").exists()


def test_release_pack_blocks_on_ledger_inconsistency(tmp_path: Path) -> None:
    """The pack gate must fail when the ledger does not mirror the registry."""

    from pipeline.release_pack import build_release_pack

    stale = (
        "# fixture ledger (missing the acme concept)\n"
        "# --- EXCLUDE_FROM_IME ---\n"
        "ENN\tregistry:enn:preferred_en (organization)\n"
        "EUROfusion\tregistry:eurofusion:preferred_en (organization)\n"
        "欧洲聚变能组织\tregistry:eurofusion:preferred_zh (organization)\n"
        "# --- ALLOW_IN_IME ---\n"
        "新奥\tretained Chinese organization name\n"
    )
    terms_dir, config, stage_dir, tar_path = _write_release_fixture(
        tmp_path, ledger=stale
    )
    (terms_dir / "registry" / "concepts.tsv").write_text(
        "# concept_id\tcategory\tpreferred_zh\tpreferred_en\n"
        "enn\torganization\t新奥\tENN\n"
        "eurofusion\torganization\t欧洲聚变能组织\tEUROfusion\n"
        "acme\tcompany\t托卡马克\tAcme\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as excinfo:
        build_release_pack(
            tag="v2026.10.30",
            stage_dir=stage_dir,
            tar_path=tar_path,
            terms_dir=terms_dir,
            config=config,
            commit="a" * 40,
            generated_at="2026-10-30T00:00:00Z",
            include_terms_sources=False,
            force=False,
        )
    assert "LEDGER_MISSING_ENTRY" in str(excinfo.value)
