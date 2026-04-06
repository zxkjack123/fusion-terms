# Registry Gap Analysis & Batch 5 Recommendations

> Date: 2026-04-04
> Baseline: 1478 concepts (1315 active) · 5602 aliases · 73 batches completed

## Executive Summary

当前术语库在 **等离子体物理、材料、包层、氚系统、磁体、加热/电流驱动、诊断、中子学** 方面覆盖较为完善。以下 **8 个主题方向** 存在明显缺口，推荐补充约 **25 个高价值术语**。

## Gap Analysis by Theme

### ① 仪表与控制 (I&C) — 缺口严重

当前仅有等离子体控制层面的概念（`plasma-control`、`real-time-control`、`feedback-control` 等），完全缺乏 **工业级 I&C 基础设施** 术语。ITER/CFETR/DEMO 文档中这些术语出现频率极高。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 1 | central-interlock-system | 中央联锁系统 | Central Interlock System | CIS | system |
| 2 | machine-protection-system | 装置保护系统 | Machine Protection System | MPS | system |
| 3 | distributed-control-system | 分布式控制系统 | Distributed Control System | DCS | system |
| 4 | codac | 控制、数据获取与通信 | Control, Data Access and Communication | CODAC | system |

> 理由：CIS/MPS 是 ITER 安全相关系统的核心组成，DCS 是聚变装置标配；CODAC 是 ITER 控制架构的统称，在国内聚变工程文献中也被直接引用。

### ② 辐射防护与去污 (Radiation Protection) — 缺口明显

已有 `alara`、`dose-limit`、剂量相关指标，但 **辐射分区、去污、解控** 等运行/退役核心概念缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 5 | radiation-zoning | 辐射分区 | Radiation Zoning | — | method |
| 6 | controlled-area | 控制区 | Controlled Area | — | concept |
| 7 | decontamination | 去污 | Decontamination | — | method |
| 8 | clearance-level | 清洁解控水平 | Clearance Level | — | limit |

> 理由：辐射分区是设施设计基础（影响屏蔽厚度、通道布局）；去污是退役和维护的核心操作；清洁解控水平直接关系废物分类和回收策略。

### ③ 制造工艺与在役检查 (Manufacturing & ISI) — 缺口明显

已有 `weldability`、`plasma-spray-coating`、`non-destructive-testing`，但 **关键连接工艺和运行期检查** 缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 9 | hot-isostatic-pressing | 热等静压 | Hot Isostatic Pressing | HIP | method |
| 10 | electron-beam-welding | 电子束焊接 | Electron Beam Welding | EBW | method |
| 11 | diffusion-bonding | 扩散连接 | Diffusion Bonding | — | method |
| 12 | in-service-inspection | 在役检查 | In-Service Inspection | ISI | method |
| 13 | additive-manufacturing | 增材制造 | Additive Manufacturing | AM | method |

> 理由：HIP 是钨/RAFM 钢部件制造核心工艺（第一壁、偏滤器靶板）；EBW 是真空容器等厚壁不锈钢部件的主要焊接方法；扩散连接用于包层/第一壁异种材料连接；ISI 是核设施法规要求；AM 是聚变部件新兴制造路线，国内外均在积极研究。

### ④ 破裂物理补充 (Disruption Physics) — 小缺口

已有 `disruption`、`disruption-mitigation`、`runaway-electron`、`halo-current`、`vertical-displacement-event`，但 **破裂时序阶段** 缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 14 | thermal-quench | 热猝灭 | Thermal Quench | TQ | concept |
| 15 | current-quench | 电流猝灭 | Current Quench | CQ | concept |

> 理由：破裂过程分为热猝灭→电流猝灭两个阶段，在破裂缓解、力学载荷分析、第一壁损伤评估中是独立使用的高频术语。

### ⑤ 燃料循环回路 (Fuel Cycle) — 结构性缺口

已有各子系统（`tritium-plant`、`isotope-separation-system`、TEP 等），但缺乏 **回路层级划分** 和 **关键性能指标**。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 16 | inner-fuel-cycle | 内燃料循环 | Inner Fuel Cycle | IFC | concept |
| 17 | outer-fuel-cycle | 外燃料循环 | Outer Fuel Cycle | OFC | concept |
| 18 | burnup-fraction | 燃耗份额 | Burnup Fraction | — | metric |

