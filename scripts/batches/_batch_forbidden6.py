#!/usr/bin/env python3
"""Batch 6: forbidden/deprecated aliases for AI mistranslations (next ~100 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 等离子体物理·运行模式 (1-15)
    # ========================================================================
    ("# ==== Batch 6A: plasma physics & operation modes ====",),
    # hybrid scenario → 混合运行模式
    (
        "混合场景",
        "hybrid-scenario",
        "zh",
        "forbidden",
        "误译scenario：正确为 混合运行模式",
    ),
    (
        "混合方案",
        "hybrid-scenario",
        "zh",
        "forbidden",
        "误译scenario：正确为 混合运行模式",
    ),
    # steady-state operation → 稳态运行
    (
        "稳定状态操作",
        "steady-state-operation",
        "zh",
        "forbidden",
        "误译：正确为 稳态运行",
    ),
    # inductive operation → 感应运行
    (
        "电感运行",
        "inductive-operation",
        "zh",
        "forbidden",
        "误译inductive：正确为 感应运行",
    ),
    (
        "归纳运行",
        "inductive-operation",
        "zh",
        "forbidden",
        "误译inductive：正确为 感应运行",
    ),
    # non-inductive operation → 非感应运行
    (
        "非电感运行",
        "non-inductive-operation",
        "zh",
        "forbidden",
        "误译inductive：正确为 非感应运行",
    ),
    # plasma confinement → 等离子体约束
    (
        "等离子体限制",
        "plasma-confinement",
        "zh",
        "forbidden",
        "误译confinement：正确为 等离子体约束",
    ),
    (
        "等离子体封闭",
        "plasma-confinement",
        "zh",
        "forbidden",
        "误译confinement：正确为 等离子体约束",
    ),
    # plasma equilibrium → 等离子体平衡
    (
        "等离子体均衡",
        "plasma-equilibrium",
        "zh",
        "forbidden",
        "误译equilibrium：正确为 等离子体平衡",
    ),
    # plasma ramp-up → 等离子体升流
    (
        "等离子体升坡",
        "plasma-ramp-up",
        "zh",
        "forbidden",
        "误译ramp-up：正确为 等离子体升流",
    ),
    (
        "等离子体斜升",
        "plasma-ramp-up",
        "zh",
        "forbidden",
        "误译ramp-up：正确为 等离子体升流",
    ),
    # plasma ramp-down → 等离子体降流
    (
        "等离子体降坡",
        "plasma-ramp-down",
        "zh",
        "forbidden",
        "误译ramp-down：正确为 等离子体降流",
    ),
    (
        "等离子体斜降",
        "plasma-ramp-down",
        "zh",
        "forbidden",
        "误译ramp-down：正确为 等离子体降流",
    ),
    # stored energy → 等离子体储能
    ("存储能量", "stored-energy", "zh", "forbidden", "误译：正确为 等离子体储能"),
    # ignition → 点火
    ("点燃", "ignition", "zh", "forbidden", "误译ignition(聚变义)：正确为 点火"),
    ("引燃", "ignition", "zh", "forbidden", "误译ignition(聚变义)：正确为 点火"),
    # ignition temperature → 点火温度
    (
        "燃点",
        "ignition-temperature",
        "zh",
        "forbidden",
        "误译(化学义)：聚变应为 点火温度",
    ),
    # extended MHD → 扩展MHD
    ("延伸MHD", "extended-mhd", "zh", "forbidden", "误译extended：正确为 扩展MHD"),
    # MHD stability limit → MHD稳定极限
    (
        "MHD稳定性限制",
        "mhd-stability-limit",
        "zh",
        "forbidden",
        "误译limit：正确为 MHD稳定极限",
    ),
    # hot-ion mode → 热离子模式
    ("热离子模", "hot-ion-mode", "zh", "deprecated", "缺字'式'：应为 热离子模式"),
    # plasma rotation → 等离子体旋转
    (
        "等离子旋转",
        "plasma-rotation",
        "zh",
        "forbidden",
        "缺字'体'：正确为 等离子体旋转",
    ),
    (
        "等离子体转动",
        "plasma-rotation",
        "zh",
        "deprecated",
        "非标准：应为 等离子体旋转",
    ),
    # ========================================================================
    # B. 波·加热·电流驱动·数理 (16-30)
    # ========================================================================
    ("# ==== Batch 6B: waves, heating, math-physics ====",),
    # electron Bernstein wave → 电子伯恩斯坦波
    (
        "电子伯恩斯坦波动",
        "electron-bernstein-wave",
        "zh",
        "forbidden",
        "误加'动'：正确为 电子伯恩斯坦波",
    ),
    # ion Bernstein wave → 离子伯恩斯坦波
    (
        "离子伯恩斯坦波动",
        "ion-bernstein-wave",
        "zh",
        "forbidden",
        "误加'动'：正确为 离子伯恩斯坦波",
    ),
    # nonlinear coupling → 非线性耦合
    (
        "非线性联接",
        "nonlinear-coupling",
        "zh",
        "forbidden",
        "误译coupling：正确为 非线性耦合",
    ),
    (
        "非线性联结",
        "nonlinear-coupling",
        "zh",
        "forbidden",
        "误译coupling：正确为 非线性耦合",
    ),
    # wave absorption → 波吸收
    ("波吸附", "wave-absorption", "zh", "forbidden", "误译absorption：正确为 波吸收"),
    # full-wave simulation → 全波模拟
    ("全波仿真", "full-wave-simulation", "zh", "deprecated", "非标准：应为 全波模拟"),
    # N-parallel → 平行折射率
    ("N平行", "n-parallel", "zh", "forbidden", "误译：正确为 平行折射率"),
    # ray tracing → 射线追踪
    (
        "光线追踪",
        "ray-tracing",
        "zh",
        "forbidden",
        "误译ray(计算机图形学义)：正确为 射线追踪",
    ),
    # collisional damping → 碰撞阻尼
    (
        "碰撞衰减",
        "collisional-damping",
        "zh",
        "forbidden",
        "误译damping：正确为 碰撞阻尼",
    ),
    (
        "碰撞减振",
        "collisional-damping",
        "zh",
        "forbidden",
        "误译damping：正确为 碰撞阻尼",
    ),
    # continuum kinetic → 连续谱动理学
    (
        "连续动力学",
        "continuum-kinetic",
        "zh",
        "forbidden",
        "误译kinetic：正确为 连续谱动理学",
    ),
    (
        "连续谱运动学",
        "continuum-kinetic",
        "zh",
        "forbidden",
        "误译kinetic：正确为 连续谱动理学",
    ),
    # Fokker-Planck equation → Fokker-Planck方程
    (
        "福克尔-普朗克方程",
        "fokker-planck-equation",
        "zh",
        "forbidden",
        "误音译人名：正确保留 Fokker-Planck方程",
    ),
    # Vlasov equation → Vlasov方程
    (
        "弗拉索夫方程",
        "vlasov-equation",
        "zh",
        "forbidden",
        "误音译人名：正确保留 Vlasov方程",
    ),
    # reaction rate coefficient → 反应速率系数
    (
        "反应率系数",
        "reaction-rate-coefficient",
        "zh",
        "deprecated",
        "缺字'速'：应为 反应速率系数",
    ),
    # cross section → 截面
    ("横截面", "cross-section", "zh", "forbidden", "误译(几何义)：核物理应为 截面"),
    ("横断面", "cross-section", "zh", "forbidden", "误译(几何义)：核物理应为 截面"),
    # Coulomb barrier → 库仑势垒
    ("库仑障碍", "coulomb-barrier", "zh", "forbidden", "误译barrier：正确为 库仑势垒"),
    # particle-in-cell → 粒子网格法
    (
        "粒子内胞法",
        "particle-in-cell",
        "zh",
        "forbidden",
        "误译in-cell：正确为 粒子网格法",
    ),
    ("粒子池法", "particle-in-cell", "zh", "forbidden", "误译：正确为 粒子网格法"),
    # ========================================================================
    # C. 磁场·几何·对称性 (31-42)
    # ========================================================================
    ("# ==== Batch 6C: magnetic geometry & symmetry ====",),
    # magnetic helicity → 磁螺旋度
    ("磁螺旋", "magnetic-helicity", "zh", "forbidden", "缺字'度'：正确为 磁螺旋度"),
    # magnetic axis → 磁轴
    ("磁性轴", "magnetic-axis", "zh", "forbidden", "误译magnetic：正确为 磁轴"),
    # magnetic self-organization → 磁自组织
    (
        "磁性自我组织",
        "magnetic-self-organization",
        "zh",
        "forbidden",
        "误译：正确为 磁自组织",
    ),
    # magnetic nozzle → 磁喷管
    ("磁性喷嘴", "magnetic-nozzle", "zh", "forbidden", "误译nozzle：正确为 磁喷管"),
    # flux expansion → 磁通膨胀
    (
        "通量扩张",
        "flux-expansion",
        "zh",
        "forbidden",
        "误译flux+expansion：正确为 磁通膨胀",
    ),
    ("磁通扩张", "flux-expansion", "zh", "forbidden", "误译expansion：正确为 磁通膨胀"),
    # flux amplification → 磁通放大
    ("通量放大", "flux-amplification", "zh", "forbidden", "误译flux：正确为 磁通放大"),
    # flux conserver → 磁通守恒器
    (
        "磁通保守器",
        "flux-conserver",
        "zh",
        "forbidden",
        "误译conserver：正确为 磁通守恒器",
    ),
    # flux confinement → 磁通约束
    (
        "通量限制",
        "flux-confinement",
        "zh",
        "forbidden",
        "误译flux+confinement：正确为 磁通约束",
    ),
    # quasi-axisymmetry → 准轴对称
    ("拟轴对称", "quasi-axisymmetry", "zh", "deprecated", "非标准：应为 准轴对称"),
    # quasi-helical symmetry → 准螺旋对称
    (
        "拟螺旋对称",
        "quasi-helical-symmetry",
        "zh",
        "deprecated",
        "非标准：应为 准螺旋对称",
    ),
    # quasi-isodynamic → 准等动力
    ("准等动态", "quasi-isodynamic", "zh", "forbidden", "误译：正确为 准等动力"),
    # modular coil → 模块化线圈
    ("模块线圈", "modular-coil", "zh", "deprecated", "缺字'化'：应为 模块化线圈"),
    # ========================================================================
    # D. 偏滤器·SOL·粒子 (43-58)
    # ========================================================================
    ("# ==== Batch 6D: divertor, SOL, particles ====",),
    # divertor baffle → 偏滤器挡板
    (
        "偏滤器障板",
        "divertor-baffle",
        "zh",
        "forbidden",
        "误译baffle：正确为 偏滤器挡板",
    ),
    (
        "分流器挡板",
        "divertor-baffle",
        "zh",
        "forbidden",
        "误译divertor：正确为 偏滤器挡板",
    ),
    # divertor heat flux → 偏滤器热负荷
    (
        "偏滤器热通量",
        "divertor-heat-flux",
        "zh",
        "forbidden",
        "误译heat flux：正确为 偏滤器热负荷",
    ),
    # divertor replacement → 偏滤器更换
    (
        "偏滤器替换",
        "divertor-replacement",
        "zh",
        "deprecated",
        "非标准：应为 偏滤器更换",
    ),
    # Super-X divertor → Super-X偏滤器
    (
        "超X偏滤器",
        "super-x-divertor",
        "zh",
        "forbidden",
        "误译Super：正确保留 Super-X偏滤器",
    ),
    # liquid metal divertor → 液态金属偏滤器
    (
        "液体金属偏滤器",
        "liquid-metal-divertor",
        "zh",
        "forbidden",
        "误译liquid：正确为 液态金属偏滤器",
    ),
    # passing particle → 通行粒子
    ("经过粒子", "passing-particle", "zh", "forbidden", "误译passing：正确为 通行粒子"),
    ("路过粒子", "passing-particle", "zh", "forbidden", "误译passing：正确为 通行粒子"),
    # orbit loss → 轨道损失
    ("轨道丢失", "orbit-loss", "zh", "forbidden", "误译loss：正确为 轨道损失"),
    # prompt loss → 瞬时损失
    ("快速损失", "prompt-loss", "zh", "forbidden", "误译prompt：正确为 瞬时损失"),
    # energetic particle → 高能粒子
    (
        "能量粒子",
        "energetic-particle",
        "zh",
        "forbidden",
        "误译energetic：正确为 高能粒子",
    ),
    # wall pumping → 壁抽气效应
    ("壁泵送", "wall-pumping", "zh", "forbidden", "误译pumping：正确为 壁抽气效应"),
    # outgassing → 出气
    ("放气", "outgassing", "zh", "deprecated", "非标准：应为 出气"),
    # base pressure → 本底气压
    ("基础气压", "base-pressure", "zh", "forbidden", "误译base：正确为 本底气压"),
    (
        "基底压力",
        "base-pressure",
        "zh",
        "forbidden",
        "误译base+pressure：正确为 本底气压",
    ),
    # pedestal width → 基座宽度
    ("底座宽度", "pedestal-width", "zh", "forbidden", "误译pedestal：正确为 基座宽度"),
    ("台座宽度", "pedestal-width", "zh", "forbidden", "误译pedestal：正确为 基座宽度"),
    # pressure pedestal → 压力基座
    (
        "压力底座",
        "pressure-pedestal",
        "zh",
        "forbidden",
        "误译pedestal：正确为 压力基座",
    ),
    (
        "压力台座",
        "pressure-pedestal",
        "zh",
        "forbidden",
        "误译pedestal：正确为 压力基座",
    ),
    # temperature pedestal → 温度基座
    (
        "温度底座",
        "temperature-pedestal",
        "zh",
        "forbidden",
        "误译pedestal：正确为 温度基座",
    ),
    # SOL width → SOL宽度
    ("刮削层宽", "sol-width", "zh", "deprecated", "缺规范性：应为 SOL宽度"),
    # ========================================================================
    # E. 中子·辐射防护·安全 (59-72)
    # ========================================================================
    ("# ==== Batch 6E: neutronics, radiation protection, safety ====",),
    # activation analysis → 活化分析
    (
        "激活分析",
        "activation-analysis",
        "zh",
        "forbidden",
        "误译activation：正确为 活化分析",
    ),
    # activation foil → 活化箔
    ("激活箔片", "activation-foil", "zh", "forbidden", "误译activation：正确为 活化箔"),
    ("激活箔", "activation-foil", "zh", "forbidden", "误译activation：正确为 活化箔"),
    # effective dose → 有效剂量
    ("有效的剂量", "effective-dose", "zh", "forbidden", "语法错：正确为 有效剂量"),
    # public exposure → 公众照射
    ("公众暴露", "public-exposure", "zh", "forbidden", "误译exposure：正确为 公众照射"),
    # high-level waste → 高放废物
    ("高水平废物", "high-level-waste", "zh", "forbidden", "误译level：正确为 高放废物"),
    ("高放射性废物", "high-level-waste", "zh", "deprecated", "非标准：应为 高放废物"),
    # intermediate-level waste → 中放废物
    (
        "中水平废物",
        "intermediate-level-waste",
        "zh",
        "forbidden",
        "误译level：正确为 中放废物",
    ),
    (
        "中放射性废物",
        "intermediate-level-waste",
        "zh",
        "deprecated",
        "非标准：应为 中放废物",
    ),
    # low-level waste → 低放废物
    ("低水平废物", "low-level-waste", "zh", "forbidden", "误译level：正确为 低放废物"),
    ("低放射性废物", "low-level-waste", "zh", "deprecated", "非标准：应为 低放废物"),
    # waste classification → 废物分级
    (
        "废物分类",
        "waste-classification",
        "zh",
        "forbidden",
        "误译classification(分级≠分类)：正确为 废物分级",
    ),
    # ALARA → 合理可行尽量低
    ("阿拉拉", "alara", "zh", "forbidden", "误音译缩写：正确展开为 合理可行尽量低"),
    # derived air concentration → 导出空气浓度
    (
        "衍生空气浓度",
        "derived-air-concentration",
        "zh",
        "forbidden",
        "误译derived：正确为 导出空气浓度",
    ),
    # in-vessel LOCA → 真空室内失冷事故
    (
        "容器内LOCA",
        "in-vessel-loca",
        "zh",
        "forbidden",
        "误译vessel：正确为 真空室内失冷事故",
    ),
    # ex-vessel LOCA → 真空室外失冷事故
    (
        "容器外LOCA",
        "ex-vessel-loca",
        "zh",
        "forbidden",
        "误译vessel：正确为 真空室外失冷事故",
    ),
    # decommissioning cost → 退役费用
    ("退役成本", "decommissioning-cost", "zh", "deprecated", "非标准：应为 退役费用"),
    # hydrogen safety → 氢安全
    ("氢气安全", "hydrogen-safety", "zh", "deprecated", "非标准：应为 氢安全"),
    # ========================================================================
    # F. 材料·包层·冷却·制造 (73-85)
    # ========================================================================
    ("# ==== Batch 6F: materials, blanket, cooling ====",),
    # liquid metal coolant → 液态金属冷却剂
    (
        "液体金属冷却剂",
        "liquid-metal-coolant",
        "zh",
        "forbidden",
        "误译liquid：正确为 液态金属冷却剂",
    ),
    # lithium coating → 锂涂覆
    (
        "锂涂层",
        "lithium-coating",
        "zh",
        "deprecated",
        "非标准(coating→涂覆≠涂层)：应为 锂涂覆",
    ),
    # lithium wall → 锂壁
    ("锂墙", "lithium-wall", "zh", "forbidden", "误译wall：正确为 锂壁"),
    # TCAP → 热循环吸收工艺
    ("热循环吸收过程", "tcap", "zh", "forbidden", "误译process：正确为 热循环吸收工艺"),
    # tritium plant → 氚工厂
    ("氚厂", "tritium-plant", "zh", "deprecated", "缩略非标准：应为 氚工厂"),
    # vacuum pumping → 真空抽气
    ("真空泵送", "vacuum-pumping", "zh", "forbidden", "误译pumping：正确为 真空抽气"),
    # thermal shock → 热冲击
    ("热震", "thermal-shock", "zh", "deprecated", "非标准：应为 热冲击"),
    ("热休克", "thermal-shock", "zh", "forbidden", "误用医学义：正确为 热冲击"),
    # thermal force → 热力
    ("热力学力", "thermal-force", "zh", "forbidden", "误译：正确为 热力"),
    # power deposition profile → 功率沉积分布
    (
        "功率沉积剖面",
        "power-deposition-profile",
        "zh",
        "deprecated",
        "非标准：应为 功率沉积分布",
    ),
    # power degradation → 功率退化
    (
        "功率降解",
        "power-degradation",
        "zh",
        "forbidden",
        "误译degradation：正确为 功率退化",
    ),
    # FRC merging → 场反并合
    ("FRC合并", "frc-merging", "zh", "forbidden", "误译merging：正确为 场反并合"),
    # spheromak merging → 球马克并合
    (
        "球马克合并",
        "spheromak-merging",
        "zh",
        "forbidden",
        "误译merging：正确为 球马克并合",
    ),
    # compact toroid injection → 紧凑环注入
    (
        "紧凑环面注入",
        "compact-toroid-injection",
        "zh",
        "forbidden",
        "误译toroid(环≠环面)：正确为 紧凑环注入",
    ),
    # ========================================================================
    # G. 诊断·建模·控制 (86-93)
    # ========================================================================
    ("# ==== Batch 6G: diagnostics, modeling, control ====",),
    # magnetic diagnostics → 磁诊断
    (
        "磁性诊断",
        "magnetic-diagnostics",
        "zh",
        "forbidden",
        "误译magnetic：正确为 磁诊断",
    ),
    # impurity spectroscopy → 杂质光谱
    (
        "杂质光谱学",
        "impurity-spectroscopy",
        "zh",
        "deprecated",
        "非标准：应为 杂质光谱",
    ),
    # integrated modeling → 集成建模
    (
        "集成模型",
        "integrated-modeling",
        "zh",
        "forbidden",
        "误译modeling(动词义)：正确为 集成建模",
    ),
    ("一体化模型", "integrated-modeling", "zh", "forbidden", "误译：正确为 集成建模"),
    # surrogate model → 代理模型
    (
        "替代模型",
        "surrogate-model",
        "zh",
        "forbidden",
        "误译surrogate：正确为 代理模型",
    ),
    # digital twin → 数字孪生
    ("数字双胞胎", "digital-twin", "zh", "forbidden", "误译twin：正确为 数字孪生"),
    # shape control → 形状控制
    ("造型控制", "shape-control", "zh", "forbidden", "误译shape：正确为 形状控制"),
    # gap control → 间隙控制
    ("间距控制", "gap-control", "zh", "forbidden", "误译gap：正确为 间隙控制"),
    # slowing-down time → 滑脱时间
    (
        "减速时间",
        "slowing-down-time",
        "zh",
        "forbidden",
        "误译slowing-down：正确为 滑脱时间",
    ),
    # ========================================================================
    # H. 堆设计·经济·先进概念 (94-100)
    # ========================================================================
    ("# ==== Batch 6H: reactor design, economics, advanced ====",),
    # prototype reactor → 原型堆
    ("原型反应堆", "prototype-reactor", "zh", "deprecated", "非标准：应为 原型堆"),
    # nth-of-a-kind → 第N台堆
    ("第N种", "nth-of-a-kind", "zh", "forbidden", "误译：正确为 第N台堆"),
    # fusion gain → 聚变增益因子
    # NOTE: '聚变增益' skipped — already alias of energy-gain
    # fusion roadmap → 聚变路线图
    ("聚变路标", "fusion-roadmap", "zh", "forbidden", "误译roadmap：正确为 聚变路线图"),
    # regulatory approval → 审批许可
    ("监管批准", "regulatory-approval", "zh", "forbidden", "误译：正确为 审批许可"),
    # synchrotron radiation → 同步辐射
    (
        "同步加速器辐射",
        "synchrotron-radiation",
        "zh",
        "forbidden",
        "啰嗦/误译：正确为 同步辐射",
    ),
    # spin-polarized fuel → 自旋极化燃料
    (
        "自旋偏振燃料",
        "spin-polarized-fuel",
        "zh",
        "forbidden",
        "误译polarized：正确为 自旋极化燃料",
    ),
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
