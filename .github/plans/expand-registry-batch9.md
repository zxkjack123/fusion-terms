# 术语注册表扩展 — 批次 9：消防通风、机械部件、加热硬件子部件、真空计量

## 背景与目标

- **问题/需求描述**：注册表（1430 concepts / 6060 aliases / 1430 evidence）在 Batch 8 完成废物管理链、环境监测、电气配电、建设调试、辐射仪表、结构老化与腐蚀补充后，系统性缺口分析（2026-04-04）识别出 4 个高优先级空白子领域：①消防/HVAC/限制区通风系统（整个子领域仅 `hvac` 1条，消防子领域完全空白，已连续 3 轮计划标记 deferred）、②通用机械部件/管道/阀门（波纹管/法兰/密封垫/阀门等工程高频词汇零覆盖）、③NBI 束线和回旋管内部子部件（仅有系统级 `neutral-beam-injection` 和 `gyrotron`，子部件全缺）、④真空计量与吸气剂技术（泵类有 `cryopump`/`turbomolecular-pump`，但所有真空计类型和 NEG 吸气剂缺失）。
- **根因分析**：此前各批次侧重物理/材料/安全/结构等学科概念，对核设施通用工程基础设施（消防、管道、阀门）和加热系统硬件子部件覆盖不足。
- **目标**：新增 30 个概念（Batch 87–89），共约 150 条 aliases、30 条 evidence，配套更新 EN/ZH allowlist。
- **非目标（不做什么）**：
  - 不添加无损检测方法术语（UT/RT/ECT 等）— 留待 Batch 10
  - 不添加磁体工程细节（current-sharing-temperature 等）— 留待 Batch 10
  - 不添加国家核安全监管机构术语（ASN/NRC/NNSA 等）— 留待 Batch 10+
  - 不添加热力循环/功率转换术语（Brayton/Rankine cycle 等）— 留待 Batch 10+
  - 不修改 pipeline 源代码或 config.toml 参数
- **已有代码/流程复用分析**：
  - 三表追加流程：复用（与 Batch 84–86 完全一致的 TSV 追加 + 验证 + 导出链路）
  - allowlist 同步流程：复用（按 Batch 8 格式追加注释头 + 令牌行）
  - 验证/导出/构建/测试：复用（`validate_registry` → `export_registry --translation-dict` → `build_terms` → `pytest`）

## 技术方案

- **方案概述**：分 3 个 batch（87/88/89）各 10 条追加到 concepts.tsv / aliases.tsv / evidence.tsv，同步 allowlist，最终全量验证导出测试。
- **关键设计决策**：
  1. `containment-building` 不作为独立概念添加 — 已有 `containment`（安全壳）概念覆盖。改用 `ventilation-zone`（通风分区）替代，这是核设施 HVAC 设计的核心分类概念
  2. `confinement-ventilation` 使用缩写 CVS — 需确认不与现有缩写冲突（已验证无冲突）
  3. `hepa-filter` 使用缩写 HEPA — 已验证无冲突
  4. `non-evaporable-getter` 使用缩写 NEG — 已验证无冲突
  5. `magnetron-injection-gun` 使用缩写 MIG — 已验证无冲突
  6. `residual-ion-dump` 使用缩写 RID — 已验证无冲突
  7. NBI 子部件 category 使用 `device`（与已有 `negative-ion-source` device 类别一致），被动组件使用 `concept`
  8. `penning-gauge` preferred_en 使用大写 "Penning gauge"（人名源词保留大写），concept_id 仍用小写
  9. `relief-valve` preferred_zh 使用"安全阀"（GB/T 标准译名），alias 包含"泄压阀"
  10. `ecrh-launcher` preferred_en 使用 "ECRH launcher"（ITER 标准用法），alias 包含 "electron cyclotron launcher" 全称
  11. evidence source 统一使用 `internal:registry-gap-review:batch9`
  12. 所有 Batch 均需在 concepts 追加前运行 `grep -c` 预检确认 concept_id 不重复
- **影响范围**：
  - `terms/registry/concepts.tsv` — 追加 30 行（+3 批注释行）
  - `terms/registry/aliases.tsv` — 追加约 150 行（+3 批注释行）
  - `terms/registry/evidence.tsv` — 追加 30 行
  - `terms/allowlist_en.txt` — 追加约 60 条 EN tokens
  - `terms/allowlist_zh.txt` — 追加约 60 条 ZH tokens
  - `artifacts/translation_dict.json` — 重新生成（预期 en2zh ≥ 2774）
  - `artifacts/domain_terms.txt` — 重新生成（预期 ≥ 3326）

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|-------------|-----------|---------|---------|---------|------------|
| concepts.tsv 追加 | concept_id 与已有条目重复 | 数据冲突 | Y | 每个 Task 追加前 `grep -c ^<id>` 预检；`validate_registry` 后置检查 | validate 报 duplicate ERROR |
| aliases.tsv 追加 | surface_form 映射到错误 concept_id | 数据错误 | Y | 人工 review + validate_registry 检测 orphan | validate 报 orphan alias WARNING |
| aliases.tsv 追加 | 缩写与已有缩写冲突 | 数据冲突 | Y | 提前 grep 验证 CVS/HEPA/NEG/MIG/RID 唯一性 | export 生产歧义翻译 |
| evidence.tsv 追加 | 行数与 concepts 不匹配 | 数据完整性 | Y | validate_registry 行数一致性检查 | validate 报 count mismatch |
| allowlist 追加 | 遗漏 token 导致 build_terms 过滤掉新增术语 | 遗漏 | Y | Task 4.1 验证 domain_terms 行数 ≥ 预期下限 | 术语不出现在 IME 词库 |
| export --translation-dict | 新 zh alias 含非法字符 | 编码错误 | Y | export 输出 ERROR/WARNING 行检查 | 翻译字典条目缺失 |
| build_terms | config.toml 参数与新术语不兼容 | 配置问题 | N/A | build_terms 不依赖术语内容，仅依赖格式 | 不适用 |
| pytest | 现有测试因新数据量变化而断言失败 | 测试回归 | Y | 检查测试是否有硬编码计数断言，必要时更新 | pytest FAIL |
| git commit | pre-commit hook 检测到格式问题 | 格式错误 | Y | ruff + trim-whitespace + fix-EOF 在每次 commit 前自动执行 | commit 被拒 → 修正后重提交 |

