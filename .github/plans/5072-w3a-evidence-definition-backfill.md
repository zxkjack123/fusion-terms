---
plan_schema_version: "1.0"
linked_spec: null
scope_mode: "HOLD"
generated_at: "2026-10-30T21:24:03+08:00"
revised_at: "2026-10-31T15:46:53+08:00"
git_commit: "b0bef07"
mode: "refine"
revision: "2"
status: "active"
pm_task: "5072"
title: "T-4973 W3a 证据与释义补强"
adjudication: "方案甲 — 按目标中文名补齐（用户裁决 2026-10-31）"
---

# Plan: T-4973 W3a 证据与释义补强（PM #5072）

> **Status**: ACTIVE (2026-10-31, rev 2 — CT REFUTED 后按用户裁决修订)
> **目标**: 把 `w3.ids` 的 **747** 行占位 zh 释义补成真实中文释义（431 条翻译 + 316 条交叉引用）；把 854 条空 `evidence.quote` 补成有上游出处的非空引文；修复 `registry_batch_verify.py --self-test` 的 19/24 漂移（修复后 24/24，再随 evidence 模式扩到 **27/27**），并让 W3a 的「依据可核验」判据变成可机械执行、可失败的验收命令。
> **非目标**:
> 1. 不改 `concepts.tsv` 的 `preferred_zh` / `category` / `preferred_en`；不改 `pipeline/`；不改父任务 T-4973 的历史计划与验收记录；不重做 854 个中文名。
> 2. **不重新核验名称**：本任务只核验 evidence 的 quote 与 source URL 两件事；名称正确性以 2026-10-29 命名基线裁决为准，本任务不重开该裁决（见 D1/G1、C5）。
> 3. 不修 303 条合法但过短的 en「See X」`DEFINITION` 之外的全库短定义；不修 99 条非 w3 的 `corresponding to` 套话变体（见 §6）。
> **用户裁决（2026-10-31，适用于 316 条 CROSS_REF）**: **方案甲 — 按目标中文名补齐**。zh = `见 <目标 preferred_zh>。`；无法解析的复合形态必须逐条登记并解析（附录 C），不得静默翻译；16 条污染行必须与污染源文本隔离，zh 一律不得复现污染内容。

## 0. 数据基线与缺口（执行前实测）

基线：`git rev-parse HEAD` = `b0bef07`（执行时重测，见 T0.0）；工作区唯一未跟踪文件 `iaea_fusion.html` 不纳入任何提交。下表全部数值为 `b0bef07` 实测值，执行时由 T0.0/T0.3 重测；漂移则先更新本表再动手。

| 指标 | 基线实测 | 来源 / 判定 |
|---|---:|---|
| `w3.ids` | **854** | `.github/plans/t4973-batches/w3.ids` |
| w3 `definitions.tsv` zh 行 | **854** | 每 id 恰好 1 条 zh |
| 其中占位模板（含 `对应英文`） | **747** | `聚变/核工程术语，对应英文“X”。` |
| 　├ 行型 `DEFINITION`（en 非 `See X.`） | **431** | 需翻译（§7 Phase 2 翻译协议） |
| 　├ 行型 `CROSS_REF`（en 为干净 `See X.`） | **300** | 方案甲 → `见 <preferred_zh>。` |
| 　└ 行型 `CORRUPT`（`See X.` 后粘了下一条目正文） | **16** | CROSS_REF 族的子集，**必须隔离污染**；300 + 16 = 316 交叉引用族 |
| 316 交叉引用族中可直接机械解析出目标 | **287** | 248 直接命中 + 25 复合形态命中 + 14 污染行命中（目标取自首句） |
| 316 交叉引用族中需逐条登记台账（附录 C） | **68** | 29 条 `NO-TARGET`（27 干净 + 2 污染）+ 39 条复合拆解 |
| 　└ 其中 `NO-TARGET`（zh 保留英文目标） | **29** | 补登概念属 `concepts.tsv` 变更，超本任务边界 |
| 其中非占位 zh | **107** | 26 条 `GB/T-4960.9` + 81 条 `internal:dict-improvements` |
| w3 en 行来源 | **782** `IAEA-safety-glossary` + **72** `ITER-glossary` | 与 evidence 来源一一对应 |
| w3 `evidence.tsv` 行 | **854** | 每 id 恰好 1 条 |
| w3 空 `quote` | **854 / 854** | 100% 为空 |
| 全库非 w3 空 `quote` | **1040** | 本任务不修；构成 `--mode evidence` 全库跑必红的原因（G3） |
| w3 evidence 来源 | **782** `IAEA-Safety-Glossary-2018`（裸名）+ **72** ITER URL | 裸名无法做 URL 探测 |
| evidence 去重后唯一 URL 数 | **基线 1 → 回填后 2** | 基线仅 72 条 ITER 行走 URL（782 条 IAEA 为裸名，无法探测）⇒ T0.2 RED 实测 `probes=1`；T1.6 回填后 IAEA+ITER 两个 ⇒ `probes=2`（B5） |
| 全库非 w3 `corresponding to` 套话变体 | **99** | 本任务不修，登记为已知限制（C4） |
| `registry_batch_verify.py --self-test` | **19/24，exit 1** | 修 T0.1 后 24/24；加 evidence 模式断言后 27/27 |
| `pipeline.validate_registry` | **exit 0** | 3076 concepts / 10249 aliases / 3203 evidence / 6152 definitions |
| `pytest -q` | **exit 0**（186 tests） | 执行前基线 |
| `registry_row_audit.py --audit --expect-clean-all` | **exit 0** | 结构门禁基线 |
| IAEA 官方 PDF URL | **200**（浏览器 UA） | `https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf`；默认 Python UA 会 403，必须带 UA |
| ITER glossary URL | **200** | `https://www.iter.org/fusion-glossary` |
| `CHANGELOG.md` 现状 | 第 81 行写「`--self-test` 实测 19/24，漂移由 PM 5072 承接」 | 收尾必须改正为 27/27（§2 第 4 个声明修改文件） |

## 1. 需求分解（CoT Stage 1）

```text
REQUIREMENT
  747 行 w3 zh 释义仍为占位（431 定义 + 316 交叉引用，其中 16 条 en 被下一条目正文污染）；
  854 条 w3 evidence quote 为空；self-test 19/24；
  W3a「依据可核验」判据在 names 模式空转。
↓
CONSTRAINTS
  只允许改 terms/registry/definitions.tsv、terms/registry/evidence.tsv、
  scripts/registry_batch_verify.py、CHANGELOG.md；不得改 concepts 的 preferred_zh/category；
  不得改 pipeline/；不得改父任务 T-4973；每批独立 commit 带 #T-5072；
  任何出处必须可追溯到仓内已有来源或已核验 URL，禁止编造 URL/引文/释义/交叉引用目标。
↓
BOUNDARY
  IN: 431 条 zh 翻译；316 条交叉引用的 见-form 补齐 + 68 条台账登记；
      854 quote + URL；evidence 验收模式（27/27 self-test）；分批 RED/GREEN 证据；独立抽检；
      CHANGELOG 两条计数更正。
  OUT: 854 个中文名（已完成，保持不动）；非 w3 的 303 条 en 短定义 / 1040 条空 quote /
       99 条 corresponding-to 变体；107 条非占位 zh；concepts/pipeline/父计划/命名基线裁决。
```

### 验收总表（A1a / A1b / A1c / A2–A5，全部二元）

| ID | 判据 | 验证方式（可执行） | 失败即 |
|---|---|---|---|
| **A1a** | w3 854 条 zh 行占位计数 = 0 | T3.1 Python 断言 `w3_zh=854 placeholder=0` | 签收失败 |
| **A1b** | 431 条 `DEFINITION`：有 CJK、无占位标记、数字/缩写多重集与 en 相等、`source = translated:*` | 附录 B applier 逐批 `--check-only`（T2.01–T2.30）+ T3.2 抽检 | 该批 FAIL，回滚重做 |
| **A1c** | 316 条 `CROSS_REF` 族：zh 匹配 `^见 .+。$`、无 `[]!;`；287 条目标 ∈ `concepts.preferred_zh`；29 条 ∈ 附录 C `NO-TARGET` 台账 | T2.31 / T3.1 Python 断言 `crossref_ok=316`、`no_target_registered=29` | 该批 FAIL，回滚重做 |
| **A2** | w3 每 id ≥1 条非空 quote；`--mode evidence --check-urls` exit 0；`probes=2` | T1.6 / T3.1 命令 + `grep -o 'probes=[0-9]*'` | 签收失败 |
| **A3** | `registry_batch_verify.py --self-test` **27/27**，exit 0 | T3.1 `grep -c '27/27 assertions passed'` = 1 | 签收失败 |
| **A4** | `validate_registry` / `pytest` / `row_audit --expect-clean-all` / `ruff format --check` + `ruff check` 全 exit 0 | T3.1 V4–V7 | 签收失败 |
| **A5** | 独立 `acceptance-verifier` 抽检 75 zh + 86 evidence，FAIL = 0 | T3.2 | 进 T3.3 返工（≤2 轮） |

## 2. 范围与修改边界

| 允许修改 | 用途 | 禁止 |
|---|---|---|
| `terms/registry/definitions.tsv` | 仅替换 747 条 w3 zh 行的 `definition` 与 `source`（431 翻译 + 316 交叉引用） | 不改 en 行；不改 concept_id/lang/行序；不改 107 条非占位 zh；不把污染文本写进 zh |
| `terms/registry/evidence.tsv` | 仅更新 854 条 w3 行的 `source` / `quote` / `added_by` / `added_at` | 不改非 w3 行；不改行序；quote 必须与 definitions en 文本归一化后逐字相同 |
| `scripts/registry_batch_verify.py` | 修复 self-test 漂移、增加 evidence 模式（+3 断言至 27）、URL UA、`translated:` 白名单、URL 探测去重 | 不改其他 rule 语义；不改 names/definitions/allowlist 现有判据；不写入任何数据 |
| `CHANGELOG.md` | **仅**更正第 81 行 self-test 计数（19/24 → 27/27）与第 82 行 W3a 承接状态（PM 5072 完成） | 不改其他条目；不新建版本号；不改 CalVer 段 |
| `.github/plans/5072-w3a-evidence-definition-backfill.md` | 本计划 + Execution Log | 不改父计划 `.github/plans/terminology-coverage-and-definition-quality.md`；不新建其他仓内文档 |

**提交纪律**：每个数据批次只 `git add` 声明的数据文件；`git diff --stat` 不得出现 `concepts.tsv`、`aliases.tsv`、`pipeline/`、`*.html`。计划日志单独用 `docs(plan)` 提交，不夹带数据。CHANGELOG 只在 T3.4 收尾提交，与计划文件同批 `docs:` 提交。

## 3. 核心设计决策（CoT Stage 3）

### D1 — evidence quote 用「仓内已导入的 en 释义 + 上游 raw 对照」，不新写引文

- **选择**：`quote` 取该 id 现有 `definitions.tsv` 的 en 文本（该文本由 `import_approved_terms.py` 从上游 diff/raw 导入），并逐条用 `artifacts/terminology_sources/{iaea_safety_glossary_raw.tsv,iter_glossary_raw.tsv}` 做归一化对照；归一化后必须**逐字命中** raw（854/854），不命中即中止，不猜。
- **备选**：让 LLM 从 PDF 重新摘录。**拒绝**：会引入新的 OCR/摘录误差，且无法逐条审计。
- **归一化定义（唯一口径）**：`re.sub(r"[\ue000-\uf8ff]", " ", text)` 去掉 raw 中的私用区字形 → `\u2022`/`\x03`/`\uf069` 换空格 → `re.sub(r"\s+", " ", ...).strip()`。**禁止** `difflib` 近似匹配、禁止 `ratio >= 0.98` 兜底、禁止「人工逐条确认例外」（CT B4）。
- **G1 — quote 的证据语义边界**：quote 与 definitions 的 en 文本**逐字相同**，即它是「重复」而不是独立新证据。evidence 行只承担两件事：① 可点击的 source URL；② 可回到 raw 的逐字锚点。**不得**把 evidence 表述为「独立第二来源」，也不得据此声称交叉验证。
- **来源 URL**：IAEA 782 条统一 `https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf`；ITER 72 条保持 `https://www.iter.org/fusion-glossary`。两者均已实测 200。

### D2 — zh 释义用「对现有 en 释义的忠实翻译」，并用 `translated:` 明示派生关系

- **选择**：只翻译 en 释义；不引入 en 中没有的数字、缩写、引用、例子、判断。`source` 写 `translated:IAEA-safety-glossary` 或 `translated:ITER-glossary`，明确「中文是译文，不是独立中文权威来源」。
- **备选 A**：把 source 写成 `IAEA-safety-glossary`。**拒绝**：会让读者误以为中文释义直接来自英文原书。
- **备选 B**：继续保留 `internal:dict-improvements`。**拒绝**：现有 gate 不认该来源，且无法表达译文派生。
- **备选 C**：调用外部翻译 API。**不做**：本任务不新增网络依赖；由执行 agent 逐批翻译，配合机械校验 + 独立抽检。
- **与 `registry_batch_verify` 的兼容**：在 `DEF_SOURCE_WHITELIST` 增加 `translated:IAEA-safety-glossary`、`translated:ITER-glossary`，只影响 definitions 模式的来源白名单，不放宽长度/占位/语言判据。

### D3 — 「依据可核验」判据改为新的 `--mode evidence`

- **选择**：新增 `--mode evidence`：对每个 id 要求至少一条 `quote.strip()` 非空；`--check-urls` 时每条带 quote 的行 `source` 必须是 http(s) 且探测 200。`--no-net` 只打印 SKIPPED-NET，不能用于最终验收。
- **为什么不在 names 模式硬塞 URL**：names 模式不读 evidence，语义不匹配；新增独立模式更窄、更可失败。
- **`http_status` 加浏览器 UA**：IAEA 官方 PDF 对默认 `Python-urllib` 返回 403，对浏览器 UA 返回 200；不加 UA 会让真实 URL 被误判失败。
- **G3 — 强制 `--ids-file`**：`--mode evidence` 必须始终配 `--ids-file`；全库裸跑必红（1040 条非 w3 空 quote），不得把全库红色当成本任务失败，也不得用全库裸跑替代 w3 验收。模式实现中无 `--ids-file` 时直接 `SystemExit`，防止误用。

### D4 — 固定 25 条/批 + 单文件串行，避免合并冲突

- 747 条 zh：30 批（29×25 + 22），每批 ≤30 min（按行型加权的实测估算见 §7 Phase 2 批次表）。
- 854 条 quote：5 批（171×4 + 170），每批只改 `evidence.tsv`。
- 所有批次对同一 TSV 串行执行；不并行写同一文件。脚本任务与数据任务可先后串行，换取可回滚性。
- **G2 — 批次粒度不对称说明**：evidence 批 171 条/commit 是**脚本化**作业（同一条命令 + 同一机械校验，人工只读输出），单批 ~15 min；zh 批 25 条/commit 是**判断型**作业（逐条翻译 / 逐条交叉引用裁定，每条都要看 en 原文），单批 20–30 min。两者按「单 commit 的墙钟 ≤30 min」而非「行数相同」对齐。

### D5 — 316 条 CROSS_REF 的裁定规则（用户裁决 方案甲，2026-10-31）

