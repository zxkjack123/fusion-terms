#!/usr/bin/env python3
"""Batch 9 (final sweep): forbidden/deprecated aliases for orgs, devices, materials, remnants."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 机构名误译 (1-12)
    # ========================================================================
    ("# ==== Batch 9A: organization name mistranslations ====",),

    # EUROfusion → 欧洲聚变能组织
    ("欧洲融合组织", "eurofusion", "zh", "forbidden", "误译fusion：正确为 欧洲聚变能组织"),

    # F4E → 聚变能源机构
    ("融合换能机构", "f4e", "zh", "forbidden", "误译fusion：正确为 聚变能源机构"),

    # SWIP → 核工业西南物理研究院
    ("西南物理研究所", "swip", "zh", "forbidden", "误译(研究院≠研究所)：正确为 核工业西南物理研究院"),

    # ASIPP → 等离子体物理研究所
    ("等离子物理研究所", "asipp", "zh", "forbidden", "缺字'体'：正确为 等离子体物理研究所"),

    # CFS → 联邦聚变系统
    ("联邦融合系统", "cfs", "zh", "forbidden", "误译fusion：正确为 联邦聚变系统"),

    # General Atomics → 通用原子能
    ("通用原子", "general-atomics", "zh", "forbidden", "缺字'能'：正确为 通用原子能"),
    ("一般原子能", "general-atomics", "zh", "forbidden", "误译general：正确为 通用原子能"),

    # IPP Garching → 马克斯·普朗克等离子体物理研究所
    ("IPP加兴研究所", "ipp-garching", "zh", "forbidden", "误译(应给全称)：正确为 马克斯·普朗克等离子体物理研究所"),

    # IAEA → 国际原子能机构
    ("国际原子能组织", "iaea", "zh", "forbidden", "误译(机构≠组织)：正确为 国际原子能机构"),

    # ENN → 新奥
    ("ENN能源", "enn", "zh", "forbidden", "冗赘：正确为 新奥"),

    # TAE Technologies → TAE Technologies
    ("TAE技术", "tae-technologies", "zh", "forbidden", "误译Technologies(应保留英文)：正确为 TAE Technologies"),
    ("TAE科技", "tae-technologies", "zh", "forbidden", "误译Technologies：正确为 TAE Technologies"),

    # Helion Energy → Helion Energy
    ("赫利昂能源", "helion-energy", "zh", "forbidden", "误音译(应保留英文)：正确为 Helion Energy"),

    # HB11 Energy → HB11 Energy
    ("HB11能源", "hb11-energy", "zh", "forbidden", "误译(应保留英文)：正确为 HB11 Energy"),

    # LPP Fusion → LPP Fusion
    ("LPP融合", "lpp-fusion", "zh", "forbidden", "误译fusion(应保留英文)：正确为 LPP Fusion"),

    # ========================================================================
    # B. 装置名误译 (13-18)
    # ========================================================================
    ("# ==== Batch 9B: device name mistranslations ====",),

    # CFETR → 中国聚变工程试验堆
    ("中国聚变工程实验反应堆", "cfetr", "zh", "forbidden", "误译(试验堆≠实验反应堆)：正确为 中国聚变工程试验堆"),

    # IFMIF → 国际聚变材料辐照装置
    ("国际融合材料辐照设施", "ifmif", "zh", "forbidden", "误译fusion+facility：正确为 国际聚变材料辐照装置"),

    # SG-III → 神光三号
    ("神光3号", "sg-iii", "zh", "deprecated", "非标准(三号≠3号)：应为 神光三号"),

    # Laser Mégajoule → 兆焦耳激光装置
    ("激光兆焦装置", "laser-megajoule", "zh", "forbidden", "语序错：正确为 兆焦耳激光装置"),

    # ENN compact fusion → 新奥紧凑聚变装置
    ("ENN紧凑融合装置", "enn-compact-fusion", "zh", "forbidden", "误译：正确为 新奥紧凑聚变装置"),

    # ENN CST → 新奥球形托卡马克
    ("ENN球形托卡马克", "enn-cst", "zh", "deprecated", "非标准：应为 新奥球形托卡马克"),

    # ========================================================================
    # C. 装置名纠偏·英文专有名保留 (19-41)
    # ========================================================================
    ("# ==== Batch 9C: device name corrections ====",),

    # EAST
    ("东方超环", "east", "zh", "forbidden", "非官方简译(装置名应保留 EAST)"),

    # JET
    ("联合欧洲环", "jet", "zh", "forbidden", "非官方简译(装置名应保留 JET)"),

    # DIII-D
    ("D三-D", "diii-d", "zh", "forbidden", "误译(装置名应保留 DIII-D)"),
    ("D3-D", "diii-d", "en", "forbidden", "误写(正确为 DIII-D)"),

    # ASDEX Upgrade
    ("ASDEX升级", "asdex-upgrade", "zh", "forbidden", "误译Upgrade(装置名应保留 ASDEX Upgrade)"),

    # KSTAR
    ("韩国之星", "kstar", "zh", "forbidden", "误译(装置名应保留 KSTAR)"),
    ("K-Star", "kstar", "en", "forbidden", "误写(正确为 KSTAR)"),

    # SPARC
    ("斯帕克", "sparc", "zh", "forbidden", "误音译(装置名应保留 SPARC)"),

    # ARC
    ("弧", "arc", "zh", "forbidden", "误混同名词(装置名应保留 ARC)"),

    # STEP
    ("步骤", "step", "zh", "forbidden", "误混同名词(装置名应保留 STEP)"),

    # NSTX-U
    ("NSTX-U升级", "nstx-u", "zh", "forbidden", "冗赘(U已含upgrade义)"),

    # MAST-U
    ("MAST升级", "mast-u", "zh", "forbidden", "误译(装置名应保留 MAST-U)"),

    # JT-60SA
    ("JT60SA", "jt-60sa", "en", "forbidden", "缺连字符(正确为 JT-60SA)"),

    # HL-2A
    ("环流器二号A", "hl-2a", "zh", "deprecated", "非标准(缩写场景应保留 HL-2A)"),

    # HL-2M
    ("环流器二号M", "hl-2m", "zh", "deprecated", "非标准(缩写场景应保留 HL-2M)"),

    # Wendelstein 7-X
    ("温德尔斯坦7-X", "wendelstein-7x", "zh", "forbidden", "误音译(装置名应保留 Wendelstein 7-X)"),

    # HSX
    ("螺旋对称实验", "helically-symmetric-experiment", "zh", "forbidden", "非标准冗译(装置名应保留 HSX)"),

    # RFX-mod
    ("RFX改进型", "rfx-mod", "zh", "forbidden", "误译mod(装置名应保留 RFX-mod)"),

    # C-2W
    ("C2W", "c-2w", "en", "forbidden", "缺连字符(正确为 C-2W)"),

    # NIF
    ("国家点火设施", "nif", "zh", "forbidden", "非官方中文(装置名应保留 NIF)"),

    # EXL-50
    # NOTE: 'EXL50' skipped — already exists as alias

    # EXL-50U
    # NOTE: 'EXL50U' skipped — already exists as alias

    # SSPX
    ("稳态球马克实验", "sspx", "zh", "forbidden", "非标准冗译(装置名应保留 SSPX)"),

    # ========================================================================
    # D. 材料名误译 (42-49)
    # ========================================================================
    ("# ==== Batch 9D: material name mistranslations ====",),

    # tungsten → 钨
    ("钨金属", "tungsten", "zh", "deprecated", "冗赘：应为 钨"),

    # Nb3Sn → 铌三锡
    ("铌锡三", "nb3sn", "zh", "forbidden", "语序错：正确为 铌三锡"),

    # NbTi → 铌钛
    ("铌-钛", "nbti", "zh", "deprecated", "非标准(不需连字符)：应为 铌钛"),

    # EUROFER → EUROFER钢
    ("欧洲铁素体钢", "eurofer", "zh", "forbidden", "误展开缩写：正确为 EUROFER钢"),

    # CLF-1 → CLF-1钢
    ("CLF-1合金", "clf-1", "zh", "forbidden", "材质标示错(钢≠合金)：正确为 CLF-1钢"),

    # CLAM → CLAM钢
    ("CLAM合金", "clam", "zh", "forbidden", "材质标示错(钢≠合金)：正确为 CLAM钢"),

    # CuCrZr → CuCrZr合金
    # NOTE: '铜铬锆' skipped — already exists as alias

    # F82H → F82H钢
    ("F82H合金", "f82h", "zh", "forbidden", "材质标示错(钢≠合金)：正确为 F82H钢"),

    # ========================================================================
    # E. 剩余物理概念 (50)
    # ========================================================================
    ("# ==== Batch 9E: remaining physics concepts ====",),

    # thermal power → 热功率
    ("热电力", "thermal-power", "zh", "forbidden", "误译power(功率≠电力)：正确为 热功率"),
    ("热量功率", "thermal-power", "zh", "forbidden", "冗赘：正确为 热功率"),

    # MARFE
    ("马尔夫", "marfe", "zh", "forbidden", "误音译缩写(应保留 MARFE)"),
]


def write_tsv_rows(path, rows):
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:
                f.write(row[0] + "\n")
            else:
                f.write(T.join(row) + "\n")


if __name__ == "__main__":
    write_tsv_rows(REG / "aliases.tsv", WRONG_ALIASES)
    n = sum(1 for r in WRONG_ALIASES if len(r) > 1)
    print(f"Appended {n} forbidden/deprecated aliases")