## 时序推演

| 阶段 | 关键决策 | 潜在阻塞 | 缓解策略 |
|------|---------|----------|----------|
| 实施初期（Phase 1: Batch 87） | 消防/HVAC/建筑 10 概念追加；CVS/HEPA 缩写确认 | CVS 可能与某个未知代码缩写冲突 | 已预检无冲突；若发现冲突则去掉缩写，仅保留全称 |
| 实施中期（Phase 2: Batch 88） | 机械部件 10 概念；需确认"安全阀" vs "泄压阀"标准译名 | pressurizer 在 PWR 语境常见但聚变语境较少 | 仍添加（WCLL/DCLL blanket 回路有稳压器需求），notes 标注应用场景 |
| 实施后期（Phase 3–4: Batch 89 + 验证） | NBI/gyrotron 子部件分类决策；全量导出测试 | MIG 缩写在焊接领域有歧义（MIG welding） | notes 字段标注"gyrotron context"；alias 不添加 "MIG welding" |

## 执行计划

### Phase 1: Batch 87 — 消防 / HVAC / 限制区通风 / 核设施建筑

#### ✅ Task 1.1: Batch 87 三表追加

- **目标**：向 concepts / aliases / evidence 三表追加 10 个消防/HVAC/建筑概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在末尾追加批注释行 + 10 条概念
  - 文件 `terms/registry/aliases.tsv`：在末尾追加批注释行 + 约 50 条别名
  - 文件 `terms/registry/evidence.tsv`：在末尾追加 10 条证据行

**concepts.tsv 追加数据**（tab 分隔）：

```tsv
# ==== Batch 87: fire protection / HVAC / confinement ventilation / nuclear buildings ====
fire-detection-system	system	火灾探测系统	fire detection system		active	核设施探测火灾并触发报警的自动系统
fire-suppression-system	system	灭火系统	fire suppression system		active	核设施灭火装置 (气体/水喷淋/泡沫)
fire-damper	concept	防火阀	fire damper		active	安装在通风管道中阻止火焰和烟气蔓延的防火隔断装置
confinement-ventilation	system	限制区通风系统	confinement ventilation system	CVS	active	维持放射性区域负压并过滤排气的通风系统
emergency-exhaust-system	system	事故排风系统	emergency exhaust system		active	事故工况下从限制区快速排出含放射性气体的应急排风系统
hepa-filter	concept	高效空气过滤器	HEPA filter	HEPA	active	对 ≥0.3 μm 颗粒过滤效率 ≥99.97% 的高效空气过滤器
activated-carbon-filter	concept	活性炭过滤器	activated carbon filter		active	利用活性炭吸附去除气态放射性碘和有机碘的过滤装置
ventilation-zone	concept	通风分区	ventilation zone		active	按放射性污染风险等级对核设施区域进行通风气流方向管控的分区 (C1/C2/C3)
tritium-building	concept	氚厂房	tritium building		active	内设氚处理、贮存及回收设备的独立专用建筑
tokamak-pit	concept	托卡马克堆坑	tokamak pit		active	托卡马克装置地下基坑结构 (bioshield 内)
```

**aliases.tsv 追加数据**（tab 分隔）：

