from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass
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

# Lowercase English word tokens (used to capture phrase components like
# neutral/beam/injection).
# We keep this conservative to avoid swamping candidates with generic prose.
EN_WORD_RE = re.compile(r"\b[a-z]{3,24}\b")

# LaTeX / math noise tokens that are rarely meaningful as terminology
# candidates.
# These can leak from PDF->MD conversion (sometimes losing the leading
# backslash).
LATEX_NOISE_EN_WORDS: set[str] = {
    "mathrm",
    "mathbf",
    "boldsymbol",
    "mathcal",
    "mathit",
    "mathsf",
    "textrm",
    "text",
    "left",
    "right",
    # Common Greek macro names observed as candidate noise
    "omega",
    "theta",
    "phi",
}

# Minimal built-in stopwords for the EN_WORD_RE path only.
# This is intentionally small; a full stopword list should live in
# terms/stopwords_en.txt
# and be applied via --en-stopwords for filtered outputs.
COMMON_EN_STOPWORDS: set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "may",
    "more",
    "most",
    "not",
    "of",
    "on",
    "one",
    "or",
    "our",
    "out",
    "she",
    "should",
    "such",
    "than",
    "that",
    "the",
    "their",
    "there",
    "these",
    "they",
    "this",
    "those",
    "to",
    "too",
    "was",
    "we",
    "were",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
}

# Phrase extraction: conservative RAKE-like segmentation.
PHRASE_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]{1,}\b")


def _extract_en_phrases_rake(line: str, *, stopwords: set[str]) -> set[str]:
    """Extract English phrases from a cleaned line.

    - Remove acronyms (so e.g. "(NBI)" doesn't pollute phrases).
    - Tokenize words with hyphen support.
    - Split on stopwords.
    - Keep 2-6 word phrases.

    The caller-provided stopwords are applied in addition to this module's
    built-in conservative stopword/noise filters.

    NOTE: This is for *candidate discovery only* and is intentionally
    conservative.
    """

    # Drop acronyms so they don't get folded into phrases.
    s = ACRONYM_RE.sub(" ", line)

    # Tokenize words with hyphen support, but ignore LaTeX macro names.
    # Example: "\\omega" should not yield the token "omega".
    words: list[str] = []
    for m in PHRASE_WORD_RE.finditer(s):
        # Ignore LaTeX macro names, robust to stray characters between the
        # backslash and the word.
        if "\\" in s[max(0, m.start() - 2) : m.start()]:
            continue
        w = m.group(0).lower()
        if w in LATEX_NOISE_EN_WORDS:
            continue
        words.append(w)

    phrases: set[str] = set()
    buf: list[str] = []
    for w in words:
        if w in stopwords:
            if 2 <= len(buf) <= 6:
                phrases.add(" ".join(buf))
            buf = []
            continue
        buf.append(w)
        if len(buf) > 6:
            # If it gets too long, keep the tail window to avoid
            # unbounded phrases.
            buf = buf[-6:]

    if 2 <= len(buf) <= 6:
        phrases.add(" ".join(buf))

    return phrases


