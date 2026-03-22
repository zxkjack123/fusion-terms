#!/usr/bin/env python3
"""Batch 50: Add 25 new concepts + alias enrichment for ~20 existing concepts."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONCEPTS_TSV = ROOT / "terms" / "registry" / "concepts.tsv"
ALIASES_TSV  = ROOT / "terms" / "registry" / "aliases.tsv"
EVIDENCE_TSV = ROOT / "terms" / "registry" / "evidence.tsv"
DATE = "2026-03-22"
BATCH = "batch-50"
AUTHOR = "copilot"

def write_tsv_rows(path: pathlib.Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:          # comment row
                f.write(row[0] + "\n")
            else:
                f.write("\t".join(row) + "\n")


# ──────────────────────────────────────────────────────
#  Part 1: 25 new concepts
# ──────────────────────────────────────────────────────
NEW_CONCEPTS = [
    # (concept_id, category, preferred_zh, preferred_en, preferred_abbr, status, notes)
    # -- plasma physics fundamentals --
    ("debye-shielding",           "concept",    "德拜屏蔽",          "Debye shielding",     "",     "active", "Debye shielding / screening of electric charges in plasma"),
    ("plasma-resistivity",        "concept",    "等离子体电阻率",    "plasma resistivity",  "",     "active", "Spitzer or anomalous resistivity of plasma"),
    ("flux-coordinate",           "concept",    "磁通坐标",          "flux coordinate",     "",     "active", "Coordinate system based on magnetic flux surfaces"),
    ("field-line-tracing",        "method",     "磁力线追踪",        "field-line tracing",  "",     "active", "Numerical tracing of magnetic field lines"),
    ("sawtooth-instability",      "concept",    "锯齿不稳定性",      "sawtooth instability","",     "active", "Periodic core relaxation event (m=1, n=1 internal kink)"),
    ("current-drive",             "concept",    "电流驱动",          "current drive",       "CD",   "active", "Non-inductive methods for driving plasma current"),
    ("triple-product",            "metric",     "三重积",            "triple product",      "",     "active", "nTτ_E figure of merit for fusion plasmas"),
    # -- heating / current drive --
    ("lower-hybrid-heating",      "method",     "低杂波加热",        "lower hybrid heating","LHH",  "active", "Heating via lower hybrid waves"),
    ("neutral-beam-current-drive","method",     "中性束电流驱动",    "neutral beam current drive","NBCD","active","Current drive via neutral beam injection"),
    # -- confinement --
    ("energy-confinement-time",   "metric",     "能量约束时间",      "energy confinement time","",  "active", "Time scale for plasma energy loss"),
    ("ignition-condition",        "concept",    "点火条件",          "ignition condition",   "",    "active", "Condition for self-sustained fusion burn"),
    # -- divertor/SOL --
    ("detachment",                "concept",    "脱靶",              "detachment",           "",    "active", "Plasma detachment from divertor target"),
    ("high-recycling",            "concept",    "高再循环",          "high recycling",       "",    "active", "High recycling regime in SOL/divertor"),
    ("sheath",                    "concept",    "鞘层",              "sheath",               "",    "active", "Plasma boundary sheath at material surfaces"),
    # -- blanket --
    ("ceramic-breeder",           "material",   "陶瓷增殖剂",        "ceramic breeder",     "",    "active", "Ceramic lithium compound for tritium breeding (Li4SiO4, Li2TiO3)"),
    ("wcll",                      "system",     "水冷锂铅包层",      "water-cooled lithium-lead","WCLL","active","EU water-cooled lithium-lead blanket concept"),
    # -- safety --
    ("loss-of-vacuum-accident",   "concept",    "失真空事故",        "loss of vacuum accident","LOVA","active","Design basis accident: loss of vacuum boundary integrity"),
    # -- neutronics --
    ("neutron-activation",        "concept",    "中子活化",          "neutron activation",   "",    "active", "Activation of materials by neutron irradiation"),
    ("neutron-camera",            "diagnostic", "中子照相机",        "neutron camera",       "",    "active", "Spatially-resolved neutron emission diagnostic"),
    # -- stellarator --
    ("helias",                    "device",     "HELIAS",            "HELIAS",               "",    "active", "Helical-axis advanced stellarator concept"),
    ("quasi-symmetric-stellarator","concept",   "准对称仿星器",      "quasi-symmetric stellarator","QSS","active","Stellarator with quasi-symmetry in |B|"),
    # -- power plant --
    ("coolant-loop",              "system",     "冷却回路",          "coolant loop",         "",    "active", "Primary/secondary coolant circulation loop"),
    ("power-conversion-system",   "system",     "能量转换系统",      "power conversion system","PCS","active","Heat-to-electricity conversion system"),
    ("maintenance-period",        "metric",     "维护周期",          "maintenance period",   "",    "active", "Scheduled maintenance interval for fusion plant"),
    # -- simulation --
    ("gyrokinetic-simulation",    "method",     "回旋动理学模拟",    "gyrokinetic simulation","",   "active", "First-principles simulation of plasma micro-turbulence"),
]

# ──────────────────────────────────────────────────────
#  Part 2: Aliases for new concepts
# ──────────────────────────────────────────────────────
NEW_ALIASES = [
    # (text, concept_id, lang, kind, comment)
    ("# ==== Batch 50: new concepts — plasma physics ====",),

    # debye-shielding
    ("德拜屏蔽",         "debye-shielding",      "zh",  "preferred", ""),
    ("Debye shielding",  "debye-shielding",      "en",  "preferred", ""),
    ("Debye screening",  "debye-shielding",      "en",  "alias",     "synonym"),
    ("德拜屏蔽效应",     "debye-shielding",      "zh",  "alias",     "full form"),

    # plasma-resistivity
    ("等离子体电阻率",   "plasma-resistivity",   "zh",  "preferred", ""),
    ("plasma resistivity","plasma-resistivity",  "en",  "preferred", ""),
    ("Spitzer resistivity","plasma-resistivity", "en",  "alias",     "classical form"),
    ("斯皮策电阻率",     "plasma-resistivity",   "zh",  "alias",     "classical form"),
    ("等离子体电阻",     "plasma-resistivity",   "zh",  "alias",     "short form"),

    # flux-coordinate
    ("磁通坐标",         "flux-coordinate",      "zh",  "preferred", ""),
    ("flux coordinate",  "flux-coordinate",      "en",  "preferred", ""),
    ("flux coordinates", "flux-coordinate",      "en",  "alias",     "plural"),
    ("磁通量坐标",       "flux-coordinate",      "zh",  "alias",     "full form"),

    # field-line-tracing
    ("磁力线追踪",       "field-line-tracing",   "zh",  "preferred", ""),
    ("field-line tracing","field-line-tracing",  "en",  "preferred", ""),
    ("field line tracing","field-line-tracing",  "en",  "alias",     "no hyphen"),

    # sawtooth-instability
    ("锯齿不稳定性",     "sawtooth-instability", "zh",  "preferred", ""),
    ("sawtooth instability","sawtooth-instability","en","preferred",  ""),
    ("sawtooth oscillation","sawtooth-instability","en","alias",      "synonym"),
    ("sawtooth crash",   "sawtooth-instability", "en",  "alias",     "event name"),
    ("锯齿振荡",         "sawtooth-instability", "zh",  "alias",     "synonym"),

    # current-drive
    ("电流驱动",         "current-drive",        "zh",  "preferred", ""),
    ("current drive",    "current-drive",        "en",  "preferred", ""),
    ("CD",               "current-drive",        "abbr","preferred",  "canonical abbr"),
    ("non-inductive current drive","current-drive","en","alias",     "full form"),
    ("非感应电流驱动",   "current-drive",        "zh",  "alias",     "non-inductive form"),

    # triple-product
    ("三重积",           "triple-product",       "zh",  "preferred", ""),
    ("triple product",   "triple-product",       "en",  "preferred", ""),
    ("fusion triple product","triple-product",   "en",  "alias",     "full form"),
    ("聚变三重积",       "triple-product",       "zh",  "alias",     "full form"),
    ("nTτ",              "triple-product",       "en",  "alias",     "formula notation"),

    ("# ==== Batch 50: new concepts — heating/CD ====",),

    # lower-hybrid-heating
    ("低杂波加热",       "lower-hybrid-heating", "zh",  "preferred", ""),
    ("lower hybrid heating","lower-hybrid-heating","en","preferred",  ""),
    ("LHH",              "lower-hybrid-heating", "abbr","preferred",  "canonical abbr"),
    ("低混杂波加热",     "lower-hybrid-heating", "zh",  "alias",     "variant"),

    # neutral-beam-current-drive
    ("中性束电流驱动",   "neutral-beam-current-drive","zh","preferred",""),
    ("neutral beam current drive","neutral-beam-current-drive","en","preferred",""),
    ("NBCD",             "neutral-beam-current-drive","abbr","preferred","canonical abbr"),

    ("# ==== Batch 50: new concepts — confinement ====",),

    # energy-confinement-time
    ("能量约束时间",     "energy-confinement-time","zh","preferred",  ""),
    ("energy confinement time","energy-confinement-time","en","preferred",""),
    ("τ_E",              "energy-confinement-time","en","alias",     "symbol (see also tau-e)"),
    ("能量约束时间τE",   "energy-confinement-time","zh","alias",     "with symbol"),

    # ignition-condition
    ("点火条件",         "ignition-condition",   "zh",  "preferred", ""),
    ("ignition condition","ignition-condition",  "en",  "preferred", ""),
    ("ignition criterion","ignition-condition",  "en",  "alias",     "synonym"),
    ("点火判据",         "ignition-condition",   "zh",  "alias",     "synonym"),

    ("# ==== Batch 50: new concepts — divertor/SOL ====",),

    # detachment
    ("脱靶",             "detachment",           "zh",  "preferred", ""),
    ("detachment",       "detachment",           "en",  "preferred", ""),
    ("plasma detachment","detachment",           "en",  "alias",     "full form"),
    ("等离子体脱靶",     "detachment",           "zh",  "alias",     "full form"),
    ("偏滤器脱靶",       "detachment",           "zh",  "alias",     "divertor context"),

    # high-recycling
    ("高再循环",         "high-recycling",       "zh",  "preferred", ""),
    ("high recycling",   "high-recycling",       "en",  "preferred", ""),
    ("high-recycling regime","high-recycling",   "en",  "alias",     "regime form"),
    ("高再循环区",       "high-recycling",       "zh",  "alias",     "regime form"),

    # sheath
    ("鞘层",             "sheath",               "zh",  "preferred", ""),
    ("sheath",           "sheath",               "en",  "preferred", ""),
    ("plasma sheath",    "sheath",               "en",  "alias",     "full form"),
    ("等离子体鞘层",     "sheath",               "zh",  "alias",     "full form"),
    ("Debye sheath",     "sheath",               "en",  "alias",     "synonym"),

    ("# ==== Batch 50: new concepts — blanket/material ====",),

    # ceramic-breeder
    ("陶瓷增殖剂",       "ceramic-breeder",      "zh",  "preferred", ""),
    ("ceramic breeder",  "ceramic-breeder",      "en",  "preferred", ""),
    ("陶瓷增殖材料",     "ceramic-breeder",      "zh",  "alias",     "variant"),

    # wcll
    ("水冷锂铅包层",     "wcll",                 "zh",  "preferred", ""),
    ("water-cooled lithium-lead","wcll",          "en", "preferred",  ""),
    ("WCLL",             "wcll",                 "abbr","preferred",  "canonical abbr"),
    ("water-cooled lithium-lead blanket","wcll",  "en", "alias",     "full form"),

    ("# ==== Batch 50: new concepts — safety ====",),

    # loss-of-vacuum-accident
    ("失真空事故",       "loss-of-vacuum-accident","zh","preferred",  ""),
    ("loss of vacuum accident","loss-of-vacuum-accident","en","preferred",""),
    ("LOVA",             "loss-of-vacuum-accident","abbr","preferred","canonical abbr"),

    ("# ==== Batch 50: new concepts — neutronics ====",),

    # neutron-activation
    ("中子活化",         "neutron-activation",   "zh",  "preferred", ""),
    ("neutron activation","neutron-activation",  "en",  "preferred", ""),
    ("中子活化分析",     "neutron-activation",   "zh",  "alias",     "analysis context"),

    # neutron-camera
    ("中子照相机",       "neutron-camera",       "zh",  "preferred", ""),
    ("neutron camera",   "neutron-camera",       "en",  "preferred", ""),
    ("中子相机",         "neutron-camera",       "zh",  "alias",     "short form"),

    ("# ==== Batch 50: new concepts — stellarator ====",),

    # helias
    ("HELIAS",           "helias",               "abbr","preferred",  "canonical abbr"),
    ("helical-axis advanced stellarator","helias","en", "alias",     "expansion"),

    # quasi-symmetric-stellarator
    ("准对称仿星器",     "quasi-symmetric-stellarator","zh","preferred",""),
    ("quasi-symmetric stellarator","quasi-symmetric-stellarator","en","preferred",""),
    ("QSS",              "quasi-symmetric-stellarator","abbr","preferred","canonical abbr"),
    ("准对称优化仿星器", "quasi-symmetric-stellarator","zh","alias","variant"),

    ("# ==== Batch 50: new concepts — power plant ====",),

    # coolant-loop
    ("冷却回路",         "coolant-loop",         "zh",  "preferred", ""),
    ("coolant loop",     "coolant-loop",         "en",  "preferred", ""),
    ("coolant circuit",  "coolant-loop",         "en",  "alias",     "synonym"),
    ("冷却循环回路",     "coolant-loop",         "zh",  "alias",     "full form"),

    # power-conversion-system
    ("能量转换系统",     "power-conversion-system","zh","preferred",  ""),
    ("power conversion system","power-conversion-system","en","preferred",""),
    ("PCS",              "power-conversion-system","abbr","preferred","canonical abbr"),

    # maintenance-period
    ("维护周期",         "maintenance-period",   "zh",  "preferred", ""),
    ("maintenance period","maintenance-period",  "en",  "preferred", ""),
    ("maintenance interval","maintenance-period","en",  "alias",     "synonym"),
    ("维护间隔",         "maintenance-period",   "zh",  "alias",     "synonym"),

    ("# ==== Batch 50: new concepts — simulation ====",),

    # gyrokinetic-simulation
    ("回旋动理学模拟",   "gyrokinetic-simulation","zh","preferred",  ""),
    ("gyrokinetic simulation","gyrokinetic-simulation","en","preferred",""),
    ("GK simulation",    "gyrokinetic-simulation","en","alias",      "short form"),
    ("GK模拟",           "gyrokinetic-simulation","zh","alias",      "short form"),
]

# ──────────────────────────────────────────────────────
#  Part 3: Alias enrichment for existing concepts
#  (concepts that already exist but proposed aliases are not yet registered)
# ──────────────────────────────────────────────────────
ENRICH_ALIASES = [
    ("# ==== Batch 50: alias enrichment for existing concepts ====",),

    # hccb — add HCSB synonym
    ("HCSB",                     "hccb",  "abbr", "alias",  "helium-cooled solid breeder synonym"),
    ("helium-cooled solid breeder","hccb", "en",   "alias",  "alternate name"),

    # flux-surface — add magnetic flux surface alias
    # (磁通量面 conflict found → it is NOT yet an alias of flux-surface, so add)
    # Actually it IS already an alias (the conflict check showed it maps to flux-surface)
    # So skip 磁通量面.

    # eccd — add full-name aliases
    ("electron cyclotron current drive","eccd","en","alias","full expansion"),

    # tbm — add test blanket module form
    # conflict shows "test blanket module" already maps to tbm → skip

    # dcll — add full form
    # conflict shows "dual-coolant lithium-lead" already maps to dcll → skip

    # deep-penetration — add neutron streaming alias
    # conflict shows "neutron streaming" already maps to deep-penetration → skip

    # loss-of-coolant-accident — add 冷却剂丧失事故 variant
    ("冷却剂丧失事故",   "loss-of-coolant-accident","zh","alias","variant translation"),

    # loss-of-flow-accident — add 冷却剂失流事故 variant
    ("冷却剂失流事故",   "loss-of-flow-accident","zh","alias","variant translation"),

    # fuel-capsule — add generic capsule alias
    ("capsule",          "fuel-capsule",    "en",  "alias",  "generic short form"),

    # laser-driven-fusion — add short form
    ("laser fusion",     "laser-driven-fusion","en","alias", "short form"),
    ("激光聚变",         "laser-driven-fusion","zh","alias", "short form"),

    # fispact-ii — add FISPACT short form
    # conflict shows FISPACT already maps to fispact-ii → skip

    # bolometer — add bolometry
    ("bolometry",        "bolometer",       "en",  "alias",  "technique name"),
    ("辐射热测量",       "bolometer",       "zh",  "alias",  "technique name"),

    # charge-exchange-recombination-spectroscopy — add short forms
    ("CXS",              "charge-exchange-recombination-spectroscopy","abbr","alias","short abbr"),
    ("charge-exchange spectroscopy","charge-exchange-recombination-spectroscopy","en","alias","short name"),

    # dpa — add displacement per atom full form
    # conflict shows "displacement per atom" already maps to dpa → skip

    # hcll — add water-cooled variant is new concept wcll, skip here

    # capsule-implosion — add generic forms
    ("implosion",        "capsule-implosion","en",  "alias",  "generic short form"),
    ("内爆",             "capsule-implosion","zh",  "alias",  "generic short form"),

    # compression — too generic, add to capsule-implosion context
    ("fuel compression", "capsule-implosion","en",  "alias",  "compression context"),

    # magnetic-diagnostics — add singular form
    ("magnetic diagnostic","magnetic-diagnostics","en","alias","singular form"),

    # shutdown-dose-rate — add shut-down form
    ("shut-down dose rate","shutdown-dose-rate","en","alias","hyphenated form"),

    # rafm-steel — add full written-out forms
    ("reduced activation ferritic-martensitic steel","rafm-steel","en","alias","full name"),
    ("RAFM钢",          "rafm-steel",      "zh",  "alias",  "abbr+Chinese"),

    # ods-steel — add full form
    ("oxide dispersion strengthened steel","ods-steel","en","alias","full name"),
    ("ODS钢",           "ods-steel",       "zh",  "alias",  "abbr+Chinese"),

    # sic-sic-composite — add SiCf/SiC form
    ("SiCf/SiC",        "sic-sic-composite","en", "alias",  "fiber-reinforced form"),
    ("silicon carbide composite","sic-sic-composite","en","alias","generic name"),
]

# ──────────────────────────────────────────────────────
#  Part 4: Evidence for new concepts
# ──────────────────────────────────────────────────────
NEW_EVIDENCE = [
    # (concept_id, source, quote, added_by, added_at)
    ("debye-shielding",           f"internal:expansion:{BATCH}","Debye shielding in plasma",AUTHOR,DATE),
    ("plasma-resistivity",        f"internal:expansion:{BATCH}","Classical Spitzer resistivity",AUTHOR,DATE),
    ("flux-coordinate",           f"internal:expansion:{BATCH}","Magnetic flux coordinate system",AUTHOR,DATE),
    ("field-line-tracing",        f"internal:expansion:{BATCH}","Magnetic field line tracing method",AUTHOR,DATE),
    ("sawtooth-instability",      f"internal:expansion:{BATCH}","Internal kink sawtooth oscillation",AUTHOR,DATE),
    ("current-drive",             f"internal:expansion:{BATCH}","Non-inductive plasma current drive",AUTHOR,DATE),
    ("triple-product",            f"internal:expansion:{BATCH}","Lawson triple product nTτE",AUTHOR,DATE),
    ("lower-hybrid-heating",      f"internal:expansion:{BATCH}","Lower hybrid wave heating",AUTHOR,DATE),
    ("neutral-beam-current-drive",f"internal:expansion:{BATCH}","NBI current drive",AUTHOR,DATE),
    ("energy-confinement-time",   f"internal:expansion:{BATCH}","τE energy confinement time",AUTHOR,DATE),
    ("ignition-condition",        f"internal:expansion:{BATCH}","Self-sustained fusion ignition",AUTHOR,DATE),
    ("detachment",                f"internal:expansion:{BATCH}","Divertor plasma detachment",AUTHOR,DATE),
    ("high-recycling",            f"internal:expansion:{BATCH}","High recycling divertor regime",AUTHOR,DATE),
    ("sheath",                    f"internal:expansion:{BATCH}","Plasma-wall boundary sheath",AUTHOR,DATE),
    ("ceramic-breeder",           f"internal:expansion:{BATCH}","Li4SiO4/Li2TiO3 ceramic breeder",AUTHOR,DATE),
    ("wcll",                      f"internal:expansion:{BATCH}","EU WCLL blanket concept",AUTHOR,DATE),
    ("loss-of-vacuum-accident",   f"internal:expansion:{BATCH}","LOVA design basis accident",AUTHOR,DATE),
    ("neutron-activation",        f"internal:expansion:{BATCH}","Neutron-induced activation",AUTHOR,DATE),
    ("neutron-camera",            f"internal:expansion:{BATCH}","Spatially resolved neutron diagnostic",AUTHOR,DATE),
    ("helias",                    f"internal:expansion:{BATCH}","HELIAS stellarator concept",AUTHOR,DATE),
    ("quasi-symmetric-stellarator",f"internal:expansion:{BATCH}","Quasi-symmetry optimized stellarator",AUTHOR,DATE),
    ("coolant-loop",              f"internal:expansion:{BATCH}","Primary/secondary coolant loop",AUTHOR,DATE),
    ("power-conversion-system",   f"internal:expansion:{BATCH}","PCS heat-to-electricity",AUTHOR,DATE),
    ("maintenance-period",        f"internal:expansion:{BATCH}","Scheduled maintenance interval",AUTHOR,DATE),
    ("gyrokinetic-simulation",    f"internal:expansion:{BATCH}","GK turbulence simulation",AUTHOR,DATE),
]


def main():
    print(f"=== Batch 50: +{len(NEW_CONCEPTS)} new concepts ===")
    write_tsv_rows(CONCEPTS_TSV, NEW_CONCEPTS)
    print(f"  concepts.tsv: appended {len(NEW_CONCEPTS)} rows")

    alias_data = [r for r in NEW_ALIASES if len(r) > 1]
    write_tsv_rows(ALIASES_TSV, NEW_ALIASES)
    print(f"  aliases.tsv:  appended {len(alias_data)} data + {len(NEW_ALIASES)-len(alias_data)} comment rows")

    enrich_data = [r for r in ENRICH_ALIASES if len(r) > 1]
    write_tsv_rows(ALIASES_TSV, ENRICH_ALIASES)
    print(f"  aliases.tsv:  appended {len(enrich_data)} enrichment aliases + {len(ENRICH_ALIASES)-len(enrich_data)} comment rows")

    write_tsv_rows(EVIDENCE_TSV, NEW_EVIDENCE)
    print(f"  evidence.tsv: appended {len(NEW_EVIDENCE)} rows")

    total_aliases = len(alias_data) + len(enrich_data)
    print(f"\nTotal: {len(NEW_CONCEPTS)} concepts, {total_aliases} aliases, {len(NEW_EVIDENCE)} evidence rows")


if __name__ == "__main__":
    main()
