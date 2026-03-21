# Changelog

本项目的变更记录与版本策略。

## 版本策略（CalVer）

- 采用 **CalVer**（日历版本）：`vYYYY.MM.DD`。
- 若同一天需要多次发布：`vYYYY.MM.DD.N`（从 1 开始递增）。
- “发布（release）”的最小动作：
  1) 更新本文件的 *Unreleased* 区块（把条目移动到新版本号下）。
  2) 确保质量门禁全绿：`python -m compileall` + `pytest`。
  3) 打 Git tag：`vYYYY.MM.DD`（或 `vYYYY.MM.DD.N`）。

> 说明：导出产物中的 `schema_version`（例如 `*_build_stats.json`、registry 导出 manifest 等）用于 **数据格式/兼容性**；它与项目的 CalVer tag 不同维度，按需要独立演进。

## Unreleased

### Added


### Changed


### Fixed

## v2026.03.21.9

### Added

- **误译禁用别名 Batch 9（最终扫尾）**：新增 52 条 `forbidden`/`deprecated` 别名，覆盖 5 大类 50 概念：
  - A. 机构名（eurofusion, f4e, swip, asipp, iaea, general-atomics 等 12 家）
  - B. 中国/国际装置名（cfetr, ifmif, sg-iii, laser-megajoule, enn-compact-fusion 等）
  - C. 英文装置名保留纠偏（east, jet, diii-d, sparc, arc, step, wendelstein-7x, nif 等 23 台）
  - D. 材料名（tungsten, nb3sn, eurofer, clf-1, clam, f82h 等）
  - E. 剩余概念（thermal-power, marfe）

### Fixed

- 清理 allowlist_zh.txt 中 1 条泄漏的禁用文本。
- 移除 3 个与已有别名冲突的条目（EXL50, EXL50U, 铜铬锆）。

## v2026.03.21.8


### Fixed

## v2026.03.21.8

### Added

- **误译禁用别名 Batch 8**：新增 98 条 `forbidden`/`deprecated` 别名，覆盖 8 大类 85 概念：
  - A. 仿星器·磁镜·先进概念（stellarator-optimization, theta-pinch, mirror-machine, traveling-wave-direct-energy-converter 等）
  - B. 包层缩写（HCCB, WCCB, HCLL, HCPB, fusion-neutron 等）
  - C. 诊断·测量（soft-x-ray, spectroscopy, ece-imaging, waveguide 等）
  - D. 超导·材料（low-temperature-superconductor, carbon-fiber-composite, graphite, siliconization 等）
  - E. 物理量·模式·不稳定性（pfirsch-schlueter-current, rsae, bae, z-effective, continuum-radiation 等）
  - F. 运行·控制（real-time-control, iter-to-demo, laser-energy-balance 等）
  - G. 数值方法·AI（computational-fluid-dynamics, bayesian-inference, uncertainty-quantification 等）
  - H. 工程·经济（steam-turbine 类已在 B7；本批 thermal-efficiency, hvac, icrf-antenna, large-helical-device 等）

### Fixed

- 清理 allowlist_zh.txt 中 1 条泄漏的禁用文本。
- 移除与 `thermal-force` 冲突的 `热力→thermal-power` 重复别名。
- 移除与已有别名冲突的 `铅锂→lithium-lead` 重复条目。

## v2026.03.21.7

### Added

- **误译禁用别名 Batch 7**：新增 137 条 `forbidden`/`deprecated` 别名，覆盖 8 大类 100 概念：
  - A. 等离子体·参数·控制（plasma-current, heat-load, advanced-tokamak, gas-puffing 等）
  - B. 惯性约束·先进聚变（fuel-capsule, target-fabrication, proton-boron-fusion, beam-target-fusion 等）
  - C. 包层·系统·冷却（tokamak-exhaust-processing-system, fuel-pellet, swirl-tube 等）
  - D. 安全·剂量·核数据（dose-limit, nuclear-data-library, photon-transport 等）
  - E. 壁·粉尘·材料·侵蚀（dust, elm-induced-erosion, runaway-electron-damage, recycling 等）
  - F. 碰撞区·新经典·输运（banana-regime, plateau-regime, bootstrap-generation, actuator 等）
  - G. 数值方法·AI·建模（finite-element-method, taylor-relaxation, radiation-dominated-regime 等）
  - H. 堆设计·经济（steam-turbine, gas-turbine, electrical-grid-connection 等）

