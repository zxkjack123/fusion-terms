# AI 错误翻译反模式扩展 — 执行计划

## 背景与目标

- **问题/需求描述**：当前 registry 中许多已有概念虽然有正确的 preferred_zh，但缺少 forbidden/deprecated 中文反模式别名。AI 翻译工具（GPT、DeepSeek、豆包等）在翻译聚变术语时有系统性错误模式——这些错误翻译若不录入 registry，就无法通过下游 vale/substitution 管道自动检测和纠正（即识别"AI味"）。同时有少量概念本身尚未收录。
- **根因分析**：前期 registry 建设重点在概念收录和 preferred 别名，forbidden/deprecated 反模式的系统性补充工作尚未完成。尤其以下领域缺口最大：MHD 不稳定性、破裂阶段、等离子体运行阶段、中子-材料-辐照、氚工艺。
- **目标**：
  1. 为 ~20 个已有概念批量补充 ~43 条 forbidden/deprecated 中文别名
  2. 新增 4 个缺失概念（含其 preferred + alias + forbidden 别名 + evidence）
  3. 全量验证通过
- **非目标（不做什么）**：
  - 不修改任何已有 preferred_zh — 不做
  - 不调整已有 forbidden/deprecated 别名的措辞 — 不做
  - 不修改 pipeline 代码或测试 — 不做
  - 不修改 allowlist/denylist — 除非 validator 报错要求同步
- **已有代码/流程复用分析**：
  - TSV 追加模式：复用（aliases.tsv 按 concept_id 分段追加）
  - validate_registry + pytest 验收链：复用
  - git commit per-task 模式：复用（每个 Phase 结束后 commit）

## 技术方案

- **方案概述**：纯数据追加操作——向 aliases.tsv 追加 forbidden/deprecated 行，向 concepts.tsv / evidence.tsv 追加新概念行。不涉及代码修改。
- **关键设计决策**：
  1. 别名冲突预检已完成（上轮对话），所有拟新增别名均已确认不与现有别名冲突
  2. 新概念 ID 命名遵循 kebab-case 惯例
  3. 每个 Phase 合并为一次 commit（减少 commit 数量，提高效率）
- **影响范围**：
  - `terms/registry/aliases.tsv`：追加 ~55 行
  - `terms/registry/concepts.tsv`：追加 4 行
  - `terms/registry/evidence.tsv`：追加 4 行
  - `terms/allowlist_zh.txt`：可能需要补新概念的 preferred_zh（如 validator 要求）

## Error & Rescue Map（关键失败路径映射）

| 代码路径/操作 | 可能的失败 | 错误类型 | 已处理？ | 处理方式 | 用户可见行为 |
|---|---|---|---|---|---|
| aliases.tsv 追加 | 别名字符串已被其他 concept_id 占用 | validator: alias maps to multiple concepts | Y | 上轮预检已排除冲突；Task 执行时再次 validate | validator 报错，commit 阻断 |
| concepts.tsv 追加 | concept_id 重复 | validator: duplicate concept_id | Y | 上轮预检已排除；每 Phase 后 validate | validator 报错 |
| allowlist_zh.txt | 新 preferred_zh 不在 allowlist 中 | validator: preferred not in allowlist | Y | 各 Task 验收时检查，按需补 allowlist | validator 报错 |
| deprecated term 出现在 allowlist | validator: deprecated in allowlist | Y | 本次只新增 forbidden/deprecated，不改 preferred；但如果某个 forbidden 刚好在 allowlist 中，validator 会报错 | 需检查并从 allowlist 删除 |
| pre-commit hook 拒绝 | trailing whitespace / pytest fail | Y | TSV 手动构造时注意尾部空格；每 Phase 后 pytest | commit 失败 |

## 执行计划

### Phase 1: MHD 不稳定性 — forbidden/deprecated 补充