CACHE_SCHEMA_VERSION = 1


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _sha1_str(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def _compute_file_sha256(md_path: Path) -> str:
    hasher = hashlib.sha256()
    with md_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _extractor_signature(
    *,
    min_zh_len: int,
    max_zh_len: int,
    en_phrases: str,
) -> str:
    # Any extraction-rule change should change this signature.
    # NOTE: Keep this compatible with Python 3.11 syntax. In particular,
    # avoid backslashes inside f-string expressions.
    stopwords_blob = "\n".join(sorted(COMMON_EN_STOPWORDS))
    stopwords_sha1 = _sha1_str(stopwords_blob)
    latex_noise_blob = "\n".join(sorted(LATEX_NOISE_EN_WORDS))
    latex_noise_sha1 = _sha1_str(latex_noise_blob)
    payload = "\n".join(
        [
            f"schema={CACHE_SCHEMA_VERSION}",
            # Extraction rule version markers (bump when behavior changes).
            "rule_latex_macro_gate=1",
            "rule_clean_md_latex_style=1",
            f"min_zh_len={min_zh_len}",
            f"max_zh_len={max_zh_len}",
            f"ACRONYM_RE={ACRONYM_RE.pattern}",
            f"HYPHEN_TERM_RE={HYPHEN_TERM_RE.pattern}",
            f"MATERIAL_FORMULA_RE={MATERIAL_FORMULA_RE.pattern}",
            f"SLASH_MIX_RE={SLASH_MIX_RE.pattern}",
            f"EN_WORD_RE={EN_WORD_RE.pattern}",
            f"COMMON_EN_STOPWORDS_SHA1={stopwords_sha1}",
            f"LATEX_NOISE_EN_WORDS_SHA1={latex_noise_sha1}",
            f"en_phrases={en_phrases}",
            f"PHRASE_WORD_RE={PHRASE_WORD_RE.pattern}",
        ]
    )
    return _sha1_str(payload)


@dataclass
class _CacheIndexEntry:
    mtime_ns: int
    size: int
    sha256: str
    result_relpath: str


def _load_cache_index(cache_dir: Path) -> dict:
    idx_path = cache_dir / "index.json"
    if not idx_path.exists():
        return {}
    try:
        return json.loads(idx_path.read_text("utf-8"))
    except Exception as e:
        # Corrupt cache; treat as missing.
        warnings.warn(
            f"cache index corrupted, rebuilding: {e}",
            stacklevel=2,
        )
        return {}


def _save_cache_index(cache_dir: Path, index: dict) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    index_path = cache_dir / "index.json"
    tmp_path = cache_dir / f"index.json.tmp.{os.getpid()}.{id(index)}"
    try:
        tmp_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2),
            "utf-8",
        )
        os.replace(tmp_path, index_path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def _cache_entry_from_dict(d: dict) -> _CacheIndexEntry | None:
    try:
        return _CacheIndexEntry(
            mtime_ns=int(d["mtime_ns"]),
            size=int(d["size"]),
            sha256=str(d.get("sha256", "")),
            result_relpath=str(d["result_relpath"]),
        )
    except Exception as e:
        warnings.warn(
            f"cache entry malformed: {e}",
            stacklevel=2,
        )
        return None


def _load_cached_results(
    *,
    incremental: bool,
    cache_enabled: bool,
    cache_dir: Path | None,
    cache_files: dict[str, dict],
    md_path: Path,
    md_key: str,
    st_mtime_ns: int,
    st_size: int,
) -> tuple[dict | None, _CacheIndexEntry | None, Path | None]:
    cached_entry = (
        _cache_entry_from_dict(cache_files[md_key])
        if md_key in cache_files
        else None
        if cache_enabled
        else None
    )

    can_use_cache = False
    cached_result_path: Path | None = None
    if cache_enabled and cached_entry is not None and cache_dir is not None:
        if cached_entry.mtime_ns == st_mtime_ns and cached_entry.size == st_size:
            sha_matches = True
            if cached_entry.sha256:
                try:
                    sha_matches = cached_entry.sha256 == _compute_file_sha256(md_path)
                except (FileNotFoundError, OSError) as exc:
                    warnings.warn(
                        f"cache sha256 check failed for {md_key}: {exc}",
                        stacklevel=2,
                    )
                    sha_matches = False

            if sha_matches:
                cached_result_path = cache_dir / cached_entry.result_relpath
                if cached_result_path.exists():
                    can_use_cache = True

    if not (incremental and can_use_cache and cached_result_path is not None):
        return None, cached_entry, cached_result_path

    try:
        data = json.loads(cached_result_path.read_text("utf-8"))
    except Exception as e:
        warnings.warn(
            f"cache entry unreadable for {md_key}: {e}",
            stacklevel=2,
        )
        return None, cached_entry, cached_result_path

    return data, cached_entry, cached_result_path


def _save_file_cache(
    *,
    cache_enabled: bool,
    cache_dir: Path | None,
    cache_files: dict[str, dict],
    md_key: str,
    st_mtime_ns: int,
    st_size: int,
    extractor_sig: str,
    text: str,
    file_zh_counts: Counter[str],
    file_en_counts: Counter[str],
    file_zh_examples: dict[str, list[str]],
    file_en_examples: dict[str, list[str]],
    file_en_phrase_counts: Counter[str],
    file_en_phrase_examples: dict[str, list[str]],
    want_en_phrases: bool,
) -> None:
    if not (cache_enabled and cache_dir is not None):
        return

    relpath = f"files/{_sha1_str(md_key)}.json"
    result_path = cache_dir / relpath
    result_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "version": CACHE_SCHEMA_VERSION,
        "extractor_sig": extractor_sig,
        "path": md_key,
        "mtime_ns": int(st_mtime_ns),
        "size": int(st_size),
        "sha256": _sha256_text(text),
        "zh_counts": dict(file_zh_counts),
        "en_counts": dict(file_en_counts),
        "zh_examples": file_zh_examples,
        "en_examples": file_en_examples,
        "en_phrase_counts": (dict(file_en_phrase_counts) if want_en_phrases else {}),
        "en_phrase_examples": (file_en_phrase_examples if want_en_phrases else {}),
    }
    _tmp = result_path.with_suffix(f".tmp.{os.getpid()}")
    try:
        _tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            "utf-8",
        )
        os.replace(_tmp, result_path)
    finally:
        if _tmp.exists():
            try:
                _tmp.unlink()
            except OSError:
                pass
    cache_files[md_key] = {
        "mtime_ns": int(st_mtime_ns),
        "size": int(st_size),
        "sha256": payload["sha256"],
        "result_relpath": relpath,
    }


