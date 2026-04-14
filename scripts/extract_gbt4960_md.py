#!/usr/bin/env python3
"""Extract terminology from GB/T 4960.9-2013 Markdown (converted via pdf2md).

Parses the structured Markdown that pdf2md produced from the scanned PDF.
Each term entry follows the pattern:

    2.1.1                          ← numbered line (alone)
                                   ← blank line
    中文术语 English term[; ABBR]  ← zh + en on same line
                                   ← blank or next paragraph
    定义文本...                     ← definition (zero or more lines)

Output: TSV with columns  term_id  zh  en  abbr  definition  status

Usage:
    python3 scripts/extract_gbt4960_md.py [--md PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MD_PATH = Path.home() / "Zotero/storage/B2RVUCN5/GB-T 4960.md"
OUT_PATH = Path("artifacts/terminology_sources/gbt4960_9_terms.tsv")

# Match a standalone numbered entry like  2.1.1  or  2.4.73
# Allow OCR spacing artifacts like  "2. 1. 101"  or  "2. 1.303"
# Also match heading-style entries like  "# 2.3.1"
RE_NUM = re.compile(r"^(?:#\s+)?(\d+)\.\s*(\d+)\.\s*(\d+)$")

# Match the "Chinese English[; ABBR]" line.
# Chinese portion: CJK chars (+ some punctuation / LaTeX artefacts / α β θ)
# English portion: starts with lowercase/uppercase ASCII letter
# Optional abbreviation after semicolon.
RE_TERM_LINE = re.compile(
    r"^(.+?)\s+"                       # Chinese part (greedy-lazy up to space before English)
    r"([A-Za-z][\w\s\-/(),.'·]+)"      # English part
    r"(?:;\s*([A-Z][A-Za-z0-9\-/]+))?" # optional abbreviation after ;
    r"\s*$"
)


def _clean_latex(text: str) -> str:
    """Remove Markdown / LaTeX artefacts from OCR-converted text."""
    # Common LaTeX wrappers
    text = re.sub(r"\$[^$]*\$", lambda m: _latex_to_text(m.group(0)), text)
    # Bold markers
    text = text.replace("**", "")
    # Normalize full-width parentheses to ASCII
    text = text.replace("（", "(").replace("）", ")")
    # Normalize curly/smart quotes to ASCII
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # Private-use-area chars
    text = re.sub(r"[\ue000-\uf8ff]", " ", text)
    # Collapse whitespace
    text = re.sub(r"  +", " ", text).strip()
    return text


def _latex_to_text(latex: str) -> str:
    """Best-effort convert simple LaTeX to plain text."""
    s = latex.strip("$").strip()
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\pmb\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\alpha", "α", s)
    s = re.sub(r"\\beta", "β", s)
    s = re.sub(r"\\theta", "θ", s)
    s = re.sub(r"\\gamma", "γ", s)
    s = re.sub(r"[{}\\]", "", s)
    return s.strip()


def _split_zh_en(line: str) -> tuple[str, str, str]:
    """Split a combined zh+en term line into (zh, en, abbr).

    The Chinese portion ends where an ASCII-letter word starts.
    Abbreviation follows a semicolon after the English part.
    """
    line = _clean_latex(line)

    # Try to find where English text starts: first run of ASCII letter
    # preceded by whitespace.  Chinese text may contain ASCII digits
    # and parentheses but not leading ASCII letter words.
    # Also match CamelCase/joined words (OCR artifact) like "InternationalThermonuclear..."
    # Also match quote-prefixed English like "active"environment
    m = re.search(r'(?<=\s)(["\']?[A-Za-z][\w\s\-/(),.\'"·:;]+)$', line)
    if not m:
        # Entire line is Chinese (no English)
        return line.strip(), "", ""

    en_raw = m.group(1).strip()
    zh = line[: m.start()].strip()

    # Split off abbreviation after ";" (with or without space)
    abbr = ""
    if ";" in en_raw:
        parts = en_raw.rsplit(";", 1)
        en_clean = parts[0].strip()
        abbr_candidate = parts[1].strip()
        # Only treat as abbreviation if short and uppercase-ish
        if len(abbr_candidate) <= 20 and re.match(r"^[A-Z][\w\-/]+", abbr_candidate):
            abbr = re.match(r"^[A-Z][\w\-/]+", abbr_candidate).group(0)
            en_raw = en_clean

    # Fix OCR joined words: insert space before internal uppercase letters
    # e.g. "InternationalThermonuclearExperimentalReactor" →
    #      "International Thermonuclear Experimental Reactor"
    if en_raw and " " not in en_raw and len(en_raw) > 20:
        en_raw = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", en_raw)

    return zh, en_raw.strip(), abbr


def parse_markdown(md_text: str) -> list[dict[str, str]]:
    """Parse the GB/T 4960.9 markdown into a list of term dicts."""
    lines = md_text.split("\n")
    entries: list[dict[str, str]] = []

    i = 0
    n = len(lines)
    # Track where the index / appendix starts so we stop before it
    while i < n:
        line = lines[i].strip()

        # Stop at the index section
        if line in ("# 索引", "索引", "# 汉语拼音索引", "汉语拼音索引"):
            break

        # Match numbered entry
        m = RE_NUM.match(line)
        if not m:
            i += 1
            continue

        term_id = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"

        # Skip blank lines after the number
        j = i + 1
        while j < n and not lines[j].strip():
            j += 1

        if j >= n:
            break

        # The next non-blank line should be the term line (zh + en)
        term_line = lines[j].strip()
        j += 1

        # Some OCR entries may have the term split across two lines
        # (e.g. zh on one line, en on the next).  Try merging if the
        # first line looks entirely Chinese.
        if term_line and not re.search(r"[A-Za-z]", term_line):
            # Skip blanks
            k = j
            while k < n and not lines[k].strip():
                k += 1
            if k < n:
                next_line = lines[k].strip()
                if re.match(r"[A-Za-z]", next_line):
                    term_line = term_line + " " + next_line
                    j = k + 1

        zh, en, abbr = _split_zh_en(term_line)

        # Collect definition lines until the next numbered entry or section heading
        def_lines: list[str] = []
        while j < n:
            dl = lines[j].strip()
            # Stop conditions
            if RE_NUM.match(dl):
                break
            if dl.startswith("# "):
                break
            if dl in ("索引", "汉语拼音索引"):
                break
            # Check if a line ends with an inline entry number (OCR artifact)
            # e.g. "...与离子密度平方根成反比。2.1.11"
            m_inline = re.search(r"[。）)](\d+\.\s*\d+\.\s*\d+)\s*$", dl)
            if m_inline:
                # Keep the definition text before the number
                before = dl[: m_inline.start() + 1]  # include the punctuation
                if before.strip():
                    def_lines.append(before.strip())
                # Inject the number as a virtual standalone line for the next iteration
                inline_id = re.sub(r"\s+", "", m_inline.group(1))
                lines[j] = inline_id  # overwrite so RE_NUM catches it
                break
            # Skip blank lines (but allow them inside definitions)
            if dl:
                def_lines.append(dl)
            j += 1

        definition = _clean_latex(" ".join(def_lines))
        # Strip notes — lines starting with 注：
        # Keep the note as part of the definition for full fidelity
        definition = re.sub(r"\s+", " ", definition).strip()

        if zh or en:
            entries.append({
                "term_id": term_id,
                "zh": zh,
                "en": en,
                "abbr": abbr,
                "definition": definition,
                "status": "draft",
            })

        i = j

    return entries


def write_tsv(entries: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# term_id\tzh\ten\tabbr\tdefinition\tstatus\n")
        for e in entries:
            vals = [
                e.get("term_id", ""),
                e.get("zh", "").replace("\t", " "),
                e.get("en", "").replace("\t", " "),
                e.get("abbr", "").replace("\t", " "),
                e.get("definition", "").replace("\t", " ").replace("\n", " "),
                e.get("status", "draft"),
            ]
            f.write("\t".join(vals) + "\n")
    print(f"Wrote {out_path}  ({len(entries)} entries)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", type=Path, default=MD_PATH, help="Path to the converted Markdown file")
    parser.add_argument("--out", type=Path, default=OUT_PATH, help="Output TSV path")
    args = parser.parse_args()

    if not args.md.exists():
        print(f"ERROR: Markdown file not found: {args.md}", file=sys.stderr)
        print("Run pdf2md first to convert the GB/T 4960.9 PDF.", file=sys.stderr)
        raise SystemExit(1)

    print(f"Reading {args.md} ...")
    md_text = args.md.read_text(encoding="utf-8")
    print(f"  {len(md_text):,} chars, {md_text.count(chr(10)):,} lines")

    entries = parse_markdown(md_text)
    print(f"  Extracted {len(entries)} term entries")

    # Summary by section
    sections: dict[str, int] = {}
    for e in entries:
        sec = ".".join(e["term_id"].split(".")[:2])
        sections[sec] = sections.get(sec, 0) + 1
    for sec, cnt in sorted(sections.items()):
        print(f"    Section {sec}: {cnt} terms")

    # Check for entries without English
    no_en = [e for e in entries if not e["en"]]
    if no_en:
        print(f"  WARNING: {len(no_en)} entries without English term:")
        for e in no_en[:10]:
            print(f"    {e['term_id']} {e['zh']}")

    write_tsv(entries, args.out)


if __name__ == "__main__":
    main()
