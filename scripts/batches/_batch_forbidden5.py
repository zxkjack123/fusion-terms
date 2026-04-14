#!/usr/bin/env python3
"""Batch 5: forbidden/deprecated aliases for AI mistranslations (next ~100 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 等离子体平衡·稳定性·MHD (1-18)
    # ========================================================================
    ("# ==== Batch 5A: equilibrium, stability, MHD ====",),
    # ideal MHD → 理想磁流体力学
    ("理想MHD力学", "ideal-mhd", "zh", "forbidden", "误译：正确为 理想磁流体力学"),
    # resistive MHD → 电阻磁流体力学
    (
        "阻性磁流体",
        "resistive-mhd",
        "zh",
        "forbidden",
        "误译resistive：正确为 电阻磁流体力学",
    ),
    ("电阻性MHD", "resistive-mhd", "zh", "deprecated", "非标准：应为 电阻磁流体力学"),
    # reduced MHD → 约化MHD
    ("简化MHD", "reduced-mhd", "zh", "forbidden", "误译reduced：正确为 约化MHD"),
    ("降阶MHD", "reduced-mhd", "zh", "forbidden", "误译reduced：正确为 约化MHD"),
    # Grad-Shafranov equation → Grad-Shafranov方程
    (
        "格拉德-沙弗拉诺夫方程",
        "grad-shafranov-equation",
        "zh",
        "forbidden",
        "误音译人名：正确保留 Grad-Shafranov方程",
    ),
    # free-boundary equilibrium → 自由边界平衡
    (
        "自由边界均衡",
        "free-boundary-equilibrium",
        "zh",
        "forbidden",
        "误译equilibrium：正确为 自由边界平衡",
    ),
    # force-free equilibrium → 无力平衡
    (
        "力自由平衡",
        "force-free-equilibrium",
        "zh",
        "forbidden",
        "误译force-free：正确为 无力平衡",
    ),
    (
        "无外力平衡",
        "force-free-equilibrium",
        "zh",
        "forbidden",
        "误译force-free：正确为 无力平衡",
    ),
    # sawtooth crash → 锯齿崩塌
    ("锯齿崩溃", "sawtooth-crash", "zh", "forbidden", "误译crash：正确为 锯齿崩塌"),
    ("锯齿坠毁", "sawtooth-crash", "zh", "forbidden", "误译crash：正确为 锯齿崩塌"),
    # dynamo effect → 发电机效应
    ("动力效应", "dynamo-effect", "zh", "forbidden", "误译dynamo：正确为 发电机效应"),
    ("发电机效果", "dynamo-effect", "zh", "forbidden", "误译effect：正确为 发电机效应"),
    # current hole → 电流空洞
    ("电流孔", "current-hole", "zh", "forbidden", "误译hole：正确为 电流空洞"),
    ("电流空心", "current-hole", "zh", "forbidden", "误译hole：正确为 电流空洞"),
    # negative triangularity → 负三角形变
    (
        "负三角形",
        "negative-triangularity",
        "zh",
        "forbidden",
        "误译triangularity：正确为 负三角形变",
    ),
    (
        "负三角变形",
        "negative-triangularity",
        "zh",
        "forbidden",
        "误译triangularity：正确为 负三角形变",
    ),
    # double-null → 双零位形
    ("双零点", "double-null", "zh", "forbidden", "误译null：正确为 双零位形"),
    ("双空位形", "double-null", "zh", "forbidden", "误译：正确为 双零位形"),
    # single-null → 单零位形
    ("单零点", "single-null", "zh", "forbidden", "误译null：正确为 单零位形"),
    ("单空位形", "single-null", "zh", "forbidden", "误译：正确为 单零位形"),
    # high beta → 高比压
    ("高贝塔", "high-beta", "zh", "forbidden", "误音译beta：正确为 高比压"),
    # poloidal beta → 极向比压
    ("极向贝塔", "poloidal-beta", "zh", "forbidden", "误音译beta：正确为 极向比压"),
    # toroidal field → 环向磁场
    ("环形磁场", "toroidal-field", "zh", "forbidden", "误译toroidal：正确为 环向磁场"),
    # poloidal field → 极向磁场
    ("极化磁场", "poloidal-field", "zh", "forbidden", "误译poloidal：正确为 极向磁场"),
    # q-profile → 安全因子剖面
    ("q值分布", "q-profile", "zh", "deprecated", "非标准：应为 安全因子剖面"),
    (
        "q描述文件",
        "q-profile",
        "zh",
        "forbidden",
        "误译profile(计算机义)：正确为 安全因子剖面",
    ),
    # rotation reversal → 旋转反转
    ("旋转逆转", "rotation-reversal", "zh", "deprecated", "非标准：应为 旋转反转"),
    (
        "旋转倒置",
        "rotation-reversal",
        "zh",
        "forbidden",
        "误译reversal：正确为 旋转反转",
    ),
    # ========================================================================
    # B. 输运·湍流·动理学 (19-32)
    # ========================================================================
    ("# ==== Batch 5B: transport, turbulence, kinetics ====",),
    # drift kinetics → 漂移动理学
    (
        "漂移动力学",
        "drift-kinetics",
        "zh",
        "forbidden",
        "误译kinetics：正确为 漂移动理学",
    ),
    (
        "漂移运动学",
        "drift-kinetics",
        "zh",
        "forbidden",
        "误译kinetics：正确为 漂移动理学",
    ),
    # blob transport → 团块输运
    (
        "斑点传输",
        "blob-transport",
        "zh",
        "forbidden",
        "误译blob+transport：正确为 团块输运",
    ),
    ("气泡输运", "blob-transport", "zh", "forbidden", "误译blob：正确为 团块输运"),
    # avalanche transport → 雪崩输运
    (
        "雪崩传输",
        "avalanche-transport",
        "zh",
        "forbidden",
        "误译transport：正确为 雪崩输运",
    ),
    # staircase transport → 阶梯输运
    (
        "楼梯输运",
        "staircase-transport",
        "zh",
        "forbidden",
        "误译staircase：正确为 阶梯输运",
    ),
    ("台阶输运", "staircase-transport", "zh", "deprecated", "非标准：应为 阶梯输运"),
    # turbulence suppression → 湍流抑制
    (
        "紊流压制",
        "turbulence-suppression",
        "zh",
        "forbidden",
        "双误(紊流+压制)：正确为 湍流抑制",
    ),
    (
        "湍流压抑",
        "turbulence-suppression",
        "zh",
        "forbidden",
        "误译suppression：正确为 湍流抑制",
    ),
    # turbulence saturation → 湍流饱和
    (
        "紊流饱和",
        "turbulence-saturation",
        "zh",
        "forbidden",
        "误译turbulence：正确为 湍流饱和",
    ),
    # subcritical turbulence → 亚临界湍流
    (
        "次临界紊流",
        "subcritical-turbulence",
        "zh",
        "forbidden",
        "双误(次临界+紊流)：正确为 亚临界湍流",
    ),
    (
        "亚临界紊流",
        "subcritical-turbulence",
        "zh",
        "forbidden",
        "误译turbulence：正确为 亚临界湍流",
    ),
    # parallel transport → 平行输运
    (
        "平行传输",
        "parallel-transport",
        "zh",
        "forbidden",
        "误译transport：正确为 平行输运",
    ),
    (
        "并行输运",
        "parallel-transport",
        "zh",
        "forbidden",
        "误译parallel(计算机义)：正确为 平行输运",
    ),
    # critical gradient → 临界梯度
    (
        "关键梯度",
        "critical-gradient",
        "zh",
        "forbidden",
        "误译critical：正确为 临界梯度",
    ),
    # critical balance → 临界平衡
    (
        "关键平衡",
        "critical-balance",
        "zh",
        "forbidden",
        "误译critical：正确为 临界平衡",
    ),
    # particle confinement time → 粒子约束时间
    (
        "粒子限制时间",
        "particle-confinement-time",
        "zh",
        "forbidden",
        "误译confinement：正确为 粒子约束时间",
    ),
    (
        "粒子封闭时间",
        "particle-confinement-time",
        "zh",
        "forbidden",
        "误译confinement：正确为 粒子约束时间",
    ),
    # spectral transfer → 能谱级联
    (
        "频谱转移",
        "spectral-transfer",
        "zh",
        "forbidden",
        "误译spectral+transfer：正确为 能谱级联",
    ),
    (
        "光谱传输",
        "spectral-transfer",
        "zh",
        "forbidden",
        "误译spectral+transfer：正确为 能谱级联",
    ),
    # predator-prey oscillation → 捕食-被捕食振荡
    (
        "掠食者-猎物振荡",
        "predator-prey-oscillation",
        "zh",
        "forbidden",
        "误译：正确为 捕食-被捕食振荡",
    ),
    # delta-f method → δf方法
    ("增量f法", "delta-f-method", "zh", "deprecated", "非标准：应为 δf方法"),
    # ========================================================================
    # C. 边界·偏滤器·等离子体壁 (33-50)
    # ========================================================================
    ("# ==== Batch 5C: boundary, divertor, PSI ====",),
    # plasma-facing material → 面向等离子体材料
    (
        "等离子体面材料",
        "plasma-facing-material",
        "zh",
        "forbidden",
        "误译facing：正确为 面向等离子体材料",
    ),
    (
        "面对等离子体材料",
        "plasma-facing-material",
        "zh",
        "forbidden",
        "误译facing：正确为 面向等离子体材料",
    ),
    # plasma-surface interaction → 等离子体表面相互作用
    (
        "等离子体表面交互",
        "plasma-surface-interaction",
        "zh",
        "forbidden",
        "误译interaction：正确为 等离子体表面相互作用",
    ),
    # detachment control → 脱靶控制
    (
        "分离控制",
        "detachment-control",
        "zh",
        "forbidden",
        "误译detachment：正确为 脱靶控制",
    ),
    (
        "剥离控制",
        "detachment-control",
        "zh",
        "forbidden",
        "误译detachment：正确为 脱靶控制",
    ),
    # detachment front → 脱靶前沿
    (
        "分离前沿",
        "detachment-front",
        "zh",
        "forbidden",
        "误译detachment：正确为 脱靶前沿",
    ),
    (
        "脱离前锋",
        "detachment-front",
        "zh",
        "forbidden",
        "误译detachment+front：正确为 脱靶前沿",
    ),
    # ELM mitigation → ELM缓解
    ("ELM减缓", "elm-mitigation", "zh", "deprecated", "非标准：应为 ELM缓解"),
    ("ELM减轻", "elm-mitigation", "zh", "deprecated", "非标准：应为 ELM缓解"),
    # disruption erosion → 破裂侵蚀
    (
        "中断侵蚀",
        "disruption-erosion",
        "zh",
        "forbidden",
        "误译disruption：正确为 破裂侵蚀",
    ),
    (
        "破坏侵蚀",
        "disruption-erosion",
        "zh",
        "forbidden",
        "误译disruption：正确为 破裂侵蚀",
    ),
    # physical sputtering → 物理溅射
    (
        "物理喷溅",
        "physical-sputtering",
        "zh",
        "forbidden",
        "误译sputtering：正确为 物理溅射",
    ),
    (
        "物理飞溅",
        "physical-sputtering",
        "zh",
        "forbidden",
        "误译sputtering：正确为 物理溅射",
    ),
    # prompt redeposition → 即时再沉积
    (
        "快速再沉积",
        "prompt-redeposition",
        "zh",
        "deprecated",
        "非标准：应为 即时再沉积",
    ),
    (
        "及时再堆积",
        "prompt-redeposition",
        "zh",
        "forbidden",
        "误译prompt+redeposition：正确为 即时再沉积",
    ),
    # fuel recycling → 燃料再循环
    (
        "燃料回收",
        "fuel-recycling",
        "zh",
        "forbidden",
        "误译recycling：正确为 燃料再循环",
    ),
    (
        "燃料循环利用",
        "fuel-recycling",
        "zh",
        "forbidden",
        "误译recycling：正确为 燃料再循环",
    ),
    # vapor shielding → 蒸汽屏蔽
    (
        "蒸气防护",
        "vapor-shielding",
        "zh",
        "forbidden",
        "误译shielding：正确为 蒸汽屏蔽",
    ),
    (
        "蒸汽遮蔽",
        "vapor-shielding",
        "zh",
        "forbidden",
        "误译shielding：正确为 蒸汽屏蔽",
    ),
    # long-leg divertor → 长腿偏滤器
    (
        "长支路偏滤器",
        "long-leg-divertor",
        "zh",
        "forbidden",
        "误译leg：正确为 长腿偏滤器",
    ),
    (
        "长臂偏滤器",
        "long-leg-divertor",
        "zh",
        "forbidden",
        "误译leg：正确为 长腿偏滤器",
    ),
    # pellet ablation → 弹丸烧蚀
    (
        "颗粒消融",
        "pellet-ablation",
        "zh",
        "forbidden",
        "误译pellet+ablation：正确为 弹丸烧蚀",
    ),
    ("弹丸熔蚀", "pellet-ablation", "zh", "deprecated", "非标准：应为 弹丸烧蚀"),
    # presheath → 预鞘
    ("前鞘", "presheath", "zh", "deprecated", "非标准：应为 预鞘"),
    ("预护套", "presheath", "zh", "forbidden", "误译sheath：正确为 预鞘"),
    # density pump-out → 密度泵出
    ("密度抽出", "density-pump-out", "zh", "deprecated", "非标准：应为 密度泵出"),
    # private flux region → 私有磁通区
    (
        "私通量区",
        "private-flux-region",
        "zh",
        "forbidden",
        "误译flux：正确为 私有磁通区",
    ),
    ("私密通量域", "private-flux-region", "zh", "forbidden", "误译：正确为 私有磁通区"),
    # melt damage → 熔化损伤
    ("融化损害", "melt-damage", "zh", "forbidden", "误译melt+damage：正确为 熔化损伤"),
    # I-mode → I模
    ("I模式", "i-mode", "zh", "deprecated", "非标准：应为 I模"),
    # massive gas injection → 大量气体注入
    (
        "大规模气体注射",
        "massive-gas-injection",
        "zh",
        "forbidden",
        "误译injection：正确为 大量气体注入",
    ),
    # ========================================================================
    # D. 超导·磁体·电工 (51-60)
    # ========================================================================
    ("# ==== Batch 5D: superconducting magnets, electrical ====",),
    # winding pack → 绕组包
    ("绕线包", "winding-pack", "zh", "deprecated", "非标准：应为 绕组包"),
    # magnet bore → 磁体孔径
    ("磁铁孔径", "magnet-bore", "zh", "forbidden", "误译magnet：正确为 磁体孔径"),
    ("磁体膛径", "magnet-bore", "zh", "deprecated", "非标准：应为 磁体孔径"),
    # joint resistance → 接头电阻
    ("关节电阻", "joint-resistance", "zh", "forbidden", "误译joint：正确为 接头电阻"),
    ("连接电阻", "joint-resistance", "zh", "deprecated", "非标准：应为 接头电阻"),
    # eddy current → 涡流
    ("涡电流", "eddy-current", "zh", "deprecated", "非标准：应为 涡流"),
    ("漩涡电流", "eddy-current", "zh", "forbidden", "误译eddy：正确为 涡流"),
    # AC loss → 交流损耗
    ("交流损失", "ac-loss", "zh", "forbidden", "误译loss：正确为 交流损耗"),
    # insulation material → 绝缘材料
    (
        "隔热材料",
        "insulation-material",
        "zh",
        "forbidden",
        "误译insulation：正确为 绝缘材料",
    ),
    # magnetic stored energy → 磁储能
    ("磁存储能量", "magnetic-stored-energy", "zh", "forbidden", "误译：正确为 磁储能"),
    # magnet structure → 磁体结构件
    (
        "磁铁结构",
        "magnet-structure",
        "zh",
        "forbidden",
        "误译magnet：正确为 磁体结构件",
    ),
    # magnet cooling → 磁体冷却
    ("磁铁冷却", "magnet-cooling", "zh", "forbidden", "误译magnet：正确为 磁体冷却"),
    # TF ripple → 环向场纹波
    ("TF波纹", "tf-ripple", "zh", "deprecated", "非标准：应为 环向场纹波"),
    (
        "环形场波纹",
        "tf-ripple",
        "zh",
        "forbidden",
        "双误(环形≠环向、波纹≠纹波)：正确为 环向场纹波",
    ),
    # ========================================================================
    # E. 中子学·辐射防护·蒙卡 (61-75)
    # ========================================================================
    ("# ==== Batch 5E: neutronics, radiation protection, MC ====",),
    # neutron flux → 中子通量
    ("中子流量", "neutron-flux", "zh", "forbidden", "误译flux：正确为 中子通量"),
    (
        "中子磁通",
        "neutron-flux",
        "zh",
        "forbidden",
        "误译flux(电磁义)：正确为 中子通量",
    ),
    # neutron spectrum → 中子能谱
    (
        "中子频谱",
        "neutron-spectrum",
        "zh",
        "forbidden",
        "误译spectrum：正确为 中子能谱",
    ),
    (
        "中子光谱",
        "neutron-spectrum",
        "zh",
        "forbidden",
        "误译spectrum：正确为 中子能谱",
    ),
    # neutron yield → 中子产额
    ("中子产量", "neutron-yield", "zh", "deprecated", "非标准：应为 中子产额"),
    ("中子收率", "neutron-yield", "zh", "forbidden", "误译yield：正确为 中子产额"),
    # shielding penetration → 屏蔽穿透
    (
        "屏蔽渗透",
        "shielding-penetration",
        "zh",
        "forbidden",
        "误译penetration：正确为 屏蔽穿透",
    ),
    # radiation streaming → 流道串流
    (
        "辐射流",
        "radiation-streaming",
        "zh",
        "forbidden",
        "误译streaming：正确为 流道串流",
    ),
    (
        "辐射流动",
        "radiation-streaming",
        "zh",
        "forbidden",
        "误译streaming：正确为 流道串流",
    ),
    # weight window → 权窗
    ("权重窗口", "weight-window", "zh", "forbidden", "误译：正确为 权窗"),
    ("重量窗口", "weight-window", "zh", "forbidden", "误译weight：正确为 权窗"),
    # variance reduction → 方差缩减
    (
        "方差减少",
        "variance-reduction",
        "zh",
        "forbidden",
        "误译reduction：正确为 方差缩减",
    ),
    (
        "方差降低",
        "variance-reduction",
        "zh",
        "forbidden",
        "误译reduction：正确为 方差缩减",
    ),
    # clearance index → 清洁解控指数
    (
        "清除指数",
        "clearance-index",
        "zh",
        "forbidden",
        "误译clearance：正确为 清洁解控指数",
    ),
    (
        "间隙指标",
        "clearance-index",
        "zh",
        "forbidden",
        "误译clearance(机械义)：正确为 清洁解控指数",
    ),
    # equivalent dose → 当量剂量
    (
        "等效剂量",
        "equivalent-dose",
        "zh",
        "forbidden",
        "误译equivalent：正确为 当量剂量",
    ),
    # occupational exposure → 职业照射
    (
        "职业暴露",
        "occupational-exposure",
        "zh",
        "forbidden",
        "误译exposure：正确为 职业照射",
    ),
    # gas production rate → 气体产额
    ("气体产生率", "gas-production-rate", "zh", "forbidden", "误译：正确为 气体产额"),
    (
        "气体生产率",
        "gas-production-rate",
        "zh",
        "forbidden",
        "误译production：正确为 气体产额",
    ),
    # shielding labyrinth → 迷宫通道
    ("屏蔽迷宫", "shielding-labyrinth", "zh", "deprecated", "非标准：应为 迷宫通道"),
    # nuclear response function → 核响应函数
    (
        "核反应函数",
        "nuclear-response-function",
        "zh",
        "forbidden",
        "误译response≠reaction：正确为 核响应函数",
    ),
    # neutron source → 中子源
    ("中子来源", "neutron-source", "zh", "forbidden", "误译source：正确为 中子源"),
    # tallying → 计数统计
    ("记账", "tallying", "zh", "forbidden", "误译tallying：正确为 计数统计"),
    ("清点", "tallying", "zh", "forbidden", "误译tallying：正确为 计数统计"),
    # ========================================================================
    # F. 材料·制造·部件 (76-85)
    # ========================================================================
    ("# ==== Batch 5F: materials, manufacturing, components ====",),
    # tungsten monoblock → 钨单块
    (
        "钨整体块",
        "tungsten-monoblock",
        "zh",
        "forbidden",
        "误译monoblock：正确为 钨单块",
    ),
    # plasma spray coating → 等离子喷涂
    (
        "等离子体喷涂",
        "plasma-spray-coating",
        "zh",
        "forbidden",
        "误加'体'字：正确为 等离子喷涂",
    ),
    # in-bore welding → 孔内焊接
    ("膛内焊接", "in-bore-welding", "zh", "deprecated", "非标准：应为 孔内焊接"),
    # hypervapotron → 超蒸发管
    ("超蒸发器", "hypervapotron", "zh", "forbidden", "误译：正确为 超蒸发管"),
    # helium bubble → 氦泡
    ("氦气泡", "helium-bubble", "zh", "deprecated", "非标准：应为 氦泡"),
    ("氦气气泡", "helium-bubble", "zh", "forbidden", "啰嗦：正确为 氦泡"),
    # surface roughening → 表面粗糙化
    ("表面粗化", "surface-roughening", "zh", "deprecated", "非标准：应为 表面粗糙化"),
    # tungsten accumulation → 钨积聚
    ("钨堆积", "tungsten-accumulation", "zh", "deprecated", "非标准：应为 钨积聚"),
    ("钨累积", "tungsten-accumulation", "zh", "deprecated", "非标准：应为 钨积聚"),
    # metal hydride bed → 金属氢化物床
    (
        "金属氢化物层",
        "metal-hydride-bed",
        "zh",
        "forbidden",
        "误译bed：正确为 金属氢化物床",
    ),
    # articulated boom → 铰接臂
    (
        "关节吊臂",
        "articulated-boom",
        "zh",
        "forbidden",
        "误译articulated：正确为 铰接臂",
    ),
    ("铰链臂", "articulated-boom", "zh", "forbidden", "误译articulated：正确为 铰接臂"),
    # purge gas → 吹扫气
    ("净化气", "purge-gas", "zh", "forbidden", "误译purge：正确为 吹扫气"),
    ("清洗气", "purge-gas", "zh", "forbidden", "误译purge：正确为 吹扫气"),
    # ========================================================================
    # G. 堆系统·经济·许可 (86-95)
    # ========================================================================
    ("# ==== Batch 5G: reactor systems, economics, licensing ====",),
    # auxiliary power → 厂用电
    ("辅助电力", "auxiliary-power", "zh", "forbidden", "误译：正确为 厂用电"),
    ("辅助功率", "auxiliary-power", "zh", "forbidden", "误译：正确为 厂用电"),
    # recirculating power → 循环功率
    (
        "回流功率",
        "recirculating-power",
        "zh",
        "forbidden",
        "误译recirculating：正确为 循环功率",
    ),
    # first-of-a-kind → 首台堆
    ("首种", "first-of-a-kind", "zh", "forbidden", "误译：正确为 首台堆"),
    ("第一同类", "first-of-a-kind", "zh", "forbidden", "误译：正确为 首台堆"),
    # overnight capital cost → 隔夜建设成本
    (
        "过夜资本成本",
        "overnight-capital-cost",
        "zh",
        "forbidden",
        "误译overnight：正确为 隔夜建设成本",
    ),
    # vertical displacement event → 垂直位移事件
    (
        "竖直位移事件",
        "vertical-displacement-event",
        "zh",
        "deprecated",
        "非标准：应为 垂直位移事件",
    ),
    # intermediate heat exchanger → 中间换热器
    (
        "中间热交换器",
        "intermediate-heat-exchanger",
        "zh",
        "deprecated",
        "非标准：应为 中间换热器",
    ),
    # levelized cost → 平准化成本
    (
        "标准化成本",
        "levelized-cost",
        "zh",
        "forbidden",
        "误译levelized：正确为 平准化成本",
    ),
    (
        "水平化成本",
        "levelized-cost",
        "zh",
        "forbidden",
        "误译levelized：正确为 平准化成本",
    ),
    # engineering gain → 工程增益因子
    (
        "工程收益",
        "engineering-gain",
        "zh",
        "forbidden",
        "误译gain：正确为 工程增益因子",
    ),
    # integrated commissioning → 综合调试
    (
        "集成调试",
        "integrated-commissioning",
        "zh",
        "deprecated",
        "非标准：应为 综合调试",
    ),
    (
        "整体投运",
        "integrated-commissioning",
        "zh",
        "forbidden",
        "误译commissioning：正确为 综合调试",
    ),
    # availability → 可用率
    (
        "可用性",
        "availability",
        "zh",
        "forbidden",
        "误译availability(堆工程应为比率)：正确为 可用率",
    ),
    # ========================================================================
    # H. 聚变方案·特殊概念 (96-100)
    # ========================================================================
    ("# ==== Batch 5H: fusion schemes & special concepts ====",),
    # alpha channeling → α粒子能量导引
    (
        "α通道",
        "alpha-channeling",
        "zh",
        "forbidden",
        "误译channeling：正确为 α粒子能量导引",
    ),
    (
        "α引导",
        "alpha-channeling",
        "zh",
        "forbidden",
        "误译channeling：正确为 α粒子能量导引",
    ),
    # aneutronic fusion → 无中子聚变
    (
        "非中子聚变",
        "aneutronic-fusion",
        "zh",
        "forbidden",
        "误译aneutronic：正确为 无中子聚变",
    ),
    (
        "无中子融合",
        "aneutronic-fusion",
        "zh",
        "forbidden",
        "误用日语'融合'：正确为 无中子聚变",
    ),
    # coaxial helicity injection → 同轴螺旋度注入
    (
        "同轴螺旋注入",
        "coaxial-helicity-injection",
        "zh",
        "forbidden",
        "缺字'度'：正确为 同轴螺旋度注入",
    ),
    # spheromak → 球马克
    ("球状等离子体", "spheromak", "zh", "forbidden", "误译spheromak：正确为 球马克"),
    (
        "球形托马克",
        "spheromak",
        "zh",
        "forbidden",
        "spheromak≠spherical tokamak：正确为 球马克",
    ),
    # direct energy conversion → 直接能量转换
    (
        "直接能量变换",
        "direct-energy-conversion",
        "zh",
        "deprecated",
        "非标准：应为 直接能量转换",
    ),
    (
        "直接能源转化",
        "direct-energy-conversion",
        "zh",
        "forbidden",
        "误译：正确为 直接能量转换",
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