```tsv
# ---- Batch 87 aliases ----
fire detection system	fire-detection-system	en	preferred	preferred en
火灾探测系统	fire-detection-system	zh	preferred	preferred zh
fire-detection-system	fire-detection-system	en	alias	hyphenated form
fire alarm system	fire-detection-system	en	alias	synonym
火灾报警系统	fire-detection-system	zh	alias	alarm-focused zh
fire suppression system	fire-suppression-system	en	preferred	preferred en
灭火系统	fire-suppression-system	zh	preferred	preferred zh
fire-suppression-system	fire-suppression-system	en	alias	hyphenated form
fire extinguishing system	fire-suppression-system	en	alias	synonym
消防灭火系统	fire-suppression-system	zh	alias	expanded zh
fire damper	fire-damper	en	preferred	preferred en
防火阀	fire-damper	zh	preferred	preferred zh
fire-damper	fire-damper	en	alias	hyphenated form
防火风阀	fire-damper	zh	alias	variant zh
confinement ventilation system	confinement-ventilation	en	preferred	preferred en
限制区通风系统	confinement-ventilation	zh	preferred	preferred zh
CVS	confinement-ventilation	abbr	preferred	canonical abbr
confinement-ventilation	confinement-ventilation	en	alias	hyphenated form
confinement ventilation	confinement-ventilation	en	alias	short form
安全壳通风	confinement-ventilation	zh	alias	containment-focus zh
emergency exhaust system	emergency-exhaust-system	en	preferred	preferred en
事故排风系统	emergency-exhaust-system	zh	preferred	preferred zh
emergency-exhaust-system	emergency-exhaust-system	en	alias	hyphenated form
emergency ventilation	emergency-exhaust-system	en	alias	short form
应急排风系统	emergency-exhaust-system	zh	alias	variant zh
HEPA filter	hepa-filter	en	preferred	preferred en
高效空气过滤器	hepa-filter	zh	preferred	preferred zh
HEPA	hepa-filter	abbr	preferred	canonical abbr
hepa-filter	hepa-filter	en	alias	hyphenated form
high-efficiency particulate air filter	hepa-filter	en	alias	expanded form
高效过滤器	hepa-filter	zh	alias	short zh
activated carbon filter	activated-carbon-filter	en	preferred	preferred en
活性炭过滤器	activated-carbon-filter	zh	preferred	preferred zh
activated-carbon-filter	activated-carbon-filter	en	alias	hyphenated form
charcoal filter	activated-carbon-filter	en	alias	synonym
activated charcoal filter	activated-carbon-filter	en	alias	charcoal variant
活性碳过滤器	activated-carbon-filter	zh	alias	char-variant zh
ventilation zone	ventilation-zone	en	preferred	preferred en
通风分区	ventilation-zone	zh	preferred	preferred zh
ventilation-zone	ventilation-zone	en	alias	hyphenated form
通风区域	ventilation-zone	zh	alias	variant zh
tritium building	tritium-building	en	preferred	preferred en
氚厂房	tritium-building	zh	preferred	preferred zh
tritium-building	tritium-building	en	alias	hyphenated form
tritium plant building	tritium-building	en	alias	expanded form
氚处理厂房	tritium-building	zh	alias	processing-focus zh
tokamak pit	tokamak-pit	en	preferred	preferred en
托卡马克堆坑	tokamak-pit	zh	preferred	preferred zh
tokamak-pit	tokamak-pit	en	alias	hyphenated form
bioshield pit	tokamak-pit	en	alias	alternative name
堆坑	tokamak-pit	zh	alias	short zh
```

**evidence.tsv 追加数据**（tab 分隔）：

```tsv
fire-detection-system	internal:registry-gap-review:batch9	Automatic fire detection and alarm system for nuclear facilities (IAEA NS-G-1.7)	copilot	2026-04-04
fire-suppression-system	internal:registry-gap-review:batch9	Fire suppression installation for nuclear facility rooms (gas/water spray/foam)	copilot	2026-04-04
fire-damper	internal:registry-gap-review:batch9	Fire barrier device installed in ventilation ducts to prevent flame and smoke spread	copilot	2026-04-04
confinement-ventilation	internal:registry-gap-review:batch9	Ventilation system maintaining negative pressure in radioactive areas with filtered exhaust (ITER CVS)	copilot	2026-04-04
emergency-exhaust-system	internal:registry-gap-review:batch9	Emergency ventilation for rapid extraction of radioactive gases from confinement areas	copilot	2026-04-04
hepa-filter	internal:registry-gap-review:batch9	High-efficiency particulate air filter with >=99.97% efficiency for >=0.3um particles (DOE-STD-3020)	copilot	2026-04-04
activated-carbon-filter	internal:registry-gap-review:batch9	Activated carbon adsorption filter for gaseous radioactive iodine removal	copilot	2026-04-04
ventilation-zone	internal:registry-gap-review:batch9	Nuclear facility area zoning by contamination risk for ventilation airflow direction control (C1/C2/C3)	copilot	2026-04-04
tritium-building	internal:registry-gap-review:batch9	Dedicated building housing tritium processing, storage, and recovery equipment	copilot	2026-04-04
tokamak-pit	internal:registry-gap-review:batch9	Below-grade excavation structure for tokamak installation within the bioshield	copilot	2026-04-04
```

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中已有的 1619 行、`terms/registry/aliases.tsv` 中已有的 6858 行、`terms/registry/evidence.tsv` 中已有的 1520 行。仅 append。
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：registry OK，concepts = 1440，aliases ≈ 6910+，evidence = 1440，无 ERROR
  - 运行 `grep -c '^fire-detection-system\|^fire-suppression-system\|^fire-damper\|^confinement-ventilation\|^emergency-exhaust-system\|^hepa-filter\|^activated-carbon-filter\|^ventilation-zone\|^tritium-building\|^tokamak-pit' terms/registry/concepts.tsv` → 预期 = 10
- **验收标准**：
  - ✅ concepts.tsv 新增恰好 10 行数据行（不含注释行）
  - ✅ aliases.tsv 新增恰好 51 行数据行（不含注释行）
  - ✅ evidence.tsv 新增恰好 10 行数据行
  - ✅ validate_registry 无 ERROR
  - ✅ CVS/HEPA 缩写各仅映射到 1 个 concept_id
  - ✅ 每个 concept 至少有 en preferred + zh preferred + 1 个 alias
- **潜在风险**：`confinement-ventilation` concept_id 与已有 `confinement-function` 共享 "confinement" 前缀，但 concept_id 不同，不会冲突。`ventilation-zone` 与 `radiation-zoning`（已有）有语义关联但不重复。

#### ✅ Task 1.2: Batch 87 allowlist 同步

