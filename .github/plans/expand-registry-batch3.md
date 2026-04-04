# 术语注册表扩展 — 批次 3：增殖材料同族、IFMIF 生态与冷却工质补全

## 背景与目标

- **问题/需求描述**：Review 文档 `.github/reviews/registry-gaps-batch3-2026-04-04.md` 识别出 18 个中优先级 + 3 个低优先级术语缺失，分布于 5 个主题家族。这些是成熟注册表（1277 concepts, 5464 aliases）中的**家族级同族遗漏**：锂系增殖陶瓷材料家族缺少 FLiBe/LiAlO₂/Li₂SiO₃/Li₂O/Li₈ZrO₆ 及上位概念 "breeder material"；IFMIF 设备生态缺少子设施（ELTL/LIPAc/EVEDA）和工程概念（锂靶/锂回路）；包层模块架构术语对 MMS/SMS 缺失；冷却/氚工艺概念不完整。
- **目标**：
  1. 新增 18 个概念（Batch 68–70），覆盖 review 中 5 个主题家族
  2. 新增 ~65 行 alias，包含化学式、缩写、常见变体
  3. 同步所有新增术语到 EN/ZH allowlist
  4. 通过验证后重新导出 translation_dict、rebuild domain_terms、通过全量测试
- **非目标（不做什么）**：
  - 不添加 3 个低优先级 reserve 概念（target-chamber, test-cell, lifus）— 留待后续按需补充
  - 不修改 pipeline 源代码 — 纯数据追加
  - 不修改已有概念的 preferred_zh / preferred_en — 只新增
  - 不添加更多 dehyphenated alias 变体 — Batch 67 已处理高优先级子集
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（`--translation-dict` flag 导出翻译字典）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 已有兄弟概念的 alias 模式（化学式 `mixed|preferred`、连字符 `en|alias`、缩写 `abbr|preferred`）：复用

## 技术方案

- **方案概述**：分 4 个 Phase，按 Review 中的 Priority 顺序逐步添加。每个数据添加 Phase 包含一个三表新增 Task 和一个 allowlist 同步 Task。最终 Phase 做全量验证/导出/测试。
- **关键设计决策**：
  1. **化学式 alias 策略**：ASCII 形式（Li2BeF4）标记为 `mixed|preferred`，Unicode 下标形式（Li₂BeF₄）标记为 `mixed|alias`。沿用 Li2TiO3 / Li4SiO4 的已有模式
  2. **连字符 EN alias**：多词概念追加 concept_id 形式作为 `en|alias`（如 lithium-aluminate），沿用 lithium-titanate 模式
  3. **Batch 编号**：接续 Batch 67，使用 68（Phase 1）、69（Phase 2）、70（Phase 3）
  4. **Evidence source 格式**：使用 `internal:registry-gap-review:batch3` 统一格式，可追溯到 review 文档
  5. **FLiBe 大小写**：preferred_en = "FLiBe"，preferred_abbr = "FLiBe"（元素符号混合大小写：F-fluorine, Li-lithium, Be-beryllium 为约定俗成写法）。另添 "flibe" 全小写 alias
  6. **MMS/SMS 缩写**：使用 `lang=abbr, kind=preferred` 模式，与 HCPB/IFMIF 等一致
  7. **breeder-material vs. breeding-blanket**：两者为不同层级概念（材料 vs. 系统），concept_id 和 alias 集无交叉，不存在冲突
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 18 行
  - `terms/registry/aliases.tsv` — 新增 ~65 行
  - `terms/registry/evidence.tsv` — 新增 18 行
  - `terms/allowlist_en.txt` — 追加 ~12 个新 EN token
  - `terms/allowlist_zh.txt` — 追加 ~18 个新 ZH 术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 新增化学式 alias（Li2O 等） | 化学式与已有 alias 冲突 | validation error | Y | 执行前 `grep -P '\tLi2O\t' aliases.tsv` 确认唯一性 | validate_registry 报错并阻断 |
