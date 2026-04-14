#!/usr/bin/env python3
"""Fetch the ITER Fusion Glossary and output a staging TSV.

Scrapes https://www.iter.org/fusion-glossary for term names and definitions,
writing to artifacts/terminology_sources/iter_glossary_raw.tsv.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://www.iter.org/fusion-glossary"
OUT_DIR = Path("artifacts/terminology_sources")


def _fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": "fusion-terms/1.0 (terminology research)"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def _clean_text(s: str) -> str:
    s = html.unescape(s)
    s = _strip_tags(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_glossary(raw_html: str) -> list[dict[str, str]]:
    """Extract term/definition pairs from accordion-faq structure."""
    items: list[dict[str, str]] = []

    # Each glossary entry is an accordion-faq__item containing:
    #   - accordion-faq__title with the term name
    #   - content-rte node n-glossary with the definition
    # We extract them pairwise.
    title_pattern = re.compile(
        r'accordion-faq__title[^>]*>(.*?)</(?:span|h\d|div)',
        re.DOTALL,
    )
    # Definition: article with class content-rte node n-glossary
    def_pattern = re.compile(
        r'class="content-rte\s+node\s+n-glossary[^"]*"[^>]*>(.*?)</article>',
        re.DOTALL,
    )

    titles_raw = title_pattern.findall(raw_html)
    defs_raw = def_pattern.findall(raw_html)

    # If definition count doesn't match, fall back to extracting definitions
    # from the broader accordion blocks.
    if len(defs_raw) != len(titles_raw):
        # Fallback: extract from accordion-faq__well blocks
        well_pattern = re.compile(
            r'accordion-faq__well[^>]*>(.*?)</div>\s*</div>\s*</div>',
            re.DOTALL,
        )
        defs_raw = well_pattern.findall(raw_html)

    for i, title_html in enumerate(titles_raw):
        term = _clean_text(title_html)
        if not term:
            continue
        definition = ""
        if i < len(defs_raw):
            definition = _clean_text(defs_raw[i])
        items.append({"term": term, "definition": definition})

    return items


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "iter_glossary_raw.tsv"

    print(f"Fetching {URL} ...")
    raw_html = _fetch_html(URL)
    print(f"  HTML size: {len(raw_html):,} bytes")

    items = parse_glossary(raw_html)
    print(f"  Extracted {len(items)} terms")

    if len(items) < 50:
        print(
            "ERROR: extracted fewer than 50 terms — the page structure may have changed.",
            file=sys.stderr,
        )
        sys.exit(1)

    fetch_date = date.today().isoformat()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# term\tdefinition\tfetch_date\n")
        for item in items:
            term = item["term"].replace("\t", " ")
            defn = item["definition"].replace("\t", " ").replace("\n", " ")
            f.write(f"{term}\t{defn}\t{fetch_date}\n")

    print(f"  Wrote {out_path} ({len(items)} entries)")

    # Quick sanity checks
    no_def = sum(1 for it in items if not it["definition"])
    if no_def > 0:
        print(f"  Note: {no_def} terms have empty definitions")

    # Check for HTML residue
    html_residue = sum(1 for it in items if "<" in it["term"] or ">" in it["term"])
    if html_residue:
        print(f"  WARNING: {html_residue} terms contain HTML tag residue", file=sys.stderr)


if __name__ == "__main__":
    main()
