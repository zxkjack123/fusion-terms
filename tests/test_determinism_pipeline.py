from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _write_stub_rime_importer(script_path: Path) -> None:
    """Write a deterministic stub for rime_import_wordlist.py.

    The real script is an external dependency on the user's machine.
    For tests we provide a minimal deterministic implementation that
    produces a stable payload.
    """

    script_path.write_text(
        """#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--import', dest='do_import', action='store_true')
    args = p.parse_args()

    inp = Path(args.input)
    outp = Path(args.output)
    outp.parent.mkdir(parents=True, exist_ok=True)

    # Deterministic: one output row per term, stable ordering.
    terms = [
        ln.strip()
        for ln in inp.read_text('utf-8', errors='ignore').splitlines()
        if ln.strip()
    ]
    terms = sorted(set(terms))

    # Emit a 3-column TSV: text, code, weight
    # Use a simple stable "code" derived from the term.
    lines = []
    for t in terms:
        code = t.lower()
        lines.append(f"{t}\t{code}\t1")

    outp.write_text(
        "\\n".join(lines) + ("\\n" if lines else ""),
        encoding='utf-8',
    )

    # --import is ignored in the stub (no side effects).


if __name__ == '__main__':
    main()
""",
        encoding="utf-8",
    )
    script_path.chmod(0o755)


def test_extract_candidates_tsv_is_byte_identical_across_runs(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "tests" / "fixtures" / "corpus"

    out_dir = tmp_path / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    args = [
        sys.executable,
        "-m",
        "pipeline.extract_candidates",
        "--source-root",
        str(corpus_root),
        "--out-dir",
        str(out_dir),
        "--max-files",
        "100",
    ]

    p1 = subprocess.run(
        args,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p1.returncode == 0, f"run1 stdout:\n{p1.stdout}\nstderr:\n{p1.stderr}"

    en1 = (out_dir / "candidates_en.tsv").read_bytes()
    zh1 = (out_dir / "candidates_zh.tsv").read_bytes()

    p2 = subprocess.run(
        args,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    assert p2.returncode == 0, f"run2 stdout:\n{p2.stdout}\nstderr:\n{p2.stderr}"

    en2 = (out_dir / "candidates_en.tsv").read_bytes()
    zh2 = (out_dir / "candidates_zh.tsv").read_bytes()

    assert en2 == en1
    assert zh2 == zh1


def test_end_to_end_chain_is_deterministic_on_fixture_corpus(
    tmp_path: Path,
) -> None:
    """Run extract -> build_terms -> rime_export twice.

    Compare output hashes across two runs.
    """

    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "tests" / "fixtures" / "corpus"

    def run_chain(run_root: Path) -> dict[str, str]:
        out_dir = run_root / "artifacts"
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) extract
        p = subprocess.run(
            [
                sys.executable,
                "-m",
                "pipeline.extract_candidates",
                "--source-root",
                str(corpus_root),
                "--out-dir",
                str(out_dir),
                "--max-files",
                "100",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"extract stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

        # 2) build terms (use a small, hermetic terms dir)
        terms_dir = run_root / "terms"
        terms_dir.mkdir(parents=True, exist_ok=True)
        (terms_dir / "allowlist_en.txt").write_text(
            "ITER\nNBI\n",
            encoding="utf-8",
        )
        (terms_dir / "allowlist_zh.txt").write_text("托卡马克\n", encoding="utf-8")
        (terms_dir / "denylist.txt").write_text("", encoding="utf-8")
        (terms_dir / "synonyms.tsv").write_text("", encoding="utf-8")

        p = subprocess.run(
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
        assert p.returncode == 0, f"build stdout:\n{p.stdout}\nstderr:\n{p.stderr}"

        # 3) rime export (use stub importer)
        stub_script = run_root / "rime_import_wordlist.py"
        _write_stub_rime_importer(stub_script)

        p = subprocess.run(
            [
                sys.executable,
                "-m",
                "pipeline.rime_export",
                "--input",
                str(out_dir / "domain_terms.txt"),
                "--output",
                str(out_dir / ".rime_import_rime_ice.txt"),
                "--rime-script",
                str(stub_script),
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, (
            f"rime_export stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )

        # Hash a minimal set of "contract" artifacts.
        return {
            "candidates_en.tsv": _sha256_file(out_dir / "candidates_en.tsv"),
            "candidates_zh.tsv": _sha256_file(out_dir / "candidates_zh.tsv"),
            "domain_terms.txt": _sha256_file(out_dir / "domain_terms.txt"),
            ".rime_import_rime_ice.txt": _sha256_file(
                out_dir / ".rime_import_rime_ice.txt"
            ),
        }

    h1 = run_chain(tmp_path / "run1")
    h2 = run_chain(tmp_path / "run2")

    assert h2 == h1
