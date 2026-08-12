---
plan_schema_version: "1.0"
linked_spec: null
scope_mode: "EXPANSION"
generated_at: "2026-08-12T00:00:00Z"
git_commit: "213d594"
files_sha256:
  terms/allowlist_zh.txt: "auto"
  terms/allowlist_en.txt: "auto"
  terms/synonyms.tsv: "auto"
  terms/denylist.txt: "auto"
---

# Plan: 聚变堆氚安全/包容术语批量入库（#2540 扩展）

## 背景与目标

- **问题/需求描述**：PM #2540 要求新增"三级包容/二级包容/3-Level Confinement"相关术语。
  用户调研后决定扩展范围，将聚变堆氚安全、包容、屏蔽相关的 **25 组**中英术语一并入库（含 #2540 原始 2 组，共 **27 组**中英术语）。
- **目标**：将 27 组术语写入 `terms/` 下的 4 个平面文本文件，验证通过后 git tag + push。
- **非目标（不做什么）**：
  - 不修改 `terms/registry/` 结构化数据（概念级定义另行评估）
  - 不修改 pipeline 代码
  - 不修改 stopwords

## 修改方案

- **修改路径分类**：Medium（27 组术语 × 4 文件 = 约 75 行新数据）
- **方案概述**：分两个子任务批量追加到 `allowlist_zh.txt`、`allowlist_en.txt`、`synonyms.tsv`、`denylist.txt`
- **关键设计决策**：
  - 采用末尾追加模式（与现有 batch 55-89 实践一致），带 `# --- Tritium safety / confinement (Batch 90) ---` 节注释
  - 使用 `confinement` 而非 `containment`（与 ITER 官方术语和现有数据库一致）
  - P0 词条包含 #2540 原始需求（三级包容/二级包容）+ 补全项
- **影响范围**：仅 `terms/` 目录下 4 个平面文本文件

---

## 执行计划

### Phase 1: 术语文件修改

#### Task 1.1: 写入 allowlist 文件（25 组 × 2 语言）

- **目标**：将 27 组中英术语分别追加到 `terms/allowlist_zh.txt` 和 `terms/allowlist_en.txt`
- **依赖**：无
- **frontier**：是
- **执行者**：Task Executor
- **修改内容**：

  文件 `terms/allowlist_zh.txt`（追加操作 — 文件当前末行为 `反磁通信号`，末尾已有 `\n`）：
  ```bash
  # Step 1: 写一个空行作为分隔
  echo '' >> terms/allowlist_zh.txt
  # Step 2: 追加下列内容（注意：每行一个字面术语，无前导/尾随空格）
  cat >> terms/allowlist_zh.txt << 'ENDOFTERMS'
  # --- Tritium safety / confinement (Batch 90) ---
  三级包容
  二级包容
  一级包容
  第一包容屏障
  最终包容屏障
  包容边界
  包容完整性
  分级包容
  静态包容
  动态包容
  负压包容
  包容监测
  氚事故释放
  氚环境排放
  氚源项评估
  氚剂量评估
  氚缓解
  渗透降低因子
  氚扩散阻挡层
  防氚涂层
  氚内照射剂量
  手套箱去氚
  氚废气处理
  含氚废水处理
  氚排放监测
  氚职业照射
  氚可接受剂量
  ENDOFTERMS
  ```

  文件 `terms/allowlist_en.txt`（追加操作 — 文件当前末行为 `Penning-vacuum-gauge`，末尾已有 `\n`）：
  ```bash
  # Step 1: 写空行分隔
  echo '' >> terms/allowlist_en.txt
  # Step 2: 追加下列内容
  cat >> terms/allowlist_en.txt << 'ENDOFTERMS'
  # --- Tritium safety / confinement (Batch 90) ---
  3-Level Confinement
  Level-2 Confinement
  Level-1 Confinement
  first confinement barrier
  last confinement barrier
  confinement boundary
  confinement integrity
  graded confinement
  static confinement
  dynamic confinement
  negative-pressure confinement
  confinement monitoring
  tritium accidental release
  tritium environmental discharge
  tritium source term assessment
  tritium dose assessment
  tritium mitigation
  permeation reduction factor
  PRF
  tritium diffusion barrier
  tritium-barrier coating
  tritium internal dose
  glovebox detritiation
  tritium off-gas treatment
  tritiated water treatment
  tritium emission monitoring
  occupational tritium exposure
  acceptable tritium dose
  ENDOFTERMS
  ```

