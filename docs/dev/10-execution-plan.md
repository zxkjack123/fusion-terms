# fusion-terms 执行计划（分阶段实施）

> 本文把 `docs/dev/*` 的设计方案，落成可直接指导实施的工程执行计划。
>
> 核心原则：**不把 userdb 当源数据**，repo 内以 `terms/*` 为唯一真相；流水线保持可复现：
>
> `sources (外部 Markdown 语料)` → `candidates (候选)` → `review (allow/deny/synonyms)` → `artifacts (产物)` → `Rime 导入/词典`

## 0. 当前工作区现状（基线）

仓库路径：`/home/gw/opt/fusion-terms`

已具备：

- 配置：`config.toml`（默认语料根目录：`/home/gw/ComputeData/pdf2md/ZoteroIngest/staging`）
- 抽词：`pipeline/extract_candidates.py`
  - 输出：`artifacts/candidates_zh.tsv`、`artifacts/candidates_en.tsv`、`artifacts/extract_stats.json`
- 构建：`pipeline/build_terms.py`
  - 输入：`terms/allowlist_zh.txt`、`terms/allowlist_en.txt`、`terms/denylist.txt`、`terms/synonyms.tsv`
  - 输出：`artifacts/domain_terms.txt`
- Rime 导入辅助：`pipeline/rime_export.py`（复用 `/home/gw/.local/bin/rime_import_wordlist.py`）
- 同步到 Fcitx/Rime wordlists：`pipeline/sync_to_fcitx.py`
- VS Code Tasks：`.vscode/tasks.json`（extract/build/sync/export/import）
- 设计文档：`docs/dev/01..04`（架构、流水线、Rime 集成、英文短语增强模式规划）

本执行计划在不破坏上述结构的前提下，按阶段增强：可复现性、抽词质量、增量更新、审核体验、Rime 稳定集成、发布协作。

---

## 1. 阶段 0：工程化基线（可复现 + 可检查）

### 任务 0.1：仓库卫生与工程约束（lint/test/ignore/CI）

**目标**

- 把“能跑”升级为“可复现、可协作、可持续迭代”。
- 明确哪些产物提交、哪些不提交，避免 artifacts/缓存污染 git。

**修改内容**

- 新增（或完善）工程配置：
  - `pyproject.toml`（推荐）：统一 Python 工具配置（pytest/ruff/black/isort/mypy 等，可分阶段启用）
  - `tests/`：最小单测框架与 fixtures
  - `.gitignore`：补全忽略项（如 `.mypy_cache/`、临时 artifacts、缓存）
- （可选）新增 CI：GitHub Actions 在 PR 上跑最小测试集（已添加：`.github/workflows/ci.yml`）。
- （可选）新增 pre-commit：提交前自动做基础检查（已添加：`.pre-commit-config.yaml`）。

**测试内容**

- 在 `tests/fixtures/` 小语料上跑通：`extract → build`。
- 确认 VS Code tasks 仍正常（尤其 `python -m pipeline.*` 模式 import 不受 cwd 影响）。

**验收指标**

- 新机器 clone 后，仅依赖 Python，即可在 fixtures 上一键跑通流程。
- git status 不被缓存/大文件污染。

---

## 2. 阶段 1：第一版“可用词库”（立刻提升输入法体验）

### 任务 1.1：审核准则定稿（review 的“宪法”）

**目标**

- 将 `docs/dev/01-architecture.md` 的范围，固化为更可执行的审核规则，减少每次审核决策成本。

**修改内容**

- 在以下两种方式中二选一（推荐 A）：
  - A）新增 `docs/dev/05-review-rules.md`
  - B）在 `docs/dev/01-architecture.md` 追加“命名/规范化约定”章节

建议至少写清：

- 英文大小写规范：缩写全大写（`NBI`），普通英文单词按惯例（一般小写；专名按惯例）
- 连字符与空格：`H-mode` vs `H mode` 的 preferred form
- 数字/符号：`q95`、`β_N`、`D-T`、`W/Be` 的收录与规范
- 中英双收策略：例如 “托卡马克 / tokamak” 是否双收，还是 synonyms 归一
- 英文多词词组策略（重要）：**词组不作为一个词条入库**。
  - 例：`neutral beam` 只需确保 `neutral` 与 `beam` 在词表中即可
  - 明确不做：`neutralbeam` / `neutral_beam` 这类“无空格二元搭配”
  - 这会带来取舍：短语级一键输出不追求；靠“原子词 + 输入法联想/补全/学习”满足日常输入