def _merge_cached_file_data(
    *,
    md_path: Path,
    cached_data: dict,
    zh_counts: Counter[str],
    en_counts: Counter[str],
    zh_examples: DefaultDict[str, list[str]],
    en_examples: DefaultDict[str, list[str]],
    zh_files: DefaultDict[str, list[str]],
    en_files: DefaultDict[str, list[str]],
    en_phrase_counts: Counter[str],
    en_phrase_examples: DefaultDict[str, list[str]],
    en_phrase_files: DefaultDict[str, list[str]],
    max_examples: int,
    max_files_per_term: int,
    want_en_phrases: bool,
) -> None:
    file_zh_counts = {k: int(v) for k, v in cached_data.get("zh_counts", {}).items()}
    file_en_counts = {k: int(v) for k, v in cached_data.get("en_counts", {}).items()}
    file_zh_examples = {
        k: list(v) for k, v in cached_data.get("zh_examples", {}).items()
    }
    file_en_examples = {
        k: list(v) for k, v in cached_data.get("en_examples", {}).items()
    }

    zh_counts.update(file_zh_counts)
    en_counts.update(file_en_counts)

    md_str = str(md_path)
    for term in file_zh_counts.keys():
        if len(zh_files[term]) < max_files_per_term:
            zh_files[term].append(md_str)
    for tok in file_en_counts.keys():
        if len(en_files[tok]) < max_files_per_term:
            en_files[tok].append(md_str)

    for term, ex_list in file_zh_examples.items():
        if len(zh_examples[term]) >= max_examples:
            continue
        for ex in ex_list:
            if len(zh_examples[term]) >= max_examples:
                break
            zh_examples[term].append(ex)
    for tok, ex_list in file_en_examples.items():
        if len(en_examples[tok]) >= max_examples:
            continue
        for ex in ex_list:
            if len(en_examples[tok]) >= max_examples:
                break
            en_examples[tok].append(ex)

    if not want_en_phrases:
        return

    cached_phr_counts = {
        k: int(v) for k, v in cached_data.get("en_phrase_counts", {}).items()
    }
    en_phrase_counts.update(cached_phr_counts)

    for phr in cached_phr_counts.keys():
        if len(en_phrase_files[phr]) < max_files_per_term:
            en_phrase_files[phr].append(md_str)

    cached_phr_examples = {
        k: list(v) for k, v in cached_data.get("en_phrase_examples", {}).items()
    }
    for phr, ex_list in cached_phr_examples.items():
        if len(en_phrase_examples[phr]) >= max_examples:
            continue
        for ex in ex_list:
            if len(en_phrase_examples[phr]) >= max_examples:
                break
            en_phrase_examples[phr].append(ex)


@dataclass
class _FileExtractResult:
    text: str
    zh_counts: Counter[str]
    en_counts: Counter[str]
    en_phrase_counts: Counter[str]
    zh_examples: dict[str, list[str]]
    en_examples: dict[str, list[str]]
    en_phrase_examples: dict[str, list[str]]


def _load_old_cache_counts(
    *,
    incremental: bool,
    cache_enabled: bool,
    cache_dir: Path | None,
    cached_entry: _CacheIndexEntry | None,
    md_key: str,
) -> tuple[dict[str, int], dict[str, int]]:
    if not (
        incremental
        and cache_enabled
        and cache_dir is not None
        and cached_entry is not None
    ):
        return {}, {}

    old_path = cache_dir / cached_entry.result_relpath
    if not old_path.exists():
        return {}, {}

    try:
        old_data = json.loads(old_path.read_text("utf-8"))
        old_zh_counts = {k: int(v) for k, v in old_data.get("zh_counts", {}).items()}
        old_en_counts = {k: int(v) for k, v in old_data.get("en_counts", {}).items()}
        return old_zh_counts, old_en_counts
    except Exception as e:
        warnings.warn(
            f"old cache data unreadable for {md_key}: {e}",
            stacklevel=2,
        )
        return {}, {}