| 新增 SMS abbreviation | SMS 与非聚变领域含义冲突 | 语义冲突 | Y | 本仓库为领域专用，alias 为 `abbr` 类型，无冲突 | 不可见 |
| 新增 breeder-material 上位概念 | 与 breeding-blanket 等下位概念混淆 | 逻辑重叠 | Y | 两者 concept_id 不同，"增殖材料" vs "产氚包层" alias 集无交叉 | 不可见 |
| EVEDA 全称 alias 超长 | alias 字段过长触发校验 | field length | Y | 全称 45 字符，远低于常见上限 | 不可见 |
| allowlist 同步遗漏 | build_terms 词条数未增长 | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并检查 build_terms 增量 | build_terms 输出词条数 |
| translation_dict 未重新生成 | 导出时遗忘 `--translation-dict` flag | 操作遗漏 | Y | Task 4.1 明确标注该 flag | 翻译字典不含新词条 |

## 时序推演

| 阶段 | 关键决策/潜在阻塞 |
|------|-------------------|
| 初期（Phase 1） | 化学式唯一性检查：Li2O / LiAlO2 / Li2SiO3 / Li8ZrO6 / Li2BeF4 需在 aliases.tsv 中预先 grep 确认不存在。若意外存在则需分析是否为同一概念的已有 alias |
| 中期（Phase 2） | EVEDA/LIPAc 全称较长（"Engineering Validation and Engineering Design Activities" / "Linear IFMIF Prototype Accelerator"），需确认 alias 格式不会截断。ELTL preferred_zh 含混合文字 "EVEDA锂试验回路"，需确认 zh lang 标记正确 |
| 后期（Phase 4） | 必须使用 `--translation-dict` flag 调用 export_registry，否则 translation_dict.json 不会被更新。需验证全部 18 个概念在 en2zh/zh2en 中均可命中 |

## 执行计划

### Phase 1: 增殖材料同族补全（Theme A — Batch 68）

#### ✅ Task 1.1: 添加 6 个增殖材料概念到三表