- **修改边界**：
  - 仅追加到文件末尾，不得删除、修改或重排现有行
  - ⛔ 不得修改其他任何文件
  - ⛔ 不得在术语中插入制表符或前导/尾随空格
  - 中英文术语必须一一对应（第 N 个中文术语对应第 N 个英文术语，便于交叉核对）

- **质量检查方式**：
  - 检查项 1：`grep -c "一级包容" terms/allowlist_zh.txt` 输出 `1`
  - 检查项 2：`grep -c "Level-1 Confinement" terms/allowlist_en.txt` 输出 `1`
  - 检查项 3：`grep -c "tritium-barrier coating" terms/allowlist_en.txt` 输出 `1`（验证最末术语存在）
  - 检查项 4：`sort terms/allowlist_zh.txt | uniq -d | grep -v "^#" | grep -v "^$"` 无输出（无重复）
  - 检查项 5：`sort terms/allowlist_en.txt | uniq -d | grep -v "^#" | grep -v "^$"` 无输出（无重复）

- **验收标准**：
  - ✅ `grep -c "^一级包容$" terms/allowlist_zh.txt` = 1
  - ✅ `grep -c "^Level-1 Confinement$" terms/allowlist_en.txt` = 1
  - ✅ `grep -c "^# --- Tritium safety / confinement (Batch 90) ---$" terms/allowlist_zh.txt` = 1
  - ✅ 文件末尾无多余连续空行（`tail -1 terms/allowlist_zh.txt` 应输出术语而非空行）
  - ✅ 注释行 `# --- Tritium safety / confinement (Batch 90) ---` 前恰好有一个空行作为分隔

- **潜在风险**：低。纯文本追加，不涉及解析器修改。

- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断
  - 歧义点：[如有] 具体字段名与歧义描述

---

#### Task 1.2: 写入 synonyms 和 denylist 文件

- **目标**：将废弃术语→推荐术语的映射写入 `terms/synonyms.tsv`，将应禁用的旧术语写入 `terms/denylist.txt`
- **依赖**：T1.1（需要 allowlist 中的 preferred 形式作为 synonyms 的 target 列）
- **frontier**：否（依赖 T1.1）
- **执行者**：Task Executor
- **修改内容**：

  文件 `terms/synonyms.tsv`（追加操作 — 文件当前末行为 `tokamaks\ttokamak\ten`，TAB 分隔已验证）：
  ```bash
  # 直接追加（无需空行分隔 — synonyms.tsv 格式紧凑，每行都是数据行）
  cat >> terms/synonyms.tsv << 'ENDOFTERMS'
  三层围包	三级包容	zh
  二层围包	二级包容	zh
  一层围包	一级包容	zh
  3-Loop-Confinement	3-Level Confinement	en
  static containment	static confinement	en
  dynamic containment	dynamic confinement	en
  containment boundary	confinement boundary	en
  containment integrity	confinement integrity	en
  ENDOFTERMS
  ```
  > ⚠️ 关键：列之间必须用字面 TAB 字符（ASCII 0x09）分隔，不可用空格。上述代码块中 `\t` 显示为视觉空格，实际写入时使用 TAB。

  文件 `terms/denylist.txt`（追加操作 — 追加到文件末尾）：
  ```bash
  cat >> terms/denylist.txt << 'ENDOFTERMS'
  三层围包
  二层围包
  一层围包
  3-Loop-Confinement
  ENDOFTERMS
  ```

- **修改边界**：
  - synonyms.tsv: 仅追加到文件末尾，TAB 分隔，不修改现有行
  - denylist.txt: 追加到文件末尾（或 AUTO-INBOX section 内）
  - ⛔ 不得修改其他文件
  - ⛔ synonyms.tsv 中不得使用空格代替 TAB

