#!/usr/bin/env python3
"""Batch 3: forbidden/deprecated aliases for AI mistranslations (next 100 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 运行模式与等离子体物理 (1-20)
    # ========================================================================
    ("# ==== Batch 3A: operation modes & plasma physics ====",),
    # confinement scaling law → 约束标度律
    (
        "约束缩放律",
        "confinement-scaling",
        "zh",
        "forbidden",
        "误译scaling：正确为 约束标度律",
    ),
    (
        "封闭标度律",
        "confinement-scaling",
        "zh",
        "forbidden",
        "误译confinement：正确为 约束标度律",
    ),
    # internal transport barrier → 内输运垒
    (
        "内部传输屏障",
        "internal-transport-barrier",
        "zh",
        "forbidden",
        "误译transport+barrier：正确为 内输运垒",
    ),
    (
        "内部输运屏障",
        "internal-transport-barrier",
        "zh",
        "forbidden",
        "误译barrier：正确为 内输运垒",
    ),
    # edge transport barrier → 边缘输运垒
    (
        "边缘传输屏障",
        "edge-transport-barrier",
        "zh",
        "forbidden",
        "误译transport+barrier：正确为 边缘输运垒",
    ),
    (
        "边缘输运屏障",
        "edge-transport-barrier",
        "zh",
        "forbidden",
        "误译barrier：正确为 边缘输运垒",
    ),
    # transport barrier → 输运垒
    (
        "传输屏障",
        "transport-barrier",
        "zh",
        "forbidden",
        "误译transport+barrier：正确为 输运垒",
    ),
    ("输运屏障", "transport-barrier", "zh", "forbidden", "误译barrier：正确为 输运垒"),
    # density peaking → 密度峰化
    (
        "密度峰值化",
        "density-peaking",
        "zh",
        "forbidden",
        "误译peaking：正确为 密度峰化",
    ),
    ("密度尖化", "density-peaking", "zh", "forbidden", "误译peaking：正确为 密度峰化"),
    # peeling-ballooning mode → 剥离-气球模
    (
        "剥皮-气球模式",
        "peeling-ballooning-mode",
        "zh",
        "forbidden",
        "误译peeling+mode：正确为 剥离-气球模",
    ),
    (
        "剥离-膨胀模",
        "peeling-ballooning-mode",
        "zh",
        "forbidden",
        "误译ballooning：正确为 剥离-气球模",
    ),
    (
        "剥离-气球模式",
        "peeling-ballooning-mode",
        "zh",
        "deprecated",
        "非标准：应为 剥离-气球模",
    ),
    # resistive wall mode → 电阻壁模
    ("阻性壁模式", "resistive-wall-mode", "zh", "deprecated", "非标准：应为 电阻壁模"),
    ("电阻墙模", "resistive-wall-mode", "zh", "forbidden", "误译wall：正确为 电阻壁模"),
    ("电阻壁模式", "resistive-wall-mode", "zh", "deprecated", "非标准：应为 电阻壁模"),
    # energetic particle mode → 高能粒子模
    (
        "高能粒子模式",
        "energetic-particle-mode",
        "zh",
        "deprecated",
        "非标准：应为 高能粒子模",
    ),
    # fishbone instability → 鱼骨模不稳定性
    (
        "鱼刺不稳定性",
        "fishbone-instability",
        "zh",
        "forbidden",
        "误译fishbone：正确为 鱼骨模不稳定性",
    ),
    (
        "鱼骨不稳定性",
        "fishbone-instability",
        "zh",
        "deprecated",
        "缺字'模'：应为 鱼骨模不稳定性",
    ),
    # geodesic acoustic mode → 测地声模
    (
        "大地声波模式",
        "geodesic-acoustic-mode",
        "zh",
        "forbidden",
        "误译geodesic：正确为 测地声模",
    ),
    (
        "测地声模式",
        "geodesic-acoustic-mode",
        "zh",
        "deprecated",
        "非标准：应为 测地声模",
    ),
    (
        "测地声学模",
        "geodesic-acoustic-mode",
        "zh",
        "deprecated",
        "非标准：应为 测地声模",
    ),
    # resonant magnetic perturbation → 共振磁扰动
    (
        "谐振磁扰动",
        "resonant-magnetic-perturbation",
        "zh",
        "forbidden",
        "误译resonant：聚变应为 共振磁扰动",
    ),
    # reversed field pinch → 反场箍缩
    (
        "反向场收缩",
        "reversed-field-pinch",
        "zh",
        "forbidden",
        "误译pinch：正确为 反场箍缩",
    ),
    (
        "反场收缩",
        "reversed-field-pinch",
        "zh",
        "forbidden",
        "误译pinch：正确为 反场箍缩",
    ),
    # reversed shear → 反磁剪切
    ("反向剪切", "reversed-shear", "zh", "forbidden", "缺字'磁'：正确为 反磁剪切"),
    # L-H transition → L-H转换
    ("LH过渡", "l-h-transition", "zh", "forbidden", "误译+格式错：正确为 L-H转换"),
    ("L到H转变", "l-h-transition", "zh", "deprecated", "非标准：应为 L-H转换"),
    # quiescent H-mode → 静默H模
    (
        "平静H模式",
        "quiescent-h-mode",
        "zh",
        "forbidden",
        "误译quiescent+mode：正确为 静默H模",
    ),
    ("安静H模", "quiescent-h-mode", "zh", "forbidden", "误译quiescent：正确为 静默H模"),
    # plasma sustainment → 等离子体维持
    (
        "等离子体维护",
        "plasma-sustainment",
        "zh",
        "forbidden",
        "误译sustainment：正确为 等离子体维持",
    ),
    # fully non-inductive operation → 完全非感应运行
    (
        "完全非电感运行",
        "fully-non-inductive",
        "zh",
        "forbidden",
        "误译inductive：正确为 完全非感应运行",
    ),
    # intrinsic rotation → 本征旋转
    (
        "内在旋转",
        "intrinsic-rotation",
        "zh",
        "forbidden",
        "误译intrinsic：正确为 本征旋转",
    ),
    ("固有旋转", "intrinsic-rotation", "zh", "deprecated", "非标准：应为 本征旋转"),
    # profile stiffness → 剖面刚性
    (
        "剖面僵硬度",
        "profile-stiffness",
        "zh",
        "forbidden",
        "误译stiffness：正确为 剖面刚性",
    ),
    (
        "分布刚度",
        "profile-stiffness",
        "zh",
        "forbidden",
        "误译profile：正确为 剖面刚性",
    ),
    # radiation collapse → 辐射坍塌
    ("辐射塌缩", "radiation-collapse", "zh", "deprecated", "非标准：应为 辐射坍塌"),
    (
        "辐射崩溃",
        "radiation-collapse",
        "zh",
        "forbidden",
        "误译collapse：正确为 辐射坍塌",
    ),
    # ========================================================================
    # B. 加热·波·电流驱动 (21-35)
    # ========================================================================
    ("# ==== Batch 3B: heating, waves, current drive ====",),
    # ECCD → 电子回旋电流驱动
    (
        "电子环回电流驱动",
        "eccd",
        "zh",
        "forbidden",
        "误译cyclotron：正确为 电子回旋电流驱动",
    ),
    # mode conversion → 模式转换
    ("模态转换", "mode-conversion", "zh", "forbidden", "误译mode：聚变应为 模式转换"),
    # minority heating → 少数粒子加热
    (
        "少数派加热",
        "minority-heating",
        "zh",
        "forbidden",
        "误译minority：正确为 少数粒子加热",
    ),
    (
        "少量加热",
        "minority-heating",
        "zh",
        "forbidden",
        "误译minority：正确为 少数粒子加热",
    ),
    # harmonic heating → 谐波加热
    (
        "谐振加热",
        "harmonic-heating",
        "zh",
        "forbidden",
        "误译harmonic：正确为 谐波加热",
    ),
    # fast wave → 快波
    ("快速波", "fast-wave", "zh", "deprecated", "非标准：应为 快波"),
    # slow wave → 慢波
    ("缓慢波", "slow-wave", "zh", "forbidden", "误译slow：正确为 慢波"),
    # helicon current drive → 螺旋波电流驱动
    (
        "赫利孔电流驱动",
        "helicon-current-drive",
        "zh",
        "forbidden",
        "误音译helicon：正确为 螺旋波电流驱动",
    ),
    (
        "螺旋子电流驱动",
        "helicon-current-drive",
        "zh",
        "forbidden",
        "误译helicon：正确为 螺旋波电流驱动",
    ),
    # negative ion source → 负离子源
    (
        "阴离子源",
        "negative-ion-source",
        "zh",
        "forbidden",
        "误译negative：聚变应为 负离子源",
    ),
    # parametric instability → 参数不稳定性
    (
        "参量不稳定性",
        "parametric-instability",
        "zh",
        "deprecated",
        "非标准变体：应为 参数不稳定性",
    ),
    # multipactor → 二次电子倍增放电
    (
        "多路放电",
        "multipactor",
        "zh",
        "forbidden",
        "误译multipactor：正确为 二次电子倍增放电",
    ),
    (
        "多重放电",
        "multipactor",
        "zh",
        "forbidden",
        "误译multipactor：正确为 二次电子倍增放电",
    ),
    # antenna coupling → 天线耦合
    (
        "天线连接",
        "antenna-coupling",
        "zh",
        "forbidden",
        "误译coupling：正确为 天线耦合",
    ),
    (
        "天线配对",
        "antenna-coupling",
        "zh",
        "forbidden",
        "误译coupling：正确为 天线耦合",
    ),
    # antenna loading → 天线负载
    ("天线加载", "antenna-loading", "zh", "forbidden", "误译loading：正确为 天线负载"),
    # helicity injection → 螺旋度注入
    (
        "螺旋注入",
        "helicity-injection",
        "zh",
        "forbidden",
        "缺字'度'：正确为 螺旋度注入",
    ),
    # ========================================================================
    # C. 诊断·数据·控制 (36-45)
    # ========================================================================
    ("# ==== Batch 3C: diagnostics, data, control ====",),
    # Doppler backscattering → 多普勒背散射
    (
        "多普勒反向散射",
        "doppler-backscattering",
        "zh",
        "forbidden",
        "误译back-：正确为 多普勒背散射",
    ),
    # Doppler broadening → 多普勒展宽
    (
        "多普勒增宽",
        "doppler-broadening",
        "zh",
        "forbidden",
        "误译broadening：正确为 多普勒展宽",
    ),
    # Stark broadening → 斯塔克展宽
    (
        "斯塔克增宽",
        "stark-broadening",
        "zh",
        "forbidden",
        "误译broadening：正确为 斯塔克展宽",
    ),
    # synthetic diagnostics → 合成诊断
    (
        "综合诊断",
        "synthetic-diagnostics",
        "zh",
        "forbidden",
        "误译synthetic：正确为 合成诊断",
    ),
    (
        "人工诊断",
        "synthetic-diagnostics",
        "zh",
        "forbidden",
        "误译synthetic：正确为 合成诊断",
    ),
    # model predictive control → 模型预测控制
    (
        "模型预判控制",
        "model-predictive-control",
        "zh",
        "forbidden",
        "误译predictive：正确为 模型预测控制",
    ),
    # Mirnov coil → 米尔诺夫线圈
    ("米尔诺夫圈", "mirnov-coil", "zh", "forbidden", "缺字'线'：正确为 米尔诺夫线圈"),
    # Rogowski coil → 罗戈夫斯基线圈
    (
        "罗科夫斯基线圈",
        "rogowski-coil",
        "zh",
        "forbidden",
        "音译错：正确为 罗戈夫斯基线圈",
    ),
    (
        "罗戈斯基线圈",
        "rogowski-coil",
        "zh",
        "deprecated",
        "音译变体：应为 罗戈夫斯基线圈",
    ),
    # diamagnetic loop → 抗磁环
    ("反磁环", "diamagnetic-loop", "zh", "forbidden", "误译dia-：正确为 抗磁环"),
    ("逆磁环", "diamagnetic-loop", "zh", "forbidden", "误译dia-：正确为 抗磁环"),
    # phase contrast imaging → 相衬成像
    (
        "相位对比成像",
        "phase-contrast-imaging",
        "zh",
        "forbidden",
        "误译contrast：正确为 相衬成像",
    ),
    # IR thermography → 红外热成像
    ("红外热图法", "ir-thermography", "zh", "deprecated", "非标准：应为 红外热成像"),
    # ========================================================================
    # D. 堆工程·结构·系统 (46-60)
    # ========================================================================
    ("# ==== Batch 3D: reactor engineering & systems ====",),
    # thermal shield → 冷屏
    # (skip: 热屏蔽 already exists as alias)
    ("热防护罩", "thermal-shield", "zh", "forbidden", "误译：聚变低温术语正确为 冷屏"),
    # equatorial port → 赤道窗口
    ("赤道端口", "equatorial-port", "zh", "forbidden", "误译port：聚变应为 赤道窗口"),
    # maintenance port → 维护窗口
    ("维护端口", "maintenance-port", "zh", "forbidden", "误译port：聚变应为 维护窗口"),
    # divertor dome → 偏滤器穹顶
    ("偏滤器圆顶", "divertor-dome", "zh", "forbidden", "误译dome：正确为 偏滤器穹顶"),
    # divertor target → 偏滤器靶板
    (
        "偏滤器目标",
        "divertor-target",
        "zh",
        "forbidden",
        "误译target：聚变应为 偏滤器靶板",
    ),
    # divertor pumping → 偏滤器抽气
    ("偏滤器泵抽", "divertor-pumping", "zh", "deprecated", "非标准：应为 偏滤器抽气"),
    # magnet feeder → 磁体馈线
    ("磁场馈线", "magnet-feeder", "zh", "forbidden", "误译magnet：正确为 磁体馈线"),
    ("磁体供电线", "magnet-feeder", "zh", "forbidden", "误译feeder：正确为 磁体馈线"),
    # superconducting joint → 超导接头
    (
        "超导关节",
        "superconducting-joint",
        "zh",
        "forbidden",
        "误译joint：正确为 超导接头",
    ),
    (
        "超导接合",
        "superconducting-joint",
        "zh",
        "forbidden",
        "误译joint：正确为 超导接头",
    ),
    # toroidal field coil → 纵场线圈
    (
        "环向场线圈",
        "toroidal-field-coil",
        "zh",
        "deprecated",
        "非标准：聚变惯用 纵场线圈",
    ),
    # plant layout → 电站布局
    ("工厂布局", "plant-layout", "zh", "forbidden", "误译plant：聚变应为 电站布局"),
    # plant lifetime → 电站寿命
    ("工厂寿命", "plant-lifetime", "zh", "forbidden", "误译plant：聚变应为 电站寿命"),
    # steam generator → 蒸汽发生器
    (
        "蒸汽发电机",
        "steam-generator",
        "zh",
        "forbidden",
        "误译generator：正确为 蒸汽发生器",
    ),
    # heat exchanger → 换热器
    ("热交换器", "heat-exchanger", "zh", "deprecated", "非标准：工程应为 换热器"),
    # supercritical CO2 cycle → 超临界二氧化碳循环
    (
        "超超临界CO2循环",
        "supercritical-co2-cycle",
        "zh",
        "forbidden",
        "混淆超/超超临界：正确为 超临界二氧化碳循环",
    ),
    # Rankine cycle → 朗肯循环
    ("兰金循环", "rankine-cycle", "zh", "forbidden", "音译错：正确为 朗肯循环"),
    ("朗金循环", "rankine-cycle", "zh", "forbidden", "音译错：正确为 朗肯循环"),
    # ========================================================================
    # E. 材料·辐照·超导 (61-75)
    # ========================================================================
    ("# ==== Batch 3E: materials, irradiation, superconductors ====",),
    # radiation hardening → 辐照硬化
    ("辐射硬化", "radiation-hardening", "zh", "forbidden", "误译：此语境为辐照硬化"),
    # radiation-induced segregation → 辐照偏析
    (
        "辐射诱导分离",
        "radiation-induced-segregation",
        "zh",
        "forbidden",
        "误译segregation：正确为 辐照偏析",
    ),
    (
        "辐照分离",
        "radiation-induced-segregation",
        "zh",
        "forbidden",
        "误译segregation：正确为 辐照偏析",
    ),
    # recrystallization → 再结晶
    ("重结晶", "recrystallization", "zh", "forbidden", "误译re-：正确为 再结晶"),
    # Frenkel pair → Frenkel缺陷对
    (
        "弗伦克尔对",
        "frenkel-pair",
        "zh",
        "forbidden",
        "误音译+缺'缺陷'：正确为 Frenkel缺陷对",
    ),
    # interstitial atom → 间隙原子
    (
        "间质原子",
        "interstitial-atom",
        "zh",
        "forbidden",
        "误译interstitial：正确为 间隙原子",
    ),
    # transmutation → 嬗变
    ("转化", "transmutation", "zh", "forbidden", "误译transmutation：核物理应为 嬗变"),
    # (skip: 核嬗变 already exists as alias)
    # SiC/SiC composite → 碳化硅复合材料
    (
        "SiC/SiC复合物",
        "sic-sic-composite",
        "zh",
        "deprecated",
        "非标准：应为 碳化硅复合材料",
    ),
    # thermal barrier coating → 热障涂层
    (
        "热屏障涂层",
        "thermal-barrier-coating",
        "zh",
        "forbidden",
        "误译barrier：正确为 热障涂层",
    ),
    # lithium orthosilicate → 正硅酸锂
    (
        "原硅酸锂",
        "lithium-orthosilicate",
        "zh",
        "forbidden",
        "误译ortho-：正确为 正硅酸锂",
    ),
    # post-irradiation examination → 辐照后检验
    (
        "辐射后检查",
        "post-irradiation-examination",
        "zh",
        "forbidden",
        "双重误译：正确为 辐照后检验",
    ),
    (
        "辐照后检查",
        "post-irradiation-examination",
        "zh",
        "deprecated",
        "非标准：应为 辐照后检验",
    ),
    # quench detection → 失超检测
    (
        "淬灭检测",
        "quench-detection",
        "zh",
        "forbidden",
        "误译quench：超导应为 失超检测",
    ),
    # quench protection → 失超保护
    (
        "淬灭保护",
        "quench-protection",
        "zh",
        "forbidden",
        "误译quench：超导应为 失超保护",
    ),
    # fatigue life → 疲劳寿命
    ("疲劳生命", "fatigue-life", "zh", "forbidden", "误译life：正确为 疲劳寿命"),
    ("疲劳周期", "fatigue-life", "zh", "forbidden", "误译life：正确为 疲劳寿命"),
    # strain sensitivity → 应变敏感性
    (
        "应力敏感性",
        "strain-sensitivity",
        "zh",
        "forbidden",
        "混淆strain/stress：正确为 应变敏感性",
    ),
    # ========================================================================
    # F. 氚·安全·许可 (76-90)
    # ========================================================================
    ("# ==== Batch 3F: tritium, safety, licensing ====",),
    # tritium self-sufficiency → 氚自持
    (
        "氚自足",
        "tritium-self-sufficiency",
        "zh",
        "forbidden",
        "误译：聚变术语应为 氚自持",
    ),
    (
        "氚自给自足",
        "tritium-self-sufficiency",
        "zh",
        "forbidden",
        "误译：聚变术语应为 氚自持",
    ),
    # tritium inventory → 氚存量
    (
        "氚库存",
        "tritium-inventory",
        "zh",
        "forbidden",
        "误译inventory：聚变应为 氚存量",
    ),
    # tritium startup inventory → 氚启动存量
    (
        "氚启动库存",
        "tritium-startup-inventory",
        "zh",
        "forbidden",
        "误译inventory：正确为 氚启动存量",
    ),
    # tritium removal → 氚滞留清除
    (
        "氚去除",
        "tritium-removal",
        "zh",
        "forbidden",
        "误译：缺'滞留'，正确为 氚滞留清除",
    ),
    # design basis accident → 设计基准事故
    (
        "设计基础事故",
        "design-basis-accident",
        "zh",
        "forbidden",
        "误译basis：正确为 设计基准事故",
    ),
    # maximum credible accident → 最大可信事故
    (
        "最大可能事故",
        "maximum-credible-accident",
        "zh",
        "forbidden",
        "误译credible：正确为 最大可信事故",
    ),
    # safety case → 安全论证
    ("安全案例", "safety-case", "zh", "forbidden", "误译case：正确为 安全论证"),
    # safety classification → 安全分级
    (
        "安全分类",
        "safety-classification",
        "zh",
        "forbidden",
        "误译classification：此语境应为 安全分级",
    ),
    # emergency planning zone → 应急计划区
    (
        "紧急规划区",
        "emergency-planning-zone",
        "zh",
        "forbidden",
        "误译emergency+planning：正确为 应急计划区",
    ),
    # dose constraint → 剂量约束
    (
        "剂量限制",
        "dose-constraint",
        "zh",
        "forbidden",
        "误译constraint：正确为 剂量约束",
    ),
    # shutdown dose rate → 停堆剂量率
    (
        "关机剂量率",
        "shutdown-dose-rate",
        "zh",
        "forbidden",
        "误译shutdown：聚变应为 停堆剂量率",
    ),
    (
        "停机剂量率",
        "shutdown-dose-rate",
        "zh",
        "forbidden",
        "误译shutdown：聚变应为 停堆剂量率",
    ),
    # regulatory framework → 监管框架
    ("法规框架", "regulatory-framework", "zh", "deprecated", "非标准：应为 监管框架"),
    # public acceptance → 公众接受度
    (
        "公共接受",
        "public-acceptance",
        "zh",
        "forbidden",
        "误译public：正确为 公众接受度",
    ),
    ("公众接受", "public-acceptance", "zh", "deprecated", "缺字'度'：应为 公众接受度"),
    # ========================================================================
    # G. ICF·先进概念·装置 (91-100)
    # ========================================================================
    ("# ==== Batch 3G: ICF, advanced concepts, devices ====",),
    # field-reversed configuration → 场反位形
    (
        "场反转配置",
        "field-reversed-configuration",
        "zh",
        "forbidden",
        "误译configuration：正确为 场反位形",
    ),
    (
        "场反转构型",
        "field-reversed-configuration",
        "zh",
        "deprecated",
        "非标准：应为 场反位形",
    ),
    # compact toroid → 紧凑环
    ("紧凑环面体", "compact-toroid", "zh", "forbidden", "误译toroid：正确为 紧凑环"),
    # tandem mirror → 串列磁镜
    ("串联磁镜", "tandem-mirror", "zh", "forbidden", "误译tandem：正确为 串列磁镜"),
    # magneto-inertial fusion → 磁化惯性聚变
    (
        "磁惯性聚变",
        "magneto-inertial-fusion",
        "zh",
        "forbidden",
        "缺字'化'：正确为 磁化惯性聚变",
    ),
    # heavy-ion fusion → 重离子聚变
    ("重粒子聚变", "heavy-ion-fusion", "zh", "forbidden", "误译ion：正确为 重离子聚变"),
    # muon-catalyzed fusion → μ子催化聚变
    ("介子催化聚变", "muon-catalyzed-fusion", "zh", "forbidden", "误译muon：μ子≠介子"),
    # hot-spot ignition → 中心热斑点火
    (
        "热点点火",
        "hot-spot-ignition",
        "zh",
        "forbidden",
        "误译hot spot：ICF应为 中心热斑点火",
    ),
    # implosion velocity → 内爆速度
    ("爆聚速度", "implosion-velocity", "zh", "deprecated", "非标准：应为 内爆速度"),
    # DEMO → 示范堆
    ("演示堆", "demo", "zh", "forbidden", "误译demo：正确为 示范堆"),
    ("示范反应堆", "demo", "zh", "deprecated", "啰嗦：应为 示范堆"),
    # fusion pilot plant → 聚变试验电站
    (
        "聚变试点电站",
        "fusion-pilot-plant",
        "zh",
        "forbidden",
        "误译pilot：正确为 聚变试验电站",
    ),
    (
        "聚变试验工厂",
        "fusion-pilot-plant",
        "zh",
        "forbidden",
        "误译plant：正确为 聚变试验电站",
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