### Fixed

- 移除与已有别名冲突的 `蒙特卡洛方法→monte-carlo-method` 重复条目。

## v2026.03.21.6

### Added

- **误译禁用别名 Batch 6**：新增 123 条 `forbidden`/`deprecated` 别名，覆盖 8 大类 ~100 概念：
  - A. 等离子体物理·运行模式（hybrid-scenario, steady-state-operation, ignition 等）
  - B. 波·加热·数理（ray-tracing, cross-section, coulomb-barrier, particle-in-cell 等）
  - C. 磁场·几何·对称性（magnetic-helicity, flux-expansion, quasi-axisymmetry 等）
  - D. 偏滤器·SOL·粒子（divertor-baffle, passing-particle, pedestal-width 等）
  - E. 中子·辐射防护·安全（activation-analysis, high-level-waste, ALARA 等）
  - F. 材料·包层·冷却（liquid-metal-coolant, TCAP, thermal-shock, FRC-merging 等）
  - G. 诊断·建模·控制（surrogate-model, digital-twin, slowing-down-time 等）
  - H. 堆设计·经济（prototype-reactor, synchrotron-radiation, spin-polarized-fuel 等）

### Fixed

- 清理 allowlist_zh.txt 中 2 条泄漏的禁用/废弃文本。
- 移除与 `energy-gain` 冲突的 `聚变增益→fusion-gain` 重复别名。

## v2026.03.21.5

### Added

- **误译禁用别名 Batch 5**：新增 157 条 `forbidden`/`deprecated` 别名，覆盖 8 大类 100 概念：
  - A. MHD·平衡·稳定性（理想/电阻/约化MHD、锯齿崩塌、负三角形变、双/单零位形 …）
  - B. 输运·湍流·动理学（漂移动理学、团块输运、湍流抑制/饱和、临界梯度 …）
  - C. 边界·偏滤器·等离子体壁（脱靶控制、破裂侵蚀、物理溅射、蒸汽屏蔽 …）
  - D. 超导·磁体·电工（绕组包、接头电阻、涡流、环向场纹波 …）
  - E. 中子学·辐射防护·蒙卡（中子通量/能谱/产额、权窗、方差缩减 …）
  - F. 材料·制造·部件（钨单块、等离子喷涂、铰接臂、吹扫气 …）
  - G. 堆系统·经济·许可（厂用电、平准化成本、首台堆、综合调试 …）
  - H. 聚变方案·特殊概念（α粒子能量导引、无中子聚变、球马克 …）
  - 累计：866 概念，3210 别名（含 823 条 forbidden/deprecated）。

### Fixed

- 移除 allowlist_zh 中 2 条误收录的禁用词。

## v2026.03.21.4

### Added

- **误译禁用别名 Batch 4**：新增 120 条 `forbidden`/`deprecated` 别名，覆盖 7 大类 ~100 概念：
  - A. MHD 不稳定性（内扭曲模、磁岛、磁阱、交换不稳定性、锁模、误差场、TEM、ETG、KBM …）
  - B. 输运·漂移·动理学（新经典输运、动量输运、自举电流、瓦尔箍缩、E×B漂移、抗磁漂移 …）
  - C. 诊断·光谱（电子回旋辐射、复合辐射、汤姆逊散射、运动斯塔克效应、反射仪 …）
  - D. 堆工程（一/二回路、热工水力、遥维护、真空室、低温恒温器、偏滤器卡匣 …）
  - E. 中子学·屏蔽·剂量（中子学、中子倍增剂、氚增殖比、比释动能、天空反照 …）
  - F. 材料·钨·粉尘（钨绒毛、钛酸锂、粉尘存量、产氚包层 …）
  - G. 聚变方案·先进概念（惯性约束聚变、热核聚变、聚变电站、仿星器、球形托卡马克 …）
  - 累计：866 概念，3053 别名（含 666 条 forbidden/deprecated）。