- **目标**：将 Batch 87 新增术语的所有 EN 表面形式和 ZH 表面形式同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加注释行 `# --- Batch 87 Phase 1 allowlist sync ---` + EN tokens
  - 文件 `terms/allowlist_zh.txt`：追加注释行 `# --- Batch 87 Phase 1 allowlist sync ---` + ZH tokens

**EN tokens**（每行一个）：

```
fire-detection-system
fire-suppression-system
fire-damper
confinement-ventilation
confinement-ventilation-system
CVS
emergency-exhaust-system
emergency-ventilation
hepa-filter
HEPA
high-efficiency-particulate-air-filter
activated-carbon-filter
charcoal-filter
ventilation-zone
tritium-building
tokamak-pit
bioshield-pit
```

**ZH tokens**（每行一个）：

```
火灾探测系统
火灾报警系统
灭火系统
消防灭火系统
防火阀
防火风阀
限制区通风系统
安全壳通风
事故排风系统
应急排风系统
高效空气过滤器
高效过滤器
活性炭过滤器
活性碳过滤器
通风分区
通风区域
氚厂房
氚处理厂房
托卡马克堆坑
堆坑
```

- **修改边界**：不得修改 allowlist 已有内容。仅追加。不得修改 `terms/denylist.txt`、`terms/stopwords_*.txt`。
- **测试要求**：
  - 运行 `sort terms/allowlist_en.txt | uniq -d` → 预期无重复行
  - 运行 `sort terms/allowlist_zh.txt | uniq -d` → 预期无重复行
- **验收标准**：
  - ✅ allowlist_en.txt 新增 17 个 EN tokens
  - ✅ allowlist_zh.txt 新增 20 个 ZH tokens
  - ✅ 无重复行
- **潜在风险**：`CVS` 在 EN allowlist 中可能被 build_terms 误匹配为版本控制系统缩写。但 allowlist 仅控制通过/拒绝，不影响语义。若下游出现歧义可在后续批次添加到 denylist。

### Phase 2: Batch 88 — 通用机械部件 / 管道 / 阀门

#### ✅ Task 2.1: Batch 88 三表追加

- **目标**：向 concepts / aliases / evidence 三表追加 10 个通用机械部件概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在末尾追加批注释行 + 10 条概念
  - 文件 `terms/registry/aliases.tsv`：在末尾追加批注释行 + 约 50 条别名
  - 文件 `terms/registry/evidence.tsv`：在末尾追加 10 条证据行

**concepts.tsv 追加数据**（tab 分隔）：

```tsv
# ==== Batch 88: generic mechanical components / piping / valves ====
bellows	concept	波纹管	bellows		active	用于管道系统热膨胀补偿和振动吸收的柔性金属元件
flange	concept	法兰	flange		active	用于管道/容器连接的盘状连接件
gasket	concept	密封垫片	gasket		active	法兰或接头间防止流体泄漏的密封元件
pressurizer	concept	稳压器	pressurizer		active	维持冷却回路系统压力的压力控制容器 (WCLL/DCLL blanket 回路)
isolation-valve	concept	隔离阀	isolation valve		active	切断或接通管路中介质流的截断阀
relief-valve	concept	安全阀	relief valve		active	超压时自动开启泄放流体以保护设备的压力安全装置
check-valve	concept	止回阀	check valve		active	仅允许单向流动、防止介质回流的阀门
expansion-joint	concept	膨胀节	expansion joint		active	吸收管道热膨胀位移的柔性补偿元件
rupture-disc	concept	爆破片	rupture disc		active	超压时主动破裂泄放压力的非重闭式安全装置
pipe-whip-restraint	concept	管道甩击约束装置	pipe whip restraint		active	限制高能管道断裂后甩击运动的结构约束件 (核级管道安全要求)
```

**aliases.tsv 追加数据**（tab 分隔）：

```tsv
# ---- Batch 88 aliases ----
bellows	bellows	en	preferred	preferred en
波纹管	bellows	zh	preferred	preferred zh
metal bellows	bellows	en	alias	material-specific
金属波纹管	bellows	zh	alias	material-specific zh
补偿器	bellows	zh	alias	function-name zh
flange	flange	en	preferred	preferred en
法兰	flange	zh	preferred	preferred zh
pipe flange	flange	en	alias	piping-context
法兰盘	flange	zh	alias	variant zh
gasket	gasket	en	preferred	preferred en
密封垫片	gasket	zh	preferred	preferred zh
sealing gasket	gasket	en	alias	expanded form
垫片	gasket	zh	alias	short zh
密封件	gasket	zh	alias	generic zh
pressurizer	pressurizer	en	preferred	preferred en
稳压器	pressurizer	zh	preferred	preferred zh
pressuriser	pressurizer	en	alias	British spelling
加压器	pressurizer	zh	alias	variant zh
isolation valve	isolation-valve	en	preferred	preferred en
隔离阀	isolation-valve	zh	preferred	preferred zh
isolation-valve	isolation-valve	en	alias	hyphenated form
shut-off valve	isolation-valve	en	alias	synonym
截止阀	isolation-valve	zh	alias	variant zh
relief valve	relief-valve	en	preferred	preferred en
安全阀	relief-valve	zh	preferred	preferred zh
relief-valve	relief-valve	en	alias	hyphenated form
safety relief valve	relief-valve	en	alias	expanded form
pressure relief valve	relief-valve	en	alias	full form
泄压阀	relief-valve	zh	alias	variant zh
check valve	check-valve	en	preferred	preferred en
止回阀	check-valve	zh	preferred	preferred zh
check-valve	check-valve	en	alias	hyphenated form
non-return valve	check-valve	en	alias	British synonym
逆止阀	check-valve	zh	alias	variant zh
expansion joint	expansion-joint	en	preferred	preferred en
膨胀节	expansion-joint	zh	preferred	preferred zh
expansion-joint	expansion-joint	en	alias	hyphenated form
伸缩节	expansion-joint	zh	alias	variant zh
伸缩接头	expansion-joint	zh	alias	connector-form zh
rupture disc	rupture-disc	en	preferred	preferred en
爆破片	rupture-disc	zh	preferred	preferred zh
rupture-disc	rupture-disc	en	alias	hyphenated form
rupture disk	rupture-disc	en	alias	US spelling
bursting disc	rupture-disc	en	alias	synonym
爆破膜	rupture-disc	zh	alias	variant zh
pipe whip restraint	pipe-whip-restraint	en	preferred	preferred en
管道甩击约束装置	pipe-whip-restraint	zh	preferred	preferred zh
pipe-whip-restraint	pipe-whip-restraint	en	alias	hyphenated form
pipe whip protection	pipe-whip-restraint	en	alias	protection variant
管鞭约束	pipe-whip-restraint	zh	alias	short zh
```