#### ✅ Task 1.1: kink-mode / ballooning-mode / interchange / fishbone / peeling-ballooning 反模式
- **目标**：为 5 个 MHD 不稳定性概念补充 forbidden/deprecated 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加以下行（按 concept_id 分组插入对应段落末尾）

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 弯折模 | kink-mode | zh | forbidden | 误译kink(扭曲≠弯折)：正确为 扭曲模 |
    | 纽结模 | kink-mode | zh | forbidden | 误译kink(扭曲≠纽结)：正确为 扭曲模 |
    | 鼓包模 | ballooning-mode | zh | forbidden | 误译ballooning：正确为 气球模 |
    | 置换不稳定性 | interchange-instability | zh | forbidden | 误译interchange(化学义)：正确为 交换不稳定性 |
    | 鱼骨形不稳定性 | fishbone-instability | zh | deprecated | 啰嗦变体：应为 鱼骨模不稳定性 |
    | 剥落-气球模 | peeling-ballooning-mode | zh | forbidden | 误译peeling(剥离≠剥落)：正确为 剥离-气球模 |
    | 去皮-气球模 | peeling-ballooning-mode | zh | forbidden | 误译peeling(剥离≠去皮)：正确为 剥离-气球模 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`、`pipeline/` 目录下任何文件
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期输出：仅有已知的 6 个 pre-existing IME allowlist 错误（Abaqus/B2/CENDL/CFX/CuCrZr/RAMI），无新增错误
  - 运行 `python3 -c "..." ` 检查无 alias→多concept_id 冲突
- **验收标准**：
  - ✅ 7 条新 alias 行成功追加
  - ✅ validate_registry 无新增报错
  - ✅ 无多 concept_id 映射冲突
- **潜在风险**：`去皮-气球模` 等含连字符的别名需确保格式正确（TSV 中连字符是合法内容字符）

### Phase 2: 破裂阶段 — thermal-quench / current-quench 反模式

#### ✅ Task 2.1: thermal-quench / current-quench forbidden 别名
- **目标**：为 2 个破裂阶段概念补充 6 条 forbidden 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 热淬灭 | thermal-quench | zh | forbidden | 误用金属义淬：正确为 热猝灭 |
    | 热骤冷 | thermal-quench | zh | forbidden | 误译quench：正确为 热猝灭 |
    | 热淬火 | thermal-quench | zh | forbidden | 金属热处理义：正确为 热猝灭 |
    | 热量猝灭 | thermal-quench | zh | forbidden | AI冗余加词：正确为 热猝灭 |
    | 电流淬灭 | current-quench | zh | forbidden | 误用金属义淬：正确为 电流猝灭 |
    | 电流骤降 | current-quench | zh | forbidden | 误译quench(猝灭≠骤降)：正确为 电流猝灭 |
    | 电流淬火 | current-quench | zh | forbidden | 金属热处理义：正确为 电流猝灭 |
    | 电流急停 | current-quench | zh | forbidden | 误译quench(猝灭≠急停)：正确为 电流猝灭 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误
- **验收标准**：
  - ✅ 8 条新 forbidden 行成功追加
  - ✅ validate_registry 无新增报错
- **潜在风险**：无——均为现有概念的纯追加操作

### Phase 3: 等离子体运行 — flat-top / safety-factor / tau-e 反模式

#### Task 3.1: flat-top / safety-factor / tau-e forbidden 别名
- **目标**：为 3 个等离子体运行/约束概念补充 forbidden 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 稳态段 | flat-top | zh | forbidden | 误译flat-top(平顶段≠稳态段)：正确为 平顶段 |
    | 平台期 | flat-top | zh | forbidden | 误译flat-top(医学/经济义)：正确为 平顶段 |
    | 安全参数 | safety-factor | zh | forbidden | 误译factor(因子≠参数)：正确为 安全因子 |
    | 限制时间 | tau-e | zh | forbidden | 误译confinement(约束≠限制)：正确为 能量约束时间 |
    | 封闭时间 | tau-e | zh | forbidden | 误译confinement(约束≠封闭)：正确为 能量约束时间 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误
  - 运行 `python3 -c "..."` 检查 `坪区` 已映射到 `plateau-regime`、新 `稳态段` 映射到 `flat-top`，无冲突
- **验收标准**：
  - ✅ 5 条新 forbidden 行成功追加
  - ✅ `稳态段`→`flat-top` 不与其他概念冲突
  - ✅ validate_registry 无新增报错
- **潜在风险**：`稳态段` 可能在某些语境下有合理用法，但在 flat-top 上下文中属误译，标记为 forbidden 合理

### Phase 4: 中子学与辐照材料 — 反模式补充

#### Task 4.1: reduced-activation / decay-heat / dpa / transmutation / void-swelling / irradiation-embrittlement / blistering forbidden 别名
- **目标**：为 7 个中子-材料-辐照概念补充 forbidden/deprecated 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 降低活化 | reduced-activation | zh | forbidden | 非标准直译：正确为 低活化 |
    | 减活化 | reduced-activation | zh | forbidden | 非标准译法：正确为 低活化 |
    | 降活 | reduced-activation | zh | forbidden | 非标准缩略：正确为 低活化 |
    | 衰变余热 | decay-heat | zh | deprecated | 非标准混合：应为 衰变热 或 余热 |
    | 每原子位移 | dpa | zh | forbidden | 直译acronym：正确为 离位损伤(dpa) |
    | 核转变 | transmutation | zh | forbidden | 非标准：正确为 嬗变 |
    | 核变换 | transmutation | zh | forbidden | 误译transmutation：正确为 嬗变 |
    | 空隙肿胀 | void-swelling | zh | forbidden | 误译void(空洞≠空隙)：正确为 辐照肿胀 |
    | 辐照脆性 | irradiation-embrittlement | zh | forbidden | 误译embrittlement(脆化≠脆性)：正确为 辐照脆化 |
    | 气泡化 | blistering | zh | forbidden | 误译blistering：正确为 起泡 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`；不得修改 `terms/allowlist_zh.txt` 除非 validator 要求
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误
- **验收标准**：
  - ✅ 10 条新行成功追加
  - ✅ validate_registry 无新增报错
