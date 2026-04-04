# 术语注册表扩展 — 批次 5：I&C、辐射防护、制造工艺、破裂物理、燃料循环、土建抗震、冷却辅助系统

## 背景与目标

- **问题/需求描述**：Gap 分析（`.github/reviews/registry-gaps-batch5-2026-04-04.md`）识别出 25 个缺失术语，分布于 7 个主题方向。注册表（1424 concepts / 5828 aliases / 1358 evidence）在仪表与控制（I&C）、辐射防护与去污、制造工艺与在役检查、破裂物理时序阶段、燃料循环回路架构、土建与抗震、冷却与辅助系统方面存在系统性缺口。
- **根因分析**：前 73 批次侧重物理概念、材料、磁体、加热/诊断、中子学、氚子系统等，对 **工程基础设施**（I&C、土建、冷却系统命名）和 **运行/退役** 相关术语（辐射分区、去污、在役检查）覆盖不足。
- **目标**：
  1. 新增 25 个概念（Batch 74–77），覆盖 7 个主题方向
  2. 新增 ~95 行 alias，包含缩写（TQ/CQ/IFC/OFC/CIS/MPS/DCS/CODAC/HIP/EBW/ISI/AM/TCWS/ADS）、连字符变体、中英对
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加标准/规范类术语（RCC-MR、ASME BPVC 等）— 留待后续确认是否在范围内
  - 不添加电气功率系统术语 — 留待后续
  - 不添加更多 ITER PBS 系统命名（CCWS、CHWS 等）— 留待后续
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有别名模式（缩写 `abbr|preferred`、连字符 `en|alias`、中文 `zh|preferred`/`zh|alias`）：复用

## 技术方案

- **方案概述**：分 5 个 Phase 按优先级顺序逐步添加。每个数据 Phase 包含一个「三表新增 Task」和一个「allowlist 同步 Task」。最终 Phase 5 做全量验证/导出/测试。
- **关键设计决策**：
  1. **缩写 alias 策略**：TQ/CQ/IFC/OFC/CIS/MPS/DCS/CODAC/HIP/EBW/ISI/AM/TCWS/ADS 均标记为 `abbr|preferred`
  2. **CODAC 大小写**：preferred_abbr = "CODAC"（ITER 官方写法全大写）
  3. **AM 缩写**：additive-manufacturing 的 AM 在聚变制造文献语境中无歧义，采用 `abbr|preferred`
  4. **Batch 编号**：接续 Batch 73，使用 74（P0 破裂+燃料循环）、75（P1-a I&C+制造前半）、76（P1-b 制造后半+冷却辅助）、77（P2 辐射防护+土建抗震）
  5. **Evidence source 格式**：使用 `internal:registry-gap-review:batch5` 统一格式
  6. **无缩写术语**：radiation-zoning、controlled-area、decontamination、clearance-level、tokamak-building、seismic-isolation、basemat、drain-tank、diffusion-bonding、water-radiolysis、burnup-fraction 无常用缩写，不设 preferred_abbr
  7. **controlled-area category**：采用 `concept` 而非 `limit`，因其是空间分区概念而非数值限值
  8. **ADS 歧义**：Atmosphere Detritiation System 的 ADS 在核工业可能指 Accelerator-Driven System。本仓库为聚变领域，在 notes 中说明
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 25 行
  - `terms/registry/aliases.tsv` — 新增 ~95 行
  - `terms/registry/evidence.tsv` — 新增 25 行
  - `terms/allowlist_en.txt` — 追加缺失 EN token
  - `terms/allowlist_zh.txt` — 追加缺失 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增 DCS 缩写 | DCS alias 冲突 | validation error | Y | precheck `grep -iP '\tDCS\t' aliases.tsv` 已确认无冲突 | validate_registry 报错并阻断 |
