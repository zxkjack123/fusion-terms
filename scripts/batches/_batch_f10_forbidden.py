#!/usr/bin/env python3
"""Batch F10: forbidden/deprecated aliases for 31 concepts without coverage.

Covers:  10 concept  +  4 device  +  4 method  +  1 material
       +  3 system   +  2 metric  +  1 diagnostic  +  6 code
Total:  50 aliases  →  31 concepts
"""

import pathlib

ALIASES_TSV = pathlib.Path("terms/registry/aliases.tsv")

# (text, concept_id, lang, kind, comment)
DATA = [
    # ── concept (10 concepts, 20 aliases) ──────────────────────────
    ("# ==== batch F10: forbidden for 31 uncovered concepts ====",),
    # current-drive
    ("电流传动", "current-drive", "zh", "forbidden", "传动=mechanical transmission"),
    ("电流驱力", "current-drive", "zh", "forbidden", "驱力 is non-standard hybrid"),
    # debye-shielding
    ("德拜遮蔽", "debye-shielding", "zh", "forbidden", "遮蔽 not standard for plasma shielding"),
    ("德拜防护", "debye-shielding", "zh", "forbidden", "防护=protection, wrong domain"),
    # flux-coordinate
    ("通量坐标", "flux-coordinate", "zh", "forbidden", "generic 通量 ambiguous; use 磁通坐标"),
    # high-recycling
    ("高回收", "high-recycling", "zh", "forbidden", "回收=recovery/recycling of materials"),
    ("高循环", "high-recycling", "zh", "forbidden", "drops 再; 循环 alone is ambiguous"),
    # ignition-condition
    ("着火条件", "ignition-condition", "zh", "forbidden", "着火=combustion ignition"),
    ("引燃条件", "ignition-condition", "zh", "forbidden", "引燃=lighting a fire"),
    # loss-of-vacuum-accident
    ("真空丧失事故", "loss-of-vacuum-accident", "zh", "forbidden", "non-standard phrasing"),
    ("真空破坏事故", "loss-of-vacuum-accident", "zh", "forbidden", "破坏=destruction, wrong"),
    # monte-carlo-method
    ("蒙地卡罗方法", "monte-carlo-method", "zh", "forbidden", "Taiwan transliteration, non-standard"),
    ("蒙地卡罗法", "monte-carlo-method", "zh", "forbidden", "Taiwan transliteration, non-standard"),
    # neutron-activation
    ("中子激活", "neutron-activation", "zh", "forbidden", "激活=activate a system, not nuclear activation"),
    ("中子激发", "neutron-activation", "zh", "forbidden", "激发=excitation, different process"),
    # plasma-resistivity
    ("等离子体阻率", "plasma-resistivity", "zh", "forbidden", "阻率 non-standard; use 电阻率"),
    ("等离子电阻率", "plasma-resistivity", "zh", "deprecated", "missing 体; standard form is 等离子体电阻率"),
    # quasi-symmetric-stellarator
    ("准对称恒星器", "quasi-symmetric-stellarator", "zh", "forbidden", "恒星器=literal translation, wrong"),
    ("拟对称仿星器", "quasi-symmetric-stellarator", "zh", "forbidden", "拟对称 non-standard; use 准对称"),

    # ── device (4 concepts, 4 aliases) ─────────────────────────────
    ("最佳", "cfetrcoolact", "zh", "forbidden", "AI mistranslates BEST as adjective"),
    ("多内斯", "dones", "zh", "forbidden", "wrong transliteration of acronym"),
    ("赫利亚斯", "helias", "zh", "forbidden", "wrong transliteration of acronym"),
    ("欧米伽", "omega", "zh", "forbidden", "wrong transliteration of facility name"),

    # ── method (4 concepts, 8 aliases) ─────────────────────────────
    # field-line-tracing
    ("场线追踪", "field-line-tracing", "zh", "forbidden", "场线 non-standard; use 磁力线"),
    ("磁场线追迹", "field-line-tracing", "zh", "forbidden", "磁场线/追迹 both non-standard"),
    # gyrokinetic-simulation
    ("陀螺动力学模拟", "gyrokinetic-simulation", "zh", "forbidden", "陀螺动力学=gyroscopic dynamics"),
    ("旋转动理学模拟", "gyrokinetic-simulation", "zh", "forbidden", "旋转=rotation, not gyro"),
    # lower-hybrid-heating
    ("下混合波加热", "lower-hybrid-heating", "zh", "forbidden", "literal translation of 'lower hybrid'"),
    ("低杂交波加热", "lower-hybrid-heating", "zh", "forbidden", "杂交=biological hybridization"),
    # neutral-beam-current-drive
    ("中性粒子束电流传动", "neutral-beam-current-drive", "zh", "forbidden", "粒子束+传动 both wrong"),
    ("中性光束电流驱动", "neutral-beam-current-drive", "zh", "forbidden", "光束=light beam, wrong"),

    # ── material (1 concept, 2 aliases) ────────────────────────────
    ("陶瓷繁殖剂", "ceramic-breeder", "zh", "forbidden", "繁殖=biological breeding"),
    ("陶瓷育种剂", "ceramic-breeder", "zh", "forbidden", "育种=plant breeding"),

    # ── system (3 concepts, 5 aliases) ─────────────────────────────
    # coolant-loop
    ("制冷回路", "coolant-loop", "zh", "forbidden", "制冷=refrigeration"),
    ("冷冻回路", "coolant-loop", "zh", "forbidden", "冷冻=freezing"),
    # power-conversion-system
    ("功率转换系统", "power-conversion-system", "zh", "forbidden", "功率转换 wrong phrasing in fusion"),
    ("电力转换系统", "power-conversion-system", "zh", "forbidden", "电力 wrong domain term"),
    # wcll
    ("水冷铅锂包层", "wcll", "zh", "forbidden", "wrong order: 锂铅 not 铅锂"),

    # ── metric (2 concepts, 4 aliases) ─────────────────────────────
    # fusion-gain
    ("聚变收益", "fusion-gain", "zh", "forbidden", "收益=financial return"),
    ("聚变倍增", "fusion-gain", "zh", "forbidden", "倍增=doubling, wrong term"),
    # maintenance-period
    ("保养周期", "maintenance-period", "zh", "forbidden", "保养=vehicle/appliance maintenance"),
    ("保修周期", "maintenance-period", "zh", "forbidden", "保修=warranty period"),

    # ── diagnostic (1 concept, 2 aliases) ──────────────────────────
    ("中子摄像机", "neutron-camera", "zh", "forbidden", "摄像机=video camera"),
    ("中子摄影机", "neutron-camera", "zh", "forbidden", "摄影机=film camera"),

    # ── code (6 concepts, 5 aliases) ───────────────────────────────
    ("科西嘉", "corsica", "zh", "forbidden", "AI translates code name as Corsica island"),
    ("迪娜", "dina", "zh", "forbidden", "AI translates code name as person name"),
    ("巨人4", "geant4", "zh", "forbidden", "AI translates French géant as 巨人"),
    ("海伦娜", "helena", "zh", "forbidden", "AI translates code name as person name"),
    ("的黎波里", "tripoli", "zh", "forbidden", "AI translates code name as Tripoli city"),
]


def write_tsv_rows(path: pathlib.Path, rows: list[tuple]) -> int:
    """Append tab-joined rows, return count of data rows written."""
    n = 0
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:          # comment-only row
                f.write(row[0] + "\n")
            else:
                f.write("\t".join(row) + "\n")
                n += 1
    return n


if __name__ == "__main__":
    n = write_tsv_rows(ALIASES_TSV, DATA)
    concepts = {r[1] for r in DATA if len(r) > 1}
    forbidden = sum(1 for r in DATA if len(r) > 1 and r[3] == "forbidden")
    deprecated = sum(1 for r in DATA if len(r) > 1 and r[3] == "deprecated")
    print(f"Wrote {n} aliases ({forbidden} forbidden + {deprecated} deprecated) "
          f"for {len(concepts)} concepts")
