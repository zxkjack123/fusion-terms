#!/usr/bin/env python3
"""Batch 8: forbidden/deprecated aliases for AI mistranslations (~85 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 仿星器·磁镜·先进概念 (1-16)
    # ========================================================================
    ("# ==== Batch 8A: stellarator, mirror, advanced concepts ====",),

    # stellarator optimization → 仿星器优化
    ("恒星器优化", "stellarator-optimization", "zh", "forbidden", "误译stellarator：正确为 仿星器优化"),

    # quasi-symmetry → 准对称
    ("拟对称", "quasi-symmetry", "zh", "deprecated", "非标准：应为 准对称"),

    # coil complexity → 线圈复杂度
    ("线圈复杂性", "coil-complexity", "zh", "deprecated", "非标准：应为 线圈复杂度"),

    # single helical state → 单螺旋态
    ("单螺旋状态", "single-helical-state", "zh", "deprecated", "非标准(态≠状态)：应为 单螺旋态"),

    # pulsed poloidal current drive → 脉冲极向电流驱动
    ("脉冲极性电流驱动", "pulsed-poloidal-current-drive", "zh", "forbidden", "误译poloidal(极向≠极性)：正确为 脉冲极向电流驱动"),

    # theta pinch → θ箍缩
    ("θ夹紧", "theta-pinch", "zh", "forbidden", "误译pinch：正确为 θ箍缩"),
    ("θ捏缩", "theta-pinch", "zh", "forbidden", "误译pinch：正确为 θ箍缩"),

    # translation → 平移 (FRC context)
    ("翻译", "translation", "zh", "forbidden", "误译(语言义)：FRC语境正确为 平移"),

    # rotational instability → 旋转不稳定性
    ("旋转不稳定", "rotational-instability", "zh", "deprecated", "缺字'性'：应为 旋转不稳定性"),
    ("转动不稳定性", "rotational-instability", "zh", "deprecated", "非标准：应为 旋转不稳定性"),

    # dense plasma focus → 稠密等离子体焦点
    ("致密等离子焦点", "dense-plasma-focus", "zh", "forbidden", "缺字'体'：正确为 稠密等离子体焦点"),
    ("密集等离子体焦点", "dense-plasma-focus", "zh", "forbidden", "误译dense(稠密≠密集)：正确为 稠密等离子体焦点"),

    # mirror machine → 磁镜装置
    ("镜子机", "mirror-machine", "zh", "forbidden", "误译mirror+machine：正确为 磁镜装置"),
    ("镜像机器", "mirror-machine", "zh", "forbidden", "误译mirror+machine：正确为 磁镜装置"),

    # plasma gun → 等离子体枪
    ("等离子枪", "plasma-gun", "zh", "forbidden", "缺字'体'：正确为 等离子体枪"),

    # traveling wave direct energy converter → 行波直接能量转换器
    ("旅行波直接能量转换器", "traveling-wave-direct-energy-converter", "zh", "forbidden", "误译traveling(行波≠旅行波)：正确为 行波直接能量转换器"),

    # odd-parity rotating magnetic field → 奇宇称旋转磁场
    ("奇偶旋转磁场", "odd-parity-rotating-magnetic-field", "zh", "forbidden", "误译odd-parity(奇宇称≠奇偶)：正确为 奇宇称旋转磁场"),
    ("奇奇偶性旋转磁场", "odd-parity-rotating-magnetic-field", "zh", "forbidden", "误译parity：正确为 奇宇称旋转磁场"),

    # neutral beam driven FRC → 中性束驱动场反
    ("中性光束驱动FRC", "neutral-beam-driven-frc", "zh", "forbidden", "误译beam(束≠光束)：正确为 中性束驱动场反"),

    # coaxial plasma gun → 同轴等离子体枪
    ("同轴等离子枪", "coaxial-plasma-gun", "zh", "forbidden", "缺字'体'：正确为 同轴等离子体枪"),

    # pinch parameter → 箍缩参数
    ("收缩参数", "pinch-parameter", "zh", "forbidden", "误译pinch(箍缩≠收缩)：正确为 箍缩参数"),
    ("夹缩参数", "pinch-parameter", "zh", "forbidden", "误译pinch：正确为 箍缩参数"),

    # ========================================================================
    # B. 包层·系统缩写 (17-22)
    # ========================================================================
    ("# ==== Batch 8B: blanket acronyms ====",),

    # HCCB → 氦冷固态包层
    ("氦冷陶瓷包层", "hccb", "zh", "forbidden", "混淆HCCB/WCCB：正确为 氦冷固态包层"),

    # WCCB → 水冷陶瓷包层
    ("水冷固态包层", "wccb", "zh", "forbidden", "混淆WCCB/HCCB：正确为 水冷陶瓷包层"),

    # HCLL → 氦冷锂铅包层
    ("氦冷液态铅锂包层", "hcll", "zh", "forbidden", "冗译+顺序倒：正确为 氦冷锂铅包层"),

    # HCPB → 氦冷球床包层
    ("氦冷鹅卵石床包层", "hcpb", "zh", "forbidden", "误译pebble bed(球床≠鹅卵石床)：正确为 氦冷球床包层"),

    # fusion neutron → 聚变中子
    ("融合中子", "fusion-neutron", "zh", "forbidden", "误译fusion：正确为 聚变中子"),

    # lithium-lead → 锂铅
    # NOTE: '铅锂' skipped — already exists as alias

    # ========================================================================
    # C. 诊断·测量 (23-29)
    # ========================================================================
    ("# ==== Batch 8C: diagnostics & measurement ====",),

    # soft X-ray → 软X射线
    ("柔软X射线", "soft-x-ray", "zh", "forbidden", "误译soft(物理义)：正确为 软X射线"),

    # neutron diagnostics → 中子诊断
    ("中子诊断学", "neutron-diagnostics", "zh", "forbidden", "误加'学'：正确为 中子诊断"),

    # spectroscopy → 光谱诊断
    ("光谱学", "spectroscopy", "zh", "deprecated", "聚变诊断语境应为 光谱诊断"),

    # ECE imaging → ECE成像
    ("ECE影像", "ece-imaging", "zh", "forbidden", "误译imaging：正确为 ECE成像"),
    ("ECE图像", "ece-imaging", "zh", "forbidden", "误译imaging(成像≠图像)：正确为 ECE成像"),

    # plasma-sprayed tungsten → 等离子喷涂钨
    ("等离子体喷涂钨", "plasma-sprayed-tungsten", "zh", "forbidden", "喷涂场景用'等离子'不用'体'：正确为 等离子喷涂钨"),

    # electromagnetic force → 电磁力
    ("电磁学力", "electromagnetic-force", "zh", "forbidden", "误加'学'：正确为 电磁力"),

    # waveguide → 波导
    ("导波管", "waveguide", "zh", "deprecated", "非标准：应为 波导"),
    ("波导管", "waveguide", "zh", "deprecated", "非标准(冗赘)：应为 波导"),

    # ========================================================================
    # D. 超导·材料 (30-36)
    # ========================================================================
    ("# ==== Batch 8D: superconductor & materials ====",),

    # low-temperature superconductor → 低温超导体
    ("低温超级导体", "low-temperature-superconductor", "zh", "forbidden", "误译super-(超导≠超级导)：正确为 低温超导体"),

    # carbon fiber composite → 碳纤维复合材料
    ("碳纤维合成材料", "carbon-fiber-composite", "zh", "forbidden", "混淆composite/synthetic：正确为 碳纤维复合材料"),

    # vanadium alloy → 钒合金
    ("钒合金材料", "vanadium-alloy", "zh", "deprecated", "冗赘：应为 钒合金"),

    # functional material → 功能材料
    ("功能性材料", "functional-material", "zh", "deprecated", "冗赘：应为 功能材料"),

    # mixed material → 混合材料
    ("混合物质", "mixed-material", "zh", "forbidden", "误译material(材料≠物质)：正确为 混合材料"),

    # graphite → 石墨
    ("碳墨", "graphite", "zh", "forbidden", "误译graphite：正确为 石墨"),

    # siliconization → 硅化
    ("硅化处理", "siliconization", "zh", "deprecated", "冗赘：应为 硅化"),
    ("硅化作用", "siliconization", "zh", "deprecated", "非标准：应为 硅化"),

    # ========================================================================
    # E. 物理量·模式·不稳定性 (37-56)
    # ========================================================================
    ("# ==== Batch 8E: physics quantities, modes, instabilities ====",),

    # ion temperature → 离子温度
    ("离子体温度", "ion-temperature", "zh", "forbidden", "误加'体'：正确为 离子温度"),

    # electron temperature → 电子温度
    ("电子体温度", "electron-temperature", "zh", "forbidden", "误加'体'：正确为 电子温度"),

    # radiation loss → 辐射损失
    ("辐射损耗", "radiation-loss", "zh", "deprecated", "非标准：应为 辐射损失"),
    ("辐射丢失", "radiation-loss", "zh", "forbidden", "误译loss：正确为 辐射损失"),

    # Pfirsch-Schlüter current → Pfirsch-Schlüter电流
    ("普费尔施-施吕特电流", "pfirsch-schlueter-current", "zh", "forbidden", "误音译人名：正确保留 Pfirsch-Schlüter电流"),

    # Pfirsch-Schlüter regime → Pfirsch-Schlüter区
    ("普费尔施-施吕特区", "pfirsch-schlueter-regime", "zh", "forbidden", "误音译人名：正确保留 Pfirsch-Schlüter区"),

    # RSAE → 反剪切Alfvén本征模
    ("逆剪切阿尔芬本征模", "rsae", "zh", "forbidden", "误音译Alfvén+误译reverse(反剪切≠逆剪切)：正确为 反剪切Alfvén本征模"),

    # BAE → β诱导Alfvén本征模
    ("β引起的阿尔芬本征模", "bae", "zh", "forbidden", "误音译Alfvén+冗译：正确为 β诱导Alfvén本征模"),

    # D-T reaction → D-T反应
    ("氘-氚反应", "dt-reaction", "zh", "deprecated", "缩写场景应保留 D-T反应"),

    # D-D reaction → D-D反应
    ("氘-氘反应", "dd-reaction", "zh", "deprecated", "缩写场景应保留 D-D反应"),

    # D-³He reaction → D-³He反应
    ("氘-氦3反应", "d-he3-reaction", "zh", "deprecated", "缺上标：应保留 D-³He反应"),

    # Q value → Q值
    ("Q值反应", "q-value-reaction", "zh", "forbidden", "冗加'反应'：正确为 Q值"),

    # Z effective → 有效电荷数
    ("Z有效", "z-effective", "zh", "forbidden", "误译：正确为 有效电荷数"),
    ("Z效应", "z-effective", "zh", "forbidden", "误译effective：正确为 有效电荷数"),

    # super H-mode → 超级H模
    ("超H模式", "super-h-mode", "zh", "forbidden", "误译super+mode：正确为 超级H模"),

    # mix instability → 混合不稳定性
    ("混合不稳定", "mix-instability", "zh", "deprecated", "缺字'性'：应为 混合不稳定性"),

    # charge exchange loss → 电荷交换损失
    ("电荷交换丢失", "charge-exchange-loss", "zh", "forbidden", "误译loss：正确为 电荷交换损失"),

    # continuum radiation → 连续辐射
    ("连续体辐射", "continuum-radiation", "zh", "forbidden", "误译continuum(连续≠连续体)：正确为 连续辐射"),

    # turbulence spreading → 湍流扩展
    ("湍流传播", "turbulence-spreading", "zh", "forbidden", "误译spreading(扩展≠传播)：正确为 湍流扩展"),
    ("湍流蔓延", "turbulence-spreading", "zh", "forbidden", "误译spreading：正确为 湍流扩展"),

    # neutral pressure → 中性气压
    ("中性压力", "neutral-pressure", "zh", "forbidden", "误译(气压≠压力)：正确为 中性气压"),

    # vertical stability → 垂直稳定性
    ("竖直稳定性", "vertical-stability", "zh", "forbidden", "误译vertical(垂直≠竖直)：正确为 垂直稳定性"),

    # power density → 功率密度
    ("电力密度", "power-density", "zh", "forbidden", "误译power(功率≠电力)：正确为 功率密度"),

    # ========================================================================
    # F. 运行·控制·偏滤器 (57-64)
    # ========================================================================
    ("# ==== Batch 8F: operation, control, divertor ====",),

    # real-time control → 实时控制
    ("实际时间控制", "real-time-control", "zh", "forbidden", "误译real-time：正确为 实时控制"),

    # advanced divertor concept → 先进偏滤器概念
    ("高级偏滤器概念", "advanced-divertor-concept", "zh", "forbidden", "误译advanced：正确为 先进偏滤器概念"),

    # ITER to DEMO → ITER到DEMO
    ("ITER到演示", "iter-to-demo", "zh", "forbidden", "误译DEMO(专有名称)：正确保留 ITER到DEMO"),

    # gas balance → 气体平衡
    ("气态平衡", "gas-balance", "zh", "forbidden", "误译gas(气体≠气态)：正确为 气体平衡"),

    # friction force → 摩擦力
    ("摩擦力量", "friction-force", "zh", "forbidden", "冗赘force(力≠力量)：正确为 摩擦力"),

    # photon dose → 光子剂量
    ("光子量", "photon-dose", "zh", "forbidden", "缺字'剂'：正确为 光子剂量"),

    # laser energy balance → 激光能量平衡
    ("激光能量余额", "laser-energy-balance", "zh", "forbidden", "误用财务义balance：正确为 激光能量平衡"),

    # gain curve → 增益曲线
    ("增益弯曲", "gain-curve", "zh", "forbidden", "误译curve：正确为 增益曲线"),

    # ========================================================================
    # G. 数值方法·AI (66-76, skip 72)
    # ========================================================================
    ("# ==== Batch 8G: numerical methods & AI ====",),

    # finite volume method → 有限体积法
    ("有限容积法", "finite-volume-method", "zh", "deprecated", "非标准(体积≠容积)：应为 有限体积法"),

    # computational fluid dynamics → 计算流体力学
    ("计算流体动力学", "computational-fluid-dynamics", "zh", "forbidden", "误译dynamics(力学≠动力学)：正确为 计算流体力学"),

    # mesh generation → 网格生成
    ("网格产生", "mesh-generation", "zh", "deprecated", "非标准：应为 网格生成"),

    # full-f method → 全f方法
    ("完全f方法", "full-f-method", "zh", "forbidden", "误译full(全≠完全)：正确为 全f方法"),

    # Bayesian inference → 贝叶斯推断
    ("贝叶斯推理", "bayesian-inference", "zh", "forbidden", "误译inference(推断≠推理)：正确为 贝叶斯推断"),

    # uncertainty quantification → 不确定性量化
    ("不确定度量化", "uncertainty-quantification", "zh", "forbidden", "误译uncertainty(不确定性≠不确定度)：正确为 不确定性量化"),

    # learning rate → 学习率 (reactor economics context)
    ("学习速率", "learning-rate", "zh", "deprecated", "堆经济语境非标准：应为 学习率"),

    # supply chain → 供应链
    ("供给链", "supply-chain", "zh", "forbidden", "误译supply(供应≠供给)：正确为 供应链"),

    # pipe cutting → 管道切割
    ("管子切割", "pipe-cutting", "zh", "forbidden", "误译pipe(管道≠管子)：正确为 管道切割"),

    # remote inspection → 远程检测
    ("远程检查", "remote-inspection", "zh", "deprecated", "非标准：应为 远程检测"),

    # ========================================================================
    # H. 工程·经济·辅助 (77-88, skip 86)
    # ========================================================================
    ("# ==== Batch 8H: engineering & BOP ====",),

    # thermal efficiency → 热效率
    ("热力效率", "thermal-efficiency", "zh", "forbidden", "误译thermal(热≠热力)：正确为 热效率"),

    # thermal power → 热功率
    # NOTE: '热力' skipped — already preferred alias of thermal-force

    # power supply → 电源系统
    ("电力供应", "power-supply", "zh", "forbidden", "误译power supply：正确为 电源系统"),
    ("供电", "power-supply", "zh", "deprecated", "过度简化：应为 电源系统"),

    # water treatment → 水处理系统
    ("水处理", "water-treatment", "zh", "deprecated", "缺字'系统'：应为 水处理系统"),

    # HVAC → 暖通空调
    ("加热通风空调", "hvac", "zh", "forbidden", "啰嗦译法：正确为 暖通空调"),

    # cooling tower → 冷却塔
    ("冷却水塔", "cooling-tower", "zh", "forbidden", "误译：正确为 冷却塔"),

    # scheduled maintenance → 计划维护
    ("定期维护", "scheduled-maintenance", "zh", "forbidden", "误译scheduled(计划≠定期)：正确为 计划维护"),
    ("预定维护", "scheduled-maintenance", "zh", "forbidden", "误译scheduled：正确为 计划维护"),

    # workflow automation → 工作流自动化
    ("工作流程自动化", "workflow-automation", "zh", "deprecated", "冗赘(流≠流程)：应为 工作流自动化"),

    # rotating magnetic field → 旋转磁场
    ("转动磁场", "rotating-magnetic-field", "zh", "deprecated", "非标准：应为 旋转磁场"),

    # ICRF antenna → 离子回旋天线
    ("ICRF天线", "icrf-antenna", "zh", "deprecated", "非标准缩写：应为 离子回旋天线"),
    ("离子回旋共振天线", "icrf-antenna", "zh", "forbidden", "冗赘(回旋已含共振义)：正确为 离子回旋天线"),

    # large helical device → 大型螺旋装置
    ("大螺旋装置", "large-helical-device", "zh", "forbidden", "缺字'型'：正确为 大型螺旋装置"),
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
