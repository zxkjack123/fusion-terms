from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_dummy_importer(path: Path, *, payload_lines: list[str]) -> None:
    """Create a dummy importer script that writes a fixed payload TSV.

    The generator under test calls it with: python3 script --input X --output Y
    """

    payload = "".join(payload_lines)
    code = f"""#!/usr/bin/env python3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--import', dest='do_import', action='store_true')
args = parser.parse_args()

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text({payload!r}, encoding='utf-8')
"""

    path.write_text(code, encoding="utf-8")
    path.chmod(0o755)


def test_generate_baked_dict_yaml_is_deterministic_and_contains_payload(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    wordlist = tmp_path / "domain_terms.txt"
    wordlist.write_text("ITER\n托卡马克\n", encoding="utf-8")

    importer = tmp_path / "dummy_importer.py"
    _write_dummy_importer(
        importer,
        payload_lines=[
            "ITER\tITER\t100\n",
            "托卡马克\ttuo ka ma ke\t100\n",
        ],
    )

    out_yaml = tmp_path / "fusion_terms.dict.yaml"

    def run_once() -> str:
        p = subprocess.run(
            [
                sys.executable,
                "-m",
                "pipeline.generate_dict_yaml",
                "--input",
                str(wordlist),
                "--output",
                str(out_yaml),
                "--rime-script",
                str(importer),
                "--name",
                "fusion_terms",
                "--version",
                "0.1",
            ],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        assert p.returncode == 0, f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        return out_yaml.read_text("utf-8", errors="ignore")

    first = run_once()
    second = run_once()

    # No timestamps; should be byte-for-byte deterministic.
    assert first == second

    assert 'name: "fusion_terms"' in first
    assert "columns:" in first
    assert "..." in first

    # Payload present.
    assert "ITER\tITER\t100" in first
    assert "托卡马克\ttuo ka ma ke\t100" in first