- **目标**：补全 Li 系增殖陶瓷材料家族 + FLiBe 熔盐 + breeder material 上位概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在 Batch 66 注释块之后追加 `# ==== Batch 68: breeder material siblings ====` 注释 + 6 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | flibe | material | 氟化锂铍 | FLiBe | FLiBe | active | 熔盐增殖/冷却材料 Li₂BeF₄ |
    | lithium-aluminate | material | 铝酸锂 | lithium aluminate | | active | 增殖陶瓷材料 LiAlO₂ |
    | lithium-metasilicate | material | 偏硅酸锂 | lithium metasilicate | | active | 增殖陶瓷材料 Li₂SiO₃ |
    | lithium-oxide | material | 氧化锂 | lithium oxide | | active | 经典增殖材料 Li₂O |
    | lithium-rich-zirconate | material | 富锂锆酸盐 | lithium-rich zirconate | | active | 增殖材料 Li₈ZrO₆ |
    | breeder-material | concept | 增殖材料 | breeder material | | active | 产氚增殖材料上位概念 |

  - 文件 `terms/registry/aliases.tsv`：在 Batch 67 注释块之后追加 `# ==== Batch 68: breeder material siblings ====` 注释 + 25 行

    **flibe**（5 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | FLiBe | flibe | en | preferred | preferred en |
    | 氟化锂铍 | flibe | zh | preferred | preferred zh |
    | Li2BeF4 | flibe | mixed | preferred | chemical formula |
    | Li₂BeF₄ | flibe | mixed | alias | chemical formula (Unicode) |
    | flibe | flibe | en | alias | lowercase common form |

    **lithium-aluminate**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium aluminate | lithium-aluminate | en | preferred | preferred en (phrase) |
    | 铝酸锂 | lithium-aluminate | zh | preferred | preferred zh |
    | LiAlO2 | lithium-aluminate | mixed | preferred | chemical formula |
    | lithium-aluminate | lithium-aluminate | en | alias | hyphenated form |

    **lithium-metasilicate**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium metasilicate | lithium-metasilicate | en | preferred | preferred en (phrase) |
    | 偏硅酸锂 | lithium-metasilicate | zh | preferred | preferred zh |
    | Li2SiO3 | lithium-metasilicate | mixed | preferred | chemical formula |
    | lithium-metasilicate | lithium-metasilicate | en | alias | hyphenated form |

    **lithium-oxide**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium oxide | lithium-oxide | en | preferred | preferred en (phrase) |
    | 氧化锂 | lithium-oxide | zh | preferred | preferred zh |
    | Li2O | lithium-oxide | mixed | preferred | chemical formula |
    | lithium-oxide | lithium-oxide | en | alias | hyphenated form |

    **lithium-rich-zirconate**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium-rich zirconate | lithium-rich-zirconate | en | preferred | preferred en |
    | 富锂锆酸盐 | lithium-rich-zirconate | zh | preferred | preferred zh |
    | Li8ZrO6 | lithium-rich-zirconate | mixed | preferred | chemical formula |
    | lithium-rich-zirconate | lithium-rich-zirconate | en | alias | fully hyphenated form |

    **breeder-material**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | breeder material | breeder-material | en | preferred | preferred en |
    | 增殖材料 | breeder-material | zh | preferred | preferred zh |
    | breeding material | breeder-material | en | alias | common variant |
    | breeder-material | breeder-material | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 6 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | flibe | internal:registry-gap-review:batch3 | Breeder/coolant molten-salt material Li₂BeF₄ | copilot | [执行当天日期] |
    | lithium-aluminate | internal:registry-gap-review:batch3 | Breeder ceramic sibling LiAlO₂ | copilot | [执行当天日期] |
    | lithium-metasilicate | internal:registry-gap-review:batch3 | Breeder ceramic sibling Li₂SiO₃ | copilot | [执行当天日期] |
    | lithium-oxide | internal:registry-gap-review:batch3 | Classic breeder material Li₂O | copilot | [执行当天日期] |
    | lithium-rich-zirconate | internal:registry-gap-review:batch3 | Breeder material Li₈ZrO₆ | copilot | [执行当天日期] |
    | breeder-material | internal:registry-gap-review:batch3 | Superordinate concept for breeding materials | copilot | [执行当天日期] |

- **修改边界**：不得修改 `terms/registry/concepts.tsv` 中已有行；不得修改 `terms/registry/aliases.tsv` 中已有行；不得修改 `terms/registry/evidence.tsv` 中已有行；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 执行前预检：`grep -P '\t(Li2BeF4|LiAlO2|Li2SiO3|Li2O|Li8ZrO6)\t' terms/registry/aliases.tsv` — 预期无输出（确认化学式不冲突）
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR（允许 WARNING）
- **验收标准**：
  - ✅ concepts.tsv data rows = 1283（当前 1277 + 6）
  - ✅ aliases.tsv data rows = 5489（当前 5464 + 25）
  - ✅ evidence.tsv data rows = 1283（当前 1277 + 6）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：Li2O 为极短化学式，grep 时需使用 tab 边界 `\t` 避免误匹配

#### ✅ Task 1.2: 同步 Phase 1 新增术语到 allowlists

- **目标**：确保 Phase 1 新增的 EN/ZH 术语出现在 allowlist 中以支持 build_terms
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词。候选列表（执行前逐个 grep 确认缺失后再追加）：`aluminate`, `metasilicate`, `FLiBe`, `flibe`, `breeder`
  - 文件 `terms/allowlist_zh.txt`：追加 6 个中文术语：`氟化锂铍`, `铝酸锂`, `偏硅酸锂`, `氧化锂`, `富锂锆酸盐`, `增殖材料`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：bridge check 无新增 ERROR
