#!/usr/bin/env python3
"""Import approved terminology entries from a reviewed diff TSV into the registry.

Reads a diff TSV where the ``status`` column has been changed from
``new``/``exists``/``conflict`` to ``approved``/``rejected``/``defer``.
Appends approved entries to concepts.tsv, aliases.tsv, and evidence.tsv.

The diff TSV must include at minimum:
    term, status, [definition], [zh]

For approved entries, the script generates:
    - A concept_id from the term name
    - A concepts.tsv row with the given source
    - An aliases.tsv row (preferred, en)
    - An evidence.tsv row

Usage:
    python3 scripts/import_approved_terms.py \
        --diff artifacts/terminology_sources/iter_glossary_diff.tsv \
        --source ITER-glossary \
        --evidence-url "https://www.iter.org/fusion-glossary"

    python3 scripts/import_approved_terms.py --dry-run \
        --diff artifacts/terminology_sources/iaea_glossary_diff.tsv \
        --source IAEA-safety-glossary \
        --evidence-url "IAEA-Safety-Glossary-2018"
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REGISTRY_DIR = Path("terms/registry")


def _slugify(term: str) -> str:
    """Convert a term name to a concept_id slug."""
    s = term.lower().strip()
    # Remove parenthetical qualifiers like "(plasma)"
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)
    # Replace non-alphanumeric with hyphens
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    # Collapse multiple hyphens
    s = re.sub(r"-{2,}", "-", s)
    return s


def _load_existing_concept_ids(concepts_path: Path) -> set[str]:
    ids: set[str] = set()
    for line in concepts_path.read_text("utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if parts:
            ids.add(parts[0].strip())
    return ids


def _load_existing_aliases(aliases_path: Path) -> set[str]:
    aliases: set[str] = set()
    for line in aliases_path.read_text("utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if parts:
            aliases.add(parts[0].strip().lower())
    return aliases


def _load_diff(diff_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = diff_path.read_text("utf-8").splitlines()
    header_cols: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            stripped = line.lstrip("# ").strip()
            header_cols = [c.strip() for c in stripped.split("\t")]
            continue
        parts = [c.strip() for c in line.split("\t")]
        row: dict[str, str] = {}
        for idx, val in enumerate(parts):
            col_name = header_cols[idx] if idx < len(header_cols) else f"col{idx}"
            row[col_name] = val
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--diff", type=Path, required=True,
        help="Path to the reviewed diff TSV",
    )
    parser.add_argument(
        "--source", type=str, required=True,
        help="Source tag for concepts.tsv (e.g. ITER-glossary)",
    )
    parser.add_argument(
        "--evidence-url", type=str, required=True,
        help="Evidence source URL or identifier",
    )
    parser.add_argument(
        "--category", type=str, default="concept",
        help="Default category for new concepts (default: concept)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be done without writing",
    )
    args = parser.parse_args()

    if not args.diff.exists():
        print(f"ERROR: diff file not found: {args.diff}", file=sys.stderr)
        sys.exit(1)

    concepts_path = REGISTRY_DIR / "concepts.tsv"
    aliases_path = REGISTRY_DIR / "aliases.tsv"
    evidence_path = REGISTRY_DIR / "evidence.tsv"

    existing_ids = _load_existing_concept_ids(concepts_path)
    existing_aliases = _load_existing_aliases(aliases_path)

    diff_rows = _load_diff(args.diff)
    approved = [r for r in diff_rows if r.get("status") == "approved"]

    if not approved:
        print("No approved entries found in diff file.")
        print(f"  Total rows: {len(diff_rows)}")
        statuses = {}
        for r in diff_rows:
            s = r.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        for s, c in sorted(statuses.items()):
            print(f"  {s}: {c}")
        return

    print(f"Processing {len(approved)} approved entries ...")

    new_concepts: list[str] = []
    new_aliases: list[str] = []
    new_evidence: list[str] = []
    skipped: list[str] = []
    today = date.today().isoformat()

    for row in approved:
        term = row.get("term", "").strip()
        if not term:
            continue

        concept_id = _slugify(term)
        if not concept_id:
            skipped.append(f"  SKIP (empty slug): {term}")
            continue

        if concept_id in existing_ids:
            skipped.append(f"  SKIP (concept_id exists): {concept_id} ← {term}")
            continue

        # Check for alias collision
        term_lower = term.lower()
        if term_lower in existing_aliases:
            skipped.append(f"  SKIP (alias exists): {term}")
            continue

        zh = row.get("zh", "")
        en = term  # The term from the source IS the English name
        definition = row.get("definition", "")
        abbr = ""

        # concepts.tsv: concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source
        concept_line = "\t".join([
            concept_id, args.category, zh, en, abbr,
            "active", definition[:100] if definition else "", args.source,
        ])

        # aliases.tsv: alias, concept_id, lang, kind, comment
        alias_line = f"{en}\t{concept_id}\ten\tpreferred\timported from {args.source}"
        alias_lines_extra = []
        if zh:
            alias_lines_extra.append(f"{zh}\t{concept_id}\tzh\tpreferred\timported from {args.source}")

        # evidence.tsv: concept_id, source, quote, added_by, added_at
        evidence_line = f"{concept_id}\t{args.evidence_url}\t\timport_approved_terms\t{today}"

        new_concepts.append(concept_line)
        new_aliases.append(alias_line)
        new_aliases.extend(alias_lines_extra)
        new_evidence.append(evidence_line)
        existing_ids.add(concept_id)
        existing_aliases.add(term_lower)
        if zh:
            existing_aliases.add(zh.lower())

    print("\nResults:")
    print(f"  New concepts: {len(new_concepts)}")
    print(f"  New aliases:  {len(new_aliases)}")
    print(f"  New evidence: {len(new_evidence)}")
    print(f"  Skipped:      {len(skipped)}")

    if skipped:
        for s in skipped[:20]:
            print(s)
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")

    if args.dry_run:
        print("\n[DRY RUN] No files modified.")
        if new_concepts:
            print("\nSample concept lines:")
            for c in new_concepts[:3]:
                print(f"  {c}")
        return

    # Append to files
    with open(concepts_path, "a", encoding="utf-8") as f:
        f.write("\n# ---- Imported from " + args.source + f" ({today}) ----\n")
        for line in new_concepts:
            f.write(line + "\n")

    with open(aliases_path, "a", encoding="utf-8") as f:
        f.write("\n# ---- Imported from " + args.source + f" ({today}) ----\n")
        for line in new_aliases:
            f.write(line + "\n")

    with open(evidence_path, "a", encoding="utf-8") as f:
        for line in new_evidence:
            f.write(line + "\n")

    print(f"\nAppended to {concepts_path}, {aliases_path}, {evidence_path}")


if __name__ == "__main__":
    main()
