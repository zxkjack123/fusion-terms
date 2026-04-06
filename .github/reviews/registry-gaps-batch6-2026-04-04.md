# Registry Gap Analysis & Batch 6 Recommendations

> Date: 2026-04-04
> Baseline: 1340 concepts (post-Batch 77) · 5684 aliases · 1340 evidence rows

## Executive Summary

Batch 5（74–77）补充了 I&C、辐射防护、制造工艺、破裂物理、燃料循环、土建抗震、冷却辅助共 25 个术语后，仓库覆盖度显著提升。以下 **8 个主题方向** 仍存在系统性缺口，推荐补充约 **30 个高价值术语**。

缺口严重程度：电气功率系统 >> 安全分析方法论 ≈ 等离子体运行阶段 > ITER PBS 系统 ≈ 水化学/腐蚀 > 低温子系统 ≈ 磁体保护 > 中子束/端口细化

## Gap Analysis by Theme

### ① 电气功率系统 (Electrical Power Systems) — 缺口严重

当前仅有 `power-supply`、`power-conversion-system`，完全缺乏**脉冲功率拓扑、储能、功率器件**术语。托卡马克电气系统是设施级设计的核心子系统。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 1 | pulsed-power-supply | 脉冲电源 | Pulsed Power Supply | PPS | system |
| 2 | reactive-power-compensation | 无功补偿 | Reactive Power Compensation | — | method |
| 3 | motor-generator | 电机-发电机组 | Motor-Generator | MG | device |
| 4 | flywheel-energy-storage | 飞轮储能 | Flywheel Energy Storage | FES | system |
| 5 | ac-dc-converter | 交直流变换器 | AC/DC Converter | — | device |

> **理由**：PPS 是 ITER 最大的单体电源子系统（PBS 41），为磁体与加热系统提供脉冲功率。无功补偿和 MG/飞轮储能是大型脉冲装置对电网冲击管理的核心解决方案。AC/DC 变换器是所有磁体和加热电源链的基础功率环节。EAST、CFETR 设计文献中高频出现。

### ② 安全分析方法论 (Safety Analysis) — 缺口明显

已有 `design-basis-accident`、`defense-in-depth`、`confinement-barrier`、`safety-classification`，但缺乏**超设计基准事件、安全功能、安全重要性分级**等核安全核心概念。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 6 | beyond-design-basis-event | 超设计基准事件 | Beyond Design Basis Event | BDBE | concept |
| 7 | safety-function | 安全功能 | Safety Function | SF | concept |
| 8 | safety-important-component | 安全重要物项 | Safety Important Component | SIC | concept |
| 9 | postulated-initiating-event | 假设始发事件 | Postulated Initiating Event | PIE | concept |
| 10 | confinement-system | 包容系统 | Confinement System | — | system |

> **理由**：BDBE 是 ITER RPrS / SDR 的基本术语框架；SF 和 SIC 是核安全分级的基础概念（直接决定质量保证等级和检查要求）；PIE 是确定论安全分析的起点；confinement-system 是氚包容屏障的系统级总称。这些在 ITER/CFETR 安全分析报告中几乎每页都出现。

### ③ 等离子体运行阶段 (Plasma Operation Phases) — 缺口明显

已有 `plasma-ramp-up`、`plasma-ramp-down`、`plasma-current`，但缺乏**击穿、环电压、平顶段、燃烧阶段**等关键运行时序术语。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 11 | plasma-breakdown | 等离子体击穿 | Plasma Breakdown | — | concept |
| 12 | loop-voltage | 环电压 | Loop Voltage | — | metric |
| 13 | flat-top | 平顶段 | Flat-Top | — | concept |
| 14 | burn-phase | 燃烧阶段 | Burn Phase | — | concept |
| 15 | plasma-termination | 等离子体终止 | Plasma Termination | — | concept |

> **理由**：等离子体放电的完整时序（击穿→电流爬升→平顶→燃烧→下降→终止）是实验物理和控制系统设计的基础框架。loop-voltage 是放电启动的关键参数。这些术语在 EAST/HL-2M/CFETR 实验报告和控制系统设计中高频出现。

### ④ ITER PBS 系统命名补全 (ITER Systems) — 中等缺口

已有 `tokamak-cooling-water-system`、`drain-tank`、`atmosphere-detritiation-system`，但主要辅助系统仍有缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 16 | component-cooling-water-system | 部件冷却水系统 | Component Cooling Water System | CCWS | system |
| 17 | chilled-water-system | 冷冻水系统 | Chilled Water System | CHWS | system |
| 18 | port-cell | 端口室 | Port Cell | — | concept |
| 19 | upper-port | 上端口 | Upper Port | — | concept |
| 20 | diagnostic-port | 诊断端口 | Diagnostic Port | — | concept |

> **理由**：CCWS（PBS 27）和 CHWS（PBS 28）是 ITER 热排放系统的核心组成，在热工水力分析中与 TCWS 并列出现。Port-cell 是设备布置的关键概念（承载诊断、加热、远程维护通道）。Upper-port / diagnostic-port 是端口空间分配和诊断系统集成的基本用语。

### ⑤ 水化学与腐蚀 (Water Chemistry & Corrosion) — 中等缺口

