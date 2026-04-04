# 修复翻译字典缺失词条与结构性改进

## 背景与目标

- **问题/需求描述**：`translation_dict.json` 的贪心最长匹配扫描在遇到 "lithium ceramic pebble bed" 时，因字典中缺少 `lithium ceramic` / `lithium ceramic pebble bed` / `ceramic pebble bed` 等词条，导致 LLM 兜底翻译产生 "电荷交换复合光谱 球床" 的幻觉。类似的缺失词条（共 ~20 条 en2zh + ~11 条 zh2en）导致检索翻译出错或覆盖率不足。此外存在结构性问题：连字符变体缺失（用户查询不带连字符时无法命中）、部分缩写缺失（WCPB）、有效 deprecated 别名阻断了合理的 zh2en 映射。
- **根因分析**：
  1. 锂陶瓷/铍球床等包层材料概念未在 registry 中注册
  2. 部分已有 concept 缺少常用 alias 变体（无连字符版、短形式、中文同义词）
  3. "增殖包层"、"环向场线圈" 被标记 deprecated，但用户查询中频繁使用，translation_dict 导出时被过滤
  4. 270 个含连字符的 EN alias 没有对应的无连字符版本，用户搜索无法命中
- **目标**：
  1. 补充 P0（直接导致翻译错误的 12 个缺失 concept）+ P1（提升覆盖率的 5 个 concept）
  2. 修复已有 concept 的 alias 缺失/状态问题（~10 项修改）
  3. 批量添加高优先级无连字符 EN alias 变体
  4. 通过验证后重新导出 translation_dict、build_terms
- **非目标（不做什么）**：
  - 不修改 pipeline 源代码 — 翻译管道本身无需改动
  - 不全量修复 270 个无连字符变体 — Phase 4 仅处理高优先级子集（~50 条）
  - 不修改 concept 的 preferred_zh/preferred_en — 只新增 concept 或添加/调整 alias
  - 不处理 125 个 ASCII 代码名的 zh alias 缺失 — 这些代码名通过 abbr/en 语言门控已在 en2zh 中正常工作
- **已有代码/流程复用分析**：
  - `pipeline/validate_registry.py`：复用（验证新增数据）
  - `pipeline/export_registry.py`：复用（重新导出 translation_dict.json）
  - `pipeline/build_terms.py`：复用（重建 IME 词表）
  - 现有 alias kind（deprecated → alias 升级方案）：复用现有 kind 定义，不引入新值

## 技术方案

- **方案概述**：分 5 个 Phase：P0 新建 concept → P0 修复已有 alias → P1 补充 concept → 结构性改进（无连字符变体）→ 全量验证导出。每 Phase 修改三表 + allowlist，逐步验证。
- **关键设计决策**：
  1. **deprecated → alias 升级**：对 "增殖包层"（breeding-blanket）和 "环向场线圈"（toroidal-field-coil），将 kind 从 `deprecated` 改为 `alias`，同时保留 comment（追加"升级为alias"备注）。preferred_zh 保持不变（产氚包层/纵场线圈）
  2. **"接触剂量" deprecated → alias 升级**：当前 "接触剂量" 是 `contact-dose-rate` 的 deprecated alias（comment："缺字'率'"），但用户确实使用"接触剂量"查询。升级为 alias 以支持检索
  3. **in-vessel/ex-vessel 作为独立概念**：已有 `in-vessel-loca` / `ex-vessel-loca` 仅覆盖 LOCA 场景。新建 `in-vessel` / `ex-vessel` 通用概念，覆盖 "堆内部件"/"堆外系统" 等泛化用法
  4. **无连字符变体策略**：仅为已有连字符 EN alias（lang=en, kind=preferred|alias）中的高优先级子集添加无连字符版（用空格替换连字符），跳过：(a) 结果与原文相同的，(b) 替换后与已有 alias 冲突的，(c) "X-ray"/"7-X" 等连字符属于专有名称/化学式的
  5. **Batch 编号**：接续 Batch 65（当前最高为 64）