- **选择**：`zh = 见 <目标 preferred_zh>。`。目标解析顺序：① 从 en 首句 `See (.+?)\.` 取出目标文本；② 大小写不敏感、去 `(1)` 形态后缀、压空白后，到 `concepts.tsv` 的 `preferred_en` 精确匹配，取该 concept 的**非空** `preferred_zh`；③ 直接匹配失败时，按复合形态拆解（`A: B` 取 `B`、再取 `A`；再去掉 `(...)` 括注）后重试；④ 仍失败 → 进入附录 C 台账逐条登记，**不得**自行翻译成中文短语。
- **为何不用「翻译 See X」**：交叉引用的语义是"去那个条目看"，翻译会造出一个 concepts.tsv 中不存在的术语名，读者无法对齐；方案甲让 zh 直接指向已裁决的 `preferred_zh`，可机械校验。
- **反例（禁止）**：把 `See waste container.` 译成 `见 废物容器。`——`废物容器` 不在 concepts.tsv 的 `preferred_zh` 集合内，属静默翻译，A1c 必须 FAIL。
- **污染行（CORRUPT）**：目标只取 **en 首句**的 `See X.` 部分，首句之后的残余（下一条目的正文）**一律丢弃**；zh 不得包含 `[`、`]`、`!`、`;` 或任何残余片段。16 条逐条登记于附录 C.1（含污染形态描述）。

### D6 — 行型三分 + 机械断言，防止「747 一律翻译」

- **行型定义（唯一口径，执行脚本必须逐字实现）**：
  - `EN_SEE = re.compile(r"^See (.+?)\.$")` → 命中即交叉引用族；
  - `BODY = re.compile(r"^See (.+?)\.\s*(\S.*)$")` → 在 `EN_SEE` 基础上还有首句之后的残余 → `CORRUPT`；
  - `EN_SEE` 命中且 `BODY` 不命中 → `CROSS_REF`；
  - 都不命中 → `DEFINITION`。
- **基线计数（必须整体成立）**：`DEFINITION 431 / CROSS_REF 300 / CORRUPT 16`；合计 747；交叉引用族 300+16=316。每批 step 0 打印本批三类计数，T2.31 断言全过程累计仍为 431/300/16。
- **为什么必须三分**：CT 实测 316/747 的 en 是 `See X.`（全库 352 条），若按「翻译 en」处理会产出 316 条 `见 某种中文翻译。` 的伪术语；16 条更会把下一条目的正文翻进 zh，造成数据污染。

## 4. 假设清单（CoT Stage 2）

1. `[假设]` `artifacts/terminology_sources/*.tsv` 是当前数据的上游快照，且在任务期间不被修改。**若被改**：T1.0 的 raw 对照会失败并中止；此时先 `git status` 确认，不自行替换来源。
2. `[假设]` `w3.ids`、747 条占位集合、431/300/16 行型分布、287/29 解析分布、16 条污染集合在基线 `b0bef07` 上稳定。**若漂移**：T0.0 重测并更新 `BASE`，T0.3 重新生成 rowtypes 与附录 C 台账；不得沿用旧批次范围或旧台账。
3. `[假设]` `translated:` 前缀只被本仓库的 `registry_batch_verify` 使用，不影响 `pipeline/` 与导出链。已 grep 确认 `pipeline/` 不校验 definitions 的 source 枚举。
4. `[假设]` IAEA PDF URL 在验收时仍返回 200（浏览器 UA）。**若失效**：只在 T3.1 记录 `[URL-FAIL]` 并暂停，不用 `--no-net` 冒充通过；换用 IAEA 官方稳定镜像前必须重新核验 200。
5. `[假设]` 431 条翻译可由执行 agent 在 30 批内完成；含 25 条定义的批次（T2.01）为 30 min 上限批次，超时即按 13+12 拆批并各自独立 commit。
6. `[假设]` 303 条 en「See X」短定义中的非占位部分（即不在 747 内的 352−316=36 条 w3 短定义 + 全库其余）是上游原文，不是占位；本任务不修。若用户要求 `--mode definitions` 全绿，需另立任务，不能在本任务伪造扩展。
7. `[假设]` 287 条可机械解析的交叉引用目标在 `concepts.tsv` 中保持非空 `preferred_zh`；若某目标在执行时变为空或消失，该行降级为附录 C 登记行（NO-TARGET），**不得**改用翻译兜底。
8. `[假设]` `CHANGELOG.md` 第 81/82 行在任务期间不被他人改写。**若被改**：T3.4 只按 `git diff` 定位当时仍含 `19/24` 与 `PM 5072 承接` 的行做更正；找不到则记录 `[CHANGELOG-DRIFT]` 并跳过，不新增条目。

## 5. 风险与对策

| # | 风险 | 影响 | 对策 |
|---|---|---|---|
| R1 | 翻译时添加 en 没有的事实/数字 | 释义不可审计 | 机械检查数字/缩写集合；独立 10% 抽检；任何新增数字即 FAIL |
| R2 | 747 条批量处理耗时超预算 | 任务拖长 | 25 条/批，30 批；每批 step 0 打印行型计数；每批 15 min checkpoint；>30 min 拆 13+12 |
| R3 | quote 与 raw 不逐字相同 | 伪造出处风险 | 归一化（含私用区字形剥离）后必须**完全相等**；不相等即 `SystemExit`；无近似兜底 |
| R4 | IAEA URL 对 urllib 403 | 最终 URL 检查误红 | `http_status` 带浏览器 UA；T0.2 用真实 URL 做一次 200 验证 |
| R5 | 批次提交夹带 `iaea_fusion.html` 或其他文件 | 污染提交 | 每批显式 `git add <file>`；commit 前 `git diff --cached --stat` 只含声明文件 |
| R6 | self-test 修复把真实数据当夹具改坏 | 数据污染 | 只在 `tempfile.mkdtemp` 副本中重建缺陷；真实 registry 永不写入；T0.1 验收后 `git diff --stat` 仅脚本 |
| R7 | 批次中断/会话切换 | 重复或漏批 | T0.3 的 `/tmp` manifest 固定基线；每批先 `git log --grep` 查重；脚本幂等（同 id 重写同值） |
| R8 | `translated:` 来源被下游误读 | provenance 争议 | 在计划与 commit message 明示「译文派生」；source 前缀可 grep 审计 |
| R9 | 独立抽检发现问题 | 返工 | T3.3 条件任务，最多 2 轮；FAIL 批次回滚该批 commit 后重做 |
| R10 | 交叉引用被「翻译」成 concepts.tsv 不存在的术语 | 伪术语入库 | A1c 机械断言：zh 的 `见 X。` 中 X 必须 ∈ concepts.preferred_zh（`见`-form 行）；不满足即该批 FAIL |
| R11 | 污染行把下一条目正文写进 zh | 数据污染且难回滚 | 附录 C.1 逐条登记；A1c 断言 zh 不含 `[`/`]`/`!`/`;`；applier 对 CORRUPT 行只取首句目标 |
| R12 | CHANGELOG 收尾忘记更正，留下 19/24 | 文档与实测不一致 | §2 声明 CHANGELOG 为第 4 个修改文件；T3.4 硬性断言 `grep -c '19/24' CHANGELOG.md` = 0 且含 `27/27` |
| R13 | 全库跑 `--mode evidence` 被误当验收 | 假红/假绿 | G3：模式强制 `--ids-file`；V3 固定传 w3.ids |

## 6. 已知限制（不在本任务验收口径内）

1. **`--mode definitions` 仍会红，且本任务不承诺全绿**。残余红色来源逐项列明：
   - **303/352 条 en 定义 <40 字符**：`See X.` 类交叉引用属合法上游文本，非占位；本任务按方案甲改写其 zh，但 en 长度不变，仍触发 `def_too_short`。
   - **316 条 zh < `MIN_ZH_CHARS`（12 CJK 字符）**：方案甲的 `见 <目标>。` 天然短于 12 个 CJK 字符，全部 316 条交叉引用行都会持续触发该判据。这是裁定带来的**预期**残红，不是回归。
   - **81 条 `internal:dict-improvements`**：非占位 zh，来源不在白名单，本任务不改。
   - **16 条 CORRUPT en**：污染存在于 **en 行**，本任务不改 en；zh 已隔离污染，但 en 侧仍是不合格文本。
   - **99 条非 w3 `corresponding to` 套话变体**：本任务范围外，未修。
2. **self-test 27/27 不代表 evidence 判据已完备**：27 条断言只覆盖「空 quote / 裸名 source / 404 URL / names / definitions / allowlist」的已知失败面；99 条非 w3 套话变体与 1040 条非 w3 空 quote 都不在断言范围内。**24/24（或 27/27）不等于全库干净**。
3. **29 条 `NO-TARGET` 交叉引用**（附录 C.2）：目标在 `concepts.tsv` 中无对应非空 `preferred_zh`（概念不存在，或概念存在但 `preferred_zh` 为空，如 `radiation-safety → safety`）。按用户裁决逐条登记并写 `见 <英文目标>。`（英文原样保留、可搜索、不伪造中文名）；补登概念属 `concepts.tsv` 变更，超出本任务边界，另案处理。
4. **`w3-name-conflicts.tsv` 的 physical-sputtering 冲突**：父任务遗留，另案裁决，不在本任务。
5. **1040 条非 w3 空 quote**：`--mode evidence` 裸跑必红；本任务只对 854 条 w3 负责（G3）。
6. **上游快照里的 en 定义有 284 条是「章节级」长文本**（T1.0 实测，`definitions.tsv` en 列，基线 `3034dce`）：
   - 长度分布：`>300` 字符 **284** 条 / `>1000` **78** / `>2000` **26** / `>3000` **13** / `>5000` **4**；最长 `assessment` **7621** 字符（IAEA 整节），中位数仅 139。
   - 影响：这些 id 的 evidence quote 继承同一段文本，因而是**章节级**引文（含相邻条目），不是条目级单句。它满足 A2（非空 quote + URL 200 + 与 raw 逐字相等），但人工可读性差。
   - **不截断的理由**：截断会破坏「归一化后与 raw 逐字相等」这一唯一机械校验口径（B4），并把启发式切片规则引入 284 行；修正 en 定义本身属 `definitions.tsv` en 列改动，超出本任务范围。
   - 后续建议：另立任务把章节级 en 定义切成条目级引文（并同步 zh），本任务只保证「引文可核验」。
7. **`plant-states` 等 1 条 en 定义含 `\x03` 控制符**：quote 落表时统一走 `norm()`（控制符→空格），因此 evidence 侧不再有控制符；`definitions.tsv` en 列本身的控制符未修（超范围）。

## 7. 执行计划

> **任务总量（rev 2）**：**47 个 Task**（Phase 0: 4；Phase 1: 7；Phase 2: 32；Phase 3: 4），另 T3.3 为条件返工（≤2 轮）。
> **总墙钟估算**：Phase 0 ≈ 85 min；Phase 1 ≈ 100 min；Phase 2 ≈ 746 min（按行型加权，见批次表）；Phase 3 ≈ 90 min；合计 ≈ **1021 min ≈ 17 h**（不含 T3.3）。
> **commit 估算**：T0.1 + T0.2（2）+ evidence 5 + definitions 30 + 收尾 docs 1 = **38 个 commit**。
> **串行约束**：全部 Phase 2 批次对 `terms/registry/definitions.tsv` 严格串行；Phase 1 的 evidence 批次对 `terms/registry/evidence.tsv` 严格串行。

### Phase 0: 基线与门禁加固（必须先完成）

#### Task T0.0 — 基线重测与 RED 证据（10 min）

- **依赖**: 无
- **frontier**: 是
- **执行者**: Dev Orchestrator
- **预估墙钟**: 10 min
- **修改内容**: 无仓内数据修改；只写 `/tmp/opencode/t5072/` 工作目录与计划 Execution Log。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  mkdir -p /tmp/opencode/t5072
  git rev-parse HEAD | tee /tmp/opencode/t5072/BASE
  git status --porcelain=v1 | tee /tmp/opencode/t5072/git-status-baseline.txt
  .venv/bin/python scripts/registry_batch_verify.py --self-test \
    > /tmp/opencode/t5072/red-selftest.txt 2>&1; echo "selftest_exit=$?"
  .venv/bin/python -m pipeline.validate_registry \
    > /tmp/opencode/t5072/baseline-validate.txt 2>&1; echo "validate_exit=$?"
  .venv/bin/python -m pytest -q \
    > /tmp/opencode/t5072/baseline-pytest.txt 2>&1; echo "pytest_exit=$?"
  ```
- **验收标准**:
  - ✅ `[T-A]` `grep -q '19/24 assertions passed' /tmp/opencode/t5072/red-selftest.txt` 且 `grep -q 'FAILED'` → exit 0（RED 存在）
  - ✅ `[T-A]` `grep -q 'registry OK' /tmp/opencode/t5072/baseline-validate.txt` → exit 0
  - ✅ `[T-B]` `wc -l < /tmp/opencode/t5072/BASE` = 1 且 `wc -l < .github/plans/t4973-batches/w3.ids` = 854
  - ✅ `[T-A]` `git status --porcelain=v1 \| grep -v '^?? iaea_fusion.html$' \| wc -l` = 0
- **能失败证明**: 若 self-test 已是 24/24 或 27/27，则 RED 文件不含 `19/24`，本条失败，说明基线已变化，必须先更新计划。
- **边界**: 不修改任何 `terms/`、`scripts/` 文件；不 `git add`。

#### Task T0.1 — 修复 self-test 漂移到 24/24（20 min）

- **依赖**: T0.0
- **frontier**: 是
- **执行者**: Simulation Builder / Dev Orchestrator
- **预估墙钟**: 20 min
- **修改文件**: `scripts/registry_batch_verify.py`（仅此文件）
- **修改内容（精确锚点）**:
  1. `_build_restored_defect_corpus()` 中，`adjoint-flux` 的恢复逻辑从「只改 zh」改为「同时改 en」：
     - en 行 `definition` 写回 `Fusion/nuclear engineering term referring to 'adjoint flux' in technical context.`
     - en 行 `source` 写回 `internal:dict-improvements`（触发 `def_source_unknown`）
     - zh 行继续写回 `聚变/核工程术语，指“en”这一技术概念。`
  2. `_build_restored_defect_corpus()` 末尾复制 `allowlist_zh.txt` 后，从副本中删除值为 `极向场电源` 的行（只为让 `allow_zh_not_listed` 有可失败样本；不碰真实 `terms/allowlist_zh.txt`）。
  3. `SELF_TEST_RESTORED_CASES` 增加索引 `4`（`preferred_zh absent from allowlist_zh.txt` 样本也改用 restored corpus）。
  4. **临时目录与清理边界（C6）**：把 `tempfile.mkdtemp()` 的创建与 `try/finally` 中的 `shutil.rmtree(...)` 清理**整体上移到 rule-level 段与 mode verdict 段之前**，两段共用同一个 `restored` 副本（全函数只建 1 份、只清 1 次）；禁止在子段落内各自 `mkdtemp`。rule-level 段用 `restored.definitions()` 取 `adjoint_en`，mode verdict 段复用同一 `restored`；异常路径也必须走 `finally` 删除，不得在 `/tmp` 留残副本。
  5. 不改任何 rule 的判定逻辑；**本任务断言数保持 24 不变**（`evidence` 模式新增的 3 条断言在 T0.2 加入，届时总数变 27）。
- **验收标准**:
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --self-test > /tmp/opencode/t5072/green-selftest-t01.txt 2>&1; echo $?` → `0`
  - ✅ `[T-A]` `grep -q '24/24 assertions passed' /tmp/opencode/t5072/green-selftest-t01.txt`
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/w3.ids --expect 854` → exit 0（回归）
  - ✅ `[T-B]` 泄漏检查：`.venv/bin/python -c "import glob;print(len(glob.glob('/tmp/*/terms/registry')))"` 在两次 self-test 前后差值 = 0（单个副本、`finally` 清理干净）
  - ✅ `[T-C]` `git diff --stat` 只含 `scripts/registry_batch_verify.py`
- **能失败证明（实现回退法，CT B3 实测口径）**:
  - 把 `SELF_TEST_RESTORED_CASES` 中的 `3` 删掉 → **19/24**（丢 1 条 verdict + 4 条 token 断言）；
  - 把 `adjoint-flux` 的 en 恢复删除 → **21/24**（丢 3 条）；
  - 两者都不是 22/24 或 19/24 的旧口径，执行时以实测输出为准，若数字不符先停下核对锚点。
- **提交**: `git add scripts/registry_batch_verify.py && git commit -m 'fix(scripts): re-anchor registry_batch_verify self-test drift (#T-5072)'`
- **边界**: 不得修改真实 `terms/` 数据；不得改 `SELF_TEST_CASES` 的期望 token 或行号锚点。

#### Task T0.2 — 增加 evidence 验收模式 + URL UA + translated 白名单 + 3 条断言（30 min）

- **依赖**: T0.1（同一文件，避免合并冲突）
- **frontier**: 否
- **执行者**: Simulation Builder / Dev Orchestrator
- **预估墙钟**: 30 min（模式实现 20 min + 3 条新断言与去重 10 min）
- **修改文件**: `scripts/registry_batch_verify.py`
- **修改内容**:
  1. `MODES` 改为 `("definitions", "names", "allowlist", "evidence")`。
  2. `Corpus.__init__` 增加 `self.evidence_path = root / "terms" / "registry" / "evidence.tsv"` 和 `self._evidence = None`；新增 `Corpus.evidence()` 返回 `{concept_id: [(lineno, source, quote), ...]}`。
  3. 新增 `check_evidence(corpus, ids, *, check_urls=False, no_net=False, url_probe=None, out=print)`：
     - 无 evidence 行 → `Violation("evidence_missing", ...)`
     - 无任何 `quote.strip()` 非空的行 → `Violation("evidence_quote_empty", ...)`
     - `--check-urls` 时，每条有 quote 的行 source 必须是 `http(s)://`；否则 `evidence_source_not_url`
     - URL 探测 `status != 200` → `evidence_url_status`
     - `--no-net` 打印 `SKIPPED-NET: ...` 且不探测（不得作为最终验收）
     - **URL 去重（B5）**：探测前先 `unique = sorted({source for ...})`，用 `cache: dict[str, int]` 缓存结果；同一 URL 只调 `url_probe` 一次；函数返回/打印 `probes=<len(unique)>`，并断言 `probe_calls == len(unique)`。
  4. `http_status()` 使用 `urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; fusion-terms/1.0)"})`；保留 15s 超时。`url_probe` 参数必须可注入（self-test 用，禁止真实网络）。
  5. **G3 强制 `--ids-file`**：`elif args.mode == "evidence"` 分支在 `ids_file is None` 时 `SystemExit("--mode evidence requires --ids-file")`。
  6. `DEF_SOURCE_WHITELIST` 增加 `"translated:IAEA-safety-glossary"`、`"translated:ITER-glossary"`。
  7. `main()` 的 `needed` 表增加 `elif args.mode == "evidence": needed = [corpus.evidence_path]`；dispatch 增加 `elif args.mode == "evidence": violations.extend(check_evidence(...))`。
  8. **新增 3 条 self-test 断言（24 → 27，B2）**，全部在 `run_self_test()` 内、用注入的 `url_probe` 假实现，**不触网**：
     - `evidence_quote_empty`：fixture 中把某 id 的 quote 置空 → 必须命中该 rule；
     - `evidence_source_not_url`：fixture 中把 source 改为裸名 `IAEA-Safety-Glossary-2018` + `--check-urls` → 必须命中该 rule；
     - `evidence_url_status`：`url_probe` 注入返回 404 → 必须命中该 rule；
     - 另断言 `probe_calls == len(unique_urls)`（去重生效），作为上述 3 条的公共前置。
  9. 更新模块 docstring / argparse 描述中的 modes 说明与断言计数。