### Fixed

- 移除 allowlist_zh 中 8 条误收录的禁用/弃用词。

## v2026.03.21.3

### Added

- **误译禁用别名 Batch 3**：新增 132 条 `forbidden`/`deprecated` 别名，覆盖 7 大类 ~95 概念：
  - A. 运行模式/物理（约束标度律、内输运垒、剥离-气球模、电阻壁模、鱼骨模、反场箍缩 等 20 组）
  - B. 加热/波/电流驱动（ECCD、少数粒子加热、螺旋波电流驱动、天线耦合、螺旋度注入 等 15 组）
  - C. 诊断/控制（多普勒背散射/展宽、合成诊断、米尔诺夫/罗戈夫斯基线圈、抗磁环 等 10 组）
  - D. 堆工程/系统（冷屏、赤道窗口、偏滤器穹顶/靶板、纵场线圈、朗肯循环 等 15 组）
  - E. 材料/辐照（辐照硬化/偏析、再结晶、Frenkel缺陷对、失超检测/保护、应变敏感性 等 15 组）
  - F. 氚/安全/许可（氚自持/存量、设计基准事故、安全论证/分级、停堆剂量率 等 15 组）
  - G. ICF/先进概念（场反位形、串列磁镜、μ子催化聚变、示范堆、聚变试验电站 等 10 组）

### Fixed

- 允许列表清洗：从 `allowlist_zh.txt` 移除 4 条新增 forbidden/deprecated 泄漏

### Stats

- 概念 866 | 别名 2933（其中 forbidden 382 + deprecated 164 = 546）
- domain_terms 2510 | Rime 1690

## v2026.03.21.2

### Added

- **误译禁用别名 Batch 2**：新增 149 条 `forbidden`/`deprecated` 别名，覆盖 6 大类 ~80 概念：
  - A. 等离子体物理基础量（阿尔芬本征模、香蕉轨道、碰撞率、密度极限、交换不稳定性 等）
  - B. 加热·诊断·控制（束发射光谱、辐射计、汤姆逊散射、运动斯塔克效应、反射仪 等）
  - C. 堆工程·结构（装甲瓦、转运容器、冷却歧管、铍中子倍增层、布雷顿循环 等）
  - D. 材料·辐照·损伤（级联损伤、蠕变、辐照蠕变、辐照脆化、REBCO带材、临界电流 等）
  - E. 氚·燃料循环·安全（硼化、氚衡算、低温蒸馏、辉光放电清洗、水除氚系统 等）
  - F. ICF / 惯约（烧蚀前沿、靶丸内爆、收敛比、激波点火、Z箍缩 等）

### Fixed

- 允许列表清洗：从 `allowlist_zh.txt` 移除 4 条新增 forbidden/deprecated 泄漏

### Stats

- 概念 866 | 别名 2801（其中 forbidden 274 + deprecated 140 = 414）
- domain_terms 2514 | Rime 1694

## v2026.03.21.1

### Added

- **误译禁用别名（Forbidden aliases batch）**：新增 206 条 `forbidden`/`deprecated` 别名，
  覆盖 AI 常见中文误译（5 大类 100+ 概念）：
  - 概念名词直译（刮离层→刮削层、引导电流→自举电流、恒星器→仿星器、分流器→偏滤器 等 40 组）
  - 装置/系统误译（低温容器→低温恒温器、端口塞→窗口模块、工厂余额→电站辅助系统 等 15 组）
  - 物理量/参数误译（能量封闭时间→能量约束时间、氚繁殖率→氚增殖比、展弦比→纵横比 等 15 组）
  - 过程/方法误译（等离子体分离→等离子体脱靶、杂质运输→杂质输运、中断减缓→破裂缓解 等 15 组）
  - 材料/安全/工程误译（空洞膨胀→辐照肿胀、源术语→源项、解除委任→退役 等 15 组）
  - 高频补充（新古典→新经典、撕裂模式→撕裂模、气球模式→气球模、氚保留→氚滞留 等）

### Fixed

- **允许列表-禁用别名交叉清洗**：从 `allowlist_en.txt`（-19）和 `allowlist_zh.txt`（-25）中
  移除所有 `forbidden`/`deprecated` 条目，修复 `validate_registry` 长期未通过的桥接检查。

