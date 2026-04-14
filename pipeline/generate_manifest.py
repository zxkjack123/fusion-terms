from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


_SHA1_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
_TAG_RE = re.compile(r"^v\d{4}\.\d{2}\.\d{2}(?:\.\d+)?$")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_utc_iso8601() -> str:
    # Use seconds precision for stable, human-friendly manifests.
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _validate_generated_at_utc(s: str) -> str:
    # Accept a strict UTC representation.
    # - preferred: ...Z
    # - also allow: ...+00:00 (normalized to Z)
    if s.endswith("Z"):
        # Validate parseability
        try:
            datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError as e:
            raise SystemExit(
                f"invalid generated_at (expected UTC ISO8601): {s!r}"
            ) from e
        return s

    if s.endswith("+00:00"):
        try:
            datetime.fromisoformat(s)
        except ValueError as e:
            raise SystemExit(
                f"invalid generated_at (expected UTC ISO8601): {s!r}"
            ) from e
        return s.replace("+00:00", "Z")

    raise SystemExit(
        f"generated_at must be UTC ISO8601 (end with 'Z' or '+00:00'), got: {s!r}"
    )


def _git_head_commit(repo_root: Path) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode != 0:
        msg = proc.stderr.strip() or proc.stdout.strip() or "unknown error"
        raise SystemExit(f"failed to read git commit from {repo_root}: {msg}")
    sha = proc.stdout.strip()
    return sha


def _validate_commit_sha(s: str) -> str:
    if not _SHA1_RE.match(s):
        raise SystemExit(f"commit must be a 40-hex SHA, got: {s!r}")
    return s.lower()


def _validate_tag_version(s: str) -> str:
    # Keep this guardrail lightweight: tag format is strongly recommended by contract.
    # Allow other strings, but warn via strict mode in the future if needed.
    if not _TAG_RE.match(s):
        # Still accept; downstream may use non-CalVer tags.
        return s
    return s


def _is_zh_term(t: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in t)


def _load_domain_terms(path: Path) -> list[str]:
    try:
        lines = path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(f"failed to read UTF-8 domain_terms: {path} ({e})") from e

    out: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):
            # Be tolerant: contract says it *should not* exist, but consumer may ignore.
            continue
        out.append(s)
    return out


def _counts_from_build_stats(stats_path: Path) -> dict[str, int] | None:
    if not stats_path.exists():
        return None
    try:
        data = json.loads(stats_path.read_text("utf-8"))
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"failed to read UTF-8 build stats JSON: {stats_path} ({e})"
        ) from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"invalid JSON build stats: {stats_path} ({e})") from e

    counts = data.get("counts")
    if not isinstance(counts, dict):
        return None

    total = counts.get("total")
    zh = counts.get("zh")
    en = counts.get("en")
    if not isinstance(total, int):
        return None
    if not isinstance(zh, int):
        return None
    if not isinstance(en, int):
        return None

    out: dict[str, int] = {"total": total, "zh": zh, "en": en}

    abbr = counts.get("abbr")
    if isinstance(abbr, int):
        out["abbr"] = int(abbr)

    return out