- **潜在风险**：`核嬗变` 已作为 alias 存在（非 forbidden）；本次新增 `核转变` `核变换` 是不同字符串，无冲突

### Phase 5: 氚工艺/燃料循环 — 反模式补充

#### Task 5.1: permeation / tritium-inventory / water-detritiation-system / tritium-permeation-barrier 反模式
- **目标**：为 4 个氚工艺概念补充 forbidden/deprecated 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 穿透 | permeation | zh | forbidden | 误译permeation(渗透≠穿透)：正确为 渗透 |
    | 氚清单 | tritium-inventory | zh | forbidden | inventory(清单义)误用：正确为 氚存量 |
    | 水脱氚系统 | water-detritiation-system | zh | deprecated | 非标准变体：应为 水除氚系统 |
    | 水去氚化系统 | water-detritiation-system | zh | forbidden | 非标准：正确为 水除氚系统 |
    | 氚阻挡涂层 | tritium-permeation-barrier | zh | deprecated | 不精确(涂层⊂阻挡层)：应为 氚渗透阻挡层 |
    | 氚阻隔层 | tritium-permeation-barrier | zh | forbidden | 非标准：正确为 氚渗透阻挡层 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误
- **验收标准**：
  - ✅ 6 条新行成功追加
  - ✅ validate_registry 无新增报错
- **潜在风险**：`穿透` 一词在 `deep-penetration`（深穿透）语境中另有含义；但作为 `permeation` 的误译标记为 forbidden，不冲突（forbidden alias 映射到具体 concept_id `permeation`）

### Phase 6: 工程系统 — 屏蔽/剂量率反模式 + PSI 反模式

