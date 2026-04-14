#!/usr/bin/env python3
"""Batch 54: alias enrichment for 33 sparse concepts (≤2 correct aliases).

+38 correct aliases across device / concept / method / organization /
material / metric / system / diagnostic / code categories.
"""

import pathlib

ALIASES_TSV = pathlib.Path("terms/registry/aliases.tsv")

# (text, concept_id, lang, kind, comment)
DATA = [
    ("# ==== batch 54: alias enrichment for sparse concepts ====",),
    # ── device (11 aliases, 9 concepts) ────────────────────────────
    ("低温真空泵", "cryopump", "zh", "alias", ""),
    ("cryogenic pump", "cryopump", "en", "alias", ""),
    ("Experimental Advanced Superconducting Tokamak", "east", "en", "alias", ""),
    ("电子回旋管", "gyrotron", "zh", "alias", ""),
    ("HL-2A tokamak", "hl-2a", "en", "alias", ""),
    ("HL-2M tokamak", "hl-2m", "en", "alias", ""),
    ("国际热核聚变实验堆", "iter", "zh", "alias", ""),
    ("MH bed", "metal-hydride-bed", "en", "alias", "MH = metal hydride"),
    ("负离子束源", "negative-ion-source", "zh", "alias", ""),
    ("OMEGA laser", "omega", "en", "alias", ""),
    ("OMEGA laser facility", "omega", "en", "alias", ""),
    # ── concept (16 aliases, 14 concepts) ──────────────────────────
    ("AC losses", "ac-loss", "en", "alias", "plural form"),
    ("交流功率损耗", "ac-loss", "zh", "alias", ""),
    ("bootstrap current generation", "bootstrap-generation", "en", "alias", ""),
    ("steam condenser", "condenser", "en", "alias", ""),
    ("plasma divertor", "divertor", "en", "alias", ""),
    ("dust production", "dust-generation", "en", "alias", ""),
    ("尘埃产生", "dust-generation", "zh", "alias", ""),
    ("He embrittlement", "helium-embrittlement", "en", "alias", ""),
    ("helium-induced embrittlement", "helium-embrittlement", "en", "alias", ""),
    ("ITER-DEMO transition", "iter-to-demo", "en", "alias", ""),
    ("聚变原型堆", "prototype-reactor", "zh", "alias", ""),
    ("粒子再循环", "recycling", "zh", "alias", ""),
    ("sawtooth collapse", "sawtooth-crash", "en", "alias", ""),
    ("collisionless Boltzmann equation", "vlasov-equation", "en", "alias", ""),
    ("boronisation", "boronization", "en", "alias", "British spelling"),
    ("siliconisation", "siliconization", "en", "alias", "British spelling"),
    # ── method / concept replacement aliases (5 aliases, 5 concepts) ──
    ("functional materials", "functional-material", "en", "alias", "plural"),
    ("planned maintenance", "scheduled-maintenance", "en", "alias", ""),
    ("氚清除", "tritium-removal", "zh", "alias", ""),
    # ── organization (1 alias, 1 concept) ──────────────────────────
    ("Tri Alpha Energy", "tae-technologies", "en", "alias", "former company name"),
    # ── material (2 aliases, 2 concepts) ───────────────────────────
    ("CLF-1 steel", "clf-1", "en", "alias", ""),
    ("F82H steel", "f82h", "en", "alias", ""),
    # ── metric (1 alias, 1 concept) ────────────────────────────────
    ("产气率", "gas-production-rate", "zh", "alias", ""),
    # ── system (1 alias, 1 concept) ────────────────────────────────
    ("检修口", "maintenance-port", "zh", "alias", ""),
    # ── diagnostic (1 alias, 1 concept) ────────────────────────────
    ("flux loop", "magnetic-flux-loop", "en", "alias", ""),
    # ── code (2 aliases, 2 concepts) ───────────────────────────────
    ("COMSOL Multiphysics", "comsol", "en", "alias", "full product name"),
    ("JET Integrated Transport Code", "jintrac", "en", "alias", "full name"),
]


def write_tsv_rows(path: pathlib.Path, rows: list[tuple]) -> int:
    """Append tab-joined rows, return count of data rows written."""
    n = 0
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:  # comment-only row
                f.write(row[0] + "\n")
            else:
                f.write("\t".join(row) + "\n")
                n += 1
    return n


if __name__ == "__main__":
    n = write_tsv_rows(ALIASES_TSV, DATA)
    concepts = {r[1] for r in DATA if len(r) > 1}
    print(f"Wrote {n} aliases for {len(concepts)} concepts")
