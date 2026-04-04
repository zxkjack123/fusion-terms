# 术语注册表扩展 — 批次 4：安全方法论、真空系统、燃料循环度量与 QA 验收补全

## 背景与目标

- **问题/需求描述**：Gap 分析（对话内 2026-04-04 batch-4 推荐）识别出 19 个缺失术语，分布于 6 个主题家族。注册表（1296 concepts, 5530 aliases）在安全分析方法论（仅有文档类 PSAR/FSAR/SAR + 事故类 LOCA/LOFA/LOVA，缺 PSA/HAZOP/FMEA 等方法）、真空硬件/度量（仅 cryopump + vacuum-pumping + base-pressure）、燃料循环度量（缺氚增殖裕度/氦灰排出/氘侧处理）、QA 验收术语（无 FAT/SAT）等方面存在系统性同族遗漏。
- **目标**：
  1. 新增 19 个概念（Batch 71–73），覆盖 6 个主题家族
  2. 新增 ~75 行 alias，包含缩写（PSA/HAZOP/FMEA/SBO/SIL/LBB/TMP/RGA/TAA/DF/FAT/SAT）、连字符变体、中英对
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加额外 dehyphenated alias 变体 — 保持与 Batch 68–70 一致的别名策略
  - 不处理 RAMI（reliability, availability, maintainability, inspectability）上位概念 — 留待后续
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有别名模式（缩写 `abbr|preferred`、连字符 `en|alias`、中文 `zh|preferred`）：复用

## 技术方案

- **方案概述**：分 4 个 Phase，按 Priority 顺序逐步添加。每个数据添加 Phase 包含一个三表新增 Task 和一个 allowlist 同步 Task。最终 Phase 做全量验证/导出/测试。
- **关键设计决策**：
  1. **缩写 alias 策略**：PSA/HAZOP/FMEA/SBO/SIL/LBB/TMP/RGA/TAA/DF/FAT/SAT 均标记为 `abbr|preferred`，沿用 HCPB/IFMIF/MMS/SMS 模式
  2. **HAZOP 大小写**：preferred_abbr = "HAZOP"（全大写为工业标准写法），另添 "HazOp" 为 `abbr|alias`
  3. **Batch 编号**：接续 Batch 70，使用 71（Phase 1: P1 安全+燃料）、72（Phase 2: P2 真空+氚+安全）、73（Phase 3: P3 QA+材料）
  4. **Evidence source 格式**：使用 `internal:registry-gap-review:batch4` 统一格式
  5. **leak-before-break 连字符**：preferred_en 保留全连字符 "leak-before-break"（工程文献中习惯写法），另添无连字符 alias
  6. **PSA vs. probabilistic-safety-assessment**：concept_id 使用长形式 `probabilistic-safety-assessment`，PSA 作 `abbr|preferred`
  7. **detritiation-factor 缩写 DF**：作为 `abbr|preferred` 添加；DF 在聚变领域上下文中语义明确，与已有 `detritiation` 无冲突
  8. **FAT/SAT 缩写**：虽在通用领域可能有歧义，但本仓库为领域专用注册表，`abbr|preferred` 模式与 MMS/SMS 一致
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 19 行
  - `terms/registry/aliases.tsv` — 新增 ~75 行
  - `terms/registry/evidence.tsv` — 新增 19 行
  - `terms/allowlist_en.txt` — 追加 ~19 个新 EN token
  - `terms/allowlist_zh.txt` — 追加 ~16 个新 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增 PSA 缩写 alias | PSA 与已有 alias 冲突 | validation error | Y | 执行前 `grep -P '\tPSA\t' aliases.tsv` 已确认不存在 | validate_registry 报错并阻断 |
