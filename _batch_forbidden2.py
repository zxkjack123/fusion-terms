#!/usr/bin/env python3
"""Batch 2: forbidden/deprecated aliases for AI mistranslations (concepts 50-100 from catalog)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

# Format: (wrong_text, correct_concept_id, lang, role, note)
# Skipped concepts not in registry: skin-current, whistler-wave, ece-radiometer,
# magnetic-probe, interspace, module-transporter, radiation-damage, getter, self-heating
WRONG_ALIASES = [
    # ========================================================================
    # A. 等离子体物理·基础量
    # ========================================================================
    ("# ==== Batch 2A: plasma physics fundamentals ====",),

    # Alfvén eigenmode → 阿尔芬本征模
    ("阿尔文特征模", "alfven-eigenmode", "zh", "forbidden", "误译eigenmode：正确为 阿尔芬本征模"),
    ("阿尔芬固有模", "alfven-eigenmode", "zh", "forbidden", "误译eigenmode：正确为 阿尔芬本征模"),
    ("阿尔文本征模", "alfven-eigenmode", "zh", "deprecated", "音译变体：应为 阿尔芬本征模"),

    # Alfvén continuum → Alfvén连续谱
    ("阿尔芬连续体", "alfven-continuum", "zh", "forbidden", "误译continuum：正确为 Alfvén连续谱"),
    ("Alfvén连续介质", "alfven-continuum", "zh", "forbidden", "误译continuum：正确为 Alfvén连续谱"),

    # banana orbit → 香蕉轨道
    ("香蕉环道", "banana-orbit", "zh", "forbidden", "误译orbit：正确为 香蕉轨道"),
    ("香蕉弹道", "banana-orbit", "zh", "forbidden", "误译orbit：正确为 香蕉轨道"),

    # collisionality → 碰撞率
    ("碰撞性", "collisionality", "zh", "forbidden", "误译-ality：正确为 碰撞率"),
    ("碰撞度", "collisionality", "zh", "forbidden", "误译-ality：正确为 碰撞率"),

    # Coulomb collision → 库仑碰撞
    ("库伦碰撞", "coulomb-collision", "zh", "deprecated", "音译变体：应为 库仑碰撞"),
    ("库仑冲突", "coulomb-collision", "zh", "forbidden", "误译collision：正确为 库仑碰撞"),

    # Coulomb logarithm → 库仑对数
    ("库伦对数", "coulomb-logarithm", "zh", "deprecated", "音译变体：应为 库仑对数"),

    # curvature drift → 曲率漂移
    ("弯曲漂移", "curvature-drift", "zh", "forbidden", "误译curvature：正确为 曲率漂移"),
    ("曲率偏移", "curvature-drift", "zh", "forbidden", "误译drift：正确为 曲率漂移"),

    # Debye length → 德拜长度
    ("德拜距离", "debye-length", "zh", "forbidden", "误译length：正确为 德拜长度"),

    # density limit → 密度极限
    ("密度限制", "density-limit", "zh", "forbidden", "误译limit：聚变应为 密度极限"),
    ("密度上限", "density-limit", "zh", "forbidden", "误译limit：聚变应为 密度极限"),

    # grad-B drift → 梯度B漂移
    ("磁场梯度偏移", "grad-b-drift", "zh", "forbidden", "误译drift：正确为 梯度B漂移"),
    ("梯度B偏移", "grad-b-drift", "zh", "forbidden", "误译drift：正确为 梯度B漂移"),

    # interchange instability → 交换不稳定性
    ("互换不稳定", "interchange-instability", "zh", "forbidden", "误译interchange：正确为 交换不稳定性"),
    ("替换不稳定性", "interchange-instability", "zh", "forbidden", "误译interchange：正确为 交换不稳定性"),
    ("交替不稳定性", "interchange-instability", "zh", "forbidden", "误译interchange：正确为 交换不稳定性"),

    # ITG mode → 离子温度梯度模 (concept id: itg-mode)
    ("离子温度梯度模式", "itg-mode", "zh", "deprecated", "非标准：应为 离子温度梯度模"),
    ("ITG模式", "itg-mode", "zh", "deprecated", "非标准：应为 ITG模 或 离子温度梯度模"),

    # Shafranov shift → 沙弗拉诺夫位移
    ("沙弗拉诺夫偏移", "shafranov-shift", "zh", "forbidden", "误译shift：正确为 沙弗拉诺夫位移"),
    ("夏弗拉诺夫位移", "shafranov-shift", "zh", "deprecated", "音译变体：应为 沙弗拉诺夫位移"),

    # trapped particle → 捕获粒子
    ("被困粒子", "trapped-particle", "zh", "forbidden", "误译trapped：正确为 捕获粒子"),
    ("陷阱粒子", "trapped-particle", "zh", "forbidden", "误译trapped：正确为 捕获粒子"),
    ("被捕粒子", "trapped-particle", "zh", "forbidden", "误译trapped：正确为 捕获粒子"),

    # Troyon limit → 特罗雍极限
    ("特罗伊极限", "troyon-limit", "zh", "forbidden", "音译错：正确为 特罗雍极限"),
    ("特洛扬极限", "troyon-limit", "zh", "forbidden", "音译错：正确为 特罗雍极限"),

    # Ware pinch → 韦尔箍缩
    ("韦尔收缩", "ware-pinch", "zh", "forbidden", "误译pinch：正确为 韦尔箍缩"),

    # ========================================================================
    # B. 加热·诊断·控制
    # ========================================================================
    ("# ==== Batch 2B: heating, diagnostics, control ====",),

    # beam emission spectroscopy → 束发射光谱
    ("光束发射光谱", "beam-emission-spectroscopy", "zh", "forbidden", "误译beam：正确为 束发射光谱"),
    ("束辐射光谱", "beam-emission-spectroscopy", "zh", "forbidden", "误译emission：正确为 束发射光谱"),

    # bolometer → 辐射计
    ("辐射热计", "bolometer", "zh", "forbidden", "混淆义：正确为 辐射计"),
    ("热量计", "bolometer", "zh", "forbidden", "误译：正确为 辐射计"),

    # charge exchange recombination spectroscopy → 电荷交换复合光谱
    ("电荷交换重组光谱", "charge-exchange-recombination-spectroscopy", "zh", "forbidden", "误译recombination：正确为 电荷交换复合光谱"),

    # current drive efficiency → 电流驱动效率
    ("电流驱动效能", "current-drive-efficiency", "zh", "forbidden", "误译efficiency：正确为 电流驱动效率"),

    # data-driven control → 数据驱动控制
    ("数据驱动调控", "data-driven-control", "zh", "forbidden", "误译control：正确为 数据驱动控制"),

    # density control → 密度控制
    ("密度调控", "density-control", "zh", "forbidden", "误译control：正确为 密度控制"),

    # disruption prediction → 破裂预测
    ("中断预测", "disruption-prediction", "zh", "forbidden", "误译disruption：正确为 破裂预测"),
    ("破坏预测", "disruption-prediction", "zh", "forbidden", "误译disruption：正确为 破裂预测"),

    # interferometry → 干涉仪
    ("干扰仪", "interferometry", "zh", "forbidden", "误译interference：正确为 干涉仪"),

    # motional Stark effect → 运动斯塔克效应
    ("动态斯塔克效应", "motional-stark-effect", "zh", "forbidden", "误译motional：正确为 运动斯塔克效应"),
    ("运动Stark效应", "motional-stark-effect", "zh", "deprecated", "非标准：应为 运动斯塔克效应"),

    # plasma control → 等离子体控制
    ("等离子控制", "plasma-control", "zh", "deprecated", "缺字'体'：应为 等离子体控制"),
    ("等离子体调控", "plasma-control", "zh", "forbidden", "误译control：正确为 等离子体控制"),

    # reflectometry → 反射仪
    ("反射计", "reflectometry", "zh", "deprecated", "非标准：聚变应为 反射仪"),
    ("反射测量仪", "reflectometry", "zh", "forbidden", "误译：正确为 反射仪"),

    # Thomson scattering → 汤姆逊散射
    ("汤姆森散射", "thomson-scattering", "zh", "deprecated", "音译变体：应为 汤姆逊散射"),
    ("托姆逊散射", "thomson-scattering", "zh", "forbidden", "音译错：正确为 汤姆逊散射"),

    # ========================================================================
    # C. 堆工程·结构·系统
    # ========================================================================
    ("# ==== Batch 2C: reactor engineering & structure ====",),

    # armor tile → 装甲瓦
    ("护甲瓦片", "armor-tile", "zh", "forbidden", "误译armor+tile：正确为 装甲瓦"),
    ("装甲砖", "armor-tile", "zh", "forbidden", "误译tile：正确为 装甲瓦"),
    ("装甲瓷砖", "armor-tile", "zh", "forbidden", "误译tile：正确为 装甲瓦"),

    # back plate → 背板
    ("后板", "back-plate", "zh", "forbidden", "误译back：正确为 背板"),

    # biological shield → 生物屏蔽
    ("生物防护罩", "biological-shield", "zh", "forbidden", "误译shield：正确为 生物屏蔽"),
    ("生物屏障", "biological-shield", "zh", "forbidden", "误译shield：正确为 生物屏蔽"),

    # blanket module → 包层模块
    ("毯模块", "blanket-module", "zh", "forbidden", "误译blanket：正确为 包层模块"),
    ("覆盖模块", "blanket-module", "zh", "forbidden", "误译blanket：正确为 包层模块"),

    # cable-in-conduit conductor → 管内电缆导体
    ("管道内导线", "cable-in-conduit-conductor", "zh", "forbidden", "误译conductor：正确为 管内电缆导体"),
    ("管道内电缆", "cable-in-conduit-conductor", "zh", "forbidden", "误译：正确为 管内电缆导体"),

    # cask system → 转运容器
    ("桶系统", "cask-system", "zh", "forbidden", "误译cask：正确为 转运容器"),
    ("酒桶系统", "cask-system", "zh", "forbidden", "误译cask：正确为 转运容器"),

    # closed divertor → 封闭偏滤器
    ("封闭分流器", "closed-divertor", "zh", "forbidden", "误译divertor：正确为 封闭偏滤器"),

    # coolant manifold → 冷却歧管
    ("冷却剂总管", "coolant-manifold", "zh", "forbidden", "误译manifold：正确为 冷却歧管"),
    ("冷却管汇", "coolant-manifold", "zh", "deprecated", "非标准：应为 冷却歧管"),

    # cooling channel → 冷却通道
    ("冷却管道", "cooling-channel", "zh", "deprecated", "非标准：应为 冷却通道"),
    ("冷却渠", "cooling-channel", "zh", "forbidden", "误译channel：正确为 冷却通道"),

    # demountable joint → 可拆卸接头
    ("拆卸关节", "demountable-joint", "zh", "forbidden", "误译joint：正确为 可拆卸接头"),
    ("可拆接头", "demountable-joint", "zh", "deprecated", "缺字：应为 可拆卸接头"),

    # heat sink → 热沉
    ("散热器", "heat-sink", "zh", "forbidden", "误译heat sink：IT义，聚变应为 热沉"),
    ("散热片", "heat-sink", "zh", "forbidden", "误译heat sink：IT义，聚变应为 热沉"),

    # beryllium multiplier → 铍中子倍增层
    ("铍增殖器", "beryllium-multiplier", "zh", "forbidden", "误译multiplier：正确为 铍中子倍增层"),
    ("铍乘法器", "beryllium-multiplier", "zh", "forbidden", "误译multiplier：正确为 铍中子倍增层"),
    ("铍倍增器", "beryllium-multiplier", "zh", "deprecated", "非标准：应为 铍中子倍增层"),

    # breeding zone → 增殖区
    ("繁殖区", "breeding-zone", "zh", "forbidden", "误译breeding：正确为 增殖区"),
    ("培育区", "breeding-zone", "zh", "forbidden", "误译breeding：正确为 增殖区"),

    # braze joint → 钎焊接头
    ("焊接接头", "braze-joint", "zh", "deprecated", "笼统化：应为 钎焊接头"),

    # Brayton cycle → 布雷顿循环
    ("布莱顿循环", "brayton-cycle", "zh", "forbidden", "音译错：正确为 布雷顿循环"),
    ("布拉顿循环", "brayton-cycle", "zh", "forbidden", "音译错：正确为 布雷顿循环"),

    # condenser → 凝汽器
    ("冷凝器", "condenser", "zh", "deprecated", "非标准：电力行业应为 凝汽器"),

    # confinement barrier → 包容屏障
    ("约束屏障", "confinement-barrier", "zh", "forbidden", "误译confinement：安全语境应为 包容屏障"),
    ("限制屏障", "confinement-barrier", "zh", "forbidden", "误译confinement：安全语境应为 包容屏障"),

    # confinement function → 包容功能
    ("约束功能", "confinement-function", "zh", "forbidden", "误译confinement：安全语境应为 包容功能"),
    ("限制功能", "confinement-function", "zh", "forbidden", "误译confinement：安全语境应为 包容功能"),

    # ========================================================================
    # D. 材料·辐照·损伤
    # ========================================================================
    ("# ==== Batch 2D: materials, irradiation, damage ====",),

    # cascade damage → 级联损伤
    ("级联伤害", "cascade-damage", "zh", "forbidden", "误译damage：正确为 级联损伤"),
    ("连锁损伤", "cascade-damage", "zh", "forbidden", "误译cascade：正确为 级联损伤"),

    # chemical erosion → 化学腐蚀
    ("化学侵蚀", "chemical-erosion", "zh", "deprecated", "非标准变体：应为 化学腐蚀"),

    # cracking → 裂纹
    ("开裂", "cracking", "zh", "deprecated", "非标准：聚变应为 裂纹"),
    ("裂化", "cracking", "zh", "forbidden", "误译：石化义，聚变应为 裂纹"),

    # creep → 蠕变
    ("蠕动", "creep", "zh", "forbidden", "误译creep：材料学应为 蠕变"),
    ("匍匐", "creep", "zh", "forbidden", "误译creep：材料学应为 蠕变"),

    # deep penetration → 深穿透
    ("深层渗透", "deep-penetration", "zh", "forbidden", "误译penetration：正确为 深穿透"),
    ("深度穿透", "deep-penetration", "zh", "deprecated", "非标准：应为 深穿透"),

    # irradiation creep → 辐照蠕变
    ("辐射蠕变", "irradiation-creep", "zh", "forbidden", "误译irradiation：正确为 辐照蠕变"),
    ("照射蠕变", "irradiation-creep", "zh", "forbidden", "误译irradiation：正确为 辐照蠕变"),

    # irradiation embrittlement → 辐照脆化
    ("辐射脆化", "irradiation-embrittlement", "zh", "forbidden", "误译irradiation：正确为 辐照脆化"),

    # critical current → 临界电流
    ("关键电流", "critical-current", "zh", "forbidden", "误译critical：正确为 临界电流"),

    # critical temperature → 临界温度
    ("关键温度", "critical-temperature", "zh", "forbidden", "误译critical：正确为 临界温度"),

    # critical magnetic field → 临界磁场
    ("关键磁场", "critical-magnetic-field", "zh", "forbidden", "误译critical：正确为 临界磁场"),

    # HTS → 高温超导体
    ("高温超导", "high-temperature-superconductor", "zh", "deprecated", "缺字'体'：应为 高温超导体"),

    # REBCO → REBCO带材
    ("REBCO胶带", "rebco", "zh", "forbidden", "误译tape：正确为 REBCO带材"),
    ("REBCO磁带", "rebco", "zh", "forbidden", "误译tape：正确为 REBCO带材"),

    # component lifetime → 部件寿命
    ("组件生命周期", "component-lifetime", "zh", "forbidden", "误译lifetime：正确为 部件寿命"),
    ("部件生命周期", "component-lifetime", "zh", "forbidden", "误译lifetime：正确为 部件寿命"),

    # component qualification → 部件鉴定
    ("部件资格认证", "component-qualification", "zh", "forbidden", "误译qualification：正确为 部件鉴定"),
    ("组件鉴定", "component-qualification", "zh", "deprecated", "非标准：应为 部件鉴定"),

    # ========================================================================
    # E. 氚·燃料循环·安全
    # ========================================================================
    ("# ==== Batch 2E: tritium, fuel cycle, safety ====",),

    # boronization → 硼化
    ("硼处理", "boronization", "zh", "deprecated", "笼统化：应为 硼化"),
    ("硼化处理", "boronization", "zh", "deprecated", "啰嗦：应为 硼化"),

    # bakeout → 真空烘烤
    ("烘烤", "bakeout", "zh", "deprecated", "缺修饰：应为 真空烘烤"),

    # burn control → 燃烧控制
    ("焚烧控制", "burn-control", "zh", "forbidden", "误译burn：聚变应为 燃烧控制"),

    # capacity factor → 容量因子
    ("容量系数", "capacity-factor", "zh", "forbidden", "误译factor：正确为 容量因子"),

    # contact dose rate → 接触剂量率
    ("接触辐射率", "contact-dose-rate", "zh", "forbidden", "误译dose rate：正确为 接触剂量率"),
    ("接触剂量", "contact-dose-rate", "zh", "deprecated", "缺字'率'：应为 接触剂量率"),

    # cryogenic distillation → 低温蒸馏
    ("冷冻蒸馏", "cryogenic-distillation", "zh", "forbidden", "误译cryogenic：正确为 低温蒸馏"),

    # cryogenic pellet → 低温弹丸
    ("低温颗粒", "cryogenic-pellet", "zh", "forbidden", "误译pellet：正确为 低温弹丸"),
    ("冷冻弹丸", "cryogenic-pellet", "zh", "forbidden", "误译cryogenic：正确为 低温弹丸"),

    # cryopump → 低温泵
    ("冷冻泵", "cryopump", "zh", "forbidden", "误译cryo-：正确为 低温泵"),

    # glow discharge cleaning → 辉光放电清洗
    ("发光放电清洁", "glow-discharge-cleaning", "zh", "forbidden", "误译glow：正确为 辉光放电清洗"),
    ("辉光放电清洁", "glow-discharge-cleaning", "zh", "deprecated", "非标准：应为 辉光放电清洗"),

    # isotope separation system → 同位素分离系统
    ("同位素分选系统", "isotope-separation-system", "zh", "forbidden", "误译separation：正确为 同位素分离系统"),

    # permeation → 渗透
    ("渗入", "permeation", "zh", "deprecated", "非标准：应为 渗透"),
    ("透过", "permeation", "zh", "deprecated", "非标准：应为 渗透"),

    # tritium accountancy → 氚衡算
    ("氚会计", "tritium-accountancy", "zh", "forbidden", "误译accountancy：正确为 氚衡算"),
    ("氚核算", "tritium-accountancy", "zh", "forbidden", "误译accountancy：正确为 氚衡算"),

    # tritium permeation barrier → 氚渗透阻挡层
    ("氚渗透屏障", "tritium-permeation-barrier", "zh", "deprecated", "非标准：应为 氚渗透阻挡层"),
    ("氚阻挡层", "tritium-permeation-barrier", "zh", "deprecated", "过简：应为 氚渗透阻挡层"),

    # water detritiation system → 水除氚系统
    ("水去氚系统", "water-detritiation-system", "zh", "deprecated", "非标准：应为 水除氚系统"),
    ("含氚水处理系统", "water-detritiation-system", "zh", "deprecated", "非标准：应为 水除氚系统"),

    # ========================================================================
    # F. ICF / 惯约·激光·靶
    # ========================================================================
    ("# ==== Batch 2F: ICF / inertial confinement ====",),

    # ablation front → 烧蚀前沿
    ("消融前沿", "ablation-front", "zh", "forbidden", "误译ablation：正确为 烧蚀前沿"),

    # ablator → 烧蚀层
    ("消融层", "ablator", "zh", "forbidden", "误译ablation：正确为 烧蚀层"),
    ("消融器", "ablator", "zh", "forbidden", "误译ablator：正确为 烧蚀层"),

    # areal density → 面密度
    ("面积密度", "areal-density", "zh", "forbidden", "误译areal：正确为 面密度"),

    # capsule implosion → 靶丸内爆
    ("胶囊内爆", "capsule-implosion", "zh", "forbidden", "误译capsule：ICF应为 靶丸内爆"),
    ("囊壳内爆", "capsule-implosion", "zh", "deprecated", "非标准：应为 靶丸内爆"),

    # convergence ratio → 收敛比
    ("汇聚比", "convergence-ratio", "zh", "forbidden", "误译convergence：正确为 收敛比"),
    ("收敛率", "convergence-ratio", "zh", "forbidden", "混淆ratio与rate：正确为 收敛比"),

    # indirect drive → 间接驱动
    ("间接驱动器", "indirect-drive", "zh", "forbidden", "误译drive：正确为 间接驱动"),

    # direct drive → 直接驱动
    ("直接驱动器", "direct-drive", "zh", "forbidden", "误译drive：正确为 直接驱动"),

    # laser-plasma interaction → 激光等离子体相互作用
    ("激光等离子交互", "laser-plasma-interaction", "zh", "forbidden", "缺字+非标准：正确为 激光等离子体相互作用"),
    ("激光等离子体交互作用", "laser-plasma-interaction", "zh", "forbidden", "误译interaction：正确为 激光等离子体相互作用"),

    # Rayleigh-Taylor instability → 瑞利-泰勒不稳定性
    ("雷利-泰勒不稳定性", "rayleigh-taylor-instability", "zh", "forbidden", "音译错：正确为 瑞利-泰勒不稳定性"),
    ("瑞利泰勒不稳定性", "rayleigh-taylor-instability", "zh", "deprecated", "缺连字符：应为 瑞利-泰勒不稳定性"),

    # Richtmyer-Meshkov instability → 里奇特迈耶-梅什科夫不稳定性
    ("里希特迈尔-梅什科夫不稳定性", "richtmyer-meshkov-instability", "zh", "deprecated", "音译变体：应为 里奇特迈耶-梅什科夫不稳定性"),

    # shock ignition → 激波点火
    ("冲击点火", "shock-ignition", "zh", "forbidden", "误译shock：ICF应为 激波点火"),

    # fast ignition → 快点火
    ("快速点火", "fast-ignition", "zh", "deprecated", "非标准：应为 快点火"),

    # target fabrication → 靶制备/靶制造
    # (skip: 靶制造 is current preferred; 靶加工 is acceptable variant)

    # Z-pinch → Z箍缩
    ("Z收缩", "z-pinch", "zh", "forbidden", "误译pinch：正确为 Z箍缩"),
    ("Z夹缩", "z-pinch", "zh", "forbidden", "误译pinch：正确为 Z箍缩"),
    ("Z捏缩", "z-pinch", "zh", "deprecated", "非标准：应为 Z箍缩"),
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
