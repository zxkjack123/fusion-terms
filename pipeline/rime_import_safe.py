from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class BackupItem:
    original: str
    backup: str
    kind: str  # file|dir


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _now_backup_name() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _run_importer(
    *,
    script: Path,
    input_path: Path,
    output_path: Path,
    do_import: bool,
) -> subprocess.CompletedProcess[str]:
    # Backward-compatible wrapper for older callers/tests.
    return _run_importer_v2(
        script=script,
        input_path=input_path,
        output_path=output_path,
        do_import=do_import,
        dict_name="rime_ice",
        include_non_cjk=False,
        rime_user_dir=None,
        no_restart_fcitx=False,
    )


def _run_importer_v2(
    *,
    script: Path,
    input_path: Path,
    output_path: Path,
    do_import: bool,
    dict_name: str,
    include_non_cjk: bool,
    rime_user_dir: Path | None,
    no_restart_fcitx: bool,
) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(script),
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]

    # Only add flags when they matter, to keep compatibility with
    # user's existing scripts.
    if include_non_cjk:
        cmd.append("--include-non-cjk")

    if do_import:
        cmd.extend(["--dict-name", dict_name])
        if rime_user_dir is not None:
            cmd.extend(["--rime-user-dir", str(rime_user_dir)])
        if no_restart_fcitx:
            cmd.append("--no-restart-fcitx")
        cmd.append("--import")

    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def _copy_any(src: Path, dst: Path) -> None:
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def create_backup(
    *,
    backup_root: Path,
    backup_name: str,
    paths: list[Path],
) -> Path:
    """Create a backup snapshot and return manifest path."""

    snapshot_dir = backup_root / backup_name
    _ensure_dir(snapshot_dir)

    items: list[BackupItem] = []

    for p in paths:
        if not p.exists():
            continue
        rel = str(p).lstrip("/")
        backup_path = snapshot_dir / rel
        kind = "dir" if p.is_dir() else "file"
        _copy_any(p, backup_path)
        items.append(
            BackupItem(
                original=str(p),
                backup=str(backup_path),
                kind=kind,
            )
        )

    if not items:
        raise SystemExit(
            "safe import failed: no existing backup paths found; "
            "refusing to import"
        )

    manifest = {
        "schema_version": 1,
        "backup_root": str(backup_root),
        "backup_name": backup_name,
        "snapshot_dir": str(snapshot_dir),
        "items": [item.__dict__ for item in items],
    }

    manifest_path = snapshot_dir / "manifest.json"
    manifest_path.write_text(
        (
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n"
        ),
        encoding="utf-8",
    )
    return manifest_path