#### Task 6.1: neutron-shielding / biological-shielding / contact-dose-rate / plasma-surface-interaction 反模式
- **目标**：为 4 个工程/PWI 概念补充 forbidden/deprecated 中文别名
- **修改内容**：
  - 文件 `terms/registry/aliases.tsv`：追加

    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | 中子防护 | neutron-shielding | zh | forbidden | 误译shielding(屏蔽≠防护)：正确为 中子屏蔽 |
    | 中子遮挡 | neutron-shielding | zh | forbidden | 误译shielding(屏蔽≠遮挡)：正确为 中子屏蔽 |
    | 生物防护 | biological-shielding | zh | forbidden | 误译shielding(屏蔽≠防护)：正确为 生物屏蔽体 |
    | 表面剂量率 | contact-dose-rate | zh | deprecated | 非标准：应为 接触剂量率 |
    | 等离子体壁面交互 | plasma-surface-interaction | zh | forbidden | 误译interaction(相互作用≠交互)：正确为 等离子体表面相互作用 |
    | 等离子壁互动 | plasma-surface-interaction | zh | forbidden | 误译interaction+缺'体'字：正确为 等离子体表面相互作用 |
    | 血浆壁相互作用 | plasma-surface-interaction | zh | forbidden | AI误译plasma(等离子体≠血浆)：正确为 等离子体表面相互作用 |

- **修改边界**：不得修改 `terms/registry/concepts.tsv`、`terms/registry/evidence.tsv`
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误
- **验收标准**：
  - ✅ 7 条新行成功追加
  - ✅ validate_registry 无新增报错
- **潜在风险**：`血浆壁相互作用` 是 AI 将 plasma 翻译为"血浆"的典型错误，在生物学语境合法但聚变语境下为 forbidden

### Phase 7: 新增概念 — re-erosion / afterheat / neutron-streaming / ductile-brittle-transition-temperature

#### Task 7.1: 新增 4 个缺失概念（concepts + aliases + evidence）
- **目标**：新增 4 个目前 registry 中不存在的概念，并配套 preferred/alias/forbidden 别名和 evidence
- **修改内容**：
  - 文件 `terms/registry/concepts.tsv`：在末尾追加 section header + 4 行

    | concept_id | type | preferred_zh | preferred_en | preferred_abbr | status | notes |
    |---|---|---|---|---|---|---|
    | re-erosion | concept | 再侵蚀 | re-erosion | | active | Erosion of redeposited material |
    | afterheat | metric | 余热 | afterheat | | active | Residual heat from radioactive decay after reactor shutdown (synonym of decay heat in reactor context) |
    | neutron-streaming | effect | 中子流穿 | neutron streaming | | active | Preferential neutron transport through gaps/ducts in shielding |
    | ductile-brittle-transition-temperature | metric | 韧脆转变温度 | ductile-to-brittle transition temperature | DBTT | active | Temperature below which material fracture becomes brittle |

  - 文件 `terms/registry/aliases.tsv`：追加 preferred + alias + forbidden 别名

    **re-erosion:**
    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | re-erosion | re-erosion | en | preferred | |
    | 再侵蚀 | re-erosion | zh | preferred | |
    | re erosion | re-erosion | en | alias | space variant |
    | 重新侵蚀 | re-erosion | zh | forbidden | 误译re-(再≠重新)：正确为 再侵蚀 |
    | 反复侵蚀 | re-erosion | zh | forbidden | 误译re-(再≠反复)：正确为 再侵蚀 |

    **afterheat:**
    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | afterheat | afterheat | en | preferred | |
    | 余热 | afterheat | zh | preferred | |
    | after-heat | afterheat | en | alias | hyphenated variant |
    | residual heat | afterheat | en | alias | synonym |
    | 残余热 | afterheat | zh | forbidden | 非标准：正确为 余热 |
    | 事后热 | afterheat | zh | forbidden | 误译after(余≠事后)：正确为 余热 |
    | 后续热 | afterheat | zh | forbidden | 误译after：正确为 余热 |

    **neutron-streaming:**
    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | neutron streaming | neutron-streaming | en | preferred | |
    | 中子流穿 | neutron-streaming | zh | preferred | |
    | neutron-streaming | neutron-streaming | en | alias | hyphenated form |
    | 中子漏流 | neutron-streaming | zh | forbidden | 误译streaming(流穿≠漏流)：正确为 中子流穿 |

    **ductile-brittle-transition-temperature:**
    | alias | concept_id | lang | kind | comment |
    |---|---|---|---|---|
    | ductile-to-brittle transition temperature | ductile-brittle-transition-temperature | en | preferred | |
    | 韧脆转变温度 | ductile-brittle-transition-temperature | zh | preferred | |
    | DBTT | ductile-brittle-transition-temperature | abbr | preferred | |
    | ductile-brittle transition temperature | ductile-brittle-transition-temperature | en | alias | |
    | 延脆转变 | ductile-brittle-transition-temperature | zh | forbidden | 误译ductile(韧≠延)：正确为 韧脆转变温度 |
    | 塑脆转变 | ductile-brittle-transition-temperature | zh | forbidden | 误译ductile(韧≠塑)：正确为 韧脆转变温度 |
    | 韧性-脆性转变温度 | ductile-brittle-transition-temperature | zh | deprecated | 啰嗦：应为 韧脆转变温度 |

  - 文件 `terms/registry/evidence.tsv`：追加 4 行

    | concept_id | source | quote | added_by | added_at |
    |---|---|---|---|---|
    | re-erosion | internal:registry-gap-review:pwi-antipattern | Erosion of previously redeposited layers | copilot | 2026-04-13 |
    | afterheat | internal:registry-gap-review:neutronics-antipattern | Residual heat from activation products after shutdown | copilot | 2026-04-13 |
    | neutron-streaming | internal:registry-gap-review:neutronics-antipattern | Preferential neutron paths through shielding penetrations | copilot | 2026-04-13 |
    | ductile-brittle-transition-temperature | internal:registry-gap-review:materials-antipattern | Temperature marking onset of brittle fracture behavior | copilot | 2026-04-13 |