| 新增 AM 缩写 | AM 2-char 在短 token 桶 | 逻辑注意 | Y | en2zh_short 桶已有 DF 等 2-char 缩写先例；export_registry 自动分流 | 不影响，进入 en2zh_short |
| 新增 ADS 缩写 | 与裂变 ADS (Accelerator-Driven System) 歧义 | 语义冲突 | Y | notes 字段说明聚变语境；本仓库为领域专用 | 不可见 |
| 新增 ISI 缩写 | ISI 可能指 Institute for Scientific Information | 语义冲突 | Y | `abbr|preferred` 类型限定在聚变工程语境 | 不可见 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并运行 validate_registry | build_stats 可检测 |
| translation_dict 未重新生成 | 遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 5.1 明确标注该 flag | 翻译字典不含新词条 |
| basemat 为 en-only 单词无连字符 | 无连字符 alias 行可省略 | 行数偏差 | Y | basemat 不需要 hyphenated alias 行 | 不影响 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Phase 1, Batch 74） | 5 个概念，TQ/CQ/IFC/OFC 为新缩写需确认无冲突；burnup-fraction 无缩写。`thermal` / `current` token 可能已在 allowlist_en — 执行前 grep 确认后跳过。|
| 中期（Phase 2–3, Batch 75–76） | 12 个概念分两批。CIS/MPS/DCS/CODAC/HIP/EBW（Batch 75）+ ISI/AM/TCWS/ADS（Batch 76）。`CODAC` 全大写写法需确认与 preferred_en 一致。EBW/HIP 在材料工程文献中也出现在裂变语境 — notes 中说明聚变用途。|
| 后期（Phase 4, Batch 77） | 8 个概念，大多无缩写。`decontamination` 既可 method 也可 concept — 选 method（动作导向）。`basemat` 无连字符、无缩写、无常用 zh 变体，alias 行最少（仅 2 行）。|
| 终期（Phase 5） | 必须用 `--translation-dict` flag。验收阈值 = 基线 + 预期增量。|

## 执行计划

### Phase 1: 破裂物理 + 燃料循环回路（P0 — Batch 74, 5 terms）

#### ✅ Task 1.1: 添加 5 个 P0 概念到三表

