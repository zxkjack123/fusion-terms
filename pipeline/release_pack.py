from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path

from pipeline.generate_manifest import generate_manifest
from pipeline.verify_release_contract import verify_release_contract


@dataclass(frozen=True)
class PackResult:
    stage_dir: Path
    manifest_path: Path
    tar_path: Path


def _run_module(module: str, args: list[str]) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", module, *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    msg = "\n".join([s for s in [stderr, stdout] if s])
    raise SystemExit(f"release_pack failed: module {module} exited {proc.returncode}\n{msg}")


def _iter_files_recursive(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file():
            files.append(p)
    files.sort(key=lambda x: x.relative_to(root).as_posix())
    return files


def _copy_terms_sources(*, terms_dir: Path, stage_dir: Path) -> list[str]:
    """Copy selected source-of-truth files into stage_dir.

    Returns: relative paths included.
    """

    rels: list[str] = []
    dst_terms = stage_dir / "terms"
    dst_terms.mkdir(parents=True, exist_ok=True)

    for name in [
        "allowlist_zh.txt",
        "allowlist_en.txt",
        "denylist.txt",
        "synonyms.tsv",
    ]:
        src = terms_dir / name
        if not src.exists():
            continue
        dst = dst_terms / name
        shutil.copy2(src, dst)
        rels.append(str(dst.relative_to(stage_dir).as_posix()))

    return rels


def _copy_terms_registry(*, terms_dir: Path, stage_dir: Path) -> list[str]:
    rels: list[str] = []
    src_registry = terms_dir / "registry"
    if not src_registry.exists():
        return rels

    dst_registry = stage_dir / "terms" / "registry"
    dst_registry.mkdir(parents=True, exist_ok=True)

    for name in ["concepts.tsv", "aliases.tsv", "evidence.tsv"]:
        src = src_registry / name
        if not src.exists():
            continue
        dst = dst_registry / name
        shutil.copy2(src, dst)
        rels.append(str(dst.relative_to(stage_dir).as_posix()))

    return rels


def _tar_filter_stable(ti: tarfile.TarInfo) -> tarfile.TarInfo:
    # Optional reproducibility: normalize owner + mtime to improve cache hits.
    ti.uid = 0
    ti.gid = 0
    ti.uname = ""
    ti.gname = ""
    ti.mtime = 0
    return ti


def build_release_pack(
    *,
    tag: str,
    stage_dir: Path,
    tar_path: Path,
    terms_dir: Path = Path("terms"),
    config: Path = Path("config.toml"),
    commit: str | None = None,
    generated_at: str | None = None,
    include_terms_sources: bool = True,
    include_registry_sources: bool = False,
    include_registry_exports: bool = False,
    include_query_expansions: bool = False,
    include_tag_rules: bool = False,
    include_substitutions: bool = False,
    include_vale_substitute: bool = False,
    force: bool = False,
) -> PackResult:
    """Build a v1 release artifact tarball from a clean staging directory.

    The staged directory is the release root. The tarball includes its contents
    at top level (i.e., extracting into an empty dir yields domain_terms.txt etc).
    """

    stage_dir = stage_dir.expanduser()
    tar_path = tar_path.expanduser()
    terms_dir = terms_dir.expanduser()
    config = config.expanduser()

    if stage_dir.exists():
        if not force:
            raise SystemExit(f"release_pack failed: stage dir exists (use --force): {stage_dir}")
        shutil.rmtree(stage_dir)

    stage_dir.mkdir(parents=True, exist_ok=True)

    # Safety: never write the output tarball inside staging root.
    try:
        stage_r = stage_dir.resolve()
        tar_r = tar_path.resolve()
        if tar_r == stage_r or stage_r in tar_r.parents:
            raise SystemExit(
                "release_pack failed: output tar path must not be inside stage dir "
                f"(stage={stage_dir}, out={tar_path})"
            )
    except FileNotFoundError:
        # Some parents may not exist yet; still safe to continue.
        pass

    # 1) Build core v1 artifacts directly into staging root.
    _run_module(
        "pipeline.build_terms",
        [
            "--config",
            str(config),
            "--terms-dir",
            str(terms_dir),
            "--out-dir",
            str(stage_dir),
            "--output",
            "domain_terms.txt",
        ],
    )

    rel_files: list[str] = ["domain_terms.txt"]
    if (stage_dir / "domain_terms_build_stats.json").exists():
        rel_files.append("domain_terms_build_stats.json")

    # 2) Optional: include sources of truth for auditability.
    if include_terms_sources:
        rel_files.extend(_copy_terms_sources(terms_dir=terms_dir, stage_dir=stage_dir))
    if include_registry_sources:
        rel_files.extend(_copy_terms_registry(terms_dir=terms_dir, stage_dir=stage_dir))

    # 3) Optional: export registry-derived consumer artifacts into staging.
    if include_registry_exports:
        out_artifacts = stage_dir / "artifacts"
        args = ["--config", str(config), "--terms-dir", str(terms_dir), "--out-dir", str(out_artifacts)]
        if include_query_expansions:
            args.append("--query-expansions")
        if include_tag_rules:
            args.append("--tag-rules")
        if include_substitutions:
            args.append("--substitutions")
        if include_vale_substitute:
            args.append("--vale-substitute")
        _run_module("pipeline.export_registry", args)

        # Collect all files we just created under artifacts/.
        for f in _iter_files_recursive(out_artifacts):
            rel_files.append(str(f.relative_to(stage_dir).as_posix()))

    # 4) Generate manifest within staging root.
    manifest = generate_manifest(
        root=stage_dir,
        version=tag,
        commit=commit,
        generated_at=generated_at,
        files=sorted(set(rel_files)),
        counts_from=None,
        repo_root=None,
    )
    manifest_path = stage_dir / "fusion_terms_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.as_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    # 5) Gate: staged release must be self-consistent.
    verify_release_contract(root=stage_dir)

    # 6) Pack.
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    if tar_path.exists():
        tar_path.unlink()

    all_files = _iter_files_recursive(stage_dir)
    with tarfile.open(tar_path, mode="w:gz") as tf:
        for full in all_files:
            rel = full.relative_to(stage_dir).as_posix()
            tf.add(full, arcname=rel, filter=_tar_filter_stable)

    return PackResult(stage_dir=stage_dir, manifest_path=manifest_path, tar_path=tar_path)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Build fusion-terms release artifact tarball (staging -> tar.gz)."
    )
    p.add_argument("--tag", required=True, help="Release tag (e.g. v2026.02.09)")
    p.add_argument("--config", default="config.toml", help="Path to config.toml")
    p.add_argument("--terms-dir", default="terms", help="Directory containing allow/deny/synonyms")
    p.add_argument(
        "--stage-dir",
        default=None,
        help="Staging directory (release root). Default: dist/stage/<tag>/",
    )
    p.add_argument(
        "--out",
        default=None,
        help="Output tar.gz path. Default: dist/fusion-terms-artifacts-<tag>.tar.gz",
    )
    p.add_argument(
        "--commit",
        default=None,
        help="Commit SHA (40-hex). If omitted, generate_manifest will try git.",
    )
    p.add_argument(
        "--generated-at",
        default=None,
        help="UTC ISO8601 timestamp for manifest (e.g. 2026-02-09T00:00:00Z).",
    )
    p.add_argument(
        "--no-terms-sources",
        action="store_true",
        help="Do not include terms/*.txt and terms/synonyms.tsv in the release package.",
    )
    p.add_argument(
        "--include-registry-sources",
        action="store_true",
        help="Include terms/registry/*.tsv in the release package.",
    )
    p.add_argument(
        "--include-registry-exports",
        action="store_true",
        help="Export registry-derived consumer artifacts into artifacts/ and include them.",
    )
    p.add_argument(
        "--query-expansions",
        action="store_true",
        help="When exporting registry, also include artifacts/query_expansions.json",
    )
    p.add_argument(
        "--tag-rules",
        action="store_true",
        help="When exporting registry, also include artifacts/tag_rules.jsonl",
    )
    p.add_argument(
        "--substitutions",
        action="store_true",
        help="When exporting registry, also include artifacts/terminology_substitutions.tsv",
    )
    p.add_argument(
        "--vale-substitute",
        action="store_true",
        help="When exporting registry, also include artifacts/vale/terminology_substitute.yml",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Delete existing stage dir before building.",
    )

    args = p.parse_args()

    stage_dir = Path(args.stage_dir) if args.stage_dir else (Path("dist") / "stage" / args.tag)
    out_path = (
        Path(args.out)
        if args.out
        else (Path("dist") / f"fusion-terms-artifacts-{args.tag}.tar.gz")
    )

    res = build_release_pack(
        tag=args.tag,
        stage_dir=stage_dir,
        tar_path=out_path,
        terms_dir=Path(args.terms_dir),
        config=Path(args.config),
        commit=args.commit,
        generated_at=args.generated_at,
        include_terms_sources=not args.no_terms_sources,
        include_registry_sources=bool(args.include_registry_sources),
        include_registry_exports=bool(args.include_registry_exports),
        include_query_expansions=bool(args.query_expansions),
        include_tag_rules=bool(args.tag_rules),
        include_substitutions=bool(args.substitutions),
        include_vale_substitute=bool(args.vale_substitute),
        force=bool(args.force),
    )

    print(f"staged: {res.stage_dir}")
    print(f"wrote manifest: {res.manifest_path}")
    print(f"wrote tarball: {res.tar_path}")


if __name__ == "__main__":
    main()
