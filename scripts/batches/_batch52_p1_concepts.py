#!/usr/bin/env python3
"""Batch 52 — P1 new concepts (8) + enrichment aliases for 5 existing concepts.

Subdomains:
  Heating / current drive   (2 new)
  Diagnostics               (3 new)
  Materials / PMI           (3 new)

Also enriches: interferometry, reflectometry, far-infrared-polarimetry,
               plasma-control, plasma-surface-interaction
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"


def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


TODAY = "2026-03-23"

# ── NEW CONCEPTS (8) ──────────────────────────────────────────────
concepts: list[tuple] = [
    ("# ==== Batch 52 P1: Heating / current drive ====",),
    (
        "helicon-wave",
        "concept",
        "螺旋波",
        "helicon wave",
        "",
        "active",
        "Bounded whistler wave used for plasma heating and current drive",
    ),
    (
        "wave-plasma-interaction",
        "concept",
        "波等离子体相互作用",
        "wave-plasma interaction",
        "",
        "active",
        "Coupling and energy transfer between electromagnetic waves and plasma",
    ),
    ("# ==== Batch 52 P1: Diagnostics ====",),
    (
        "hard-x-ray",
        "diagnostic",
        "硬X射线",
        "hard X-ray",
        "HXR",
        "active",
        "High-energy X-ray diagnostic for runaway electrons and fast ions",
    ),
    (
        "magnetic-probe",
        "diagnostic",
        "磁探针",
        "magnetic probe",
        "",
        "active",
        "Inductive sensor for local magnetic field fluctuation measurement",
    ),
    (
        "faraday-rotation",
        "concept",
        "法拉第旋转",
        "Faraday rotation",
        "",
        "active",
        "Rotation of polarization plane by magnetized plasma, used in polarimetry",
    ),
    ("# ==== Batch 52 P1: Materials / PMI ====",),
    (
        "material-migration",
        "concept",
        "材料迁移",
        "material migration",
        "",
        "active",
        "Net erosion-transport-redeposition of wall material inside the vessel",
    ),
    (
        "radiation-damage",
        "concept",
        "辐照损伤",
        "radiation damage",
        "",
        "active",
        "Lattice defects and property degradation from neutron/ion irradiation",
    ),
    (
        "embrittlement",
        "concept",
        "脆化",
        "embrittlement",
        "",
        "active",
        "Loss of ductility in structural materials (irradiation, helium, hydrogen)",
    ),
]

# ── ALIASES (for 8 new concepts + enrichment) ─────────────────────
aliases: list[tuple] = [
    ("# ==== Batch 52 P1: Heating / current drive ====",),
    # helicon-wave
    ("helicon wave", "helicon-wave", "en", "preferred", ""),
    ("螺旋波", "helicon-wave", "zh", "preferred", "preferred zh"),
    ("helicon", "helicon-wave", "en", "alias", "short form"),
    ("helicon-wave", "helicon-wave", "en", "alias", "hyphenated form"),
    ("螺旋波加热", "helicon-wave", "zh", "alias", "heating context"),
    ("helicon wave heating", "helicon-wave", "en", "alias", "heating context"),
    # wave-plasma-interaction
    ("wave-plasma interaction", "wave-plasma-interaction", "en", "preferred", ""),
    (
        "波等离子体相互作用",
        "wave-plasma-interaction",
        "zh",
        "preferred",
        "preferred zh",
    ),
    ("wave-plasma coupling", "wave-plasma-interaction", "en", "alias", "coupling form"),
    (
        "wave plasma interaction",
        "wave-plasma-interaction",
        "en",
        "alias",
        "no-hyphen form",
    ),
    ("波与等离子体相互作用", "wave-plasma-interaction", "zh", "alias", "expanded zh"),
    ("# ==== Batch 52 P1: Diagnostics ====",),
    # hard-x-ray
    ("hard X-ray", "hard-x-ray", "en", "preferred", ""),
    ("硬X射线", "hard-x-ray", "zh", "preferred", "preferred zh"),
    ("HXR", "hard-x-ray", "abbr", "preferred", "canonical abbr"),
    ("hard x-ray diagnostic", "hard-x-ray", "en", "alias", "diagnostic form"),
    ("hard X-ray emission", "hard-x-ray", "en", "alias", "emission form"),
    ("硬X射线诊断", "hard-x-ray", "zh", "alias", "diagnostic zh"),
    # magnetic-probe
    ("magnetic probe", "magnetic-probe", "en", "preferred", ""),
    ("磁探针", "magnetic-probe", "zh", "preferred", "preferred zh"),
    ("magnetic pickup coil", "magnetic-probe", "en", "alias", "coil form"),
    ("B-dot probe", "magnetic-probe", "en", "alias", "Bdot variant"),
    ("磁感应探针", "magnetic-probe", "zh", "alias", "inductive form"),
    # faraday-rotation
    ("Faraday rotation", "faraday-rotation", "en", "preferred", ""),
    ("法拉第旋转", "faraday-rotation", "zh", "preferred", "preferred zh"),
    ("Faraday effect", "faraday-rotation", "en", "alias", "effect form"),
    ("法拉第效应", "faraday-rotation", "zh", "alias", "effect zh form"),
    ("# ==== Batch 52 P1: Materials / PMI ====",),
    # material-migration
    ("material migration", "material-migration", "en", "preferred", ""),
    ("材料迁移", "material-migration", "zh", "preferred", "preferred zh"),
    ("wall material migration", "material-migration", "en", "alias", "wall context"),
    ("材料输运", "material-migration", "zh", "alias", "transport perspective"),
    ("壁材料迁移", "material-migration", "zh", "alias", "wall context zh"),
    # radiation-damage
    ("radiation damage", "radiation-damage", "en", "preferred", ""),
    ("辐照损伤", "radiation-damage", "zh", "preferred", "preferred zh"),
    ("neutron damage", "radiation-damage", "en", "alias", "neutron-specific"),
    ("辐射损伤", "radiation-damage", "zh", "alias", "variant zh (辐射 vs 辐照)"),
    ("辐照缺陷", "radiation-damage", "zh", "alias", "defect perspective"),
    # embrittlement
    ("embrittlement", "embrittlement", "en", "preferred", ""),
    ("脆化", "embrittlement", "zh", "preferred", "preferred zh"),
    ("material embrittlement", "embrittlement", "en", "alias", "material context"),
    ("# ==== Batch 52 P1: Enrichment aliases for existing concepts ====",),
    # interferometry enrichment
    ("interferometer", "interferometry", "en", "alias", "instrument form"),
    ("plasma interferometer", "interferometry", "en", "alias", "plasma context"),
    ("laser interferometer", "interferometry", "en", "alias", "laser form"),
    ("激光干涉仪", "interferometry", "zh", "alias", "laser zh"),
    # reflectometry enrichment
    ("reflectometer", "reflectometry", "en", "alias", "instrument form"),
    ("microwave reflectometer", "reflectometry", "en", "alias", "microwave form"),
    ("plasma reflectometry", "reflectometry", "en", "alias", "plasma context"),
    # far-infrared-polarimetry enrichment
    ("polarimetry", "far-infrared-polarimetry", "en", "alias", "generic polarimetry"),
    ("偏振测量", "far-infrared-polarimetry", "zh", "alias", "measurement form"),
    # plasma-control enrichment
    ("plasma control system", "plasma-control", "en", "alias", "system form"),
    ("等离子体控制系统", "plasma-control", "zh", "alias", "system zh form"),
    # plasma-surface-interaction enrichment
    (
        "等离子体材料相互作用",
        "plasma-surface-interaction",
        "zh",
        "alias",
        "material form zh",
    ),
    (
        "plasma material interaction",
        "plasma-surface-interaction",
        "en",
        "alias",
        "material form en",
    ),
]

# ── EVIDENCE (8 new concepts) ──────────────────────────────────────
evidence: list[tuple] = [
    ("# ==== Batch 52 P1 ====",),
    ("helicon-wave", "internal:heating:helicon-wave", "", "", TODAY),
    (
        "wave-plasma-interaction",
        "internal:heating:wave-plasma-interaction",
        "",
        "",
        TODAY,
    ),
    ("hard-x-ray", "internal:diagnostics:hard-x-ray", "", "", TODAY),
    ("magnetic-probe", "internal:diagnostics:magnetic-probe", "", "", TODAY),
    ("faraday-rotation", "internal:diagnostics:faraday-rotation", "", "", TODAY),
    ("material-migration", "internal:pmi:material-migration", "", "", TODAY),
    ("radiation-damage", "internal:pmi:radiation-damage", "", "", TODAY),
    ("embrittlement", "internal:pmi:embrittlement", "", "", TODAY),
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