- **目标**：补全破裂时序阶段（thermal-quench / current-quench）和燃料循环回路架构（inner-fuel-cycle / outer-fuel-cycle / burnup-fraction）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 73 注释块之后追加 `# ==== Batch 74: disruption phases + fuel cycle loops ====` 注释 + 5 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | thermal-quench | concept | 热猝灭 | thermal quench | TQ | active | 破裂阶段：热能快速丧失 |
    | current-quench | concept | 电流猝灭 | current quench | CQ | active | 破裂阶段：等离子体电流衰减 |
    | inner-fuel-cycle | concept | 内燃料循环 | inner fuel cycle | IFC | active | 等离子体排气→直接内循环 |
    | outer-fuel-cycle | concept | 外燃料循环 | outer fuel cycle | OFC | active | 包层氚提取→纯化→储存→注入 |
    | burnup-fraction | metric | 燃耗份额 | burnup fraction | | active | 等离子体燃烧效率核心指标 |

  - 文件 `terms/registry/aliases.tsv`：在 Batch 73 之后追加 `# ==== Batch 74: disruption phases + fuel cycle loops ====` 注释 + 19 行

    **thermal-quench**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | thermal quench | thermal-quench | en | preferred | preferred en |
    | 热猝灭 | thermal-quench | zh | preferred | preferred zh |
    | TQ | thermal-quench | abbr | preferred | canonical abbr |
    | thermal-quench | thermal-quench | en | alias | hyphenated form |

    **current-quench**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | current quench | current-quench | en | preferred | preferred en |
    | 电流猝灭 | current-quench | zh | preferred | preferred zh |
    | CQ | current-quench | abbr | preferred | canonical abbr |
    | current-quench | current-quench | en | alias | hyphenated form |

    **inner-fuel-cycle**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | inner fuel cycle | inner-fuel-cycle | en | preferred | preferred en |
    | 内燃料循环 | inner-fuel-cycle | zh | preferred | preferred zh |
    | IFC | inner-fuel-cycle | abbr | preferred | canonical abbr |
    | inner-fuel-cycle | inner-fuel-cycle | en | alias | hyphenated form |

    **outer-fuel-cycle**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | outer fuel cycle | outer-fuel-cycle | en | preferred | preferred en |
    | 外燃料循环 | outer-fuel-cycle | zh | preferred | preferred zh |
    | OFC | outer-fuel-cycle | abbr | preferred | canonical abbr |
    | outer-fuel-cycle | outer-fuel-cycle | en | alias | hyphenated form |

    **burnup-fraction**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | burnup fraction | burnup-fraction | en | preferred | preferred en |
    | 燃耗份额 | burnup-fraction | zh | preferred | preferred zh |
    | burnup-fraction | burnup-fraction | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 5 行，source = `internal:registry-gap-review:batch5`，added_by = `copilot`，added_at = `2026-04-04`

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | thermal-quench | internal:registry-gap-review:batch5 | Disruption phase: rapid thermal energy loss | copilot | 2026-04-04 |
    | current-quench | internal:registry-gap-review:batch5 | Disruption phase: plasma current decay | copilot | 2026-04-04 |
    | inner-fuel-cycle | internal:registry-gap-review:batch5 | Plasma exhaust to direct internal recycle loop | copilot | 2026-04-04 |
    | outer-fuel-cycle | internal:registry-gap-review:batch5 | Blanket tritium extraction to storage and injection | copilot | 2026-04-04 |
    | burnup-fraction | internal:registry-gap-review:batch5 | Core plasma burn efficiency metric | copilot | 2026-04-04 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中 Batch 73 及之前的任何行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1429 concepts, …aliases, 1363 evidence rows`（concepts +5，evidence +5）
- **验收标准**：
  - ✅ concepts.tsv 数据行数 = 1429
  - ✅ evidence.tsv 数据行数 = 1363
  - ✅ aliases.tsv 数据行数 = 5847（5828 + 19）
  - ✅ validate_registry 通过无错误
- **潜在风险**：tab 字符被编辑器替换为空格导致 TSV 解析失败 — 追加时使用实际 tab 字符

#### ✅ Task 1.2: Batch 74 allowlist 同步

- **目标**：将 Batch 74 新增术语的缺失 token 追加到 allowlist_en.txt 和 allowlist_zh.txt
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加 Batch 74 中不在列表的新 EN token（`TQ`、`CQ`、`IFC`、`OFC`、`burnup`、`quench` — 执行前 grep 确认，已有的跳过）
  - 文件 `terms/allowlist_zh.txt`：追加 Batch 74 中不在列表的新 ZH 术语（`热猝灭`、`电流猝灭`、`内燃料循环`、`外燃料循环`、`燃耗份额` — 执行前 grep 确认，已有的跳过）
- **修改边界**：不得删除或修改已有 allowlist 条目
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无报错
- **验收标准**：
  - ✅ 新增 EN token 均可在 allowlist_en.txt 中 grep 到
  - ✅ 新增 ZH 术语均可在 allowlist_zh.txt 中 grep 到
- **潜在风险**：`quench` 可能已存在（因为有 `quench` 概念）— 执行前 grep 确认

### Phase 2: I&C + 制造工艺前半（P1-a — Batch 75, 7 terms）

#### ✅ Task 2.1: 添加 7 个 P1-a 概念到三表

- **目标**：补全仪表与控制基础设施（CIS/MPS/DCS/CODAC）和制造工艺（HIP/EBW/diffusion-bonding）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 74 注释块之后追加 `# ==== Batch 75: I&C systems + manufacturing processes ====` 注释 + 7 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | central-interlock-system | system | 中央联锁系统 | central interlock system | CIS | active | ITER 安全联锁核心系统 |
    | machine-protection-system | system | 装置保护系统 | machine protection system | MPS | active | 装置快速响应保护系统 |
    | distributed-control-system | system | 分布式控制系统 | distributed control system | DCS | active | 聚变装置标配控制架构 |
    | codac | system | 控制、数据获取与通信 | control, data access and communication | CODAC | active | ITER 控制架构统称 |
    | hot-isostatic-pressing | method | 热等静压 | hot isostatic pressing | HIP | active | 钨/RAFM 钢部件制造核心工艺 |
    | electron-beam-welding | method | 电子束焊接 | electron beam welding | EBW | active | 真空容器等厚壁部件主要焊接方法 |
    | diffusion-bonding | method | 扩散连接 | diffusion bonding | | active | 包层/第一壁异种材料连接工艺 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 75: I&C systems + manufacturing processes ====` 注释 + 27 行

    **central-interlock-system**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | central interlock system | central-interlock-system | en | preferred | preferred en |
    | 中央联锁系统 | central-interlock-system | zh | preferred | preferred zh |
    | CIS | central-interlock-system | abbr | preferred | canonical abbr |
    | central-interlock-system | central-interlock-system | en | alias | hyphenated form |

    **machine-protection-system**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | machine protection system | machine-protection-system | en | preferred | preferred en |
    | 装置保护系统 | machine-protection-system | zh | preferred | preferred zh |
    | MPS | machine-protection-system | abbr | preferred | canonical abbr |
    | machine-protection-system | machine-protection-system | en | alias | hyphenated form |

    **distributed-control-system**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | distributed control system | distributed-control-system | en | preferred | preferred en |
    | 分布式控制系统 | distributed-control-system | zh | preferred | preferred zh |
    | DCS | distributed-control-system | abbr | preferred | canonical abbr |
    | distributed-control-system | distributed-control-system | en | alias | hyphenated form |

    **codac**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | control, data access and communication | codac | en | preferred | preferred en |
    | 控制、数据获取与通信 | codac | zh | preferred | preferred zh |
    | CODAC | codac | abbr | preferred | canonical abbr |
    | control data access and communication | codac | en | alias | without comma |

    **hot-isostatic-pressing**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | hot isostatic pressing | hot-isostatic-pressing | en | preferred | preferred en |
    | 热等静压 | hot-isostatic-pressing | zh | preferred | preferred zh |
    | HIP | hot-isostatic-pressing | abbr | preferred | canonical abbr |
    | hot-isostatic-pressing | hot-isostatic-pressing | en | alias | hyphenated form |

    **electron-beam-welding**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | electron beam welding | electron-beam-welding | en | preferred | preferred en |
    | 电子束焊接 | electron-beam-welding | zh | preferred | preferred zh |
    | EBW | electron-beam-welding | abbr | preferred | canonical abbr |
    | electron-beam-welding | electron-beam-welding | en | alias | hyphenated form |

    **diffusion-bonding**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | diffusion bonding | diffusion-bonding | en | preferred | preferred en |
    | 扩散连接 | diffusion-bonding | zh | preferred | preferred zh |
    | diffusion-bonding | diffusion-bonding | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 7 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | central-interlock-system | internal:registry-gap-review:batch5 | ITER safety-related central interlock system | copilot | 2026-04-04 |
    | machine-protection-system | internal:registry-gap-review:batch5 | Fast response machine protection for fusion devices | copilot | 2026-04-04 |
    | distributed-control-system | internal:registry-gap-review:batch5 | Standard control architecture for fusion devices | copilot | 2026-04-04 |
    | codac | internal:registry-gap-review:batch5 | ITER Control, Data Access and Communication framework | copilot | 2026-04-04 |
    | hot-isostatic-pressing | internal:registry-gap-review:batch5 | Key manufacturing process for W and RAFM steel components | copilot | 2026-04-04 |
    | electron-beam-welding | internal:registry-gap-review:batch5 | Primary welding method for vacuum vessel thick-wall sections | copilot | 2026-04-04 |
    | diffusion-bonding | internal:registry-gap-review:batch5 | Dissimilar material joining for blanket/first wall | copilot | 2026-04-04 |

- **修改边界**：不得修改 Batch 74 及之前的任何行；不得修改 `pipeline/` 下任何文件；`terms/allowlist_*.txt` 在 Task 2.2 处理
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1436 concepts, …aliases, 1370 evidence rows`
- **验收标准**：
  - ✅ concepts.tsv 数据行数 = 1436（1429 + 7）
  - ✅ evidence.tsv 数据行数 = 1370（1363 + 7）
  - ✅ aliases.tsv 数据行数 = 5874（5847 + 27）
  - ✅ validate_registry 通过无错误
