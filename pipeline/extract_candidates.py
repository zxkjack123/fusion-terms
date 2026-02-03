from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import DefaultDict

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pipeline.common import (
    clean_markdown_lines,
    ensure_dir,
    iter_markdown_files,
    read_text_file,
)


ZH_RE_TEMPLATE = r"[\u4e00-\u9fff]{{{min_len},{max_len}}}"

# English/mixed patterns tuned for fusion engineering docs (high precision)
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,12}\b")
HYPHEN_TERM_RE = re.compile(r"\b[A-Za-z0-9]{1,12}(?:-[A-Za-z0-9]{1,12})+\b")
MATERIAL_FORMULA_RE = re.compile(r"\b[A-Z][a-z]?(?:\d+)(?:[A-Z][a-z]?\d+)*\b")
SLASH_MIX_RE = re.compile(r"\b[A-Za-z]{1,6}\/[A-Za-z]{1,6}\b")


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as f:
        return tomllib.load(f)


def extract(
    source_root: Path,
    out_dir: Path,
    min_zh_len: int,
    max_zh_len: int,
    max_examples: int,
    max_files_per_term: int,
    max_files: int | None,
) -> None:
    zh_re = re.compile(
        ZH_RE_TEMPLATE.format(min_len=min_zh_len, max_len=max_zh_len)
    )

    zh_counts: Counter[str] = Counter()
    en_counts: Counter[str] = Counter()

    zh_examples: DefaultDict[str, list[str]] = defaultdict(list)
    en_examples: DefaultDict[str, list[str]] = defaultdict(list)

    zh_files: DefaultDict[str, list[str]] = defaultdict(list)
    en_files: DefaultDict[str, list[str]] = defaultdict(list)

    scanned = 0
    for md_path in iter_markdown_files(source_root):
        if max_files is not None and scanned >= max_files:
            break
        scanned += 1

        text = read_text_file(md_path)
        for line in clean_markdown_lines(text):
            # Chinese spans
            for term in zh_re.findall(line):
                zh_counts[term] += 1
                if len(zh_examples[term]) < max_examples:
                    zh_examples[term].append(line)
                if len(zh_files[term]) < max_files_per_term:
                    zh_files[term].append(str(md_path))

            # English/mixed tokens
            tokens = set()
            tokens.update(ACRONYM_RE.findall(line))
            tokens.update(HYPHEN_TERM_RE.findall(line))
            tokens.update(MATERIAL_FORMULA_RE.findall(line))
            tokens.update(SLASH_MIX_RE.findall(line))

            for tok in tokens:
                en_counts[tok] += 1
                if len(en_examples[tok]) < max_examples:
                    en_examples[tok].append(line)
                if len(en_files[tok]) < max_files_per_term:
                    en_files[tok].append(str(md_path))

    ensure_dir(out_dir)

    zh_tsv = out_dir / "candidates_zh.tsv"
    en_tsv = out_dir / "candidates_en.tsv"

    def write_tsv(
        path: Path,
        counts: Counter[str],
        examples: dict[str, list[str]],
        files: dict[str, list[str]],
    ) -> None:
        with path.open("w", encoding="utf-8") as f:
            f.write("term\tcount\texamples\tfiles\n")
            for term, cnt in counts.most_common():
                ex = " | ".join(examples.get(term, []))
                fl = " | ".join(files.get(term, []))
                f.write(f"{term}\t{cnt}\t{ex}\t{fl}\n")

    write_tsv(zh_tsv, zh_counts, zh_examples, zh_files)
    write_tsv(en_tsv, en_counts, en_examples, en_files)

    stats = {
        "source_root": str(source_root),
        "files_scanned": scanned,
        "zh_terms": len(zh_counts),
        "en_terms": len(en_counts),
        "outputs": {"zh": str(zh_tsv), "en": str(en_tsv)},
    }
    (out_dir / "extract_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        "utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract candidate fusion terms from Markdown corpus."
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to config.toml",
    )
    parser.add_argument(
        "--source-root",
        default=None,
        help="Markdown corpus root (overrides config)",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output dir (overrides config)",
    )
    parser.add_argument("--min-zh-len", type=int, default=None)
    parser.add_argument("--max-zh-len", type=int, default=None)
    parser.add_argument("--max-examples", type=int, default=None)
    parser.add_argument("--max-files-per-term", type=int, default=None)
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Limit number of markdown files for quick runs",
    )

    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    source_root = Path(
        args.source_root or cfg.get("sources", {}).get("root", ".")
    ).expanduser()
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()

    min_zh_len = int(
        args.min_zh_len or cfg.get("extract", {}).get("min_zh_len", 2)
    )
    max_zh_len = int(
        args.max_zh_len or cfg.get("extract", {}).get("max_zh_len", 8)
    )
    max_examples = int(
        args.max_examples or cfg.get("extract", {}).get("max_examples", 3)
    )
    max_files_per_term = int(
        args.max_files_per_term
        or cfg.get("extract", {}).get("max_files_per_term", 20)
    )

    if not source_root.exists():
        raise SystemExit(f"source root does not exist: {source_root}")

    extract(
        source_root=source_root,
        out_dir=out_dir,
        min_zh_len=min_zh_len,
        max_zh_len=max_zh_len,
        max_examples=max_examples,
        max_files_per_term=max_files_per_term,
        max_files=args.max_files,
    )


if __name__ == "__main__":
    main()