**测试内容**

- 取 20 个典型术语（装置/方法/材料/参数/缩写/短语），按规则走一遍，能得出一致结论。

**验收指标**

- ≥90% 的典型术语能“按规则一眼决定收不收、怎么写”。

### 任务 1.2：allowlist/denylist/synonyms 种子集（覆盖核心类别）

**目标**

- 形成第一版高价值术语集，马上能导入并显著改善输入法。

**修改内容**

- 编辑：
  - `terms/allowlist_zh.txt`
  - `terms/allowlist_en.txt`
  - `terms/denylist.txt`
  - `terms/synonyms.tsv`

建议按类别分段注释（不会影响解析）：

- Devices：ITER/EAST/JET/DIII-D/…
- Heating：NBI/ICRH/ECRH/LHCD/…
- Diagnostics：Thomson scattering / interferometry / bolometry / …
- Materials：tungsten / beryllium / Nb3Sn / CuCrZr / …
- Parameters/regimes：q95 / beta_N / pedestal / confinement / …

**测试内容**

- 运行 VS Code task：
  - `fusion-terms: build final wordlist`
  - `fusion-terms: generate rime import file`
  - （可选）`fusion-terms: sync to fcitx wordlists`
  - （可选）`fusion-terms: generate + import to Rime`

**验收指标**

- `artifacts/domain_terms.txt` 生成成功：无空行/奇怪空格/明显噪声。
- `artifacts/domain_terms.txt` 中不应出现包含空格的英文词条（即每行必须是单个 token）。
- 导入后：至少 30 个代表性术语能稳定打出（中英文各测一些）。

---

## 3. 阶段 2：抽词质量提升（降噪优先，随后提召回）

> 当前中文候选量巨大属于预期；此阶段目标是让候选更“可审”。

### 任务 2.1：Markdown 清洗增强（高性价比降噪）

**目标**

- 更好地丢弃：参考文献段落、表格噪声、图注/表注、公式碎片、模板化句子等。

**修改内容**

- 增强 `pipeline/common.py::clean_markdown_lines()`：
  - 识别并截断 references/参考文献区
  - 表格行（`| a | b |`）与长数字/符号密集行的过滤策略
  - 常见论文样板语行级过滤（注意避免误伤术语）
- 新增单测：
  - `tests/test_clean_markdown.py`
  - `tests/fixtures/` 中加入包含 code fence / table / refs 的 markdown

**测试内容**

- 单元测试：fixtures 清洗输出符合预期。
- 小样本抽词（如 `--max-files 10`）：对比清洗增强前后 top 候选的噪声占比。

**验收指标**

- 清洗相关单测覆盖关键噪声样式。
- 小样本下：top-100 候选中“明显非术语”比例显著下降。

### 任务 2.2：候选过滤输出（不破坏原始 TSV 合同）

**目标**

- 在保留 `candidates_*.tsv` 原始输出的同时，新增“过滤版候选”以提升审核效率。

**修改内容**

- 扩展 `pipeline/extract_candidates.py`（保持默认行为不变）：
  - `--min-count-zh` / `--min-count-en`
  - `--topk-zh` / `--topk-en`
  - （可选）`--zh-stopwords path` / `--en-stopwords path`

建议：把 stopwords 作为 repo 内可协作维护的种子文件（方便持续降噪），例如：

- `terms/stopwords_zh.txt`
- `terms/stopwords_en.txt`
- 新增产物（建议命名）：
  - `artifacts/candidates_zh.filtered.tsv`
  - `artifacts/candidates_en.filtered.tsv`

**测试内容**

- 单测：min-count/top-k 的过滤正确。
- 集成：小样本下 filtered 行数显著减少且包含预期术语。

**验收指标**

- 审核者可在 30–60 分钟内从 filtered 候选中挑出一批高价值术语。
- 原始候选仍保留用于回溯与调参。

---

## 4. 阶段 3：增量抽取（把“持续更新”成本降到接近 0）

### 任务 3.1：文件哈希缓存（只处理新增/变更语料）

**目标**

- 避免每次全量扫描海量 Markdown；支持增量抽取与 delta 报告。

**修改内容**

