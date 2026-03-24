from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from pipeline.build_terms import (
    validate_no_control_or_invisible_terms,
    validate_no_whitespace_terms,
)


_SHA1_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_relpath_under_root(root: Path, rel: str) -> Path:
    rel_path = Path(rel)
    if rel_path.is_absolute():
        raise SystemExit(f"contract verify failed: sha256 path must be relative, got: {rel!r}")

    root_r = root.resolve()
    full = (root / rel_path).resolve()
    if full != root_r and root_r not in full.parents:
        raise SystemExit(f"contract verify failed: sha256 path escapes root: {rel!r}")

    return full


def _normalize_generated_at_utc(s: str) -> str:
    if s.endswith("Z"):
        try:
            datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError as e:
            raise SystemExit(
                f"contract verify failed: invalid generated_at (expected UTC ISO8601): {s!r}"
            ) from e
        return s

    if s.endswith("+00:00"):
        try:
            datetime.fromisoformat(s)
        except ValueError as e:
            raise SystemExit(
                f"contract verify failed: invalid generated_at (expected UTC ISO8601): {s!r}"
            ) from e
        return s.replace("+00:00", "Z")

    raise SystemExit(
        "contract verify failed: generated_at must be UTC ISO8601 (end with 'Z' or '+00:00'), "
        f"got: {s!r}"
    )


def _load_domain_terms_strict(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"contract verify failed: missing {path}")

    try:
        lines = path.read_text("utf-8").splitlines()
    except UnicodeDecodeError as e:
        raise SystemExit(
            f"contract verify failed: {path} is not valid UTF-8 ({e}). "
            "Tip: regenerate artifacts with pipeline.build_terms."
        ) from e

    terms: list[str] = []
    for lineno, raw in enumerate(lines, start=1):
        # Strict: no blank lines, no comments.
        if raw.strip() == "":
            raise SystemExit(f"contract verify failed: {path}:{lineno}: empty line is not allowed")
        if raw.lstrip().startswith("#"):
            raise SystemExit(f"contract verify failed: {path}:{lineno}: comments are not allowed")

        # Preserve original spacing for better error messages.
        if raw != raw.strip():
            raise SystemExit(
                f"contract verify failed: {path}:{lineno}: leading/trailing whitespace is not allowed"
            )

        terms.append(raw)

    # Duplicate check (keep first-seen order for stable error).
    seen: set[str] = set()
    for t in terms:
        if t in seen:
            raise SystemExit(f"contract verify failed: {path}: duplicate term: {t!r}")
        seen.add(t)

    # Token-only + invisible/control checks.
    validate_no_whitespace_terms(set(terms), context=f"in {path.name}")
    validate_no_control_or_invisible_terms(set(terms), context=f"in {path.name}")

    return terms