### Stats

- 概念 866 | 别名 2652（其中 forbidden 162 + deprecated 103 = 265）
- domain_terms 2518 | Rime 1698

## v2026.03.21

### Added

- **术语扩充（Batch 48–49）**：新增 20 个概念、51 条别名（含 3 条已有概念补充别名），覆盖等离子体-壁相互作用领域：
  - Batch 48: PWI核心过程（presheath, co-deposition, impurity source/influx, fuel recycling, wall pumping, deposition, graphite, surface roughening, cracking 等 10 项）
  - Batch 49: 壁面损伤、瞬态载荷与粉尘（thermal shock, disruption erosion, ELM-induced erosion, runaway electron damage, prompt redeposition, lithium coating, siliconization, dust generation/transport/inventory 等 10 项）
  - 补充别名：PWI / plasma-wall interaction / 等离子体壁相互作用 → plasma-surface-interaction
- 注册表总计：866 concepts, 2456 aliases, 866 evidence rows
- allowlist 同步：+22 中文、+7 英文 token-only 别名
- domain_terms.txt 从 2531 → 2560 条

## v2026.03.19.2

### Added

- **术语扩充（Batch 45–47）**：新增 26 个概念、64 条别名（+3 条合并到已有概念），覆盖 3 个主题领域：
  - Batch 45: 磁螺旋度、重联与弛豫物理（magnetic helicity, helicity injection, CHI, Taylor relaxation/state, magnetic reconnection, tilt instability 等 10 项）
  - Batch 46: 球马克/CT装置与形成技术（SSPX, coaxial plasma gun, spheromak merging, flux conserver, plasma sustainment, EXL-50U 等 8 项新概念；4 项已存在跳过）
  - Batch 47: 氢硼聚变与先进燃料物理（ignition temperature, three-alpha reaction, laser-boron fusion, HB11 Energy, LPP Fusion, power density 等 9 项新概念；plasma focus 合并到已有 dense-plasma-focus）
- 注册表总计：846 concepts, 2405 aliases, 846 evidence rows
- allowlist 同步：+24 中文、+5 英文 token-only 别名
- domain_terms.txt 从 2502 → 2531 条

## v2026.03.19.1

### Added

- **术语扩充（Batch 36–44）**：新增 90 个概念、198 条别名，覆盖 9 个主题领域：
  - Batch 36: ICF物理与内爆（convergence ratio, areal density, RM instability, ablation front, hot-spot ignition 等 10 项）
  - Batch 37: 等离子体辐射与光谱（line radiation, recombination radiation, Z_eff, Doppler/Stark broadening 等 10 项）
  - Batch 38: 等离子体湍流与非线性物理（turbulence saturation, avalanche transport, predator-prey oscillation 等 10 项）
  - Batch 39: 辐照损伤与材料科学（cascade damage, Frenkel pair, He bubble, W fuzz, radiation hardening 等 10 项）
  - Batch 40: PFC工程与热管理（armor tile, heat sink, hypervapotron, braze joint, TBC 等 10 项）
  - Batch 41: 先进偏滤器与液态金属（liquid metal divertor, vapor shielding, detachment control, Li wall 等 10 项）
  - Batch 42: 碰撞输运与新经典物理（banana/plateau/PS regime, collisionality, bootstrap generation 等 10 项）
  - Batch 43: 遥操作与维护工程（articulated boom, cask system, in-bore welding, remote inspection 等 10 项）
  - Batch 44: AI与数字技术（digital twin, surrogate model, ML disruption prediction, Bayesian inference, UQ 等 10 项）
- 注册表总计：820 concepts, 2331 aliases, 820 evidence rows
- allowlist 同步：+103 中文、+33 英文 token-only 别名
- domain_terms.txt 从 2369 → 2502 条

## v2026.03.19

### Fixed

- **同步注册表别名到 allowlist**：Batch 9–35 新增的 559 条中文 + 571 条英文 token-only 别名已补充到 allowlist_{zh,en}.txt
- domain_terms.txt 从 1241 → 2369 条
- Rime 输入法导入从 1018 → 1575 条（仅 CJK 条目）