- 新增缓存（建议放 `artifacts/.cache.json` 或 `artifacts/.cache/`）：
  - file path → content hash → last processed → stats
- `pipeline/extract_candidates.py` 新增：
  - `--incremental`：跳过未变化文件
  - （可选）`--since YYYY-MM-DD`：仅处理某日期后新增/变更
- 新增 delta 报告：`artifacts/extract_delta.json`

**测试内容**

- 单测：同一文件二次运行会被跳过；内容变化后会重新处理。
- 集成：fixtures 模拟变更，delta 统计正确。

**验收指标**

- 二次运行跳过 >90% 未变化文件（取决于真实语料更新量）。
- delta 报告可直接指导“本次要审核哪些新增候选”。

---

## 5. 阶段 4：英文多词词组处理（按 token 入库；短语仅作“发现线索”可选）

> 你已明确：不需要无空格形式的二元搭配；多词英文词组（如 `neutral beam`）**按两个单词分别入库**即可。
> 因此本阶段的默认目标不是“让短语作为一个词条可触发”，而是：确保组成词覆盖完善、规范化一致。

### 任务 4.1：英文 token 规范化与拆分约束（默认 on）

**目标**

- 确保英文入库单位是单个 token（每行一个），避免后续 Rime 侧出现“带空格词条不触发/不稳定”的不确定性。
- 对多词词组：不追求短语级体验，专注把组成词（以及必要的缩写/符号 token）收全。

**修改内容**

- 在 `pipeline/build_terms.py` 的校验阶段增加硬性规则（已实现）：
  - 丢弃/报错：包含空格或制表符的 term
  - 允许：连字符、斜杠、点号、数字、希腊字母（按既定规范）
- 在 `docs/dev/05-review-rules.md`（或 `01-architecture.md`）把该约束写成强规则：英文词组只拆分入库，不做拼接。

**测试内容**

- 单测：构建时遇到包含空格的 term 会被阻止进入 `artifacts/domain_terms.txt`（并给出可定位的报错/统计）。

**验收指标**

- `artifacts/domain_terms.txt` 满足“每行单 token”约束。

### 任务 4.2（可选/后续）：英文短语挖掘（YAKE/RAKE/spaCy）仅作为“词汇发现线索”

**说明**

- 若未来需要“更快发现候选词”，可以启用短语挖掘，但输出只用于提示“哪些 token 值得加入 allowlist/denylist/synonyms”，而不是把短语本身导入词表。
- 该可选项的设计仍保留在 `docs/dev/04-english-phrase-extraction.md`，但其验收不再要求短语可在 Rime 中作为一个词条触发。

---

## 6. 阶段 5：审核工具化（Review Pack / Diff / 指导审核）

### 任务 5.1：生成审阅包与差分报告

**目标**

- 将审核从“翻大 TSV”升级为“定向审核新增/高价值候选”。

**修改内容**

- 新增脚本（建议）：
  - `pipeline/review_pack.py`：输出分组审阅包（Markdown/CSV）
  - `pipeline/diff_candidates.py`：对比上次候选，生成新增/上升项列表
- 文档补充：在 `docs/dev/02` 中写清建议审核节奏（每周/每次增量）。

**测试内容**

- 单测：diff 逻辑正确。
- 人工验收：review pack 是否显著提升审核速度。

**验收指标**

- 每次增量更新审核可在 30–90 分钟完成一轮有效迭代（视新增量）。

---

## 7. 阶段 6：Rime 集成加固（导入安全、可回滚、可验证）

### 任务 6.1：导入安全与幂等

**目标**

- Option A（导入 userdb）变得可控：备份、dry-run、失败可回滚。

**修改内容**

- 增强 `pipeline/rime_export.py` 或新增 `pipeline/rime_import_safe.py`：
  - `--dry-run`（只生成 import 文件不导入）
  - 导入前备份关键文件（写日志）
  - 导入后给出验证提示/检查项
- 更新 `docs/dev/03-rime-integration.md`：补充回滚流程。

**测试内容**

- dry-run 的行为测试。
- 真实导入属于手工集成测试（避免自动化脚本破坏用户环境）。

**验收指标**

- 任意一次导入都可回滚。
- 导入失败不会静默，错误信息可定位。

### 任务 6.2：Option B baked dictionary（`.dict.yaml`）

**目标**

- 生成 `fusion_terms.dict.yaml` 并能被 rime-ice 引用，获得最稳定的迁移与一致性。

