# fusion-terms 升级规划：从“输入法词表”到“术语注册表（registry）”

> ✅ **状态：已实现** — registry 于 v2026.03.16 上线，949 concepts / 4647 aliases（截至 v2026.03.24.1）。本文保留为设计参考。

> 目标：让 `fusion-terms` 作为一个**稳定、可复现、可审计**的“术语注册表”同时服务多个工具：
>
> - 输入法（Rime）：token 级词表（现有能力）
> - 写作/审稿：术语一致性门禁（Vale accept/reject、术语漂移扫描）
> - 检索/知识管理：检索 query 扩展、自动标签/索引
> - 数据与实验：指标口径、单位/量纲、元数据模板（逐步演进）
>
> **关键原则**：保持对当前 IME 流水线的兼容；先把“概念映射 + 分类 + 证据来源”做成可用的最小闭环，再逐步叠加口径/单位/公式等“高 ROI”字段。

---

## 1. 为什么需要 registry（概念层）

当前 repo 以 `terms/allowlist_*` + `denylist` + `synonyms.tsv` 为中心，能很好地生成 IME 词表。但当你要服务更多场景时，仅有“token 列表”不够：

- **同一概念多写法**需要统一口径（中文别名/旧译名/缩写混用）
- **证据链**（来源：论文/标准/内部定义）决定了术语的可信度与可追溯性
- **分类**（装置/子系统/指标/材料/方法/数据字段/软件工具…）是做检索扩展、自动标签、审稿门禁的前提
- **指标口径**（定义/单位/公式/范围/缺失值含义）是“减少实验/写作返工”的高杠杆

因此建议引入一个新的核心层：**Concept Registry（概念注册表）**。

---

## 2. 总体结构（三层：token → 概念映射 → 口径/证据）

### 2.1 Token 层（现有，继续保留）

- 面向输入法/索引的“可直接命中”的最小单位：**单 token**（强约束）
- 由 `pipeline/build_terms.py` 继续生成：`artifacts/domain_terms.txt`
- 规则：
  - 不允许空白字符（已实现）
  - 不允许不可见/控制字符（已实现）
  - 同一 alias 不允许映射到不同 preferred（已实现）

### 2.2 概念映射层（新增，最小可用闭环）

- 每个概念一个稳定的 `concept_id`
- 绑定：preferred 写法（zh/en/abbr）、别名、禁用写法、分类
- 用途：
  - 写作门禁：推荐/禁用写法提示
  - 检索扩展：同义词/缩写/中英互扩
  - 标签归一：不同写法 → 同一概念节点

### 2.3 口径/证据层（新增，分阶段演进）

- `evidence/source`：来源（DOI/标准号/内部文档链接/仓库路径）
- `definition/unit/allowed_units/formula/stat_scope`：指标口径（高 ROI）
- `metadata_slots`：方法/实验/仿真应记录的元数据模板（advanced）

---

## 3. 建议的数据模型（repo 内源数据）

为保持可读、易 merge、低门槛，优先采用 TSV + 少量 JSON（可选）。建议新增目录：

- `terms/registry/`（新）
  - `concepts.tsv`
  - `aliases.tsv`
  - `evidence.tsv`
  - `metrics.tsv`（可选，指标口径；后续再加）

当前仓库已落地最小三张表（可从这里开始填充与迭代）：

- `terms/registry/concepts.tsv`
- `terms/registry/aliases.tsv`
- `terms/registry/evidence.tsv`

说明：`evidence.tsv` 里允许先用 `internal:TODO:...` 占位，后续逐步补齐 DOI/标准号/内部链接。

为避免“真相漂移”（registry 与 `terms/*` 并存），建议把一致性校验作为常规门禁。当前仓库已提供最小校验器：

- `python -m pipeline.validate_registry --terms-dir terms`

导出多消费者产物的入口（当前已实现 Vale accept/reject；query/tag 导出在后续小任务中补齐）：

- `python -m pipeline.export_registry --terms-dir terms --out-dir artifacts`

已实现的导出项：

- Vale：`artifacts/vale/accept.txt`、`artifacts/vale/reject.txt`
- 检索扩展：`artifacts/query_expansions.json`（`--query-expansions`）
- 自动标签：`artifacts/tag_rules.jsonl`（`--tag-rules`）

### 3.1 `terms/registry/concepts.tsv`

每行一个概念（概念主表）。建议字段（可先实现前 6 列）：