> 理由：内/外燃料循环是 D-T 聚变电厂燃料系统设计的顶层架构划分（IFC = 等离子体 → 排气 → 直接内循环；OFC = 包层氚提取 → 纯化 → 储存 → 注入），文献中与 `tritium-self-sufficiency` 直接关联。`burnup-fraction` 是等离子体燃烧效率的核心指标。

### ⑥ 土建与抗震 (Civil/Seismic) — 缺口严重

仅有 `biological-shield`、`cryostat`、`vacuum-vessel`，完全缺乏 **建筑物、基础、隔震** 术语。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 19 | tokamak-building | 托卡马克厂房 | Tokamak Building | — | concept |
| 20 | seismic-isolation | 隔震 | Seismic Isolation | — | method |
| 21 | basemat | 底板 | Basemat | — | concept |
| 22 | drain-tank | 排放槽 | Drain Tank | — | system |

> 理由：ITER 的隔震系统是标志性工程设计特征（493 个隔震支座），CFETR 同样采用；tokamak-building 和 basemat 是设施描述、安全分析的基础用词；drain-tank 是 LOCA 后冷却剂收集的安全功能设备。

### ⑦ 冷却与辅助系统 (Cooling & Auxiliary) — 缺口明显

已有 `coolant-loop`、`heat-exchanger`，但 **ITER/DEMO 级别的独立冷却系统命名** 和 **水化学** 缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 23 | tokamak-cooling-water-system | 托卡马克冷却水系统 | Tokamak Cooling Water System | TCWS | system |
| 24 | atmosphere-detritiation-system | 厂房去氚系统 | Atmosphere Detritiation System | ADS | system |
| 25 | water-radiolysis | 水辐解 | Water Radiolysis | — | concept |

> 理由：TCWS 是 ITER PBS 26 的系统级名称，在工程文档中独立使用频率极高；ADS 是聚变设施三重氚包容的关键安全系统（ITER PBS 36）；水辐解直接影响冷却剂氢浓度和安全分析。

## Priority Ranking

| Priority | Theme | Terms | Impact |
|----------|-------|-------|--------|
| P0 | ④ 破裂物理补充 | 2 | 高频物理术语，补入成本极低 |
| P0 | ⑤ 燃料循环回路 | 3 | 填充顶层架构性缺口 |
| P1 | ① 仪表与控制 | 4 | ITER/DEMO 工程文档核心词汇 |
| P1 | ③ 制造与检查 | 5 | 工程制造/运行全生命周期 |
| P1 | ⑦ 冷却与辅助系统 | 3 | 安全分析高频系统名称 |
| P2 | ② 辐射防护 | 4 | 辐射安全/退役领域必备 |
| P2 | ⑥ 土建与抗震 | 4 | 设施级描述基础词汇 |

## Suggested Batching (if proceeding)

- **Batch 74** (P0, 5 terms): thermal-quench, current-quench, inner-fuel-cycle, outer-fuel-cycle, burnup-fraction
- **Batch 75** (P1-a, 7 terms): central-interlock-system, machine-protection-system, distributed-control-system, codac, hot-isostatic-pressing, electron-beam-welding, diffusion-bonding
- **Batch 76** (P1-b, 5 terms): in-service-inspection, additive-manufacturing, tokamak-cooling-water-system, atmosphere-detritiation-system, water-radiolysis
- **Batch 77** (P2, 8 terms): radiation-zoning, controlled-area, decontamination, clearance-level, tokamak-building, seismic-isolation, basemat, drain-tank

## Future Considerations (not in this batch)

以下方向在后续批次中可进一步补充：

- **设计规范/标准体系**: RCC-MR、ASME BPVC Section III、nuclear-quality-assurance（需确认是否属于术语库范围）
- **电气功率系统**: pulsed-power-supply、reactive-power-compensation、flywheel-energy-storage
- **更多 ITER PBS 系统名**: component-cooling-water-system (CCWS)、chilled-water-system (CHWS)、port-cell
- **腐蚀与水化学**: corrosion-product、hydrogen-water-chemistry、crud（更偏裂变领域）
