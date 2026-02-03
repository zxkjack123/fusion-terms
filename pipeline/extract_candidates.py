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
    min_count_zh: int | None,
    min_count_en: int | None,
    topk_zh: int | None,
    topk_en: int | None,
    zh_stopwords: set[str] | None,
    en_stopwords: set[str] | None,
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

    zh_filtered_tsv = out_dir / "candidates_zh.filtered.tsv"
    en_filtered_tsv = out_dir / "candidates_en.filtered.tsv"

    def write_tsv(
        path: Path,
        counts: Counter[str],
        examples: dict[str, list[str]],
        files: dict[str, list[str]],
        *,
        min_count: int | None = None,
        topk: int | None = None,
        stopwords: set[str] | None = None,
    ) -> None:
        with path.open("w", encoding="utf-8") as f:
            f.write("term\tcount\texamples\tfiles\n")
            written = 0
            for term, cnt in counts.most_common():
                if stopwords is not None and term in stopwords:
                    continue
                if min_count is not None and cnt < min_count:
                    continue
                if topk is not None and written >= topk:
                    break
                ex = " | ".join(examples.get(term, []))
                fl = " | ".join(files.get(term, []))
                f.write(f"{term}\t{cnt}\t{ex}\t{fl}\n")
                written += 1

    write_tsv(zh_tsv, zh_counts, zh_examples, zh_files)
    write_tsv(en_tsv, en_counts, en_examples, en_files)

    # Filtered outputs (only written when any filter flag is provided)
    want_filtered = any(
        v is not None
        for v in [min_count_zh, min_count_en, topk_zh, topk_en, zh_stopwords, en_stopwords]
    )
    if want_filtered:
        write_tsv(
            zh_filtered_tsv,
            zh_counts,
            zh_examples,
            zh_files,
            min_count=min_count_zh,
            topk=topk_zh,
            stopwords=zh_stopwords,
        )
        write_tsv(
            en_filtered_tsv,
            en_counts,
            en_examples,
            en_files,
            min_count=min_count_en,
            topk=topk_en,
            stopwords=en_stopwords,
        )

    stats = {
        "source_root": str(source_root),
        "files_scanned": scanned,
        "zh_terms": len(zh_counts),
        "en_terms": len(en_counts),
        "outputs": {
            "zh": str(zh_tsv),
            "en": str(en_tsv),
            "zh_filtered": str(zh_filtered_tsv) if want_filtered else None,
            "en_filtered": str(en_filtered_tsv) if want_filtered else None,
        },
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

    # Stage 2.2: filtered candidates for review efficiency
    parser.add_argument(
        "--min-count-zh",
        type=int,
        default=None,
        help="Write candidates_zh.filtered.tsv with terms of count >= N",
    )
    parser.add_argument(
        "--min-count-en",
        type=int,
        default=None,
        help="Write candidates_en.filtered.tsv with terms of count >= N",
    )
    parser.add_argument(
        "--topk-zh",
        type=int,
        default=None,
        help="Write candidates_zh.filtered.tsv with top K terms by count",
    )
    parser.add_argument(
        "--topk-en",
        type=int,
        default=None,
        help="Write candidates_en.filtered.tsv with top K terms by count",
    )
    parser.add_argument(
        "--zh-stopwords",
        default=None,
        help="Path to zh stopwords (one token per line) for filtered output",
    )
    parser.add_argument(
        "--en-stopwords",
        default=None,
        help="Path to en stopwords (one token per line) for filtered output",
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

    def load_stopwords(path_str: str | None) -> set[str] | None:
        if not path_str:
            return None
        p = Path(path_str).expanduser()
        if not p.exists():
            raise SystemExit(f"stopwords file does not exist: {p}")
        out: set[str] = set()
        for line in p.read_text("utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.add(s)
        return out

    zh_stop = load_stopwords(args.zh_stopwords)
    en_stop = load_stopwords(args.en_stopwords)

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
        min_count_zh=args.min_count_zh,
        min_count_en=args.min_count_en,
        topk_zh=args.topk_zh,
        topk_en=args.topk_en,
        zh_stopwords=zh_stop,
        en_stopwords=en_stop,
    )


if __name__ == "__main__":
    main()
