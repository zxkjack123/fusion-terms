#!/usr/bin/env python3
"""Batch 53F — Forbidden aliases for the 4 new P2 concepts.

occupational-dose, mean-free-path, cyclotron-frequency, magnetic-pressure
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"


def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


aliases: list[tuple] = [
    ("# ==== Batch 53F: Forbidden — P2 concepts ====",),
    # occupational-dose  (正确: 职业剂量)
    (
        "职业辐射",
        "occupational-dose",
        "zh",
        "forbidden",
        "误译dose(剂量≠辐射)：正确为 职业剂量",
    ),
    (
        "工作剂量",
        "occupational-dose",
        "zh",
        "forbidden",
        "误译occupational(职业≠工作)：正确为 职业剂量",
    ),
    (
        "职业暴露量",
        "occupational-dose",
        "zh",
        "forbidden",
        "误译dose(剂量≠暴露量)：正确为 职业剂量",
    ),
    # mean-free-path  (正确: 平均自由程)
    (
        "平均自由路径",
        "mean-free-path",
        "zh",
        "forbidden",
        "误译path(程≠路径)：正确为 平均自由程",
    ),
    ("平均自由行程", "mean-free-path", "zh", "deprecated", "非标准：应为 平均自由程"),
    (
        "平均自由道路",
        "mean-free-path",
        "zh",
        "forbidden",
        "误译path(程≠道路)：正确为 平均自由程",
    ),
    ("均自由程", "mean-free-path", "zh", "forbidden", "缺'平'字：正确为 平均自由程"),
    # cyclotron-frequency  (正确: 回旋频率)
    (
        "旋转频率",
        "cyclotron-frequency",
        "zh",
        "forbidden",
        "误译cyclotron(回旋≠旋转)：正确为 回旋频率",
    ),
    (
        "回转频率",
        "cyclotron-frequency",
        "zh",
        "forbidden",
        "误译cyclotron(回旋≠回转)：正确为 回旋频率",
    ),
    (
        "加速器频率",
        "cyclotron-frequency",
        "zh",
        "forbidden",
        "误译cyclotron(回旋≠加速器)：正确为 回旋频率",
    ),
    (
        "拉莫频率",
        "cyclotron-frequency",
        "zh",
        "forbidden",
        "误音译Larmor(拉莫尔≠拉莫)：正确为 拉莫尔频率",
    ),
    ("回旋频", "cyclotron-frequency", "zh", "deprecated", "缺'率'字：应为 回旋频率"),
    # magnetic-pressure  (正确: 磁压)
    (
        "磁力压力",
        "magnetic-pressure",
        "zh",
        "forbidden",
        "误译magnetic(磁≠磁力)：正确为 磁压",
    ),
    (
        "磁性压力",
        "magnetic-pressure",
        "zh",
        "forbidden",
        "误译magnetic(磁≠磁性)：正确为 磁压",
    ),
    (
        "磁场压强",
        "magnetic-pressure",
        "zh",
        "forbidden",
        "误译pressure(压≠压强)：正确为 磁压",
    ),
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