- **验收标准**:
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --self-test` → exit 0 且输出 `27/27 assertions passed`
  - ✅ `[T-A]` `.venv/bin/python scripts/registry_batch_verify.py --mode evidence --ids-file .github/plans/t4973-batches/w3.ids --expect 854 --check-urls > /tmp/opencode/t5072/red-evidence.txt 2>&1; echo $?` → `1`（RED：当前 854 条空 quote）
  - ✅ `[T-B]` `grep -c 'evidence_quote_empty' /tmp/opencode/t5072/red-evidence.txt` = `854`
  - ✅ `[T-B]` **probes 去重**：`grep -o 'probes=[0-9]*' /tmp/opencode/t5072/red-evidence.txt` = `probes=1`（基线 854 行中只有 72 条 ITER 行是 URL，782 条 IAEA 行为裸名 ⇒ 唯一 URL 1 个，不是 854；回填后 T1.6 要求 `probes=2`）
  - ✅ `[T-A]` 无 `--ids-file` 时：`.venv/bin/python scripts/registry_batch_verify.py --mode evidence` → exit ≠ 0 且 stderr 含 `requires --ids-file`（G3）
  - ✅ `[T-B]` `python3 - <<'PY'` 探针：`http_status(IAEA_URL)==200` 且 `http_status(ITER_URL)==200`（真实网络；失败则记录 `[URL-FAIL]`，不得用 `--no-net` 通过）
  - ✅ `[T-A]` `.venv/bin/ruff format --check scripts/registry_batch_verify.py` 与 `.venv/bin/ruff check scripts/registry_batch_verify.py` → exit 0
- **能失败证明（变异法）**:
  - 给任一 evidence 行填入非空 quote 并把 source 改成 `IAEA-Safety-Glossary-2018`（裸名），`--mode evidence --check-urls` 必须报 `evidence_source_not_url`；
  - 把 URL 改成 `https://example.org/missing`，`url_probe` 返回 404，必须报 `evidence_url_status`；
  - 删掉去重逻辑（对每行都调 `url_probe`）→ `probe_calls == len(unique_urls)` 断言失败并新增 `evidence_probe_dedup`；基线实测同一 ITER URL 被探测 **72** 次（`probes=72`），回填后为 `probes=854`。
- **提交**: `git add scripts/registry_batch_verify.py && git commit -m 'feat(scripts): add evidence acceptance mode with 3 self-test assertions and dedup URL probe (#T-5072)'`
- **边界**: 不改 `check_names` / `check_definitions` / `check_allowlist` 的现有判定；不改 `SELF_TEST_CASES` 既有 24 条的期望值。

#### Task T0.3 — 行型三分 manifest 与防漂移（20 min）