- **影响范围**：
  - `terms/registry/concepts.tsv` — 新增 ~17 行
  - `terms/registry/aliases.tsv` — 新增 ~70 行 + 修改 ~3 行（deprecated→alias）
  - `terms/registry/evidence.tsv` — 新增 ~17 行
  - `terms/allowlist_en.txt` — 追加新增英文单 token
  - `terms/allowlist_zh.txt` — 追加新增中文术语
  - `artifacts/translation_dict.json` — 重新生成
  - `artifacts/domain_terms.txt` — 重新生成

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| 修改 deprecated→alias 行 | 修改后 alias 与其他 concept 冲突 | validation error | Y | 预先 grep 检查唯一性 | validate_registry 报错并阻断 |
| 添加无连字符变体 alias | 新 alias 与已有 alias 重复 | validation error | Y | 脚本预检排除冲突项 | validate_registry 报错并阻断 |
| 新建 concept preferred_zh 与已有 zh alias 冲突 | alias 唯一性约束 | validation error | Y | 建表前 grep 检查 | validate_registry 报错并阻断 |
| 修改 deprecated alias 后 bridge check 失败 | allowlist 包含 deprecated/forbidden 项 | bridge check error | Y | 升级为 alias 后不再触发 bridge check | 不可见 |
| build_terms 词条数下降 | 新术语未同步到 allowlist | 逻辑遗漏 | Y | 每 Phase 同步 allowlist 并对比词条数 | build_terms 输出新词条数 |

## 执行计划

### Phase 1: P0 — 新建缺失 concept

#### ✅ Task 1.1: 添加 12 个 P0 缺失 concept 到三表

- **目标**：补充直接导致翻译错误和检索缺失的 12 个 concept
- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 12 行（Batch 65 注释）
  - `terms/registry/aliases.tsv`：追加 ~40 行（含 preferred en/zh + 常用变体）
  - `terms/registry/evidence.tsv`：追加 12 行

**新建 concept 清单**：

| concept_id | category | preferred_zh | preferred_en | preferred_abbr | notes |
|---|---|---|---|---|---|
| lithium-ceramic | material | 锂陶瓷 | lithium ceramic | | 包层增殖材料基础概念 |
| ceramic-pebble-bed | material | 陶瓷球床 | ceramic pebble bed | | 球床结构概念 |
| lithium-ceramic-pebble-bed | material | 锂陶瓷球床 | lithium ceramic pebble bed | | 贪心匹配断裂根因 |
| in-vessel | concept | 堆内 | in-vessel | | 泛化概念（非仅 in-vessel LOCA）|
| ex-vessel | concept | 堆外 | ex-vessel | | 泛化概念（非仅 ex-vessel LOCA）|
| reduced-activation | concept | 低活化 | reduced activation | | 泛化概念（超出 RAFM 钢范畴）|
| beryllium-pebble-bed | material | 铍球床 | beryllium pebble bed | | 中子倍增球床 |
| beryllium-neutron-multiplier | material | 铍中子倍增剂 | beryllium neutron multiplier | | 包层倍增材料 |
| tungsten-armor | material | 钨铠甲 | tungsten armor | | PFC 面向等离子体保护层 |
| helium-coolant | concept | 氦冷却剂 | helium coolant | | 包层冷却工质 |
| pressurized-water | concept | 加压水 | pressurized water | | 冷却剂类型 |
| safety-analysis-report | doc | 安全分析报告 | safety analysis report | SAR | 通用 SAR 概念（PSR/FSAR 为子类）|

**Alias 详表**（每 concept 至少 preferred en + preferred zh）：

| alias | concept_id | lang | kind | comment |
|---|---|---|---|---|
| lithium ceramic | lithium-ceramic | en | preferred | |
| 锂陶瓷 | lithium-ceramic | zh | preferred | |
| ceramic pebble bed | ceramic-pebble-bed | en | preferred | |
| 陶瓷球床 | ceramic-pebble-bed | zh | preferred | |
| lithium ceramic pebble bed | lithium-ceramic-pebble-bed | en | preferred | |
| 锂陶瓷球床 | lithium-ceramic-pebble-bed | zh | preferred | |
| in-vessel | in-vessel | en | preferred | |
| 堆内 | in-vessel | zh | preferred | |
| ex-vessel | ex-vessel | en | preferred | |
| 堆外 | ex-vessel | zh | preferred | |
| reduced activation | reduced-activation | en | preferred | |
| 低活化 | reduced-activation | zh | preferred | |
| beryllium pebble bed | beryllium-pebble-bed | en | preferred | |
| 铍球床 | beryllium-pebble-bed | zh | preferred | |
| beryllium neutron multiplier | beryllium-neutron-multiplier | en | preferred | |
| 铍中子倍增剂 | beryllium-neutron-multiplier | zh | preferred | |
| tungsten armor | tungsten-armor | en | preferred | |
| 钨铠甲 | tungsten-armor | zh | preferred | |
| tungsten armour | tungsten-armor | en | alias | British spelling |
| helium coolant | helium-coolant | en | preferred | |
| 氦冷却剂 | helium-coolant | zh | preferred | |
| He coolant | helium-coolant | en | alias | short form |
| pressurized water | pressurized-water | en | preferred | |
| 加压水 | pressurized-water | zh | preferred | |
| safety analysis report | safety-analysis-report | en | preferred | |
| 安全分析报告 | safety-analysis-report | zh | preferred | |
| SAR | safety-analysis-report | abbr | preferred | |