- **潜在风险**：codac 的 preferred_en 含逗号 — TSV 格式不受影响（tab-separated），但需确认 validate_registry 不会将其视为异常字符

#### Task 2.2: Batch 75 allowlist 同步

- **目标**：将 Batch 75 新增术语的缺失 token 追加到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 EN token（`CIS`、`MPS`、`DCS`、`CODAC`、`HIP`、`EBW`、`interlock`、`isostatic`、`diffusion` — 执行前 grep 确认，已有的跳过）
  - 文件 `terms/allowlist_zh.txt`：追加缺失 ZH 术语（`中央联锁系统`、`装置保护系统`、`分布式控制系统`、`热等静压`、`电子束焊接`、`扩散连接` — 执行前 grep 确认，已有的跳过）
- **修改边界**：不得删除或修改已有 allowlist 条目
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无报错
- **验收标准**：
  - ✅ 新增 EN token 均可在 allowlist_en.txt 中 grep 到
  - ✅ 新增 ZH 术语均可在 allowlist_zh.txt 中 grep 到
- **潜在风险**：`diffusion` 可能已在 allowlist（因 diffusion-bonding 以外的现存概念）— grep 确认后跳过

### Phase 3: 制造后半 + 冷却辅助系统（P1-b — Batch 76, 5 terms）