## v2026.03.18.1

### Added

- **术语扩充（Batch 27–35）**：新增 90 个概念、211 条别名，覆盖 9 个主题领域：
  - Batch 27: RF加热与电流驱动物理（minority heating, mode conversion, multipactor, Faraday screen 等 10 项）
  - Batch 28: 粒子轨道物理（passing/trapped particle, E×B drift, grad-B drift, orbit loss 等 10 项）
  - Batch 29: 约束标度与性能指标（confinement scaling, H-factor, Troyon limit, density limit 等 10 项）
  - Batch 30: 等离子体控制与执行器（vertical stability, burn control, MPC, plasma ramp-up/down 等 10 项）
  - Batch 31: 包层工程细节（Be multiplier, breeding zone, purge gas, irradiation creep 等 10 项）
  - Batch 32: 真空与加料技术（vacuum pumping, bakeout, pellet ablation, CT injection 等 10 项）
  - Batch 33: 核分析细节（nuclear data library, neutron flux, contact dose rate, deep penetration 等 10 项）
  - Batch 34: 聚变经济与项目管理（FOAK/NOAK, learning rate, supply chain, regulatory approval 等 10 项）
  - Batch 35: 约束模态与输运现象（I-mode, super H-mode, density peaking, W accumulation, pedestal width 等 10 项）
- 注册表总计：730 concepts, 2133 aliases, 730 evidence rows

## v2026.03.18

### Added

- **术语扩充（Batch 18–26）**：新增 88 个概念、220 条别名，覆盖 9 个主题领域：
  - Batch 18: 磁平衡与等离子体几何（magnetic-axis, LCFS→separatrix, elongation, triangularity, aspect-ratio 等 12 项）
  - Batch 19: L-H 转换与边缘输运（L-H transition, power threshold, blob transport, SOL width 等 10 项）
  - Batch 20: 等离子体波（lower hybrid wave, EBW, IBW, Alfvén continuum, RSAE, BAE, EPM 等 10 项）
  - Batch 21: 聚变反应与核物理（D-T, D-D, D-³He reaction, triple product, Coulomb logarithm 等 9 项）
  - Batch 22: 先进托卡马克与运行场景（current hole, sawtooth crash, NTV, intrinsic rotation, critical gradient 等 10 项）
  - Batch 23: 超导磁体工程（AC loss, strain sensitivity, demountable joint, winding pack 等 10 项）
  - Batch 24: 等离子体-壁相互作用细节（chemical erosion, physical sputtering, dust, GDC, boronization 等 10 项）
  - Batch 25: 计算物理方法（Fokker-Planck, Vlasov, ray tracing, δf/full-f, extended MHD 等 10 项）
  - Batch 26: 安全、法规与标准（defense in depth, IAEA, source term, EPZ 等 8 项）
- LCFS/14 MeV neutron 概念合并到既有 separatrix/fusion-neutron，新增交叉别名
- 注册表总计：640 concepts, 1922 aliases, 640 evidence rows

## v2026.03.17

### Added