**evidence.tsv 追加数据**（tab 分隔）：

```tsv
bellows	internal:registry-gap-review:batch9	Flexible metallic element for thermal expansion compensation and vibration absorption in piping	copilot	2026-04-04
flange	internal:registry-gap-review:batch9	Disc-shaped connector for pipe and vessel joints	copilot	2026-04-04
gasket	internal:registry-gap-review:batch9	Sealing element between flanges or joints to prevent fluid leakage	copilot	2026-04-04
pressurizer	internal:registry-gap-review:batch9	Pressure control vessel maintaining coolant loop system pressure (WCLL/DCLL blanket circuits)	copilot	2026-04-04
isolation-valve	internal:registry-gap-review:batch9	Shut-off valve for isolating pipe sections or equipment	copilot	2026-04-04
relief-valve	internal:registry-gap-review:batch9	Pressure safety device that opens automatically to protect equipment from overpressure (ASME BPVC)	copilot	2026-04-04
check-valve	internal:registry-gap-review:batch9	One-way flow valve preventing backflow in piping systems	copilot	2026-04-04
expansion-joint	internal:registry-gap-review:batch9	Flexible compensating element absorbing thermal expansion displacement in piping	copilot	2026-04-04
rupture-disc	internal:registry-gap-review:batch9	Non-reclosing pressure relief device that bursts at set pressure differential	copilot	2026-04-04
pipe-whip-restraint	internal:registry-gap-review:batch9	Structural restraint limiting high-energy pipe whip motion after postulated break (nuclear-grade piping)	copilot	2026-04-04
```

- **修改边界**：不得修改三表中已有行。仅 append。
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：registry OK，concepts = 1450，evidence = 1450，无 ERROR
  - 运行 `grep -c '^bellows\|^flange\|^gasket\|^pressurizer\|^isolation-valve\|^relief-valve\|^check-valve\|^expansion-joint\|^rupture-disc\|^pipe-whip-restraint' terms/registry/concepts.tsv` → 预期 = 10
- **验收标准**：
  - ✅ concepts.tsv 新增恰好 10 行数据行
  - ✅ aliases.tsv 新增恰好 50 行数据行
  - ✅ evidence.tsv 新增恰好 10 行数据行
  - ✅ validate_registry 无 ERROR
  - ✅ 每个 concept 至少有 en preferred + zh preferred + 1 个 alias
- **潜在风险**：`bellows` preferred_en 本身即为复数形式（单复数同形），不会引起歧义。`relief-valve` 的 preferred_zh "安全阀" 与安全分析领域的"安全"无关，是阀门行业标准译名（GB/T 12241）。

#### ✅ Task 2.2: Batch 88 allowlist 同步

- **目标**：将 Batch 88 新增术语的所有 EN/ZH 表面形式同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加注释行 + EN tokens
  - 文件 `terms/allowlist_zh.txt`：追加注释行 + ZH tokens

**EN tokens**（每行一个）：

```
bellows
metal-bellows
flange
pipe-flange
gasket
sealing-gasket
pressurizer
pressuriser
isolation-valve
shut-off-valve
relief-valve
safety-relief-valve
pressure-relief-valve
check-valve
non-return-valve
expansion-joint
rupture-disc
rupture-disk
bursting-disc
pipe-whip-restraint
pipe-whip-protection
```

**ZH tokens**（每行一个）：

```
波纹管
金属波纹管
补偿器
法兰
法兰盘
密封垫片
垫片
密封件
稳压器
加压器
隔离阀
截断阀
压力安全阀
泄压阀
单向阀
逆止阀
膨胀节
伸缩节
伸缩接头
爆破盘
爆破膜
管道甩击约束装置
管鞭约束
```

- **修改边界**：不得修改 allowlist 已有内容。仅追加。
- **测试要求**：
  - `sort terms/allowlist_en.txt | uniq -d` / `sort terms/allowlist_zh.txt | uniq -d` 用于观察历史重复（仓库中存在既有重复）
  - 对 Batch 88 新增 token 执行逐项计数检查，预期每个新增 token 在各自 allowlist 中出现次数 = 1
