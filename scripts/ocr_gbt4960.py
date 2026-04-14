#!/usr/bin/env python3
"""OCR-extract text from GB/T 4960.9-2013 scanned PDF and parse terminology pairs.

This script performs two stages:
1. OCR: Convert scanned PDF pages to text using tesseract (chi_sim+eng)
2. Parse: Extract structured term entries (number, zh, en, definition)

Prerequisites:
    sudo apt install tesseract-ocr tesseract-ocr-chi-sim poppler-utils
    pip install pytesseract pdf2image

Usage:
    python3 scripts/ocr_gbt4960.py              # OCR + parse
    python3 scripts/ocr_gbt4960.py --ocr-only    # OCR only (save raw text)
    python3 scripts/ocr_gbt4960.py --parse-only   # Parse existing OCR text
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PDF_PATH = Path.home() / "Zotero/storage/B2RVUCN5/GB-T 4960.pdf"
OUT_DIR = Path("artifacts/terminology_sources")
OCR_RAW_PATH = OUT_DIR / "gbt4960_9_ocr_raw.txt"
TERMS_PATH = OUT_DIR / "gbt4960_9_terms.tsv"


def _check_deps() -> None:
    """Check that required tools are installed."""
    missing = []
    if not shutil.which("tesseract"):
        missing.append("tesseract-ocr (sudo apt install tesseract-ocr tesseract-ocr-chi-sim)")
    if not shutil.which("pdftoppm"):
        missing.append("poppler-utils (sudo apt install poppler-utils)")

    if missing:
        print("ERROR: missing dependencies:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        sys.exit(1)

    # Check chi_sim language pack
    result = subprocess.run(
        ["tesseract", "--list-langs"],
        capture_output=True, text=True, timeout=10,
    )
    if "chi_sim" not in result.stdout:
        print(
            "ERROR: tesseract chi_sim language pack not installed.\n"
            "  sudo apt install tesseract-ocr-chi-sim",
            file=sys.stderr,
        )
        sys.exit(1)


def ocr_pdf(pdf_path: Path, output_path: Path) -> str:
    """OCR a scanned PDF using pdftoppm + tesseract, page by page."""
    import tempfile

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    all_text: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        # Convert PDF to images
        print("  Converting PDF to images ...")
        subprocess.run(
            ["pdftoppm", "-png", "-r", "300", str(pdf_path), str(tmp / "page")],
            check=True, timeout=600,
        )
        pages = sorted(tmp.glob("page-*.png"))
        print(f"  {len(pages)} page images generated")

        for i, page_img in enumerate(pages, 1):
            if i % 10 == 0:
                print(f"  OCR page {i}/{len(pages)} ...")
            result = subprocess.run(
                ["tesseract", str(page_img), "stdout", "-l", "chi_sim+eng"],
                capture_output=True, text=True, timeout=120,
            )
            all_text.append(f"--- PAGE {i} ---\n{result.stdout}")

    full_text = "\n".join(all_text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_text, encoding="utf-8")
    print(f"  Wrote {output_path} ({len(full_text):,} chars)")
    return full_text


def parse_terms(ocr_text: str) -> list[dict[str, str]]:
    """Extract structured terminology entries from OCR text.

    GB/T 4960.9 format:
        2.1.1
        等离子体
        plasma
        由...组成的...（definition）

    Or inline:
        2.1.1  等离子体  plasma  由...
    """
    entries: list[dict[str, str]] = []

    # Pattern for numbered entries: digits.digits[.digits]
    num_pattern = re.compile(r"^(\d+\.\d+(?:\.\d+)?)\s*$")
    # Chinese text line
    zh_pattern = re.compile(r"^([\u4e00-\u9fff][\u4e00-\u9fff\w\s（）()、]+)$")
    # English text line
    en_pattern = re.compile(r"^([A-Za-z][\w\s\-,()]+)$")
    # Inline pattern: number + zh + en (on one line)
    inline_pattern = re.compile(
        r"(\d+\.\d+(?:\.\d+)?)\s+"
        r"([\u4e00-\u9fff][\u4e00-\u9fff\w（）()、]*)\s+"
        r"([A-Za-z][\w\s\-,()]*)"
    )

    lines = ocr_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Try inline match first
        m_inline = inline_pattern.match(line)
        if m_inline:
            entry = {
                "term_id": m_inline.group(1),
                "zh": m_inline.group(2).strip(),
                "en": m_inline.group(3).strip(),
                "definition": "",
                "status": "draft",
            }
            # Collect definition from subsequent indented lines
            j = i + 1
            def_lines = []
            while j < len(lines) and lines[j].strip() and not num_pattern.match(lines[j].strip()) and not inline_pattern.match(lines[j].strip()):
                def_lines.append(lines[j].strip())
                j += 1
            entry["definition"] = " ".join(def_lines)
            entries.append(entry)
            i = j
            continue

        # Try multi-line: number, then zh, then en
        m_num = num_pattern.match(line)
        if m_num:
            term_id = m_num.group(1)
            zh = ""
            en = ""
            definition = ""
            j = i + 1
            # Look for zh line
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                m_zh = zh_pattern.match(lines[j].strip())
                if m_zh:
                    zh = m_zh.group(1).strip()
                    j += 1
            # Look for en line
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                m_en = en_pattern.match(lines[j].strip())
                if m_en:
                    en = m_en.group(1).strip()
                    j += 1
            # Collect definition
            def_lines = []
            while j < len(lines) and lines[j].strip() and not num_pattern.match(lines[j].strip()) and not inline_pattern.match(lines[j].strip()):
                def_lines.append(lines[j].strip())
                j += 1
            definition = " ".join(def_lines)

            if zh or en:
                entries.append({
                    "term_id": term_id,
                    "zh": zh,
                    "en": en,
                    "definition": definition,
                    "status": "draft",
                })
            i = j
            continue

        i += 1

    return entries


def write_terms(entries: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# term_id\tzh\ten\tdefinition\tstatus\n")
        for e in entries:
            vals = [
                e.get("term_id", ""),
                e.get("zh", "").replace("\t", " "),
                e.get("en", "").replace("\t", " "),
                e.get("definition", "").replace("\t", " ").replace("\n", " "),
                e.get("status", "draft"),
            ]
            f.write("\t".join(vals) + "\n")
    print(f"  Wrote {output_path} ({len(entries)} entries)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ocr-only", action="store_true", help="Only run OCR, skip parsing")
    parser.add_argument("--parse-only", action="store_true", help="Only parse existing OCR text")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not args.parse_only:
        _check_deps()
        print(f"OCR processing {PDF_PATH} ...")
        ocr_text = ocr_pdf(PDF_PATH, OCR_RAW_PATH)
    else:
        if not OCR_RAW_PATH.exists():
            print(f"ERROR: OCR text not found: {OCR_RAW_PATH}", file=sys.stderr)
            sys.exit(1)
        ocr_text = OCR_RAW_PATH.read_text("utf-8")
        print(f"Loaded existing OCR text: {len(ocr_text):,} chars")

    if not args.ocr_only:
        print("Parsing terminology entries ...")
        entries = parse_terms(ocr_text)
        print(f"  Found {len(entries)} entries")
        write_terms(entries, TERMS_PATH)

        # Quality check
        zh_count = sum(1 for e in entries if e["zh"])
        en_count = sum(1 for e in entries if e["en"])
        print(f"  With zh: {zh_count}, with en: {en_count}")

        if len(entries) < 50:
            print(
                f"WARNING: only {len(entries)} entries — OCR quality may be poor",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