- **修改边界**：不得修改 `pipeline/` 目录下任何文件；不得修改已有行
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：无新增错误（除 pre-existing 6 个）
  - 运行 `python3 -m pytest tests/ -q`
  - 预期：全部通过
  - 检查 `余热` alias 冲突处理：`余热` 已作为 `decay-heat` 的 alias 存在。**afterheat** 概念的 preferred_zh 设为 `余热` 会导致同一 alias 映射到两个 concept_id。**需要改用 `afterheat` 作为 `decay-heat` 的 en alias（已存在），不单独建 afterheat 概念——改为在 `decay-heat` 概念下追加 forbidden 别名。**
- **验收标准**：
  - ✅ 3 个新概念行 + 对应 aliases + evidence 成功追加（afterheat 改为 decay-heat 下补 forbidden）
  - ✅ validate_registry 无新增报错
  - ✅ pytest 全部通过
  - ✅ 无 alias→多 concept_id 冲突
  - ✅ `terms/allowlist_zh.txt` 已补入 3 个新 preferred_zh（再侵蚀、中子流穿、韧脆转变温度）
- **潜在风险**：`afterheat` 与 `decay-heat` 语义高度重叠，需要合并处理而非独立建概念；3 个新 preferred_zh 需同步加入 allowlist

> **⚠️ 设计修正**：经预检，`余热` 已作为 `decay-heat` 的 zh alias 存在。`afterheat` 也已作为 `decay-heat` 的 en alias 存在。因此 **不新建 afterheat 概念**，改为在 `decay-heat` 下追加 3 条 forbidden 别名（残余热、事后热、后续热）。最终新增概念为 3 个（re-erosion、neutron-streaming、ductile-brittle-transition-temperature）。

**修正后的 Task 7.1 内容：**

新增 3 个概念 + 在 `decay-heat` 下追加 3 条 forbidden：

  - `terms/registry/concepts.tsv`：追加 3 行（re-erosion、neutron-streaming、ductile-brittle-transition-temperature）
  - `terms/registry/aliases.tsv`：追加上述 3 个概念的 preferred/alias/forbidden + `decay-heat` 的 3 条 forbidden
  - `terms/registry/evidence.tsv`：追加 3 行

### Phase 8: 全量验证与回归测试

#### Task 8.1: 全量验证
- **目标**：运行完整验证管道确保所有修改一致性
- **修改内容**：
  - 无文件修改（纯验证）