**修改内容**

- 新增生成器：`pipeline/generate_dict_yaml.py`
- 文档：在 `docs/dev/03` 写清接入方式（`import_tables` 或 `table_translator`）与 deploy 步骤。

**测试内容**

- YAML 结构校验（关键字段齐全）。
- 手工：Rime deploy 成功且可打出。

**验收指标**

- 新机器无需依赖 userdb 学习状态，也能一致获得术语体验。

---

## 8. 阶段 7：发布与共享（可选，但强烈建议）

### 任务 7.1：版本与变更记录

**目标**

- 每次更新可回答“改了什么/为什么”，便于回滚与协作。

**修改内容**

- 新增 `CHANGELOG.md`（或 `docs/releases/`）
- `pipeline/build_terms.py` 输出摘要统计：新增/删除/总数、按语言占比
  - 默认写入：`<out-dir>/<output_stem>_build_stats.json`（例如 `artifacts/domain_terms_build_stats.json`）
  - 字段：`counts.total/zh/en/added/removed/synonyms_mapped` + `added[]/removed[]`（用于审计，可忽略）

**测试内容**

- build 输出稳定、统计一致。

**验收指标**

- 任意版本可追溯变更与原因。

---

## 9. Known risks / non-goals / measurement plan

本节把当前方案中已识别的风险点显式化，并给出“落地条目 + 验收用例表”，避免项目推进到中后期才发现关键缺口。

### 9.1 Known risks（已知风险）与对应缓解措施

#### 风险 A：中文候选量爆炸，审核不可持续

- **现象**：当前中文抽取策略偏“固定长度汉字片段”，会产出大量非术语子串。
- **影响**：候选 TSV 过大→审核效率极低→allowlist 增长停滞。
- **缓解措施（落地条目）**：
  - 优先做阶段 2：
    - 2.1 强化清洗（references、表格、图注、公式噪声）
    - 2.2 输出 filtered candidates（min-count/top-k/stopwords）
  - 引入“审阅友好输出”作为强制工序：每次 review 只看 filtered。
- **验收**：`candidates_zh.filtered.tsv` 的 top-100 中“明显非术语”比例显著下降（人工抽查）。

#### 风险 B：英文 `count` 语义易被误用

- **现象**：英文候选计数可能是“按行出现次数（line-frequency）”，不等于真实 token 出现次数。
- **影响**：阈值过滤/Top-K 策略可能失真（误杀或误留）。
- **缓解措施（落地条目）**：
  - 在 `docs/dev/02-pipeline.md` 或本文件中明确 `count` 的定义。
  - 若后续需要，提供两种计数（line-frequency 与 occurrence）并在 TSV 列名区分。
- **验收**：过滤参数（如 `--min-count-en`）能被一致解释；review 时不会因误解 `count` 做出错误取舍。

#### 风险 C：参数/符号类术语覆盖不足（q95、β_N、τ_E 等）

- **现象**：参数名常包含小写+数字、希腊字母、下划线、乘号、LaTeX 转义（例如 `\\beta_N`）。
- **影响**：你最关心的一类（参数名）可能“抽不到/很难靠自动候选发现”，只能手工 seed。
- **缓解措施（落地条目）**：
  - 阶段 1.2 先手工 seed 一批关键参数（确保立即可用）。
  - 阶段 2.2/后续增强英文候选规则：加入 parameter token pattern（例如 `q\\d+`、`beta_N`/`β_N`、`tau_E`/`τ_E`、`E×B`/`ExB` 等）。
  - 清洗阶段保留有意义的符号，不要在清洗里把它们全部剔除。
- **验收**：参数类术语在候选与最终 artifacts 中有稳定覆盖（见 9.3 验收用例表）。

#### 风险 D：英文词组按 token 入库会“丢失短语级一键输出”

- **现象**：你选择不把 `neutral beam` 这类多词短语作为单条词条导入，因此无法保证“输入一次就出整段短语”。
- **影响**：短语级输入效率可能不如“短语词条”方案；但工程复杂度与不确定性显著下降。
- **缓解措施（落地条目）**：
  - 确保组成词覆盖足够：`neutral`、`beam`、`injection` 等必须进入 allowlist（或能从候选中稳定浮现）。
  - 对强需求的短语，优先考虑引入/固化缩写（如 `NBI`）而不是做无空格拼接。
  - 继续保留 Option B baked dict 作为“将来真的需要短语体验”时的升级通道，但不作为当前验收要求。