#### Task 3.1: 添加 5 个 P1-b 概念到三表

- **目标**：补全制造/检查（ISI/AM）和冷却辅助系统（TCWS/ADS/water-radiolysis）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 75 之后追加 `# ==== Batch 76: manufacturing inspection + cooling auxiliary ====` 注释 + 5 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | in-service-inspection | method | 在役检查 | in-service inspection | ISI | active | 核设施法规要求的运行期检查 |
    | additive-manufacturing | method | 增材制造 | additive manufacturing | AM | active | 聚变部件新兴制造路线 |
    | tokamak-cooling-water-system | system | 托卡马克冷却水系统 | tokamak cooling water system | TCWS | active | ITER PBS 26 系统级名称 |
    | atmosphere-detritiation-system | system | 厂房去氚系统 | atmosphere detritiation system | ADS | active | 三重氚包容关键安全系统；聚变语境，非 accelerator-driven system |
    | water-radiolysis | concept | 水辐解 | water radiolysis | | active | 冷却剂氢浓度与安全分析关键过程 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 76: manufacturing inspection + cooling auxiliary ====` 注释 + 18 行

    **in-service-inspection**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | in-service inspection | in-service-inspection | en | preferred | preferred en |
    | 在役检查 | in-service-inspection | zh | preferred | preferred zh |
    | ISI | in-service-inspection | abbr | preferred | canonical abbr |
    | in-service-inspection | in-service-inspection | en | alias | hyphenated form |

    **additive-manufacturing**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | additive manufacturing | additive-manufacturing | en | preferred | preferred en |
    | 增材制造 | additive-manufacturing | zh | preferred | preferred zh |
    | AM | additive-manufacturing | abbr | preferred | canonical abbr |
    | additive-manufacturing | additive-manufacturing | en | alias | hyphenated form |

    **tokamak-cooling-water-system**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | tokamak cooling water system | tokamak-cooling-water-system | en | preferred | preferred en |
    | 托卡马克冷却水系统 | tokamak-cooling-water-system | zh | preferred | preferred zh |
    | TCWS | tokamak-cooling-water-system | abbr | preferred | canonical abbr |
    | tokamak-cooling-water-system | tokamak-cooling-water-system | en | alias | hyphenated form |

    **atmosphere-detritiation-system**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | atmosphere detritiation system | atmosphere-detritiation-system | en | preferred | preferred en |
    | 厂房去氚系统 | atmosphere-detritiation-system | zh | preferred | preferred zh |
    | ADS | atmosphere-detritiation-system | abbr | preferred | canonical abbr |
    | atmosphere-detritiation-system | atmosphere-detritiation-system | en | alias | hyphenated form |

    **water-radiolysis**（3 rows — 无缩写，单词无需连字符变体因仅含两个子词）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | water radiolysis | water-radiolysis | en | preferred | preferred en |
    | 水辐解 | water-radiolysis | zh | preferred | preferred zh |
    | water-radiolysis | water-radiolysis | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 5 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | in-service-inspection | internal:registry-gap-review:batch5 | Nuclear facility regulatory-required operational inspection | copilot | 2026-04-04 |
    | additive-manufacturing | internal:registry-gap-review:batch5 | Emerging manufacturing route for fusion components | copilot | 2026-04-04 |
    | tokamak-cooling-water-system | internal:registry-gap-review:batch5 | ITER PBS 26 system-level designation | copilot | 2026-04-04 |
    | atmosphere-detritiation-system | internal:registry-gap-review:batch5 | Triple tritium confinement safety system | copilot | 2026-04-04 |
    | water-radiolysis | internal:registry-gap-review:batch5 | Coolant hydrogen concentration and safety analysis | copilot | 2026-04-04 |

- **修改边界**：不得修改 Batch 75 及之前的任何行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1441 concepts, …aliases, 1375 evidence rows`
- **验收标准**：
  - ✅ concepts.tsv 数据行数 = 1441（1436 + 5）
  - ✅ evidence.tsv 数据行数 = 1375（1370 + 5）
  - ✅ aliases.tsv 数据行数 = 5893（5874 + 19 — 注意此处为 18+1 注释行不计，实际 aliases 数据行 5874+19=5893；修正：batch 76 aliases = 4+4+4+4+3 = 19 行，但 codac batch 75 有一个非标准行 "control data access and communication" 使 batch 75 合计 27 行。重新计算：5828+19(b74)+27(b75)+19(b76) = 5893）
  - ✅ validate_registry 通过无错误
