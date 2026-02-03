from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Sync artifacts/domain_terms.txt to Fcitx/Rime wordlists directory"
        )
    )
    parser.add_argument(
        "--input",
        default="artifacts/domain_terms.txt",
        help="Source wordlist (one term per line)",
    )
    parser.add_argument(
        "--dest",
        default=str(Path("~/.config/fcitx/rime/wordlists/domain_terms.txt")),
        help="Destination path (default: fcitx rime wordlists)",
    )

    args = parser.parse_args()

    src = Path(args.input).expanduser()
    dst = Path(args.dest).expanduser()

    if not src.exists():
        raise SystemExit(f"input not found: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"synced {src} -> {dst}")


if __name__ == "__main__":
    main()
