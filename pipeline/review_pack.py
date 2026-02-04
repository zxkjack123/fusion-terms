from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import ensure_dir


@dataclass(frozen=True)
class TsvRow:
    term: str
    count: int
    raw_line: str


def _load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def _resolve_under(base: Path, p: str) -> Path:
    pp = Path(p)
    return pp if pp.is_absolute() else (base / pp)


def _parse_candidates_tsv(path: Path) -> tuple[str, dict[str, TsvRow]]:
    """Parse a candidates TSV and return (header, rows_by_term).

    Expected columns: term, count, ...
    We preserve the original row line for stable re-emit.
    """

    if not path.exists():
        raise SystemExit(f"review pack failed: missing TSV: {path}")

    lines = path.read_text("utf-8", errors="ignore").splitlines()
    if not lines:
        raise SystemExit(f"review pack failed: empty TSV: {path}")

    header = lines[0].rstrip("\n")
    rows: dict[str, TsvRow] = {}

    for ln in lines[1:]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        term = parts[0].strip()
        if not term:
            continue
        try:
            cnt = int(parts[1].strip())
        except Exception:
            cnt = 0
        # Keep the last occurrence if duplicated (should not happen, but deterministic).
        rows[term] = TsvRow(term=term, count=cnt, raw_line=ln.rstrip("\n"))

    return header, rows


def _write_rows(path: Path, header: str, rows: list[TsvRow]) -> None:
    path.write_text(
        header + "\n" + "\n".join(r.raw_line for r in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )


def build_review_pack(
    *,
    out_dir: Path,
    candidates_zh: Path,
    candidates_en: Path,
    baseline_dir: Path,
    review_pack_dir: Path,
    update_baseline: bool,
) -> dict[str, object]:
    """Diff current candidates vs baseline and write a review pack.

    This is intended to reduce incremental review cost.
    """

    ensure_dir(review_pack_dir)
    ensure_dir(baseline_dir)

    base_zh_path = baseline_dir / candidates_zh.name
    base_en_path = baseline_dir / candidates_en.name

    cur_zh_header, cur_zh = _parse_candidates_tsv(candidates_zh)
    cur_en_header, cur_en = _parse_candidates_tsv(candidates_en)

    if base_zh_path.exists():
        base_zh_header, base_zh = _parse_candidates_tsv(base_zh_path)
    else:
        base_zh_header, base_zh = cur_zh_header, {}

    if base_en_path.exists():
        base_en_header, base_en = _parse_candidates_tsv(base_en_path)
    else:
        base_en_header, base_en = cur_en_header, {}

    # New and removed sets.
    new_zh_terms = set(cur_zh.keys()) - set(base_zh.keys())
    removed_zh_terms = set(base_zh.keys()) - set(cur_zh.keys())

    new_en_terms = set(cur_en.keys()) - set(base_en.keys())
    removed_en_terms = set(base_en.keys()) - set(cur_en.keys())

    # Stable ordering: most important first (count desc), then term asc.
    def _sort_key(r: TsvRow) -> tuple[int, str]:
        return (-int(r.count), r.term)

    new_zh_rows = sorted([cur_zh[t] for t in new_zh_terms], key=_sort_key)
    removed_zh_rows = sorted([base_zh[t] for t in removed_zh_terms], key=_sort_key)

    new_en_rows = sorted([cur_en[t] for t in new_en_terms], key=_sort_key)
    removed_en_rows = sorted([base_en[t] for t in removed_en_terms], key=_sort_key)

    new_zh_out = review_pack_dir / f"new_{candidates_zh.name}"
    removed_zh_out = review_pack_dir / f"removed_{candidates_zh.name}"

    new_en_out = review_pack_dir / f"new_{candidates_en.name}"
    removed_en_out = review_pack_dir / f"removed_{candidates_en.name}"

    _write_rows(new_zh_out, cur_zh_header, new_zh_rows)
    _write_rows(removed_zh_out, base_zh_header, removed_zh_rows)

    _write_rows(new_en_out, cur_en_header, new_en_rows)
    _write_rows(removed_en_out, base_en_header, removed_en_rows)

    summary = {
        "schema_version": 1,
        "out_dir": str(out_dir),
        "baseline_dir": str(baseline_dir),
        "review_pack_dir": str(review_pack_dir),
        "inputs": {
            "candidates_zh": str(candidates_zh),
            "candidates_en": str(candidates_en),
        },
        "outputs": {
            "new_zh": str(new_zh_out),
            "removed_zh": str(removed_zh_out),
            "new_en": str(new_en_out),
            "removed_en": str(removed_en_out),
        },
        "counts": {
            "new_zh": len(new_zh_rows),
            "removed_zh": len(removed_zh_rows),
            "new_en": len(new_en_rows),
            "removed_en": len(removed_en_rows),
        },
        "baseline_updated": bool(update_baseline),
    }

    (review_pack_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if update_baseline:
        shutil.copy2(candidates_zh, base_zh_path)
        shutil.copy2(candidates_en, base_en_path)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an incremental review pack by diffing candidates TSVs against a baseline snapshot."
        )
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to config.toml",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Artifacts output dir (overrides config)",
    )
    parser.add_argument(
        "--candidates-zh",
        default="candidates_zh.filtered.tsv",
        help="Candidates TSV filename/path for zh (default: candidates_zh.filtered.tsv)",
    )
    parser.add_argument(
        "--candidates-en",
        default="candidates_en.filtered.tsv",
        help="Candidates TSV filename/path for en (default: candidates_en.filtered.tsv)",
    )
    parser.add_argument(
        "--baseline-dir",
        default=None,
        help="Baseline snapshot dir (default: <out-dir>/.review_baseline)",
    )
    parser.add_argument(
        "--review-pack-dir",
        default=None,
        help="Review pack output dir (default: <out-dir>/review_pack)",
    )
    parser.add_argument(
        "--no-update-baseline",
        action="store_true",
        help="Do not update baseline snapshot after producing the review pack",
    )

    args = parser.parse_args()

    cfg = _load_config(Path(args.config))
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()
    ensure_dir(out_dir)

    candidates_zh = _resolve_under(out_dir, args.candidates_zh)
    candidates_en = _resolve_under(out_dir, args.candidates_en)

    baseline_dir = (
        Path(args.baseline_dir).expanduser()
        if args.baseline_dir
        else (out_dir / ".review_baseline")
    )
    review_pack_dir = (
        Path(args.review_pack_dir).expanduser()
        if args.review_pack_dir
        else (out_dir / "review_pack")
    )

    summary = build_review_pack(
        out_dir=out_dir,
        candidates_zh=candidates_zh,
        candidates_en=candidates_en,
        baseline_dir=baseline_dir,
        review_pack_dir=review_pack_dir,
        update_baseline=(not args.no_update_baseline),
    )

    print(
        "review pack written: "
        f"new_zh={summary['counts']['new_zh']} removed_zh={summary['counts']['removed_zh']} "
        f"new_en={summary['counts']['new_en']} removed_en={summary['counts']['removed_en']}"
    )


if __name__ == "__main__":
    main()