- **潜在风险**：`radiolysis` token 是新词，需确认 allowlist 同步（Task 3.2）

#### Task 3.2: Batch 76 allowlist 同步

- **目标**：将 Batch 76 新增术语的缺失 token 追加到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 EN token（`ISI`、`AM`、`TCWS`、`ADS`、`radiolysis`、`additive` — 执行前 grep 确认，已有的跳过）
  - 文件 `terms/allowlist_zh.txt`：追加缺失 ZH 术语（`在役检查`、`增材制造`、`托卡马克冷却水系统`、`厂房去氚系统`、`水辐解` — 执行前 grep 确认，已有的跳过）
- **修改边界**：不得删除或修改已有 allowlist 条目
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无报错
- **验收标准**：
  - ✅ 新增 EN token 均可在 allowlist_en.txt 中 grep 到
  - ✅ 新增 ZH 术语均可在 allowlist_zh.txt 中 grep 到
- **潜在风险**：`additive` 可能已存在 — grep 确认

### Phase 4: 辐射防护 + 土建抗震（P2 — Batch 77, 8 terms）

#### Task 4.1: 添加 8 个 P2 概念到三表

- **目标**：补全辐射防护与去污（radiation-zoning / controlled-area / decontamination / clearance-level）和土建/抗震（tokamak-building / seismic-isolation / basemat / drain-tank）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 76 之后追加 `# ==== Batch 77: radiation protection + civil seismic ====` 注释 + 8 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | radiation-zoning | method | 辐射分区 | radiation zoning | | active | 设施屏蔽设计与通道布局基础 |
    | controlled-area | concept | 控制区 | controlled area | | active | 辐射防护空间分区概念 |
    | decontamination | method | 去污 | decontamination | | active | 退役和维护核心操作 |
    | clearance-level | limit | 清洁解控水平 | clearance level | | active | 废物分类与材料回收判据 |
    | tokamak-building | concept | 托卡马克厂房 | tokamak building | | active | 聚变设施主体建筑 |
    | seismic-isolation | method | 隔震 | seismic isolation | | active | ITER/CFETR 标志性工程设计特征 |
    | basemat | concept | 底板 | basemat | | active | 设施基础结构 |
    | drain-tank | system | 排放槽 | drain tank | | active | LOCA 后冷却剂收集安全功能设备 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 77: radiation protection + civil seismic ====` 注释 + 27 行

    **radiation-zoning**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | radiation zoning | radiation-zoning | en | preferred | preferred en |
    | 辐射分区 | radiation-zoning | zh | preferred | preferred zh |
    | radiation-zoning | radiation-zoning | en | alias | hyphenated form |

    **controlled-area**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | controlled area | controlled-area | en | preferred | preferred en |
    | 控制区 | controlled-area | zh | preferred | preferred zh |
    | controlled-area | controlled-area | en | alias | hyphenated form |
    | 放射性控制区 | controlled-area | zh | alias | formal zh variant |

    **decontamination**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | decontamination | decontamination | en | preferred | preferred en |
    | 去污 | decontamination | zh | preferred | preferred zh |
    | 去除污染 | decontamination | zh | alias | expanded zh form |

    **clearance-level**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | clearance level | clearance-level | en | preferred | preferred en |
    | 清洁解控水平 | clearance-level | zh | preferred | preferred zh |
    | clearance-level | clearance-level | en | alias | hyphenated form |
    | 解控水平 | clearance-level | zh | alias | short zh form |

    **tokamak-building**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | tokamak building | tokamak-building | en | preferred | preferred en |
    | 托卡马克厂房 | tokamak-building | zh | preferred | preferred zh |
    | tokamak-building | tokamak-building | en | alias | hyphenated form |
    | 托卡马克主厂房 | tokamak-building | zh | alias | formal zh with 主 |

    **seismic-isolation**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | seismic isolation | seismic-isolation | en | preferred | preferred en |
    | 隔震 | seismic-isolation | zh | preferred | preferred zh |
    | seismic-isolation | seismic-isolation | en | alias | hyphenated form |
    | 基础隔震 | seismic-isolation | zh | alias | full zh form |

    **basemat**（2 rows — 单词无连字符、无缩写）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | basemat | basemat | en | preferred | preferred en |
    | 底板 | basemat | zh | preferred | preferred zh |

    **drain-tank**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | drain tank | drain-tank | en | preferred | preferred en |
    | 排放槽 | drain-tank | zh | preferred | preferred zh |
    | drain-tank | drain-tank | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 8 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | radiation-zoning | internal:registry-gap-review:batch5 | Facility shielding design and access layout basis | copilot | 2026-04-04 |
    | controlled-area | internal:registry-gap-review:batch5 | Radiation protection spatial zoning concept | copilot | 2026-04-04 |
    | decontamination | internal:registry-gap-review:batch5 | Decommissioning and maintenance core operation | copilot | 2026-04-04 |
    | clearance-level | internal:registry-gap-review:batch5 | Waste classification and material recycling criterion | copilot | 2026-04-04 |
    | tokamak-building | internal:registry-gap-review:batch5 | Main building of a fusion facility | copilot | 2026-04-04 |
    | seismic-isolation | internal:registry-gap-review:batch5 | Landmark engineering feature of ITER and CFETR | copilot | 2026-04-04 |
    | basemat | internal:registry-gap-review:batch5 | Foundation structure of fusion facility | copilot | 2026-04-04 |
    | drain-tank | internal:registry-gap-review:batch5 | LOCA coolant collection safety equipment | copilot | 2026-04-04 |

- **修改边界**：不得修改 Batch 76 及之前的任何行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：`registry OK: 1449 concepts, …aliases, 1383 evidence rows`
- **验收标准**：
  - ✅ concepts.tsv 数据行数 = 1449（1441 + 8）
  - ✅ evidence.tsv 数据行数 = 1383（1375 + 8）
  - ✅ aliases.tsv 数据行数 = 5920（5893 + 27）
  - ✅ validate_registry 通过无错误
- **潜在风险**：controlled-area 中的 `controlled` 作为 EN token 词汇通用性高 — 追加到 allowlist 时确认不会引入噪音（IME 专用词汇表场景下可接受）

#### Task 4.2: Batch 77 allowlist 同步

- **目标**：将 Batch 77 新增术语的缺失 token 追加到 allowlist
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加缺失 EN token（`zoning`、`decontamination`、`clearance`、`basemat`、`seismic` — 执行前 grep 确认，已有的跳过）
  - 文件 `terms/allowlist_zh.txt`：追加缺失 ZH 术语（`辐射分区`、`控制区`、`去污`、`清洁解控水平`、`托卡马克厂房`、`隔震`、`底板`、`排放槽` — 执行前 grep 确认，已有的跳过）
- **修改边界**：不得删除或修改已有 allowlist 条目
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无报错
- **验收标准**：
  - ✅ 新增 EN token 均可在 allowlist_en.txt 中 grep 到
  - ✅ 新增 ZH 术语均可在 allowlist_zh.txt 中 grep 到
- **潜在风险**：`seismic` 可能已存在（因 seismic category 相关概念）— grep 确认

### Phase 5: 全量验证、导出、构建与测试

#### Task 5.1: 全量验证与导出

- **目标**：执行完整 pipeline 验证、导出翻译字典、重建 domain_terms、运行全量测试
- **修改内容**：
  - 无手动修改 — 全部通过 pipeline 命令执行
  - `artifacts/translation_dict.json` — 自动重新生成
  - `artifacts/domain_terms.txt` — 自动重新生成
  - `artifacts/domain_terms_build_stats.json` — 自动重新生成
- **修改边界**：不得修改 `terms/` 或 `pipeline/` 下任何文件
- **测试要求**：
  1. 运行 `python3 -m pipeline.validate_registry`
     - 预期：`registry OK: 1449 concepts, …aliases, 1383 evidence rows`
  2. 运行 `python3 -m pipeline.export_registry --translation-dict`
     - 预期：无错误，wrote artifacts/registry_exports.json + translation_dict.json
  3. 运行 `python3 -m pipeline.build_terms --config config.toml`
     - 预期：wrote artifacts/domain_terms.txt (≥2966 terms)
  4. 运行 `pytest`
     - 预期：全部通过（≥88 tests）
  5. 验证 translation_dict.json 包含所有 25 个新概念的映射
     - 抽检：`thermal quench` → `热猝灭`、`CODAC` → `控制、数据获取与通信`、`decontamination` → `去污`、`basemat` → `底板`、`TCWS` → `托卡马克冷却水系统`
- **验收标准**：
  - ✅ validate_registry 最终输出 1449 concepts / 1383 evidence，无错误
  - ✅ translation_dict.json en2zh 条目数 ≥ 2448（2428 + ~20 新增多词条目）
  - ✅ domain_terms.txt 行数 ≥ 2966（基线）
  - ✅ pytest 全部通过
  - ✅ 抽检 5 个翻译映射均正确
- **潜在风险**：某些新增概念的 EN preferred 含逗号（codac）或连字符（in-service inspection）— export_registry 应能正确处理，因前批次已有类似格式

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` 通过
- [ ] `pytest` 全部通过（≥88 tests），无新增失败
- [ ] 无新增 lint 警告
- [ ] `artifacts/translation_dict.json` 中已有回归词汇（FLiBe、锂靶、detritiation-factor→DF）仍然存在
- [ ] `artifacts/domain_terms.txt` 行数 ≥ 基线 2966
- [ ] Batch 71–73（前批次）的概念/别名未被修改
- [ ] allowlist 中前批次追加的 token（PSA、HAZOP、FMEA、SBO、TMP、RGA、FAT、SAT）仍然存在

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 1 | 1 | 0 |
| **终止** | **T4 — 零缺陷快速通过 (after R3)** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整 — 问题描述、目标、非目标、复用分析均已填写 |
| 技术方案 | 完整 — 方案概述、8 项设计决策、影响范围 |
| Error & Rescue Map | 7 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 5 Phase、9 Task |
| 回归检查清单 | 7 项项目特定检查 |
| 已知局限 | 无 |