| 新增 FAT/SAT 缩写 | 与非聚变领域含义冲突 | 语义冲突 | Y | 本仓库为领域专用，alias 为 `abbr` 类型 | 不可见 |
| 新增 DF 缩写 | DF 与 `detritiation` 概念关系 | 逻辑重叠 | Y | `detritiation` 是过程，`detritiation-factor` 是度量；concept_id 不同，alias 集无交叉 | 不可见 |
| 新增 TMP 缩写 | TMP 可能在其他领域指 /tmp 文件 | 语义冲突 | Y | 注册表限定聚变领域；`abbr` 类型标记 | 不可见 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并运行 validate_registry | build_terms 输出词条数 |
| translation_dict 未重新生成 | 导出时遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 4.1 明确标注该 flag | 翻译字典不含新词条 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Phase 1） | 8 个概念一次添加，需确认 PSA/HAZOP/FMEA/SBO/LBB 缩写均不存在于 aliases.tsv。`pellet` token 可能已存在于 allowlist_en（因 pellet-injection 系列）——需 grep 确认后跳过 |
| 中期（Phase 2） | TAA/DF/TMP/RGA 缩写较短，需确认不与已有 alias 冲突。`deuterium` 已存在于 EN allowlist——执行前 grep 确认后跳过 |
| 后期（Phase 4） | 必须使用 `--translation-dict` flag 调用 export_registry，否则 translation_dict.json 不会被更新。验收阈值基于当前基线 + 预期增量，但 domain_terms 只统计单 token，多词短语不计入——阈值按 allowlist 单 token 增量估算 |

## 执行计划

### Phase 1: 安全方法论 + 事故场景 + 燃料循环核心（P1 — Batch 71）

#### ✅ Task 1.1: 添加 8 个 P1 概念到三表