- **修改边界**：不得修改 concepts.tsv / aliases.tsv / evidence.tsv 的已有行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0
- **验收标准**：
  - ✅ `grep "lithium ceramic pebble bed" artifacts/translation_dict.json` 后续导出时命中
  - ✅ `grep "^锂陶瓷球床	" terms/registry/aliases.tsv` 返回 1 行
  - ✅ `grep "^堆内	" terms/registry/aliases.tsv` 返回 1 行
  - ✅ validate_registry 通过
- **潜在风险**：`SAR` alias 可能与其他缩写冲突——需预检 `grep "^SAR\t" terms/registry/aliases.tsv`

#### ✅ Task 1.2: 同步 allowlist 并提交

- **目标**：将 Phase 1 新增术语同步到 allowlist，提交 git
- **修改内容**：
  - `terms/allowlist_en.txt`：追加新增英文单 token（如 `ceramic`, `armor`, `armour`——仅追加尚不存在的）
  - `terms/allowlist_zh.txt`：追加新增中文术语（锂陶瓷、陶瓷球床、锂陶瓷球床、堆内、堆外、低活化、铍球床、铍中子倍增剂、钨铠甲、氦冷却剂、加压水、安全分析报告）
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过
- **潜在风险**：allowlist 遗漏新增单 token 导致 build_terms 缺失——验收时对比词条数

### Phase 2: P0 — 修复已有 concept 的 alias 缺失

> **依赖**：Phase 1 完成后执行（避免 alias 冲突检查遗漏新增 concept）

#### ✅ Task 2.1: 添加/修改 alias 行 + 修复 nb3sn 缺失 preferred_zh

- **目标**：修复已有 concept 上的 alias 缺失和 deprecated 状态问题；修复 `nb3sn` concepts.tsv 中 preferred_zh 为空导致 en2zh 缺失
- **修改内容**：
  - `terms/registry/concepts.tsv`：
    - **修改 1 行**：`nb3sn` 行的 preferred_zh 字段从空改为 `铌三锡`
  - `terms/registry/aliases.tsv`：
    - **新增 alias 行**（追加到末尾）：

      | alias | concept_id | lang | kind | comment |
      |---|---|---|---|---|
      | plasma disruption | disruption | en | alias | 常用搜索形式 |
      | plasma facing component | plasma-facing-component | en | alias | 无连字符用户查询形式 |
      | loss of coolant | loss-of-coolant-accident | en | alias | 短形式 |
      | loss of coolant accident | loss-of-coolant-accident | en | alias | 完全无连字符形式 |
      | 失冷 | loss-of-coolant-accident | zh | alias | 口语短形式 |
      | 中心螺线管 | central-solenoid | zh | alias | 用户常用变体（preferred 保持 中心螺管）|
      | 中子壁负载 | neutron-wall-loading | zh | alias | 用户常用变体（preferred 保持 中子壁负荷）|
      | contact dose | contact-dose-rate | en | alias | 无"rate"的短形式 |

    - **修改已有行**（3 处 kind 变更）：

      | 行号 | 原内容 | 修改后 | 理由 |
      |---|---|---|---|
      | ~3604 | `增殖包层\tbreeding-blanket\tzh\tdeprecated\t非标准：应为 产氚包层` | `增殖包层\tbreeding-blanket\tzh\talias\t用户高频查询形式（升级自deprecated）` | 用户查询需覆盖 |
      | ~3438 | `环向场线圈\ttoroidal-field-coil\tzh\tdeprecated\t非标准：聚变惯用 纵场线圈` | `环向场线圈\ttoroidal-field-coil\tzh\talias\t用户高频查询形式（升级自deprecated）` | 用户查询需覆盖 |
      | (接触剂量行) | `接触剂量\tcontact-dose-rate\tzh\tdeprecated\t缺字'率'：应为 接触剂量率` | `接触剂量\tcontact-dose-rate\tzh\talias\t用户高频查询短形式（升级自deprecated）` | 用户查询需覆盖 |