- **修改边界**：N/A
- **测试要求**：
  - 运行 `python3 -m pipeline.validate_registry`
  - 预期：仅 pre-existing 6 个 IME allowlist 错误
  - 运行 `python3 -m pytest tests/ -q`
  - 预期：全部通过
  - 运行 `grep -c '^[^#]' terms/registry/concepts.tsv terms/registry/aliases.tsv terms/registry/evidence.tsv`
  - 预期 delta：concepts +3, aliases +55±2, evidence +3
  - 运行 Python 脚本检查无 multi-concept alias 映射
- **验收标准**：
  - ✅ validate_registry 无新增报错
  - ✅ pytest 100% 通过
  - ✅ 行数 delta 正确
  - ✅ 无 alias→多概念冲突
- **潜在风险**：export_registry 会因 pre-existing errors 失败——这是已知问题，不阻断本次交付

## 回归检查清单

- [ ] `python3 -m pipeline.validate_registry` — 无新增错误
- [ ] `python3 -m pytest tests/ -q` — 全部通过
- [ ] 无 alias string 映射到多个 concept_id（Python 脚本检查）
- [ ] concepts.tsv 行数 = 1476 (1473 + 3)
- [ ] aliases.tsv 行数增量 ≈ +55
- [ ] evidence.tsv 行数 = 1566 (1563 + 3)
- [ ] `terms/allowlist_zh.txt` 无 forbidden/deprecated 条目（如有新增 preferred_zh 需同步添加）

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 3 | 3 | 0 |
| R2 | 可执行性 | 2 | 2 | 0 |
| R3 | 风险与边缘 | 1 | 1 | 0 |
| **终止** | **T1 — 收敛终止** | | | **0** |

### Completion Summary

| 维度 | 结果 |
|------|------|
| 背景与目标 | 完整 |
| 技术方案 | 完整 |
| Error & Rescue Map | 5 条路径已覆盖，0 CRITICAL GAP |
| 执行计划 | 8 Phase, 8 Task |
| 回归检查清单 | 7 项检查 |
| 已知局限 | 无 |

### [R1 Issues — 结构完整性]
- **Issue R1-1**: afterheat 概念与 decay-heat 重叠（`余热` alias 冲突）→ 修正：取消 afterheat 独立概念，改为 decay-heat 下追加 forbidden ✅ 已修正
- **Issue R1-2**: 提案中多处 alias 已在上轮工作中录入（如 `扭结模`、`气球模式`、`膨胀模` 等）→ 修正：逐一排除已存在 alias，仅保留 NEW 条目 ✅ 已修正
- **Issue R1-3**: Error & Rescue Map 未覆盖 deprecated-in-allowlist 风险 → 修正：已补充第 4 行 ✅ 已修正

### [R2 Issues — 可执行性]
- **Issue R2-1**: Task 7.1 同时修改 3 个文件（concepts + aliases + evidence），超过 Phase 7 的"≤3 文件"限制仅属边界值——但 3 个文件是注册表固有的三元组，属合理例外 → 确认在限制内 ✅ 已确认
- **Issue R2-2**: Task 3.1 中 `稳态段` 可能与现有 `稳态运行` 概念混淆 → 预检确认 `稳态段` 不在 aliases.tsv 中，且映射到 `flat-top` 不冲突 ✅ 已确认

### [R3 Issues — 风险与边缘]
- **Issue R3-1**: `neutron-streaming` 概念与已有 `radiation-streaming` 高度重叠（`中子串流` 已是 `radiation-streaming` 的 alias）→ 修正：需将 `neutron-streaming` 的 forbidden 别名 `中子漏流` 挂在 `radiation-streaming` 下，但 `中子流穿` 作为独立概念有存在价值（特指中子而非广义辐射）。**保留新概念 `neutron-streaming`，但 preferred_zh 改为 `中子流穿`，并确保 `中子串流` 不重复映射。`中子串流` 已映射到 `radiation-streaming`，不再添加到 `neutron-streaming`。** ✅ 已修正