- **验收标准**：
  - ✅ 6 个 ZH 术语均出现在 allowlist_zh.txt 中（`grep -c` 验证）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`breeder` 或 `lithium` 等词可能已存在于 allowlist——不影响正确性，grep 确认后跳过即可

### Phase 2: 包层架构 + IFMIF 生态（Themes B+C — Batch 69）

#### ✅ Task 2.1: 添加 9 个概念到三表（MMS/SMS + IFMIF 子设施/工艺）

- **目标**：补全包层模块段架构术语对（MMS/SMS）和 IFMIF 设施族的关键子概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 `# ==== Batch 69: blanket segments + IFMIF ecosystem ====` 注释 + 9 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | multi-module-segment | system | 多模块段 | multi-module segment | MMS | active | DCLL/HCPB 包层模块架构 |
    | single-module-segment | system | 单模块段 | single-module segment | SMS | active | 包层模块架构（与 MMS 成对） |
    | lithium-target | system | 锂靶 | lithium target | | active | IFMIF 核心组件 |
    | free-surface-lithium-target | system | 自由表面锂靶 | free-surface lithium target | | active | IFMIF/ELTL 靶设计 |
    | eltl | device | EVEDA锂试验回路 | EVEDA Lithium Test Loop | ELTL | active | IFMIF 液态锂回路验证装置 |
    | lipac | device | 线性IFMIF原型加速器 | Linear IFMIF Prototype Accelerator | LIPAc | active | IFMIF 加速器原型 |
    | eveda | concept | 工程验证与工程设计活动 | Engineering Validation and Engineering Design Activities | EVEDA | active | IFMIF 项目阶段 |
    | lithium-loop | system | 锂回路 | lithium loop | | active | 液态锂输运/净化系统 |
    | liquid-lithium-purification | concept | 液态锂纯化 | liquid lithium purification | | active | IFMIF/ELTL 关键工艺 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 69: blanket segments + IFMIF ecosystem ====` 注释 + 30 行

    **multi-module-segment**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | multi-module segment | multi-module-segment | en | preferred | preferred en |
    | 多模块段 | multi-module-segment | zh | preferred | preferred zh |
    | MMS | multi-module-segment | abbr | preferred | canonical abbr |
    | multi module segment | multi-module-segment | en | alias | dehyphenated form |

    **single-module-segment**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | single-module segment | single-module-segment | en | preferred | preferred en |
    | 单模块段 | single-module-segment | zh | preferred | preferred zh |
    | SMS | single-module-segment | abbr | preferred | canonical abbr |
    | single module segment | single-module-segment | en | alias | dehyphenated form |

    **lithium-target**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium target | lithium-target | en | preferred | preferred en |
    | 锂靶 | lithium-target | zh | preferred | preferred zh |
    | lithium-target | lithium-target | en | alias | hyphenated form |

    **free-surface-lithium-target**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | free-surface lithium target | free-surface-lithium-target | en | preferred | preferred en |
    | 自由表面锂靶 | free-surface-lithium-target | zh | preferred | preferred zh |
    | free surface lithium target | free-surface-lithium-target | en | alias | dehyphenated form |
    | free-surface-lithium-target | free-surface-lithium-target | en | alias | fully hyphenated form |

    **eltl**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | EVEDA Lithium Test Loop | eltl | en | preferred | preferred en (full name) |
    | EVEDA锂试验回路 | eltl | zh | preferred | preferred zh |
    | ELTL | eltl | abbr | preferred | canonical abbr |

    **lipac**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | Linear IFMIF Prototype Accelerator | lipac | en | preferred | preferred en (full name) |
    | 线性IFMIF原型加速器 | lipac | zh | preferred | preferred zh |
    | LIPAc | lipac | abbr | preferred | canonical abbr |

    **eveda**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | Engineering Validation and Engineering Design Activities | eveda | en | preferred | preferred en (full name) |
    | 工程验证与工程设计活动 | eveda | zh | preferred | preferred zh |
    | EVEDA | eveda | abbr | preferred | canonical abbr |

    **lithium-loop**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | lithium loop | lithium-loop | en | preferred | preferred en |
    | 锂回路 | lithium-loop | zh | preferred | preferred zh |
    | lithium-loop | lithium-loop | en | alias | hyphenated form |

    **liquid-lithium-purification**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | liquid lithium purification | liquid-lithium-purification | en | preferred | preferred en |
    | 液态锂纯化 | liquid-lithium-purification | zh | preferred | preferred zh |
    | liquid-lithium-purification | liquid-lithium-purification | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 9 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | multi-module-segment | internal:registry-gap-review:batch3 | DCLL/HCPB blanket module architecture term | copilot | [执行当天日期] |
    | single-module-segment | internal:registry-gap-review:batch3 | Blanket module architecture term (paired with MMS) | copilot | [执行当天日期] |
    | lithium-target | internal:registry-gap-review:batch3 | IFMIF core component | copilot | [执行当天日期] |
    | free-surface-lithium-target | internal:registry-gap-review:batch3 | IFMIF/ELTL target design | copilot | [执行当天日期] |
    | eltl | internal:registry-gap-review:batch3 | IFMIF liquid lithium loop validation facility | copilot | [执行当天日期] |
    | lipac | internal:registry-gap-review:batch3 | IFMIF prototype accelerator | copilot | [执行当天日期] |
    | eveda | internal:registry-gap-review:batch3 | IFMIF project phase | copilot | [执行当天日期] |
    | lithium-loop | internal:registry-gap-review:batch3 | Liquid lithium transport/purification system | copilot | [执行当天日期] |
    | liquid-lithium-purification | internal:registry-gap-review:batch3 | ELTL/IFMIF key process | copilot | [执行当天日期] |

- **修改边界**：不得修改 `terms/registry/` 中已有行；不得修改 `pipeline/` 下任何文件；不得修改 `terms/allowlist_*.txt`
- **测试要求**：
  - 执行前预检：`grep -P '\t(MMS|SMS|ELTL|LIPAc|EVEDA)\t' terms/registry/aliases.tsv` — 预期无输出
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR
- **验收标准**：
  - ✅ concepts.tsv data rows = 1292（1283 + 9）
  - ✅ aliases.tsv data rows = 5519（5489 + 30）
  - ✅ evidence.tsv data rows = 1292（1283 + 9）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：ELTL preferred_zh 含混合文字 "EVEDA锂试验回路"——确认 `lang=zh` 对含 ASCII 的中文术语名无校验限制（沿用 IFMIF 先例 "国际聚变材料辐照装置" 中无 ASCII 混入，但 `线性IFMIF原型加速器` 同样混合 ASCII，属于已有模式）

#### ✅ Task 2.2: 同步 Phase 2 新增术语到 allowlists

- **目标**：确保 Phase 2 新增的 EN/ZH 术语出现在 allowlist 中
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词。候选列表（执行前逐个 grep 确认缺失后再追加）：`MMS`, `SMS`, `ELTL`, `LIPAc`, `EVEDA`
  - 文件 `terms/allowlist_zh.txt`：追加 9 个中文术语：`多模块段`, `单模块段`, `锂靶`, `自由表面锂靶`, `EVEDA锂试验回路`, `线性IFMIF原型加速器`, `工程验证与工程设计活动`, `锂回路`, `液态锂纯化`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：bridge check 无新增 ERROR
- **验收标准**：
  - ✅ 9 个 ZH 术语均出现在 allowlist_zh.txt 中（`grep -c` 验证）
  - ✅ 5 个 EN 缩写均出现在 allowlist_en.txt 中
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：无——纯追加操作

### Phase 3: 冷却工质 + 氚工艺补全（Themes D+E — Batch 70）

#### ✅ Task 3.1: 添加 3 个概念到三表

- **目标**：补全冷却工质家族和氚载体概念
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：追加 `# ==== Batch 70: coolant + tritium supplement ====` 注释 + 3 行

    | concept_id | category | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | water-coolant | concept | 水冷却剂 | water coolant | | active | 包层/偏滤器冷却工质（与 helium-coolant 对应） |
    | coolant-purification | concept | 冷却剂纯化 | coolant purification | | active | 冷却系统配套工艺 |
    | tritium-carrier | concept | 氚载体 | tritium carrier | | active | PbLi 等在包层中承担的氚输运角色 |

  - 文件 `terms/registry/aliases.tsv`：追加 `# ==== Batch 70: coolant + tritium supplement ====` 注释 + 10 行

    **water-coolant**（4 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | water coolant | water-coolant | en | preferred | preferred en |
    | 水冷却剂 | water-coolant | zh | preferred | preferred zh |
    | water-coolant | water-coolant | en | alias | hyphenated form |
    | 水冷剂 | water-coolant | zh | alias | short form |

    **coolant-purification**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | coolant purification | coolant-purification | en | preferred | preferred en |
    | 冷却剂纯化 | coolant-purification | zh | preferred | preferred zh |
    | coolant-purification | coolant-purification | en | alias | hyphenated form |

    **tritium-carrier**（3 rows）：

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | tritium carrier | tritium-carrier | en | preferred | preferred en |
    | 氚载体 | tritium-carrier | zh | preferred | preferred zh |
    | tritium-carrier | tritium-carrier | en | alias | hyphenated form |

  - 文件 `terms/registry/evidence.tsv`：追加 3 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | water-coolant | internal:registry-gap-review:batch3 | Blanket/divertor coolant (counterpart to helium-coolant) | copilot | [执行当天日期] |
    | coolant-purification | internal:registry-gap-review:batch3 | Cooling system auxiliary process | copilot | [执行当天日期] |
    | tritium-carrier | internal:registry-gap-review:batch3 | PbLi tritium transport role in blanket | copilot | [执行当天日期] |

