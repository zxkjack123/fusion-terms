#!/usr/bin/env python3
"""Extract terminology entries from the IAEA Safety Glossary 2018 PDF.

Parses the output of ``pdftotext -layout`` to identify glossary entries
(term name + definition text) and outputs a staging TSV.

Usage:
    python3 scripts/extract_iaea_glossary.py

Requires: pdftotext (from poppler-utils).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PDF_PATH = Path("artifacts/terminology_sources/IAEA_Safety_Glossary_2018.pdf")
OUT_PATH = Path("artifacts/terminology_sources/iaea_safety_glossary_raw.tsv")

# Glossary entries start around page 23 and end before the bibliography (~page 247).
# Adjust if the PDF version differs.
FIRST_PAGE = 23
LAST_PAGE = 250


def _extract_text(pdf_path: Path) -> str:
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("pdftotext"):
        print("ERROR: pdftotext not found. Install poppler-utils.", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        [
            "pdftotext",
            "-layout",
            "-f",
            str(FIRST_PAGE),
            "-l",
            str(LAST_PAGE),
            str(pdf_path),
            "-",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"ERROR: pdftotext failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def _is_term_line(line: str) -> bool:
    """Detect a glossary term heading line.

    Term lines are left-aligned (indent ≤ 12 chars) with alphabetic content,
    not all-uppercase page headers (like 'A', 'B', ...), and not blank.
    """
    stripped = line.strip()
    if not stripped:
        return False

    # Skip the "superseded" boilerplate
    if "superseded" in stripped.lower():
        return False

    # Skip single-letter section headers (A, B, C, ...)
    if re.match(r"^[A-Z]$", stripped):
        return False

    # Skip page numbers
    if re.match(r"^\d+$", stripped):
        return False

    # Skip lines starting with special markers
    if (
        stripped.startswith("!")
        or stripped.startswith("(")
        or stripped.startswith("See ")
    ):
        return False

    # Term lines: indented ≤ 12 chars from left, start with a letter
    indent = len(line) - len(line.lstrip())
    if indent > 12:
        return False

    # Must start with a letter (term name)
    if not stripped[0].isalpha():
        return False

    # Should not look like a continuation sentence (lowercase start with articles etc.)
    # Actual terms start with uppercase or are well-known lowercase terms
    # But many legitimate terms start lowercase... be lenient
    # Heuristic: term lines typically don't start with common sentence starters
    sentence_starters = {
        "the ",
        "a ",
        "an ",
        "in ",
        "by ",
        "for ",
        "of ",
        "to ",
        "as ",
        "it ",
        "is ",
    }
    lower_stripped = stripped.lower()
    if any(lower_stripped.startswith(s) for s in sentence_starters):
        return False

    # Must not contain definition-like patterns (long text with periods mid-line)
    if len(stripped) > 120:
        return False

    return True


def _clean_definition(lines: list[str]) -> str:
    """Join and clean definition lines."""
    text = " ".join(line.strip() for line in lines if line.strip())
    # Remove internal excess whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Remove leading bullet markers
    text = re.sub(r"^[\u2022\u2013\u2014•–—]\s*", "", text)
    return text


def parse_glossary(raw_text: str) -> list[dict[str, str]]:
    """Parse glossary entries from pdftotext layout output."""
    lines = raw_text.split("\n")
    entries: list[dict[str, str]] = []
    current_term: str | None = None
    current_def_lines: list[str] = []
    prev_blank = True  # treat start as blank

    for line in lines:
        # Skip page header/footer boilerplate
        if "superseded" in line.lower():
            prev_blank = True
            continue
        if re.match(r"^\s*\d+\s*$", line.strip()):
            prev_blank = True
            continue

        stripped = line.strip()
        if not stripped:
            prev_blank = True
            continue

        # Single-letter section headers (A, B, C, ...) act as separators
        if re.match(r"^[A-Z]$", stripped):
            prev_blank = True
            continue

        if prev_blank and _is_term_line(line):
            # Save previous entry
            if current_term:
                defn = _clean_definition(current_def_lines)
                entries.append({"term": current_term, "definition": defn})

            current_term = stripped
            current_def_lines = []
        elif current_term is not None:
            # Accumulate definition lines
            current_def_lines.append(stripped)

        prev_blank = False

    # Save last entry
    if current_term:
        defn = _clean_definition(current_def_lines)
        entries.append({"term": current_term, "definition": defn})

    return entries


def _postprocess(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    """Clean up extracted entries."""
    cleaned: list[dict[str, str]] = []
    seen_terms: set[str] = set()

    for e in entries:
        term = e["term"].strip()
        # Skip entries that are cross-references only
        defn = e["definition"].strip()
        if not term:
            continue

        # Remove numbering prefix like "1. " or "2. "
        term = re.sub(r"^\d+\.\s*", "", term).strip()

        # Skip very short non-word terms
        if len(term) < 2:
            continue

        # Deduplicate
        key = term.lower()
        if key in seen_terms:
            continue
        seen_terms.add(key)

        cleaned.append({"term": term, "definition": defn})

    return cleaned


def main() -> None:
    print(f"Extracting text from {PDF_PATH} (pages {FIRST_PAGE}-{LAST_PAGE}) ...")
    raw_text = _extract_text(PDF_PATH)
    print(f"  Text length: {len(raw_text):,} chars")

    entries = parse_glossary(raw_text)
    print(f"  Raw entries: {len(entries)}")

    entries = _postprocess(entries)
    print(f"  After cleanup: {len(entries)}")

    if len(entries) < 100:
        print(
            f"WARNING: only {len(entries)} entries extracted — may need parsing adjustments",
            file=sys.stderr,
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("# term\tdefinition\n")
        for e in entries:
            term = e["term"].replace("\t", " ")
            defn = e["definition"].replace("\t", " ").replace("\n", " ")
            f.write(f"{term}\t{defn}\n")

    print(f"  Wrote {OUT_PATH} ({len(entries)} entries)")

    # Spot-check: look for known terms
    known = {"activation", "dose", "decommissioning", "waste", "criticality"}
    found = {e["term"].lower() for e in entries}
    for k in known:
        if k in found:
            print(f"  ✓ Found '{k}'")
        else:
            print(f"  ✗ Missing '{k}' (may be in a variant form)")


if __name__ == "__main__":
    main()