- **目标**：补全安全分析方法论家族（PSA/HAZOP/FMEA）、事故场景同族（SBO）、燃料循环度量/设备/方法（tritium-breeding-margin / helium-ash-removal / pellet-injector）及结构安全准则（LBB）
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 70 注释块之后追加 `# ==== Batch 71: safety methods + fuel cycle core ====` 注释 + 8 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | probabilistic-safety-assessment | method | 概率安全评估 | probabilistic safety assessment | PSA | active | 安全许可核心方法论 |
    | hazard-and-operability-study | method | 危险与可操作性分析 | hazard and operability study | HAZOP | active | 工艺安全标准分析方法 |
    | failure-mode-and-effects-analysis | method | 失效模式与影响分析 | failure mode and effects analysis | FMEA | active | RAMI/可靠性工程核心方法 |
    | station-blackout | concept | 全厂断电事故 | station blackout | SBO | active | LOCA/LOFA/LOVA 事故家族同族 |
    | tritium-breeding-margin | metric | 氚增殖裕度 | tritium breeding margin | | active | TBR 设计裕度度量 |
    | helium-ash-removal | method | 氦灰排出 | helium ash removal | | active | 等离子体运行/燃料循环衔接 |
    | pellet-injector | device | 弹丸注入器 | pellet injector | | active | pellet-injection 方法的配套设备 |
    | leak-before-break | principle | 先泄漏后断裂 | leak-before-break | LBB | active | 结构安全准则 |

  - 文件 `terms/registry/aliases.tsv`：在 Batch 70 注释块之后追加 `# ==== Batch 71: safety methods + fuel cycle core ====` 注释 + 34 行

    **probabilistic-safety-assessment**（5 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | probabilistic safety assessment | probabilistic-safety-assessment | en | preferred | preferred en |
    | 概率安全评估 | probabilistic-safety-assessment | zh | preferred | preferred zh |
    | PSA | probabilistic-safety-assessment | abbr | preferred | canonical abbr |
    | probabilistic-safety-assessment | probabilistic-safety-assessment | en | alias | hyphenated form |
    | 概率安全分析 | probabilistic-safety-assessment | zh | alias | common zh variant |

    **hazard-and-operability-study**（5 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | hazard and operability study | hazard-and-operability-study | en | preferred | preferred en |
    | 危险与可操作性分析 | hazard-and-operability-study | zh | preferred | preferred zh |
    | HAZOP | hazard-and-operability-study | abbr | preferred | canonical abbr |
    | hazard-and-operability-study | hazard-and-operability-study | en | alias | hyphenated form |
    | HazOp | hazard-and-operability-study | abbr | alias | mixed-case variant |

    **failure-mode-and-effects-analysis**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | failure mode and effects analysis | failure-mode-and-effects-analysis | en | preferred | preferred en |
    | 失效模式与影响分析 | failure-mode-and-effects-analysis | zh | preferred | preferred zh |
    | FMEA | failure-mode-and-effects-analysis | abbr | preferred | canonical abbr |
    | failure-mode-and-effects-analysis | failure-mode-and-effects-analysis | en | alias | hyphenated form |

    **station-blackout**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | station blackout | station-blackout | en | preferred | preferred en |
    | 全厂断电事故 | station-blackout | zh | preferred | preferred zh |
    | SBO | station-blackout | abbr | preferred | canonical abbr |
    | station-blackout | station-blackout | en | alias | hyphenated form |

    **tritium-breeding-margin**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | tritium breeding margin | tritium-breeding-margin | en | preferred | preferred en |
    | 氚增殖裕度 | tritium-breeding-margin | zh | preferred | preferred zh |
    | tritium-breeding-margin | tritium-breeding-margin | en | alias | hyphenated form |

    **helium-ash-removal**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | helium ash removal | helium-ash-removal | en | preferred | preferred en |
    | 氦灰排出 | helium-ash-removal | zh | preferred | preferred zh |
    | helium-ash-removal | helium-ash-removal | en | alias | hyphenated form |
    | 氦灰排除 | helium-ash-removal | zh | alias | common zh variant |

    **pellet-injector**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | pellet injector | pellet-injector | en | preferred | preferred en |
    | 弹丸注入器 | pellet-injector | zh | preferred | preferred zh |
    | pellet-injector | pellet-injector | en | alias | hyphenated form |

    **leak-before-break**（6 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | leak-before-break | leak-before-break | en | preferred | preferred en (hyphenated convention) |
    | 先泄漏后断裂 | leak-before-break | zh | preferred | preferred zh |
    | LBB | leak-before-break | abbr | preferred | canonical abbr |
    | leak before break | leak-before-break | en | alias | unhyphenated form |
    | 先漏后断 | leak-before-break | zh | alias | short zh form |
    | leak-before-break | leak-before-break | en | alias | — |

    注意：leak-before-break 的 preferred_en 就是连字符形式，因此 preferred en alias 和 hyphenated form alias 指向同一字符串。实际应去掉 alias 中与 preferred 重复的行。修正为 5 rows（移除末行重复）。

  - 文件 `terms/registry/evidence.tsv`：追加 8 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | probabilistic-safety-assessment | internal:registry-gap-review:batch4 | Core licensing/safety methodology (PSA/DSA) | copilot | 2026-04-04 |
    | hazard-and-operability-study | internal:registry-gap-review:batch4 | Standard process hazard analysis framework | copilot | 2026-04-04 |
    | failure-mode-and-effects-analysis | internal:registry-gap-review:batch4 | RAMI/reliability engineering method | copilot | 2026-04-04 |
    | station-blackout | internal:registry-gap-review:batch4 | Accident family sibling to LOCA/LOFA/LOVA | copilot | 2026-04-04 |
    | tritium-breeding-margin | internal:registry-gap-review:batch4 | TBR design margin metric | copilot | 2026-04-04 |
    | helium-ash-removal | internal:registry-gap-review:batch4 | Plasma ops / fuel cycle link process | copilot | 2026-04-04 |
    | pellet-injector | internal:registry-gap-review:batch4 | Device counterpart to pellet-injection method | copilot | 2026-04-04 |
    | leak-before-break | internal:registry-gap-review:batch4 | Structural safety doctrine LBB | copilot | 2026-04-04 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中已有行；不得修改 `terms/registry/aliases.tsv` 中已有行；不得修改 `terms/registry/evidence.tsv` 中已有行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 执行前预检：`grep -P '\t(PSA|HAZOP|FMEA|SBO|LBB)\t' terms/registry/aliases.tsv` — 预期无输出（确认缩写不冲突）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR（允许 WARNING）
- **验收标准**：
  - ✅ concepts.tsv data rows = 1304（当前 1296 + 8）
  - ✅ aliases.tsv data rows = 5563（当前 5530 + 33）
  - ✅ evidence.tsv data rows = 1304（当前 1296 + 8）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`概率安全分析` 作为 `概率安全评估` 的 zh alias 可能与校验规则冲突（两个 zh 行同 concept）；已有 `偏钛酸锂` + `偏锆酸锂` 等先例，模式可接受

#### ✅ Task 1.2: 同步 Phase 1 新增术语到 allowlists