- **术语大幅扩充（Batch 9–17）**：新增 89 个概念、221 条别名，覆盖 9 个主题领域：
  - **Batch 9 — 等离子体物理基础**（14）：德拜鞘、德拜长度、拉莫尔半径、库仑碰撞、斯皮策电阻率、玻姆扩散、香蕉轨道、瓦尔箍缩、沙弗拉诺夫位移、等离子体频率、锁模、误差场、等离子体旋转、反常输运
  - **Batch 10 — 微观不稳定性 & 湍流输运**（7）：ITG 模、TEM、ETG 模、漂移波、剥离-气球模、微撕裂模、KBM
  - **Batch 11 — 加热与电流驱动硬件**（9）：回旋管、速调管、负离子源、波导、ICRF 天线、ECCD、电流驱动效率、功率沉积分布、螺旋波电流驱动
  - **Batch 12 — 偏滤器构型 & 先进偏滤器**（11）：偏滤器靶板、打击点、双零/单零位形、雪花偏滤器、Super-X 偏滤器、长腿偏滤器、挡板、私有磁通区、MARFE、磁通膨胀
  - **Batch 13 — 材料与辐照损伤**（10）：辐照脆化、辐照肿胀、氦脆、蠕变、疲劳寿命、活化产物、CuCrZr、钨单块、F82H、等离子喷涂钨
  - **Batch 14 — 氚循环 & 燃料处理**（9）：低温蒸馏、氚衡算、氚渗透阻挡层、燃烧份额、钯膜反应器、金属氢化物床、TCAP、燃料芯块、加料效率
  - **Batch 15 — 诊断系统**（10）：罗戈夫斯基线圈、米尔诺夫线圈、磁通环、抗磁环、BES、红外热成像、DBS、NAS、PCI、ECEI
  - **Batch 16 — 堆工程与中子学**（10）：中子学、热工水力、晕电流、涡流、窗口模块、赤道窗口、低温泵、包层模块、偏滤器卡匣、电磁力
  - **Batch 17 — 聚变组织与项目**（9）：EUROfusion、F4E、SWIP、ASIPP、CFS、TAE Technologies、Helion Energy、General Atomics、IPP Garching

### Changed

- Registry: 463 → 552 concepts, 1487 → 1702 aliases, 552 evidence rows。
- `anomalous transport` 别名从 `turbulent-transport` 移交至新概念 `anomalous-transport`。

## v2026.03.16.3

### Fixed

- 移除 2 条语义不等价的 substitution 规则（审计发现）：
  - `环型磁约束` → `托卡马克`：环型磁约束是上位概念（涵盖 tokamak / stellarator / RFP），不能自动替换为单一装置类型。
  - `divertor plate` → `divertor`：divertor plate（偏滤器靶板）是 divertor 系统的子部件，两者范围不等。

### Changed

- Substitution 规则：61 → 59 条。Registry: 463 concepts, 1487 aliases。

## v2026.03.16.2

### Fixed

- **substitution 规则质量修订**：响应 de-ai-fier 下游反馈，全面复核并修正 v2026.03.16.1 中语义不等价的替换规则。
  - 根因：deprecated 别名被映射到了不相关的 concept_id，导出管线解析 preferred form 时产生语义错误的替换建议。
  - 新增 8 个基础概念（deuterium, tritium, plasma, superconducting-magnet, radioactive-waste, fishbone-instability, poloidal-field, toroidal-field）作为 substitution 规则的正确锚点。
  - 修正 10 条语义不等价替换：
    - deutrium → ~~fusion reactivity~~ → deuterium
    - trittium / Trittium → ~~tritium retention~~ → tritium
    - 电浆 / 等离子 → ~~等离子体约束~~ → 等离子体
    - 超导磁铁 / 超导磁石 → ~~超导接头~~ → 超导磁体
    - 放射性废料 / 核废料 → ~~废物分级~~ → 放射性废物
    - 中性束注入 → ~~NBI~~ → 中性粒子束注入
    - 铍石 → ~~Be~~ → 铍
  - 移除 7 条过于宽泛或概念不等价的规则：
    - 扰动→破裂（泛词，非等同 disruption）
    - 中性束→NBI（zh→en 缩写，过宽）
    - 鱼骨模→高能粒子（概念完全不等）
    - superconducter/supraconductor→superconducting magnet（材料→装置）
    - 极向场/环向场→线圈名（字段→部件）
  - 修复 neutral-beam-injection 概念缺少 zh preferred 的问题（添加"中性粒子束注入"）。
  - 修复 beryllium 概念缺少 zh preferred 的问题（添加"铍"）。
  - 修复重复的 deprecated 条目（neutral-beam injection 出现两次）。
  - 最终规则集：61 条 substitution（全部为严格等价替换或拼写/格式修正）。

### Changed

- Registry: 463 concepts (+8 base), 1489 aliases, 463 evidence rows。

## v2026.03.16.1

### Added

