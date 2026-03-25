from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


def _load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def _run_importer(
    *,
    script: Path,
    input_path: Path,
    output_path: Path,
) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(script),
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]
    return subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )


def _render_header(*, name: str, version: str) -> str:
    # Minimal Rime dictionary YAML header.
    return "\n".join(
        [
            "# Rime dictionary",
            "# encoding: utf-8",
            "---",
            f"name: {name}",
            f"version: {version!r}",
            "sort: by_weight",
            "use_preset_vocabulary: false",
            "columns:",
            "  - text",
            "  - code",
            "  - weight",
            "...",
            "",
        ]
    )


def generate_dict_yaml(
    *,
    input_wordlist: Path,
    output_yaml: Path,
    rime_script: Path,
    dict_name: str,
    dict_version: str,
) -> None:
    if not input_wordlist.exists():
        raise SystemExit(f"input wordlist not found: {input_wordlist}")
    if not rime_script.exists():
        raise SystemExit(f"rime importer script not found: {rime_script}")

    output_yaml.parent.mkdir(parents=True, exist_ok=True)

    # Use a temp payload file; do not commit it as an artifact.
    with tempfile.NamedTemporaryFile(
        mode="w+",
        encoding="utf-8",
        prefix=".fusion_terms_payload_",
        suffix=".txt",
        dir=str(output_yaml.parent),
        delete=False,
    ) as tf:
        payload_path = Path(tf.name)

    try:
        proc = _run_importer(
            script=rime_script,
            input_path=input_wordlist,
            output_path=payload_path,
        )
        if proc.stdout:
            print(proc.stdout)
        if proc.returncode != 0:
            if proc.stderr:
                print(proc.stderr)
            raise SystemExit(proc.returncode)

        payload = payload_path.read_text("utf-8")
        # The importer should generate a 3-column TSV (text, code, weight).
        # We keep it as-is and wrap it into a .dict.yaml.

        header = _render_header(name=dict_name, version=dict_version)
        output_yaml.write_text(header + payload, encoding="utf-8")
        print(f"wrote baked dict: {output_yaml}")
    finally:
        # Best-effort cleanup; payload can be regenerated any time.
        if payload_path.exists():
            try:
                payload_path.unlink()
            except Exception:
                pass  # best-effort temp cleanup


def main() -> None:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", default="config.toml")
    pre_args, _ = pre.parse_known_args()

    config_path = Path(pre_args.config).expanduser()
    cfg = _load_config(config_path)
    rime_cfg = cfg.get("rime", {}) if isinstance(cfg, dict) else {}
    default_rime_script = str(
        (Path("~").expanduser() / ".local/bin/rime_import_wordlist.py")
    )
    if isinstance(rime_cfg, dict):
        script_val = rime_cfg.get("import_script")
        if isinstance(script_val, str) and script_val.strip():
            default_rime_script = script_val.strip()

    parser = argparse.ArgumentParser(
        description=(
            "Generate a baked Rime dictionary (.dict.yaml) from "
            "artifacts/domain_terms.txt via the existing importer script."
        )
    )
    parser.add_argument(
        "--config",
        default=str(config_path),
        help="Path to config.toml",
    )
    parser.add_argument(
        "--input",
        default="artifacts/domain_terms.txt",
        help="Input wordlist (one term per line)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output dict YAML path "
            "(default: <out-dir>/fusion_terms.dict.yaml)"
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Artifacts output dir (overrides config)",
    )
    parser.add_argument(
        "--rime-script",
        default=default_rime_script,
        help="Existing rime_import_wordlist.py path",
    )
    parser.add_argument(
        "--name",
        default="fusion_terms",
        help="Dictionary name field inside YAML (default: fusion_terms)",
    )
    parser.add_argument(
        "--version",
        default="0.1",
        help="Dictionary version string (default: 0.1)",
    )

    args = parser.parse_args()

    cfg = _load_config(Path(args.config).expanduser())
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()

    input_wordlist = Path(args.input).expanduser()
    rime_script = Path(args.rime_script).expanduser()

    output_yaml = (
        Path(args.output).expanduser()
        if args.output
        else (out_dir / "fusion_terms.dict.yaml")
    )

    generate_dict_yaml(
        input_wordlist=input_wordlist,
        output_yaml=output_yaml,
        rime_script=rime_script,
        dict_name=str(args.name),
        dict_version=str(args.version),
    )


if __name__ == "__main__":
    main()