- **质量检查方式**：
  - 检查项 1：`grep "三层围包.*三级包容" terms/synonyms.tsv` 有输出
  - 检查项 2：`grep "3-Loop-Confinement" terms/synonyms.tsv` 有输出
  - 检查项 3：`grep "^三层围包$" terms/denylist.txt` 有输出
  - 检查项 4：synonyms.tsv 每行恰好 2 个 TAB（3 列）

- **验收标准**：
  - ✅ `grep "三层围包" terms/synonyms.tsv | grep "三级包容"` 有输出
  - ✅ `grep "一层围包" terms/synonyms.tsv | grep "一级包容"` 有输出
  - ✅ `grep -c "^三层围包$" terms/denylist.txt` = 1
  - ✅ `grep -c "^一层围包$" terms/denylist.txt` = 1
  - ✅ `awk -F'\t' 'NF!=3{print NR": bad cols"}' terms/synonyms.tsv` 无输出（每行恰好 3 列）

- **潜在风险**：低。需确认 TAB 字符而非空格分隔。

- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断
  - 歧义点：[如有] 具体字段名与歧义描述

---

### Phase 2: 验证

#### Task 2.1: 运行验证脚本

- **目标**：确认所有修改通过项目的 CI 门控
- **依赖**：T1.1, T1.2
- **frontier**：否
- **执行者**：Task Executor
- **修改内容**：无代码修改 — 仅运行验证命令
- **修改边界**：不修改任何文件
- **质量检查方式**：
  - 检查项 1：`python3 -m pipeline.validate_registry`
  - 检查项 2：`pytest --cov=pipeline --cov-fail-under=45 -q`
  - 检查项 3：`mypy pipeline/ --ignore-missing-imports --no-error-summary`
  - 检查项 4：`ruff check . && ruff format --check .`

- **验收标准**：
  - ✅ `python3 -m pipeline.validate_registry` exit 0
  - ✅ `pytest` 全部通过
  - ✅ `mypy` 无新错误
  - ✅ `ruff` 无新 lint 错误

- **潜在风险**：中。若 validate_registry 拒绝新术语（如与已有概念冲突），需回溯 T1.1/T1.2 调整。

- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断
  - 歧义点：[如有] 具体字段名与歧义描述

---

### Phase 3: 版本发布

#### Task 3.1: Git commit + tag + push

- **目标**：提交所有修改，打 tag v2026.08.12 并推送
- **依赖**：T2.1（所有验证通过）
- **frontier**：否
- **执行者**：Task Executor
- **修改内容**：无代码修改 — git 操作
- **修改边界**：仅 git 操作，不修改文件
- **质量检查方式**：
  - 检查项 1：`git diff --stat` 仅包含预期的 4 个文件
  - 检查项 2：`git tag -l "v2026.08.12"` 返回 tag
  - 检查项 3：`git push && git push origin v2026.08.12` 成功

- **验收标准**：
  - ✅ `git diff --stat` 仅列出 `terms/allowlist_zh.txt`、`terms/allowlist_en.txt`、`terms/synonyms.tsv`、`terms/denylist.txt`
  - ✅ `git tag -l "v2026.08.12"` 非空
  - ✅ commit message 包含 `#2540` 引用

- **潜在风险**：低。标准 git 操作。
- **提交信息建议**：
  ```
  feat(terms): 新增氚安全/包容术语 batch 90 (27组)

  新增三级包容体系(三级/二级/一级)、氚安全、氚屏蔽/阻挡层、
  去氚工艺等27组中英术语。含废弃术语映射(三层围包→三级包容等)。

  Closes #2540
  ```

- **预留歧义标注**：
  - [ ] 无歧义：所有字段可直接执行，无需额外推断
  - 歧义点：[如有] 具体字段名与歧义描述

---

## Execution Wave（并行执行波次）

| Wave | 可并行 Task | Frontier（无人挡即刻开工） | 依赖已完成 |
|------|------------|--------------------------|------------|
| W1 | T1.1 | T1.1 | — |
| W2 | T1.2 | — | W1 |
| W3 | T2.1 | — | W2 |
| W4 | T3.1 | — | W3 |

> 注：T1.1 与 T1.2 理论上可并行（synonyms 的 target 列是手动指定的字符串），但串行执行可让 T1.2 交叉验证 T1.1 的输出。

---

