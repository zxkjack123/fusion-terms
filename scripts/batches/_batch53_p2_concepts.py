#!/usr/bin/env python3
"""Batch 53 — P2 new concepts (4) + enrichment aliases for 3 existing concepts.

New concepts:
  occupational-dose, mean-free-path, cyclotron-frequency, magnetic-pressure

Enriches: decay-heat (afterheat), plasma-equilibrium, availability

Of 34 P2 candidates, 27 already existed, 3 merged into existing concepts
(afterheat→decay-heat, mhd-equilibrium→plasma-equilibrium,
plant-availability→availability), leaving 4 truly new concepts.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"


def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


TODAY = "2026-03-23"

# ── NEW CONCEPTS (4) ──────────────────────────────────────────────
concepts: list[tuple] = [
    ("# ==== Batch 53 P2: Safety / licensing ====",),
    (
        "occupational-dose",
        "metric",
        "职业剂量",
        "occupational dose",
        "",
        "active",
        "Radiation dose received by workers in a fusion facility",
    ),
    ("# ==== Batch 53 P2: General plasma physics ====",),
    (
        "mean-free-path",
        "metric",
        "平均自由程",
        "mean free path",
        "",
        "active",
        "Average distance a particle travels between collisions",
    ),
    (
        "cyclotron-frequency",
        "metric",
        "回旋频率",
        "cyclotron frequency",
        "",
        "active",
        "Angular frequency of charged particle gyration around magnetic field line",
    ),
    (
        "magnetic-pressure",
        "concept",
        "磁压",
        "magnetic pressure",
        "",
        "active",
        "Pressure exerted by magnetic field, B²/(2μ₀)",
    ),
]

# ── ALIASES ────────────────────────────────────────────────────────
aliases: list[tuple] = [
    ("# ==== Batch 53 P2: Safety / licensing ====",),
    # occupational-dose
    ("occupational dose", "occupational-dose", "en", "preferred", ""),
    ("职业剂量", "occupational-dose", "zh", "preferred", "preferred zh"),
    (
        "occupational radiation dose",
        "occupational-dose",
        "en",
        "alias",
        "expanded form",
    ),
    ("职业照射剂量", "occupational-dose", "zh", "alias", "照射 form"),
    ("个人剂量", "occupational-dose", "zh", "alias", "personal dose zh"),
    ("# ==== Batch 53 P2: General plasma physics ====",),
    # mean-free-path
    ("mean free path", "mean-free-path", "en", "preferred", ""),
    ("平均自由程", "mean-free-path", "zh", "preferred", "preferred zh"),
    ("MFP", "mean-free-path", "abbr", "alias", "common abbreviation"),
    ("collision mean free path", "mean-free-path", "en", "alias", "collision context"),
    ("碰撞平均自由程", "mean-free-path", "zh", "alias", "collision zh"),
    # cyclotron-frequency
    ("cyclotron frequency", "cyclotron-frequency", "en", "preferred", ""),
    ("回旋频率", "cyclotron-frequency", "zh", "preferred", "preferred zh"),
    ("gyrofrequency", "cyclotron-frequency", "en", "alias", "one-word form"),
    ("Larmor frequency", "cyclotron-frequency", "en", "alias", "Larmor synonym"),
    ("ion cyclotron frequency", "cyclotron-frequency", "en", "alias", "ion species"),
    (
        "electron cyclotron frequency",
        "cyclotron-frequency",
        "en",
        "alias",
        "electron species",
    ),
    ("离子回旋频率", "cyclotron-frequency", "zh", "alias", "ion species zh"),
    ("电子回旋频率", "cyclotron-frequency", "zh", "alias", "electron species zh"),
    ("拉莫尔频率", "cyclotron-frequency", "zh", "alias", "Larmor zh"),
    # magnetic-pressure
    ("magnetic pressure", "magnetic-pressure", "en", "preferred", ""),
    ("磁压", "magnetic-pressure", "zh", "preferred", "preferred zh"),
    ("magnetic stress", "magnetic-pressure", "en", "alias", "stress form"),
    ("磁压力", "magnetic-pressure", "zh", "alias", "expanded zh"),
    ("磁场压力", "magnetic-pressure", "zh", "alias", "field-context zh"),
    ("# ==== Batch 53 P2: Enrichment aliases for existing concepts ====",),
    # decay-heat enrichment (afterheat → decay-heat)
    (
        "afterheat",
        "decay-heat",
        "en",
        "alias",
        "synonym (residual heat after shutdown)",
    ),
    ("residual heat", "decay-heat", "en", "alias", "generic synonym"),
    ("残余发热", "decay-heat", "zh", "alias", "residual form"),
    # plasma-equilibrium enrichment
    (
        "MHD equilibrium reconstruction",
        "plasma-equilibrium",
        "en",
        "alias",
        "reconstruction context",
    ),
    ("磁流体平衡", "plasma-equilibrium", "zh", "alias", "MHD zh form"),
    # availability enrichment
    ("plant availability", "availability", "en", "alias", "plant context"),
    ("装置可用率", "availability", "zh", "alias", "device zh form"),
    ("电站可用率", "availability", "zh", "alias", "power-plant zh form"),
]

# ── EVIDENCE (4 new concepts) ──────────────────────────────────────
evidence: list[tuple] = [
    ("# ==== Batch 53 P2 ====",),
    ("occupational-dose", "internal:safety:occupational-dose", "", "", TODAY),
    ("mean-free-path", "https://en.wikipedia.org/wiki/Mean_free_path", "", "", TODAY),
    (
        "cyclotron-frequency",
        "https://en.wikipedia.org/wiki/Cyclotron_resonance",
        "",
        "",
        TODAY,
    ),
    (
        "magnetic-pressure",
        "https://en.wikipedia.org/wiki/Magnetic_pressure",
        "",
        "",
        TODAY,
    ),
]

if __name__ == "__main__":
    write_tsv_rows(REG / "concepts.tsv", concepts)
    print(
        f"✓ Appended {sum(1 for r in concepts if not r[0].startswith('#'))} concept rows"
    )

    write_tsv_rows(REG / "aliases.tsv", aliases)
    print(
        f"✓ Appended {sum(1 for r in aliases if not r[0].startswith('#'))} alias rows"
    )

    write_tsv_rows(REG / "evidence.tsv", evidence)
    print(
        f"✓ Appended {sum(1 for r in evidence if not r[0].startswith('#'))} evidence rows"
    )

    print("Done — run validate_registry next.")