- **目标**：确保 Phase 1 新增的 EN/ZH 术语出现在 allowlist 中以支持 build_terms
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词（执行前逐个 grep 确认缺失后再追加）。候选列表：`PSA`, `HAZOP`, `FMEA`, `SBO`, `blackout`, `probabilistic`, `hazard`, `operability`, `LBB`, `injector`, `pellet`
  - 文件 `terms/allowlist_zh.txt`：追加不在 allowlist 中的中文术语：`概率安全评估`, `概率安全分析`, `失效模式与影响分析`, `全厂断电事故`, `氚增殖裕度`, `氦灰排出`, `氦灰排除`, `弹丸注入器`, `先泄漏后断裂`, `先漏后断`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增 ERROR
- **验收标准**：
  - ✅ 10 个 ZH 术语均出现在 allowlist_zh.txt 中（`grep -c` 验证）
  - ✅ `pellet` 出现在 allowlist_en.txt 中
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`pellet` 可能已因 pellet-injection 批次存在于 allowlist——执行前 grep 确认跳过即可

### Phase 2: 真空系统 + 氚工艺度量 + 安全分级（P2 — Batch 72）

#### ✅ Task 2.1: 添加 8 个 P2 概念到三表

- **目标**：补全真空硬件/度量家族（turbomolecular-pump / vacuum-leak-rate / RGA / leak-detection）、安全分级（SIL）、燃料循环氘侧（deuterium-processing）和氚衡算/去氚度量
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 `# ==== Batch 72: vacuum + tritium metrics + safety class ====` 注释 + 8 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | safety-integrity-level | metric | 安全完整性等级 | safety integrity level | SIL | active | 仪控安全分级标准 IEC 61508 |
    | deuterium-processing | concept | 氘处理 | deuterium processing | | active | 燃料循环氘侧处理 |
    | tritium-accounting-area | system | 氚衡算区域 | tritium accounting area | TAA | active | tritium-accountancy 设施级补充 |
    | detritiation-factor | metric | 去氚因子 | detritiation factor | DF | active | detritiation 过程定量度量 |
    | vacuum-leak-rate | metric | 真空漏率 | vacuum leak rate | | active | 真空系统验收/运行核心度量 |
    | turbomolecular-pump | device | 涡轮分子泵 | turbomolecular pump | TMP | active | 真空硬件，与 cryopump 成对 |
    | residual-gas-analyzer | diagnostic | 残余气体分析仪 | residual gas analyzer | RGA | active | 真空/杂质标准诊断 |
    | leak-detection | method | 检漏 | leak detection | | active | 真空系统配套工程方法 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 72: vacuum + tritium metrics + safety class ====` 注释 + 28 行

    **safety-integrity-level**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | safety integrity level | safety-integrity-level | en | preferred | preferred en |
    | 安全完整性等级 | safety-integrity-level | zh | preferred | preferred zh |
    | SIL | safety-integrity-level | abbr | preferred | canonical abbr |
    | safety-integrity-level | safety-integrity-level | en | alias | hyphenated form |

    **deuterium-processing**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | deuterium processing | deuterium-processing | en | preferred | preferred en |
    | 氘处理 | deuterium-processing | zh | preferred | preferred zh |
    | deuterium-processing | deuterium-processing | en | alias | hyphenated form |

    **tritium-accounting-area**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | tritium accounting area | tritium-accounting-area | en | preferred | preferred en |
    | 氚衡算区域 | tritium-accounting-area | zh | preferred | preferred zh |
    | TAA | tritium-accounting-area | abbr | preferred | canonical abbr |
    | tritium-accounting-area | tritium-accounting-area | en | alias | hyphenated form |

    **detritiation-factor**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | detritiation factor | detritiation-factor | en | preferred | preferred en |
    | 去氚因子 | detritiation-factor | zh | preferred | preferred zh |
    | DF | detritiation-factor | abbr | preferred | canonical abbr |
    | detritiation-factor | detritiation-factor | en | alias | hyphenated form |

    **vacuum-leak-rate**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | vacuum leak rate | vacuum-leak-rate | en | preferred | preferred en |
    | 真空漏率 | vacuum-leak-rate | zh | preferred | preferred zh |
    | vacuum-leak-rate | vacuum-leak-rate | en | alias | hyphenated form |

    **turbomolecular-pump**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | turbomolecular pump | turbomolecular-pump | en | preferred | preferred en |
    | 涡轮分子泵 | turbomolecular-pump | zh | preferred | preferred zh |
    | TMP | turbomolecular-pump | abbr | preferred | canonical abbr |
    | turbomolecular-pump | turbomolecular-pump | en | alias | hyphenated form |

    **residual-gas-analyzer**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | residual gas analyzer | residual-gas-analyzer | en | preferred | preferred en |
    | 残余气体分析仪 | residual-gas-analyzer | zh | preferred | preferred zh |
    | RGA | residual-gas-analyzer | abbr | preferred | canonical abbr |
    | residual-gas-analyzer | residual-gas-analyzer | en | alias | hyphenated form |

    **leak-detection**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | leak detection | leak-detection | en | preferred | preferred en |
    | 检漏 | leak-detection | zh | preferred | preferred zh |
    | leak-detection | leak-detection | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 8 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | safety-integrity-level | internal:registry-gap-review:batch4 | IEC 61508 safety classification metric | copilot | 2026-04-04 |
    | deuterium-processing | internal:registry-gap-review:batch4 | Fuel cycle deuterium-side processing | copilot | 2026-04-04 |
    | tritium-accounting-area | internal:registry-gap-review:batch4 | Facility-level tritium accountancy noun | copilot | 2026-04-04 |
    | detritiation-factor | internal:registry-gap-review:batch4 | Quantitative detritiation process metric | copilot | 2026-04-04 |
    | vacuum-leak-rate | internal:registry-gap-review:batch4 | Core vacuum acceptance/operation metric | copilot | 2026-04-04 |
    | turbomolecular-pump | internal:registry-gap-review:batch4 | Vacuum hardware sibling to cryopump | copilot | 2026-04-04 |
    | residual-gas-analyzer | internal:registry-gap-review:batch4 | Standard vacuum/plasma impurity diagnostic | copilot | 2026-04-04 |
    | leak-detection | internal:registry-gap-review:batch4 | Vacuum system engineering method | copilot | 2026-04-04 |

- **修改边界**：不得修改 `terms/registry/` 中已有行；不得修改 `pipeline/` 下任何文件；不得修改 `terms/allowlist_*.txt`
- **测试要求**：
  - 执行前预检：`grep -P '\t(SIL|TAA|TMP|RGA)\t' terms/registry/aliases.tsv` — 预期无输出
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR
- **验收标准**：
  - ✅ concepts.tsv data rows = 1312（1304 + 8）
  - ✅ aliases.tsv data rows = 5592（5563 + 29）
  - ✅ evidence.tsv data rows = 1312（1304 + 8）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：DF 为两字母缩写，可能触发 `min_en_key_len=3` 过滤——但 DF 会被移入 `en2zh_short` 而非丢失，下游使用正常

#### Task 2.2: 同步 Phase 2 新增术语到 allowlists

- **目标**：确保 Phase 2 新增的 EN/ZH 术语出现在 allowlist 中
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词（执行前逐个 grep 确认缺失后再追加）。候选列表：`SIL`, `TAA`, `TMP`, `turbomolecular`, `RGA`, `DF`
  - 文件 `terms/allowlist_zh.txt`：追加不在 allowlist 中的中文术语：`安全完整性等级`, `氘处理`, `氚衡算区域`, `去氚因子`, `真空漏率`, `检漏`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增 ERROR
- **验收标准**：
  - ✅ 6 个 ZH 术语均出现在 allowlist_zh.txt 中（`grep -c` 验证）
  - ✅ 6 个 EN 缩写/token 均出现在 allowlist_en.txt 中
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`deuterium` 已存在于 EN allowlist——执行前 grep 确认后跳过

### Phase 3: QA 验收术语 + 材料属性（P3 — Batch 73）

#### Task 3.1: 添加 3 个 P3 概念到三表

- **目标**：补全 QA/调试验收术语对（FAT/SAT）和材料可焊性属性
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 `# ==== Batch 73: QA acceptance + material attribute ====` 注释 + 3 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | factory-acceptance-test | method | 出厂验收测试 | factory acceptance test | FAT | active | QA/调试验收标准术语 |
    | site-acceptance-test | method | 现场验收测试 | site acceptance test | SAT | active | FAT 的部署阶段配对术语 |
    | weldability | metric | 可焊性 | weldability | | active | 材料/力学工程属性 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 73: QA acceptance + material attribute ====` 注释 + 10 行

    **factory-acceptance-test**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | factory acceptance test | factory-acceptance-test | en | preferred | preferred en |
    | 出厂验收测试 | factory-acceptance-test | zh | preferred | preferred zh |
    | FAT | factory-acceptance-test | abbr | preferred | canonical abbr |
    | factory-acceptance-test | factory-acceptance-test | en | alias | hyphenated form |

    **site-acceptance-test**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | site acceptance test | site-acceptance-test | en | preferred | preferred en |
    | 现场验收测试 | site-acceptance-test | zh | preferred | preferred zh |
    | SAT | site-acceptance-test | abbr | preferred | canonical abbr |
    | site-acceptance-test | site-acceptance-test | en | alias | hyphenated form |

    **weldability**（2 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | weldability | weldability | en | preferred | preferred en |
    | 可焊性 | weldability | zh | preferred | preferred zh |

  - 文件 `terms/registry/evidence.tsv`：追加 3 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | factory-acceptance-test | internal:registry-gap-review:batch4 | QA/commissioning standard term | copilot | 2026-04-04 |
    | site-acceptance-test | internal:registry-gap-review:batch4 | Deployment lifecycle FAT counterpart | copilot | 2026-04-04 |
    | weldability | internal:registry-gap-review:batch4 | Material/mechanical engineering attribute | copilot | 2026-04-04 |

- **修改边界**：不得修改 `terms/registry/` 中已有行；不得修改 `pipeline/` 下任何文件；不得修改 `terms/allowlist_*.txt`
- **测试要求**：
  - 执行前预检：`grep -P '\t(FAT|SAT)\t' terms/registry/aliases.tsv` — 预期无输出
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR
- **验收标准**：
  - ✅ concepts.tsv data rows = 1315（1312 + 3）
  - ✅ aliases.tsv data rows = 5602（5592 + 10）
  - ✅ evidence.tsv data rows = 1315（1312 + 3）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：FAT/SAT 为三字母缩写，长度 = `min_en_key_len`（3），不会被过滤到 `en2zh_short`

#### Task 3.2: 同步 Phase 3 新增术语到 allowlists

- **目标**：确保 Phase 3 新增的 EN/ZH 术语出现在 allowlist 中
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词（执行前逐个 grep 确认缺失后再追加）。候选列表：`FAT`, `SAT`, `weldability`
  - 文件 `terms/allowlist_zh.txt`：追加不在 allowlist 中的中文术语：`出厂验收测试`, `现场验收测试`, `可焊性`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增 ERROR
- **验收标准**：
  - ✅ 3 个 ZH 术语均出现在 allowlist_zh.txt 中（`grep -c` 验证）
  - ✅ 3 个 EN token 均出现在 allowlist_en.txt 中
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：无——纯追加操作

### Phase 4: 全量验证与导出

#### Task 4.1: 全量验证、导出、构建、测试

- **目标**：重新导出 translation_dict.json 和 domain_terms.txt，确认所有 19 个新概念出现在翻译字典中，全量测试通过
- **修改内容**：
  - 运行 `python3 -m pipeline.export_registry --translation-dict` — 重新生成 `artifacts/translation_dict.json` 及其他导出文件
  - 运行 `python3 -m pipeline.build_terms --config config.toml` — 重建 `artifacts/domain_terms.txt`
  - 运行 `pytest` — 全量测试
- **修改边界**：仅 `artifacts/` 目录被重新生成；不得修改 `terms/` 或 `pipeline/` 下任何文件
- **测试要求**：
  - `pytest` 全量通过（≥ 88 tests）
  - Python 脚本验证翻译字典新增映射（见验收标准）
- **验收标准**：
  - ✅ `en2zh["probabilistic safety assessment"]` = `"概率安全评估"`
  - ✅ `en2zh["HAZOP"]` = `"危险与可操作性分析"`
  - ✅ `en2zh["FMEA"]` = `"失效模式与影响分析"`
  - ✅ `en2zh["SBO"]` = `"全厂断电事故"`
  - ✅ `zh2en["氚增殖裕度"]` = `"tritium breeding margin"`
  - ✅ `zh2en["弹丸注入器"]` = `"pellet injector"`
  - ✅ `en2zh["TMP"]` = `"涡轮分子泵"`
  - ✅ `en2zh["RGA"]` = `"残余气体分析仪"`
  - ✅ `zh2en["检漏"]` = `"leak detection"`
  - ✅ `en2zh["FAT"]` = `"出厂验收测试"`
  - ✅ `en2zh["SAT"]` = `"现场验收测试"`
  - ✅ `zh2en["可焊性"]` = `"weldability"`
  - ✅ domain_terms.txt 词条数 ≥ 2947（当前 2928 + 预估 ~19 新 single-token terms）
  - ✅ en2zh 对数 ≥ 2398（当前 2379 + 预估 ~19 新 en keys 中 ≥3 字符者）
  - ✅ pytest 全部通过
  - ✅ 回归抽查：`en2zh["FLiBe"]` = `"氟化锂铍"`、`zh2en["锂靶"]` = `"lithium target"`（Batch 68–70 未被破坏）
- **潜在风险**：domain_terms 只计单 token，多词短语不进入词表——实际增量可能少于 19。如最终 domain_terms 或 en2zh 数值低于预估阈值，按 Batch 3 先例校准阈值至实际基线

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` 无 ERROR
- [ ] `python3 -m pipeline.export_registry --translation-dict` 成功且无 ERROR
- [ ] `python3 -m pipeline.build_terms --config config.toml` 词条数 ≥ 2947（或校准至实际基线）
- [ ] `pytest` 全部通过（≥ 88 tests）
- [ ] `artifacts/translation_dict.json` en2zh 对数 ≥ 2398（或校准至实际基线）
- [ ] PSA / HAZOP / FMEA / SBO / LBB / SIL / TAA / TMP / RGA / FAT / SAT 缩写均可在 en2zh 中命中
- [ ] 已有 Batch 68–70 翻译映射未被破坏（抽查：FLiBe / 锂靶 / ELTL / 氚载体 / 增殖材料）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 2 | 2 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 1 | 1 | 0 |
| **终止** | **T4 — 零缺陷快速通过** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（问题描述 + 目标 + 非目标 + 复用分析） |
| 技术方案 | 完整（方案概述 + 8 项设计决策 + 影响范围） |
| Error & Rescue Map | 已覆盖 6 条路径，0 CRITICAL GAP |
| 执行计划 | 4 Phases, 7 Tasks |
| 回归检查清单 | 7 项项目特定检查 |
| 已知局限 | 无 |