def rollback_from_manifest(manifest_path: Path) -> None:
    if not manifest_path.exists():
        raise SystemExit(
            f"rollback failed: manifest not found: {manifest_path}"
        )

    data = json.loads(manifest_path.read_text("utf-8"))
    items = data.get("items", [])
    if not isinstance(items, list) or not items:
        raise SystemExit(f"rollback failed: invalid manifest: {manifest_path}")

    # Restore in deterministic order to reduce surprises.
    items_sorted = sorted(items, key=lambda d: str(d.get("original", "")))

    for it in items_sorted:
        orig = Path(it["original"]).expanduser()
        bak = Path(it["backup"]).expanduser()
        if not bak.exists():
            raise SystemExit(f"rollback failed: missing backup path: {bak}")

        # Ensure parent exists.
        orig.parent.mkdir(parents=True, exist_ok=True)

        def _remove_existing(p: Path) -> None:
            if not p.exists():
                return
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p)
            else:
                p.unlink()

        if bak.is_dir():
            if orig.exists():
                _remove_existing(orig)
            shutil.copytree(bak, orig)
        else:
            if orig.exists():
                _remove_existing(orig)
            shutil.copy2(bak, orig)

    print(
        f"rollback OK: restored {len(items_sorted)} paths from "
        f"{manifest_path}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Safely generate a Rime import payload and (optionally) "
            "import into userdb with backups and rollback."
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
            "Rime dict_name to import into "
            "(passed through to rime_import_wordlist.py). "
            "Default: rime_ice (for rime-ice)."
        ),
    )
    parser.add_argument(
        "--include-non-cjk",
        action="store_true",
        help=(
            "Also include non-CJK terms when generating payload "
            "(passed through)."
        ),
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
        help=(
            "Do not auto-restart fcitx when the Rime userdb is locked "
            "(passed through)."
        ),
    )
    parser.add_argument(
        "--import",
        dest="do_import",
        action="store_true",
        help="Also import into Rime userdb (requires backups)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Only generate import payload; do not import "
            "(overrides --import)"
        ),
    )
    parser.add_argument(
        "--backup-path",
        action="append",
        default=[],
        help=(
            "Path to back up before importing (repeatable). "
            "Can be file or dir."
        ),
    )
    parser.add_argument(
        "--backup-root",
        default="artifacts/rime_backups",
        help="Backup root directory (default: artifacts/rime_backups)",
    )
    parser.add_argument(
        "--backup-name",
        default=None,
        help=(
            "Backup snapshot name (default: timestamp). "
            "Useful for deterministic tests."
        ),
    )
    parser.add_argument(
        "--rollback",
        default=None,
        help="Rollback using a given backup manifest.json path and exit.",
    )

    args = parser.parse_args()

    if args.rollback:
        rollback_from_manifest(Path(args.rollback).expanduser())
        return

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    script_path = Path(args.rime_script).expanduser()

    if not input_path.exists():
        raise SystemExit(f"input wordlist not found: {input_path}")
    if not script_path.exists():
        raise SystemExit(f"rime importer script not found: {script_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Step 1) Always generate payload (safe, reproducible).
    gen = _run_importer_v2(
        script=script_path,
        input_path=input_path,
        output_path=output_path,
        do_import=False,
        dict_name=args.dict_name,
        include_non_cjk=bool(args.include_non_cjk),
        rime_user_dir=(
            Path(args.rime_user_dir).expanduser()
            if args.rime_user_dir
            else None
        ),
        no_restart_fcitx=bool(args.no_restart_fcitx),
    )
    if gen.stdout:
        print(gen.stdout)
    if gen.returncode != 0:
        if gen.stderr:
            print(gen.stderr)
        raise SystemExit(gen.returncode)

    # Explicit dry-run: stop here.
    if args.dry_run or not args.do_import:
        print(f"generated import payload: {output_path}")
        print(
            "dry-run: no import performed"
            if args.dry_run
            else "no --import: payload only"
        )
        return

    # Step 2) Backup paths before import.
    backup_root = Path(args.backup_root).expanduser()
    backup_name = args.backup_name or _now_backup_name()
    backup_paths = [Path(p).expanduser() for p in args.backup_path]

    if not backup_paths:
        raise SystemExit(
            "safe import failed: --import requires at least one "
            "--backup-path (file/dir) to enable rollback"
        )

    _ensure_dir(backup_root)
    manifest_path = create_backup(
        backup_root=backup_root,
        backup_name=backup_name,
        paths=backup_paths,
    )
    print(f"backup created: {manifest_path}")

    # Step 3) Import.
    imp = _run_importer_v2(
        script=script_path,
        input_path=input_path,
        output_path=output_path,
        do_import=True,
        dict_name=args.dict_name,
        include_non_cjk=bool(args.include_non_cjk),
        rime_user_dir=(
            Path(args.rime_user_dir).expanduser()
            if args.rime_user_dir
            else None
        ),
        no_restart_fcitx=bool(args.no_restart_fcitx),
    )
    if imp.stdout:
        print(imp.stdout)

    if imp.returncode != 0:
        if imp.stderr:
            print(imp.stderr)
        # Auto-rollback on failure.
        rollback_from_manifest(manifest_path)
        raise SystemExit(imp.returncode)

    print("import OK")
    print("verification tips:")
    print("- restart Fcitx if needed")
    print(
        "- try a few fixed acceptance terms "
        "(ITER/EAST/NBI/H-mode/q95/β_N/τ_E/托卡马克)"
    )
    print(
        "rollback command: python -m pipeline.rime_import_safe "
        f"--rollback {manifest_path}"
    )


if __name__ == "__main__":
    main()
