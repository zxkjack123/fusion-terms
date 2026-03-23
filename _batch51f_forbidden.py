#!/usr/bin/env python3
"""Batch 51F — Forbidden aliases for the 27 new P0 concepts.

Covers typical AI mistranslation / hallucination patterns:
  - zh: wrong-character translations, literal transliterations, confusion with similar terms
  - en: common misspellings
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"

def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")

aliases: list[tuple] = [
    ("# ==== Batch 51F: Forbidden — Transport / micro-instabilities ====",),

    # gyro-bohm-scaling  (正确: 旋回Bohm标度 / 旋回玻姆标度)
    ("回旋Bohm标度",       "gyro-bohm-scaling", "zh", "forbidden", "误译gyro(旋回≠回旋)：正确为 旋回Bohm标度"),
    ("陀螺Bohm标度",       "gyro-bohm-scaling", "zh", "forbidden", "误译gyro：正确为 旋回Bohm标度"),
    ("旋回波姆标度",       "gyro-bohm-scaling", "zh", "forbidden", "误音译Bohm(玻姆≠波姆)：正确为 旋回玻姆标度"),
    ("旋回玻尔姆标度",     "gyro-bohm-scaling", "zh", "forbidden", "误音译Bohm(玻姆≠玻尔姆)：正确为 旋回玻姆标度"),
    ("回旋玻姆缩放",       "gyro-bohm-scaling", "zh", "forbidden", "误译gyro+scaling(标度≠缩放)：正确为 旋回Bohm标度"),

    # turbulent-diffusion  (正确: 湍流扩散输运)
    # NOTE: 湍流扩散 is alias of turbulence-spreading, so we cannot use it
    ("紊流扩散",           "turbulent-diffusion", "zh", "forbidden", "误译turbulent(湍流≠紊流)：正确为 湍流扩散输运"),
    ("湍流弥散",           "turbulent-diffusion", "zh", "forbidden", "误译diffusion(扩散≠弥散)：正确为 湍流扩散输运"),
    ("湍流扩散系数",       "turbulent-diffusion", "zh", "deprecated", "非标准：应为 湍流扩散输运"),

    # particle-pinch  (正确: 粒子箍缩)
    ("粒子挤压",           "particle-pinch", "zh", "forbidden", "误译pinch(箍缩≠挤压)：正确为 粒子箍缩"),
    ("粒子捏缩",           "particle-pinch", "zh", "forbidden", "误译pinch(箍缩≠捏缩)：正确为 粒子箍缩"),
    ("粒子收缩",           "particle-pinch", "zh", "forbidden", "误译pinch(箍缩≠收缩)：正确为 粒子箍缩"),
    ("颗粒箍缩",           "particle-pinch", "zh", "forbidden", "误译particle(粒子≠颗粒)：正确为 粒子箍缩"),

    # thermodiffusion  (正确: 热扩散)
    ("热弥散",             "thermodiffusion", "zh", "forbidden", "误译diffusion(扩散≠弥散)：正确为 热扩散"),
    ("热扩散效应",         "thermodiffusion", "zh", "deprecated", "非标准：应为 热扩散"),
    ("温度扩散",           "thermodiffusion", "zh", "forbidden", "误译thermo(热≠温度)：正确为 热扩散"),
    ("索雷效应",           "thermodiffusion", "zh", "forbidden", "误音译Soret：正确英文为 Soret effect"),

    ("# ==== Batch 51F: Forbidden — MHD stability ====",),

    # external-kink  (正确: 外扭曲模)
    ("外部扭曲模",         "external-kink", "zh", "forbidden", "误译external(外≠外部)：正确为 外扭曲模"),
    ("外部扭折模",         "external-kink", "zh", "forbidden", "误译kink+external：正确为 外扭曲模"),
    ("外扭折模",           "external-kink", "zh", "forbidden", "误译kink(扭曲≠扭折)：正确为 外扭曲模"),
    ("外扭结模",           "external-kink", "zh", "forbidden", "误译kink(扭曲≠扭结)：正确为 外扭曲模"),
    ("外扭曲模式",         "external-kink", "zh", "deprecated", "非标准：应为 外扭曲模"),

    # sausage-instability  (正确: 腊肠不稳定性)
    ("香肠模",             "sausage-instability", "zh", "deprecated", "非标准：应为 腊肠模"),
    ("热狗不稳定性",       "sausage-instability", "zh", "forbidden", "误译sausage：正确为 腊肠不稳定性"),
    ("腊肠不稳定",         "sausage-instability", "zh", "deprecated", "缺'性'字：应为 腊肠不稳定性"),
    ("肠型不稳定性",       "sausage-instability", "zh", "forbidden", "误译sausage：正确为 腊肠不稳定性"),

    # pressure-driven-mode  (正确: 压力驱动模)
    ("压力驱动模式",       "pressure-driven-mode", "zh", "deprecated", "非标准：应为 压力驱动模"),
    ("压强驱动模",         "pressure-driven-mode", "zh", "forbidden", "误译pressure(压力≠压强)：正确为 压力驱动模"),
    ("气压驱动模",         "pressure-driven-mode", "zh", "forbidden", "误译pressure(压力≠气压)：正确为 压力驱动模"),

    # current-driven-mode  (正确: 电流驱动模)
    ("电流驱动模式",       "current-driven-mode", "zh", "deprecated", "非标准：应为 电流驱动模"),
    ("电流驱动的模",       "current-driven-mode", "zh", "deprecated", "非标准：应为 电流驱动模"),
    ("流驱动模",           "current-driven-mode", "zh", "forbidden", "误缩写：正确为 电流驱动模"),

    # ideal-mhd-stability  (正确: 理想MHD稳定性)
    ("理想MHD稳定度",      "ideal-mhd-stability", "zh", "forbidden", "误译stability(稳定性≠稳定度)：正确为 理想MHD稳定性"),
    ("理想磁流体稳定度",   "ideal-mhd-stability", "zh", "forbidden", "误译stability(稳定性≠稳定度)：正确为 理想MHD稳定性"),
    ("理想磁流体力学稳定性","ideal-mhd-stability", "zh", "deprecated", "冗余：应为 理想MHD稳定性"),

    # resistive-instability  (正确: 电阻不稳定性)
    ("阻性不稳定性",       "resistive-instability", "zh", "forbidden", "误译resistive(电阻≠阻性)：正确为 电阻不稳定性"),
    ("电阻性不稳定性",     "resistive-instability", "zh", "deprecated", "非标准：应为 电阻不稳定性"),
    ("电阻不稳定",         "resistive-instability", "zh", "deprecated", "缺'性'字：应为 电阻不稳定性"),

    # global-alfven-eigenmode  (正确: 全局Alfvén本征模)
    ("全局阿尔文本征模",   "global-alfven-eigenmode", "zh", "forbidden", "误音译Alfvén(阿尔芬≠阿尔文)：正确为 全局Alfvén本征模"),
    ("全球Alfvén本征模",   "global-alfven-eigenmode", "zh", "forbidden", "误译global(全局≠全球)：正确为 全局Alfvén本征模"),
    ("整体Alfvén本征模",   "global-alfven-eigenmode", "zh", "forbidden", "误译global(全局≠整体)：正确为 全局Alfvén本征模"),
    ("全局阿尔芬特征模",   "global-alfven-eigenmode", "zh", "forbidden", "误译eigenmode(本征模≠特征模)：正确为 全局Alfvén本征模"),

    ("# ==== Batch 51F: Forbidden — SOL / divertor physics ====",),

    # parallel-heat-flux  (正确: 平行热流)
    ("并行热流",           "parallel-heat-flux", "zh", "forbidden", "误译parallel(平行≠并行)：正确为 平行热流"),
    ("平行热通量",         "parallel-heat-flux", "zh", "deprecated", "非标准：应为 平行热流"),
    ("平行热量流",         "parallel-heat-flux", "zh", "forbidden", "误译heat flux：正确为 平行热流"),

    # filament  (正确: 等离子体丝状体)
    ("等离子灯丝",         "filament", "zh", "forbidden", "误译filament(丝状体≠灯丝)：正确为 等离子体丝状体"),
    ("等离子体细丝",       "filament", "zh", "forbidden", "误译filament(丝状体≠细丝)：正确为 等离子体丝状体"),
    ("等离子纤丝",         "filament", "zh", "forbidden", "误译filament：正确为 等离子体丝状体"),
    ("纤维状结构",         "filament", "zh", "forbidden", "误译filament(丝状体≠纤维状结构)：正确为 等离子体丝状体"),
    ("灯丝",               "filament", "zh", "forbidden", "误译filament(等离子体丝状体≠灯丝)：正确为 丝状体"),

    # divertor-leg  (正确: 偏滤器腿)
    ("分流器腿",           "divertor-leg", "zh", "forbidden", "误译divertor(偏滤器≠分流器)：正确为 偏滤器腿"),
    ("偏滤器臂",           "divertor-leg", "zh", "forbidden", "误译leg(腿≠臂)：正确为 偏滤器腿"),
    ("偏转器腿",           "divertor-leg", "zh", "forbidden", "误译divertor(偏滤器≠偏转器)：正确为 偏滤器腿"),

    # flux-tube  (正确: 磁通管)
    ("通量管",             "flux-tube", "zh", "forbidden", "误译flux(磁通≠通量)：正确为 磁通管"),
    ("磁流管",             "flux-tube", "zh", "forbidden", "误译flux tube(磁通管≠磁流管)：正确为 磁通管"),
    ("磁力管",             "flux-tube", "zh", "forbidden", "误译flux tube(磁通管≠磁力管)：正确为 磁通管"),

    # connection-length  (正确: 连接长度)
    ("连通长度",           "connection-length", "zh", "forbidden", "误译connection(连接≠连通)：正确为 连接长度"),
    ("联系长度",           "connection-length", "zh", "forbidden", "误译connection(连接≠联系)：正确为 连接长度"),
    ("连线长度",           "connection-length", "zh", "forbidden", "误译connection(连接≠连线)：正确为 连接长度"),

    # wetted-area  (正确: 湿润面积)
    ("润湿面积",           "wetted-area", "zh", "deprecated", "语序：应为 湿润面积"),
    ("浸湿面积",           "wetted-area", "zh", "forbidden", "误译wetted(湿润≠浸湿)：正确为 湿润面积"),
    ("沾湿面积",           "wetted-area", "zh", "forbidden", "误译wetted(湿润≠沾湿)：正确为 湿润面积"),

    ("# ==== Batch 51F: Forbidden — Fuel cycle ====",),

    # fuel-cycle  (正确: 燃料循环)
    ("燃料周期",           "fuel-cycle", "zh", "forbidden", "误译cycle(循环≠周期)：正确为 燃料循环"),
    ("燃料回路",           "fuel-cycle", "zh", "forbidden", "误译cycle(循环≠回路)：正确为 燃料循环"),
    ("燃油循环",           "fuel-cycle", "zh", "forbidden", "误译fuel(燃料≠燃油)：正确为 燃料循环"),

    # isotope-separation  (正确: 同位素分离)
    ("同位素分割",         "isotope-separation", "zh", "forbidden", "误译separation(分离≠分割)：正确为 同位素分离"),
    ("同位素隔离",         "isotope-separation", "zh", "forbidden", "误译separation(分离≠隔离)：正确为 同位素分离"),
    ("同位素分选",         "isotope-separation", "zh", "forbidden", "误译separation(分离≠分选)：正确为 同位素分离"),

    # hydrogen-isotope  (正确: 氢同位素)
    ("氢的同位素",         "hydrogen-isotope", "zh", "deprecated", "非标准：应为 氢同位素"),
    ("氢气同位素",         "hydrogen-isotope", "zh", "forbidden", "误译hydrogen(氢≠氢气)：正确为 氢同位素"),

    # protium  (正确: 氕)
    ("质子",               "protium", "zh", "forbidden", "误译protium(氕≠质子)：正确为 氕"),
    ("轻氢",               "protium", "zh", "deprecated", "非标准：应为 氕"),
    ("普通氢",             "protium", "zh", "forbidden", "误译protium：正确为 氕"),

    # tritium-storage  (正确: 氚储存)
    ("氚存储",             "tritium-storage", "zh", "deprecated", "非标准：应为 氚储存"),
    ("氚仓储",             "tritium-storage", "zh", "forbidden", "误译storage(储存≠仓储)：正确为 氚储存"),
    ("氚保存",             "tritium-storage", "zh", "forbidden", "误译storage(储存≠保存)：正确为 氚储存"),

    # tritium-recovery  (正确: 氚回收)
    ("氚恢复",             "tritium-recovery", "zh", "forbidden", "误译recovery(回收≠恢复)：正确为 氚回收"),
    ("氚收集",             "tritium-recovery", "zh", "forbidden", "误译recovery(回收≠收集)：正确为 氚回收"),
    ("氚复原",             "tritium-recovery", "zh", "forbidden", "误译recovery(回收≠复原)：正确为 氚回收"),

    # tritium-processing  (正确: 氚处理)
    ("氚加工",             "tritium-processing", "zh", "forbidden", "误译processing(处理≠加工)：正确为 氚处理"),
    ("氚工艺",             "tritium-processing", "zh", "forbidden", "误译processing(处理≠工艺)：正确为 氚处理"),

    # palladium-membrane  (正确: 钯膜)
    ("钯薄膜",             "palladium-membrane", "zh", "deprecated", "非标准：应为 钯膜"),
    ("钯隔膜",             "palladium-membrane", "zh", "forbidden", "误译membrane(膜≠隔膜)：正确为 钯膜"),
    ("钯片",               "palladium-membrane", "zh", "forbidden", "误译membrane(膜≠片)：正确为 钯膜"),

    # getter-bed  (正确: 吸气剂床)
    ("吸附剂床",           "getter-bed", "zh", "forbidden", "误译getter(吸气剂≠吸附剂)：正确为 吸气剂床"),
    ("吸收剂床",           "getter-bed", "zh", "forbidden", "误译getter(吸气剂≠吸收剂)：正确为 吸气剂床"),
    ("除气器床",           "getter-bed", "zh", "forbidden", "误译getter(吸气剂≠除气器)：正确为 吸气剂床"),
    ("捕集器床",           "getter-bed", "zh", "forbidden", "误译getter(吸气剂≠捕集器)：正确为 吸气剂床"),

    # glovebox  (正确: 手套箱)
    ("手套盒",             "glovebox", "zh", "forbidden", "误译box(箱≠盒)：正确为 手套箱"),
    ("手套柜",             "glovebox", "zh", "forbidden", "误译glovebox(手套箱≠手套柜)：正确为 手套箱"),
]

if __name__ == "__main__":
    write_tsv_rows(REG / "aliases.tsv", aliases)
    n = sum(1 for r in aliases if not r[0].startswith("#"))
    nf = sum(1 for r in aliases if not r[0].startswith("#") and len(r) >= 4 and r[3] == "forbidden")
    nd = sum(1 for r in aliases if not r[0].startswith("#") and len(r) >= 4 and r[3] == "deprecated")
    print(f"✓ Appended {n} alias rows ({nf} forbidden, {nd} deprecated)")
    print("Done — run validate_registry next.")
