#!/usr/bin/env python3
"""Batch 7: forbidden/deprecated aliases for AI mistranslations (~100 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. 等离子体·参数·控制 (1-16)
    # ========================================================================
    ("# ==== Batch 7A: plasma parameters & control ====",),

    # plasma current → 等离子体电流
    ("等离子电流", "plasma-current", "zh", "forbidden", "缺字'体'：正确为 等离子体电流"),

    # plasma density → 等离子体密度
    ("等离子密度", "plasma-density", "zh", "forbidden", "缺字'体'：正确为 等离子体密度"),

    # plasma temperature → 等离子体温度
    ("等离子温度", "plasma-temperature", "zh", "forbidden", "缺字'体'：正确为 等离子体温度"),

    # plasma frequency → 等离子体频率
    ("等离子频率", "plasma-frequency", "zh", "forbidden", "缺字'体'：正确为 等离子体频率"),

    # plasma position control → 等离子体位置控制
    ("等离子位置控制", "plasma-position-control", "zh", "forbidden", "缺字'体'：正确为 等离子体位置控制"),

    # plasma state estimation → 等离子体状态估计
    ("等离子状态估计", "plasma-state-estimation", "zh", "forbidden", "缺字'体'：正确为 等离子体状态估计"),

    # plasma major radius → 等离子体大半径
    ("等离子体主半径", "plasma-major-radius", "zh", "forbidden", "误译major：正确为 等离子体大半径"),
    ("等离子体主要半径", "plasma-major-radius", "zh", "forbidden", "误译major：正确为 等离子体大半径"),

    # plasma minor radius → 等离子体小半径
    ("等离子体副半径", "plasma-minor-radius", "zh", "forbidden", "误译minor：正确为 等离子体小半径"),
    ("等离子体次半径", "plasma-minor-radius", "zh", "forbidden", "误译minor：正确为 等离子体小半径"),

    # X-point → X点
    ("交叉点", "x-point", "zh", "forbidden", "误译X-point：正确为 X点"),

    # heat load → 热负荷
    ("热负载", "heat-load", "zh", "forbidden", "误译load：正确为 热负荷"),
    ("热荷载", "heat-load", "zh", "forbidden", "误译load：正确为 热负荷"),

    # long pulse → 长脉冲
    ("长脉搏", "long-pulse", "zh", "forbidden", "误译pulse：正确为 长脉冲"),

    # advanced tokamak → 先进托卡马克
    ("高级托卡马克", "advanced-tokamak", "zh", "forbidden", "误译advanced：正确为 先进托卡马克"),

    # gas puffing → 充气
    ("气体吹入", "gas-puffing", "zh", "forbidden", "误译puffing：正确为 充气"),
    ("气体喷射", "gas-puffing", "zh", "forbidden", "误译puffing：正确为 充气"),

    # supersonic molecular beam injection → 超声分子束注入
    ("超音速分子束注入", "supersonic-molecular-beam-injection", "zh", "forbidden", "误译supersonic(超声≠超音速)：正确为 超声分子束注入"),

    # current profile control → 电流剖面控制
    ("电流轮廓控制", "current-profile-control", "zh", "forbidden", "误译profile：正确为 电流剖面控制"),
    ("电流配置文件控制", "current-profile-control", "zh", "forbidden", "误译profile(IT义)：正确为 电流剖面控制"),

    # steady-state high-beta → 稳态高β运行
    ("稳定状态高β", "steady-state-high-beta", "zh", "forbidden", "误译：正确为 稳态高β运行"),

    # ========================================================================
    # B. 惯性约束·先进聚变 (17-31)
    # ========================================================================
    ("# ==== Batch 7B: ICF & advanced fusion ====",),

    # fuel capsule → 靶丸
    ("燃料胶囊", "fuel-capsule", "zh", "forbidden", "误译capsule：正确为 靶丸"),
    ("燃料舱", "fuel-capsule", "zh", "forbidden", "误译capsule：正确为 靶丸"),

    # target fabrication → 靶制造
    ("目标制造", "target-fabrication", "zh", "forbidden", "误译target：正确为 靶制造"),
    ("目标加工", "target-fabrication", "zh", "forbidden", "误译target：正确为 靶制造"),

    # cryogenic target → 低温靶
    ("低温目标", "cryogenic-target", "zh", "forbidden", "误译target：正确为 低温靶"),

    # laser-driven fusion → 激光驱动聚变
    ("激光驱动融合", "laser-driven-fusion", "zh", "forbidden", "误译fusion：正确为 激光驱动聚变"),

    # proton-boron fusion → 质子-硼聚变
    ("质子-硼融合", "proton-boron-fusion", "zh", "forbidden", "误译fusion：正确为 质子-硼聚变"),
    ("质子硼融合", "proton-boron-fusion", "zh", "forbidden", "误译fusion：正确为 质子-硼聚变"),

    # laser-boron fusion → 激光硼聚变
    ("激光硼融合", "laser-boron-fusion", "zh", "forbidden", "误译fusion：正确为 激光硼聚变"),

    # advanced fuel → 先进燃料
    ("高级燃料", "advanced-fuel", "zh", "forbidden", "误译advanced：正确为 先进燃料"),

    # beam-target fusion → 束靶聚变
    ("光束目标聚变", "beam-target-fusion", "zh", "forbidden", "误译beam+target：正确为 束靶聚变"),
    ("束目标聚变", "beam-target-fusion", "zh", "forbidden", "误译target：正确为 束靶聚变"),

    # beam-beam fusion → 束束聚变
    ("光束光束聚变", "beam-beam-fusion", "zh", "forbidden", "误译beam：正确为 束束聚变"),

    # non-thermal plasma → 非热平衡等离子体
    ("非热等离子体", "non-thermal-plasma", "zh", "deprecated", "漏'平衡'：应为 非热平衡等离子体"),

    # dielectric wall accelerator → 介质壁加速器
    ("电介质墙加速器", "dielectric-wall-accelerator", "zh", "forbidden", "误译dielectric+wall：正确为 介质壁加速器"),

    # electrostatic confinement → 静电约束
    ("静电限制", "electrostatic-confinement", "zh", "forbidden", "误译confinement：正确为 静电约束"),
    ("静电封闭", "electrostatic-confinement", "zh", "forbidden", "误译confinement：正确为 静电约束"),

    # three-alpha reaction → 三α反应
    ("三阿尔法反应", "three-alpha-reaction", "zh", "forbidden", "误音译α：正确为 三α反应"),

    # side reaction → 副反应
    ("侧反应", "side-reaction", "zh", "forbidden", "误译side：正确为 副反应"),

    # fusion product spectrum → 聚变产物能谱
    ("聚变产品光谱", "fusion-product-spectrum", "zh", "forbidden", "误译product+spectrum：正确为 聚变产物能谱"),
    ("聚变产物光谱", "fusion-product-spectrum", "zh", "forbidden", "误译spectrum(能谱≠光谱)：正确为 聚变产物能谱"),

    # ========================================================================
    # C. 包层·系统·冷却·辅助 (32-47)
    # ========================================================================
    ("# ==== Batch 7C: blanket, systems, cooling ====",),

    # tokamak exhaust processing system → 托卡马克排气处理系统
    ("排放处理系统", "tokamak-exhaust-processing-system", "zh", "forbidden", "误译exhaust(排气≠排放)：正确为 托卡马克排气处理系统"),

    # breeder tritium extraction system → 增殖剂氚提取系统
    ("育种氚提取系统", "breeder-tritium-extraction-system", "zh", "forbidden", "误译breeder(增殖剂≠育种)：正确为 增殖剂氚提取系统"),
    ("繁殖器氚提取系统", "breeder-tritium-extraction-system", "zh", "forbidden", "误译breeder：正确为 增殖剂氚提取系统"),

    # storage and delivery system → 燃料储存与供应系统
    ("存储和交付系统", "storage-and-delivery-system", "zh", "forbidden", "误译delivery(供应≠交付)：正确为 燃料储存与供应系统"),

    # coolant purification system → 冷却剂净化系统
    ("冷却液净化系统", "coolant-purification-system", "zh", "forbidden", "误译coolant(冷却剂≠冷却液)：正确为 冷却剂净化系统"),

    # DCLL → 双冷锂铅包层
    ("双重冷却锂铅包层", "dcll", "zh", "forbidden", "冗译：正确为 双冷锂铅包层"),

    # helium-cooled → 氦冷
    ("氦冷却", "helium-cooled", "zh", "deprecated", "冗余：应为 氦冷"),

    # water-cooled → 水冷
    ("水冷却", "water-cooled", "zh", "deprecated", "冗余：应为 水冷"),

    # gas injection valve → 进气阀
    ("气体注入阀", "gas-injection-valve", "zh", "forbidden", "误译：正确为 进气阀"),

    # pellet guide tube → 弹丸导管
    ("颗粒导管", "pellet-guide-tube", "zh", "forbidden", "误译pellet(弹丸≠颗粒)：正确为 弹丸导管"),
    ("丸料导管", "pellet-guide-tube", "zh", "forbidden", "误译pellet：正确为 弹丸导管"),

    # palladium membrane reactor → 钯膜反应器
    ("钯薄膜反应器", "palladium-membrane-reactor", "zh", "deprecated", "非标准：应为 钯膜反应器"),

    # fuel pellet → 燃料芯块
    ("燃料颗粒", "fuel-pellet", "zh", "forbidden", "误译pellet(芯块≠颗粒)：正确为 燃料芯块"),
    ("燃料弹丸", "fuel-pellet", "zh", "forbidden", "误混聚变弹丸义：正确为 燃料芯块"),

    # coolant chemistry → 冷却剂化学
    ("冷却液化学", "coolant-chemistry", "zh", "forbidden", "误译coolant：正确为 冷却剂化学"),

    # waste heat recovery → 余热回收
    ("废热回收", "waste-heat-recovery", "zh", "forbidden", "误译waste(余热≠废热)：正确为 余热回收"),

    # magnetic flux loop → 磁通环
    ("磁通量环", "magnetic-flux-loop", "zh", "forbidden", "误译flux(磁通≠磁通量)：正确为 磁通环"),

    # swirl tube → 旋流管
    ("漩涡管", "swirl-tube", "zh", "forbidden", "误译swirl：正确为 旋流管"),
    ("涡流管", "swirl-tube", "zh", "forbidden", "误译swirl：正确为 旋流管"),

    # actively cooled component → 主动冷却部件
    ("积极冷却部件", "actively-cooled-component", "zh", "forbidden", "误译actively：正确为 主动冷却部件"),

    # ========================================================================
    # D. 安全·剂量·核数据 (48-58)
    # ========================================================================
    ("# ==== Batch 7D: safety, dose, nuclear data ====",),

    # dose limit → 剂量限值
    ("剂量极限", "dose-limit", "zh", "forbidden", "误译limit：正确为 剂量限值"),
    ("剂量上限", "dose-limit", "zh", "forbidden", "误译limit(限值≠上限)：正确为 剂量限值"),

    # occupational dose limit → 职业剂量限值
    ("职业剂量极限", "occupational-dose-limit", "zh", "forbidden", "误译limit：正确为 职业剂量限值"),

    # preliminary safety analysis report → 初步安全分析报告
    ("预备安全分析报告", "preliminary-safety-analysis-report", "zh", "forbidden", "误译preliminary：正确为 初步安全分析报告"),

    # final safety analysis report → 最终安全分析报告
    ("最后安全分析报告", "final-safety-analysis-report", "zh", "forbidden", "误译final：正确为 最终安全分析报告"),

    # dose rate mapping → 剂量率分布图
    ("剂量率映射", "dose-rate-mapping", "zh", "forbidden", "误译mapping(IT义)：正确为 剂量率分布图"),

    # dose rate survey → 剂量率巡测
    ("剂量率调查", "dose-rate-survey", "zh", "forbidden", "误译survey：正确为 剂量率巡测"),

    # nuclear data library → 核数据库
    ("核数据图书馆", "nuclear-data-library", "zh", "forbidden", "误译library：正确为 核数据库"),

    # helium production → 氦产生
    ("氦生产", "helium-production", "zh", "forbidden", "误混制造义：正确为 氦产生"),

    # neutron activation system → 中子活化系统
    ("中子激活系统", "neutron-activation-system", "zh", "forbidden", "误译activation(活化≠激活)：正确为 中子活化系统"),

    # photon transport → 光子输运
    ("光子传输", "photon-transport", "zh", "forbidden", "误译transport(输运≠传输)：正确为 光子输运"),
    ("光子运输", "photon-transport", "zh", "forbidden", "误译transport：正确为 光子输运"),

    # licensing → 许可证
    ("执照", "licensing", "zh", "forbidden", "误译licensing：正确为 许可证"),

    # ========================================================================
    # E. 壁·粉尘·材料·侵蚀 (59-72)
    # ========================================================================
    ("# ==== Batch 7E: wall, dust, erosion ====",),

    # dust → 粉尘
    ("灰尘", "dust", "zh", "forbidden", "误用生活义：正确为 粉尘"),

    # dust generation → 粉尘产生
    ("灰尘产生", "dust-generation", "zh", "forbidden", "误译dust：正确为 粉尘产生"),
    ("粉尘生成", "dust-generation", "zh", "deprecated", "非标准：应为 粉尘产生"),

    # dust transport → 粉尘输运
    ("灰尘传输", "dust-transport", "zh", "forbidden", "误译dust+transport：正确为 粉尘输运"),
    ("灰尘运输", "dust-transport", "zh", "forbidden", "误译dust+transport：正确为 粉尘输运"),
    ("粉尘传输", "dust-transport", "zh", "forbidden", "误译transport(输运≠传输)：正确为 粉尘输运"),

    # ELM-induced erosion → ELM诱发侵蚀
    ("ELM引起的腐蚀", "elm-induced-erosion", "zh", "forbidden", "侵蚀≠腐蚀：正确为 ELM诱发侵蚀"),
    ("ELM诱导侵蚀", "elm-induced-erosion", "zh", "deprecated", "非标准：应为 ELM诱发侵蚀"),

    # runaway electron damage → 逃逸电子损伤
    ("失控电子损伤", "runaway-electron-damage", "zh", "forbidden", "误译runaway：正确为 逃逸电子损伤"),
    ("跑飞电子损伤", "runaway-electron-damage", "zh", "forbidden", "误译runaway：正确为 逃逸电子损伤"),

    # arcing → 电弧
    ("弧光放电", "arcing", "zh", "deprecated", "非标准：应为 电弧"),

    # recycling → 再循环
    ("回收", "recycling", "zh", "forbidden", "误用废品义：等离子体壁义应为 再循环"),

    # deposition → 沉积
    ("沉淀", "deposition", "zh", "forbidden", "误混化学义：正确为 沉积"),

    # impurity source → 杂质源
    ("杂质来源", "impurity-source", "zh", "forbidden", "误译source(源≠来源)：正确为 杂质源"),

    # impurity influx → 杂质流入
    ("杂质涌入", "impurity-influx", "zh", "forbidden", "误译influx：正确为 杂质流入"),

    # vacancy → 空位
    ("空缺", "vacancy", "zh", "forbidden", "误用人事义：正确为 空位(晶格缺陷)"),

    # high heat flux testing → 高热流测试
    ("高热通量测试", "high-heat-flux-testing", "zh", "forbidden", "误译heat flux(热流≠热通量)：正确为 高热流测试"),

    # fusion cross section → 聚变截面
    ("聚变横截面", "fusion-cross-section", "zh", "forbidden", "误译(几何义)：核物理应为 聚变截面"),

    # radiation barrier → 辐射垒
    ("辐射壁垒", "radiation-barrier", "zh", "forbidden", "误译barrier：正确为 辐射垒"),
    ("辐射障碍", "radiation-barrier", "zh", "forbidden", "误译barrier：正确为 辐射垒"),

    # ========================================================================
    # F. 碰撞区·新经典·输运 (73-84)
    # ========================================================================
    ("# ==== Batch 7F: collisionality regimes & neoclassical ====",),

    # banana regime → 香蕉区
    ("香蕉区域", "banana-regime", "zh", "forbidden", "误译regime：正确为 香蕉区"),
    ("香蕉制度", "banana-regime", "zh", "forbidden", "误译regime(政治义)：正确为 香蕉区"),

    # plateau regime → 坪区
    ("平台区", "plateau-regime", "zh", "forbidden", "误译plateau：正确为 坪区"),
    ("高原区", "plateau-regime", "zh", "forbidden", "误译plateau(地理义)：正确为 坪区"),

    # neoclassical impurity transport → 新经典杂质输运
    ("新古典杂质输运", "neoclassical-impurity-transport", "zh", "forbidden", "误译neoclassical(新经典≠新古典)：正确为 新经典杂质输运"),
    ("新古典杂质传输", "neoclassical-impurity-transport", "zh", "forbidden", "误译neoclassical+transport：正确为 新经典杂质输运"),

    # bootstrap generation → 自举电流产生
    ("引导生成", "bootstrap-generation", "zh", "forbidden", "误用CS义：正确为 自举电流产生"),

    # poloidal asymmetry → 极向不对称性
    ("极面不对称", "poloidal-asymmetry", "zh", "forbidden", "误译poloidal(极向≠极面)：正确为 极向不对称性"),

    # bounce frequency → 弹跳频率
    ("反弹频率", "bounce-frequency", "zh", "forbidden", "误译bounce：正确为 弹跳频率"),

    # Greenwald fraction → Greenwald份额
    ("格林沃尔德分数", "greenwald-fraction", "zh", "forbidden", "误音译人名：正确保留 Greenwald份额"),

    # isotope effect → 同位素效应
    ("同位素效果", "isotope-effect", "zh", "forbidden", "误译effect(效应≠效果)：正确为 同位素效应"),

    # size scaling → 尺寸标度
    ("大小缩放", "size-scaling", "zh", "forbidden", "误译size+scaling：正确为 尺寸标度"),
    ("尺寸缩放", "size-scaling", "zh", "forbidden", "误译scaling(标度≠缩放)：正确为 尺寸标度"),

    # kinetic control → 动理学控制
    ("动力控制", "kinetic-control", "zh", "forbidden", "误译kinetic：正确为 动理学控制"),
    ("动力学控制", "kinetic-control", "zh", "forbidden", "误译kinetic(动理学≠动力学)：正确为 动理学控制"),

    # flux tube simulation → 磁通管模拟
    ("通量管模拟", "flux-tube-simulation", "zh", "forbidden", "误译flux(磁通≠通量)：正确为 磁通管模拟"),

    # actuator → 执行器
    ("致动器", "actuator", "zh", "forbidden", "误译actuator：正确为 执行器"),
    ("驱动器", "actuator", "zh", "forbidden", "误译actuator(驱动器≠执行器)：正确为 执行器"),

    # ========================================================================
    # G. 数值方法·AI·建模 (85-93)
    # ========================================================================
    ("# ==== Batch 7G: numerical methods, AI, modeling ====",),

    # Monte Carlo method → 蒙特卡罗方法
    # NOTE: '蒙特卡洛方法' skipped — already exists as alias

    # finite element method → 有限元方法
    ("有限元素方法", "finite-element-method", "zh", "forbidden", "误译element(元≠元素)：正确为 有限元方法"),

    # ML disruption prediction → 机器学习破裂预测
    ("ML中断预测", "ml-disruption-prediction", "zh", "forbidden", "误译disruption(破裂≠中断)：正确为 机器学习破裂预测"),
    ("机器学习中断预测", "ml-disruption-prediction", "zh", "forbidden", "误译disruption：正确为 机器学习破裂预测"),

    # neural network transport → 神经网络输运模型
    ("神经网络传输模型", "neural-network-transport", "zh", "forbidden", "误译transport(输运≠传输)：正确为 神经网络输运模型"),

    # Taylor relaxation → Taylor弛豫
    ("泰勒放松", "taylor-relaxation", "zh", "forbidden", "误音译+误译relaxation：正确保留 Taylor弛豫"),
    ("泰勒弛豫", "taylor-relaxation", "zh", "forbidden", "误音译Taylor：正确保留 Taylor弛豫"),

    # Taylor state → Taylor态
    ("泰勒状态", "taylor-state", "zh", "forbidden", "误音译Taylor：正确保留 Taylor态"),
    ("泰勒态", "taylor-state", "zh", "forbidden", "误音译Taylor：正确保留 Taylor态"),

    # thermo-mechanical analysis → 热机械分析
    ("热力学机械分析", "thermo-mechanical-analysis", "zh", "forbidden", "误译thermo(热≠热力学)：正确为 热机械分析"),

    # radiation-dominated regime → 辐射主导区间
    ("辐射主导制度", "radiation-dominated-regime", "zh", "forbidden", "误译regime(政治义)：正确为 辐射主导区间"),
    ("辐射主导方案", "radiation-dominated-regime", "zh", "forbidden", "误译regime：正确为 辐射主导区间"),

    # line radiation → 线辐射
    ("线性辐射", "line-radiation", "zh", "forbidden", "误译line(线≠线性)：正确为 线辐射"),

    # ========================================================================
    # H. 堆设计·经济·工程 (94-100)
    # ========================================================================
    ("# ==== Batch 7H: reactor design & economics ====",),

    # cost of electricity → 电力成本
    ("电费", "cost-of-electricity", "zh", "forbidden", "误译(过度简化)：正确为 电力成本"),

    # net electric power → 净电功率
    ("纯电力", "net-electric-power", "zh", "forbidden", "误译net+power：正确为 净电功率"),
    ("净电力", "net-electric-power", "zh", "forbidden", "误译power(功率≠电力)：正确为 净电功率"),

    # gross electric power → 总电功率
    ("毛电功率", "gross-electric-power", "zh", "forbidden", "误译gross：正确为 总电功率"),

    # steam turbine → 汽轮机
    ("蒸汽涡轮机", "steam-turbine", "zh", "forbidden", "误译turbine：正确为 汽轮机"),
    ("蒸汽涡轮", "steam-turbine", "zh", "forbidden", "误译steam+turbine：正确为 汽轮机"),

    # gas turbine → 燃气轮机
    ("气体涡轮机", "gas-turbine", "zh", "forbidden", "误译gas+turbine：正确为 燃气轮机"),
    ("气体涡轮", "gas-turbine", "zh", "forbidden", "误译gas+turbine：正确为 燃气轮机"),

    # electrical grid connection → 电网接入
    ("电气网格连接", "electrical-grid-connection", "zh", "forbidden", "误译grid+connection：正确为 电网接入"),
    ("电网连接", "electrical-grid-connection", "zh", "deprecated", "非标准：应为 电网接入"),

    # construction schedule → 建造进度
    ("建设时间表", "construction-schedule", "zh", "forbidden", "误译schedule：正确为 建造进度"),
    ("施工时间表", "construction-schedule", "zh", "forbidden", "误译construction+schedule：正确为 建造进度"),
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
