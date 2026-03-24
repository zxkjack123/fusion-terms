#!/usr/bin/env python3
"""Cleanup: remove duplicate concepts, redirect aliases, deduplicate rows."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONCEPTS_TSV = ROOT / "terms" / "registry" / "concepts.tsv"
ALIASES_TSV  = ROOT / "terms" / "registry" / "aliases.tsv"
EVIDENCE_TSV = ROOT / "terms" / "registry" / "evidence.tsv"

# ── 1. Concepts to REMOVE (duplicates of existing) ──
# new_concept_id → existing_concept_id they duplicate
REMOVE_CONCEPTS = {
    "sawtooth-instability":   "sawtooth",
    "detachment":             "plasma-detachment",
    "sheath":                 "debye-sheath",
    "triple-product":         "fusion-triple-product",
    "energy-confinement-time":"tau-e",
}

# ── 2. Aliases to DROP from kept concepts (cross-concept conflicts) ──
DROP_ALIASES = {
    # (text, concept_id) pairs to remove
    ("Spitzer resistivity", "plasma-resistivity"),
    ("斯皮策电阻率",         "plasma-resistivity"),
    ("non-inductive current drive", "current-drive"),
    ("非感应电流驱动",       "current-drive"),
}

# ── 3. Additional aliases to ADD to existing concepts (from removed redirects) ──
# These are the NEW aliases from the removed concepts that should go to the
# existing target concept, but ONLY if they don't already exist there.
REDIRECT_ADD = [
    # sawtooth-instability → sawtooth
    ("锯齿不稳定性",     "sawtooth",              "zh",  "alias", "instability form"),
    ("sawtooth instability","sawtooth",            "en",  "alias", "instability form"),
    # detachment → plasma-detachment
    ("脱靶",             "plasma-detachment",      "zh",  "alias", "short form"),
    ("detachment",       "plasma-detachment",      "en",  "alias", "short form"),
    ("偏滤器脱靶",       "plasma-detachment",      "zh",  "alias", "divertor context"),
    ("高再循环",         "high-recycling",         "zh",  "preferred", ""),  # this stays, no conflict
    # sheath → debye-sheath
    ("鞘层",             "debye-sheath",           "zh",  "alias", "short form"),
    ("sheath",           "debye-sheath",           "en",  "alias", "short form"),
    # triple-product → fusion-triple-product
    ("三重积",           "fusion-triple-product",  "zh",  "alias", "short form"),
    ("triple product",   "fusion-triple-product",  "en",  "alias", "short form"),
    ("nTτ",              "fusion-triple-product",  "en",  "alias", "formula notation"),
    # energy-confinement-time → tau-e
    ("能量约束时间",     "tau-e",                  "zh",  "alias", "full name"),
    ("energy confinement time","tau-e",            "en",  "alias", "full name"),
    ("能量约束时间τE",   "tau-e",                  "zh",  "alias", "with symbol"),
]


def process_concepts():
    """Remove duplicate concept rows, return removed IDs."""
    lines = CONCEPTS_TSV.read_text("utf-8").splitlines(keepends=True)
    out = []
    removed = 0
    for line in lines:
        if line.startswith("#") or not line.strip():
            out.append(line)
            continue
        cid = line.split("\t")[0]
        if cid in REMOVE_CONCEPTS:
            removed += 1
            continue  # skip this row
        out.append(line)
    CONCEPTS_TSV.write_text("".join(out), "utf-8")
    print(f"concepts.tsv: removed {removed} duplicate concepts")


def process_aliases():
    """Redirect aliases, drop conflicts, deduplicate."""
    lines = ALIASES_TSV.read_text("utf-8").splitlines(keepends=True)
    out = []
    seen = set()  # (text_lower, concept_id) for dedup
    redirected = 0
    dropped = 0
    deduped = 0

    for line in lines:
        if line.startswith("#") or not line.strip():
            out.append(line)
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            out.append(line)
            continue

        text, cid = parts[0], parts[1]

        # Drop specific conflict aliases
        if (text, cid) in DROP_ALIASES:
            dropped += 1
            continue

        # Redirect aliases from removed concepts to existing
        if cid in REMOVE_CONCEPTS:
            new_cid = REMOVE_CONCEPTS[cid]
            parts[1] = new_cid
            cid = new_cid
            redirected += 1
            line = "\t".join(parts) + "\n"

        # Deduplicate (keep first occurrence)
        key = (text.lower(), cid)
        if key in seen:
            deduped += 1
            continue
        seen.add(key)

        out.append(line)

    # Now add the redirect aliases
    added = 0
    for row in REDIRECT_ADD:
        key = (row[0].lower(), row[1])
        if key not in seen:
            out.append("\t".join(row) + "\n")
            seen.add(key)
            added += 1

    ALIASES_TSV.write_text("".join(out), "utf-8")
    print(f"aliases.tsv: redirected {redirected}, dropped {dropped}, deduped {deduped}, added {added} redirect aliases")


def process_evidence():
    """Remove evidence rows for removed concepts."""
    lines = EVIDENCE_TSV.read_text("utf-8").splitlines(keepends=True)
    out = []
    removed = 0
    for line in lines:
        if line.startswith("#") or not line.strip():
            out.append(line)
            continue
        cid = line.split("\t")[0]
        if cid in REMOVE_CONCEPTS:
            removed += 1
            continue
        out.append(line)
    EVIDENCE_TSV.write_text("".join(out), "utf-8")
    print(f"evidence.tsv: removed {removed} evidence rows")


def main():
    print("=== Cleanup: fixing duplicates and conflicts ===")
    process_concepts()
    process_aliases()
    process_evidence()

    # Verify counts
    import subprocess
    r = subprocess.run(
        ["grep", "-c", "^[^#]", str(CONCEPTS_TSV), str(ALIASES_TSV), str(EVIDENCE_TSV)],
        capture_output=True, text=True
    )
    print(f"\n{r.stdout.strip()}")


if __name__ == "__main__":
    main()