- **验收**：组成词在 Rime 中都可稳定触发；缩写类术语能满足多数高频输入。

#### 风险 E：`synonyms.tsv` 第三列（lang）在实现中可能未生效

- **现象**：文档允许 `alias\tpreferred\tlang(optional)`，但实现若只读前两列，则第三列仅是注释。
- **影响**：未来想做“按语言不同归一策略”时可能踩坑。
- **缓解措施（落地条目）**：
  - 已选择：在文档中明确“当前忽略第三列（lang 仅作注释/保留字段）”，并在实现中对冲突映射做硬校验。
- **验收**：团队成员不会误以为 lang 已生效；`synonyms.tsv` 出现同 alias 不同 preferred 时会 fail fast。

#### 风险 F：全量语料抽取的性能与内存边界

- **现象**：候选字典（term→count/examples/files）可能很大，全量处理会耗时/占内存。
- **影响**：跑不动/跑很慢，阻断迭代。
- **缓解措施（落地条目）**：
  - 阶段 3.1 做增量缓存（hash cache）。
  - 限制 examples/files 保存上限（当前已有），并在全量下复核是否足够。
  - 必要时引入 streaming/分桶（例如先写临时计数，再归并）。
- **验收**：二次运行增量模式能明显加速；全量模式可在可接受时间内完成（以你机器为准）。

#### 风险 G：registry 与 `terms/*` 双源并存导致“真相漂移”

- **现象**：当 `terms/allowlist_* / denylist / synonyms.tsv` 仍在使用，同时又新增 `terms/registry/*` 时，同一概念可能出现两套不同的 preferred/alias/禁用写法。
- **影响**：
  - IME 词表与写作门禁（Vale）给出的推荐/禁用提示不一致
  - 检索扩展/自动标签归一到的概念节点与实际入库 token 不一致
  - 让“多工具稳定服务”的定位失效（工具之间互相打架）
- **缓解措施（落地条目）**：
  - 在阶段 8 引入**一致性校验**（强制失败，而不是静默容忍）：
    - concept_id 唯一
    - alias 不允许映射到多个 concept_id（除非显式标记为允许多义，后续再做）
    - 禁用写法（forbidden/deprecated）不得出现在 IME 输出词表中
  - 明确迁移策略：阶段 8 先让 registry 服务 Vale/query/tag；当覆盖率足够后，再引入“从 registry 生成 allowlist/synonyms”的工具，并用回归测试保证两条路径一致。
- **验收**：
  - registry 导出产物（Vale/query/tag）是可复现的（deterministic）
  - 同一 alias 不会在不同产物中指向不同概念
  - 禁用写法不会“漏进”最终 IME 词表

### 9.2 Non-goals（非目标，避免范围失控）

- 不追求“完全自动、零人工”的术语库：**allowlist 审核**是质量保证核心。
- 不追求一次性覆盖“所有专业术语”：以迭代方式提升覆盖率。
- 不在早期就引入复杂的中文 NLP 分词/依存句法：先把清洗、过滤、review 体系做稳。
- 不把 `*.userdb` 当成可合并的源数据：它只是消费端缓存/学习状态。

### 9.3 Measurement plan（度量与验收用例表）

#### 关键度量指标（建议每轮迭代记录）

- **候选质量**：
  - filtered top-100 的“可接受率”（人工抽查）：目标逐步提升
  - 噪声主要来源分类（refs/table/caption/通用词/子串）
- **审核效率**：
  - 每小时可稳定新增多少个高质量术语（allowlist 增量）
- **覆盖面**：
  - 装置名/缩写/方法/材料/参数五类是否都有稳定增长
- **导入可靠性**：
  - 固定验收用例集导入后是否可触发
- **增量性能**：
  - `--incremental` 模式下跳过比例、运行时间变化

- **registry 质量（多工具一致性）**：
  - 证据覆盖率：核心概念中有来源（evidence/source）的比例
  - 分类覆盖率：各 category（装置/指标/方法/材料/数据字段/软件工具）概念数量的变化趋势
  - 漂移告警数：同一文档内出现 deprecated/forbidden 写法的命中次数（未来由 drift scan 产物统计）

#### 验收用例表（建议作为阶段 6 的固定回归集）