def verify_release_contract(
    *,
    root: Path,
    domain_terms: str = "domain_terms.txt",
    manifest: str = "fusion_terms_manifest.json",
) -> None:
    root = root.expanduser()
    if not root.exists():
        raise SystemExit(f"contract verify failed: root not found: {root}")
    if not root.is_dir():
        raise SystemExit(f"contract verify failed: root is not a directory: {root}")

    domain_terms_path = _safe_relpath_under_root(root, domain_terms)
    terms = _load_domain_terms_strict(domain_terms_path)

    manifest_path = _safe_relpath_under_root(root, manifest)
    if not manifest_path.exists():
        raise SystemExit(f"contract verify failed: missing {manifest_path}")

    try:
        data = json.loads(manifest_path.read_text("utf-8"))
    except UnicodeDecodeError as e:
        raise SystemExit(f"contract verify failed: {manifest_path} is not valid UTF-8 ({e})") from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"contract verify failed: invalid JSON manifest: {manifest_path} ({e})") from e

    if not isinstance(data, dict):
        raise SystemExit(f"contract verify failed: manifest must be a JSON object: {manifest_path}")

    required_top = ["version", "commit", "generated_at", "counts", "sha256"]
    missing = [k for k in required_top if k not in data]
    if missing:
        raise SystemExit(
            f"contract verify failed: manifest missing required fields {missing}: {manifest_path}"
        )

    if "schema_version" in data and data["schema_version"] != 1:
        raise SystemExit(
            f"contract verify failed: unsupported schema_version {data['schema_version']!r} (expected 1)"
        )

    version = data["version"]
    if not isinstance(version, str) or not version.strip():
        raise SystemExit("contract verify failed: manifest.version must be a non-empty string")

    commit = data["commit"]
    if not isinstance(commit, str) or not _SHA1_RE.match(commit):
        raise SystemExit("contract verify failed: manifest.commit must be a 40-hex SHA string")

    generated_at_norm = _normalize_generated_at_utc(str(data["generated_at"]))
    # If manifest used +00:00, we still accept it; encourage normalization.
    if generated_at_norm != data["generated_at"]:
        data["generated_at"] = generated_at_norm

    counts = data["counts"]
    if not isinstance(counts, dict):
        raise SystemExit("contract verify failed: manifest.counts must be an object")

    for k in ["total", "zh", "en"]:
        if k not in counts or not isinstance(counts[k], int):
            raise SystemExit(f"contract verify failed: manifest.counts.{k} must be an int")

    # Recompute counts from domain_terms.txt using the same zh heuristic as build pipeline.
    zh = [t for t in terms if any("\u4e00" <= ch <= "\u9fff" for ch in t)]
    zh_set = set(zh)
    en = [t for t in terms if t not in zh_set]

    expected_counts = {"total": len(terms), "zh": len(zh), "en": len(en)}
    for k, v in expected_counts.items():
        if counts.get(k) != v:
            raise SystemExit(
                "contract verify failed: manifest.counts mismatch; "
                f"expected {k}={v}, got {k}={counts.get(k)!r}"
            )

    sha256 = data["sha256"]
    if not isinstance(sha256, dict):
        raise SystemExit("contract verify failed: manifest.sha256 must be an object")
    if domain_terms not in sha256:
        raise SystemExit(
            f"contract verify failed: manifest.sha256 must include {domain_terms!r}"
        )

    # Verify all listed hashes.
    for rel, expected in sha256.items():
        if not isinstance(rel, str) or not rel:
            raise SystemExit("contract verify failed: manifest.sha256 keys must be non-empty strings")
        if not isinstance(expected, str) or not re.match(r"^[0-9a-f]{64}$", expected, re.IGNORECASE):
            raise SystemExit(
                f"contract verify failed: manifest.sha256[{rel!r}] must be a 64-hex sha256"
            )

        full = _safe_relpath_under_root(root, rel)
        if not full.exists():
            raise SystemExit(f"contract verify failed: sha256 file missing under root: {rel}")

        got = _sha256_file(full)
        if got.lower() != expected.lower():
            raise SystemExit(
                f"contract verify failed: sha256 mismatch for {rel}: expected {expected}, got {got}"
            )

    print(
        "contract OK: "
        f"{domain_terms} terms={len(terms)} version={version} commit={commit[:12]} generated_at={data['generated_at']}"
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Verify fusion-terms v1 release contract (domain_terms + manifest sha256)."
    )
    p.add_argument("--root", required=True, help="Release root directory (staging dir)")
    p.add_argument(
        "--domain-terms",
        default="domain_terms.txt",
        help="Wordlist filename (relative to --root). Default: domain_terms.txt",
    )
    p.add_argument(
        "--manifest",
        default="fusion_terms_manifest.json",
        help="Manifest filename (relative to --root). Default: fusion_terms_manifest.json",
    )

    args = p.parse_args()
    verify_release_contract(
        root=Path(args.root),
        domain_terms=args.domain_terms,
        manifest=args.manifest,
    )


if __name__ == "__main__":
    main()
