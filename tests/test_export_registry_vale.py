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


def test_export_registry_writes_vale_accept_reject(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)

    # allowlists needed for validator's forbidden/deprecated leak gate.
    (terms_dir / "allowlist_zh.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "allowlist_en.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "denylist.txt").write_text("\n", encoding="utf-8")
    (terms_dir / "synonyms.tsv").write_text("\n", encoding="utf-8")

    _write_registry_tables(
        terms_dir,
        concepts="iter\tdevice\n",
        aliases=(
            "ITER\titer\tabbr\tpreferred\n"
            "International Thermonuclear Experimental Reactor\titer\ten\talias\n"
            "Foo\titer\ten\tforbidden\n"
            "foo\titer\ten\tdeprecated\n"
        ),
        evidence="iter\thttps://www.iter.org\n",
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
        ],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

    accept = (
        (out_dir / "vale" / "accept.txt")
        .read_text("utf-8", errors="ignore")
        .splitlines()
    )
    reject = (
        (out_dir / "vale" / "reject.txt")
        .read_text("utf-8", errors="ignore")
        .splitlines()
    )

    # Accept includes preferred + alias, sorted.
    assert accept == sorted(accept)
    assert "ITER" in accept
    assert "International Thermonuclear Experimental Reactor" in accept

    # Reject includes forbidden + deprecated.
    assert reject == sorted(reject)
    assert "Foo" in reject
    assert "foo" in reject

    # Reject wins: if something is rejected it must not appear in accept.
    assert "Foo" not in accept
    assert "foo" not in accept

    manifest = json.loads((out_dir / "registry_exports.json").read_text("utf-8"))
    assert (out_dir / "vale" / "accept.txt").as_posix() == manifest["vale_accept"]
    assert (out_dir / "vale" / "reject.txt").as_posix() == manifest["vale_reject"]
    assert manifest["accept_count"] == len(accept)
    assert manifest["reject_count"] == len(reject)


def test_export_vale_terms_direct_call(tmp_path: Path) -> None:
    """Direct in-process call to export_vale_terms for coverage."""
    from pipeline.export_registry import export_vale_terms

    terms_dir = tmp_path / "terms"
    terms_dir.mkdir(parents=True, exist_ok=True)
    reg = terms_dir / "registry"
    reg.mkdir()
    (reg / "aliases.tsv").write_text(
        "# alias\tconcept_id\tlang\tkind\n"
        "ITER\titer\tabbr\tpreferred\n"
        "Bad\titer\ten\tforbidden\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "artifacts"
    out_dir.mkdir()

    result = export_vale_terms(terms_dir=terms_dir, out_dir=out_dir)
    assert result["accept_count"] >= 1
    assert result["reject_count"] >= 1

    from pathlib import Path as P

    accept_path = P(result["vale_accept"])
    reject_path = P(result["vale_reject"])
    assert accept_path.exists()
    assert reject_path.exists()
    assert "ITER" in accept_path.read_text("utf-8")
    assert "Bad" in reject_path.read_text("utf-8")