- **验收标准**：
  - ✅ allowlist_en.txt 新增 21 个 EN tokens
  - ✅ allowlist_zh.txt 新增 23 个 ZH tokens
  - ✅ Batch 88 新增 tokens 无重复（允许历史重复行保留）
- **潜在风险**：`bellows` 单词较短且通用，可能在 extract_candidates 中匹配到非工程语境。但 allowlist 不做语义判断，仅防过滤。

### Phase 3: Batch 89 — NBI / 回旋管子部件 / 真空计量

#### ✅ Task 3.1: Batch 89 三表追加

- **目标**：向 concepts / aliases / evidence 三表追加 10 个加热硬件子部件和真空计量概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在末尾追加批注释行 + 10 条概念
  - 文件 `terms/registry/aliases.tsv`：在末尾追加批注释行 + 约 52 条别名
  - 文件 `terms/registry/evidence.tsv`：在末尾追加 10 条证据行

**concepts.tsv 追加数据**（tab 分隔）：

```tsv
# ==== Batch 89: NBI / gyrotron sub-components / vacuum gauging ====
neutralizer	device	中和器	neutralizer		active	NBI 束线中将高能离子束中和为中性粒子束的气体/等离子体靶
accelerator-grid	concept	加速栅极	accelerator grid		active	NBI 离子源中对负离子进行多级静电加速的栅极组件
beam-dump	device	束流收集器	beam dump		active	吸收未被中和的残余离子束能量的水冷收集器 (NBI)
residual-ion-dump	device	残余离子收集器	residual ion dump	RID	active	NBI 中和器下游磁偏转后收集残余离子的高热负荷部件
magnetron-injection-gun	device	磁控注入枪	magnetron injection gun	MIG	active	回旋管中产生环形电子束的磁控电子枪 (gyrotron context)
diamond-window	concept	金刚石窗口	diamond window		active	CVD 金刚石材料的 ECRH 微波传输真空窗口 (低损耗/高功率)
ecrh-launcher	device	ECRH发射天线	ECRH launcher		active	将微波束注入等离子体的可调方向发射天线/镜组 (ITER upper launcher / equatorial launcher)
non-evaporable-getter	concept	非蒸散型吸气剂	non-evaporable getter	NEG	active	通过加热活化反复使用的固体吸气材料 (Ti-Zr-V 合金)
ion-gauge	device	电离真空计	ion gauge		active	利用气体电离原理测量中高真空度的真空计
penning-gauge	device	潘宁真空计	Penning gauge		active	利用冷阴极放电原理测量真空度的离子真空计 (无灯丝)
```

**aliases.tsv 追加数据**（tab 分隔）：

```tsv
# ---- Batch 89 aliases ----
neutralizer	neutralizer	en	preferred	preferred en
中和器	neutralizer	zh	preferred	preferred zh
neutraliser	neutralizer	en	alias	British spelling
gas neutralizer	neutralizer	en	alias	gas-target type
中和室	neutralizer	zh	alias	chamber-form zh
accelerator grid	accelerator-grid	en	preferred	preferred en
加速栅极	accelerator-grid	zh	preferred	preferred zh
accelerator-grid	accelerator-grid	en	alias	hyphenated form
acceleration grid	accelerator-grid	en	alias	variant
加速栅	accelerator-grid	zh	alias	short zh
beam dump	beam-dump	en	preferred	preferred en
束流收集器	beam-dump	zh	preferred	preferred zh
beam-dump	beam-dump	en	alias	hyphenated form
beam stop	beam-dump	en	alias	synonym
束流阻尼器	beam-dump	zh	alias	variant zh
residual ion dump	residual-ion-dump	en	preferred	preferred en
残余离子收集器	residual-ion-dump	zh	preferred	preferred zh
RID	residual-ion-dump	abbr	preferred	canonical abbr
residual-ion-dump	residual-ion-dump	en	alias	hyphenated form
残余离子阻尼器	residual-ion-dump	zh	alias	variant zh
magnetron injection gun	magnetron-injection-gun	en	preferred	preferred en
磁控注入枪	magnetron-injection-gun	zh	preferred	preferred zh
MIG	magnetron-injection-gun	abbr	preferred	canonical abbr (gyrotron context)
magnetron-injection-gun	magnetron-injection-gun	en	alias	hyphenated form
磁注入枪	magnetron-injection-gun	zh	alias	short zh
diamond window	diamond-window	en	preferred	preferred en
金刚石窗口	diamond-window	zh	preferred	preferred zh
diamond-window	diamond-window	en	alias	hyphenated form
CVD diamond window	diamond-window	en	alias	material-process specific
金刚石窗	diamond-window	zh	alias	short zh
ECRH launcher	ecrh-launcher	en	preferred	preferred en
ECRH发射天线	ecrh-launcher	zh	preferred	preferred zh
ecrh-launcher	ecrh-launcher	en	alias	hyphenated form
ECH launcher	ecrh-launcher	en	alias	short form
electron cyclotron launcher	ecrh-launcher	en	alias	expanded form
ECRH天线	ecrh-launcher	zh	alias	short zh
non-evaporable getter	non-evaporable-getter	en	preferred	preferred en
非蒸散型吸气剂	non-evaporable-getter	zh	preferred	preferred zh
NEG	non-evaporable-getter	abbr	preferred	canonical abbr
non-evaporable-getter	non-evaporable-getter	en	alias	hyphenated form
NEG pump	non-evaporable-getter	en	alias	pump usage
非蒸发型吸气剂	non-evaporable-getter	zh	alias	variant zh
ion gauge	ion-gauge	en	preferred	preferred en
电离真空计	ion-gauge	zh	preferred	preferred zh
ion-gauge	ion-gauge	en	alias	hyphenated form
ionization gauge	ion-gauge	en	alias	expanded form
hot cathode gauge	ion-gauge	en	alias	type-specific
电离规	ion-gauge	zh	alias	short zh
Penning gauge	penning-gauge	en	preferred	preferred en
潘宁真空计	penning-gauge	zh	preferred	preferred zh
penning-gauge	penning-gauge	en	alias	hyphenated form
cold cathode gauge	penning-gauge	en	alias	type-specific
Penning vacuum gauge	penning-gauge	en	alias	expanded form
潘宁规	penning-gauge	zh	alias	short zh
```

