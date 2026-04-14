#!/usr/bin/env python3
"""Compare a terminology source TSV against the existing registry aliases.

Reads a staging TSV (with at least a ``term`` column) and the registry
``aliases.tsv``, then outputs a diff report indicating which terms are
new, already exist, or conflict with existing entries.

Usage:
    python3 scripts/diff_terminology_source.py \
        --source artifacts/terminology_sources/iter_glossary_raw.tsv \
        --output artifacts/terminology_sources/iter_glossary_diff.tsv

The input TSV must have a header line (comment ``#`` prefix allowed).
The first column is treated as the term name.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _load_registry_aliases(aliases_path: Path) -> dict[str, list[dict[str, str]]]:
    """Load aliases.tsv into a dict keyed by normalized alias text.

    Returns {normalized_alias: [{concept_id, lang, kind, original_alias}, ...]}.
    """
    lookup: dict[str, list[dict[str, str]]] = {}
    for line in aliases_path.read_text("utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        if len(parts) < 4:
            continue
        alias, concept_id, lang, kind = parts[0], parts[1], parts[2], parts[3]
        key = alias.lower().strip()
        lookup.setdefault(key, []).append(
            {
                "concept_id": concept_id,
                "lang": lang,
                "kind": kind,
                "original_alias": alias,
            }
        )
    return lookup


def _load_source_terms(source_path: Path) -> list[dict[str, str]]:
    """Load a staging TSV.  First column = term, rest preserved as-is."""
    rows: list[dict[str, str]] = []
    lines = source_path.read_text("utf-8").splitlines()
    header_cols: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            # Parse header for column names
            stripped = line.lstrip("# ").strip()
            header_cols = [c.strip() for c in stripped.split("\t")]
            continue
        parts = [c.strip() for c in line.split("\t")]
        row: dict[str, str] = {}
        for i, val in enumerate(parts):
            col_name = header_cols[i] if i < len(header_cols) else f"col{i}"
            row[col_name] = val
        if "term" not in row and parts:
            row["term"] = parts[0]
        rows.append(row)
    return rows


def diff_terms(
    source_terms: list[dict[str, str]],
    alias_lookup: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    """Compare source terms against registry, return diff rows."""
    results: list[dict[str, str]] = []
    for st in source_terms:
        term = st.get("term", "")
        if not term:
            continue
        key = term.lower().strip()

        matches = alias_lookup.get(key, [])
        if not matches:
            # Also try without trailing parenthetical, e.g. "Aspect ratio (plasma)" -> "aspect ratio"
            simplified = key.split("(")[0].strip()
            if simplified != key:
                matches = alias_lookup.get(simplified, [])

        if matches:
            concept_ids = sorted(set(m["concept_id"] for m in matches))
            status = "exists"
            matched_id = concept_ids[0]
            if len(concept_ids) > 1:
                status = "conflict"
                matched_id = "|".join(concept_ids)
        else:
            status = "new"
            matched_id = ""

        result = {
            "term": term,
            "status": status,
            "matched_concept_id": matched_id,
        }
        # Carry through any extra columns from source
        for k, v in st.items():
            if k != "term" and k not in result:
                result[k] = v
        results.append(result)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the staging terminology TSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output diff TSV path (default: derive from source name)",
    )
    parser.add_argument(
        "--aliases",
        type=Path,
        default=Path("terms/registry/aliases.tsv"),
        help="Path to registry aliases.tsv",
    )
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: source file not found: {args.source}", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        stem = args.source.stem.replace("_raw", "_diff")
        args.output = args.source.parent / f"{stem}.tsv"

    alias_lookup = _load_registry_aliases(args.aliases)
    source_terms = _load_source_terms(args.source)

    if not source_terms:
        print("ERROR: no terms found in source file", file=sys.stderr)
        sys.exit(1)

    results = diff_terms(source_terms, alias_lookup)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    extra_cols = []
    for r in results:
        for k in r:
            if k not in ("term", "status", "matched_concept_id") and k not in extra_cols:
                extra_cols.append(k)

    with open(args.output, "w", encoding="utf-8") as f:
        cols = ["term", "status", "matched_concept_id"] + extra_cols
        f.write("# " + "\t".join(cols) + "\n")
        for r in results:
            vals = [r.get(c, "") for c in cols]
            f.write("\t".join(vals) + "\n")

    # Statistics
    counts = {"new": 0, "exists": 0, "conflict": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"Diff report: {args.output}")
    print(f"  Total: {len(results)}")
    for status, count in sorted(counts.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