- 术语纠错规则大幅扩充：新增 60+ deprecated/forbidden 别名，驱动 Vale substitution 规则（2 → 68 条）。
  - 英文常见拼写错误：tokomak, stellerator, bremstrahlung, disrution, Langmuire, trittium 等
  - 英文风格规范：H mode → H-mode, magneto-hydrodynamics → magnetohydrodynamics, scrapeoff → scrape-off 等
  - 中文非规范用词：等离子→等离子体, 电浆→等离子体, 超导磁铁→超导磁体, 中性束→中性粒子束注入, 边界局域模→边缘局域模 等
  - ITER 全称拼写错误检测（Research→Reactor, Internation→International）
- de-ai-fier 已同步更新：`fusion_terms_substitute.yml` 包含 68 条 swap 规则。

## v2026.03.16

### Added

- 术语库大规模扩充（32 → 455 concepts, 197 → 1408 aliases）：
  - 等离子体物理（磁约束基础、等离子体不稳定性、输运与湍流）
  - 等离子体—壁相互作用（溅射、再沉积、杂质输运、偏滤器物理）
  - 等离子体诊断（Thomson散射、ECE、干涉仪、Langmuir探针等）
  - 超导磁体（CICC、失超、HTS/LTS、磁体系统）
  - 仿星器 / 反场箍缩 / 场反位形 / 惯性约束聚变
  - p-B11 / 氢硼聚变（ENN 新奥装置、FRC 技术）
  - 聚变工程系统（真空/结构、氚系统、包层材料、冷却剂、中子学、主要装置 18 台）
  - 等离子体控制与运行（磁控/加热/粒子/位形控制）
  - 理论与模拟（MHD、漂移动理学、蒙特卡罗方法等）
  - 模拟工具与核数据（54 codes: ITER codes, CFD, MHD, PIC, 中子学, 活化, 停堆剂量率）
  - 数值方法（有限元/体/差分、自适应网格、并行计算等 15 条）
  - 聚变经济与路线图（FPP, COE, TRL, LCOE, Q, Qeng 等 20 条）
  - 聚变安全与废物（LOCA, LOFA, LLW/ILW/HLW, DBA 等 15 条）
  - 功率转化与电厂辅助系统（Rankine/Brayton/sCO2 循环, BOP, IHX 等 24 条）
- 术语库校验：455 concepts, 1408 aliases, 455 evidence rows，全部通过 validate_registry。
- 输入法导入：1018 entries 已导入 Rime (rime_ice)。

## v2026.03.02

### Changed

- 纯风格层清理：批量修复 `pipeline/` 与 `tests/` 中的行宽/格式噪音（仅重排与折行，不改变运行行为）。
- 文档更新：`README.md` 中 release 示例 tag 更新为 `v2026.03.02`。

### Fixed

- 解释器一致性：`pipeline.generate_dict_yaml`、`pipeline.rime_export`、`pipeline.rime_import_safe` 的子进程调用统一使用当前解释器（`sys.executable`），避免环境漂移。
- Rime 回滚健壮性：`pipeline.rime_import_safe` 在目标路径类型漂移（文件/目录互换）场景下可稳定恢复备份。
- `pipeline.review_pack` 返回类型收紧为 `TypedDict`，消除 `summary['counts'][...]` 的静态类型噪音。

## v2026.02.11.2

### Added

- 术语库扩充：补充氚燃料循环系统常用缩写及全称（TEP/TES/ISS/WDS/SDS/CPS），中英文 token-only。
- registry：为上述缩写补充 concept/alias 映射（缩写作为 alias，全称作为 preferred），便于下游做规范化建议。
- 术语库扩充：补充安全分析报告缩写及全称（PSAR/FSAR），中英文 token-only；并在 registry 中增加 acronyms→preferred 映射。
- 术语库扩充：补充辐射防护与屏蔽相关术语（ALARA、剂量约束/限值、屏蔽穿透、天空反照、串流、迷宫通道等），并在 registry 中增加规范化映射。
- 术语库扩充：补充辐射防护口径相关中文术语（职业照射、公众照射、有效剂量、当量剂量、导出空气浓度/DAC）并补齐 registry 映射。

## v2026.02.11.1

### Added

- 术语库扩充：补充 MCNP/FISPACT 及相关核数据/方差缩减/活化清单与停堆剂量率等中英文 token-only 术语。

## v2026.02.11

### Added