def _counts_from_registry_exports(exports_path: Path) -> dict[str, int] | None:
    """Extract optional substitution-related counts from artifacts/registry_exports.json.

    This is a best-effort enhancement for downstream acceptance gates.
    Missing or malformed files should not break manifest generation.
    """

    if not exports_path.exists():
        return None
    try:
        data = json.loads(exports_path.read_text("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None

    out: dict[str, int] = {}
    # Keep keys stable and explicit for consumers.
    sub_count = data.get("substitution_count")
    if isinstance(sub_count, int):
        out["terminology_substitutions_count"] = int(sub_count)

    vale_sub_count = data.get("vale_terminology_substitute_count")
    if isinstance(vale_sub_count, int):
        out["vale_terminology_substitute_count"] = int(vale_sub_count)

    return out or None


def _safe_relpath_under_root(root: Path, rel: str) -> Path:
    rel_path = Path(rel)
    if rel_path.is_absolute():
        raise SystemExit(
            f"manifest files must be relative to release root, got absolute: {rel!r}"
        )

    root_r = root.resolve()
    full = (root / rel_path).resolve()

    # Ensure full is under root (or equal).
    if full != root_r and root_r not in full.parents:
        raise SystemExit(f"manifest file escapes release root: {rel!r}")

    return full


@dataclass(frozen=True)
class Manifest:
    version: str
    commit: str
    generated_at: str
    counts: dict[str, int]
    sha256: dict[str, str]

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "version": self.version,
            "commit": self.commit,
            "generated_at": self.generated_at,
            "counts": self.counts,
            "sha256": self.sha256,
        }


def generate_manifest(
    *,
    root: Path,
    version: str,
    commit: str | None,
    generated_at: str | None,
    files: list[str],
    counts_from: str | None = None,
    repo_root: Path | None = None,
) -> Manifest:
    root = root.expanduser()
    if not root.exists():
        raise SystemExit(f"release root not found: {root}")
    if not root.is_dir():
        raise SystemExit(f"release root is not a directory: {root}")

    version = _validate_tag_version(version)

    if commit is None:
        rr = (repo_root or Path.cwd()).expanduser()
        commit = _git_head_commit(rr)
    commit = _validate_commit_sha(commit)

    if generated_at is None:
        generated_at_norm = _now_utc_iso8601()
    else:
        generated_at_norm = _validate_generated_at_utc(generated_at)

    if not files:
        raise SystemExit("no manifest files specified (use --files)")

    # counts
    counts: dict[str, int] | None = None
    if counts_from is not None:
        stats_path = _safe_relpath_under_root(root, counts_from)
        counts = _counts_from_build_stats(stats_path)
        if counts is None:
            raise SystemExit(
                f"counts-from did not contain usable counts (expected counts.total/zh/en ints): {stats_path}"
            )
    else:
        # auto-detect build stats if present
        stats_path = root / "domain_terms_build_stats.json"
        counts = _counts_from_build_stats(stats_path)

    # fallback: compute from domain_terms.txt
    if counts is None:
        # Prefer the canonical wordlist name under root; avoid accidentally counting
        # a different artifact if caller didn't include domain_terms.txt in --files.
        if (root / "domain_terms.txt").exists():
            terms_path = _safe_relpath_under_root(root, "domain_terms.txt")
        else:
            # fallback: try to locate a provided file that looks like domain_terms.txt
            candidates = [f for f in files if f.endswith("domain_terms.txt")]
            if not candidates:
                raise SystemExit(
                    "unable to compute counts: missing domain_terms.txt and no build stats available"
                )
            terms_path = _safe_relpath_under_root(root, candidates[0])
        terms = sorted(set(_load_domain_terms(terms_path)))
        zh = [t for t in terms if _is_zh_term(t)]
        zh_set = set(zh)
        en = [t for t in terms if t not in zh_set]
        counts = {"total": len(terms), "zh": len(zh), "en": len(en)}

    # Optional: carry substitution-related counts into the main manifest for easier downstream QA.
    reg_counts = _counts_from_registry_exports(
        root / "artifacts" / "registry_exports.json"
    )
    if reg_counts:
        # Do not overwrite the core keys; only add extra counters.
        for k, v in reg_counts.items():
            if k not in counts:
                counts[k] = v

    # sha256
    sha256: dict[str, str] = {}
    for rel in files:
        full = _safe_relpath_under_root(root, rel)
        if not full.exists():
            raise SystemExit(f"manifest file not found under release root: {rel}")
        sha256[rel] = _sha256_file(full)

    return Manifest(
        version=version,
        commit=commit,
        generated_at=generated_at_norm,
        counts=counts,
        sha256=sha256,
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Generate fusion-terms release manifest JSON"
    )
    p.add_argument("--root", required=True, help="Release root directory (staging dir)")
    p.add_argument("--version", required=True, help="Release tag (e.g. v2026.02.08)")
    p.add_argument(
        "--commit", default=None, help="Commit SHA (40-hex). If omitted, read from git."
    )
    p.add_argument(
        "--repo-root",
        default=None,
        help="Repo root for git lookup (only used when --commit is omitted). Default: cwd.",
    )
    p.add_argument(
        "--generated-at",
        default=None,
        help="UTC ISO8601 timestamp (e.g. 2026-02-08T03:21:00Z). If omitted, uses now().",
    )
    p.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Files (relative to --root) to hash into sha256 mapping.",
    )
    p.add_argument(
        "--counts-from",
        default=None,
        help=(
            "Optional build stats JSON path (relative to --root) to source counts from. "
            "If omitted, auto-detects domain_terms_build_stats.json under root."
        ),
    )
    p.add_argument(
        "--output",
        default="fusion_terms_manifest.json",
        help="Manifest filename (written under --root). Default: fusion_terms_manifest.json",
    )

    args = p.parse_args()

    root = Path(args.root)
    out_path = root.expanduser() / args.output

    manifest = generate_manifest(
        root=root,
        version=args.version,
        commit=args.commit,
        generated_at=args.generated_at,
        files=list(args.files),
        counts_from=args.counts_from,
        repo_root=Path(args.repo_root).expanduser() if args.repo_root else None,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(manifest.as_dict(), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