- **修改边界**：不得修改 `terms/registry/` 中已有行；不得修改 `pipeline/` 下任何文件；不得修改 `terms/allowlist_*.txt`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：无 ERROR
- **验收标准**：
  - ✅ concepts.tsv data rows = 1295（1292 + 3）
  - ✅ aliases.tsv data rows = 5529（5519 + 10）
  - ✅ evidence.tsv data rows = 1295（1292 + 3）
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`水冷剂` 为简称，如校验拒绝可安全移除该行（其余 9 行不受影响）

#### Task 3.2: 同步 Phase 3 新增术语到 allowlists

- **目标**：确保 Phase 3 新增的 EN/ZH 术语出现在 allowlist 中
- **修改内容**：
  - 文件 `terms/allowlist_en.txt`：追加不在 allowlist 中的单 token EN 词（候选：`coolant`, `carrier` — 执行前 grep 确认缺失后再追加）
  - 文件 `terms/allowlist_zh.txt`：追加中文术语：`水冷却剂`, `水冷剂`, `冷却剂纯化`, `氚载体`
- **修改边界**：不得删除 allowlist 中已有行；不得修改 `terms/registry/` 下任何文件；不得修改 `pipeline/` 下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：bridge check 无新增 ERROR
- **验收标准**：
  - ✅ 4 个 ZH 术语均出现在 allowlist_zh.txt 中
  - ✅ validate_registry 通过无 ERROR