下表是一套最小但覆盖关键类型的用例。每次做了“清洗/抽取/构建/导入”相关改动，都建议跑一遍。

| 类别         | 代表用例（示例）                                        |    预期出现在 candidates | 预期出现在 artifacts/domain_terms.txt | 预期在 Rime 可触发（A 或 B） |
| ------------ | ------------------------------------------------------- | -----------------------: | ------------------------------------: | ---------------------------: |
| 装置/设施    | ITER, EAST, JET, DIII-D                                 |                 是（en） |                                    是 |                           是 |
| 缩写         | ICRH, ECRH, NBI, ELM, H-mode                            |                 是（en） |                                    是 |                           是 |
| 英文词组拆分 | neutral beam injection（拆分为 neutral/beam/injection） |                 是（en） |                                    是 |                           是 |
| 材料/牌号    | Nb3Sn, CuCrZr, tungsten, beryllium                      |                 是（en） |                                    是 |                           是 |
| 参数/符号    | q95, beta_N / β_N, tau_E / τ_E                          | 规则增强后：应为是（en） |                                    是 |                           是 |
| 混合串       | D-T, W/Be                                               |                 是（en） |                                    是 |                           是 |

说明：

- 若某一类在 candidates 中长期缺失，应优先通过“规则增强 + 清洗不误伤”解决，而不是完全依赖手工 seed。
- 本方案不要求“英文短语带空格”作为单条词条可触发；验收仅关注拆分后的 token 覆盖与可触发性。

---

## 10. 进度跟踪 Checklist（建议贴到 issue/项目看板）

### 阶段 0：基线

- [x] `.gitignore` 完整忽略缓存（含 `.mypy_cache/`）
- [x] `tests/fixtures` + 最小单测框架已建立
- [x] fixtures 上 `extract → build` 可复现跑通
- [x] pre-commit 配置已提供（`.pre-commit-config.yaml`）
- [x] CI 已提供（`.github/workflows/ci.yml`，运行 pytest + compileall）

### 阶段 1：第一版可用词表

- [x] 审核规则文档定稿（大小写/连字符/混写/符号；见 `docs/dev/05-review-rules.md`）
- [x] `allowlist_zh/en` 有覆盖核心类别的种子术语
- [x] `synonyms.tsv` 覆盖常见变体归一
- [x] `synonyms.tsv` 冲突映射会被构建拒绝（同 alias 不同 preferred）
- [x] 构建拒绝不可见/控制字符词条（例如零宽空格 U+200B）
- [ ] 构建 + 导入后：关键术语可稳定打出
  - [x] 提供手工验收包生成器（`python -m pipeline.ime_acceptance_pack` 生成 `ime_acceptance_terms.txt/json`）

### 阶段 2：降噪与审阅友好

- [x] 清洗增强有单测（refs/table/caption 等）
- [x] 提供 filtered candidates 输出（min-count/top-k/stopwords）
- [x] 提供 repo 内 stopwords 种子（`terms/stopwords_zh.txt` / `terms/stopwords_en.txt`）
- [x] 2026-02-03：完成一次 top-100 抽查记录（见下）
- [x] 2026-02-04：在 500-file 样本 + `terms/stopwords_zh.txt` 下，top-100 噪声明显下降（见下）

抽查记录（2026-02-03）：

- 样本：真实语料子集 `--max-files 500`
- 命令：`python3 -m pipeline.extract_candidates --source-root /home/gw/ComputeData/pdf2md/ZoteroIngest/staging --out-dir artifacts --max-files 500 --min-count-zh 3 --topk-zh 120 --incremental`
- 观察：`candidates_zh.filtered.tsv` 的 top-30 仍出现大量通用/结构性片段（如：`其中`、`例如`、`所示`、`此外`、`所以`、`但是`、`得到`、`因此`、`如图`、`从式`、`称为`、`左右`、`以上`、`量级` 等），说明中文侧还需要进一步降噪（下一步通常会倾向引入 `--zh-stopwords` 的常用噪声词表 + 更强的结构性行过滤/分割策略）。

抽查记录（2026-02-04）：