**evidence.tsv 追加数据**（tab 分隔）：

```tsv
neutralizer	internal:registry-gap-review:batch9	Gas/plasma target neutralizing high-energy ion beam in NBI beamline	copilot	2026-04-04
accelerator-grid	internal:registry-gap-review:batch9	Multi-stage electrostatic accelerator grid assembly in NBI negative ion source	copilot	2026-04-04
beam-dump	internal:registry-gap-review:batch9	Water-cooled collector absorbing residual un-neutralized ion beam energy in NBI	copilot	2026-04-04
residual-ion-dump	internal:registry-gap-review:batch9	High heat flux component collecting magnetically deflected residual ions downstream of NBI neutralizer	copilot	2026-04-04
magnetron-injection-gun	internal:registry-gap-review:batch9	Magnetron-type electron gun producing annular electron beam in gyrotron (MIG)	copilot	2026-04-04
diamond-window	internal:registry-gap-review:batch9	CVD diamond vacuum window for low-loss high-power ECRH microwave transmission	copilot	2026-04-04
ecrh-launcher	internal:registry-gap-review:batch9	Steerable antenna/mirror assembly injecting microwave beam into plasma (ITER upper/equatorial launcher)	copilot	2026-04-04
non-evaporable-getter	internal:registry-gap-review:batch9	Solid getter material (Ti-Zr-V alloy) reactivatable by heating for repeated use in vacuum systems	copilot	2026-04-04
ion-gauge	internal:registry-gap-review:batch9	Vacuum gauge measuring medium-to-high vacuum by gas ionization principle	copilot	2026-04-04
penning-gauge	internal:registry-gap-review:batch9	Cold cathode discharge vacuum gauge without filament (Penning principle)	copilot	2026-04-04
```

- **修改边界**：不得修改三表中已有行（含 Phase 1/2 新增行）。仅 append。
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：registry OK，concepts = 1460，evidence = 1460，无 ERROR
  - 运行 `grep -c '^neutralizer\|^accelerator-grid\|^beam-dump\|^residual-ion-dump\|^magnetron-injection-gun\|^diamond-window\|^ecrh-launcher\|^non-evaporable-getter\|^ion-gauge\|^penning-gauge' terms/registry/concepts.tsv` → 预期 = 10
- **验收标准**：
  - ✅ concepts.tsv 新增恰好 10 行数据行
  - ✅ aliases.tsv 新增恰好 54 行数据行
  - ✅ evidence.tsv 新增恰好 10 行数据行
  - ✅ validate_registry 无 ERROR
  - ✅ RID/MIG/NEG 缩写各仅映射到 1 个 concept_id
  - ✅ MIG 不与焊接领域概念冲突（registry 中无 MIG-welding 条目）
  - ✅ 每个 concept 至少有 en preferred + zh preferred + 1 个 alias
- **潜在风险**：`MIG` 在焊接领域是 "Metal Inert Gas" 缩写，但本注册表不覆盖焊接工艺术语（`electron-beam-welding` 已有，但无 MIG welding）。若未来加入焊接术语需重新评估。`beam-dump` 在加速器物理中有更广泛含义，此处 notes 和 evidence 均标注 NBI 语境。

#### ✅ Task 3.2: Batch 89 allowlist 同步

- **目标**：将 Batch 89 新增术语的所有 EN/ZH 表面形式同步到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加注释行 + EN tokens
  - 文件 `terms/allowlist_zh.txt`：追加注释行 + ZH tokens

**EN tokens**（每行一个）：

```
neutralizer
neutraliser
gas-neutralizer
accelerator-grid
acceleration-grid
beam-dump
beam-stop
residual-ion-dump
RID
magnetron-injection-gun
MIG
diamond-window
CVD-diamond-window
ecrh-launcher
ECH-launcher
electron-cyclotron-launcher
non-evaporable-getter
NEG
NEG-pump
ion-gauge
ionization-gauge
hot-cathode-gauge
penning-gauge
cold-cathode-gauge
Penning-vacuum-gauge
```

**ZH tokens**（每行一个）：

```
中和器
中和室
加速栅极
加速栅
束流收集器
束流阻尼器
残余离子收集器
残余离子阻尼器
磁控注入枪
磁注入枪
金刚石窗口
金刚石窗
ECRH发射天线
ECRH天线
非蒸散型吸气剂
非蒸发型吸气剂
电离真空计
离子规
潘宁真空计
潘宁规
```

- **修改边界**：不得修改 allowlist 已有内容。仅追加。
- **测试要求**：
  - `sort terms/allowlist_en.txt | uniq -d` / `sort terms/allowlist_zh.txt | uniq -d` 用于观察历史重复（仓库中存在既有重复）
  - 对 Batch 89 新增 token 执行逐项计数检查，预期每个新增 token 在各自 allowlist 中出现次数 = 1
