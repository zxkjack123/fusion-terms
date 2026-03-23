#!/usr/bin/env python3
"""Append Batch 48-49 terms + supplementary aliases to the registry."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

CONCEPTS = [
    # Batch 48: Core PWI Processes
    ("# ==== Batch 48: Core Plasma-Wall Interaction Processes ====",),
    ("presheath", "concept", "预鞘", "presheath", "", "active", "Ion acceleration transition region ahead of the Debye sheath"),
    ("co-deposition", "concept", "共沉积", "co-deposition", "", "active", "Simultaneous deposition of eroded material with hydrogen isotopes"),
    ("impurity-source", "concept", "杂质源", "impurity source", "", "active", "Impurity production yield and spatial distribution at the wall"),
    ("impurity-influx", "metric", "杂质流入", "impurity influx", "", "active", "Impurity flux entering plasma from wall surfaces"),
    ("fuel-recycling", "concept", "燃料再循环", "fuel recycling", "", "active", "Hydrogen isotope adsorption-release cycle at the wall"),
    ("wall-pumping", "concept", "壁抽气效应", "wall pumping", "", "active", "Wall hydrogen absorption causing plasma density decrease"),
    ("deposition", "concept", "沉积", "deposition", "", "active", "Material deposition process on wall surfaces"),
    ("graphite", "material", "石墨", "graphite", "", "active", "Legacy carbon-based PFC material"),
    ("surface-roughening", "concept", "表面粗糙化", "surface roughening", "", "active", "Wall surface morphology roughening from plasma exposure"),
    ("cracking", "concept", "裂纹", "cracking", "", "active", "PFC surface cracking from thermal cycling or shock"),
    # Batch 49: Wall Damage, Transient Loads & Dust
    ("# ==== Batch 49: Wall Damage, Transient Loads & Dust ====",),
    ("thermal-shock", "concept", "热冲击", "thermal shock", "", "active", "Single-pulse high heat flux damage to PFC"),
    ("disruption-erosion", "concept", "破裂侵蚀", "disruption erosion", "", "active", "Severe wall erosion during plasma disruption events"),
    ("elm-induced-erosion", "concept", "ELM诱发侵蚀", "ELM-induced erosion", "", "active", "Wall erosion caused by ELM transient heat loads"),
    ("runaway-electron-damage", "concept", "逃逸电子损伤", "runaway electron damage", "", "active", "Deep localized PFC damage from runaway electron impact"),
    ("prompt-redeposition", "concept", "即时再沉积", "prompt redeposition", "", "active", "Sputtered particle near-field redeposition under magnetic confinement"),
    ("lithium-coating", "method", "锂涂覆", "lithium coating", "", "active", "Lithium evaporation/injection wall conditioning technique"),
    ("siliconization", "method", "硅化", "siliconization", "", "active", "Silane glow discharge wall conditioning technique"),
    ("dust-generation", "concept", "粉尘产生", "dust generation", "", "active", "Dust production mechanism from plasma erosion and flaking"),
    ("dust-transport", "concept", "粉尘输运", "dust transport", "", "active", "Dust dynamics, mobilization and transport inside vacuum vessel"),
    ("dust-inventory", "metric", "粉尘存量", "dust inventory", "", "active", "Total mobilizable dust quantity inside vacuum vessel"),
]

ALIASES = [
    # Batch 48: Core PWI Processes
    ("# ==== Batch 48: Core Plasma-Wall Interaction Processes ====",),
    ("presheath", "presheath", "en", "preferred", ""),
    ("预鞘", "presheath", "zh", "preferred", ""),
    ("co-deposition", "co-deposition", "en", "preferred", ""),
    ("共沉积", "co-deposition", "zh", "preferred", ""),
    ("codeposition", "co-deposition", "en", "alias", ""),
    ("impurity source", "impurity-source", "en", "preferred", ""),
    ("杂质源", "impurity-source", "zh", "preferred", ""),
    ("impurity influx", "impurity-influx", "en", "preferred", ""),
    ("杂质流入", "impurity-influx", "zh", "preferred", ""),
    ("fuel recycling", "fuel-recycling", "en", "preferred", ""),
    ("燃料再循环", "fuel-recycling", "zh", "preferred", ""),
    ("particle recycling", "fuel-recycling", "en", "alias", ""),
    ("wall pumping", "wall-pumping", "en", "preferred", ""),
    ("壁抽气效应", "wall-pumping", "zh", "preferred", ""),
    ("壁抽气", "wall-pumping", "zh", "alias", ""),
    ("deposition", "deposition", "en", "preferred", ""),
    ("沉积", "deposition", "zh", "preferred", ""),
    ("graphite", "graphite", "en", "preferred", ""),
    ("石墨", "graphite", "zh", "preferred", ""),
    ("surface roughening", "surface-roughening", "en", "preferred", ""),
    ("表面粗糙化", "surface-roughening", "zh", "preferred", ""),
    ("cracking", "cracking", "en", "preferred", ""),
    ("裂纹", "cracking", "zh", "preferred", ""),
    ("thermal cracking", "cracking", "en", "alias", ""),
    # Batch 49: Wall Damage, Transient Loads & Dust
    ("# ==== Batch 49: Wall Damage, Transient Loads & Dust ====",),
    ("thermal shock", "thermal-shock", "en", "preferred", ""),
    ("热冲击", "thermal-shock", "zh", "preferred", ""),
    ("disruption erosion", "disruption-erosion", "en", "preferred", ""),
    ("破裂侵蚀", "disruption-erosion", "zh", "preferred", ""),
    ("ELM-induced erosion", "elm-induced-erosion", "en", "preferred", ""),
    ("ELM诱发侵蚀", "elm-induced-erosion", "zh", "preferred", ""),
    ("runaway electron damage", "runaway-electron-damage", "en", "preferred", ""),
    ("逃逸电子损伤", "runaway-electron-damage", "zh", "preferred", ""),
    ("RE damage", "runaway-electron-damage", "en", "alias", ""),
    ("prompt redeposition", "prompt-redeposition", "en", "preferred", ""),
    ("即时再沉积", "prompt-redeposition", "zh", "preferred", ""),
    ("lithium coating", "lithium-coating", "en", "preferred", ""),
    ("锂涂覆", "lithium-coating", "zh", "preferred", ""),
    ("Li coating", "lithium-coating", "en", "alias", ""),
    ("锂蒸镀", "lithium-coating", "zh", "alias", ""),
    ("siliconization", "siliconization", "en", "preferred", ""),
    ("硅化", "siliconization", "zh", "preferred", ""),
    ("dust generation", "dust-generation", "en", "preferred", ""),
    ("粉尘产生", "dust-generation", "zh", "preferred", ""),
    ("dust transport", "dust-transport", "en", "preferred", ""),
    ("粉尘输运", "dust-transport", "zh", "preferred", ""),
    ("dust inventory", "dust-inventory", "en", "preferred", ""),
    ("粉尘存量", "dust-inventory", "zh", "preferred", ""),
    ("dust limit", "dust-inventory", "en", "alias", ""),
    # Supplementary aliases for existing plasma-surface-interaction
    ("# ==== Supplementary aliases for plasma-surface-interaction ====",),
    ("PWI", "plasma-surface-interaction", "abbr", "alias", ""),
    ("plasma-wall interaction", "plasma-surface-interaction", "en", "alias", ""),
    ("等离子体壁相互作用", "plasma-surface-interaction", "zh", "alias", ""),
]

EVIDENCE = [
    ("presheath", "internal:expansion:batch-48", "Ion acceleration ahead of sheath", "copilot", "2026-03-21"),
    ("co-deposition", "internal:expansion:batch-48", "Eroded material + H co-deposition", "copilot", "2026-03-21"),
    ("impurity-source", "internal:expansion:batch-48", "Wall impurity production", "copilot", "2026-03-21"),
    ("impurity-influx", "internal:expansion:batch-48", "Impurity flux into plasma", "copilot", "2026-03-21"),
    ("fuel-recycling", "internal:expansion:batch-48", "H isotope wall recycling", "copilot", "2026-03-21"),
    ("wall-pumping", "internal:expansion:batch-48", "Wall H absorption effect", "copilot", "2026-03-21"),
    ("deposition", "internal:expansion:batch-48", "Material wall deposition", "copilot", "2026-03-21"),
    ("graphite", "internal:expansion:batch-48", "Legacy C PFC material", "copilot", "2026-03-21"),
    ("surface-roughening", "internal:expansion:batch-48", "Plasma exposure roughening", "copilot", "2026-03-21"),
    ("cracking", "internal:expansion:batch-48", "PFC surface cracking", "copilot", "2026-03-21"),
    ("thermal-shock", "internal:expansion:batch-49", "Single-pulse HHF damage", "copilot", "2026-03-21"),
    ("disruption-erosion", "internal:expansion:batch-49", "Disruption wall erosion", "copilot", "2026-03-21"),
    ("elm-induced-erosion", "internal:expansion:batch-49", "ELM transient erosion", "copilot", "2026-03-21"),
    ("runaway-electron-damage", "internal:expansion:batch-49", "RE impact PFC damage", "copilot", "2026-03-21"),
    ("prompt-redeposition", "internal:expansion:batch-49", "Near-field redeposition", "copilot", "2026-03-21"),
    ("lithium-coating", "internal:expansion:batch-49", "Li wall conditioning", "copilot", "2026-03-21"),
    ("siliconization", "internal:expansion:batch-49", "Silane GDC conditioning", "copilot", "2026-03-21"),
    ("dust-generation", "internal:expansion:batch-49", "Erosion dust production", "copilot", "2026-03-21"),
    ("dust-transport", "internal:expansion:batch-49", "In-vessel dust dynamics", "copilot", "2026-03-21"),
    ("dust-inventory", "internal:expansion:batch-49", "Mobilizable dust quantity", "copilot", "2026-03-21"),
]


def write_tsv_rows(path, rows):
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:
                f.write(row[0] + "\n")
            else:
                f.write(T.join(row) + "\n")


if __name__ == "__main__":
    write_tsv_rows(REG / "concepts.tsv", CONCEPTS)
    n_c = sum(1 for r in CONCEPTS if len(r) > 1)
    print(f"Appended {n_c} concepts")

    write_tsv_rows(REG / "aliases.tsv", ALIASES)
    n_a = sum(1 for r in ALIASES if len(r) > 1)
    print(f"Appended {n_a} aliases")

    write_tsv_rows(REG / "evidence.tsv", EVIDENCE)
    print(f"Appended {len(EVIDENCE)} evidence rows")