- 样本：同上（真实语料子集 `--max-files 500`）
- 命令：`python3 -m pipeline.extract_candidates --source-root /home/gw/ComputeData/pdf2md/ZoteroIngest/staging --out-dir artifacts --max-files 500 --min-count-zh 3 --topk-zh 120 --zh-stopwords terms/stopwords_zh.txt --incremental`
- 观察：top-100 中上一轮的典型结构词（`其中/例如/所示/此外/所以/但是/因此/如图/量级...`）被 stopwords 有效剔除；本次用同一套启发式标记做粗略估计，noise-ish 从 **21/100** 降到 **5/100**（仅作对比参考，不是严格指标）。
- 仍可能残留的通用噪声例子：`从式`、`这时`、`近年来`、`如果`、`也就是说` 等（可按实际 review 体验再决定是否加入 stopwords）。

### 阶段 3：增量更新

- [x] 有 hash cache，未变文件可跳过（`extract_candidates --incremental`）
- [x] 有 delta 报告（新/变/跳过统计；见 `artifacts/extract_delta.json`）
- [x] 增量审核成本显著下降（无变更时：增量抽取跳过全部文件，review pack diff 为空；已用回归测试固化）

### 阶段 4：英文词组处理（token 级）

- [x] 构建产物不含空格词条（每行单 token）
- [x] 多词词组的组成词（neutral/beam/injection 等）能在候选与最终词表中稳定覆盖（英文候选抽取会从含技术 token 的行补充提取小写组成词）
- [x] （可选）短语挖掘仅作为“发现线索”启用，不作为验收项（`extract_candidates --en-phrases rake` 写出 `candidates_en_phrases.tsv`）

### 阶段 5：审核工具化

- [x] review pack / diff 新增候选可用（入口：`python -m pipeline.review_pack --out-dir artifacts`）
- [x] allow/deny/synonyms 更新更省时（入口：`python -m pipeline.apply_decisions --terms-dir terms --decisions artifacts/review_pack/decisions.tsv --apply`；默认 dry-run）

### 阶段 6：Rime 稳定集成

- [x] 导入安全（备份/回滚/dry-run/验证；入口：`python -m pipeline.rime_import_safe`；真实导入仍建议手工集成测试）
- [x] baked dict 方案可用（可选，但建议最终上；入口：`python -m pipeline.generate_dict_yaml`；Rime deploy 属于手工集成测试）

### 阶段 7：发布协作

- [x] changelog/版本策略明确（见仓库根目录 `CHANGELOG.md`）
- [x] 构建统计报表（新增/删除/归一化）可生成（`build_terms` 默认写出 `*_build_stats.json`）

### 阶段 8：术语注册表（registry）升级（多工具稳定服务）

> 目标：让本项目不仅生成 IME token 词表，还能稳定服务写作门禁（Vale）、检索扩展、自动标签、以及后续的指标口径/单位等“知识基础设施”。
> 兼容策略：先新增 registry 源数据与导出产物；不打断现有 `terms/*` → `build_terms` → `domain_terms.txt` 的输入法路径。

- [x] 增加 registry 设计文档与最小数据模型（concepts/aliases/evidence）（见 `docs/dev/06-terminology-registry-upgrade.md`）
- [x] 任务 8.1：落地最小 registry 源数据（`terms/registry/concepts.tsv` + `aliases.tsv` + `evidence.tsv`）
  - 验收：至少覆盖一小批 must-have 概念（装置/缩写/指标/材料/方法各≥1），并能表达 preferred/alias/forbidden
- [x] 任务 8.2：registry 一致性校验（validator）
  - 验收：概念 id 唯一；alias 不冲突；非法字符被拒绝；forbidden/deprecated 不得出现在 IME allowlists（由 `python -m pipeline.validate_registry` 与单测保证）
- [x] 任务 8.3：导出多消费者产物（exporter）
  - [x] 8.3a Vale：`artifacts/vale/accept.txt` / `artifacts/vale/reject.txt`（入口：`python -m pipeline.export_registry`）
  - [x] 8.3b 检索扩展：`artifacts/query_expansions.json`（入口：`python -m pipeline.export_registry --query-expansions`）
  - [x] 8.3c 自动标签：`artifacts/tag_rules.jsonl`（alias → concept_id/category；入口：`python -m pipeline.export_registry --tag-rules`）
  - 验收：导出可复现（排序稳定），且同一 alias 在各产物指向一致
- [x] 任务 8.4：与现有 IME 路径的关系固化（不破坏兼容）
  - 验收：现有 `build_terms` 行为不变；registry 产物的引入不会要求用户更改 IME 工作流（已用回归测试覆盖）