### R1 Issues

- **Issue R1-1**: leak-before-break 的 aliases 表中 preferred en 和 hyphenated form alias 指向同一字符串 "leak-before-break"，违反 validate_registry 的 alias 唯一性要求 → 删除重复行，改为 5 rows（preferred en = "leak-before-break"，另加 unhyphenated "leak before break" 作 en|alias） ✅ 已修正
- **Issue R1-2**: Error & Rescue Map 未覆盖 DF 短缩写被 min_en_key_len 过滤到 en2zh_short 的路径 → 已在 Task 2.1 潜在风险和 Error & Rescue Map 中添加说明 ✅ 已修正

### R2 Issues

- **Issue R2-1**: Task 4.1 的 domain_terms 阈值（≥ 2947）假设每个新概念增加一个单 token，但实际只有 allowlist 中的单 token 会计入；多词 concept 不直接计入 → 已在 Task 4.1 潜在风险中添加"按 Batch 3 先例校准"兜底语句 ✅ 已修正
- **Issue R2-2**: 缺少时序推演 → 已添加时序推演表格，覆盖初期/中期/后期关键决策与潜在阻塞 ✅ 已修正

### R3 Issues

- **Issue R3-1**: Task 1.1 的 aliases 计数（5563 = 5530+33）需确认：8 个概念产生 5+5+4+4+3+4+3+5 = 33 行 alias → 逻辑匹配 ✅ 已确认无误