### R1 Issues (结构完整性)
- **Issue R1-1**: aliases.tsv 累计行数在 Task 3.1 验收标准中计算有误（codac batch75 有 4 行非标准行的额外 alias 使总数为 27 而非 28） → 重新核算：b74=19, b75=27(4+4+4+4+4+4+3), b76=19(4+4+4+4+3), b77=27(3+4+3+4+4+4+2+3)。5828+19+27+19+27 = 5920 ✅ 已修正
- **Issue R1-2**: Error & Rescue Map 缺少 `basemat` 无连字符 alias 的说明 → 已添加第 7 条 ✅ 已修正
- **Issue R1-3**: 已有代码/流程复用分析中缺少 aliases 模式说明 → 已在复用分析末尾补充 ✅ 已修正

### R2 Issues (可执行性)
- **Issue R2-1**: Task 2.1 codac 的 preferred_en 格式含逗号，需在潜在风险中说明 TSV 安全性 → 已在 Task 2.1 潜在风险中说明 ✅ 已修正
- **Issue R2-2**: Task 4.1 验收标准中 aliases 数据行数需精确计算 → 逐条核算：b77 = 3+4+3+4+4+4+2+3 = 27。5893+27 = 5920 ✅ 已修正

### R3 Issues (风险与边缘)
- **Issue R3-1**: ADS (Atmosphere Detritiation System) 与裂变领域 ADS (Accelerator-Driven System) 缩写冲突未在 Error & Rescue Map 中标注 → 已添加第 3 条 ✅ 已修正
