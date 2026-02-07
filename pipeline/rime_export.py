from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Rime import file from artifacts/domain_terms.txt"
        )
    )
    parser.add_argument(
        "--input",
        default="artifacts/domain_terms.txt",
        help="Input wordlist (one term per line)",
    )
    parser.add_argument(
        "--output",
        default="artifacts/.rime_import_rime_ice.txt",
        help="Output import payload path",
    )
    parser.add_argument(
        "--rime-script",
        default=str(Path("~/.local/bin/rime_import_wordlist.py")),
        help="Existing rime_import_wordlist.py path",
    )
    parser.add_argument(
        "--dict-name",
        default="rime_ice",
        help=(
            "Rime dict_name to import into (only used with --import). "
            "Default: rime_ice (for rime-ice)."
        ),
    )
    parser.add_argument(
        "--include-non-cjk",
        action="store_true",
        help="Also include non-CJK terms (passed through to rime_import_wordlist.py).",
    )
    parser.add_argument(
        "--rime-user-dir",
        default=None,
        help=(
            "Override Rime user dir when importing (passed through). "
            "Example for fcitx-rime: ~/.config/fcitx/rime"
        ),
    )
    parser.add_argument(
        "--no-restart-fcitx",
        action="store_true",
        help="Do not auto-restart fcitx when the Rime userdb is locked (passed through).",
    )
    parser.add_argument(
        "--import",
        dest="do_import",
        action="store_true",
        help="Also import into Rime userdb",
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    script_path = Path(args.rime_script).expanduser()

    if not input_path.exists():
        raise SystemExit(f"input wordlist not found: {input_path}")
    if not script_path.exists():
        raise SystemExit(f"rime importer script not found: {script_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python3",
        str(script_path),
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]
    if args.include_non_cjk:
        cmd.append("--include-non-cjk")
    if args.do_import:
        cmd.extend(["--dict-name", args.dict_name])
        if args.rime_user_dir:
            cmd.extend(["--rime-user-dir", str(Path(args.rime_user_dir).expanduser())])
        if args.no_restart_fcitx:
            cmd.append("--no-restart-fcitx")
        cmd.append("--import")

    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout)
    if proc.returncode != 0:
        if proc.stderr:
            print(proc.stderr)
        raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