- **修改边界**：
  - concepts.tsv 仅修改 `nb3sn` 行的 preferred_zh 字段
  - 不得修改 evidence.tsv
  - aliases.tsv 仅修改上述 3 行（deprecated→alias）+ 追加 8 行
  - **注意**：修改 deprecated → alias 后需确认对应 alias 不在 denylist 中（bridge check）
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0
  - 预检：`grep "^增殖包层\t" terms/registry/aliases.tsv` 确认 kind 为 alias
- **验收标准**：
  - ✅ `grep "^plasma disruption\t" terms/registry/aliases.tsv` 返回 1 行
  - ✅ `grep "^plasma facing component\t" terms/registry/aliases.tsv` 返回 1 行
  - ✅ `grep "^增殖包层\t" terms/registry/aliases.tsv` 显示 kind=alias（非 deprecated）
  - ✅ `grep "^环向场线圈\t" terms/registry/aliases.tsv` 显示 kind=alias
  - ✅ `grep "^接触剂量\t" terms/registry/aliases.tsv` 显示 kind=alias
  - ✅ `grep "^失冷\t" terms/registry/aliases.tsv` 返回 1 行
  - ✅ `awk -F'\t' '$1=="nb3sn"{print $3}' terms/registry/concepts.tsv` 输出 `铌三锡`（非空）
  - ✅ validate_registry 通过（含 bridge check）
- **潜在风险**：
  - "增殖包层" 和 "环向场线圈" 之前被 deprecated 可能有特定原因，升级后可能引起术语规范化争议——但用户明确要求覆盖这些查询，且 preferred_zh 保持不变
  - "接触剂量" 升级后，用户使用"接触剂量"查询会命中 `contact-dose-rate` → 翻译为"contact dose rate"——准确但可能比"contact dose"更正式
  - `nb3sn` preferred_zh 修改为"铌三锡"——需确认此行 tab 字段对齐不被破坏

#### Task 2.2: 同步 allowlist 并提交

- **目标**：将 Phase 2 新增/修改的 alias 同步到 allowlist
- **修改内容**：
  - `terms/allowlist_zh.txt`：追加 失冷、中心螺线管、中子壁负载、增殖包层、环向场线圈、接触剂量（如尚不存在）
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过
- **潜在风险**：deprecated→alias 升级后的术语如未添加到 allowlist_zh 则 bridge check 仍通过但 IME 词表缺失

### Phase 3: P1 — 补充覆盖率 concept

> **依赖**：Phase 2 完成后执行

#### Task 3.1: 添加 5 个 P1 concept 到三表

- **目标**：补充提升专业检索覆盖率的二级缺失 concept
- **修改内容**：
  - `terms/registry/concepts.tsv`：追加 5 行（Batch 66 注释）
  - `terms/registry/aliases.tsv`：追加 ~18 行
  - `terms/registry/evidence.tsv`：追加 5 行

**新建 concept 清单**：

| concept_id | category | preferred_zh | preferred_en | preferred_abbr | notes |
|---|---|---|---|---|---|
| wcpb | concept | 水冷球床包层 | water-cooled pebble bed | WCPB | 水冷球床包层型号 |
| beryllium-pebble | material | 铍球 | beryllium pebble | | 铍增殖剂颗粒 |
| lithium-metatitanate | material | 偏钛酸锂 | lithium metatitanate | | Li₂TiO₃ 陶瓷增殖剂 |
| lithium-metazirconate | material | 偏锆酸锂 | lithium metazirconate | | Li₂ZrO₃ 陶瓷增殖剂 |
| primary-heat-transfer | concept | 一回路传热 | primary heat transfer | | 一回路热工 |

**Alias 详表**：

| alias | concept_id | lang | kind | comment |
|---|---|---|---|---|
| water-cooled pebble bed | wcpb | en | preferred | |
| 水冷球床包层 | wcpb | zh | preferred | |
| WCPB | wcpb | abbr | preferred | |
| water cooled pebble bed | wcpb | en | alias | 无连字符形式 |
| beryllium pebble | beryllium-pebble | en | preferred | |
| 铍球 | beryllium-pebble | zh | preferred | |
| lithium metatitanate | lithium-metatitanate | en | preferred | |
| 偏钛酸锂 | lithium-metatitanate | zh | preferred | |
| Li2TiO3 | lithium-metatitanate | en | alias | 化学式 |
| lithium metazirconate | lithium-metazirconate | en | preferred | |
| 偏锆酸锂 | lithium-metazirconate | zh | preferred | |
| Li2ZrO3 | lithium-metazirconate | en | alias | 化学式 |
| primary heat transfer | primary-heat-transfer | en | preferred | |
| 一回路传热 | primary-heat-transfer | zh | preferred | |
| primary heat transport | primary-heat-transfer | en | alias | 变体 |

- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：
  - ✅ `grep "^WCPB\t" terms/registry/aliases.tsv` 返回 1 行
  - ✅ `grep "^偏钛酸锂\t" terms/registry/aliases.tsv` 返回 1 行
  - ✅ validate_registry 通过
- **潜在风险**：`Li2TiO3` / `Li2ZrO3` 中的下标写法不一致——统一用纯 ASCII（Li2TiO3）而非 Unicode 下标

#### Task 3.2: 同步 allowlist 并提交

- **目标**：将 Phase 3 新增术语同步到 allowlist
- **修改内容**：allowlist_en.txt、allowlist_zh.txt 追加
- **修改边界**：不得修改已有行
- **测试要求**：validate_registry 通过
- **验收标准**：✅ validate_registry 通过
- **潜在风险**：P1 优先级较低，如时间不足可跳过此 Phase 而不影响 P0 修复

### Phase 4: 结构性改进 — 高优先级无连字符 alias 变体

> **依赖**：Phase 1-3 完成后执行（脚本需扫全量 alias 避免冲突）

#### Task 4.1: 批量添加高优先级无连字符 EN alias

- **目标**：为最常被用户搜索的含连字符 EN alias 添加无连字符版本，避免贪心匹配断裂
- **修改内容**：
  - `terms/registry/aliases.tsv`：追加 ~50 行（Batch 67 注释）
  - 通过脚本实现：
    1. 从 aliases.tsv 提取所有 `lang=en, kind∈{preferred,alias}` 且包含内部连字符的 alias
    2. 过滤排除：化学式/专有名（`X-ray`, `Nb3Sn`, `7-X`, `Grad-Shafranov`, `Rayleigh-Taylor` 等）；替换后与已有 alias 重复的；替换后 alias 文本不变的
    3. 按优先级选取前 ~50 条：优先选择 kind=preferred 的、concept category 为 material/concept/system 的
    4. 为每个生成 alias 行：`{space_version}\t{concept_id}\ten\talias\t无连字符查询形式`

**预期高优先级目标示例**（最终列表由脚本实际执行决定）：

| 原连字符 alias | 无连字符 alias | concept_id |
|---|---|---|
| high-temperature superconductor | high temperature superconductor | hts |
| low-temperature superconductor | low temperature superconductor | lts |
| cable-in-conduit conductor | cable in conduit conductor | cicc |
| reduced-activation ferritic/martensitic steel | reduced activation ferritic/martensitic steel | rafm-steel |
| as-low-as-reasonably-achievable | as low as reasonably achievable | alara |
| preliminary-safety-analysis-report | preliminary safety analysis report | preliminary-safety-analysis-report |
| final-safety-analysis-report | final safety analysis report | final-safety-analysis-report |
| ... | ... | ... |

> 注意：Phase 2 已添加的 "plasma facing component"、"loss of coolant accident" 不重复添加