def _process_single_file(
    *,
    md_path: Path,
    zh_re: re.Pattern[str],
    want_en_phrases: bool,
    en_phrases: str,
) -> _FileExtractResult:
    file_zh_counts: Counter[str] = Counter()
    file_en_counts: Counter[str] = Counter()
    file_en_phrase_counts: Counter[str] = Counter()
    file_zh_examples: dict[str, list[str]] = {}
    file_en_examples: dict[str, list[str]] = {}
    file_en_phrase_examples: dict[str, list[str]] = {}

    text = read_text_file(md_path)
    for line in clean_markdown_lines(text):
        # Chinese spans
        for term in zh_re.findall(line):
            file_zh_counts[term] += 1
            if term not in file_zh_examples:
                # Keep at most 1 example per term per file (cache bounded).
                file_zh_examples[term] = [line]

        # English/mixed tokens
        tokens = set()
        tokens.update(ACRONYM_RE.findall(line))
        tokens.update(HYPHEN_TERM_RE.findall(line))
        tokens.update(MATERIAL_FORMULA_RE.findall(line))
        tokens.update(SLASH_MIX_RE.findall(line))

        # Phrase component words: only harvest plain lowercase words from
        # lines that already contain some technical token.
        if tokens:
            low = line.lower()
            for m in EN_WORD_RE.finditer(low):
                w = m.group(0)
                # LaTeX macro name like "\\omega". Be robust to
                # stray/invisible
                # characters between the backslash and the macro name by
                # checking a small lookback window.
                if "\\" in low[max(0, m.start() - 2) : m.start()]:
                    continue
                if w in LATEX_NOISE_EN_WORDS:
                    continue
                if w in COMMON_EN_STOPWORDS:
                    continue
                tokens.add(w)

        for tok in tokens:
            file_en_counts[tok] += 1
            if tok not in file_en_examples:
                file_en_examples[tok] = [line]

        if want_en_phrases and en_phrases == "rake":
            phrase_stop = COMMON_EN_STOPWORDS
            phrases = _extract_en_phrases_rake(line, stopwords=phrase_stop)
            for phr in phrases:
                file_en_phrase_counts[phr] += 1
                if phr not in file_en_phrase_examples:
                    file_en_phrase_examples[phr] = [line]

    return _FileExtractResult(
        text=text,
        zh_counts=file_zh_counts,
        en_counts=file_en_counts,
        en_phrase_counts=file_en_phrase_counts,
        zh_examples=file_zh_examples,
        en_examples=file_en_examples,
        en_phrase_examples=file_en_phrase_examples,
    )


def _update_incremental_deltas(
    *,
    new_zh_counts: dict[str, int],
    new_en_counts: dict[str, int],
    old_zh_counts: dict[str, int],
    old_en_counts: dict[str, int],
    zh_added_delta: Counter[str],
    zh_removed_delta: Counter[str],
    en_added_delta: Counter[str],
    en_removed_delta: Counter[str],
) -> None:
    for term, new_cnt in new_zh_counts.items():
        old_cnt = old_zh_counts.get(term, 0)
        if new_cnt > old_cnt:
            zh_added_delta[term] += new_cnt - old_cnt
    for term, old_cnt in old_zh_counts.items():
        new_cnt = new_zh_counts.get(term, 0)
        if old_cnt > new_cnt:
            zh_removed_delta[term] += old_cnt - new_cnt

    for tok, new_cnt in new_en_counts.items():
        old_cnt = old_en_counts.get(tok, 0)
        if new_cnt > old_cnt:
            en_added_delta[tok] += new_cnt - old_cnt
    for tok, old_cnt in old_en_counts.items():
        new_cnt = new_en_counts.get(tok, 0)
        if old_cnt > new_cnt:
            en_removed_delta[tok] += old_cnt - new_cnt


def _merge_file_contrib(
    *,
    md_path: Path,
    file_zh_counts: dict[str, int],
    file_en_counts: dict[str, int],
    file_zh_examples: dict[str, list[str]],
    file_en_examples: dict[str, list[str]],
    zh_counts: Counter[str],
    en_counts: Counter[str],
    zh_examples: DefaultDict[str, list[str]],
    en_examples: DefaultDict[str, list[str]],
    zh_files: DefaultDict[str, list[str]],
    en_files: DefaultDict[str, list[str]],
    max_examples: int,
    max_files_per_term: int,
) -> None:
    zh_counts.update(file_zh_counts)
    en_counts.update(file_en_counts)

    md_str = str(md_path)
    for term in file_zh_counts.keys():
        if len(zh_files[term]) < max_files_per_term:
            zh_files[term].append(md_str)
    for tok in file_en_counts.keys():
        if len(en_files[tok]) < max_files_per_term:
            en_files[tok].append(md_str)

    for term, ex_list in file_zh_examples.items():
        if len(zh_examples[term]) >= max_examples:
            continue
        for ex in ex_list:
            if len(zh_examples[term]) >= max_examples:
                break
            zh_examples[term].append(ex)
    for tok, ex_list in file_en_examples.items():
        if len(en_examples[tok]) >= max_examples:
            continue
        for ex in ex_list:
            if len(en_examples[tok]) >= max_examples:
                break
            en_examples[tok].append(ex)


def _merge_phrase_contrib(
    *,
    md_path: Path,
    file_en_phrase_counts: dict[str, int],
    file_en_phrase_examples: dict[str, list[str]],
    en_phrase_counts: Counter[str],
    en_phrase_examples: DefaultDict[str, list[str]],
    en_phrase_files: DefaultDict[str, list[str]],
    max_examples: int,
    max_files_per_term: int,
) -> None:
    en_phrase_counts.update(file_en_phrase_counts)

    md_str = str(md_path)
    for phr in file_en_phrase_counts.keys():
        if len(en_phrase_files[phr]) < max_files_per_term:
            en_phrase_files[phr].append(md_str)

    for phr, ex_list in file_en_phrase_examples.items():
        if len(en_phrase_examples[phr]) >= max_examples:
            continue
        for ex in ex_list:
            if len(en_phrase_examples[phr]) >= max_examples:
                break
            en_phrase_examples[phr].append(ex)