Batch 5 新增了 `water-radiolysis`，但**水化学控制方案和腐蚀产物**管理仍是空白。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 21 | hydrogen-water-chemistry | 加氢水化学 | Hydrogen Water Chemistry | HWC | method |
| 22 | corrosion-product | 腐蚀产物 | Corrosion Product | — | concept |
| 23 | activated-corrosion-product | 活化腐蚀产物 | Activated Corrosion Product | ACP | concept |

> **理由**：HWC 是 ITER TCWS 的基线水化学控制方案（通过溶解氢抑制辐解氧生成）。腐蚀产物及其活化是冷却回路辐射剂量和维护策略的主要驱动因素。ACP 直接关系到职业照射控制和系统去污需求。

### ⑥ 低温子系统 (Cryogenic Subsystems) — 小缺口

已有 `cryoplant`、`cryostat`、`cryopump`、`thermal-shield`，但**低温分配和关键设备**缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 24 | cryoline | 低温传输线 | Cryoline | — | system |
| 25 | cold-box | 冷箱 | Cold Box | — | device |

> **理由**：Cryoline 是连接冷源与磁体馈线的低温流体传输系统（ITER 有数公里低温管线）。Cold-box 是低温制冷系统的核心单元（完成氦气的膨胀制冷）。在大型超导装置工程文档中频繁使用。

### ⑦ 磁体保护 (Magnet Protection) — 小缺口

已有 `quench-detection`、`quench-protection`、`current-lead`，但**能量卸放回路关键部件**缺失。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 26 | dump-resistor | 卸能电阻 | Dump Resistor | — | device |
| 27 | bypass-diode | 旁路二极管 | Bypass Diode | — | device |

> **理由**：磁体失超后通过 dump resistor 快速卸放磁储能（ITER TF 磁体储能约 41 GJ），是磁体保护系统的核心硬件。Bypass diode 保护磁体分段在失超时免受过压，是超导磁体串联电路的标准保护配置。

### ⑧ 标准、规范与质保 (Standards & QA) — 补充性

Batch 5 标注为"非目标"，但其中 **RCC-MR** 和核质保概念在聚变工程文档中引用极为普遍，建议纳入。

| # | concept_id | preferred_zh | preferred_en | abbr | category |
|---|-----------|-------------|-------------|------|----------|
| 28 | rcc-mr | 核设备设计建造规范 | Design and Construction Rules for Mechanical Components of Nuclear Installations | RCC-MR | doc |
| 29 | nuclear-quality-assurance | 核质量保证 | Nuclear Quality Assurance | NQA | method |
| 30 | irradiation-test | 辐照试验 | Irradiation Test | — | method |

> **理由**：RCC-MR 是 ITER/DEMO 包层、第一壁、偏滤器结构设计的基线规范。NQA 是核设施建造/运行许可的制度性基础。辐照试验是聚变材料验证的核心手段（IFMIF/DONES 的存在意义），当前仓库有 `irradiation-embrittlement`、`irradiation-creep` 等辐照效应但缺少试验本身。

## Priority Ranking

| Priority | Theme | Terms | Impact |
|----------|-------|-------|--------|
| P0 | ① 电气功率系统 | 5 | 补全最严重的系统级盲区 |
| P0 | ② 安全分析方法论 | 5 | 核安全文献核心框架术语 |
| P1 | ③ 等离子体运行阶段 | 5 | 实验运行基础时序 |
| P1 | ④ ITER PBS 系统 | 5 | 工程文档高频系统命名 |
| P1 | ⑤ 水化学与腐蚀 | 3 | TCWS 运行安全关键 |
| P2 | ⑥ 低温子系统 | 2 | 低温工程补充 |
| P2 | ⑦ 磁体保护 | 2 | 磁体保护硬件补充 |
| P2 | ⑧ 标准与质保 | 3 | 规范/制度性术语 |

## Suggested Batching

- **Batch 78** (P0, 10 terms): pulsed-power-supply, reactive-power-compensation, motor-generator, flywheel-energy-storage, ac-dc-converter, beyond-design-basis-event, safety-function, safety-important-component, postulated-initiating-event, confinement-system
- **Batch 79** (P1-a, 10 terms): plasma-breakdown, loop-voltage, flat-top, burn-phase, plasma-termination, component-cooling-water-system, chilled-water-system, port-cell, upper-port, diagnostic-port
- **Batch 80** (P1-b + P2, 10 terms): hydrogen-water-chemistry, corrosion-product, activated-corrosion-product, cryoline, cold-box, dump-resistor, bypass-diode, rcc-mr, nuclear-quality-assurance, irradiation-test

## Future Considerations (not in this batch)

以下方向可在更后续批次中继续补充：

- **更细粒度 NBI 部件**: heating-neutral-beam (HNB), diagnostic-neutral-beam (DNB), neutral-beam-cell, beam-source, ion-dump
- **更多端口/真空容器细节**: vacuum-vessel-sector, lower-port, port-limiter
- **等离子体约束模式**: i-mode, enhanced-confinement
- **先进燃料**: D-3He-fuel, p-11B-fuel (范围待确认)
- **退役技术细节**: remote-dismantling, activated-component-storage, waste-cementation
- **数字化/AI**: machine-learning-disruption-prediction, real-time-equilibrium-reconstruction (可能过于具体)
- **监管/许可**: nuclear-regulatory-body, operating-license, construction-permit
