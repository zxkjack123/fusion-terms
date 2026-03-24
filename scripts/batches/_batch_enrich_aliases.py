#!/usr/bin/env python3
"""Batch 50b: Alias enrichment for ~280 sparse concepts.

Adds synonym/variant/abbreviation aliases to concepts that currently
have only their preferred zh + preferred en (≤2 correct aliases).
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ALIASES_TSV = ROOT / "terms" / "registry" / "aliases.tsv"

def write_tsv_rows(path: pathlib.Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:
                f.write(row[0] + "\n")
            else:
                f.write("\t".join(row) + "\n")


ENRICH = [
    # ================================================================
    #  CONCEPT category (151 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — concept ====",),

    # ablation-front
    ("烧蚀界面",         "ablation-front",       "zh", "alias", "variant"),

    # ac-loss
    ("AC loss",          "ac-loss",              "en", "alias", "capitalized"),
    ("交流损失",         "ac-loss",              "zh", "alias", "variant"),

    # activation-product
    ("放射性活化产物",   "activation-product",   "zh", "alias", "full form"),
    ("activation products", "activation-product","en", "alias", "plural"),

    # actuator
    ("致动器",           "actuator",             "zh", "alias", "variant"),

    # advanced-divertor-concept
    ("先进偏滤器",       "advanced-divertor-concept","zh","alias","short form"),

    # alfven-continuum
    ("阿尔芬连续谱",    "alfven-continuum",     "zh", "alias", "transliterated"),
    ("Alfvén连续体",     "alfven-continuum",     "zh", "alias", "variant"),

    # anomalous-transport
    ("反常输运系数",     "anomalous-transport",  "zh", "alias", "coefficient context"),

    # antenna-coupling
    ("天线耦合效率",     "antenna-coupling",     "zh", "alias", "efficiency context"),

    # avalanche-transport
    ("雪崩式输运",       "avalanche-transport",  "zh", "alias", "variant"),

    # banana-regime
    ("香蕉轨道区",       "banana-regime",        "zh", "alias", "orbit form"),
    ("banana regime",    "banana-regime",        "en", "alias", "no hyphen"),

    # blanket
    ("包层系统",         "blanket",              "zh", "alias", "system form"),

    # blistering
    ("表面起泡",         "blistering",           "zh", "alias", "surface context"),

    # bohm-diffusion
    ("玻姆扩散系数",     "bohm-diffusion",       "zh", "alias", "coefficient form"),

    # bootstrap-generation
    ("自举电流",         "bootstrap-generation", "zh", "alias", "short form"),

    # capsule-implosion — already enriched in batch 50

    # chemical-erosion
    ("化学溅射",         "chemical-erosion",     "zh", "alias", "sputtering form"),
    ("chemical sputtering","chemical-erosion",   "en", "alias", "sputtering form"),

    # clearance
    ("解控",             "clearance",            "zh", "alias", "short form"),

    # collisional-damping
    ("碰撞阻尼效应",    "collisional-damping",  "zh", "alias", "full form"),

    # condenser
    ("冷凝器",           "condenser",            "zh", "alias", "variant"),

    # construction-schedule
    ("建造计划",         "construction-schedule", "zh", "alias", "variant"),

    # continuum-radiation
    ("连续谱辐射",       "continuum-radiation",  "zh", "alias", "variant"),
    ("bremsstrahlung",   "continuum-radiation",  "en", "alias", "major component"),

    # coolant-chemistry
    ("冷却剂化学控制",   "coolant-chemistry",    "zh", "alias", "control context"),

    # coulomb-collision
    ("库仑散射",         "coulomb-collision",    "zh", "alias", "scattering form"),

    # critical-balance
    ("临界平衡假说",     "critical-balance",     "zh", "alias", "hypothesis form"),

    # critical-gradient
    ("临界梯度模型",     "critical-gradient",    "zh", "alias", "model context"),

    # current-hole
    ("电流空心",         "current-hole",         "zh", "alias", "variant"),

    # curvature-drift
    ("曲率漂移速度",     "curvature-drift",      "zh", "alias", "velocity form"),

    # d-he3-reaction
    ("氘氦三反应",       "d-he3-reaction",       "zh", "alias", "Chinese form"),
    ("D-He3 reaction",   "d-he3-reaction",       "en", "alias", "ASCII form"),

    # decommissioning
    ("退役拆除",         "decommissioning",      "zh", "alias", "full form"),

    # defense-in-depth
    ("纵深防御原则",     "defense-in-depth",     "zh", "alias", "principle form"),
    ("DiD",              "defense-in-depth",     "abbr","alias", "abbreviation"),

    # density-peaking
    ("密度峰化因子",     "density-peaking",      "zh", "alias", "factor form"),

    # density-pump-out
    ("密度抽空",         "density-pump-out",     "zh", "alias", "variant"),

    # deposition
    ("沉积层",           "deposition",           "zh", "alias", "layer form"),

    # detachment-front
    ("脱靶锋面",         "detachment-front",     "zh", "alias", "variant"),

    # diamagnetic-drift
    ("抗磁漂移速度",     "diamagnetic-drift",    "zh", "alias", "velocity form"),

    # digital-twin
    ("数字孪生体",       "digital-twin",         "zh", "alias", "entity form"),

    # disruption-erosion
    ("破裂侵蚀量",       "disruption-erosion",   "zh", "alias", "quantity form"),

    # divertor
    ("分流器",           "divertor",             "zh", "alias", "literary variant"),

    # doppler-broadening
    ("多普勒加宽",       "doppler-broadening",   "zh", "alias", "variant"),

    # drift-wave
    ("漂移波不稳定性",   "drift-wave",           "zh", "alias", "instability form"),
    ("drift-wave instability","drift-wave",      "en", "alias", "instability form"),

    # dust-generation
    ("粉尘生成",         "dust-generation",      "zh", "alias", "variant"),

    # dust-transport
    ("粉尘迁移",         "dust-transport",       "zh", "alias", "variant"),

    # eddy-current
    ("涡电流",           "eddy-current",         "zh", "alias", "variant"),
    ("eddy currents",    "eddy-current",         "en", "alias", "plural"),

    # electromagnetic-force
    ("电磁力载荷",       "electromagnetic-force", "zh", "alias", "load form"),
    ("EM force",         "electromagnetic-force", "en", "alias", "short form"),

    # elm-induced-erosion
    ("ELM侵蚀",         "elm-induced-erosion",  "zh", "alias", "short form"),

    # error-field
    ("误差磁场",         "error-field",          "zh", "alias", "full form"),
    ("error field correction","error-field",     "en", "alias", "correction form"),

    # extended-mhd
    ("扩展磁流体力学",   "extended-mhd",         "zh", "alias", "full form"),

    # flux-amplification
    ("磁通放大系数",     "flux-amplification",   "zh", "alias", "coefficient form"),

    # flux-expansion
    ("磁通膨胀率",       "flux-expansion",       "zh", "alias", "rate form"),

    # fokker-planck-equation
    ("福克-普朗克方程",  "fokker-planck-equation","zh", "alias", "transliterated"),

    # force-free-equilibrium
    ("无力场平衡",       "force-free-equilibrium","zh","alias", "variant"),

    # frenkel-pair
    ("弗伦克尔缺陷对",   "frenkel-pair",         "zh", "alias", "transliterated"),
    ("Frenkel defect pair","frenkel-pair",       "en", "alias", "expanded"),

    # friction-force
    ("摩擦力矩",         "friction-force",       "zh", "alias", "torque form"),

    # fuel-pellet
    ("燃料芯丸",         "fuel-pellet",          "zh", "alias", "variant"),
    ("fuel pellets",     "fuel-pellet",          "en", "alias", "plural"),

    # fully-non-inductive
    ("全非感应运行",     "fully-non-inductive",  "zh", "alias", "short form"),

    # fusion-product-spectrum
    ("聚变产物谱",       "fusion-product-spectrum","zh","alias", "short form"),

    # gain-curve
    ("增益特性曲线",     "gain-curve",           "zh", "alias", "full form"),

    # gas-balance
    ("气体平衡分析",     "gas-balance",          "zh", "alias", "analysis form"),

    # grad-b-drift
    ("梯度B漂移",        "grad-b-drift",         "zh", "alias", "variant"),
    ("gradient-B drift", "grad-b-drift",         "en", "alias", "expanded"),

    # halo-current
    ("晕电流分布",       "halo-current",         "zh", "alias", "distribution form"),
    ("halo currents",    "halo-current",         "en", "alias", "plural"),

    # helium-embrittlement
    ("氦脆化",           "helium-embrittlement", "zh", "alias", "variant"),

    # i-mode
    ("I-mode",           "i-mode",               "en", "alias", "hyphenated"),
    ("I模态",            "i-mode",               "zh", "alias", "variant"),

    # impurity-accumulation
    ("杂质聚集",         "impurity-accumulation","zh", "alias", "variant"),

    # impurity-source
    ("杂质源强度",       "impurity-source",      "zh", "alias", "strength form"),

    # interstitial-atom
    ("间隙缺陷",         "interstitial-atom",    "zh", "alias", "defect form"),
    ("interstitial",     "interstitial-atom",    "en", "alias", "short form"),

    # irradiation-creep
    ("辐照蠕变速率",     "irradiation-creep",    "zh", "alias", "rate form"),

    # irradiation-embrittlement
    ("辐照脆化温度",     "irradiation-embrittlement","zh","alias","temperature form"),
    ("radiation embrittlement","irradiation-embrittlement","en","alias","synonym"),

    # isotope-effect
    ("同位素效应系数",   "isotope-effect",       "zh", "alias", "coefficient form"),

    # laser-energy-balance
    ("激光能量守恒",     "laser-energy-balance", "zh", "alias", "conservation form"),

    # limiter
    ("限制器结构",       "limiter",              "zh", "alias", "structural form"),

    # line-radiation
    ("线谱辐射",         "line-radiation",       "zh", "alias", "spectral form"),

    # locked-mode
    ("锁模不稳定性",     "locked-mode",          "zh", "alias", "instability form"),

    # long-leg-divertor
    ("长腿型偏滤器",     "long-leg-divertor",    "zh", "alias", "variant"),

    # magnetic-axis
    ("磁轴位置",         "magnetic-axis",        "zh", "alias", "position context"),

    # magnetic-helicity
    ("磁螺旋度守恒",     "magnetic-helicity",    "zh", "alias", "conservation form"),

    # magnetic-self-organization
    ("磁自组织现象",     "magnetic-self-organization","zh","alias","phenomenon form"),

    # marfe
    ("边缘辐射不稳定性", "marfe",                "zh", "alias", "descriptive"),
    ("Multifaceted Asymmetric Radiation From the Edge","marfe","en","alias","full expansion"),

    # melt-damage
    ("熔化损坏",         "melt-damage",          "zh", "alias", "variant"),

    # micro-tearing-mode
    ("微撕裂模不稳定性", "micro-tearing-mode",   "zh", "alias", "instability form"),
    ("MTM",              "micro-tearing-mode",   "abbr","alias","abbreviation"),

    # mix-instability
    ("混合不稳定性模",   "mix-instability",      "zh", "alias", "mode form"),

    # mode-conversion
    ("模式转化",         "mode-conversion",      "zh", "alias", "variant"),

    # momentum-transport
    ("动量输运系数",     "momentum-transport",   "zh", "alias", "coefficient form"),

    # multipactor
    ("multipactor discharge","multipactor",      "en", "alias", "full form"),
    ("二次电子倍增",     "multipactor",          "zh", "alias", "short form"),

    # neoclassical-impurity-transport
    ("新经典杂质输运系数","neoclassical-impurity-transport","zh","alias","coefficient"),

    # neutronics
    ("中子学分析",       "neutronics",           "zh", "alias", "analysis form"),
    ("neutronics analysis","neutronics",         "en", "alias", "analysis form"),

    # nonlinear-coupling
    ("非线性耦合效应",   "nonlinear-coupling",   "zh", "alias", "effect form"),

    # nuclear-data-library
    ("核数据库文件",     "nuclear-data-library", "zh", "alias", "file form"),

    # nuclear-response-function
    ("核响应函数谱",     "nuclear-response-function","zh","alias","spectrum form"),

    # outgassing
    ("出气率",           "outgassing",           "zh", "alias", "rate form"),
    ("放气",             "outgassing",           "zh", "alias", "variant"),

    # parallel-transport
    ("平行方向输运",     "parallel-transport",   "zh", "alias", "directional form"),

    # parametric-instability
    ("参量不稳定性",     "parametric-instability","zh","alias", "variant"),
    ("parametric decay","parametric-instability","en", "alias", "decay form"),

    # pedestal
    ("台基区",           "pedestal",             "zh", "alias", "region form"),
    ("H模台基",          "pedestal",             "zh", "alias", "H-mode form"),

    # pellet-ablation
    ("弹丸烧蚀速率",    "pellet-ablation",      "zh", "alias", "rate form"),

    # physical-sputtering
    ("物理溅射产额",     "physical-sputtering",  "zh", "alias", "yield form"),
    ("physical sputtering yield","physical-sputtering","en","alias","yield form"),

    # plasma
    ("等离子体物理",     "plasma",               "zh", "alias", "physics form"),

    # plateau-regime
    ("坪区输运",         "plateau-regime",       "zh", "alias", "transport form"),

    # poloidal-asymmetry
    ("极向非对称",       "poloidal-asymmetry",   "zh", "alias", "variant"),

    # power-degradation
    ("功率退化效应",     "power-degradation",    "zh", "alias", "effect form"),

    # power-deposition-profile
    ("功率沉积剖面",     "power-deposition-profile","zh","alias","variant"),

    # predator-prey-oscillation
    ("捕食-被食振荡",    "predator-prey-oscillation","zh","alias","variant"),

    # presheath
    ("预鞘层",           "presheath",            "zh", "alias", "variant"),

    # pressure-pedestal
    ("压力台基",         "pressure-pedestal",    "zh", "alias", "variant"),

    # profile-stiffness
    ("剖面刚度",         "profile-stiffness",    "zh", "alias", "variant"),

    # prompt-redeposition
    ("即时再沉积效应",   "prompt-redeposition",  "zh", "alias", "effect form"),

    # prototype-reactor
    ("原型反应堆",       "prototype-reactor",    "zh", "alias", "full form"),

    # quench
    ("失超事件",         "quench",               "zh", "alias", "event form"),
    ("quench event",     "quench",               "en", "alias", "event form"),

    # radiation-barrier
    ("辐射势垒",         "radiation-barrier",    "zh", "alias", "potential form"),

    # radiation-collapse
    ("辐射坍塌事件",     "radiation-collapse",   "zh", "alias", "event form"),

    # radiation-dominated-regime
    ("辐射主导区",       "radiation-dominated-regime","zh","alias","short form"),

    # radiation-hardening
    ("辐照硬化效应",     "radiation-hardening",  "zh", "alias", "effect form"),

    # recombination-radiation
    ("复合辐射谱",       "recombination-radiation","zh","alias","spectrum form"),

    # recrystallization
    ("再结晶温度",       "recrystallization",    "zh", "alias", "temperature form"),

    # recycling
    ("再循环系数",       "recycling",            "zh", "alias", "coefficient form"),

    # redeposition
    ("再沉积层",         "redeposition",         "zh", "alias", "layer form"),

    # reduced-mhd
    ("约化磁流体力学",   "reduced-mhd",          "zh", "alias", "full form"),

    # regulatory-approval
    ("监管审批",         "regulatory-approval",   "zh", "alias", "variant"),

    # rotation-reversal
    ("旋转反向",         "rotation-reversal",    "zh", "alias", "variant"),

    # safety-classification
    ("安全等级划分",     "safety-classification", "zh", "alias", "variant"),

    # sawtooth-crash
    ("锯齿崩溃",         "sawtooth-crash",       "zh", "alias", "variant"),

    # size-scaling
    ("尺寸标度律",       "size-scaling",         "zh", "alias", "law form"),
    ("size scaling law", "size-scaling",         "en", "alias", "law form"),

    # slow-wave
    ("慢波结构",         "slow-wave",            "zh", "alias", "structure form"),

    # snowflake-divertor
    ("雪花型偏滤器",     "snowflake-divertor",   "zh", "alias", "variant"),

    # source-term
    ("放射性源项",       "source-term",          "zh", "alias", "radioactive form"),

    # spectral-transfer
    ("能谱传递",         "spectral-transfer",    "zh", "alias", "variant"),

    # staircase-transport
    ("阶梯式输运",       "staircase-transport",  "zh", "alias", "variant"),

    # stark-broadening
    ("斯塔克加宽",       "stark-broadening",     "zh", "alias", "variant"),

    # steady-state-high-beta
    ("稳态高比压运行",   "steady-state-high-beta","zh", "alias", "variant"),

    # strain-sensitivity
    ("应变敏感度",       "strain-sensitivity",   "zh", "alias", "variant"),

    # strike-point
    ("打击点位置",       "strike-point",         "zh", "alias", "position form"),

    # subcritical-turbulence
    ("亚临界湍流激发",   "subcritical-turbulence","zh", "alias", "excitation form"),

    # super-h-mode
    ("Super H模",        "super-h-mode",         "zh", "alias", "variant"),
    ("super H-mode",     "super-h-mode",         "en", "alias", "variant"),

    # super-x-divertor
    ("Super-X偏滤器结构","super-x-divertor",     "zh", "alias", "structural form"),

    # supply-chain
    ("供应链管理",       "supply-chain",         "zh", "alias", "management form"),

    # surface-roughening
    ("表面粗化",         "surface-roughening",   "zh", "alias", "variant"),

    # taylor-relaxation
    ("泰勒弛豫",         "taylor-relaxation",    "zh", "alias", "transliterated"),

    # taylor-state
    ("泰勒态",           "taylor-state",         "zh", "alias", "transliterated"),

    # temperature-pedestal
    ("温度台基区",       "temperature-pedestal", "zh", "alias", "region form"),

    # thermal-fatigue
    ("热疲劳裂纹",       "thermal-fatigue",      "zh", "alias", "crack form"),

    # thermal-force
    ("热梯度力",         "thermal-force",        "zh", "alias", "gradient form"),

    # thermal-shock
    ("热冲击损伤",       "thermal-shock",        "zh", "alias", "damage form"),

    # tokamak
    ("托卡马克装置",     "tokamak",              "zh", "alias", "device form"),

    # trapped-particle
    ("俘获粒子效应",     "trapped-particle",     "zh", "alias", "effect form"),
    ("trapped particles","trapped-particle",     "en", "alias", "plural"),

    # tritium-accountancy
    ("氚账目管理",       "tritium-accountancy",  "zh", "alias", "management form"),

    # turbulence-saturation
    ("湍流饱和水平",     "turbulence-saturation","zh", "alias", "level form"),

    # turbulence-spreading
    ("湍流扩散",         "turbulence-spreading", "zh", "alias", "variant"),

    # turbulence-suppression
    ("湍流抑制机制",     "turbulence-suppression","zh","alias", "mechanism form"),

    # two-fluid-model
    ("二流体模型",       "two-fluid-model",      "zh", "alias", "variant"),

    # vacancy
    ("空位缺陷",         "vacancy",              "zh", "alias", "defect form"),
    ("vacancy defect",   "vacancy",              "en", "alias", "defect form"),

    # vapor-shielding
    ("蒸汽屏蔽效应",     "vapor-shielding",      "zh", "alias", "effect form"),

    # vertical-stability
    ("垂直稳定控制",     "vertical-stability",   "zh", "alias", "control form"),
    ("VDE",              "vertical-stability",   "abbr","alias", "linked to VDE instability"),

    # vlasov-equation
    ("弗拉索夫方程",     "vlasov-equation",      "zh", "alias", "transliterated"),

    # ================================================================
    #  DIAGNOSTIC category (8 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — diagnostic ====",),

    # diamagnetic-loop
    ("抗磁环诊断",       "diamagnetic-loop",     "zh", "alias", "diagnostic form"),

    # impurity-spectroscopy
    ("杂质光谱诊断",     "impurity-spectroscopy","zh", "alias", "diagnostic form"),

    # magnetic-flux-loop
    ("磁通量环",         "magnetic-flux-loop",   "zh", "alias", "variant"),

    # mirnov-coil
    ("Mirnov线圈",       "mirnov-coil",          "zh", "alias", "mixed form"),
    ("Mirnov probe",     "mirnov-coil",          "en", "alias", "probe form"),

    # reflectometry
    ("反射计诊断",       "reflectometry",        "zh", "alias", "diagnostic form"),
    ("microwave reflectometry","reflectometry",  "en", "alias", "microwave form"),

    # rogowski-coil
    ("Rogowski线圈",     "rogowski-coil",        "zh", "alias", "mixed form"),

    # spectroscopy
    ("光谱学",           "spectroscopy",         "zh", "alias", "science form"),
    ("光谱分析",         "spectroscopy",         "zh", "alias", "analysis form"),

    # thomson-scattering
    ("汤姆逊散射",       "thomson-scattering",   "zh", "alias", "preferred zh"),
    ("汤姆森散射",       "thomson-scattering",   "zh", "alias", "variant transliteration"),
    ("TS",               "thomson-scattering",   "abbr","alias", "abbreviation"),
    ("Thomson scattering diagnostic","thomson-scattering","en","alias","diagnostic form"),

    # ================================================================
    #  EFFECT category (1 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — effect ====",),

    # ware-pinch
    ("Ware箍缩",         "ware-pinch",           "zh", "alias", "mixed form"),
    ("Ware pinch effect","ware-pinch",           "en", "alias", "effect form"),

    # ================================================================
    #  LIMIT category (1 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — limit ====",),

    # occupational-dose-limit
    ("职业照射限值",     "occupational-dose-limit","zh","alias", "variant"),

    # ================================================================
    #  MATERIAL category (11 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — material ====",),

    # clam
    ("CLAM钢",           "clam",                 "zh", "alias", "steel qualifier"),
    ("China Low Activation Martensitic steel","clam","en","alias","full expansion"),

    # clf-1
    ("CLF-1钢",          "clf-1",                "zh", "alias", "steel qualifier"),

    # cucrzr
    ("铜铬锆合金",       "cucrzr",               "zh", "alias", "Chinese name"),
    ("copper chromium zirconium","cucrzr",       "en", "alias", "full name"),

    # eurofer
    ("EUROFER钢",        "eurofer",              "zh", "alias", "steel qualifier"),
    ("EUROFER97",        "eurofer",              "en", "alias", "versioned form"),

    # f82h
    ("F82H钢",           "f82h",                 "zh", "alias", "steel qualifier"),

    # functional-material
    ("功能性材料",       "functional-material",  "zh", "alias", "variant"),

    # graphite
    ("石墨材料",         "graphite",             "zh", "alias", "material form"),
    ("carbon",           "graphite",             "en", "alias", "element synonym"),

    # insulation-material
    ("绝缘材料体系",     "insulation-material",  "zh", "alias", "system form"),

    # nb3sn
    ("铌三锡",           "nb3sn",                "zh", "alias", "Chinese name"),
    ("Nb₃Sn",            "nb3sn",                "en", "alias", "subscript form"),

    # rebco
    ("REBCO超导带材",    "rebco",                "zh", "alias", "conductor form"),
    ("rare-earth barium copper oxide","rebco",   "en", "alias", "full expansion"),

    # tungsten
    ("钨",               "tungsten",             "zh", "alias", "Chinese name"),
    ("tungsten",         "tungsten",             "en", "alias", "full name"),

    # ================================================================
    #  METHOD category (34 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — method ====",),

    # bayesian-inference
    ("贝叶斯推理",       "bayesian-inference",   "zh", "alias", "variant"),

    # boronization
    ("硼化处理",         "boronization",         "zh", "alias", "treatment form"),

    # burn-control
    ("聚变燃烧控制",     "burn-control",         "zh", "alias", "fusion context"),

    # component-qualification
    ("部件认证",         "component-qualification","zh","alias","variant"),

    # cryogenic-distillation
    ("低温蒸馏分离",     "cryogenic-distillation","zh","alias","separation form"),

    # data-driven-control
    ("数据驱动控制方法", "data-driven-control",  "zh", "alias", "method form"),

    # delta-f-method
    ("δf方法",           "delta-f-method",       "zh", "alias", "symbol form"),
    ("delta-f simulation","delta-f-method",      "en", "alias", "simulation form"),

    # detachment-control
    ("脱靶控制技术",     "detachment-control",   "zh", "alias", "technique form"),

    # divertor-replacement
    ("偏滤器更换操作",   "divertor-replacement", "zh", "alias", "operation form"),

    # dose-rate-survey
    ("剂量率巡检",       "dose-rate-survey",     "zh", "alias", "variant"),

    # feedback-control
    ("反馈控制系统",     "feedback-control",     "zh", "alias", "system form"),

    # full-f-method
    ("全f模拟方法",      "full-f-method",        "zh", "alias", "simulation form"),
    ("full-f simulation","full-f-method",        "en", "alias", "simulation form"),

    # full-wave-simulation
    ("全波模拟方法",     "full-wave-simulation", "zh", "alias", "method form"),

    # gap-control
    ("间隙控制系统",     "gap-control",          "zh", "alias", "system form"),

    # helicon-current-drive
    ("螺旋波电流驱动技术","helicon-current-drive","zh","alias","technique form"),
    ("HCD",              "helicon-current-drive","abbr","alias","abbreviation"),

    # in-bore-welding
    ("孔内对接焊",       "in-bore-welding",      "zh", "alias", "variant"),

    # integrated-commissioning
    ("综合调试验收",     "integrated-commissioning","zh","alias","acceptance form"),

    # kinetic-control
    ("动理学控制方法",   "kinetic-control",      "zh", "alias", "method form"),

    # ml-disruption-prediction
    ("机器学习破裂预警", "ml-disruption-prediction","zh","alias","warning form"),

    # neural-network-transport
    ("神经网络输运替代模型","neural-network-transport","zh","alias","surrogate form"),

    # pipe-cutting
    ("管道切断",         "pipe-cutting",         "zh", "alias", "variant"),

    # plasma-spray-coating
    ("等离子喷涂涂层",   "plasma-spray-coating", "zh", "alias", "coating form"),

    # plasma-sprayed-tungsten
    ("等离子喷涂钨涂层", "plasma-sprayed-tungsten","zh","alias","coating form"),

    # plasma-state-estimation
    ("等离子体状态重建", "plasma-state-estimation","zh","alias","reconstruction form"),

    # ray-tracing
    ("射线追踪方法",     "ray-tracing",          "zh", "alias", "method form"),
    ("ray tracing",      "ray-tracing",          "en", "alias", "no hyphen"),

    # remote-inspection
    ("远程巡检",         "remote-inspection",    "zh", "alias", "variant"),

    # scheduled-maintenance
    ("定期维护",         "scheduled-maintenance","zh", "alias", "variant"),

    # siliconization
    ("硅化处理",         "siliconization",       "zh", "alias", "treatment form"),

    # surrogate-model
    ("替代模型",         "surrogate-model",      "zh", "alias", "variant"),

    # synthetic-diagnostics
    ("合成诊断方法",     "synthetic-diagnostics","zh", "alias", "method form"),

    # thermo-mechanical-analysis
    ("热力学-机械分析",  "thermo-mechanical-analysis","zh","alias","variant"),
    ("TMA",              "thermo-mechanical-analysis","abbr","alias","abbreviation"),

    # tritium-removal
    ("去氚",             "tritium-removal",      "zh", "alias", "short form"),
    ("detritiation",     "tritium-removal",      "en", "alias", "synonym"),

    # wall-conditioning
    ("壁处理",           "wall-conditioning",    "zh", "alias", "short form"),
    ("wall conditioning technique","wall-conditioning","en","alias","technique form"),

    # workflow-automation
    ("工作流自动化系统", "workflow-automation",  "zh", "alias", "system form"),

    # ================================================================
    #  METRIC category (41 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — metric ====",),

    # antenna-loading
    ("天线负载阻抗",     "antenna-loading",      "zh", "alias", "impedance form"),

    # aspect-ratio
    ("纵横比参数",       "aspect-ratio",         "zh", "alias", "parameter form"),
    ("A",                "aspect-ratio",         "en", "alias", "symbol"),

    # availability
    ("可用率指标",       "availability",         "zh", "alias", "metric form"),

    # base-pressure
    ("本底真空",         "base-pressure",        "zh", "alias", "vacuum form"),

    # beta-n
    ("归一化比压",       "beta-n",               "zh", "alias", "Chinese name"),
    ("normalized beta",  "beta-n",               "en", "alias", "full name"),
    ("βN",               "beta-n",               "en", "alias", "Greek symbol"),

    # bootstrap-fraction
    ("自举份额",         "bootstrap-fraction",   "zh", "alias", "short form"),

    # bounce-frequency
    ("弹跳频率周期",     "bounce-frequency",     "zh", "alias", "period form"),

    # burn-fraction
    ("燃烧份额比",       "burn-fraction",        "zh", "alias", "ratio form"),

    # clearance-index
    ("清洁解控指标",     "clearance-index",      "zh", "alias", "variant"),

    # component-lifetime
    ("部件使用寿命",     "component-lifetime",   "zh", "alias", "usage form"),

    # contact-dose-rate
    ("接触剂量率限值",   "contact-dose-rate",    "zh", "alias", "limit form"),

    # convergence-ratio
    ("汇聚比",           "convergence-ratio",    "zh", "alias", "short form"),
    ("CR",               "convergence-ratio",    "abbr","alias", "abbreviation"),

    # coulomb-logarithm
    ("库仑对数值",       "coulomb-logarithm",    "zh", "alias", "value form"),
    ("ln Λ",             "coulomb-logarithm",    "en", "alias", "formula notation"),

    # current-drive-efficiency
    ("电流驱动效率系数", "current-drive-efficiency","zh","alias","coefficient form"),

    # decommissioning-cost
    ("退役成本",         "decommissioning-cost", "zh", "alias", "variant"),

    # density-limit
    ("Greenwald密度极限","density-limit",        "zh", "alias", "Greenwald form"),
    ("Greenwald limit",  "density-limit",        "en", "alias", "Greenwald form"),

    # divertor-heat-flux
    ("偏滤器热流",       "divertor-heat-flux",   "zh", "alias", "short form"),

    # fatigue-life
    ("疲劳寿命周期",     "fatigue-life",         "zh", "alias", "cycle form"),

    # fueling-efficiency
    ("加料效率指标",     "fueling-efficiency",   "zh", "alias", "metric form"),

    # gas-production-rate
    ("气体产生率",       "gas-production-rate",  "zh", "alias", "variant"),

    # ignition-temperature
    ("聚变点火温度",     "ignition-temperature", "zh", "alias", "fusion form"),

    # implosion-velocity
    ("内爆速度参数",     "implosion-velocity",   "zh", "alias", "parameter form"),

    # impurity-influx
    ("杂质流入率",       "impurity-influx",      "zh", "alias", "rate form"),

    # joint-resistance
    ("接头电阻值",       "joint-resistance",     "zh", "alias", "value form"),

    # kerma
    ("比释动能系数",     "kerma",                "zh", "alias", "coefficient form"),
    ("KERMA",            "kerma",                "en", "alias", "uppercase"),

    # learning-rate
    ("学习速率",         "learning-rate",        "zh", "alias", "variant"),

    # magnet-bore
    ("磁体内径",         "magnet-bore",          "zh", "alias", "variant"),

    # magnetic-shear
    ("磁剪切参数",       "magnetic-shear",       "zh", "alias", "parameter form"),

    # neutral-pressure
    ("中性气体压力",     "neutral-pressure",     "zh", "alias", "full form"),

    # neutron-flux
    ("中子注量率",       "neutron-flux",         "zh", "alias", "fluence rate form"),

    # neutron-yield
    ("中子产额率",       "neutron-yield",        "zh", "alias", "rate form"),

    # pedestal-width
    ("台基宽度参数",     "pedestal-width",       "zh", "alias", "parameter form"),

    # pinch-parameter
    ("箍缩参数值",       "pinch-parameter",      "zh", "alias", "value form"),

    # plasma-frequency
    ("等离子体振荡频率", "plasma-frequency",     "zh", "alias", "oscillation form"),

    # power-density
    ("功率密度分布",     "power-density",        "zh", "alias", "distribution form"),

    # q-value-reaction
    ("反应Q值",          "q-value-reaction",     "zh", "alias", "variant"),

    # q95
    ("95%磁通面安全因子","q95",                  "zh", "alias", "descriptive"),

    # recycling-coefficient
    ("再循环系数值",     "recycling-coefficient","zh", "alias", "value form"),

    # shafranov-shift
    ("沙弗拉诺夫位移量","shafranov-shift",      "zh", "alias", "amount form"),
    ("Shafranov位移",    "shafranov-shift",      "zh", "alias", "mixed form"),

    # tritium-retention
    ("氚滞留量",         "tritium-retention",    "zh", "alias", "quantity form"),

    # troyon-limit
    ("Troyon限制",       "troyon-limit",         "zh", "alias", "variant"),
    ("Troyon beta limit","troyon-limit",         "en", "alias", "beta form"),

    # ================================================================
    #  SYSTEM category (34 sparse)
    # ================================================================
    ("# ==== Batch 50b: alias enrichment — system ====",),

    # activation-foil
    ("活化箔片",         "activation-foil",      "zh", "alias", "variant"),

    # actively-cooled-component
    ("主动冷却部件结构", "actively-cooled-component","zh","alias","structural form"),

    # armor-tile
    ("装甲瓦片",         "armor-tile",           "zh", "alias", "variant"),
    ("armour tile",      "armor-tile",           "en", "alias", "British spelling"),

    # articulated-boom
    ("铰接臂机构",       "articulated-boom",     "zh", "alias", "mechanism form"),

    # back-plate
    ("背板结构",         "back-plate",           "zh", "alias", "structural form"),

    # baffle
    ("挡板结构",         "baffle",               "zh", "alias", "structural form"),

    # blanket-module
    ("包层组件",         "blanket-module",       "zh", "alias", "variant"),

    # braze-joint
    ("钎焊接头连接",     "braze-joint",          "zh", "alias", "connection form"),
    ("brazed joint",     "braze-joint",          "en", "alias", "past participle"),

    # breeding-zone
    ("增殖区域",         "breeding-zone",        "zh", "alias", "variant"),

    # closed-divertor
    ("封闭型偏滤器",     "closed-divertor",      "zh", "alias", "variant"),

    # coolant-manifold
    ("冷却歧管系统",     "coolant-manifold",     "zh", "alias", "system form"),

    # cooling-channel
    ("冷却流道",         "cooling-channel",      "zh", "alias", "variant"),

    # demountable-joint
    ("可拆卸连接",       "demountable-joint",    "zh", "alias", "connection form"),

    # divertor-baffle
    ("偏滤器挡板结构",   "divertor-baffle",      "zh", "alias", "structural form"),

    # divertor-cassette
    ("偏滤器盒体",       "divertor-cassette",    "zh", "alias", "variant"),

    # divertor-dome
    ("偏滤器穹顶板",     "divertor-dome",        "zh", "alias", "plate form"),

    # divertor-pumping
    ("偏滤器抽气系统",   "divertor-pumping",     "zh", "alias", "system form"),

    # equatorial-port
    ("赤道窗口端口",     "equatorial-port",      "zh", "alias", "port form"),

    # flux-conserver
    ("磁通守恒壁",       "flux-conserver",       "zh", "alias", "wall form"),

    # gas-injection-valve
    ("充气阀",           "gas-injection-valve",  "zh", "alias", "variant"),

    # heat-sink
    ("散热器",           "heat-sink",            "zh", "alias", "variant"),

    # hypervapotron
    ("超蒸发冷却管",     "hypervapotron",        "zh", "alias", "cooling form"),

    # liquid-metal-divertor
    ("液态金属偏滤器靶", "liquid-metal-divertor","zh", "alias", "target form"),

    # lithium-wall
    ("锂壁面板",         "lithium-wall",         "zh", "alias", "panel form"),

    # magnet-cooling
    ("磁体冷却系统",     "magnet-cooling",       "zh", "alias", "system form"),

    # magnet-structure
    ("磁体支撑结构",     "magnet-structure",     "zh", "alias", "support form"),

    # maintenance-port
    ("维护端口",         "maintenance-port",     "zh", "alias", "variant"),

    # pellet-guide-tube
    ("弹丸输运管",       "pellet-guide-tube",    "zh", "alias", "transport form"),

    # port-plug
    ("端口模块",         "port-plug",            "zh", "alias", "variant"),

    # swirl-tube
    ("旋流冷却管",       "swirl-tube",           "zh", "alias", "cooling form"),

    # tungsten-monoblock
    ("钨单块结构",       "tungsten-monoblock",   "zh", "alias", "structural form"),

    # vacuum-pumping
    ("真空抽气系统",     "vacuum-pumping",       "zh", "alias", "system form"),

    # waveguide
    ("波导管",           "waveguide",            "zh", "alias", "pipe form"),
    ("微波波导",         "waveguide",            "zh", "alias", "microwave form"),

    # winding-pack
    ("绕组包体",         "winding-pack",         "zh", "alias", "body form"),
]


def main():
    # Load existing alias texts for dedup
    existing = set()
    with open(ALIASES_TSV) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                existing.add((parts[0].lower(), parts[1]))

    comment_rows = [r for r in ENRICH if len(r) == 1]

    # Filter out duplicates
    to_write = []
    skipped = 0
    for row in ENRICH:
        if len(row) == 1:
            to_write.append(row)
            continue
        key = (row[0].lower(), row[1])
        if key in existing:
            skipped += 1
            continue
        existing.add(key)
        to_write.append(row)

    new_data = [r for r in to_write if len(r) > 1]
    write_tsv_rows(ALIASES_TSV, to_write)
    print(f"Alias enrichment: wrote {len(new_data)} new aliases ({skipped} duplicates skipped)")
    print(f"Comment rows: {len(comment_rows)}")


if __name__ == "__main__":
    main()
