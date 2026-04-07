from __future__ import annotations

import argparse
import os
import shutil
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


def main() -> None:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", default="config.toml")
    pre_args, _ = pre.parse_known_args()
    config_path = Path(pre_args.config).expanduser()
    cfg = _load_config(config_path)
    rime_cfg = cfg.get("rime", {}) if isinstance(cfg, dict) else {}

    default_dest = str(Path("~/.config/fcitx/rime/wordlists/domain_terms.txt"))
    if isinstance(rime_cfg, dict):
        v = rime_cfg.get("sync_dest")
        if isinstance(v, str) and v.strip():
            default_dest = v.strip()

    parser = argparse.ArgumentParser(
        description=(
            "Sync artifacts/domain_terms.txt to Fcitx/Rime wordlists directory"
        )
    )
    parser.add_argument(
        "--config",
        default=str(config_path),
        help="Path to config.toml (used for [rime] defaults)",
    )
    parser.add_argument(
        "--input",
        default="artifacts/domain_terms.txt",
        help="Source wordlist (one term per line)",
    )
    parser.add_argument(
        "--dest",
        default=default_dest,
        help="Destination path (default: fcitx rime wordlists)",
    )

    args = parser.parse_args()

    src = Path(args.input).expanduser()
    dst = Path(args.dest).expanduser()

    if not src.exists():
        raise SystemExit(f"input not found: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst_tmp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=dst.parent,
            prefix=f".{dst.name}.",
            suffix=".tmp",
            delete=False,
        ) as tmpf:
            dst_tmp = Path(tmpf.name)
        shutil.copyfile(src, dst_tmp)
        os.replace(dst_tmp, dst)
    finally:
        if dst_tmp is not None:
            try:
                dst_tmp.unlink()
            except FileNotFoundError:
                pass
    print(f"synced {src} -> {dst}")


if __name__ == "__main__":
    main()