- **验收标准**：
  - ✅ allowlist_en.txt 新增 25 个 EN tokens
  - ✅ allowlist_zh.txt 新增 20 个 ZH tokens
  - ✅ Batch 89 新增 tokens 无重复（允许历史重复行保留）
- **潜在风险**：`MIG` 和 `NEG` 是 3 字符 tokens，`min_en_key_len=3`（config.toml 设置），刚好符合阈值，不会被过滤到 short-token 区。

### Phase 4: 全量验证、导出与测试

#### Task 4.1: 全量验证导出测试

- **目标**：对三批全部 30 条新增概念执行完整的验证、导出、构建和回归测试
- **修改内容**：
  - `terms/` 目录：无修改（仅读取验证）
  - `artifacts/translation_dict.json` — 由 `export_registry --translation-dict` 重新生成（此为自动产物，非手工编辑）
  - `artifacts/domain_terms.txt` — 由 `build_terms` 重新生成（此为自动产物，非手工编辑）
- **修改边界**：不得修改 `terms/` 目录下任何文件。不得修改 pipeline 源代码。artifacts 目录文件仅通过 pipeline 命令重新生成。
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry` → registry OK: 1460 concepts, ~7020 aliases, 1460 evidence rows, no ERROR
  - 运行 `python3 -m pipeline.export_registry --translation-dict` → no ERROR；检查 `artifacts/translation_dict.json` en2zh 条数 ≥ 2774
  - 翻译抽检 5 条：
    - "fire detection system" → 火灾探测系统
    - "bellows" → 波纹管
    - "relief valve" → 安全阀
    - "neutralizer" → 中和器
    - "Penning gauge" → 潘宁真空计
  - 运行 VS Code task `fusion-terms: build final wordlist` → `artifacts/domain_terms.txt` 行数 ≥ 3326
  - 运行 `pytest -q` → all pass
  - 运行 `get_errors` → 无新增 ERROR（pre-existing lint 警告预期存在）
- **验收标准**：
  - ✅ validate_registry: concepts = 1460, evidence = 1460, no ERROR
  - ✅ translation_dict.json en2zh ≥ 2774
  - ✅ 5/5 翻译抽检 PASS
  - ✅ domain_terms.txt ≥ 3326 行
  - ✅ pytest 全部通过
  - ✅ 无新增 lint ERROR
  - ✅ CVS/HEPA/RID/MIG/NEG 各缩写仅映射到 1 个 concept_id
- **潜在风险**：若现有测试中有硬编码的 concept 计数断言，可能需要更新预期值。在 pytest 失败时检查失败原因，若为计数断言则更新。

## 回归检查清单

- [ ] `pytest -q` 全部通过
- [ ] 无新增 lint ERROR（`get_errors`）
- [ ] `python3 -m pipeline.validate_registry` → registry OK, no ERROR
- [ ] `artifacts/translation_dict.json` en2zh ≥ 2774
- [ ] `artifacts/domain_terms.txt` ≥ 3326 行
- [ ] CVS 缩写仅映射到 `confinement-ventilation`
- [ ] HEPA 缩写仅映射到 `hepa-filter`
- [ ] NEG 缩写仅映射到 `non-evaporable-getter`
- [ ] MIG 缩写仅映射到 `magnetron-injection-gun`
- [ ] RID 缩写仅映射到 `residual-ion-dump`
- [ ] 所有 batch9 evidence 行 source = `internal:registry-gap-review:batch9`
- [ ] `sort terms/allowlist_en.txt | uniq -d` 无输出
- [ ] `sort terms/allowlist_zh.txt | uniq -d` 无输出
- [ ] no duplicate concept_id: `cut -f1 terms/registry/concepts.tsv | grep -v '^#' | sort | uniq -d` → empty

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 1 | 1 | 0 |
| R3 | 风险与边缘 | 1 | 1 | 0 |
| **终止** | **T5 — 指标驱动收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（问题描述/目标/非目标/复用分析均存在） |
| 技术方案 | 完整（12 项设计决策、7 文件影响范围） |
| Error & Rescue Map | 9 条路径覆盖，0 CRITICAL GAP |
| 执行计划 | 4 Phases, 7 Tasks |
| 回归检查清单 | 14 项（含 5 项缩写唯一性项目特定检查） |
| 已知局限 | 无 |

### R1 Issues (结构完整性)
- **Issue R1-1**: Batch 87 aliases 验收标准写 51 但实际数据块 52 行 → 重新计数后修正为 52，后因 R3 移除 1 条后归位 51 ✅ 已修正
- **Issue R1-2**: Batch 88 aliases 验收标准写 51 但实际数据块 50 行 → 修正为 50 ✅ 已修正
- **Issue R1-3**: Batch 89 aliases 验收标准写 53 但实际数据块 54 行 → 修正为 54 ✅ 已修正

### R2 Issues (可执行性)
- **Issue R2-1**: Task 4.1 修改内容"无文件修改"与 artifacts 重新生成矛盾 → 明确区分 terms/ 只读 + artifacts/ 自动重新生成 ✅ 已修正

### R3 Issues (风险与边缘)
- **Issue R3-1**: Alias `confinement zone` → `ventilation-zone` 存在语义歧义（可能被误读为 confinement-function 安全壳功能）→ 移除该别名 ✅ 已修正
