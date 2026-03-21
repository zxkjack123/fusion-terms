#!/usr/bin/env python3
"""Batch-add forbidden/deprecated aliases for common AI mistranslations of fusion terms."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

# Format: (wrong_text, correct_concept_id, lang, role, note)
# role: "forbidden" = factually wrong/misspelling, "deprecated" = non-standard variant
WRONG_ALIASES = [
    # ========================================================================
    # 1. Concept nouns — direct translation / false friends (items 1-40)
    # ========================================================================
    ("# ==== Common AI mistranslations: concept nouns ====",),

    # scrape-off layer → 刮削层
    ("刮离层", "scrape-off-layer", "zh", "forbidden", "误译：正确为 刮削层"),
    ("刮除层", "scrape-off-layer", "zh", "forbidden", "误译：正确为 刮削层"),
    ("擦除层", "scrape-off-layer", "zh", "forbidden", "误译：正确为 刮削层"),

    # bootstrap current → 自举电流
    ("引导电流", "bootstrap-current", "zh", "forbidden", "误译bootstrap：正确为 自举电流"),
    ("启动电流", "bootstrap-current", "zh", "forbidden", "误译bootstrap：正确为 自举电流"),
    ("拔靴电流", "bootstrap-current", "zh", "forbidden", "误译bootstrap：正确为 自举电流"),

    # stellarator → 仿星器
    ("恒星器", "stellarator", "zh", "forbidden", "误译stellar：正确为 仿星器"),
    ("星器", "stellarator", "zh", "forbidden", "误译：正确为 仿星器"),

    # tokamak → 托卡马克
    ("托克马克", "tokamak", "zh", "forbidden", "音译变体：正确为 托卡马克"),
    ("托克马科", "tokamak", "zh", "forbidden", "音译变体：正确为 托卡马克"),

    # divertor → 偏滤器
    ("分流器", "divertor", "zh", "forbidden", "误译divert：正确为 偏滤器"),
    ("转向器", "divertor", "zh", "forbidden", "误译divert：正确为 偏滤器"),
    ("偏转器", "divertor", "zh", "forbidden", "误译divert：正确为 偏滤器"),

    # disruption → 破裂
    ("中断", "disruption", "zh", "forbidden", "误译disruption：聚变语境正确为 破裂"),
    ("扰动", "disruption", "zh", "forbidden", "误译disruption：聚变语境正确为 破裂"),

    # confinement → 约束
    ("封闭", "magnetic-confinement", "zh", "forbidden", "误译confinement：正确为 约束"),
    ("封锁", "magnetic-confinement", "zh", "forbidden", "误译confinement：正确为 约束"),

    # pedestal → 台基
    ("底座", "pedestal", "zh", "forbidden", "误译pedestal：聚变语境正确为 台基"),

    # H-mode → 高约束模
    ("H模式", "h-mode", "zh", "deprecated", "非标准：应为 高约束模 或 H-mode"),
    ("高模式", "h-mode", "zh", "forbidden", "误译：正确为 高约束模"),

    # L-mode → 低约束模
    ("L模式", "l-mode", "zh", "deprecated", "非标准：应为 低约束模 或 L-mode"),
    ("低模式", "l-mode", "zh", "forbidden", "误译：正确为 低约束模"),

    # sawtooth → 锯齿
    ("锯齿波", "sawtooth", "zh", "deprecated", "非标准：聚变语境应为 锯齿"),

    # ELM → 边缘局域模
    ("边缘定域模", "edge-localized-mode", "zh", "deprecated", "非标准：应为 边缘局域模"),
    ("边缘局部模", "edge-localized-mode", "zh", "forbidden", "误译：正确为 边缘局域模"),
    ("边缘局部化模式", "edge-localized-mode", "zh", "forbidden", "误译：正确为 边缘局域模"),

    # limiter → 限制器
    ("限幅器", "limiter", "zh", "forbidden", "误译：电子学术语，聚变应为 限制器"),
    ("限位器", "limiter", "zh", "forbidden", "误译：机械术语，聚变应为 限制器"),

    # blanket → 包层
    ("覆盖层", "blanket", "zh", "forbidden", "误译blanket：正确为 包层"),
    ("毯子", "blanket", "zh", "forbidden", "误译blanket：正确为 包层"),
    ("毯层", "blanket", "zh", "forbidden", "误译blanket：正确为 包层"),

    # pellet injection → 弹丸注入
    ("颗粒注入", "pellet-injection", "zh", "forbidden", "误译pellet：正确为 弹丸注入"),
    ("丸注入", "pellet-injection", "zh", "forbidden", "误译：正确为 弹丸注入"),
    ("丸料注入", "pellet-injection", "zh", "forbidden", "误译：正确为 弹丸注入"),

    # first wall → 第一壁
    ("首壁", "first-wall", "zh", "deprecated", "非标准变体：应为 第一壁"),
    ("前壁", "first-wall", "zh", "forbidden", "误译：正确为 第一壁"),

    # breeding blanket → 产氚包层
    ("增殖毯", "breeding-blanket", "zh", "forbidden", "误译breeding+blanket：正确为 产氚包层"),
    ("繁殖包层", "breeding-blanket", "zh", "forbidden", "误译breeding：正确为 产氚包层"),
    ("繁殖毯", "breeding-blanket", "zh", "forbidden", "误译breeding+blanket：正确为 产氚包层"),

    # neutral beam injection → 中性粒子束注入
    ("中性束注射", "neutral-beam-injection", "zh", "forbidden", "误译injection：注入非注射"),
    ("中性光束注入", "neutral-beam-injection", "zh", "forbidden", "误译beam：正确为 中性粒子束注入"),

    # impurity seeding → 杂质注入
    ("杂质播种", "impurity-seeding", "zh", "forbidden", "误译seeding：正确为 杂质注入"),
    ("杂质播撒", "impurity-seeding", "zh", "forbidden", "误译seeding：正确为 杂质注入"),

    # runaway electron → 逃逸电子
    ("失控电子", "runaway-electron", "zh", "forbidden", "误译runaway：正确为 逃逸电子"),
    ("跑道电子", "runaway-electron", "zh", "forbidden", "误译runaway：正确为 逃逸电子"),

    # quench → 失超
    ("淬灭", "quench", "zh", "forbidden", "误译quench：超导语境正确为 失超"),
    ("淬火", "quench", "zh", "forbidden", "误译quench：金属热处理义，超导应为 失超"),
    ("骤冷", "quench", "zh", "forbidden", "误译quench：超导语境正确为 失超"),

    # remote handling → 遥操作
    ("远程处理", "remote-handling", "zh", "forbidden", "误译handling：正确为 遥操作"),

    # hot cell → 热室
    ("热单元", "hot-cell", "zh", "forbidden", "误译cell：正确为 热室"),
    ("热腔", "hot-cell", "zh", "forbidden", "误译cell：正确为 热室"),

    # activation product → 活化产物
    ("激活产物", "activation-product", "zh", "forbidden", "误译activation：核物理应为 活化产物"),

    # halo current → 晕电流
    ("光环电流", "halo-current", "zh", "forbidden", "误译halo：正确为 晕电流"),
    ("光晕电流", "halo-current", "zh", "forbidden", "误译halo：正确为 晕电流"),

    # magnetic shear → 磁剪切
    ("磁切变", "magnetic-shear", "zh", "deprecated", "非标准变体：应为 磁剪切"),

    # flux surface → 磁面
    ("通量表面", "flux-surface", "zh", "forbidden", "误译flux surface：聚变应为 磁面"),
    # (skip: 磁通面 already exists as alias)
    ("磁通量面", "flux-surface", "zh", "forbidden", "误译：正确为 磁面"),

    # locked mode → 锁模
    ("锁定模式", "locked-mode", "zh", "forbidden", "误译：聚变应为 锁模"),

    # strike point → 打击点
    ("撞击点", "strike-point", "zh", "deprecated", "非标准变体：应为 打击点"),

    # separatrix → 分界面
    ("分离线", "separatrix", "zh", "forbidden", "误译separatrix：正确为 分界面"),

    # bremsstrahlung → 韧致辐射
    ("制动辐射", "bremsstrahlung", "zh", "deprecated", "非标准变体：应为 韧致辐射"),
    ("轫致制动辐射", "bremsstrahlung", "zh", "forbidden", "误译：正确为 韧致辐射"),

    # gyrotron → 回旋管
    ("旋转管", "gyrotron", "zh", "forbidden", "误译gyro：正确为 回旋管"),
    ("陀螺管", "gyrotron", "zh", "forbidden", "误译gyro：正确为 回旋管"),

    # Alfvén wave → 阿尔芬波
    ("阿尔文波", "alfven-wave", "zh", "deprecated", "非标准音译：应为 阿尔芬波"),
    ("阿尔弗文波", "alfven-wave", "zh", "forbidden", "误音译：正确为 阿尔芬波"),
    ("阿尔维恩波", "alfven-wave", "zh", "forbidden", "误音译：正确为 阿尔芬波"),

    # Lawson criterion → 劳森判据
    ("劳森准则", "lawson-criterion", "zh", "deprecated", "非标准：应为 劳森判据"),
    ("劳森标准", "lawson-criterion", "zh", "deprecated", "非标准：应为 劳森判据"),
    ("劳森条件", "lawson-criterion", "zh", "deprecated", "非标准：应为 劳森判据"),

    # plasma beta → 等离子体比压
    ("等离子体贝塔", "plasma-beta", "zh", "forbidden", "误音译β：正确为 等离子体比压"),

    # shattered pellet injection → 碎裂弹丸注入
    ("碎片弹丸注入", "shattered-pellet-injection", "zh", "deprecated", "非标准：应为 碎裂弹丸注入"),
    ("粉碎弹丸注射", "shattered-pellet-injection", "zh", "forbidden", "误译：正确为 碎裂弹丸注入"),

    # ========================================================================
    # 2. Device / system mistranslations (items 41-55)
    # ========================================================================
    ("# ==== Common AI mistranslations: devices & systems ====",),

    # cryostat → 低温恒温器
    ("低温容器", "cryostat", "zh", "deprecated", "非标准：应为 低温恒温器"),
    ("冷冻槽", "cryostat", "zh", "forbidden", "误译：正确为 低温恒温器"),

    # central solenoid → 中心螺管
    ("中央螺线管", "central-solenoid", "zh", "deprecated", "非标准：应为 中心螺管"),

    # poloidal field coil → 极向场线圈
    ("环形磁场线圈", "poloidal-field-coil", "zh", "forbidden", "误译：与纵场线圈混淆，正确为 极向场线圈"),

    # vacuum vessel → 真空室
    ("真空容器", "vacuum-vessel", "zh", "deprecated", "非标准变体：应为 真空室"),

    # port plug → 窗口模块
    ("端口塞", "port-plug", "zh", "forbidden", "误译plug：正确为 窗口模块"),
    ("端口插头", "port-plug", "zh", "forbidden", "误译plug：正确为 窗口模块"),
    ("端口堵头", "port-plug", "zh", "forbidden", "误译plug：正确为 窗口模块"),

    # test blanket module → 产氚模块 (TBM)
    ("测试包层模块", "tbm", "zh", "forbidden", "误译test+blanket：正确为 产氚模块"),
    ("试验毯模块", "tbm", "zh", "forbidden", "误译test+blanket：正确为 产氚模块"),

    # balance of plant → 电站辅助系统
    ("工厂余额", "balance-of-plant", "zh", "forbidden", "误译balance：正确为 电站辅助系统"),
    ("设备平衡", "balance-of-plant", "zh", "forbidden", "误译balance：正确为 电站辅助系统"),
    ("工厂平衡", "balance-of-plant", "zh", "forbidden", "误译balance：正确为 电站辅助系统"),

    # hohlraum → 黑腔
    ("空心腔", "hohlraum", "zh", "forbidden", "误译hohlraum：正确为 黑腔"),

    # current lead → 电流引线
    ("导流线", "current-lead", "zh", "deprecated", "非标准：应为 电流引线"),

    # cryoplant → 低温制冷系统
    ("低温工厂", "cryoplant", "zh", "forbidden", "误译plant：正确为 低温制冷系统"),

    # baffle → 挡板
    ("折流板", "baffle", "zh", "deprecated", "化工义：聚变应为 挡板"),

    # klystron → 速调管
    ("速度调制管", "klystron", "zh", "deprecated", "啰嗦：应为 速调管"),

    # Faraday screen → 法拉第屏
    ("法拉第屏幕", "faraday-screen", "zh", "forbidden", "误译screen：正确为 法拉第屏"),

    # ========================================================================
    # 3. Physical quantities / parameters (items 56-70)
    # ========================================================================
    ("# ==== Common AI mistranslations: physical quantities ====",),

    # energy confinement time → 能量约束时间
    ("能量封闭时间", "tau-e", "zh", "forbidden", "误译confinement：正确为 能量约束时间"),
    ("能量限制时间", "tau-e", "zh", "forbidden", "误译confinement：正确为 能量约束时间"),

    # fusion triple product → 聚变三乘积
    ("聚变三重积", "fusion-triple-product", "zh", "deprecated", "非标准：应为 聚变三乘积"),
    ("聚变三参数", "fusion-triple-product", "zh", "forbidden", "误译：正确为 聚变三乘积"),

    # neutron wall loading → 中子壁负荷
    ("中子墙负载", "neutron-wall-loading", "zh", "forbidden", "误译wall=墙：正确为 中子壁负荷"),
    ("中子壁载荷", "neutron-wall-loading", "zh", "deprecated", "非标准：应为 中子壁负荷"),

    # heat flux → 热流密度
    ("热通量", "heat-flux", "zh", "deprecated", "非标准变体：聚变应为 热流密度"),

    # DPA → 离位损伤
    ("原子位移", "dpa", "zh", "deprecated", "非标准：应为 离位损伤 (dpa)"),

    # tritium breeding ratio → 氚增殖比
    ("氚繁殖率", "tritium-breeding-ratio", "zh", "forbidden", "误译breeding：正确为 氚增殖比"),
    ("氚产率", "tritium-breeding-ratio", "zh", "forbidden", "误译：正确为 氚增殖比"),

    # burn fraction → 燃烧份额
    ("燃尽率", "burn-fraction", "zh", "forbidden", "误译：正确为 燃烧份额"),
    ("燃烧分数", "burn-fraction", "zh", "deprecated", "非标准：应为 燃烧份额"),

    # bootstrap fraction → 自举电流份额
    ("引导分数", "bootstrap-fraction", "zh", "forbidden", "误译bootstrap+fraction：正确为 自举电流份额"),
    ("启动比例", "bootstrap-fraction", "zh", "forbidden", "误译bootstrap：正确为 自举电流份额"),

    # H-factor → H因子
    ("H因素", "h-factor", "zh", "forbidden", "误译factor：聚变应为 H因子"),
    ("H系数", "h-factor", "zh", "forbidden", "误译factor：聚变应为 H因子"),

    # Greenwald density → 格林沃尔德密度
    ("格林沃尔德限值", "greenwald-density", "zh", "deprecated", "混淆density与limit：应为 格林沃尔德密度"),

    # rotational transform → 旋转变换
    ("旋转转换", "rotational-transform", "zh", "deprecated", "非标准：应为 旋转变换"),
    ("旋转变形", "rotational-transform", "zh", "forbidden", "误译：正确为 旋转变换"),

    # aspect ratio → 纵横比
    ("展弦比", "aspect-ratio", "zh", "forbidden", "误译：航空术语，聚变应为 纵横比"),
    ("宽高比", "aspect-ratio", "zh", "forbidden", "误译：通用IT义，聚变应为 纵横比"),
    ("长径比", "aspect-ratio", "zh", "deprecated", "非标准：聚变应为 纵横比"),

    # elongation → 拉长比
    ("伸长率", "plasma-elongation", "zh", "forbidden", "误译：材料学术语，聚变应为 拉长比"),
    ("延伸率", "plasma-elongation", "zh", "forbidden", "误译：材料学术语，聚变应为 拉长比"),

    # triangularity → 三角形变
    ("三角度", "plasma-triangularity", "zh", "forbidden", "误译：正确为 三角形变"),
    ("三角性", "plasma-triangularity", "zh", "forbidden", "误译：正确为 三角形变"),
    ("三角变形", "plasma-triangularity", "zh", "deprecated", "非标准：应为 三角形变"),

    # recycling coefficient → 再循环系数
    ("回收系数", "recycling-coefficient", "zh", "forbidden", "误译recycling：正确为 再循环系数"),

    # ========================================================================
    # 4. Process / method mistranslations (items 71-85)
    # ========================================================================
    ("# ==== Common AI mistranslations: processes & methods ====",),

    # plasma detachment → 等离子体脱靶
    ("等离子体分离", "plasma-detachment", "zh", "forbidden", "误译detachment：正确为 等离子体脱靶"),
    ("等离子体脱离", "plasma-detachment", "zh", "forbidden", "误译detachment：正确为 等离子体脱靶"),

    # impurity transport → 杂质输运
    ("杂质运输", "impurity-transport", "zh", "forbidden", "误译transport：聚变应为 杂质输运"),
    ("杂质传输", "impurity-transport", "zh", "deprecated", "非标准：应为 杂质输运"),

    # anomalous transport → 反常输运
    ("异常传输", "anomalous-transport", "zh", "forbidden", "误译：聚变应为 反常输运"),
    ("异常输运", "anomalous-transport", "zh", "deprecated", "非标准：应为 反常输运"),

    # wall conditioning → 壁面处理
    ("壁调节", "wall-conditioning", "zh", "deprecated", "非标准：应为 壁面处理"),

    # sputtering → 溅射
    ("飞溅", "sputtering", "zh", "forbidden", "误译sputtering：正确为 溅射"),
    ("喷射", "sputtering", "zh", "forbidden", "误译sputtering：正确为 溅射"),
    ("喷溅", "sputtering", "zh", "forbidden", "误译sputtering：正确为 溅射"),

    # blistering → 起泡
    ("水泡", "blistering", "zh", "forbidden", "误译blistering：正确为 起泡"),
    ("鼓泡", "blistering", "zh", "forbidden", "误译blistering：正确为 起泡"),

    # redeposition → 再沉积
    ("重新沉积", "redeposition", "zh", "deprecated", "啰嗦：应为 再沉积"),

    # co-deposition → 共沉积
    ("联合沉积", "co-deposition", "zh", "forbidden", "误译co-：正确为 共沉积"),
    ("共同沉积", "co-deposition", "zh", "deprecated", "啰嗦：应为 共沉积"),

    # disruption mitigation → 破裂缓解
    ("中断减缓", "disruption-mitigation", "zh", "forbidden", "双重误译：正确为 破裂缓解"),
    ("干扰缓解", "disruption-mitigation", "zh", "forbidden", "误译disruption：正确为 破裂缓解"),
    ("破裂缓冲", "disruption-mitigation", "zh", "forbidden", "误译mitigation：正确为 破裂缓解"),

    # ELM suppression → ELM抑制
    ("ELM压制", "elm-suppression", "zh", "deprecated", "非标准：应为 ELM抑制"),
    ("ELM消除", "elm-suppression", "zh", "forbidden", "概念错误：suppression≠消除"),

    # equilibrium reconstruction → 平衡重建
    ("平衡重构", "equilibrium-reconstruction", "zh", "deprecated", "非标准：应为 平衡重建"),

    # magnetic reconnection → 磁重联
    ("磁重连", "magnetic-reconnection", "zh", "deprecated", "非标准变体：应为 磁重联"),
    ("磁重新连接", "magnetic-reconnection", "zh", "forbidden", "误译：正确为 磁重联"),
    ("磁再连接", "magnetic-reconnection", "zh", "forbidden", "误译：正确为 磁重联"),

    # ========================================================================
    # 5. Materials / safety / engineering (items 86-100)
    # ========================================================================
    ("# ==== Common AI mistranslations: materials, safety, engineering ====",),

    # RAFM steel → 低活化铁素体/马氏体钢
    ("降低活化钢", "rafm-steel", "zh", "forbidden", "误译：正确为 低活化铁素体/马氏体钢"),

    # ODS steel → 氧化物弥散强化钢
    ("氧化物分散钢", "ods-steel", "zh", "forbidden", "误译dispersion：正确为 氧化物弥散强化钢"),

    # helium embrittlement → 氦脆
    ("氦脆化", "helium-embrittlement", "zh", "deprecated", "啰嗦：应为 氦脆"),

    # void swelling → 辐照肿胀
    ("空洞膨胀", "void-swelling", "zh", "forbidden", "误译void：正确为 辐照肿胀"),
    ("空位膨胀", "void-swelling", "zh", "forbidden", "误译void：正确为 辐照肿胀"),

    # LOCA → 失冷事故
    ("冷却剂丧失事故", "loss-of-coolant-accident", "zh", "deprecated", "啰嗦：应为 失冷事故"),

    # LOFA → 失流事故
    ("流量丧失事故", "loss-of-flow-accident", "zh", "deprecated", "啰嗦：应为 失流事故"),

    # decay heat → 衰变热
    ("衰减热", "decay-heat", "zh", "forbidden", "误译decay：正确为 衰变热"),

    # radiation shielding → 屏蔽
    ("辐射遮蔽", "radiation-shielding", "zh", "deprecated", "非标准：应为 屏蔽"),

    # clearance → 清洁解控
    ("间隙", "clearance", "zh", "forbidden", "误译：机械义，核安全应为 清洁解控"),

    # defense in depth → 纵深防御
    ("深度防御", "defense-in-depth", "zh", "deprecated", "非标准：应为 纵深防御"),

    # source term → 源项
    ("源术语", "source-term", "zh", "forbidden", "误译term：正确为 源项"),
    ("源条件", "source-term", "zh", "forbidden", "误译term：正确为 源项"),

    # decommissioning → 退役
    ("解除委任", "decommissioning", "zh", "forbidden", "误译commission：正确为 退役"),

    # nuclear heating → 核热
    ("核加热", "nuclear-heating", "zh", "deprecated", "啰嗦：应为 核热"),

    # safety factor → 安全因子
    ("安全系数", "safety-factor", "zh", "deprecated", "非标准：聚变(q)应为 安全因子"),

    # ========================================================================
    # 6. Additional high-frequency AI errors
    # ========================================================================
    ("# ==== Additional high-frequency AI mistranslations ====",),

    # Debye sheath → 德拜鞘
    ("德拜鞘层", "debye-sheath", "zh", "deprecated", "啰嗦：应为 德拜鞘"),

    # energy gain → 能量增益
    ("能量增长", "energy-gain", "zh", "forbidden", "误译gain：正确为 能量增益"),

    # ohmic heating → 欧姆加热
    ("电阻加热", "ohmic-heating", "zh", "deprecated", "非标准：聚变应为 欧姆加热"),

    # tearing mode → 撕裂模
    # (skip: 撕裂模式 already exists as deprecated)

    # kink mode → 扭曲模
    ("扭曲模式", "kink-mode", "zh", "deprecated", "非标准：应为 扭曲模"),

    # ballooning mode → 气球模
    ("气球模式", "ballooning-mode", "zh", "deprecated", "非标准：应为 气球模"),
    ("膨胀模", "ballooning-mode", "zh", "forbidden", "误译ballooning：正确为 气球模"),

    # neoclassical transport → 新经典输运
    ("新古典输运", "neoclassical-transport", "zh", "forbidden", "误译neoclassical：正确为 新经典输运"),
    ("新型经典输运", "neoclassical-transport", "zh", "forbidden", "误译neoclassical：正确为 新经典输运"),

    # NTM → 新经典撕裂模
    ("新古典撕裂模", "neoclassical-tearing-mode", "zh", "forbidden", "误译neoclassical：正确为 新经典撕裂模"),

    # Bohm diffusion → 玻姆扩散
    ("波姆扩散", "bohm-diffusion", "zh", "deprecated", "音译变体：应为 玻姆扩散"),
    ("博姆扩散", "bohm-diffusion", "zh", "deprecated", "音译变体：应为 玻姆扩散"),

    # turbulent transport → 湍流输运
    ("湍流传输", "turbulent-transport", "zh", "deprecated", "非标准：应为 湍流输运"),
    ("湍流运输", "turbulent-transport", "zh", "forbidden", "误译transport：正确为 湍流输运"),

    # cross-field transport → 垂直输运 (cross-field)
    ("跨场输运", "cross-field-transport", "zh", "deprecated", "非标准：应为 垂直输运 / 横向输运"),

    # drift wave → 漂移波
    ("漂流波", "drift-wave", "zh", "forbidden", "误译drift：正确为 漂移波"),

    # zonal flow → 带状流
    ("区域流", "zonal-flow", "zh", "forbidden", "误译zonal：正确为 带状流"),
    ("环带流", "zonal-flow", "zh", "deprecated", "非标准：应为 带状流"),

    # power threshold → 功率阈值
    ("功率门槛", "power-threshold", "zh", "deprecated", "非标准：应为 功率阈值"),

    # plasma shaping → 等离子体成形
    ("等离子体整形", "plasma-shaping", "zh", "forbidden", "误译shaping：正确为 等离子体成形"),

    # feedback control → 反馈控制
    ("回馈控制", "feedback-control", "zh", "deprecated", "非标准：应为 反馈控制"),

    # impurity accumulation → 杂质积聚
    ("杂质积累", "impurity-accumulation", "zh", "deprecated", "非标准：应为 杂质积聚"),
    ("杂质堆积", "impurity-accumulation", "zh", "deprecated", "非标准：应为 杂质积聚"),

    # tritium retention → 氚滞留
    ("氚保留", "tritium-retention", "zh", "forbidden", "误译retention：正确为 氚滞留"),
    ("氚残留", "tritium-retention", "zh", "deprecated", "非标准：应为 氚滞留"),

    # fuel retention → 燃料滞留
    ("燃料保留", "fuel-retention", "zh", "forbidden", "误译retention：正确为 燃料滞留"),

    # erosion → 侵蚀
    ("腐蚀", "erosion", "zh", "deprecated", "非标准：corrosion≠erosion，应为 侵蚀"),

    # thermal fatigue → 热疲劳
    ("热疲劳损伤", "thermal-fatigue", "zh", "deprecated", "啰嗦：应为 热疲劳"),

    # plasma-facing component → 面向等离子体部件
    ("等离子体面组件", "plasma-facing-component", "zh", "forbidden", "误译：正确为 面向等离子体部件"),
    ("面等离子部件", "plasma-facing-component", "zh", "forbidden", "误译：正确为 面向等离子体部件"),

    # superconducting magnet → 超导磁体
    # (skip: 超导磁铁 already exists as deprecated)

    # lower hybrid current drive → 低杂波电流驱动
    ("低混合波电流驱动", "lower-hybrid-current-drive", "zh", "forbidden", "误译hybrid：正确为 低杂波电流驱动"),
    ("低混杂波驱动", "lower-hybrid-current-drive", "zh", "forbidden", "误译：正确为 低杂波电流驱动"),

    # ECRH → 电子回旋共振加热
    ("电子环回共振加热", "electron-cyclotron-resonance-heating", "zh", "forbidden", "误译cyclotron：正确为 电子回旋共振加热"),

    # ICRH → 离子回旋共振加热
    ("离子环回共振加热", "ion-cyclotron-resonance-heating", "zh", "forbidden", "误译cyclotron：正确为 离子回旋共振加热"),

    # bootstrap current optimization → 自举电流优化
    ("引导电流优化", "bootstrap-current-optimization", "zh", "forbidden", "误译bootstrap：正确为 自举电流优化"),

    # detritiation → 去氚
    ("脱氚", "detritiation", "zh", "deprecated", "非标准：应为 去氚"),

    # Spitzer resistivity → 斯皮策电阻率
    ("斯皮泽电阻率", "spitzer-resistivity", "zh", "deprecated", "音译变体：应为 斯皮策电阻率"),

    # Larmor radius → 拉莫尔半径
    ("拉莫半径", "larmor-radius", "zh", "deprecated", "非标准：应为 拉莫尔半径"),
    ("拉莫尔回旋半径", "larmor-radius", "zh", "deprecated", "啰嗦：应为 拉莫尔半径"),

    # island divertor → 岛偏滤器
    ("岛分流器", "island-divertor", "zh", "forbidden", "误译divertor：正确为 岛偏滤器"),

    # snowflake divertor → 雪花偏滤器
    ("雪花分流器", "snowflake-divertor", "zh", "forbidden", "误译divertor：正确为 雪花偏滤器"),

    # power balance → 功率平衡
    ("电力平衡", "power-balance", "zh", "forbidden", "误译power：聚变应为 功率平衡"),

    # magnetic mirror → 磁镜
    ("磁面镜", "magnetic-mirror", "zh", "forbidden", "误译：正确为 磁镜"),

    # plasma instability → 等离子体不稳定性
    ("等离子不稳定", "plasma-instability", "zh", "deprecated", "缺字'体'：应为 等离子体不稳定性"),

    # divertor cassette → 偏滤器卡匣
    ("偏滤器盒", "divertor-cassette", "zh", "forbidden", "误译cassette：正确为 偏滤器卡匣"),

    # fueling efficiency → 加料效率
    ("加油效率", "fueling-efficiency", "zh", "forbidden", "误译fueling：聚变应为 加料效率"),
    ("供料效率", "fueling-efficiency", "zh", "deprecated", "非标准：应为 加料效率"),
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