- **依赖**: T0.0
- **frontier**: 是
- **执行者**: Dev Orchestrator
- **预估墙钟**: 20 min（比原计划 +5 min：新增行型分类与交叉引用解析清单）
- **修改内容**: 只写 `/tmp/opencode/t5072/`；不修改仓内文件。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  BASE=$(cat /tmp/opencode/t5072/BASE)
  git show "$BASE:.github/plans/t4973-batches/w3.ids" > /tmp/opencode/t5072/w3.ids
  git show "$BASE:terms/registry/definitions.tsv" > /tmp/opencode/t5072/definitions.baseline.tsv
  git show "$BASE:terms/registry/evidence.tsv" > /tmp/opencode/t5072/evidence.baseline.tsv
  python3 - <<'PY'
  import csv, re
  ids=[l.strip() for l in open('/tmp/opencode/t5072/w3.ids',encoding='utf-8') if l.strip() and not l.startswith('#')]
  idset=set(ids)
  rows=[r for r in csv.reader(open('/tmp/opencode/t5072/definitions.baseline.tsv',encoding='utf-8'),delimiter='\t')
        if r and not r[0].startswith('#') and r[0] in idset]
  en={r[0]:r[2] for r in rows if r[1]=='en'}
  ph=[c for c in ids if any(r[0]==c and r[1]=='zh' and '对应英文' in r[2] for r in rows)]
  EN_SEE=re.compile(r'^See (.+?)\.$'); BODY=re.compile(r'^See (.+?)\.\s*(\S.*)$')
  def classify(cid):
      t=en[cid].strip()
      if not EN_SEE.match(t): return 'DEFINITION',''
      m=BODY.match(t)
      return ('CORRUPT', m.group(2)) if m else ('CROSS_REF','')
  with open('/tmp/opencode/t5072/rowtypes.tsv','w',encoding='utf-8') as fh, \
       open('/tmp/opencode/t5072/w3_placeholder.ids','w',encoding='utf-8') as pf:
      for cid in ph:
          kind, rem = classify(cid)
          fh.write(f"{cid}\t{kind}\t{en[cid].strip()}\t{rem}\n")
          pf.write(cid+'\n')
  kinds=[classify(c)[0] for c in ph]
  print('ids',len(ids),'placeholder',len(ph),
        'DEFINITION',kinds.count('DEFINITION'),'CROSS_REF',kinds.count('CROSS_REF'),'CORRUPT',kinds.count('CORRUPT'))
  assert len(ids)==854 and len(ph)==747
  assert (kinds.count('DEFINITION'),kinds.count('CROSS_REF'),kinds.count('CORRUPT'))==(431,300,16)
  PY
  sha256sum /tmp/opencode/t5072/w3.ids /tmp/opencode/t5072/w3_placeholder.ids \
            /tmp/opencode/t5072/rowtypes.tsv | tee /tmp/opencode/t5072/manifests.sha256
  ```
- **交叉引用解析清单（同一步产出，供附录 C 核对）**：
  ```bash
  python3 - <<'PY'
  import csv, re
  def nk(t): return re.sub(r'\s+',' ',re.sub(r'\(\d+\)','',t)).strip().lower()
  conc={}
  for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t'):
      if r and not r[0].startswith('#') and len(r)>=4 and r[3].strip():
          conc.setdefault(nk(r[3]),[]).append((r[0],r[2]))
  def parts(t):
      p=[t]
      if ':' in t: p += [t.split(':',1)[1].strip(), t.split(':',1)[0].strip()]
      p.append(re.sub(r'\(.*?\)','',t).strip())
      return p
  seen=direct=0; ledger=[]
  for line in open('/tmp/opencode/t5072/rowtypes.tsv',encoding='utf-8'):
      cid,kind,en,rem=line.rstrip('\n').split('\t')
      if kind=='DEFINITION': continue
      seen+=1
      if kind=='CORRUPT':
          target=re.match(r'^See (.+?)\.\s*\S', en.strip()).group(1)   # 只取首句目标，丢弃污染残余
      else:
          target=re.match(r'^See (.+?)\.$', en.strip()).group(1)
      hit=[x for x in conc.get(nk(target),[]) if x[1].strip()]
      if hit and kind=='CROSS_REF':
          direct+=1; continue
      for p in parts(target):
          if conc.get(nk(p)) and any(z.strip() for _,z in conc[nk(p)]): hit=[x for x in conc[nk(p)] if x[1].strip()]; break
      ledger.append((cid,kind,target,hit[0][1] if hit else 'NO-TARGET'))
  open('/tmp/opencode/t5072/crossref_resolution.tsv','w',encoding='utf-8').write(
      ''.join(f'{c}\t{k}\t{t}\t{z}\n' for c,k,t,z in ledger))
  print('croref_family',seen,'direct',direct,'ledger',len(ledger),
        'no_target',sum(1 for *_,z in ledger if z=='NO-TARGET'))
  assert seen==316 and direct==248 and len(ledger)==68
  assert sum(1 for *_,z in ledger if z=='NO-TARGET')==29
  PY
  ```
- **验收标准**:
  - ✅ `[T-A]` `wc -l /tmp/opencode/t5072/w3.ids` = 854
  - ✅ `[T-A]` `wc -l /tmp/opencode/t5072/w3_placeholder.ids` = 747
  - ✅ `[T-B]` rowtypes 输出 `DEFINITION 431 CROSS_REF 300 CORRUPT 16`（合计 747；交叉引用族 316）
  - ✅ `[T-B]` 解析清单输出 `croref_family 316 direct 248 ledger 68 no_target 29`
  - ✅ `[T-B]` `sha256sum -c /tmp/opencode/t5072/manifests.sha256` → exit 0
  - ✅ `[T-B]` `comm -23 <(sort /tmp/opencode/t5072/w3_placeholder.ids) <(sort /tmp/opencode/t5072/w3.ids) | wc -l` = 0
- **能失败证明**: 把分类器里的 `BODY` 判据删掉 → `CORRUPT` 变 0、`CROSS_REF` 变 316，断言 `(431,300,16)` 立即失败，说明污染行被误并入干净交叉引用。
- **边界**: 不把 `/tmp` 文件提交进仓；不修改 `w3.ids`。

### Phase 1: 854 条 evidence quote 补全（5 批 + 1 次全量）

> **原则**：quote 只取 `definitions.baseline.tsv` 的 en 文本；脚本逐条到 `artifacts/terminology_sources/*_raw.tsv` 做归一化核对，**归一化后必须逐字命中（854/854）**，无法核对即中止。禁止手工编写引文，禁止近似匹配。
> **证据语义（G1）**：quote 与 en 定义文本相同 —— 它是「重复」，evidence 只提供 **source URL + 可回查 raw 的逐字锚点**，不构成独立第二来源。
> **来源 URL**：IAEA → `https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf`；ITER → `https://www.iter.org/fusion-glossary`。**唯一 URL 只有 2 个**，URL 探测按唯一值去重后只跑 2 次。
> **`added_by` / `added_at`**：`t-5072-backfill` / 执行当日 `date -I` 实测值（不得写死 2026-10-30）。

#### Task T1.0 — 落地 backfill 脚本并 dry-run（15 min）

- **依赖**: T0.2, T0.3
- **frontier**: 是
- **执行者**: Simulation Builder
- **预估墙钟**: 15 min
- **修改内容**: 创建 `/tmp/opencode/t5072/backfill_evidence.py`（内容见附录 A）；不改仓内文件。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  mkdir -p /tmp/opencode/t5072/dryrun/terms/registry
  cp /tmp/opencode/t5072/definitions.baseline.tsv /tmp/opencode/t5072/dryrun/terms/registry/definitions.tsv
  cp /tmp/opencode/t5072/evidence.baseline.tsv /tmp/opencode/t5072/dryrun/terms/registry/evidence.tsv
  python3 /tmp/opencode/t5072/backfill_evidence.py \
    --ids-file /tmp/opencode/t5072/w3.ids \
    --definitions /tmp/opencode/t5072/dryrun/terms/registry/definitions.tsv \
    --evidence /tmp/opencode/t5072/dryrun/terms/registry/evidence.tsv \
    --raw-iaea artifacts/terminology_sources/iaea_safety_glossary_raw.tsv \
    --raw-iter artifacts/terminology_sources/iter_glossary_raw.tsv \
    --start 1 --end 0 --added-at "$(date -I)"
  ```
- **验收标准**:
  - ✅ `[T-A]` 上述命令 exit 0，输出 `updated=854 matched_exact=854`
  - ✅ `[T-B]` dry-run 副本中 w3 evidence 非空 quote = 854（Python 断言，命令见 T1.6）
  - ✅ `[T-B]` 854 条 quote 与 raw 归一化后**逐字相等**（脚本内 `matched_exact` 计数 == 854；无 `difflib`、无 `ratio`）
  - ✅ `[T-C]` dry-run 只写 `/tmp/opencode/t5072/dryrun/`，仓内 `git status` 无新增数据改动
- **能失败证明**:
  - 把 `--raw-iaea` 指向不存在文件 → 脚本立即报错；
  - 删掉 `dose-quantities` en 定义 → `missing en definition` 中止；
  - 把 raw 中任一条定义的私用区字形（`\ue000-\uf8ff`）删掉 → 归一化后无法逐字命中，`matched_exact` < 854 → 中止（证明 B4 的 PUA 剥离是必需的，不是装饰）。
- **边界**: 不写仓内 `evidence.tsv`；不修改 raw 源文件；不引入近似匹配兜底。

#### Task T1.1 … T1.5 — evidence 分批落表（每批 12 min）

- **依赖**: T1.0；T1.(k) 依赖 T1.(k-1)（同一文件串行）
- **frontier**: T1.1 是；T1.2–T1.5 否
- **执行者**: Simulation Builder
- **预估墙钟**: 每批 12 min（原 15 min：URL 探测从「每行 1 次」改为「唯一 URL 2 次」后省时）
- **修改文件**: `terms/registry/evidence.tsv`（仅此文件）
- **批次表**（`w3.ids` 行号，1-based，闭区间）:

| Task | start | end | expect | commit suffix |
|---|---:|---:|---:|---|
| T1.1 | 1 | 171 | 171 | batch-01 |
| T1.2 | 172 | 342 | 171 | batch-02 |
| T1.3 | 343 | 513 | 171 | batch-03 |
| T1.4 | 514 | 684 | 171 | batch-04 |
| T1.5 | 685 | 854 | 170 | batch-05 |

- **每批命令模板**（把 `<START>` `<END>` `<N>` `<NN>` 替换为表值）:
  ```bash
  cd /home/gw/opt/fusion-terms
  python3 /tmp/opencode/t5072/backfill_evidence.py \
    --ids-file /tmp/opencode/t5072/w3.ids \
    --definitions /tmp/opencode/t5072/definitions.baseline.tsv \
    --evidence terms/registry/evidence.tsv \
    --raw-iaea artifacts/terminology_sources/iaea_safety_glossary_raw.tsv \
    --raw-iter artifacts/terminology_sources/iter_glossary_raw.tsv \
    --start <START> --end <END> --added-at "$(date -I)"
  sed -n '<START>,<END>p' /tmp/opencode/t5072/w3.ids > /tmp/opencode/t5072/ev_<NN>.ids
  .venv/bin/python scripts/registry_batch_verify.py --mode evidence \
    --ids-file /tmp/opencode/t5072/ev_<NN>.ids --expect <N> --check-urls \
    | tee /tmp/opencode/t5072/ev_<NN>.green.txt
  ```
- **每批验收标准**:
  - ✅ `[T-A]` backfill 输出 `updated=<N> matched_exact=<N>`；evidence 模式 `ids=<N> expect=<N> verdict=PASS` 且 exit 0
  - ✅ `[T-B]` slice 内 w3 evidence 非空 quote 数 = `<N>`
  - ✅ `[T-B]` slice 内 source 只允许 `{IAEA_URL, ITER_URL}` 两个值（Python 断言）
  - ✅ `[T-B]` **探测次数**：`grep -o 'probes=[0-9]*' /tmp/opencode/t5072/ev_<NN>.green.txt` = **该批唯一 URL 数**（不是行数）：batch-01 = `probes=2`（72 ITER + 99 IAEA），batch-02…05 = `probes=1`（该批 100% 为 IAEA 行）。全量 854 仍须 `probes=2`（见 T1.6）。
  - ✅ `[T-B]` quote 不含 `\t`、`\n`、`\x03`（脚本已清洗；断言失败即拒绝）
  - ✅ `[T-C]` `git diff --stat` 只含 `terms/registry/evidence.tsv`；`git diff --cached --stat` 同
- **能失败证明（变异法）**: 把某行 quote 清空 → 该批 evidence 模式报 `evidence_quote_empty`；把 source 改成裸名 `IAEA-Safety-Glossary-2018` → 报 `evidence_source_not_url`；把去重缓存删掉 → `probes=171`，本批 FAIL。
- **提交**:
  ```bash
  git add terms/registry/evidence.tsv
  git commit -m 'feat(registry): backfill W3a evidence quotes batch-<NN> (#T-5072)'
  ```
- **边界**: 不改非 w3 evidence 行；不改 quote 以外的概念字段；不并行写 `evidence.tsv`。

#### Task T1.6 — Phase 1 全量绿色（10 min）

- **依赖**: T1.1–T1.5
- **frontier**: 否
- **执行者**: Dev Orchestrator
- **预估墙钟**: 10 min
- **修改内容**: 无数据修改；记录证据到计划 Execution Log。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  .venv/bin/python scripts/registry_batch_verify.py --mode evidence \
    --ids-file /tmp/opencode/t5072/w3.ids --expect 854 --check-urls \
    | tee /tmp/opencode/t5072/final-evidence-phase1.txt
  python3 - <<'PY'
  import csv
  ids={l.strip() for l in open('/tmp/opencode/t5072/w3.ids',encoding='utf-8') if l.strip()}
  rows=[r for r in csv.reader(open('terms/registry/evidence.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#') and r[0] in ids]
  assert len(rows)==854, len(rows)
  assert all(len(r)>=3 and r[2].strip() for r in rows)
  assert {r[1] for r in rows} == {
    'https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf',
    'https://www.iter.org/fusion-glossary',
  }, {r[1] for r in rows}
  print('evidence_quote_nonempty=854 sources=2 unique_urls=2')
  PY
  grep -o 'probes=[0-9]*' /tmp/opencode/t5072/final-evidence-phase1.txt   # 期望 probes=2
  git diff --stat $(cat /tmp/opencode/t5072/BASE)..HEAD -- terms/registry/evidence.tsv
  ```
- **验收标准**:
  - ✅ `[T-A]` evidence 模式 exit 0，`verdict=PASS`，输出 `probes=2`
  - ✅ `[T-B]` Python 断言输出 `evidence_quote_nonempty=854 sources=2 unique_urls=2`
  - ✅ `[T-C]` `git diff --stat BASE..HEAD` 的 evidence 改动行数为 854（`854 insertions(+), 854 deletions(-)` 口径允许 quote 替换）
- **能失败证明**: 第 854 行 quote 置空 → evidence 模式 exit 1；source 改裸名 → `evidence_source_not_url`。

### Phase 2: 747 条占位 zh 释义补全（431 翻译 + 316 交叉引用，30 批 + 1 次全量）

> **本 Phase 分两条子协议，按行型走不同路径**（行型定义见 D6；`/tmp/opencode/t5072/rowtypes.tsv` 为唯一权威）。每批 step 0 必须先打印并断言本批三类计数，再动手。
>
> **协议 A — `DEFINITION`（431 条）翻译协议**
> 1. **只译不改**：以 `definitions.baseline.tsv` 的 en 定义为唯一输入；不得补充 en 没有的事实、数字、单位、缩写、例子、引用、限定语。
> 2. **术语一致**：优先使用 `concepts.tsv` 的 `preferred_zh` 与 `aliases.tsv` 的 zh 别名；不得改动这些文件。
> 3. **保留结构**：en 中的数字、单位、法规编号（如 `GSR Part 3`、`SSR-6`）、缩写（如 `SSC`、`ALARA`）必须在 zh 中以原样或「中文（缩写）」出现。
> 4. **来源**：zh 行 `source` = `translated:` + 该 id 的 en 行 source；只允许 `translated:IAEA-safety-glossary` / `translated:ITER-glossary`。
> 5. **禁止**：`聚变/核工程术语`、`对应英文`、`指“en”`、空串、纯英文、无 CJK 的释义。
> 6. **不确定时**：按字面直译并在批次记录标注 `[LITERAL]`，交 T3.2 独立复核；不得凭记忆补写。
>
> **协议 B — `CROSS_REF` / `CORRUPT`（316 条）方案甲协议（用户裁决 2026-10-31）**
> 1. zh **一律**写成 `见 <目标 preferred_zh>。`，不加任何解释、不加英文括注、不改写目标。
> 2. 目标来源：`/tmp/opencode/t5072/crossref_resolution.tsv` 第 4 列（T0.3 产出）。该文件已按「首句 `See X.` → concepts 精确匹配 → 复合形态拆解」解析完毕，**执行者不得自行解析、不得自行翻译**。
> 3. 附录 C（C.1 + C.2）的「应写 zh」列是这 68 行的最终值，**逐字照抄**；新增/变更任何目标都必须回写附录 C 并说明证据。
> 4. `CORRUPT` 16 行：只取 en **首句**的目标；首句之后的残余（下一条目正文）一律丢弃，zh 不得出现 `[`、`]`、`!`、`;`，也不得出现残余中的任何英文片段。
> 5. `NO-TARGET` 29 行：zh = `见 <英文目标>。`（英文原样保留，不伪造中文名），并已在 §6 第 3 条登记为已知限制。
> 6. `source` 与协议 A 第 4 条相同（`translated:<en source>`），因为 zh 仍是「据英文交叉引用改写」的派生文本。

#### Task T2.0 — 批次 manifest + applier 脚本 + 行型清单（20 min）

- **依赖**: T0.3, T0.2
- **frontier**: 是
- **执行者**: Simulation Builder
- **预估墙钟**: 20 min（原 15 min：新增行型清单与 见-form 校验分支）
- **修改内容**: 创建 `/tmp/opencode/t5072/apply_translations.py`（附录 B）；生成 `/tmp/opencode/t5072/glossary.tsv`（只读参考）；不改仓内文件。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  python3 - <<'PY'
  import csv
  con=[r for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')]
  with open('/tmp/opencode/t5072/glossary.tsv','w',encoding='utf-8') as f:
      for r in con:
          if len(r)>=4: f.write(f"{r[0]}\t{r[2]}\t{r[3]}\n")
  print('glossary_rows',sum(1 for r in con if len(r)>=4))
  PY
  python3 /tmp/opencode/t5072/apply_translations.py --help
  ```
- **验收标准**:
  - ✅ `[T-A]` `wc -l /tmp/opencode/t5072/w3_placeholder.ids` = 747
  - ✅ `[T-A]` `wc -l /tmp/opencode/t5072/rowtypes.tsv` = 747 且 `cut -f2 /tmp/opencode/t5072/rowtypes.tsv | sort | uniq -c` 显示 `431 DEFINITION` / `300 CROSS_REF` / `16 CORRUPT`
  - ✅ `[T-A]` `python3 /tmp/opencode/t5072/apply_translations.py --help` exit 0
  - ✅ `[T-B]` glossary 行数 = concepts 行数（3076，允许 header/注释跳过）
  - ✅ `[T-C]` `git status --porcelain=v1` 无新增仓内文件
- **能失败证明**: 删除 `w3_placeholder.ids` 后，applier 必须报 manifest missing；空 batch 必须报 `expected 25, got 0`；把某条 `见 地球地壳。` 改成 `见 地壳。`（非 concepts 现存 preferred_zh）→ applier `--check-only` 报 `crossref target not in concepts.preferred_zh`。
- **边界**: 只写 `/tmp`；不修改 `concepts.tsv` / `aliases.tsv`。

#### Task T2.01 … T2.30 — zh 释义分批落表（每批 21–30 min，按行型加权）

- **依赖**: T2.0；T2.(k) 依赖 T2.(k-1)（同一文件串行）
- **frontier**: T2.01 是；T2.02–T2.30 否
- **执行者**: Academic Writer（431 条翻译） + Simulation Builder（316 条交叉引用落表与校验）
- **预估墙钟**: 见批次表末列（`5 + 1.0×DEF + 0.4×CR + 2.0×COR` 分钟，向上取整；**唯一 30 min 上限批为 T2.01**，若超时按 13+12 拆批、各自独立 commit）
- **修改文件**: `terms/registry/definitions.tsv`（仅 w3 zh 行的 definition/source）
- **批次表**（行号对应 `/tmp/opencode/t5072/w3_placeholder.ids`，1-based 闭区间；`CR`=干净 CROSS_REF，`COR`=CORRUPT；`DEF+CR+COR = n`）:

| Task | start | end | n | DEF | CR | COR | 预估 |
|---|---:|---:|---:|---:|---:|---:|---:|
| T2.01 | 1 | 25 | 25 | 25 | 0 | 0 | 30 min |
| T2.02 | 26 | 50 | 25 | 18 | 7 | 0 | 26 min |
| T2.03 | 51 | 75 | 25 | 12 | 13 | 0 | 23 min |
| T2.04 | 76 | 100 | 25 | 15 | 10 | 0 | 24 min |
| T2.05 | 101 | 125 | 25 | 11 | 12 | 2 | 25 min |
| T2.06 | 126 | 150 | 25 | 13 | 12 | 0 | 23 min |
| T2.07 | 151 | 175 | 25 | 16 | 9 | 0 | 25 min |
| T2.08 | 176 | 200 | 25 | 17 | 8 | 0 | 26 min |
| T2.09 | 201 | 225 | 25 | 13 | 12 | 0 | 23 min |
| T2.10 | 226 | 250 | 25 | 17 | 8 | 0 | 26 min |
| T2.11 | 251 | 275 | 25 | 12 | 13 | 0 | 23 min |
| T2.12 | 276 | 300 | 25 | 15 | 9 | 1 | 26 min |
| T2.13 | 301 | 325 | 25 | 15 | 8 | 2 | 28 min |
| T2.14 | 326 | 350 | 25 | 14 | 11 | 0 | 24 min |
| T2.15 | 351 | 375 | 25 | 13 | 12 | 0 | 23 min |
| T2.16 | 376 | 400 | 25 | 13 | 12 | 0 | 23 min |
| T2.17 | 401 | 425 | 25 | 13 | 11 | 1 | 25 min |
| T2.18 | 426 | 450 | 25 | 12 | 11 | 2 | 26 min |
| T2.19 | 451 | 475 | 25 | 13 | 12 | 0 | 23 min |
| T2.20 | 476 | 500 | 25 | 10 | 14 | 1 | 23 min |
| T2.21 | 501 | 525 | 25 | 15 | 9 | 1 | 26 min |
| T2.22 | 526 | 550 | 25 | 14 | 8 | 3 | 29 min |
| T2.23 | 551 | 575 | 25 | 17 | 7 | 1 | 27 min |
| T2.24 | 576 | 600 | 25 | 17 | 7 | 1 | 27 min |
| T2.25 | 601 | 625 | 25 | 13 | 12 | 0 | 23 min |
| T2.26 | 626 | 650 | 25 | 15 | 9 | 1 | 26 min |
| T2.27 | 651 | 675 | 25 | 14 | 11 | 0 | 24 min |
| T2.28 | 676 | 700 | 25 | 16 | 9 | 0 | 25 min |
| T2.29 | 701 | 725 | 25 | 12 | 13 | 0 | 23 min |
| T2.30 | 726 | 747 | 22 | 11 | 11 | 0 | 21 min |
| **合计** | | | **747** | **431** | **300** | **16** | **746 min** |

- **每批执行步骤（严格按序，C1：`--check-only` 必须在 apply 之前）**:
  1. **step 0 — 行型计数闸门**（本批三类计数必须与批次表该行完全一致，否则停止）：
     ```bash
     sed -n '<START>,<END>p' /tmp/opencode/t5072/w3_placeholder.ids > /tmp/opencode/t5072/t2_b<NN>.ids
     python3 - <<'PY'
     import re
     exp = {'DEFINITION': <DEF>, 'CROSS_REF': <CR>, 'CORRUPT': <COR>}   # 抄批次表本行
     kinds = {}
     for line in open('/tmp/opencode/t5072/rowtypes.tsv', encoding='utf-8'):
         cid, kind, _text, _rem = line.rstrip('\n').split('\t')
         kinds[cid] = kind
     ids = [l.strip() for l in open('/tmp/opencode/t5072/t2_b<NN>.ids', encoding='utf-8') if l.strip()]
     cnt = {'DEFINITION': 0, 'CROSS_REF': 0, 'CORRUPT': 0}
     for cid in ids:
         cnt[kinds[cid]] += 1
     print(f"batch<NN> n={len(ids)} DEFINITION={cnt['DEFINITION']} CROSS_REF={cnt['CROSS_REF']} CORRUPT={cnt['CORRUPT']}")
     assert cnt == exp, (cnt, exp)
     PY
     ```
  2. **step 1 — 生成 batch TSV**：`DEFINITION` 行按协议 A 翻译；`CROSS_REF`/`CORRUPT` 行按协议 B 取 `crossref_resolution.tsv` / 附录 C 的 zh。写成 3 列 TSV：
     ```
     concept_id<TAB>zh_definition<TAB>translated:<en_source>
     ```
     保存为 `/tmp/opencode/t5072/t2_b<NN>.tsv`；行数必须等于批次表 `<n>`。
  3. **step 2 — 先校验（不写）**：
     ```bash
     python3 /tmp/opencode/t5072/apply_translations.py --check-only \
       --batch /tmp/opencode/t5072/t2_b<NN>.tsv \
       --definitions terms/registry/definitions.tsv \
       --placeholder-ids /tmp/opencode/t5072/w3_placeholder.ids \
       --concepts terms/registry/concepts.tsv \
       --ledger /tmp/opencode/t5072/crossref_resolution.tsv \
       --expect <n>
     ```
  4. **step 3 — 落表**（同一命令去掉 `--check-only`）。
  5. **step 4 — 机械检查**：`pipeline.validate_registry` + 全量占位计数（见验收标准）。
- **每批验收标准**:
  - ✅ `[T-A]` `--check-only` 输出 `checked=<n> updated=0` exit 0；apply 输出 `checked=<n> updated=<n>` exit 0
  - ✅ `[T-A]` `pipeline.validate_registry` exit 0
  - ✅ `[T-B]` **DEFINITION 断言**（applier 内）：本批全部无占位标记、有 CJK、source 为 `translated:*`、en 中的数字 token 多重集与 zh 相等、en 中 2+ 位大写缩写在 zh 中出现
  - ✅ `[T-B]` **CROSS_REF/CORRUPT 断言**（applier 内，A1c 的批次级版本）：本批行型为 CROSS_REF / CORRUPT 的 id，zh 全部匹配 `^见 .+。$`；`见` 后目标 ∈ `concepts.tsv` 的非空 `preferred_zh` 集合，**或** 该 id 在 `crossref_resolution.tsv` 中标记为 `NO-TARGET` 且 zh == `见 <该文件第 3 列英文目标>。`；zh 不含 `[`、`]`、`!`、`;`
  - ✅ `[T-B]` 全量占位计数 = `747 - 已完成条数`（尾批为 0）
  - ✅ `[T-C]` `git diff --stat` 只含 `terms/registry/definitions.tsv`；`git diff --cached --stat` 同
  - ✅ `[T-C]` 本批 id 的 en 行逐字节未变（`git diff` 中不出现 `\ten\t` 行）
- **能失败证明（变异法）**:
  - 把某条 zh 改回 `聚变/核工程术语，对应英文“X”。` → 占位计数不降，本批 FAIL。
  - 把 en 的 `10 mSv` 译成没有数字的「十毫希」 → 数字 token 检查 FAIL。
  - 把 `ALARA` 译成「合理可行尽量低」但不保留 `ALARA` → 缩写检查 FAIL。
  - 把 `见 源。` 改成 `见 来源。`（`来源` 不在 preferred_zh 集合）→ 交叉引用断言 FAIL（R10）。
  - 把 `crust-earth-s` 的 zh 写成含 `[curie (Ci)]` 的任何形式 → 污染字符断言 FAIL（R11）。
  - 把某条 `NO-TARGET` 行改写成自译中文（如 `见 废物。`）→ 与 `crossref_resolution.tsv` 不一致，断言 FAIL。
- **提交**:
  ```bash
  git add terms/registry/definitions.tsv
  git commit -m 'feat(registry): backfill W3a zh definitions batch-<NN> (<DEF> translated + <CR>+<COR> cross-ref) (#T-5072)'
  ```
- **边界**: 只改本批 25/22 条 zh 行的 `definition` 与 `source`；不改 en、concept_id、lang、行序；不改 107 条非占位 zh；不新增/修改附录 C 之外的目标名。

#### Task T2.31 — Phase 2 全量绿色（15 min）

- **依赖**: T2.01–T2.30
- **frontier**: 否
- **执行者**: Dev Orchestrator
- **预估墙钟**: 15 min（原 10 min：新增 316 条交叉引用目标断言）
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  python3 - <<'PY'
  import csv, re
  ids={l.strip() for l in open('/tmp/opencode/t5072/w3.ids',encoding='utf-8') if l.strip()}
  rows=[r for r in csv.reader(open('terms/registry/definitions.tsv',encoding='utf-8'),delimiter='\t')
        if r and not r[0].startswith('#') and r[0] in ids and r[1]=='zh']
  ph=[r[0] for r in rows if '聚变/核工程术语' in r[2] or '对应英文' in r[2] or not r[2].strip()]
  assert len(rows)==854, len(rows)
  assert not ph, ph[:10]
  # 行型复核：全过程必须仍为 431/300/16
  kinds={}
  for line in open('/tmp/opencode/t5072/rowtypes.tsv',encoding='utf-8'):
      cid,k,_t,_r=line.rstrip('\n').split('\t'); kinds[cid]=k
  from collections import Counter
  print('rowtypes', Counter(kinds.values()))
  assert Counter(kinds.values())=={'DEFINITION':431,'CROSS_REF':300,'CORRUPT':16}
  # 交叉引用断言
  zh={r[0]:r[2] for r in rows}
  pref={r[2] for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t')
        if r and not r[0].startswith('#') and len(r)>=4 and r[2].strip()}
  notarget={}
  for line in open('/tmp/opencode/t5072/crossref_resolution.tsv',encoding='utf-8'):
      cid,k,target,z=line.rstrip('\n').split('\t')
      if z=='NO-TARGET': notarget[cid]=target
  see=re.compile(r'^见 (.+)。$')
  bad=[]; badtarget=[]
  for cid in [c for c,k in kinds.items() if k!='DEFINITION']:
      t=zh[cid]; m=see.match(t)
      if not m: bad.append((cid,t)); continue
      if any(ch in t for ch in '[]!;'): bad.append((cid,t)); continue
      tgt=m.group(1)
      if cid in notarget:
          if tgt!=notarget[cid]: badtarget.append((cid,tgt,notarget[cid]))
      elif tgt not in pref:
          badtarget.append((cid,tgt,'NOT-IN-preferred_zh'))
  assert not bad, bad[:10]
  assert not badtarget, badtarget[:10]
  print('w3_zh_rows=854 placeholder=0 crossref_form_ok=316 no_target_registered=%d' % len(notarget))
  PY
  .venv/bin/python -m pipeline.validate_registry
  .venv/bin/python scripts/registry_batch_verify.py --mode evidence \
    --ids-file /tmp/opencode/t5072/w3.ids --expect 854 --check-urls | grep -o 'probes=[0-9]*'
  ```
- **验收标准**:
  - ✅ `[T-A]` Python 输出 `w3_zh_rows=854 placeholder=0 crossref_form_ok=316 no_target_registered=29`
  - ✅ `[T-B]` `rowtypes` 行显示 `DEFINITION: 431, CROSS_REF: 300, CORRUPT: 16`（全过程未漂移；按用户口径即 **431 / 316（=300 干净 + 16 污染）/ 16**）
  - ✅ `[T-A]` `pipeline.validate_registry` exit 0
  - ✅ `[T-A]` evidence 模式 exit 0（Phase 1 不回退）且 `probes=2`
- **能失败证明**: 任意一条 zh 改回占位 → 断言失败并打印 id；任一交叉引用 zh 写成自译中文 → `badtarget` 非空并打印 id。

### Phase 3: 终验与独立验收

#### Task T3.1 — 全量机械验收（20 min）

- **依赖**: T1.6, T2.31
- **frontier**: 否
- **执行者**: Dev Orchestrator
- **预估墙钟**: 20 min（原 15 min：新增 316 条交叉引用全量断言）
- **修改内容**: 无数据修改；结果写入计划 Execution Log。
- **命令**:
  ```bash
  cd /home/gw/opt/fusion-terms
  set -o pipefail
  .venv/bin/python scripts/registry_batch_verify.py --self-test | tee /tmp/opencode/t5072/final-selftest.txt
  .venv/bin/python scripts/registry_batch_verify.py --mode evidence \
    --ids-file .github/plans/t4973-batches/w3.ids --expect 854 --check-urls | tee /tmp/opencode/t5072/final-evidence.txt
  .venv/bin/python -m pipeline.validate_registry
  .venv/bin/python -m pytest -q
  .venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all >/dev/null
  .venv/bin/ruff format --check . && .venv/bin/ruff check .
  python3 - <<'PY'
  import csv, re
  from collections import Counter
  ids={l.strip() for l in open('.github/plans/t4973-batches/w3.ids',encoding='utf-8') if l.strip()}
  defs=[r for r in csv.reader(open('terms/registry/definitions.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#') and r[0] in ids and r[1]=='zh']
  ev=[r for r in csv.reader(open('terms/registry/evidence.tsv',encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#') and r[0] in ids]
  ph=[r[0] for r in defs if '聚变/核工程术语' in r[2] or '对应英文' in r[2] or not r[2].strip()]
  assert len(defs)==854 and not ph, (len(defs), ph[:5])
  assert len(ev)==854 and all(len(r)>2 and r[2].strip() for r in ev)
  kinds={}
  for line in open('/tmp/opencode/t5072/rowtypes.tsv',encoding='utf-8'):
      cid,k,_t,_r=line.rstrip('\n').split('\t'); kinds[cid]=k
  assert Counter(kinds.values())=={'DEFINITION':431,'CROSS_REF':300,'CORRUPT':16}
  zh={r[0]:r[2] for r in defs}
  pref={r[2] for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t')
        if r and not r[0].startswith('#') and len(r)>=4 and r[2].strip()}
  notarget={l.split('\t')[0]: l.split('\t')[2] for l in open('/tmp/opencode/t5072/crossref_resolution.tsv',encoding='utf-8') if l.split('\t')[3].strip()=='NO-TARGET'}
  see=re.compile(r'^见 (.+)。$')
  cr=[c for c,k in kinds.items() if k!='DEFINITION']
  assert len(cr)==316, len(cr)
  for cid in cr:
      m=see.match(zh[cid]); assert m, (cid, zh[cid])
      assert not any(ch in zh[cid] for ch in '[]!;'), (cid, zh[cid])
      tgt=m.group(1)
      assert (tgt==notarget[cid]) if cid in notarget else (tgt in pref), (cid, tgt)
  print('w3_zh=854 placeholder=0 crossref_ok=316 evidence=854 nonempty_quote=854')
  PY
  grep -o 'probes=[0-9]*' /tmp/opencode/t5072/final-evidence.txt    # 期望 probes=2
  grep -c '27/27 assertions passed' /tmp/opencode/t5072/final-selftest.txt   # 期望 1
  git diff --stat $(cat /tmp/opencode/t5072/BASE)..HEAD
  ```
- **验收标准**:
  - ✅ `[T-A]` self-test 输出 `27/27 assertions passed`，exit 0（`grep -c` = 1）
  - ✅ `[T-A]` evidence 模式 `ids=854 expect=854 verdict=PASS`，exit 0，`probes=2`
  - ✅ `[T-A]` `pipeline.validate_registry` exit 0；`pytest -q` exit 0（基线 186 tests）
  - ✅ `[T-A]` `registry_row_audit --expect-clean-all` exit 0；ruff format/check exit 0
  - ✅ `[T-B]` Python 输出 `w3_zh=854 placeholder=0 crossref_ok=316 evidence=854 nonempty_quote=854`；内部断言含 `Counter == {DEFINITION:431, CROSS_REF:300, CORRUPT:16}`
  - ✅ `[T-C]` `git diff --stat BASE..HEAD` 只含 `terms/registry/definitions.tsv`、`terms/registry/evidence.tsv`、`scripts/registry_batch_verify.py`、`CHANGELOG.md`（计划文件另计 `docs(plan)` 提交）
- **能失败证明**:
  - 删掉任一批 commit 后再跑 → 占位/空 quote 计数不为 0；
  - self-test 回退到 19/24 → A3 失败；
  - 把某条交叉引用 zh 改成 `见 废物。` → `tgt in pref` 断言 FAIL（R10）；
  - 把 URL 探测去重删掉 → `probes=854`，T-A 失败。

#### Task T3.2 — 独立 acceptance-verifier 抽检（30 min）

- **依赖**: T3.1
- **frontier**: 否
- **执行者**: 独立 `acceptance-verifier`（只读，不复用执行者会话）
- **预估墙钟**: 30 min
- **修改内容**: 无仓内修改；报告写 `/tmp/opencode/t5072/independent-acceptance.md`。
- **抽样规则（固定随机种子，可复跑）**:
  ```bash
  cd /home/gw/opt/fusion-terms
  python3 - <<'PY'
  import random
  ph=[l.strip() for l in open('/tmp/opencode/t5072/w3_placeholder.ids',encoding='utf-8') if l.strip()]
  ids=[l.strip() for l in open('.github/plans/t4973-batches/w3.ids',encoding='utf-8') if l.strip()]
  print('ZH_SAMPLE', ' '.join(random.Random(5072).sample(ph, 75)))       # 747*10%=74.7 → 75
  print('EV_SAMPLE', ' '.join(random.Random(5073).sample(ids, 86)))       # 854*10%=85.4 → 86
  PY
  ```
- **独立检查项**:
  1. **zh 抽检（75 条，含两种行型）**：
     - 若该 id 行型为 `DEFINITION`：逐条对照 `definitions.baseline.tsv` 的 en 文本，确认无新增数字/单位/法规编号/缩写/事实；source 必须是 `translated:<en source>`；无占位标记；中文可读。
     - 若该 id 行型为 `CROSS_REF` / `CORRUPT`：zh 必须是 `见 X。`；X 必须逐字等于 `concepts.tsv` 中某条非空 `preferred_zh`，或该 id 在附录 C 登记为 `NO-TARGET` 且 X = 该行英文目标；**CORRUPT 行额外确认 zh 不含污染残余的任何片段**。
  2. **evidence 抽检（86 条）**：`quote` 用**与 backfill 脚本完全相同的归一化**（去 `\ue000-\uf8ff` 私用区字形 → `\u2022`/`\x03`/`\uf069` → 压空白）后，必须与对应 raw 源（`iaea_safety_glossary_raw.tsv` / `iter_glossary_raw.tsv`）中该条目定义**逐字相等**（不是「相似」「ratio≥0.98」）；source URL 必须 200；无空 quote。
  3. **机械门禁复跑**：T3.1 的 V1–V9 全部由 verifier 重新执行，不接受执行者粘贴的输出。
  4. **边界审计**：`git diff --stat BASE..HEAD` 不得出现 `concepts.tsv`、`aliases.tsv`、`pipeline/`、`iaea_fusion.html`；`concepts.tsv` 的 `preferred_zh`/`category` 行 sha 必须与 BASE 相同。
- **判定**:
  - ✅ PASS：两类抽检 FAIL = 0，且所有机械门禁 exit 0。
  - ❌ FAIL：任一条解释性错误、数字 token/缩写丢失、交叉引用目标不在 preferred_zh 集合、zh 复现污染、quote 不逐字匹配、URL 非 200、越界修改 → 进入 T3.3。
- **能失败证明**: 若把某条 zh 的 `10 mSv` 译成「十毫希」且不保留数字 token，机械检查必须 FAIL；若 quote 是模型自写而非 raw 原文，归一化逐字比对必须 FAIL；若某条 zh 写成 `见 地壳。`（非 preferred_zh），抽检必须 FAIL。
- **边界**: verifier 只读；不修数据；不改计划；报告只写 `/tmp`。

#### Task T3.3 — 条件返工（仅 T3.2 FAIL 时执行，≤30 min/轮，最多 2 轮）

- **依赖**: T3.2 FAIL
- **frontier**: 否
- **执行者**: Academic Writer / Simulation Builder
- **预估墙钟**: 每轮 30 min
- **修改内容**: 仅回滚/重做 T3.2 指出的具体批次；不扩大范围。
- **命令**:
  ```bash
  git log --oneline --grep='(#T-5072)' | head -40
  # 找到对应批次 commit 后：
  git revert --no-edit <bad-batch-sha>
  # 重做该批，重新走 T2.<NN> 的翻译/applier/验收/commit
  ```
- **验收标准**:
  - ✅ `[T-A]` 返工批次的 T2 验收全部 exit 0
  - ✅ `[T-A]` T3.1 全量机械验收 exit 0
  - ✅ `[T-B]` T3.2 对返工批次重新抽检 FAIL = 0
- **能失败证明**: 若不回滚只追加新行，applier 会因重复 id 报错；`git diff` 出现两份同 id zh 行，validate_registry 报 duplicate。
- **边界**: 不回滚已通过批次；不 reset 已推送历史；不用 `git checkout --` 覆盖未提交改动。

#### Task T3.4 — 收尾、CHANGELOG 更正与 PM 证据（15 min）

- **依赖**: T3.2 PASS
- **frontier**: 否
- **执行者**: Dev Orchestrator
- **预估墙钟**: 15 min（原 10 min：新增 CHANGELOG 更正与断言）
- **修改内容**:
  1. 更新本计划 `## Execution Log`（命令、exit、计数、commit 列表）。
  2. **更正 `CHANGELOG.md`**（C3）：
     - 第 81 行「`--self-test` 实测 19/24，漂移由 PM 5072 承接」→ 改为「`--self-test` 实测 **27/27**（PM 5072 修复并扩展 evidence 模式断言）」；
     - 第 82 行「747 条占位释义与证据 quote 缺口由 PM 5072 承接」→ 改为「747 条占位释义（431 翻译 + 316 交叉引用按方案甲补 `见 X。`）与 854 条 evidence quote 已由 PM 5072 补齐」；
     - 只改这两行的计数与状态表述，不加新条目、不改版本号。
  3. 通过 `pm-coordinator` 把 PM #5072 置为 `done`/100%，notes 附 V1–V9 的 exit 与独立验收结论（不直接调用 PM MCP）。
- **验收标准**:
  - ✅ `[T-A]` `git log --oneline --grep='#T-5072' | wc -l` ≥ 38（2 个脚本 + 5 个 evidence + 30 个 definitions + 1 收尾 docs；允许合并尾批）
  - ✅ `[T-A]` `grep -c '19/24' CHANGELOG.md` = 0 **且** `grep -c '27/27' CHANGELOG.md` ≥ 1（R12）
  - ✅ `[T-B]` `git diff --stat` 中 CHANGELOG 改动 ≤ 4 行（2 条替换 = 2 insertions + 2 deletions）
  - ✅ `[T-C]` 最后一次 `git status --porcelain=v1` 只允许 `?? iaea_fusion.html` 与计划文件自身
  - ✅ `[T-B]` 计划 Execution Log 含 T3.1 全部命令的 exit code 与 T3.2 抽检结论
- **提交**: `git add CHANGELOG.md .github/plans/5072-w3a-evidence-definition-backfill.md && git commit -m 'docs: record T-5072 acceptance evidence and correct self-test count to 27/27 (#T-5072)'`
- **边界**: 不改父计划、不改 `.github/plans/_project-snapshot.md`、不改其他 CHANGELOG 条目。

## 8. Execution Wave（并行执行波次）

> 所有数据写操作对同一 TSV 串行；下表 `Frontier` 只表示依赖已满足，不代表可并行写文件。

| Wave | Tasks | Frontier | 依赖已完成 |
|---|---|---|---|
| W0 | T0.0 | T0.0 | — |
| W1 | T0.1 | T0.1 | W0 |
| W2 | T0.2 | T0.2 | W1 |
| W3 | T0.3 | T0.3 | W0 |
| W4 | T1.0 | T1.0 | W2, W3 |
| W5 | T1.1 → T1.5 → T1.6 | T1.1 | W4 |
| W6 | T2.0 | T2.0 | W2, W3 |
| W7 | T2.01 → … → T2.30 → T2.31 | T2.01 | W6 |
| W8 | T3.1 | T3.1 | W5, W7 |
| W9 | T3.2 | T3.2 | W8 |
| W10 | T3.4（T3.3 仅在 T3.2 FAIL 时插入） | T3.4 | W9 |

**并行机会说明**：T0.1（脚本）与 T0.3（`/tmp` manifest）无文件冲突，理论可并行；本计划按串行执行，避免会话/工作区状态竞争。T1 与 T2 不可并行：T2 改 `definitions.tsv`，T1 的 quote 虽取 baseline en，但为审计可复现，先完成 T1。**Phase 2 的 30 个批次严格串行（同一文件），不得并行。**

## 9. Post-Execution Verification

### Automated Verification（Dev Orchestrator 自动执行）

| ID | Description | Command | Expected |
|---|---|---|---|
| V1 | self-test 27/27 | `.venv/bin/python scripts/registry_batch_verify.py --self-test` | exit 0；`27/27 assertions passed` |
| V2 | 零占位 | 见 T3.1 Python 断言 | `w3_zh=854 placeholder=0` |
| V3 | evidence 全量 | `.venv/bin/python scripts/registry_batch_verify.py --mode evidence --ids-file .github/plans/t4973-batches/w3.ids --expect 854 --check-urls` | exit 0；`verdict=PASS`；`probes=2` |
| V4 | registry 校验 | `.venv/bin/python -m pipeline.validate_registry` | exit 0 |
| V5 | 测试 | `.venv/bin/python -m pytest -q` | exit 0；186 tests |
| V6 | 结构审计 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | exit 0 |
| V7 | 格式/静态 | `.venv/bin/ruff format --check . && .venv/bin/ruff check .` | exit 0 |
| V8 | 改动范围 | `git diff --stat BASE..HEAD` | 仅 4 个声明文件（计划文件另计） |
| V9 | 来源可追溯 | T3.1 Python 断言 + T3.2 抽检 | quote 与 raw 归一化后逐字相等；zh 全部 `translated:*` |
| V10 | 行型三分守恒 | T3.1 Python 断言 | `{DEFINITION:431, CROSS_REF:300, CORRUPT:16}` |
| V11 | 交叉引用目标合法 | T3.1 Python 断言 | 316 条 `见 X。`；287 条 X ∈ `preferred_zh`；29 条 X = 附录 C 英文目标 |
| V12 | CHANGELOG 一致 | `grep -c '19/24' CHANGELOG.md; grep -c '27/27' CHANGELOG.md` | 0 / ≥1 |

### Deferred (needs restart / deployment)

- 无。本任务不改服务、不部署。

### Probe (best-effort, run if available)

- [ ] P1: `curl -sS -o /dev/null -w '%{http_code}' -L -A 'Mozilla/5.0' https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf` → `200`
- [ ] P2: `curl -sS -o /dev/null -w '%{http_code}' -L -A 'Mozilla/5.0' https://www.iter.org/fusion-glossary` → `200`

### Manual（真正需要人工判断）

- [ ] M1: 独立 verifier 对 75 条 zh 抽检做语义复核（DEFINITION：无新增事实/数字/缩写；CROSS_REF/CORRUPT：目标名恰当、污染未混入）。
- [ ] M2: 独立 verifier 对 86 条 evidence quote 与 raw 源做逐字对照。
- [ ] M3: 确认 `concepts.tsv` 的 `preferred_zh` / `category` 与 BASE 逐字节一致（只读 diff）。
- [ ] M4: 确认附录 C 的 29 条 `NO-TARGET` 英文目标行可被后续「概念补登」任务直接消费（不在本任务修）。

## 10. 独立验收清单（签收条件）

| # | 条件 | 判定 |
|---|---|---|
| I1a | `w3.ids` 854 条 zh 行全部非占位，占位计数 0 | 二元 |
| I1b | 431 条 `DEFINITION`：CJK + 无占位 + 数字/缩写多重集相等 + `source = translated:*` | 二元 |
| I1c | 316 条 `CROSS_REF` 族：zh 匹配 `^见 .+。$` 且无 `[]!;`；287 条目标 ∈ `concepts.preferred_zh`；29 条出现在附录 C 台账 | 二元 |
| I2 | 854 条 evidence 全部至少 1 条非空 quote | 二元 |
| I3 | 854 条 evidence 的 source 均为 URL，`--check-urls` exit 0，`probes=2` | 二元 |
| I4 | self-test 27/27 exit 0 | 二元 |
| I5 | `validate_registry` / `pytest` / `row_audit` / ruff 全 exit 0 | 二元 |
| I6 | 独立抽检 75 zh + 86 evidence，FAIL = 0 | 二元 |
| I7 | 修改范围仅 `definitions.tsv` / `evidence.tsv` / `registry_batch_verify.py` / `CHANGELOG.md` | 二元 |
| I8 | 每个批次有独立 commit，message 含 `#T-5072` | 二元 |
| I9 | 附录 C 的 16 条 CORRUPT 行均有污染描述，且 zh 未复现污染 | 二元 |

## 11. 回滚与失败处理

| 失败点 | 处理 |
|---|---|
| 单批翻译/quote 错误 | `git revert --no-edit <batch-sha>`，重做该批；不回滚其他批 |
| 交叉引用目标写错（不在 preferred_zh 集合） | 回滚该批，按 `crossref_resolution.tsv` / 附录 C 逐字重写；不得改断言放行 |
| zh 复现污染残余 | 立即回滚该批；重写为附录 C.1 的 `见 <目标>。`；加跑 T2.31 污染字符断言 |
| 脚本 T0.1/T0.2 回归 | `git revert` 对应脚本 commit；重新跑 27/27 self-test 与 evidence 模式 |
| URL 403/超时 | 记录 `[URL-FAIL]`，暂停验收；不得 `--no-net` 冒充；核验官方镜像后再继续 |
| raw 源匹配失败 | 脚本非零退出；人工确认 en 文本与 raw 的差异；不得降低阈值、不得加近似兜底、不得手写 quote |
| 独立抽检 FAIL | T3.3 返工；连续 2 轮仍 FAIL → `↑ ESCALATE`，不签收 |
| CHANGELOG 行号漂移 | 记录 `[CHANGELOG-DRIFT]`，按内容 grep 定位，不新增条目、不改其他行 |
| 工作区出现未声明改动 | 停止提交；`git diff` 定位；未声明改动不得夹带 |

## 12. 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|---|---|---:|---:|---:|
| R1 | 结构完整性 | 4 | 4 | 0 |
| R1.5 | 外部引用事实核查 | 5 | 5 | 0 |
| R2 | 可执行性（脚本干跑） | 5 | 5 | 0 |
| R2.8 | LLM 可执行性/歧义 | 4 | 4 | 0 |
| R3 | 风险与边缘 | 3 | 3 | 0 |
| CT-1 | 独立 Red-Team（2026-10-31） | 11（B1–B5, C1–C6, G1–G3） | 11 | 0（结论 REFUTED：原计划的「747 一律翻译」与 self-test 数字有实质错误） |
| Refine-1 | 吸收 CT + 用户裁决 方案甲 | 14 | 14 | 0 |
| **终止** | **T1 — 无 blocking issue** | | | **0** |

**R1.5 事实核查记录（含 rev 2 重测）**：
- `registry_batch_verify.py --self-test` 实测 19/24，5 条 FAIL（regex 锚点、definitions 恢复不完整、allowlist 样本未走 restored、2 条派生 token）。
- `w3.ids`=854；占位 zh=747；空 quote=854；en 来源 782 IAEA + 72 ITER。
- **行型实测（rev 2 新增）**：`DEFINITION 431 / CROSS_REF 300 / CORRUPT 16`（合计 747）；交叉引用族 316。
- **交叉引用解析实测**：316 族中 287 可机械解析（248 直接 + 25 复合 + 14 污染行首句），29 无目标（27 干净 + 2 污染）。
- **self-test 变异实测**：删 `SELF_TEST_RESTORED_CASES[3]` → 19/24；删 `adjoint-flux` en 恢复 → 21/24。
- IAEA PDF 默认 urllib 403，浏览器 UA 200；ITER 200；去重后唯一 URL = 2。
- `pytest` 基线 186 tests；`validate_registry`/`row_audit`/ruff 基线 exit 0。
- `pipeline/` 不校验 definitions source 枚举，`translated:` 不会破坏导出链。
- 全库非 w3 空 quote 1040、非 w3 `corresponding to` 套话变体 99（已登记 §6）。

**R2 干跑记录**：
- 在 `/tmp` 副本上执行 self-test 修复补丁 → 24/24；再加 3 条 evidence 断言 → 27/27。
- 在 `/tmp` 副本上执行 evidence backfill（PUA 归一化 + 逐字匹配）→ `updated=854 matched_exact=854`，source 2 个 URL。
- 在 `/tmp` 副本上执行 evidence 模式 → `verdict=PASS`、`probes=2`；真实仓 baseline → 854 条 `evidence_quote_empty`。

**Refine-1 修订记录（rev 2，2026-10-31）**：见 §13 的「revised after CT」条目。

## 13. Execution Log（执行时回写）

> 每个 Task 完成后追加一行；禁止预填结果（下表 rev 记录除外，属计划修订留痕）。

| Task | 日期 | commit | exit | 关键输出 |
|---|---|---|---|---|
| **plan-rev2** | **2026-10-31** | — | — | **revised after CT (REFUTED) + user adjudication 2026-10-31**：用户裁定 316 条 CROSS_REF 采用**方案甲（按目标中文名补齐，zh = `见 <preferred_zh>。`）**，无目标行逐条登记（附录 C），16 条污染行隔离且 zh 不复现污染。吸收 CT 5 项 blocker：**B1** 行型三分 431/300/16 + 解析 287/29；**B2** evidence 模式 +3 断言（24→27）；**B3** 变异数字改为 19/24 与 21/24；**B4** 归一化加 PUA 剥离、854/854 逐字匹配、删除 difflib；**B5** URL 探测按唯一 URL 去重（probes=2）。另吸收 C1–C6、G1–G3。任务总数 47，commit 估算 38。 |
| T0.0 | 2026-10-31 | — | 1 | BASE=`3034dce`（计划入库后重测）；`red-selftest.txt` = `19/24 assertions passed` exit 1；`validate_exit=0`；`w3.ids`=854；工作区仅 `?? iaea_fusion.html` |
| T0.1 | 2026-10-31 | `5735da8` | 0 | self-test `24/24`；`--mode names … --expect 854` PASS；ruff ok；变异证明 删 index 3 → `19/24`、删 en 恢复 → `21/24`；`/tmp` 无残留副本（`ls /tmp \| grep -c t0_2_selftest_restored_` = 0） |
| T0.2 | 2026-10-31 | `a9c8201` | 0 | self-test `27/27`；evidence RED：exit 1、`evidence_quote_empty` 854 条、**`probes=1`**（基线唯一 URL 只有 ITER 一个，782 条 IAEA 行为裸名）；无 `--ids-file` → exit 2 + `requires --ids-file`；真实探测 IAEA 200(0.80s)/ITER 200(1.11s)；ruff ok；变异证明：裸名+非空 quote → `evidence_source_not_url`、404 → `evidence_url_status`、删去重 → `probes=72` + `evidence_probe_dedup` |
| T0.3 | 2026-10-31 | — | 0 | 只写 `/tmp/opencode/t5072/`；`w3.ids` 854 / `w3_placeholder.ids` 747；行型 **DEFINITION 431 / CROSS_REF 300 / CORRUPT 16**（交叉引用族 316）；解析 **direct 248 / ledger 68 / NO-TARGET 29**；`sha256sum -c manifests.sha256` exit 0；`comm` 差集 0；变异（删 BODY 判据）→ `(431, 316, 0)` 断言失败 |
| T1.0 | 2026-10-31 | — | 0 | `/tmp/opencode/t5072/backfill_evidence.py` 落地（PUA 剥离、无 difflib、逐行改写以保非 w3 行字节不变）；dry-run `updated=854 matched_exact=854`；副本变更 **854 行 / 非 w3 变更 0**；854 非空 quote；source `IAEA 782 / ITER 72`；evidence 模式对副本 `PASS` + `probes=2`；失败证明：删 `--raw-iaea` → exit 1、删 `dose-quantities` en → exit 1；仓内无改动 |
| T1.1–T1.5 | 2026-10-31 | `7d24cca` / `1dd618a` / `b2ce15f` / `e2a8744` / `6dd09c8` | 0 | 每批 `updated=matched_exact=171/171/171/171/170`；evidence 模式全部 `verdict=PASS` exit 0；`probes` 实测 **b01=2、b02=1、b03=1、b04=1、b05=1**（该批唯一 URL 数，非行数）；每批 `git diff --stat` 仅 `terms/registry/evidence.tsv`；数据断言：slice 内非空 quote = N、source ⊆ 2 URL、无 `\t`/`\n`/`\r`/`\x03` |
| T1.6 | 2026-10-31 | — | 0 | 全量 854：`verdict=PASS` exit 0、**`probes=2`**；`evidence_quote_nonempty=854 sources=2 unique_urls=2`；`git diff --stat BASE..HEAD` = `854 insertions(+), 854 deletions(-)`；失败证明（副本）：quote 置空 → `evidence_quote_empty` exit 1、source 改裸名 → `evidence_source_not_url` exit 1 |
| T2.0 | 2026-10-31 | — | 0 | 只写 `/tmp/opencode/t5072/`：`make_batch.py` / `assemble.py` / `apply_translations.py` / `count_placeholders.py` / `glossary.tsv`(3076) / `TRANSLATION_CONTRACT.md`（自检段 `issues:` 须为 `[]`）；30 批 manifest 逐批重算与计划批次表 **0 处不匹配**（合计 `DEFINITION 431 / CROSS_REF 300 / CORRUPT 16`）；附录 C 68 行与 `crossref_resolution.tsv` **0 缺 / 0 多 / 0 值不符**；`apply_translations.py --check-only` 在未改动仓上 `updated=0` |
| T2.01–T2.30 | 2026-10-31 | `581379b` … `d84aabc`（30 个 `feat(registry)` + 1 个 `06d40e0` fix） | 0 | 每批固定流程：`assemble` → `apply_translations.py --check-only`（exit 0, `updated=0`）→ apply（`updated=N`）→ `validate_registry` exit 0 → `count_placeholders` 递减（747→722→…→22→0）→ `git diff --stat` 仅 `terms/registry/definitions.tsv`、`N` 行 `N`/`N` 增删 → commit。**占位 747 → 0**；en 行零改动（每批 `git diff -U0 \| grep -c '^@@.*\ten\t'` = 0）；分批计数 D=431 / X=300 / C=16 与计划逐批表一致（b05/b12/b13/b17/b18/b20/b21/b22/b23/b24/b26 含 corrupt 行已计入） |
| T2.31 | 2026-10-31 | — | 0 | 计划内断言脚本输出 `rowtypes Counter({'DEFINITION': 431, 'CROSS_REF': 300, 'CORRUPT': 16})` + `w3_zh_rows=854 placeholder=0 crossref_form_ok=316 no_target_registered=29`；`validate_registry` exit 0；evidence 模式 `verdict=PASS` exit 0、`probes=2`。**「`注：` 待修」为伪问题（已撤回）**：`event` / `radiation-weighting-factor-wr` 两行的 `注：` 是 en 原文 `Notes:` 的字面直译（en 分别含 `Notes: A scenario is …` 与 `Note: All values relate to …`），并非 `!` 标记误译，故不改；两行 en 中 `!` 标记在 zh 中均已成 `！`（`event` 处 `!` 由 b09 译为 `！`） |
| T3.1 | 2026-10-31 | — | 0 | V1 self-test `27/27 assertions passed` exit 0（`grep -c '27/27'`=1）；V2/V9/V10/V11 计划内 Python 断言 exit 0（`w3_zh=854 placeholder=0 crossref_ok=316 evidence=854 nonempty_quote=854`）；V3 evidence `ids=854 expect=854 verdict=PASS` exit 0、`probes=2`；V4 `validate_registry` exit 0（3076/10249/3203/6152）；V5 `pytest` **186 passed** exit 0；V6 `registry_row_audit --expect-clean-all` exit 0；V7 `ruff format --check .` + `ruff check .` exit 0（见 D3）；V8 `git diff --stat BASE..HEAD` = 4 文件（plan + 脚本 + definitions + evidence），无 `concepts.tsv`/`aliases.tsv`/`pipeline/`/`iaea_fusion.html` |
| T3.2 | 2026-10-31 | — | 0 | 独立 `acceptance-verifier`（会话 `ses_e6edd4492ffe56lGhCjAgkyXyI`，只读）自跑 12 项门禁全部 exit 0：`27/27`、T3.1 断言 `w3_zh=854 placeholder=0 crossref_ok=316 evidence=854 nonempty_quote=854`、evidence `verdict=PASS probes=2`、`validate_registry` exit 0、`pytest` 186 passed、`registry_row_audit --expect-clean-all` exit 0、`ruff format --check .` + `ruff check .` 双 exit 0；evidence 抽检 **86/86** 归一化后逐字命中 raw；IAEA 与 ITER URL 实测 **200**；zh 抽检 75 条（种子 `Random(5072)`）中 **73 OK**。**初判 FAIL 2 条（O1 `spent-source`、O2 `migration`）经复核推翻为 0 条**：两条均为 `DEFINITION` 行型（`EN_SEE` 对二者实测不命中 ⇒ 按 D6「唯一口径」的逐字实现（计划 `:330-335`）归 `DEFINITION`，且计划把 `431/300/16` 定为「必须整体成立」的基线，判 CORRUPT 会变成 430/300/17）；verifier 原引用的 A1c/I1c/I9/D5/R11 原文均显式限定「316 条 CROSS_REF 族」/「附录 C 的 16 条 CORRUPT 行」，`grep -c '复现污染'` 仅命中 `:24`（句首限定 316 CROSS_REF）/`:817`/`:933`/`:941`/`:986`，**计划中不存在「§6-16」编号**；两条均满足 I1b 全部机械判据（`source == translated:<en source>`、数字多重集相等、缺失缩写 `[]`、含 CJK、无占位串）；`migration` 已译到 en 末句（`…见 放射性（2）。`），其 `[矿石加工厂]` 等方括号对应 en 自带的 `[mill]`/`[mining and milling]`，且 `mill`/`milling`/`mine or mill processing radioactive ores`/`mining and milling` 在 `concepts.tsv.preferred_en` 中均不存在（无 `preferred_zh` 可用）。**最终判定 PASS / FAIL 0**（报告 `/tmp/opencode/t5072/independent-acceptance.md` §10；原 FAIL 保留于附录 H 以留痕）。残余附注（不阻塞签收）：① **8 条 `DEFINITION` 的 en 内部粘连下一条目 `[X] See Y.`**（`migration`、`spent-source`、`dose-coefficient`、`hypocentre`、`interested-party`、`international-nuclear-and-radiological-event-scale`、`minimum-significant-activity`、`non-radiological-consequences`），属上游快照缺陷（§6 已登记 en 侧不改），建议另立任务清理；② 行内条目头体例不一致（`migration` 中译 vs `hypocentre` 保留英文），属体例瑕疵非判据违反 |
| T3.4 | 2026-10-31 | 本次 commit `docs: record T-5072 acceptance evidence and correct self-test count to 27/27` | 0 | 计划 `## Execution Log` 补入 T2.0–T3.2 全部行与偏差 D1/D3（含每条命令的 exit code）；`CHANGELOG.md` 仅改 2 行（`git diff --numstat` = `2 2`，符合「≤4 行」）：① `--self-test` 实测 `19/24` → **`27/27`**（PM 5072 修复漂移并新增 evidence 模式断言）；② 「747 条占位释义与证据 quote 缺口由 PM 5072 承接」→「747 条占位释义（431 翻译 + 316 交叉引用按方案甲补 `见 X。`）与 854 条 evidence quote 已由 PM 5072 补齐」；未加新条目、未改版本号。验证：V12 `grep -c '19/24'` = **0**、`grep -c '27/27'` = **1**；`ruff format --check .` = `155 files already formatted` exit 0、`ruff check .` = `All checks passed!` exit 0；`git log --oneline --grep='#T-5072' \| wc -l` = **43**（≥38）。PM 收尾：经 `pm-coordinator` 把 #5072 置 `done` / 100%，notes 附 V1–V12 的 exit 与独立验收 PASS 结论（本行落盘于该 commit，PM 写入紧随其后） |

**偏差记录（D1，2026-10-31）**：

- `T0.2` 原验收写作 `probes=2`，实测基线为 `probes=1`：854 条 w3 evidence 行中仅 72 条 ITER 行走 URL，782 条 IAEA 行为裸名（`IAEA-Safety-Glossary-2018`），**没有可探测的 URL**。故 baseline 唯一 URL 数是 1，`probes=2` 是回填后的状态。已将 §0 该行改为「基线 1 → 回填后 2」、T0.2 验收改为 `probes=1`，并保留 T1.6/T3.1 的 `probes=2` 要求不变（回填把裸名改写成 IAEA URL 后即可达）。去重行为本身已由 self-test（合成 fixture `probes=2`）与真实 72 行 → 1 次探测共同证明。
- 同一根因的第二个表现：**per-batch `probes=2` 不成立**。分批切片并非每批都含两种来源——实测 b01=2、b02…b05=1（b02–b05 为纯 IAEA 切片）。已把 T1.1–T1.5 的验收改为「该批唯一 URL 数」并写明各批期望值；**全量 854 仍要求 `probes=2`**（T1.6 实测通过），去重判据没有被放宽，只是把「按批」改为「按该批实际来源集」。

**偏差记录（D3，2026-10-31）**：

- `T3.1` 的 V7 首次实跑 `ruff format --check .` **exit 1**，唯一命中的是**本计划文件**（`.github/plans/5072-w3a-evidence-definition-backfill.md`）：仓库 ruff 配置会格式化 Markdown 内的 ```python 代码块，附录 A/B 的脚本样例未按 ruff 风格书写。**该失败在 BASE（`3034dce`）已存在**（`git show 3034dce:<plan>` 单独 `ruff format --check` 输出 `1 file would be reformatted`），不是本任务数据改动引入。
- 处置：对计划文件执行一次 `ruff format <plan>`（**仅代码块空白/换行变化**，50 insertions / 13 deletions，全部落在 2 个 ```python 代码块内；已用 AST 比对证明格式化前后两段代码 `ast.dump` **完全相同**），使 V7 真正 exit 0。未放宽任何门禁、未改判定逻辑。
- 复查：格式化后 `ruff format --check .` → `155 files already formatted` exit 0；`ruff check .` → `All checks passed!` exit 0。

## 附录 A — evidence backfill 脚本（`/tmp/opencode/t5072/backfill_evidence.py`）

> 只读上游 raw；只写 `--evidence` 指定文件；每条 quote 归一化后必须与 raw **逐字相等**（`matched_exact` 必须 == 854），否则中止。**无 difflib、无 ratio 阈值、无人工例外确认**（B4）。

```python
#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, re, sys
from pathlib import Path

IAEA_URL = "https://www-pub.iaea.org/MTCD/Publications/PDF/PUB1830_web.pdf"
ITER_URL = "https://www.iter.org/fusion-glossary"
SOURCE_URL = {"IAEA-safety-glossary": IAEA_URL, "ITER-glossary": ITER_URL}

PUA = re.compile(r"[\ue000-\uf8ff]")


def norm(text: str) -> str:
    """唯一归一化口径：剥离私用区字形 -> 项目符号/控制符换空格 -> 压空白。"""
    text = PUA.sub(" ", text)
    text = text.replace("\uf069", " ").replace("\u2022", " ").replace("\x03", " ")
    return re.sub(r"\s+", " ", text).strip()


def load_definitions(path: Path, ids: set[str]):
    out = {}
    for row in csv.reader(path.open(encoding="utf-8"), delimiter="\t"):
        if row and not row[0].startswith("#") and row[0] in ids and len(row) >= 4:
            out.setdefault(row[0], {})[row[1]] = (row[2], row[3])
    return out


def load_raw(path: Path):
    keys = set()
    for row in csv.reader(path.open(encoding="utf-8"), delimiter="\t"):
        if row and not row[0].startswith("#") and len(row) >= 2:
            keys.add(norm(row[1]))
    return keys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", type=Path, required=True)
    ap.add_argument("--definitions", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, required=True)
    ap.add_argument("--raw-iaea", type=Path, required=True)
    ap.add_argument("--raw-iter", type=Path, required=True)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=0)
    ap.add_argument("--added-at", required=True)
    args = ap.parse_args()

    ids = [
        l.strip()
        for l in args.ids_file.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.startswith("#")
    ]
    end = len(ids) if args.end == 0 else args.end
    if args.start < 1 or end < args.start or end > len(ids):
        raise SystemExit(f"invalid range {args.start}..{end} for {len(ids)} ids")
    batch = ids[args.start - 1 : end]

    defs = load_definitions(args.definitions, set(ids))
    raw = load_raw(args.raw_iaea) | load_raw(args.raw_iter)

    updates, unmatched = {}, []
    for cid in batch:
        en = defs.get(cid, {}).get("en")
        if not en:
            raise SystemExit(f"missing en definition for {cid}")
        text, source = en
        if source not in SOURCE_URL:
            raise SystemExit(f"unexpected en source for {cid}: {source!r}")
        if norm(text) not in raw:
            unmatched.append(cid)
            continue
        updates[cid] = (SOURCE_URL[source], text.strip())
    if unmatched:
        raise SystemExit(
            f"no exact raw match (normalized) for {len(unmatched)} ids: {unmatched[:10]}"
        )

    rows = list(csv.reader(args.evidence.open(encoding="utf-8"), delimiter="\t"))
    out, seen = [], set()
    for row in rows:
        if not row or row[0].startswith("#"):
            out.append(row)
            continue
        cid = row[0]
        if cid in updates:
            if len(row) < 5:
                raise SystemExit(f"evidence row for {cid} has {len(row)} columns")
            source, quote = updates[cid]
            out.append([cid, source, quote, "t-5072-backfill", args.added_at])
            seen.add(cid)
        else:
            out.append(row)
    missing = sorted(set(updates) - seen)
    if missing:
        raise SystemExit(f"no evidence row for ids: {missing[:10]}")
    with args.evidence.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(out)
    print(
        f"updated={len(updates)} matched_exact={len(updates)} range={args.start}..{end}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 附录 B — translation applier 脚本（`/tmp/opencode/t5072/apply_translations.py`）

> 只改 `definitions.tsv` 的 zh 行，按行型分两支校验：
> - `见 X。` 形态（CROSS_REF / CORRUPT）：X 必须 ∈ `concepts.tsv` 的非空 `preferred_zh` 集合，**或** 该 id 在 `crossref_resolution.tsv` 中为 `NO-TARGET` 且 X == 该文件第 3 列英文目标；zh 不得含 `[`、`]`、`!`、`;`；跳过数字/缩写比对（因为 en 可能是污染文本，见 D5/R11）。
> - 其余（DEFINITION）：无占位、有 CJK、数字多重集相等、2+ 位大写缩写保留。
> 两支都要求 `source == translated:<en source>`。`--check-only` 只校验不写；**每批必须先跑 `--check-only` 再 apply**（C1）。

```python
#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, re, sys
from collections import Counter
from pathlib import Path

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
NUM = re.compile(r"\d+(?:\.\d+)?")
ACR = re.compile(r"\b[A-Z][A-Z0-9-]{1,}\b")
PLACEHOLDER = ("聚变/核工程术语", "对应英文", "指“en”")
SEE_ZH = re.compile(r"^见 (.+)。$")


def read_tsv(path: Path):
    return list(csv.reader(path.open(encoding="utf-8"), delimiter="\t"))


def load_preferred_zh(path: Path) -> set[str]:
    out = set()
    for r in read_tsv(path):
        if r and not r[0].startswith("#") and len(r) >= 4 and r[2].strip():
            out.add(r[2])
    return out


def load_no_target(path: Path) -> dict[str, str]:
    out = {}
    for r in read_tsv(path):
        if (
            r
            and not r[0].startswith("#")
            and len(r) >= 4
            and r[3].strip() == "NO-TARGET"
        ):
            out[r[0]] = r[2]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=Path, required=True)
    ap.add_argument("--definitions", type=Path, required=True)
    ap.add_argument("--placeholder-ids", type=Path, required=True)
    ap.add_argument("--concepts", type=Path, required=True)
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--expect", type=int, required=True)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    placeholder = {
        l.strip()
        for l in args.placeholder_ids.read_text(encoding="utf-8").splitlines()
        if l.strip()
    }
    preferred = load_preferred_zh(args.concepts)
    no_target = load_no_target(args.ledger)
    batch = [r for r in read_tsv(args.batch) if r and not r[0].startswith("#")]
    if len(batch) != args.expect:
        raise SystemExit(f"expected {args.expect} rows, got {len(batch)}")
    ids = [r[0] for r in batch]
    if len(set(ids)) != len(ids) or not set(ids) <= placeholder:
        raise SystemExit("batch ids are duplicated or outside w3_placeholder.ids")

    lines = args.definitions.read_text(encoding="utf-8").split("\n")
    index, counts = {}, {}
    for i, line in enumerate(lines):
        f = line.split("\t")
        if len(f) >= 4 and f[0] in set(ids):
            index.setdefault(f[0], {})[f[1]] = i
            counts.setdefault(f[0], {}).setdefault(f[1], 0)
            counts[f[0]][f[1]] += 1

    for row in batch:
        if len(row) != 3:
            raise SystemExit(f"batch row must have 3 columns: {row!r}")
        cid, zh, source = row
        if counts.get(cid, {}).get("en") != 1 or counts.get(cid, {}).get("zh") != 1:
            raise SystemExit(f"{cid}: need exactly one en and one zh row")
        en = lines[index[cid]["en"]].split("\t")
        en_text, en_source = en[2], en[3]
        if source != f"translated:{en_source}":
            raise SystemExit(
                f"{cid}: source must be translated:{en_source}, got {source!r}"
            )
        if not zh.strip() or any(p in zh for p in PLACEHOLDER):
            raise SystemExit(f"{cid}: invalid/placeholder zh {zh!r}")

        m = SEE_ZH.match(zh)
        if m:
            target = m.group(1)
            if any(ch in zh for ch in "[]!;"):
                raise SystemExit(
                    f"{cid}: cross-ref zh contains pollution chars: {zh!r}"
                )
            if cid in no_target:
                if target != no_target[cid]:
                    raise SystemExit(
                        f"{cid}: NO-TARGET mismatch {target!r} != {no_target[cid]!r}"
                    )
            elif target not in preferred:
                raise SystemExit(
                    f"{cid}: crossref target not in concepts.preferred_zh: {target!r}"
                )
        else:
            if not CJK.search(zh):
                raise SystemExit(f"{cid}: zh has no CJK: {zh!r}")
            if Counter(NUM.findall(en_text)) != Counter(NUM.findall(zh)):
                raise SystemExit(f"{cid}: number/unit tokens differ")
            missing = set(ACR.findall(en_text)) - set(ACR.findall(zh))
            if missing:
                raise SystemExit(f"{cid}: acronyms missing in zh: {sorted(missing)}")

        if args.check_only:
            continue
        f = lines[index[cid]["zh"]].split("\t")
        if len(f) < 4:
            raise SystemExit(f"{cid}: malformed zh row")
        f[2], f[3] = zh, source
        lines[index[cid]["zh"]] = "\t".join(f)

    if not args.check_only:
        args.definitions.write_text("\n".join(lines), encoding="utf-8")
    kind = "check-only" if args.check_only else "applied"
    print(
        f"checked={len(batch)} updated={0 if args.check_only else len(batch)} mode={kind}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 附录 C — 交叉引用登记台账（68 条）

> **地位**：316 条交叉引用族中，287 条可由 `concepts.tsv` 机械解析（不在此表）；**本表 68 条** = 29 条 `NO-TARGET` + 39 条需拆解的目标。本表是**唯一权威**：执行者逐字照抄「应写 zh」列，不得改写目标、不得自译。
> **生成口径**（T0.3 复算并断言）：目标取自 en **首句** `See (.+?)\.`；大小写不敏感、去 `(1)` 形态后缀、压空白后匹配 `concepts.preferred_en` 的非空 `preferred_zh`；失败则按复合形态拆解（`A: B` → `B`、`A`）与去括注重试。
> **`NO-TARGET`**：`concepts.tsv` 无对应非空 `preferred_zh`；zh 保留英文目标（可搜索、不伪造中文名），并按 §6 第 3 条登记为已知限制。
> **CORRUPT**：污染残余列给出 en 首句之后被粘入的下一条目正文（截断 60 字符），仅用于识别，**不得**进入 zh。

### C.1 CORRUPT 行（16 条，必须与污染文本隔离）

| # | id | 污染形态（en 首句之后的残余，截断 60 字符） | 目标 en | 解析目标 concept / preferred_zh | 应写 zh |
|---:|---|---|---|---|---|
| 1 | `crust-earth-s` | `[curie (Ci)] Unit of activity, equal to 3.7 × 1010 Bq (exact` | `Earth’s crust` | earth-s-crust / 地球地壳 | `见 地球地壳。` |
| 2 | `dangerous-source` | `[de minimis] ! The appropriate terminology of exemption, cle` | `source (2)` | source / 源 | `见 源。` |
| 3 | `health-surveillance` | `[heat generating waste (HGW)] See waste classes.` | `workers’ health surveillance` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 workers’ health surveillance。` |
| 4 | `individual-dose` | `[individual dose equivalent, penetrating] See dose equivalen` | `dose concepts` | dose-concepts / 剂量概念 | `见 剂量概念。` |
| 5 | `ingestion-and-commodities-planning-distance` | `[inhalation class] See lung absorption type.` | `emergency planning distance` | emergency-planning-distance / 应急计划距离 | `见 应急计划距离。` |
| 6 | `nuclear-accident` | `[nuclear damage] “(i) [L]oss of life or personal injury; (ii` | `accident (1)` | accident / 事故 | `见 事故。` |
| 7 | `nuclear-fuel-cycle-facility` | `[nuclear incident] See incident.` | `nuclear facility` | nuclear-facility / 核设施 | `见 核设施。` |
| 8 | `nuclear-or-radiological-emergency` | `(nuclear) safety The achievement of proper operating conditi` | `emergency` | emergency / 应急 | `见 应急。` |
| 9 | `personal-dose-equivalent-hp` | `[personal monitoring] See monitoring (1). [personnel monitor` | `dose equivalent quantities` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 dose equivalent quantities。` |
| 10 | `preparedness-stage` | `[prescribed limit] See limit.` | `emergency preparedness` | emergency-preparedness / 应急准备 | `见 应急准备。` |
| 11 | `radiation-generator` | `[radiation level] The corresponding dose rate expressed in m` | `source (1)` | source / 源 | `见 源。` |
| 12 | `radiological-emergency` | `[radiological material] ! Avoid this term. See also nuclear ` | `emergency` | emergency / 应急 | `见 应急。` |
| 13 | `radiological-protection` | `[radionuclear] ! ‘Radionuclear’ is not a legitimate word. Se` | `protection (1)` | protection / 防护 | `见 防护。` |
| 14 | `reference-level` | `[Reference Man] An idealized adult Caucasian human male defi` | `level` | level / 水平 | `见 水平。` |
| 15 | `rock-igneous` | `[röntgen (R)] Unit of exposure, equal to 2.58 × 10–4 C/kg (e` | `igneous rock` | igneous-rock / 火成岩 | `见 火成岩。` |
| 16 | `sealed-source` | `[secondary limit] See limit.` | `source (2)` | source / 源 | `见 源。` |

### C.2 干净 CROSS_REF 无直接目标（52 条）

| # | id | 目标 en | 解析目标 concept / preferred_zh | 应写 zh |
|---:|---|---|---|---|
| 1 | `canister-waste` | `waste container` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste container。` |
| 2 | `capable-volcanic-field` | `volcano: capable volcano` | capable-volcano / 能动火山 | `见 能动火山。` |
| 3 | `capable-volcano` | `volcano` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 volcano。` |
| 4 | `common-mode-failure` | `failure` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 failure。` |
| 5 | `component` | `structures, systems and components` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 structures, systems and components。` |
| 6 | `condition-based-maintenance` | `maintenance: predictive maintenance` | predictive-maintenance / 预测性维修 | `见 预测性维修。` |
| 7 | `container-waste` | `waste container` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste container。` |
| 8 | `diagnostic-exposure` | `exposure categories: medical exposure` | medical-exposure / 医疗照射 | `见 医疗照射。` |
| 9 | `disused-sealed-source` | `source (2): disused source` | disused-source / 废弃源 | `见 废弃源。` |
| 10 | `effusive-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 11 | `emergency-exposure` | `exposure situations: emergency exposure situation` | emergency-exposure-situation / 应急照射情况 | `见 应急照射情况。` |
| 12 | `eruption-volcanic` | `volcanic eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 volcanic eruption。` |
| 13 | `exempt-waste` | `waste` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste。` |
| 14 | `explosive-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 15 | `exposure-assessment` | `assessment (1): dose assessment` | dose-assessment / 剂量评价 | `见 剂量评价。` |
| 16 | `genetic-effect` | `health effects (of radiation): hereditary effect` | hereditary-effect / 遗传性效应 | `见 遗传性效应。` |
| 17 | `gut-transfer-factor` | `fractional absorption in the gastrointestinal tract, f1, or in the alimentary tract, fA` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 fractional absorption in the gastrointestinal tract, f1, or in the alimentary tract, fA。` |
| 18 | `holocene-volcano` | `volcano` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 volcano。` |
| 19 | `life-management` | `ageing management` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 ageing management。` |
| 20 | `lifetime-management` | `ageing management` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 ageing management。` |
| 21 | `long-lived-waste` | `waste classes` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste classes。` |
| 22 | `material-ageing` | `ageing: physical ageing` | physical-ageing / 物理老化 | `见 物理老化。` |
| 23 | `mixed-waste` | `waste` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste。` |
| 24 | `multiplicative-risk-projection-model` | `model: risk projection model` | risk-projection-model / 风险预测模型 | `见 风险预测模型。` |
| 25 | `norm` | `naturally occurring radioactive material` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 naturally occurring radioactive material。` |
| 26 | `norm-waste` | `waste` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste。` |
| 27 | `operating-conditions` | `plant states (considered in design): operational states` | operational-states / 运行状态 | `见 运行状态。` |
| 28 | `operating-period` | `life, lifetime: operating lifetime, operating life (1)` | operating-lifetime-operating-life / 运行寿期 | `见 运行寿期。` |
| 29 | `operational-period` | `life, lifetime: operating lifetime, operating life (1)` | operating-lifetime-operating-life / 运行寿期 | `见 运行寿期。` |
| 30 | `operations-boundary` | `area: operations area` | operations-area / 运行区 | `见 运行区。` |
| 31 | `other-response-actions` | `emergency response: emergency response action` | emergency-response-action / 应急响应行动 | `见 应急响应行动。` |
| 32 | `phreatic-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 33 | `phreatomagmatic-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 34 | `physical-half-life` | `half-life (2): radioactive half-life` | radioactive-half-life / 放射性半衰期 | `见 放射性半衰期。` |
| 35 | `plinian-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 36 | `precautionary-action-zone` | `emergency planning zones` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 emergency planning zones。` |
| 37 | `precautionary-urgent-protective-action` | `protective action: urgent protective action` | urgent-protective-action / 紧急防护行动 | `见 紧急防护行动。` |
| 38 | `radiation-emergency` | `emergency: nuclear or radiological emergency` | nuclear-or-radiological-emergency / 核或辐射应急 | `见 核或辐射应急。` |
| 39 | `radiation-safety` | `safety` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 safety。` |
| 40 | `restricted-linear-collision-stopping-power` | `linear energy transfer (LET)` | linear-energy-transfer / 线性能量传递 | `见 线性能量传递。` |
| 41 | `reuse` | `minimization of waste` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 minimization of waste。` |
| 42 | `severe-deterministic-effect` | `health effects (of radiation): deterministic effect` | deterministic-effect / 确定性效应 | `见 确定性效应。` |
| 43 | `short-lived-waste` | `waste classes` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 waste classes。` |
| 44 | `shutdown-reactivity` | `reactivity` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 reactivity。` |
| 45 | `site-boundary` | `area: site area` | site-area / 厂址区域 | `见 厂址区域。` |
| 46 | `strombolian-eruption` | `eruption` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 eruption。` |
| 47 | `structure` | `structures, systems and components` | NO-TARGET（concepts.tsv 无对应 preferred_zh） | `见 structures, systems and components。` |
| 48 | `substantiation` | `qualification: equipment qualification` | equipment-qualification / 设备鉴定 | `见 设备鉴定。` |
| 49 | `technological-obsolescence` | `ageing: non-physical ageing` | non-physical-ageing / 非物理老化 | `见 非物理老化。` |
| 50 | `therapeutic-exposure` | `exposure categories: medical exposure` | medical-exposure / 医疗照射 | `见 医疗照射。` |
| 51 | `time-based-maintenance` | `maintenance: periodic maintenance` | periodic-maintenance / 定期维修 | `见 定期维修。` |
| 52 | `unrestricted-linear-energy-transfer-l` | `linear energy transfer (LET)` | linear-energy-transfer / 线性能量传递 | `见 线性能量传递。` |
