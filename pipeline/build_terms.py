from __future__ import annotations

import argparse
from pathlib import Path

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import ensure_dir, load_simple_list, load_synonyms_tsv


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

    ensure_dir(out_dir)
    out_path = out_dir / args.output

    # Stable ordering: zh first (roughly), then en; within each: lexicographic
    zh = sorted(
        [t for t in final_terms if any("\u4e00" <= ch <= "\u9fff" for ch in t)]
    )
    en = sorted([t for t in final_terms if t not in set(zh)])

    out_path.write_text("\n".join(zh + en) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(final_terms)} terms)")


if __name__ == "__main__":
    main()
