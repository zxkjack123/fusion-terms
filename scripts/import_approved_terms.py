#!/usr/bin/env python3
"""Import terminology entries from a diff TSV into the registry.

Reads a diff TSV and imports entries into concepts.tsv, aliases.tsv,
evidence.tsv, and definitions.tsv.

Two modes:
  - Default: only import rows where ``status`` == ``approved``
  - ``--import-all``: import all rows (``new`` → new concept, ``exists`` → definition only,
    ``conflict`` → skipped unless handled by ``--conflict-map``)

The diff TSV must include at minimum:  term, status, [definition], [zh]

Usage:
    # Import all ITER glossary terms
    python3 scripts/import_approved_terms.py --import-all \
        --diff artifacts/terminology_sources/iter_glossary_diff.tsv \
        --source ITER-glossary \
        --evidence-url "https://www.iter.org/fusion-glossary"

    # Import only approved rows
    python3 scripts/import_approved_terms.py \
        --diff artifacts/terminology_sources/iaea_glossary_diff.tsv \
        --source IAEA-safety-glossary \
        --evidence-url "IAEA-Safety-Glossary-2018"

    # Handle conflict entries with explicit concept_id mapping
    python3 scripts/import_approved_terms.py --import-all \
        --diff diff.tsv --source SRC --evidence-url URL \
        --conflict-map "Q=q-fusion-gain"
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
        "--import-all", action="store_true",
        help="Import all rows: 'new' as new concepts, 'exists' for definitions only",
    )
    parser.add_argument(
        "--conflict-map", type=str, action="append", default=[],
        help="Map conflict term to concept_id: 'TERM=concept-id' (repeatable)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be done without writing",
    )
    args = parser.parse_args()

    if not args.diff.exists():
        print(f"ERROR: diff file not found: {args.diff}", file=sys.stderr)
        sys.exit(1)

    # Parse conflict map
    conflict_map: dict[str, str] = {}
    for spec in args.conflict_map:
        if "=" not in spec:
            print(f"ERROR: --conflict-map must be TERM=concept-id, got: {spec}", file=sys.stderr)
            sys.exit(1)
        term_key, cid = spec.split("=", 1)
        conflict_map[term_key.strip()] = cid.strip()

    concepts_path = REGISTRY_DIR / "concepts.tsv"
    aliases_path = REGISTRY_DIR / "aliases.tsv"
    evidence_path = REGISTRY_DIR / "evidence.tsv"
    definitions_path = REGISTRY_DIR / "definitions.tsv"

    existing_ids = _load_existing_concept_ids(concepts_path)
    existing_aliases = _load_existing_aliases(aliases_path)

    diff_rows = _load_diff(args.diff)

    if args.import_all:
        candidates = diff_rows
    else:
        candidates = [r for r in diff_rows if r.get("status") == "approved"]

    if not candidates:
        print("No importable entries found in diff file.")
        print(f"  Total rows: {len(diff_rows)}")
        statuses: dict[str, int] = {}
        for r in diff_rows:
            s = r.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        for s, c in sorted(statuses.items()):
            print(f"  {s}: {c}")
        return

    print(f"Processing {len(candidates)} entries ...")

    new_concepts: list[str] = []
    new_aliases: list[str] = []
    new_evidence: list[str] = []
    new_definitions: list[str] = []
    skipped: list[str] = []
    stats = {"new_concept": 0, "def_only": 0, "conflict_resolved": 0, "skipped": 0}
    today = date.today().isoformat()

    for row in candidates:
        term = row.get("term", "").strip()
        if not term:
            continue

        status = row.get("status", "")
        definition = row.get("definition", "").strip()
        matched_ids = row.get("matched_concept_id", "").strip()

        # --- Handle conflict entries ---
        if status == "conflict":
            if term in conflict_map:
                concept_id = conflict_map[term]
                if concept_id in existing_ids and definition:
                    new_definitions.append(
                        f"{concept_id}\ten\t{definition}\t{args.source}"
                    )
                    stats["conflict_resolved"] += 1
                    stats["def_only"] += 1
                elif concept_id not in existing_ids:
                    skipped.append(f"  SKIP (conflict-map concept_id not found): {term} → {concept_id}")
                    stats["skipped"] += 1
                continue
            else:
                skipped.append(f"  SKIP (conflict, no --conflict-map): {term} (matched: {matched_ids})")
                stats["skipped"] += 1
                continue

        # --- Handle "exists" entries: definition only ---
        if status == "exists" and args.import_all:
            if matched_ids and definition:
                # matched_concept_id may contain multiple IDs separated by |
                primary_id = matched_ids.split("|")[0].strip()
                if primary_id in existing_ids:
                    new_definitions.append(
                        f"{primary_id}\ten\t{definition}\t{args.source}"
                    )
                    stats["def_only"] += 1
            else:
                skipped.append(f"  SKIP (exists, no definition or match): {term}")
                stats["skipped"] += 1
            continue

        # --- Handle "new" or "approved" entries: full import ---
        concept_id = _slugify(term)
        if not concept_id:
            skipped.append(f"  SKIP (empty slug): {term}")
            stats["skipped"] += 1
            continue

        if concept_id in existing_ids:
            # Concept already exists but wasn't caught as "exists" — add definition only
            if definition:
                new_definitions.append(
                    f"{concept_id}\ten\t{definition}\t{args.source}"
                )
                stats["def_only"] += 1
            else:
                skipped.append(f"  SKIP (concept_id exists): {concept_id} ← {term}")
                stats["skipped"] += 1
            continue

        # Check for alias collision
        term_lower = term.lower()
        if term_lower in existing_aliases:
            skipped.append(f"  SKIP (alias exists): {term}")
            stats["skipped"] += 1
            continue

        zh = row.get("zh", "")
        en = term
        abbr = ""

        # concepts.tsv: concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes, source
        concept_line = "\t".join([
            concept_id, args.category, zh, en, abbr,
            "active", "", args.source,
        ])

        # aliases.tsv: alias, concept_id, lang, kind, comment
        alias_line = f"{en}\t{concept_id}\ten\tpreferred\timported from {args.source}"
        alias_lines_extra = []
        if zh:
            alias_lines_extra.append(f"{zh}\t{concept_id}\tzh\tpreferred\timported from {args.source}")

        # evidence.tsv: concept_id, source, quote, added_by, added_at
        evidence_line = f"{concept_id}\t{args.evidence_url}\t\timport_approved_terms\t{today}"

        # definitions.tsv: concept_id, lang, definition, source
        if definition:
            new_definitions.append(f"{concept_id}\ten\t{definition}\t{args.source}")

        new_concepts.append(concept_line)
        new_aliases.append(alias_line)
        new_aliases.extend(alias_lines_extra)
        new_evidence.append(evidence_line)
        existing_ids.add(concept_id)
        existing_aliases.add(term_lower)
        if zh:
            existing_aliases.add(zh.lower())
        stats["new_concept"] += 1

    print("\nResults:")
    print(f"  New concepts:    {stats['new_concept']}")
    print(f"  Definitions:     {len(new_definitions)} (def-only: {stats['def_only']})")
    print(f"  New aliases:     {len(new_aliases)}")
    print(f"  New evidence:    {len(new_evidence)}")
    print(f"  Conflict resolved: {stats['conflict_resolved']}")
    print(f"  Skipped:         {stats['skipped']}")

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
    if new_concepts:
        with open(concepts_path, "a", encoding="utf-8") as f:
            f.write("\n# ---- Imported from " + args.source + f" ({today}) ----\n")
            for line in new_concepts:
                f.write(line + "\n")

    if new_aliases:
        with open(aliases_path, "a", encoding="utf-8") as f:
            f.write("\n# ---- Imported from " + args.source + f" ({today}) ----\n")
            for line in new_aliases:
                f.write(line + "\n")

    if new_evidence:
        with open(evidence_path, "a", encoding="utf-8") as f:
            for line in new_evidence:
                f.write(line + "\n")

    if new_definitions:
        with open(definitions_path, "a", encoding="utf-8") as f:
            f.write("# ---- Imported from " + args.source + f" ({today}) ----\n")
            for line in new_definitions:
                f.write(line + "\n")

    print(f"\nAppended to registry files in {REGISTRY_DIR}")


if __name__ == "__main__":
    main()