- v1.1 substitution 导出增强：在 registry 中补齐最小 deprecated 映射种子，使 `artifacts/terminology_substitutions.tsv` 与 `artifacts/vale/terminology_substitute.yml` 的 swap 非空；同时在 `fusion_terms_manifest.json` 的 counts 中增加 substitution 计数字段，便于下游验收。

## v2026.02.10

### Added

- 术语库扩充：补充仿星器相关术语（装置/磁几何/新古典）中英文词条。

## v2026.02.09.1

### Added

- 术语库扩充：补充 p-11B（氢硼 / HB11）聚变相关中英文术语种子。

## v2026.02.09

### Added

- 对外交付（de-ai-fier 接口 v1/v1.1）核心产物：
  - manifest 生成器：`pipeline/generate_manifest.py`（生成 `fusion_terms_manifest.json`，包含 sha256 + counts）。
  - 契约校验器：`pipeline/verify_release_contract.py`（校验 `domain_terms.txt` + manifest sha256 + counts 自洽）。
  - release 打包器：`pipeline/release_pack.py`（生成 `fusion-terms-artifacts-<tag>.tar.gz`，可用于离线门禁接入）。
- registry 强语义 substitution 导出（v1.1）：
  - `pipeline.export_registry --substitutions`：导出 `artifacts/terminology_substitutions.tsv`。
  - `pipeline.export_registry --vale-substitute`：导出 `artifacts/vale/terminology_substitute.yml`。
- 文档：`README.md` 增加 de-ai-fier 接入示例（方式 A 固定 tag 构建 / 方式 B 下载 Release 资产包）。

### Changed

- release 包构建可选纳入 registry 导出产物（query expansions/tag rules/substitutions/Vale YAML），并由 manifest 的 sha256 覆盖校验。

## v2026.02.07

### Added

- 术语库扩充：补齐聚变装置工程体系的关键中文术语，覆盖仪控/联锁/DAQ、辐射监测细分、氚形态与取样、真空子部件、热工水力测量、辐照效应与制造连接工艺等。
  - 默认配置下，`pipeline.build_terms` 生成的 `artifacts/domain_terms.txt` 词条规模提升到 **1066**。

### Changed

- Rime 导入/导出脚本增强：为调用 `rime_import_wordlist.py` 增加参数透传，支持指定 `dict_name`、覆盖 `rime_user_dir`、可选包含非 CJK 词条，以及在 userdb 锁定时禁用自动重启 fcitx。
- 停用词与噪声治理：补充一批在语料中稳定出现的噪声 token（如章节编号、OCR/LaTeX 伪词等），降低候选抽取污染。


## v2026.02.05

### Added

- 构建统计报表：`pipeline.build_terms` 默认写出 `*_build_stats.json`（新增/删除/总数、zh/en 拆分、synonyms 归一化计数）。
- Rime 集成加固：安全导入包装器（dry-run/备份/失败回滚）与 baked dict 生成器（`fusion_terms.dict.yaml`）。
- 审核工具化：review pack（候选增量 diff）与 decisions apply（将审阅决定确定性写入 allow/deny/synonyms）。
- registry 升级：validator + 多消费者导出（Vale accept/reject、query expansions、tag rules）与 IME 兼容回归保障。
- 抽词增强：支持按 glob 排除派生/噪声 Markdown 文件（`config.toml [sources].exclude_globs` + `--exclude-glob`）。

### Changed

- 构建门禁更严格：拒绝 whitespace 词条、不可见/控制字符、以及冲突 synonyms 映射。
- 抽词流水线：增量 cache + delta report；提供 filtered candidates 输出与 stopwords 种子支持。
- 编码策略收紧：对 `terms/`、registry、decisions 等人工维护输入采用 UTF-8 strict（坏编码直接报错）；对外部语料 Markdown 读取在遇到坏字节时用 U+FFFD 替换并发出告警，避免静默丢字节。
- 工作流更可移植：Rime importer 默认路径使用 `~/.local/bin/rime_import_wordlist.py`（不写死用户名/家目录）。

### Fixed

- 抽词文件遍历兼容：`iter_markdown_files()` 不再漏掉 `.MD`（大写扩展名）的 Markdown 文件。