## Post-Execution Verification

### Automated Verification（Task Executor 自动执行）

| ID | Description | Command | Expected |
|----|-------------|---------|----------|
| V1 | 术语总数一致性 | `grep -cFf <(printf '三级包容\n二级包容\n一级包容\n第一包容屏障\n最终包容屏障\n包容边界\n包容完整性\n分级包容\n静态包容\n动态包容\n负压包容\n包容监测\n氚事故释放\n氚环境排放\n氚源项评估\n氚剂量评估\n氚缓解\n渗透降低因子\n氚扩散阻挡层\n防氚涂层\n氚内照射剂量\n手套箱去氚\n氚废气处理\n含氚废水处理\n氚排放监测\n氚职业照射\n氚可接受剂量') terms/allowlist_zh.txt` | 27 |
| V2 | 去重检查 | `sort terms/allowlist_zh.txt \| uniq -d \| grep -v "^#" \| grep -v "^$"` | 无输出（无重复） |
| V3 | Registry 完整性 | `python3 -m pipeline.validate_registry` | exit 0 |
| V4 | 测试套件 | `pytest --cov=pipeline --cov-fail-under=45 -q` | exit 0 |

### Manual（真正需要人工判断）

- [ ] M1: 人工检查 git diff，确认新增术语无拼写错误
- [ ] M2: 确认 `#2540` 相关 PM 任务状态更新为 done

---

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性 | 2 | 2 | 0 |
| R1.5 | 外部引用事实核查 | 0 | 0 | 0 |
| R2 | 可执行性（含脚本干跑） | 3 | 3 | 0 |
| R2.8 | LLM 可执行性审查 | 3 | 3 | 0 |
| R3 | 风险与边缘（含跨轮一致性） | 2 | 2 | 0 |
| **终止** | **T3 — 全部修正清零** | | | **0** |

### 审查详情

**R1 — 结构完整性**
- [修正] 原 V1 命令使用 `grep -cP`（Perl regex，不跨平台）→ 改为 `grep -cFf` + process substitution
- [修正] T1.1 质量检查 4/5 用"新增行数"描述过于机械 → 改为去重检查（更有意义的验证）

**R1.5 — 外部引用事实核查**
- 验证 `terms/allowlist_zh.txt` 末尾为 `反磁通信号`（无尾随空行）
- 验证 `terms/allowlist_en.txt` 末尾为 `Penning-vacuum-gauge`（无尾随空行）
- 验证 `terms/synonyms.tsv` 末尾为 `tokamaks→tokamak→en`，TAB 分隔确认
- 验证 `terms/denylist.txt` 末尾为 `马克装置`
- 验证 `python3 -m pipeline.validate_registry` 可运行（当前输出 "registry OK: 3064 concepts"）
- 验证 `pytest --co` 存在 11 个测试文件

**R2 — 可执行性（含脚本干跑）**
- [修正] T1.1/T1.2 "append only" 描述不够具体 → 改为完整的 `cat >> file << 'ENDOFTERMS'` bash 命令
- [修正] T1.2 验收标准 `grep -cP` → `grep | grep`（无需 Perl regex）
- [修正] denylist 位置 "AUTO-INBOX 之前或末尾" 消除歧义 → 明确追加到文件末尾

**R2.8 — LLM 可执行性审查**
- [修正] 明确 alllists 需要先 `echo '' >> file` 写空行分隔，再追加术语
- [修正] synonyms.tsv 明确 TAB 字符（ASCII 0x09），给出 `awk` 列数检查命令
- [修正] 消除 `grep -cP` 所有出现（3 处），全部改为 POSIX 兼容写法

**R3 — 风险与边缘**
- [修正] T1.2 的 preferred 列引用 T1.1 新增术语（如 `一级包容`、`static confinement`）→ 串行执行设计已确保一致性
- [修正] **关键遗漏**：原始 #2540 的 `三级包容`、`二级包容`、`3-Level Confinement` 在初版 T1.1 追加列表中缺失 → 已补全（术语总数 25→27）
- 已验证 PRF 在 allowlist_en.txt 中不存在（不会重复）
- 回滚策略：如验证失败，`git checkout -- terms/` 恢复所有文件