def _write_tsv(
    *,
    path: Path,
    counts: Counter[str],
    examples: dict[str, list[str]],
    files: dict[str, list[str]],
    min_count: int | None = None,
    topk: int | None = None,
    stopwords: set[str] | None = None,
) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("term\tcount\texamples\tfiles\n")
        written = 0
        # Stable ordering: count desc, then term asc.
        for term, cnt in sorted(
            counts.items(),
            key=lambda kv: (-kv[1], kv[0]),
        ):
            if stopwords is not None and term in stopwords:
                continue
            if min_count is not None and cnt < min_count:
                continue
            if topk is not None and written >= topk:
                break
            ex = " | ".join(examples.get(term, []))
            fl = " | ".join(files.get(term, []))
            ex = ex.replace("\t", " ").replace("\n", " ").replace("\r", " ")
            fl = fl.replace("\t", " ").replace("\n", " ").replace("\r", " ")
            f.write(f"{term}\t{cnt}\t{ex}\t{fl}\n")
            written += 1


def _write_extract_outputs(
    *,
    out_dir: Path,
    source_root: Path,
    scanned: int,
    zh_counts: Counter[str],
    en_counts: Counter[str],
    en_phrase_counts: Counter[str],
    zh_examples: dict[str, list[str]],
    en_examples: dict[str, list[str]],
    en_phrase_examples: dict[str, list[str]],
    zh_files: dict[str, list[str]],
    en_files: dict[str, list[str]],
    en_phrase_files: dict[str, list[str]],
    min_count_zh: int | None,
    min_count_en: int | None,
    topk_zh: int | None,
    topk_en: int | None,
    zh_stopwords: set[str] | None,
    en_stopwords: set[str] | None,
    want_en_phrases: bool,
    incremental: bool,
    cache_enabled: bool,
    cache_dir: Path | None,
    extractor_sig: str,
    cache_hits: int,
    cache_misses: int,
    processed_files: int,
    skipped_files: int,
    cache_invalidated: bool,
    zh_added_delta: Counter[str],
    zh_removed_delta: Counter[str],
    en_added_delta: Counter[str],
    en_removed_delta: Counter[str],
    processed_paths_sample: list[str],
) -> dict[str, object]:
    ensure_dir(out_dir)

    zh_tsv = out_dir / "candidates_zh.tsv"
    en_tsv = out_dir / "candidates_en.tsv"
    en_phr_tsv = out_dir / "candidates_en_phrases.tsv"

    zh_filtered_tsv = out_dir / "candidates_zh.filtered.tsv"
    en_filtered_tsv = out_dir / "candidates_en.filtered.tsv"

    _write_tsv(
        path=zh_tsv,
        counts=zh_counts,
        examples=zh_examples,
        files=zh_files,
    )
    _write_tsv(
        path=en_tsv,
        counts=en_counts,
        examples=en_examples,
        files=en_files,
    )

    want_filtered = any(
        v is not None
        for v in [
            min_count_zh,
            min_count_en,
            topk_zh,
            topk_en,
            zh_stopwords,
            en_stopwords,
        ]
    )
    if want_filtered:
        _write_tsv(
            path=zh_filtered_tsv,
            counts=zh_counts,
            examples=zh_examples,
            files=zh_files,
            min_count=min_count_zh,
            topk=topk_zh,
            stopwords=zh_stopwords,
        )
        _write_tsv(
            path=en_filtered_tsv,
            counts=en_counts,
            examples=en_examples,
            files=en_files,
            min_count=min_count_en,
            topk=topk_en,
            stopwords=en_stopwords,
        )

    outputs: dict[str, str | None] = {
        "zh": str(zh_tsv),
        "en": str(en_tsv),
        "zh_filtered": str(zh_filtered_tsv) if want_filtered else None,
        "en_filtered": str(en_filtered_tsv) if want_filtered else None,
        "en_phrases": str(en_phr_tsv) if want_en_phrases else None,
    }

    stats: dict[str, object] = {
        "source_root": str(source_root),
        "files_scanned": scanned,
        "zh_terms": len(zh_counts),
        "en_terms": len(en_counts),
        "en_phrase_terms": len(en_phrase_counts) if want_en_phrases else 0,
        "cache": {
            "enabled": cache_enabled,
            "incremental": incremental,
            "dir": str(cache_dir) if cache_dir is not None else None,
            "extractor_sig": extractor_sig,
            "hits": cache_hits,
            "misses": cache_misses,
            "processed_files": processed_files,
            "skipped_files": skipped_files,
            "invalidated": cache_invalidated,
        },
        "outputs": outputs,
    }

    if incremental:

        def _top_delta(counter: Counter[str], n: int = 200):
            return [{"term": t, "delta": int(d)} for t, d in counter.most_common(n)]

        delta = {
            "source_root": str(source_root),
            "files": {
                "scanned": scanned,
                "processed": processed_files,
                "skipped": skipped_files,
                "processed_sample": processed_paths_sample,
            },
            "cache": {
                "dir": str(cache_dir) if cache_dir is not None else None,
                "extractor_sig": extractor_sig,
                "hits": cache_hits,
                "misses": cache_misses,
                "invalidated": cache_invalidated,
            },
            "terms": {
                "zh": {
                    "added": _top_delta(zh_added_delta),
                    "removed": _top_delta(zh_removed_delta),
                    "added_total": int(sum(zh_added_delta.values())),
                    "removed_total": int(sum(zh_removed_delta.values())),
                },
                "en": {
                    "added": _top_delta(en_added_delta),
                    "removed": _top_delta(en_removed_delta),
                    "added_total": int(sum(en_added_delta.values())),
                    "removed_total": int(sum(en_removed_delta.values())),
                },
            },
        }
        (out_dir / "extract_delta.json").write_text(
            json.dumps(delta, ensure_ascii=False, indent=2),
            "utf-8",
        )
        outputs["delta"] = str(out_dir / "extract_delta.json")

    (out_dir / "extract_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        "utf-8",
    )

    if want_en_phrases:
        _write_tsv(
            path=en_phr_tsv,
            counts=en_phrase_counts,
            examples=en_phrase_examples,
            files=en_phrase_files,
        )

    return stats