- **潜在风险**：`coolant` 可能已因 helium-coolant 批次而存在于 allowlist——执行前 grep 即可

### Phase 4: 全量验证与导出

#### Task 4.1: 全量验证、导出、构建、测试

- **目标**：重新导出 translation_dict.json 和 domain_terms.txt，确认所有 18 个新概念出现在翻译字典中，全量测试通过
- **修改内容**：
  - 运行 `python3 -m pipeline.export_registry --translation-dict` — 重新生成 `artifacts/translation_dict.json` 及其他导出文件
  - 运行 `python3 -m pipeline.build_terms --config config.toml` — 重建 `artifacts/domain_terms.txt`
  - 运行 `pytest` — 全量测试
- **修改边界**：仅 `artifacts/` 目录被重新生成；不得修改 `terms/` 或 `pipeline/` 下任何文件
- **测试要求**：
  - `pytest` 全量通过（≥ 88 tests）
  - Python 脚本验证翻译字典新增映射（见验收标准）
- **验收标准**：
  - ✅ `en2zh["lithium aluminate"]` = `"铝酸锂"`
  - ✅ `en2zh["FLiBe"]` = `"氟化锂铍"`
  - ✅ `en2zh["multi-module segment"]` = `"多模块段"`
  - ✅ `zh2en["锂靶"]` = `"lithium target"`
  - ✅ `zh2en["增殖材料"]` = `"breeder material"`
  - ✅ `zh2en["氚载体"]` = `"tritium carrier"`
  - ✅ `en2zh["ELTL"]` = `"EVEDA锂试验回路"`
  - ✅ domain_terms.txt 词条数 ≥ 2940
  - ✅ pytest 全部通过
