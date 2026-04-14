#!/usr/bin/env python3
"""Batch 4: forbidden/deprecated aliases for AI mistranslations (next ~100 concepts)."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

WRONG_ALIASES = [
    # ========================================================================
    # A. MHD 不稳定性 (1-20)
    # ========================================================================
    ("# ==== Batch 4A: MHD instabilities ====",),
    # internal kink mode → 内扭曲模
    (
        "内部扭曲模",
        "internal-kink-mode",
        "zh",
        "forbidden",
        "误译internal：正确为 内扭曲模",
    ),
    (
        "内部扭折模",
        "internal-kink-mode",
        "zh",
        "forbidden",
        "误译kink：正确为 内扭曲模",
    ),
    ("内扭曲模式", "internal-kink-mode", "zh", "deprecated", "非标准：应为 内扭曲模"),
    # kink mode → 扭曲模
    ("扭折模", "kink-mode", "zh", "forbidden", "误译kink：正确为 扭曲模"),
    ("扭结模", "kink-mode", "zh", "forbidden", "误译kink：正确为 扭曲模"),
    # magnetic island → 磁岛
    ("磁性岛", "magnetic-island", "zh", "forbidden", "误译magnetic：正确为 磁岛"),
    ("磁力岛", "magnetic-island", "zh", "forbidden", "误译magnetic：正确为 磁岛"),
    # magnetic well → 磁阱
    ("磁井", "magnetic-well", "zh", "forbidden", "误译well：正确为 磁阱"),
    ("磁势阱", "magnetic-well", "zh", "deprecated", "非标准用法：应为 磁阱"),
    # interchange instability → 交换不稳定性
    (
        "互换不稳定性",
        "interchange-instability",
        "zh",
        "forbidden",
        "误译interchange：正确为 交换不稳定性",
    ),
    # locked mode → 锁模
    ("锁定模", "locked-mode", "zh", "forbidden", "误译locked：正确为 锁模"),
    ("锁模式", "locked-mode", "zh", "deprecated", "非标准：应为 锁模"),
    # error field → 误差场
    ("错误场", "error-field", "zh", "forbidden", "误译error：正确为 误差场"),
    ("误差磁场", "error-field", "zh", "deprecated", "非标准：应为 误差场"),
    # tilt instability → 倾斜不稳定性
    (
        "倾覆不稳定性",
        "tilt-instability",
        "zh",
        "forbidden",
        "误译tilt：正确为 倾斜不稳定性",
    ),
    (
        "翻转不稳定性",
        "tilt-instability",
        "zh",
        "forbidden",
        "误译tilt：正确为 倾斜不稳定性",
    ),
    # micro-tearing mode → 微撕裂模
    ("微撕裂模式", "micro-tearing-mode", "zh", "deprecated", "非标准：应为 微撕裂模"),
    (
        "微断裂模",
        "micro-tearing-mode",
        "zh",
        "forbidden",
        "误译tearing：正确为 微撕裂模",
    ),
    # neoclassical tearing mode → 新经典撕裂模
    # (新古典撕裂模、新经典撕裂模式 already in registry)
    # KBM → 动理学气球模
    ("动力学气球模", "kbm", "zh", "forbidden", "误译kinetic：正确为 动理学气球模"),
    ("运动学气球模", "kbm", "zh", "forbidden", "误译kinetic：正确为 动理学气球模"),
    ("动理气球模式", "kbm", "zh", "deprecated", "非标准：应为 动理学气球模"),
    # ETG mode → 电子温度梯度模
    ("电子温度梯度模式", "etg-mode", "zh", "deprecated", "非标准：应为 电子温度梯度模"),
    (
        "电子热梯度模",
        "etg-mode",
        "zh",
        "forbidden",
        "误译temperature：正确为 电子温度梯度模",
    ),
    # TEM → 俘获电子模
    ("捕获电子模式", "tem", "zh", "deprecated", "非标准：应为 俘获电子模"),
    ("陷俘电子模", "tem", "zh", "forbidden", "误译trapped：正确为 俘获电子模"),
    ("捕获电子模", "tem", "zh", "deprecated", "用字非标准：应为 俘获电子模"),
    # magnetic reconnection → 磁重联
    ("磁力线重联", "magnetic-reconnection", "zh", "deprecated", "非标准：应为 磁重联"),
    # Alfvén wave → 阿尔芬波
    ("阿尔芬波动", "alfven-wave", "zh", "forbidden", "误加词：正确为 阿尔芬波"),
    # ========================================================================
    # B. 输运·漂移·动理学 (21-40)
    # ========================================================================
    ("# ==== Batch 4B: transport, drift, kinetics ====",),
    # neoclassical transport → 新经典输运
    (
        "新经典传输",
        "neoclassical-transport",
        "zh",
        "forbidden",
        "误译transport：正确为 新经典输运",
    ),
    # anomalous transport → 反常输运
    # (异常输运、异常传输 already in registry)
    # momentum transport → 动量输运
    (
        "动量传输",
        "momentum-transport",
        "zh",
        "forbidden",
        "误译transport：正确为 动量输运",
    ),
    (
        "动量转移",
        "momentum-transport",
        "zh",
        "forbidden",
        "误译transport：正确为 动量输运",
    ),
    # bootstrap current → 自举电流
    (
        "自引导电流",
        "bootstrap-current",
        "zh",
        "forbidden",
        "误译bootstrap：正确为 自举电流",
    ),
    (
        "自持电流",
        "bootstrap-current",
        "zh",
        "forbidden",
        "误译bootstrap：应为 自举电流",
    ),
    # Ware pinch → 瓦尔箍缩
    ("韦尔箍缩", "ware-pinch", "zh", "forbidden", "音译错：正确为 瓦尔箍缩"),
    ("维尔收缩", "ware-pinch", "zh", "forbidden", "双误(音译+pinch)：正确为 瓦尔箍缩"),
    ("瓦尔收缩", "ware-pinch", "zh", "forbidden", "误译pinch：正确为 瓦尔箍缩"),
    # banana orbit → 香蕉轨道
    ("香蕉形轨道", "banana-orbit", "zh", "deprecated", "非标准：应为 香蕉轨道"),
    # E×B drift → E×B漂移
    ("E×B偏移", "exb-drift", "zh", "forbidden", "误译drift：正确为 E×B漂移"),
    ("ExB漂移", "exb-drift", "zh", "deprecated", "格式非标准：应为 E×B漂移"),
    # diamagnetic drift → 抗磁漂移
    ("逆磁漂移", "diamagnetic-drift", "zh", "forbidden", "误译dia-：正确为 抗磁漂移"),
    ("反磁漂移", "diamagnetic-drift", "zh", "forbidden", "误译dia-：正确为 抗磁漂移"),
    ("抗磁偏移", "diamagnetic-drift", "zh", "forbidden", "误译drift：正确为 抗磁漂移"),
    # precession drift → 进动漂移
    (
        "岁差漂移",
        "precession-drift",
        "zh",
        "forbidden",
        "误译precession：正确为 进动漂移",
    ),
    ("旋进漂移", "precession-drift", "zh", "deprecated", "非标准：应为 进动漂移"),
    # NTV → 新经典环向粘滞
    (
        "新古典环向粘滞",
        "ntv",
        "zh",
        "forbidden",
        "误译neoclassical：正确为 新经典环向粘滞",
    ),
    ("新经典环形粘滞", "ntv", "zh", "forbidden", "误译toroidal：正确为 新经典环向粘滞"),
    ("新经典环向粘性", "ntv", "zh", "deprecated", "非标准：应为 新经典环向粘滞"),
    # gyrokinetics → 回旋动理学
    ("陀螺动理学", "gyrokinetics", "zh", "forbidden", "误译gyro：正确为 回旋动理学"),
    # two-fluid model → 双流体模型
    ("两流体模型", "two-fluid-model", "zh", "deprecated", "非标准：应为 双流体模型"),
    (
        "双液体模型",
        "two-fluid-model",
        "zh",
        "forbidden",
        "误译fluid：正确为 双流体模型",
    ),
    # ========================================================================
    # C. 诊断·光谱 (41-55)
    # ========================================================================
    ("# ==== Batch 4C: diagnostics & spectroscopy ====",),
    # electron cyclotron emission → 电子回旋辐射
    (
        "电子环行辐射",
        "electron-cyclotron-emission",
        "zh",
        "forbidden",
        "误译cyclotron：正确为 电子回旋辐射",
    ),
    (
        "电子回旋发射",
        "electron-cyclotron-emission",
        "zh",
        "forbidden",
        "误译emission：正确为 电子回旋辐射",
    ),
    # recombination radiation → 复合辐射
    (
        "再结合辐射",
        "recombination-radiation",
        "zh",
        "forbidden",
        "误译recombination：正确为 复合辐射",
    ),
    (
        "重组辐射",
        "recombination-radiation",
        "zh",
        "forbidden",
        "误译recombination：正确为 复合辐射",
    ),
    # Thomson scattering → 汤姆逊散射
    (
        "托马斯散射",
        "thomson-scattering",
        "zh",
        "forbidden",
        "音译错：正确为 汤姆逊散射",
    ),
    (
        "汤普逊散射",
        "thomson-scattering",
        "zh",
        "forbidden",
        "音译错(Thompson≠Thomson)：正确为 汤姆逊散射",
    ),
    # charge-exchange recombination spectroscopy → 电荷交换复合光谱
    (
        "电荷交换光谱",
        "charge-exchange-recombination-spectroscopy",
        "zh",
        "deprecated",
        "缺recombination：应为 电荷交换复合光谱",
    ),
    (
        "电荷转移复合光谱",
        "charge-exchange-recombination-spectroscopy",
        "zh",
        "forbidden",
        "误译exchange：正确为 电荷交换复合光谱",
    ),
    # motional Stark effect → 运动斯塔克效应
    (
        "运动斯塔克效果",
        "motional-stark-effect",
        "zh",
        "forbidden",
        "误译effect：正确为 运动斯塔克效应",
    ),
    # reflectometry → 反射仪
    ("反射测量法", "reflectometry", "zh", "forbidden", "误译：正确为 反射仪"),
    # far-infrared polarimetry → 远红外偏振仪
    (
        "远红外极化仪",
        "far-infrared-polarimetry",
        "zh",
        "forbidden",
        "误译polarimetry：正确为 远红外偏振仪",
    ),
    (
        "远红外偏振测量",
        "far-infrared-polarimetry",
        "zh",
        "deprecated",
        "非标准：应为 远红外偏振仪",
    ),
    # lower hybrid wave → 低杂波
    ("低混杂波", "lower-hybrid-wave", "zh", "forbidden", "误译hybrid：正确为 低杂波"),
    (
        "下混合波",
        "lower-hybrid-wave",
        "zh",
        "forbidden",
        "误译lower+hybrid：正确为 低杂波",
    ),
    # ========================================================================
    # D. 堆工程 (56-70)
    # ========================================================================
    ("# ==== Batch 4D: reactor engineering ====",),
    # primary loop → 一回路
    ("主回路", "primary-loop", "zh", "deprecated", "非标准：应为 一回路"),
    ("初级回路", "primary-loop", "zh", "forbidden", "误译primary：正确为 一回路"),
    ("一次回路", "primary-loop", "zh", "deprecated", "非标准：应为 一回路"),
    # secondary loop → 二回路
    ("次级回路", "secondary-loop", "zh", "forbidden", "误译secondary：正确为 二回路"),
    ("辅助回路", "secondary-loop", "zh", "forbidden", "误译secondary：正确为 二回路"),
    ("二次回路", "secondary-loop", "zh", "deprecated", "非标准：应为 二回路"),
    # thermal hydraulics → 热工水力
    (
        "热液压学",
        "thermal-hydraulics",
        "zh",
        "forbidden",
        "误译hydraulics：正确为 热工水力",
    ),
    ("热力学水力学", "thermal-hydraulics", "zh", "forbidden", "误译：正确为 热工水力"),
    ("热水力学", "thermal-hydraulics", "zh", "deprecated", "非标准：应为 热工水力"),
    # remote maintenance → 遥维护
    ("远程维护", "remote-maintenance", "zh", "deprecated", "非标准：应为 遥维护"),
    (
        "远程维修",
        "remote-maintenance",
        "zh",
        "forbidden",
        "误译maintenance：正确为 遥维护",
    ),
    # vacuum vessel → 真空室
    ("真空船", "vacuum-vessel", "zh", "forbidden", "误译vessel：正确为 真空室"),
    # thermal shield → 冷屏
    # (热屏蔽、热防护罩 already in registry)
    # cryostat → 低温恒温器
    ("低温恒温箱", "cryostat", "zh", "deprecated", "非标准：应为 低温恒温器"),
    ("冷冻恒温器", "cryostat", "zh", "forbidden", "误译cryo-：正确为 低温恒温器"),
    # divertor cassette → 偏滤器卡匣
    (
        "分流器暗匣",
        "divertor-cassette",
        "zh",
        "forbidden",
        "误译divertor+cassette：正确为 偏滤器卡匣",
    ),
    # equatorial port → 赤道窗口
    ("赤道口", "equatorial-port", "zh", "deprecated", "非标准：应为 赤道窗口"),
    # ========================================================================
    # E. 中子学·屏蔽·剂量 (71-85)
    # ========================================================================
    ("# ==== Batch 4E: neutronics, shielding, dosimetry ====",),
    # neutronics → 中子学
    ("中子物理学", "neutronics", "zh", "deprecated", "非标准：应为 中子学"),
    ("中子物理", "neutronics", "zh", "deprecated", "非标准：应为 中子学"),
    # neutron multiplier → 中子倍增剂
    (
        "中子倍增器",
        "neutron-multiplier",
        "zh",
        "forbidden",
        "误译multiplier：正确为 中子倍增剂",
    ),
    (
        "中子增殖器",
        "neutron-multiplier",
        "zh",
        "forbidden",
        "误译multiplier：正确为 中子倍增剂",
    ),
    # tritium breeding ratio → 氚增殖比
    (
        "氚繁殖比",
        "tritium-breeding-ratio",
        "zh",
        "forbidden",
        "误译breeding：正确为 氚增殖比",
    ),
    (
        "氚培育比",
        "tritium-breeding-ratio",
        "zh",
        "forbidden",
        "误译breeding：正确为 氚增殖比",
    ),
    # neutron wall loading → 中子壁负荷
    (
        "中子墙负荷",
        "neutron-wall-loading",
        "zh",
        "forbidden",
        "误译wall：正确为 中子壁负荷",
    ),
    # nuclear heating → 核热
    # (核加热 already in registry)
    # kerma → 比释动能
    ("动能释放率", "kerma", "zh", "forbidden", "误译kerma：正确为 比释动能"),
    ("内玛", "kerma", "zh", "forbidden", "误音译kerma：正确为 比释动能"),
    # skyshine → 天空反照
    ("天空闪烁", "skyshine", "zh", "forbidden", "误译skyshine：正确为 天空反照"),
    ("天际辐射", "skyshine", "zh", "forbidden", "误译skyshine：正确为 天空反照"),
    # shutdown dose rate → 停堆剂量率
    # (停机剂量率、关机剂量率 already in registry)
    # irradiation embrittlement → 辐照脆化
    (
        "照射脆化",
        "irradiation-embrittlement",
        "zh",
        "deprecated",
        "非标准：应为 辐照脆化",
    ),
    # void swelling → 辐照肿胀
    ("空洞肿胀", "void-swelling", "zh", "forbidden", "误译void：正确为 辐照肿胀"),
    # helium embrittlement → 氦脆
    ("氦致脆化", "helium-embrittlement", "zh", "deprecated", "非标准：应为 氦脆"),
    # irradiation creep → 辐照蠕变
    # (辐射蠕变、照射蠕变 already in registry)
    # ========================================================================
    # F. 材料·钨·粉尘 (86-95)
    # ========================================================================
    ("# ==== Batch 4F: materials, tungsten, dust ====",),
    # tungsten fuzz → 钨绒毛
    ("钨毛刺", "tungsten-fuzz", "zh", "forbidden", "误译fuzz：正确为 钨绒毛"),
    ("钨模糊层", "tungsten-fuzz", "zh", "forbidden", "误译fuzz：正确为 钨绒毛"),
    # lithium titanate → 钛酸锂
    ("钛锂酸盐", "lithium-titanate", "zh", "forbidden", "误译titanate：正确为 钛酸锂"),
    # dust inventory → 粉尘存量
    (
        "灰尘库存",
        "dust-inventory",
        "zh",
        "forbidden",
        "误译dust+inventory：正确为 粉尘存量",
    ),
    ("粉尘清单", "dust-inventory", "zh", "forbidden", "误译inventory：正确为 粉尘存量"),
    # tritium permeation barrier → 氚渗透阻挡层
    (
        "氚渗透阻碍层",
        "tritium-permeation-barrier",
        "zh",
        "forbidden",
        "用字错：正确为 氚渗透阻挡层",
    ),
    # tritium inventory → 氚存量
    ("氚盘存", "tritium-inventory", "zh", "forbidden", "误译inventory：正确为 氚存量"),
    # breeding blanket → 产氚包层
    ("繁殖层", "breeding-blanket", "zh", "forbidden", "误译breeding：正确为 产氚包层"),
    (
        "培育包层",
        "breeding-blanket",
        "zh",
        "forbidden",
        "误译breeding：正确为 产氚包层",
    ),
    ("增殖包层", "breeding-blanket", "zh", "deprecated", "非标准：应为 产氚包层"),
    # ========================================================================
    # G. 聚变方案·先进概念 (96-100+)
    # ========================================================================
    ("# ==== Batch 4G: fusion schemes & advanced concepts ====",),
    # inertial confinement fusion → 惯性约束聚变
    (
        "惯性限制聚变",
        "inertial-confinement-fusion",
        "zh",
        "forbidden",
        "误译confinement：正确为 惯性约束聚变",
    ),
    (
        "惯性封闭聚变",
        "inertial-confinement-fusion",
        "zh",
        "forbidden",
        "误译confinement：正确为 惯性约束聚变",
    ),
    # thermonuclear fusion → 热核聚变
    (
        "热核融合",
        "thermonuclear-fusion",
        "zh",
        "forbidden",
        "误用日语'融合'：正确为 热核聚变",
    ),
    ("热核反应", "thermonuclear-fusion", "zh", "deprecated", "非标准：应为 热核聚变"),
    # fusion power plant → 聚变电站
    ("聚变发电厂", "fusion-power-plant", "zh", "forbidden", "误译：正确为 聚变电站"),
    ("聚变发电站", "fusion-power-plant", "zh", "deprecated", "非标准：应为 聚变电站"),
    # stellarator → 仿星器
    ("星辰器", "stellarator", "zh", "forbidden", "误译stellarator：正确为 仿星器"),
    # spherical tokamak → 球形托卡马克
    (
        "球状托卡马克",
        "spherical-tokamak",
        "zh",
        "deprecated",
        "非标准：应为 球形托卡马克",
    ),
    (
        "球型托克马克",
        "spherical-tokamak",
        "zh",
        "forbidden",
        "双误(型≠形、音译)：正确为 球形托卡马克",
    ),
    # fusion reactivity → 聚变反应率
    (
        "聚变反应性",
        "fusion-reactivity",
        "zh",
        "forbidden",
        "误译reactivity：正确为 聚变反应率",
    ),
    (
        "聚变反应活性",
        "fusion-reactivity",
        "zh",
        "forbidden",
        "误译reactivity：正确为 聚变反应率",
    ),
    # technology readiness level → 技术就绪度
    (
        "技术成熟度",
        "technology-readiness-level",
        "zh",
        "deprecated",
        "非标准变体：应为 技术就绪度",
    ),
    (
        "技术准备水平",
        "technology-readiness-level",
        "zh",
        "forbidden",
        "误译：正确为 技术就绪度",
    ),
    (
        "技术就绪水平",
        "technology-readiness-level",
        "zh",
        "forbidden",
        "误译level：正确为 技术就绪度",
    ),
    # Alfvén eigenmode → 阿尔芬本征模
    (
        "阿尔芬特征模",
        "alfven-eigenmode",
        "zh",
        "forbidden",
        "误译eigen-：正确为 阿尔芬本征模",
    ),
    # toroidal Alfvén eigenmode → 环向阿尔芬本征模
    (
        "环形阿尔芬本征模",
        "toroidal-alfven-eigenmode",
        "zh",
        "deprecated",
        "非标准：应为 环向阿尔芬本征模",
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