def _prepare_cache_state(
    *,
    cache_enabled: bool,
    cache_dir: Path | None,
    extractor_sig: str,
) -> tuple[dict, dict[str, dict], bool]:
    cache_invalidated = False
    cache_index: dict = {}
    cache_files: dict[str, dict] = {}

    if cache_enabled and cache_dir is not None:
        cache_index = _load_cache_index(cache_dir)
        if (
            cache_index.get("version") != CACHE_SCHEMA_VERSION
            or cache_index.get("extractor_sig") != extractor_sig
        ):
            cache_index = {
                "version": CACHE_SCHEMA_VERSION,
                "extractor_sig": extractor_sig,
                "files": {},
            }
            cache_invalidated = True
        cache_files = cache_index.setdefault("files", {})

    return cache_index, cache_files, cache_invalidated


def _scan_markdown_corpus(
    *,
    source_root: Path,
    exclude_globs: list[str] | None,
    max_files: int | None,
    incremental: bool,
    cache_enabled: bool,
    cache_dir: Path | None,
    cache_files: dict[str, dict],
    zh_re: re.Pattern[str],
    en_phrases: str,
    want_en_phrases: bool,
    max_examples: int,
    max_files_per_term: int,
    extractor_sig: str,
    zh_counts: Counter[str],
    en_counts: Counter[str],
    en_phrase_counts: Counter[str],
    zh_examples: DefaultDict[str, list[str]],
    en_examples: DefaultDict[str, list[str]],
    en_phrase_examples: DefaultDict[str, list[str]],
    zh_files: DefaultDict[str, list[str]],
    en_files: DefaultDict[str, list[str]],
    en_phrase_files: DefaultDict[str, list[str]],
    zh_added_delta: Counter[str],
    zh_removed_delta: Counter[str],
    en_added_delta: Counter[str],
    en_removed_delta: Counter[str],
) -> tuple[int, int, int, int, int, list[str]]:
    cache_hits = 0
    cache_misses = 0
    processed_files = 0
    skipped_files = 0
    processed_paths_sample: list[str] = []
    scanned = 0

    for md_path in iter_markdown_files(
        source_root,
        exclude_globs=exclude_globs or None,
    ):
        if max_files is not None and scanned >= max_files:
            break
        scanned += 1

        try:
            st = md_path.stat()
        except (FileNotFoundError, OSError) as exc:
            warnings.warn(f"skipping {md_path}: {exc}", stacklevel=2)
            continue
        md_key = str(md_path)
        cached_data, cached_entry, _ = _load_cached_results(
            incremental=incremental,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            cache_files=cache_files,
            md_path=md_path,
            md_key=md_key,
            st_mtime_ns=int(st.st_mtime_ns),
            st_size=int(st.st_size),
        )

        if incremental and cached_data is not None:
            cache_hits += 1
            skipped_files += 1
            _merge_cached_file_data(
                md_path=md_path,
                cached_data=cached_data,
                zh_counts=zh_counts,
                en_counts=en_counts,
                zh_examples=zh_examples,
                en_examples=en_examples,
                zh_files=zh_files,
                en_files=en_files,
                en_phrase_counts=en_phrase_counts,
                en_phrase_examples=en_phrase_examples,
                en_phrase_files=en_phrase_files,
                max_examples=max_examples,
                max_files_per_term=max_files_per_term,
                want_en_phrases=want_en_phrases,
            )
            continue

        if cache_enabled:
            cache_misses += 1
        processed_files += 1
        if len(processed_paths_sample) < 50:
            processed_paths_sample.append(md_key)

        old_zh_counts, old_en_counts = _load_old_cache_counts(
            incremental=incremental,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            cached_entry=cached_entry,
            md_key=md_key,
        )

        try:
            file_result = _process_single_file(
                md_path=md_path,
                zh_re=zh_re,
                want_en_phrases=want_en_phrases,
                en_phrases=en_phrases,
            )
        except (FileNotFoundError, OSError) as exc:
            warnings.warn(f"skipping {md_path}: {exc}", stacklevel=2)
            continue

        if incremental:
            _update_incremental_deltas(
                new_zh_counts=dict(file_result.zh_counts),
                new_en_counts=dict(file_result.en_counts),
                old_zh_counts=old_zh_counts,
                old_en_counts=old_en_counts,
                zh_added_delta=zh_added_delta,
                zh_removed_delta=zh_removed_delta,
                en_added_delta=en_added_delta,
                en_removed_delta=en_removed_delta,
            )

        _merge_file_contrib(
            md_path=md_path,
            file_zh_counts=dict(file_result.zh_counts),
            file_en_counts=dict(file_result.en_counts),
            file_zh_examples=file_result.zh_examples,
            file_en_examples=file_result.en_examples,
            zh_counts=zh_counts,
            en_counts=en_counts,
            zh_examples=zh_examples,
            en_examples=en_examples,
            zh_files=zh_files,
            en_files=en_files,
            max_examples=max_examples,
            max_files_per_term=max_files_per_term,
        )

        if want_en_phrases:
            _merge_phrase_contrib(
                md_path=md_path,
                file_en_phrase_counts=dict(file_result.en_phrase_counts),
                file_en_phrase_examples=file_result.en_phrase_examples,
                en_phrase_counts=en_phrase_counts,
                en_phrase_examples=en_phrase_examples,
                en_phrase_files=en_phrase_files,
                max_examples=max_examples,
                max_files_per_term=max_files_per_term,
            )

        _save_file_cache(
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            cache_files=cache_files,
            md_key=md_key,
            st_mtime_ns=int(st.st_mtime_ns),
            st_size=int(st.st_size),
            extractor_sig=extractor_sig,
            text=file_result.text,
            file_zh_counts=file_result.zh_counts,
            file_en_counts=file_result.en_counts,
            file_zh_examples=file_result.zh_examples,
            file_en_examples=file_result.en_examples,
            file_en_phrase_counts=file_result.en_phrase_counts,
            file_en_phrase_examples=file_result.en_phrase_examples,
            want_en_phrases=want_en_phrases,
        )

    return (
        scanned,
        cache_hits,
        cache_misses,
        processed_files,
        skipped_files,
        processed_paths_sample,
    )


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
    en_phrases: str,
    incremental: bool,
    cache_dir: Path | None,
    exclude_globs: list[str] | None = None,
) -> None:
    zh_re = re.compile(ZH_RE_TEMPLATE.format(min_len=min_zh_len, max_len=max_zh_len))

    zh_counts: Counter[str] = Counter()
    en_counts: Counter[str] = Counter()

    want_en_phrases = (en_phrases or "off") != "off"
    en_phrase_counts: Counter[str] = Counter()

    zh_examples: DefaultDict[str, list[str]] = defaultdict(list)
    en_examples: DefaultDict[str, list[str]] = defaultdict(list)
    en_phrase_examples: DefaultDict[str, list[str]] = defaultdict(list)

    zh_files: DefaultDict[str, list[str]] = defaultdict(list)
    en_files: DefaultDict[str, list[str]] = defaultdict(list)
    en_phrase_files: DefaultDict[str, list[str]] = defaultdict(list)

    extractor_sig = _extractor_signature(
        min_zh_len=min_zh_len,
        max_zh_len=max_zh_len,
        en_phrases=str(en_phrases or "off"),
    )

    cache_enabled = incremental or cache_dir is not None
    cache_dir = cache_dir
    if cache_enabled and cache_dir is None:
        cache_dir = out_dir / ".cache" / "extract_v1"

    cache_index, cache_files, cache_invalidated = _prepare_cache_state(
        cache_enabled=cache_enabled,
        cache_dir=cache_dir,
        extractor_sig=extractor_sig,
    )

    # Delta report: aggregate term changes across processed files.
    zh_added_delta: Counter[str] = Counter()
    zh_removed_delta: Counter[str] = Counter()
    en_added_delta: Counter[str] = Counter()
    en_removed_delta: Counter[str] = Counter()
    (
        scanned,
        cache_hits,
        cache_misses,
        processed_files,
        skipped_files,
        processed_paths_sample,
    ) = _scan_markdown_corpus(
        source_root=source_root,
        exclude_globs=exclude_globs,
        max_files=max_files,
        incremental=incremental,
        cache_enabled=cache_enabled,
        cache_dir=cache_dir,
        cache_files=cache_files,
        zh_re=zh_re,
        en_phrases=en_phrases,
        want_en_phrases=want_en_phrases,
        max_examples=max_examples,
        max_files_per_term=max_files_per_term,
        extractor_sig=extractor_sig,
        zh_counts=zh_counts,
        en_counts=en_counts,
        en_phrase_counts=en_phrase_counts,
        zh_examples=zh_examples,
        en_examples=en_examples,
        en_phrase_examples=en_phrase_examples,
        zh_files=zh_files,
        en_files=en_files,
        en_phrase_files=en_phrase_files,
        zh_added_delta=zh_added_delta,
        zh_removed_delta=zh_removed_delta,
        en_added_delta=en_added_delta,
        en_removed_delta=en_removed_delta,
    )

    if cache_enabled and cache_dir is not None:
        cache_index["version"] = CACHE_SCHEMA_VERSION
        cache_index["extractor_sig"] = extractor_sig
        cache_index["files"] = cache_files
        _save_cache_index(cache_dir, cache_index)

    _write_extract_outputs(
        out_dir=out_dir,
        source_root=source_root,
        scanned=scanned,
        zh_counts=zh_counts,
        en_counts=en_counts,
        en_phrase_counts=en_phrase_counts,
        zh_examples=zh_examples,
        en_examples=en_examples,
        en_phrase_examples=en_phrase_examples,
        zh_files=zh_files,
        en_files=en_files,
        en_phrase_files=en_phrase_files,
        min_count_zh=min_count_zh,
        min_count_en=min_count_en,
        topk_zh=topk_zh,
        topk_en=topk_en,
        zh_stopwords=zh_stopwords,
        en_stopwords=en_stopwords,
        want_en_phrases=want_en_phrases,
        incremental=incremental,
        cache_enabled=cache_enabled,
        cache_dir=cache_dir,
        extractor_sig=extractor_sig,
        cache_hits=cache_hits,
        cache_misses=cache_misses,
        processed_files=processed_files,
        skipped_files=skipped_files,
        cache_invalidated=cache_invalidated,
        zh_added_delta=zh_added_delta,
        zh_removed_delta=zh_removed_delta,
        en_added_delta=en_added_delta,
        en_removed_delta=en_removed_delta,
        processed_paths_sample=processed_paths_sample,
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
        "--exclude-glob",
        action="append",
        default=[],
        help=(
            "Exclude markdown files by glob (repeatable). "
            "Matched against both basename and path relative to source root. "
            "Example: --exclude-glob '*.qa_report.md'"
        ),
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

    # Stage 3.1: incremental extraction cache
    parser.add_argument(
        "--incremental",
        action="store_true",
        help=("Incremental: skip unchanged files; writes extract_delta.json"),
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help=("Cache dir (default: <out_dir>/.cache/extract_v1 when incremental)"),
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

    # Stage 4.2 (optional): phrase discovery mode
    parser.add_argument(
        "--en-phrases",
        default="off",
        choices=["off", "rake"],
        help=(
            "Optional English phrase discovery mode "
            "(writes candidates_en_phrases.tsv). "
            "Default: off"
        ),
    )

    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    source_root = Path(
        args.source_root or cfg.get("sources", {}).get("root", ".")
    ).expanduser()
    out_dir = Path(
        args.out_dir or cfg.get("artifacts", {}).get("out_dir", "artifacts")
    ).expanduser()

    min_zh_len = int(args.min_zh_len or cfg.get("extract", {}).get("min_zh_len", 2))
    max_zh_len = int(args.max_zh_len or cfg.get("extract", {}).get("max_zh_len", 8))
    max_examples = int(
        args.max_examples or cfg.get("extract", {}).get("max_examples", 3)
    )
    max_files_per_term = int(
        args.max_files_per_term or cfg.get("extract", {}).get("max_files_per_term", 20)
    )

    def load_stopwords(path_str: str | None) -> set[str] | None:
        if not path_str:
            return None
        p = Path(path_str).expanduser()
        if not p.exists():
            raise SystemExit(f"stopwords file does not exist: {p}")
        out: set[str] = set()
        try:
            lines = p.read_text("utf-8").splitlines()
        except UnicodeDecodeError as e:
            raise SystemExit(
                f"stopwords file is not valid UTF-8: {p} ({e}). "
                "Tip: re-save stopwords as UTF-8 without BOM."
            ) from e

        for line in lines:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.add(s)
        return out

    zh_stop = load_stopwords(args.zh_stopwords)
    en_stop = load_stopwords(args.en_stopwords)

    if not source_root.exists():
        raise SystemExit(f"source root does not exist: {source_root}")

    # Optional: exclude derived/noise markdown files.
    cfg_ex = cfg.get("sources", {}).get("exclude_globs", [])
    exclude_globs: list[str] = []
    if isinstance(cfg_ex, list):
        exclude_globs.extend([str(x) for x in cfg_ex if str(x).strip()])
    elif isinstance(cfg_ex, str) and cfg_ex.strip():
        exclude_globs.append(cfg_ex.strip())

    exclude_globs.extend([str(x) for x in (args.exclude_glob or []) if str(x).strip()])

    cache_dir = Path(args.cache_dir).expanduser() if args.cache_dir else None

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
        en_phrases=str(args.en_phrases),
        incremental=bool(args.incremental),
        cache_dir=cache_dir,
        exclude_globs=exclude_globs or None,
    )


if __name__ == "__main__":
    main()