- `concept_id`：稳定 id（建议小写、`-` 分隔，如 `neutral-beam-injection`）
- `category`：分类（枚举或自由文本；推荐先自由文本，后续收敛）
- `preferred_zh`：推荐中文写法（可空）
- `preferred_en`：推荐英文写法（可空；必须是单 token 或拆分后的核心 token 组合的“概念名”，不直接用于 IME）
- `preferred_abbr`：推荐缩写（可空）
- `status`：`active|deprecated|draft`
- `notes`：可选备注

> 注：`preferred_en` 在 registry 层可以是短语，但**导出到 IME 时必须拆分为 token**；短语本身不进入 IME 词表。

### 3.2 `terms/registry/aliases.tsv`

别名/禁用写法表（面向写作门禁 + 检索扩展 + 标签归一）。建议字段：

- `alias`：别名字符串（允许短语；但若要进入 IME，则必须另有 token 形态）
- `concept_id`：归一到哪个概念
- `lang`：`zh|en|abbr|mixed|unknown`
- `kind`：`preferred|alias|deprecated|forbidden`
- `comment`：来源/说明（可选）

### 3.3 `terms/registry/evidence.tsv`

证据链（最小实现：把来源挂上即可）。建议字段：

- `concept_id`
- `source`：DOI/URL/标准号/内部文档路径
- `quote`：可选摘录（短）
- `added_by` / `added_at`：可选

### 3.4 `terms/registry/metrics.tsv`（后续）

指标口径（高 ROI）。建议字段：

- `concept_id`
- `definition`
- `unit`
- `allowed_units`（逗号分隔或 JSON）
- `formula`（可用 LaTeX）
- `stat_scope`（统计口径/范围）

---

## 4. 产物与消费者（统一从 registry 导出）

建议新增统一导出脚本（未来实现）：`pipeline/export_registry.py`，输出以下 artifacts：

### 4.1 输入法（现有能力保持不变）

- `artifacts/domain_terms.txt`：单 token 词表（`build_terms` 继续提供）
- 未来：由 registry 自动生成 allowlist/denylist/synonyms，或直接生成 domain_terms（但保留现有接口作为兼容层）

### 4.2 写作/审稿（Vale / drift scan）

- `artifacts/vale/accept.txt`：推荐写法（preferred + 常见 alias）
- `artifacts/vale/reject.txt`：禁用写法（forbidden + deprecated）
- `artifacts/review/term_drift_report.json`：同一文档内出现多个写法时的提示（后续工具）

### 4.3 检索 query 扩展

- `artifacts/query_expansions.json`：`concept_id -> {queries: [...], aliases: [...], preferred: ...}`
- 可直接用于 Scholar/WoS/arXiv/Crossref 检索串生成

### 4.4 自动标签/索引

- `artifacts/tag_rules.jsonl`：alias/pattern -> concept_id/category
- 用于扫描你的 Markdown/PDF2MD 语料，把笔记/文献自动贴标签并归一到概念

### 4.5 内容生成 / 去 AI 化服务

- registry 天然是“术语口径/定义/单位/证据”数据库：
  - 生成一致的术语卡片（定义+例句+证据）
  - 生成指标模板槽位（证据、单位、判据）
  - 在改写/去 AI 化时，确保术语写法稳定、口径一致

---

## 5. 与现有 repo 的兼容策略（迁移路径）

为了不打断你已经可用的 IME 流程，采用“渐进迁移”：

1) **保持现状**：`terms/allowlist_* / denylist / synonyms.tsv` 继续是 IME 的直接输入。
2) **新增 registry（不接管构建）**：先把最关键概念（must-have）录入 `concepts.tsv + aliases.tsv + evidence.tsv`。
3) **新增导出器**：从 registry 导出 Vale/Query/Tag 等产物；IME 仍使用现有 `build_terms`。
4) **后续再接管 IME**：当 registry 覆盖率足够高时，再引入“从 registry 生成 allowlist/synonyms”的工具，并用测试保证两条路径产物一致。

---

## 6. 最小下一步（建议落地顺序）

为了立刻服务“写作门禁 + 检索扩展 + 标签归一”，最小闭环只需要：

- `concepts.tsv`：加上 `category`
- `aliases.tsv`：把常见别名/缩写归一到 `concept_id`
- `evidence.tsv`：每个关键概念至少 1 条来源

随后即可实现：

- 自动生成 Vale accept/reject
- 自动生成 query expansions
- 自动生成 tag rules

指标口径（`metrics.tsv`）可以作为第二波高 ROI 增量。