- **修改边界**：
  - 仅追加新行到 aliases.tsv
  - 不修改 concepts.tsv、evidence.tsv
  - 不修改已有 alias 行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry --terms-dir terms`
  - 预期输出：exit code 0，无 alias 冲突
- **验收标准**：
  - ✅ validate_registry 通过
  - ✅ 新增 alias 数量 ≥ 40
  - ✅ `grep "plasma facing component" terms/registry/aliases.tsv` 命中无连字符版
  - ✅ `grep "high temperature superconductor" terms/registry/aliases.tsv` 命中无连字符版
- **潜在风险**：
  - 连字符属于专有名称的误替换（如 `Wendelstein 7-X` → `Wendelstein 7 X`）——脚本需维护排除名单
  - 大量新 alias 可能引入与后续 Phase 意外冲突——先 validate 再提交

### Phase 5: 验证与导出

> **依赖**：Phase 1-4 全部完成

#### Task 5.1: 全量验证 + 导出 + 测试

- **目标**：确保所有修改通过完整验证，重新生成 translation_dict
- **修改内容**：无源文件修改
- **修改边界**：不修改 pipeline/、terms/、tests/ 中的任何文件
- **测试要求**：
  - `python3 -m pipeline.validate_registry --terms-dir terms` → exit 0
  - `python3 -m pipeline.export_registry` → exit 0
  - `python3 -m pipeline.build_terms --config config.toml` → exit 0
  - `python3 -m pytest tests/ -x` → 全部通过
- **验收标准**：
  - ✅ 全部命令 exit 0
  - ✅ `translation_dict.json` 中 `en2zh` 包含 `lithium ceramic pebble bed` → `锂陶瓷球床`
  - ✅ `translation_dict.json` 中 `zh2en` 包含 `增殖包层` → `breeding blanket`
  - ✅ `translation_dict.json` 中 `zh2en` 包含 `钨铠甲` → `tungsten armor`
  - ✅ `translation_dict.json` 中 `en2zh` 包含 `plasma facing component` → `面向等离子体部件`
  - ✅ `translation_dict.json` 中 `en2zh` 包含 `safety analysis report` → `安全分析报告`
  - ✅ `domain_terms.txt` 词条数 ≥ 2860（上次 2854）
  - ✅ pytest 全部通过
- **潜在风险**：snapshot/regression 测试可能 hardcode 了之前的计数——如出现需检查是 snapshot 还是逻辑错误

## 时序推演（Temporal Interrogation）

| 阶段 | 时间点 | 关键决策/潜在阻塞 |
|------|--------|--------------------|
| 初期（Phase 1-2）| P0 概念建立 + alias 修复 | SAR 缩写是否冲突？nb3sn preferred_zh 修改是否引起回归？deprecated→alias 升级后 bridge check 是否通过？ |
| 中期（Phase 3-4）| P1 补充 + 无连字符变体 | 脚本生成的 ~50 个无连字符 alias 中是否有与 Phase 1-3 新增 alias 冲突的？排除名单是否完整（化学式、专有名）? |
| 后期（Phase 5）| 全量验证 | translation_dict 中 en2zh/zh2en 是否包含所有用户报告的 P0 缺失项？pytest 是否有 snapshot 测试被新增数据打破？ |

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry --terms-dir terms` exit code 0
- [ ] `python3 -m pipeline.export_registry` exit code 0
- [ ] `python3 -m pipeline.build_terms --config config.toml` exit code 0
- [ ] `python3 -m pytest tests/ -x` 全部通过
- [ ] `artifacts/translation_dict.json` 中 `en2zh` 包含用户报告的 P0 缺失词条
- [ ] `artifacts/translation_dict.json` 中 `zh2en` 包含用户报告的 P0 缺失 zh→en 映射
- [ ] `terms/registry/aliases.tsv` 中无跨 concept alias 冲突
- [ ] 无 deprecated alias 出现在 allowlist 中（bridge check）
- [ ] awk 检查 concepts.tsv 无重复 concept_id

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
| 背景与目标 | 完整：问题描述、根因分析、目标（4项）、非目标（4项+理由）、复用分析（4项） |
| 技术方案 | 完整：方案概述、5 项设计决策、影响范围（7 个文件） |
| Error & Rescue Map | 5 条路径已覆盖，0 CRITICAL GAP |
| 时序推演 | 3 阶段关键决策/阻塞点已标注 |
| 执行计划 | 5 Phases、9 Tasks（12+5 新 concept、~11 alias 修复、~50 无连字符变体）|
| 回归检查清单 | 9 项检查（含 en2zh/zh2en 特定验证） |
| 已知局限 | 无 |

### R1 Issues
- **Issue R1-1**: Tasks 1.2, 2.2, 3.2 缺少潜在风险字段 → 已为每个 Task 补充 ✅ 已修正
- **Issue R1-2**: Task 5.1 缺少修改边界字段 → 已补充 "不修改 pipeline/、terms/、tests/" ✅ 已修正

### R2 Issues
- **Issue R2-1**: Phase 间缺少依赖关系标注 → 已在每个 Phase 标题下添加 `> 依赖：...` ✅ 已修正
- **Issue R2-2**: 缺少时序推演 → 已添加 Temporal Interrogation 表格（初期/中期/后期） ✅ 已修正

### R3 Issues
- **Issue R3-1**: `nb3sn` concepts.tsv 中 preferred_zh 为空导致 en2zh 缺失 "Nb3Sn→铌三锡" → 已将 nb3sn preferred_zh 修复纳入 Task 2.1，并添加验收标准和潜在风险 ✅ 已修正
