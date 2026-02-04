from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import ensure_dir, load_simple_list, load_synonyms_tsv


WHITESPACE_RE = re.compile(r"\s")


def validate_no_control_or_invisible_terms(terms: set[str], *, context: str) -> None:
    """Fail fast if any term contains control/invisible Unicode characters.

    This protects against accidental copy/paste artifacts (e.g. ZERO WIDTH SPACE)
    that are nearly impossible to spot in reviews but can break downstream tools.
    """

    offenders: list[tuple[str, list[str]]] = []
    for t in terms:
        bad_desc: list[str] = []
        for ch in t:
            cat = unicodedata.category(ch)
            if cat.startswith("C"):
                name = unicodedata.name(ch, "<unknown>")
                bad_desc.append(f"U+{ord(ch):04X} {name} ({cat})")
        if bad_desc:
            offenders.append((t, bad_desc))

    if not offenders:
        return

    offenders.sort(key=lambda x: x[0])
    preview_lines: list[str] = []
    for term, bad in offenders[:20]:
        shown = ", ".join(bad[:3])
        more = "" if len(bad) <= 3 else f", ... +{len(bad) - 3} more"
        preview_lines.append(f"- {term!r}: {shown}{more}")
    preview = "\n".join(preview_lines)
    more_terms = "" if len(offenders) <= 20 else f"\n... and {len(offenders) - 20} more"

    raise SystemExit(
        "wordlist terms must not contain control/invisible Unicode characters "
        f"({context}).\n"
        "Tip: watch for zero-width spaces when copy/pasting from PDFs/Markdown.\n"
        f"offending terms:\n{preview}{more_terms}"
    )


def validate_no_whitespace_terms(terms: set[str], *, context: str) -> None:
    """Fail fast if any term contains whitespace.

    This repository's wordlist contract is one-term-per-line, and (by design)
    English multi-word phrases must be split into atomic tokens.
    """

    bad = sorted({t for t in terms if WHITESPACE_RE.search(t)})
    if not bad:
        return

    preview = "\n".join(f"- {t!r}" for t in bad[:20])
    more = "" if len(bad) <= 20 else f"\n... and {len(bad) - 20} more"
    raise SystemExit(
        "wordlist terms must not contain whitespace "
        f"({context}); split phrases into tokens instead.\n"
        f"offending terms:\n{preview}{more}"
    )


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def normalize_terms(
    terms: set[str],
    deny: set[str],
    synonyms: dict[str, str],
    keep_aliases: bool,
) -> set[str]:
    out: set[str] = set()
    for t in terms:
        if t in deny:
            continue
        preferred = synonyms.get(t, t)
        if preferred in deny:
            continue
        out.add(preferred)
        if keep_aliases and preferred != t and t not in deny:
            out.add(t)
    return out


def _is_zh_term(t: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in t)


def _load_wordlist_terms(path: Path) -> set[str]:
    if not path.exists():
        return set()
    out: set[str] = set()
    for line in path.read_text("utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s:
            out.add(s)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build final fusion term wordlist from curated lists."
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to config.toml",
    )
    parser.add_argument(
        "--terms-dir",
        default="terms",
        help="Directory containing allow/deny/synonyms",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output dir (overrides config)",
    )
    parser.add_argument(
        "--keep-aliases",
        action="store_true",
        help="Also keep alias forms from synonyms.tsv",
    )
    parser.add_argument(
        "--output",
        default="domain_terms.txt",
        help="Output filename under out-dir",
    )
    parser.add_argument(
        "--stats-json",
        default=None,
        help=(
            "Optional build stats JSON output path. "
            "Default: <out-dir>/<output_stem>_build_stats.json"
        ),
    )

    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()

    terms_dir = Path(args.terms_dir)
    allow_zh = load_simple_list(terms_dir / "allowlist_zh.txt")
    allow_en = load_simple_list(terms_dir / "allowlist_en.txt")
    deny = load_simple_list(terms_dir / "denylist.txt")
    synonyms = load_synonyms_tsv(terms_dir / "synonyms.tsv")

    merged = set()
    merged |= allow_zh
    merged |= allow_en

    final_terms = normalize_terms(
        merged,
        deny=deny,
        synonyms=synonyms,
        keep_aliases=args.keep_aliases,
    )

    # Stats: how many inputs were normalized by synonyms.
    synonyms_mapped = 0
    for t in merged:
        if t in deny:
            continue
        preferred = synonyms.get(t, t)
        if preferred != t and preferred not in deny:
            synonyms_mapped += 1

    validate_no_whitespace_terms(final_terms, context="after deny/synonyms normalization")
    validate_no_control_or_invisible_terms(
        final_terms, context="after deny/synonyms normalization"
    )

    ensure_dir(out_dir)
    out_path = out_dir / args.output

    prev_terms = _load_wordlist_terms(out_path)

    # Stable ordering: zh first (roughly), then en; within each: lexicographic
    zh = sorted([t for t in final_terms if _is_zh_term(t)])
    en = sorted([t for t in final_terms if t not in set(zh)])

    out_path.write_text("\n".join(zh + en) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(final_terms)} terms)")

    # Build stats report (deterministic JSON).
    output_stem = Path(args.output).stem
    stats_path = (
        Path(args.stats_json).expanduser()
        if args.stats_json
        else (out_dir / f"{output_stem}_build_stats.json")
    )

    added = sorted(final_terms - prev_terms)
    removed = sorted(prev_terms - final_terms)

    stats = {
        "schema_version": 1,
        "wordlist": str(out_path),
        "stats_path": str(stats_path),
        "counts": {
            "total": len(final_terms),
            "zh": len(zh),
            "en": len(en),
            "synonyms_mapped": int(synonyms_mapped),
            "added": len(added),
            "removed": len(removed),
        },
        # Keep full lists for auditability; consumers can ignore.
        "added": added,
        "removed": removed,
    }

    stats_path.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {stats_path}")


if __name__ == "__main__":
    main()