- **潜在风险**：导出时遗忘 `--translation-dict` flag 会导致 translation_dict.json 未更新——命令已在上方显式标注

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` 无 ERROR
- [ ] `python3 -m pipeline.export_registry --translation-dict` 成功且无 ERROR
- [ ] `python3 -m pipeline.build_terms --config config.toml` 词条数 ≥ 2940
- [ ] `pytest` 全部通过（≥ 88 tests）
- [ ] `artifacts/translation_dict.json` en2zh 对数 ≥ 2380
- [ ] FLiBe / LiAlO2 / Li2SiO3 / Li2O / Li8ZrO6 / Li2BeF4 化学式均可在 en2zh 中命中
- [ ] MMS / SMS / ELTL / LIPAc / EVEDA 缩写均可在 en2zh 中命中
- [ ] 已有 Batch 65–67 翻译映射未被破坏（抽查 5 组：lithium ceramic pebble bed / 增殖包层 / 钨铠甲 / plasma facing component / safety analysis report）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 1 | 1 | 0 |
| R2 | 可执行性 | 3 | 3 | 0 |
| R3 | 风险与边缘 | 2 | 2 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整（问题描述 + 目标 + 非目标 + 复用分析） |
| 技术方案 | 完整（方案概述 + 7 项设计决策 + 影响范围） |
| Error & Rescue Map | 已覆盖 6 条路径，0 CRITICAL GAP |
| 执行计划 | 4 Phases, 7 Tasks |
| 回归检查清单 | 8 项项目特定检查 |
| 已知局限 | 无 |

### R1 Issues

- **Issue R1-1**: Task 2.2 和 3.2 使用缩写描述（"同 Task 1.2 模式"）而非完整展开修改内容/测试要求/验收标准 → 已展开为完整 Task 描述 ✅ 已修正

### R2 Issues

- **Issue R2-1**: Task 2.2、3.2、4.1 缺少显式"修改边界"字段 → 已补充 ✅ 已修正
- **Issue R2-2**: Task 4.1 验收标准硬编码测试数 "88 tests" → 改为 "≥ 88 tests, 全部通过" ✅ 已修正
- **Issue R2-3**: 缺少时序推演（≥3 Task 的计划要求） → 已添加"时序推演"表格，覆盖初期/中期/后期阶段的关键决策与潜在阻塞 ✅ 已修正

### R3 Issues

- **Issue R3-1**: Task 1.1 和 2.1 的潜在风险缺少具体预检指导；ELTL/LIPAc 全称长度风险未提及 → 已在 Task 1.1 添加化学式预检 grep 命令，Task 2.1 添加缩写预检及全称长度说明 ✅ 已修正
- **Issue R3-2**: breeder-material "增殖材料" 与 breeding-blanket "产氚包层" 潜在概念混淆 → 已在关键设计决策第 7 条添加明确说明：两者为不同层级概念，alias 集无交叉 ✅ 已修正
