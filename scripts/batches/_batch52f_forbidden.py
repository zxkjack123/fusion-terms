#!/usr/bin/env python3
"""Batch 52F — Forbidden aliases for the 8 new P1 concepts.

Covers typical AI mistranslation patterns for:
  helicon-wave, wave-plasma-interaction, hard-x-ray, magnetic-probe,
  faraday-rotation, material-migration, radiation-damage, embrittlement
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"


def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


aliases: list[tuple] = [
    ("# ==== Batch 52F: Forbidden — Heating / current drive ====",),
    # helicon-wave  (正确: 螺旋波)
    ("氦康波", "helicon-wave", "zh", "forbidden", "误音译helicon：正确为 螺旋波"),
    ("赫利肯波", "helicon-wave", "zh", "forbidden", "误音译helicon：正确为 螺旋波"),
    (
        "螺线波",
        "helicon-wave",
        "zh",
        "forbidden",
        "误译helicon(螺旋≠螺线)：正确为 螺旋波",
    ),
    ("螺旋形波", "helicon-wave", "zh", "forbidden", "误译：正确为 螺旋波"),
    # wave-plasma-interaction  (正确: 波等离子体相互作用)
    (
        "波等离子体交互作用",
        "wave-plasma-interaction",
        "zh",
        "forbidden",
        "误译interaction(相互作用≠交互作用)：正确为 波等离子体相互作用",
    ),
    (
        "波等离子交互",
        "wave-plasma-interaction",
        "zh",
        "forbidden",
        "双误(缺'体'+交互)：正确为 波等离子体相互作用",
    ),
    (
        "波浪等离子体相互作用",
        "wave-plasma-interaction",
        "zh",
        "forbidden",
        "误译wave(波≠波浪)：正确为 波等离子体相互作用",
    ),
    (
        "波等离子体互动",
        "wave-plasma-interaction",
        "zh",
        "forbidden",
        "误译interaction(相互作用≠互动)：正确为 波等离子体相互作用",
    ),
    ("# ==== Batch 52F: Forbidden — Diagnostics ====",),
    # hard-x-ray  (正确: 硬X射线)
    ("硬X光", "hard-x-ray", "zh", "forbidden", "误译X-ray(X射线≠X光)：正确为 硬X射线"),
    ("硬X光线", "hard-x-ray", "zh", "forbidden", "误译X-ray：正确为 硬X射线"),
    ("硬X线", "hard-x-ray", "zh", "deprecated", "省略'射'字：应为 硬X射线"),
    ("强X射线", "hard-x-ray", "zh", "forbidden", "误译hard(硬≠强)：正确为 硬X射线"),
    # magnetic-probe  (正确: 磁探针)
    (
        "磁力探针",
        "magnetic-probe",
        "zh",
        "forbidden",
        "误译magnetic(磁≠磁力)：正确为 磁探针",
    ),
    (
        "磁性探针",
        "magnetic-probe",
        "zh",
        "forbidden",
        "误译magnetic(磁≠磁性)：正确为 磁探针",
    ),
    (
        "磁场探头",
        "magnetic-probe",
        "zh",
        "forbidden",
        "误译probe(探针≠探头)：正确为 磁探针",
    ),
    (
        "磁探头",
        "magnetic-probe",
        "zh",
        "forbidden",
        "误译probe(探针≠探头)：正确为 磁探针",
    ),
    # faraday-rotation  (正确: 法拉第旋转)
    (
        "法拉弟旋转",
        "faraday-rotation",
        "zh",
        "forbidden",
        "误音译Faraday(法拉第≠法拉弟)：正确为 法拉第旋转",
    ),
    (
        "法拉第转动",
        "faraday-rotation",
        "zh",
        "forbidden",
        "误译rotation(旋转≠转动)：正确为 法拉第旋转",
    ),
    (
        "法拉第偏转",
        "faraday-rotation",
        "zh",
        "forbidden",
        "误译rotation(旋转≠偏转)：正确为 法拉第旋转",
    ),
    (
        "法拉第回转",
        "faraday-rotation",
        "zh",
        "forbidden",
        "误译rotation(旋转≠回转)：正确为 法拉第旋转",
    ),
    ("# ==== Batch 52F: Forbidden — Materials / PMI ====",),
    # material-migration  (正确: 材料迁移)
    (
        "材料移动",
        "material-migration",
        "zh",
        "forbidden",
        "误译migration(迁移≠移动)：正确为 材料迁移",
    ),
    (
        "材料转移",
        "material-migration",
        "zh",
        "forbidden",
        "误译migration(迁移≠转移)：正确为 材料迁移",
    ),
    (
        "材料移行",
        "material-migration",
        "zh",
        "forbidden",
        "误译migration(迁移≠移行)：正确为 材料迁移",
    ),
    (
        "物质迁移",
        "material-migration",
        "zh",
        "forbidden",
        "误译material(材料≠物质)：正确为 材料迁移",
    ),
    # radiation-damage  (正确: 辐照损伤)
    (
        "辐射伤害",
        "radiation-damage",
        "zh",
        "forbidden",
        "误译damage(损伤≠伤害)：正确为 辐照损伤",
    ),
    (
        "辐射损害",
        "radiation-damage",
        "zh",
        "forbidden",
        "误译damage(损伤≠损害)：正确为 辐照损伤",
    ),
    (
        "放射损伤",
        "radiation-damage",
        "zh",
        "forbidden",
        "误译radiation(辐照≠放射)：正确为 辐照损伤",
    ),
    ("射线损伤", "radiation-damage", "zh", "deprecated", "非标准：应为 辐照损伤"),
    # embrittlement  (正确: 脆化)
    (
        "脆性化",
        "embrittlement",
        "zh",
        "forbidden",
        "误译embrittlement(脆化≠脆性化)：正确为 脆化",
    ),
    (
        "变脆",
        "embrittlement",
        "zh",
        "forbidden",
        "误译embrittlement(脆化≠变脆)：正确为 脆化",
    ),
    ("脆裂", "embrittlement", "zh", "forbidden", "误译(脆化≠脆裂)：正确为 脆化"),
]

if __name__ == "__main__":
    write_tsv_rows(REG / "aliases.tsv", aliases)
    n = sum(1 for r in aliases if not r[0].startswith("#"))
    nf = sum(
        1
        for r in aliases
        if not r[0].startswith("#") and len(r) >= 4 and r[3] == "forbidden"
    )
    nd = sum(
        1
        for r in aliases
        if not r[0].startswith("#") and len(r) >= 4 and r[3] == "deprecated"
    )
    print(f"✓ Appended {n} alias rows ({nf} forbidden, {nd} deprecated)")
    print("Done — run validate_registry next.")
