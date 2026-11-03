---
plan_schema_version: "1.0"
linked_spec: null
scope_mode: "HOLD"
generated_at: "2026-11-02T15:40:00+08:00"
git_commit: "115da749251f6a8c94e8a1d4ea0ce3c412c614bf"
mode: "improve"
revision: "4 (CLOSEOUT: 20 Task 全部执行完成并独立验收 PASS；执行区间固化 115da74..3d54c3e；计划归档至 completed/；见 §Execution Log E2)"
status: "completed"
pm_task: "5184"
project: "FUSION-TERMS (id240)"
title: "四阶段收口：状态回写 → 术语冲突查证 → 小样目视核验 → 分批语义抽检"
files_sha256:
  terms/registry/concepts.tsv: "auto (执行时重测)"
  terms/registry/definitions.tsv: "auto (执行时重测)"
  terms/registry/evidence.tsv: "auto (执行时重测)"
  terms/registry/aliases.tsv: "auto (执行时重测)"
  .github/plans/terminology-coverage-and-definition-quality.md: "auto (执行时重测)"
  .github/plans/5072-w3a-evidence-definition-backfill.md: "auto (执行时重测)"
---

# Plan: 四阶段收口（PM #5184 / FUSION-TERMS id240）

> **Status**: COMPLETED（2026-11-03 收口；`date` 实测 `Tue Nov  3 03:06:54 PM CST 2026`）——**20 个 Task 全部执行并提交**，执行区间 **`115da74..3d54c3e`**，独立验收（acceptance-verifier，`/tmp/opencode/t5184-final-acceptance.md`）**V1–V9 全 PASS**，探针 P1 `--self-test` = 27/27、P2 `pytest -q` = 178 passed。父计划 **M4 已勾（10/10 PASS）；M1 保持未勾（55 PASS / 9 FAIL / 0 UNDECIDABLE，未达 64/64）；M3 保持未勾（`待用户裁决 (D2)`）**。计划文件已按完成计划归档规则移至 `.github/plans/completed/5184-four-stage-closeout.md`。
> **历史状态（保留，勿抹）**：初始 2026-11-02 为 ACTIVE；2026-11-03 IMPROVE-1 阶段为 `T1.2 AC FAIL / 未完成`，见下行与 §Execution Log E1。
> **本计划只做四件事，且按用户批准的顺序串行**：**S1 状态回写 → S2 术语冲突查证 → S3 小样目视核验 → S4 分批语义抽检**。
> **四阶段的共同性质**：**除 `docs/reviews/t5184/` 下的报告与状态行外，不写任何数据**。`terms/`、`artifacts/`、`pipeline/`、`scripts/` 四阶段全程只读（S1/S2/S3/S4 均逐条断言 `git diff --stat -- terms/ artifacts/ pipeline/ scripts/` 为空）。
> **每阶段独立 commit，commit message 必带 `#T-5184`，不 push。**
> **状态只勾证据确凿项**：M1/M3/M4 三个未勾项的勾选只允许发生在「产出该证据的那个阶段」，且必须过本计划该阶段的机械 AC；发现 FAIL 时**不得**转写为 PASS，只登记缺陷并保持未勾选。
> **IMPROVE-1（2026-11-03，`date` 实测 `2026-11-03T08:40:56+08:00`；`git rev-parse HEAD` = `52dc8e8`）**：T1.2 的 commit `52dc8e8` **已生成但 AC 未通过**（旧 AC#5 对「内容以 `- ` 开头的行」空转，且词白名单未容纳 §5072 被删旧行 ⇒ 不可满足）⇒ **T1.2 未完成**，T1.3 / S2–S4 **不得启动**。本轮只修正该机械 AC 与「先验收、后提交」门控，并在 §Execution Log E1 如实登记；未改数据、未改 `52dc8e8`、未产生新 commit。

## 背景与目标

- **问题/需求描述（用户 2026-11-02 批准的顺序，父代理委派 prompt 原文）**：
  1. **状态回写**；
  2. **术语冲突查证**（`physical-sputtering` / `物理溅射` 同时是 `sputtering` 的 zh 别名）；
  3. **小样目视核验**（T0.4 的 99 行 + T0.5 的 80 行修复后 10 行列语义）；
  4. **分批语义抽检**（W1 共 39 批 / 756 ids，每 5 批组 ≥8 行**确定性**样本）。
- **要消除的现状错误（均已实测，见下 §事实基线）**：
  - 父计划 §Manual 的 **M1/M3/M4 三项仍未勾选**（`terminology-coverage-and-definition-quality.md:979/981/982`），但**没有任何一份收口报告**说明「为什么未勾、缺什么证据、谁去补」。
  - **5072 计划 frontmatter `status: "active"`，而同文件 Execution Log 的 T3.2/T3.4 记录独立验收 PASS 且 PM 已置 done/100%** — 状态与日志不一致。
  - **5072 的数据（`definitions.tsv` / `evidence.tsv`）不在任何 tag 内**（`git tag --contains d84aabc` = 0 / `git tag --contains 115da74` = 0；`git diff --stat v2026.10.30 HEAD -- terms/registry/` 显示 definitions 1494 行 + evidence 1708 行变更）⇒ **不得宣称 5072 数据已发布**。
  - **`5110` / `v2026.10.30` 已发布**（tag `fa34be1`，`origin/master` 含该 tag，`dist/fusion-terms-artifacts-v2026.10.30.tar.gz(+.sha256)` 在库，`verify_release_contract --root dist/stage/v2026.10.30` → `contract OK: terms=6375 version=v2026.10.30 commit=fa34be1f6d6d`）⇒ **无需重发**（用户指示）。
- **目标（二元可判）**：
  1. `docs/reviews/t5184/` 存在且含四份可审计产物（README + 状态回写 + M3 查证 + M4 目视 + M1 抽检）；
  2. 5072 状态字段与日志一致，且明确写入「数据未进入任何发布 tag」；
  3. `physical-sputtering` 冲突有**证据 + 裁决建议**（**不修数据**，交用户裁决）；
  4. M4 的 10 行目视留痕（含逐列判定）；
  5. M1 的 8 组 × 8 行 = 64 行语义抽检留痕，且每行都能回溯到**原文/上下文**（`notes` 逐字 或 上游 raw 行 或 URL+日期）；
  6. M1/M3/M4 的勾选状态与证据严格对应。
- **非目标（本计划明确不做）**：
  - ⛔ **不修任何 aliases / concepts / definitions / evidence 数据**。S2 只输出「证据 + 裁决建议」，修复需用户裁决。
  - ⛔ **不重发、不改 `v2026.10.30`**（用户指示：已发布无需重发）。
  - ⛔ **不宣称 5072 数据已发布**（无 tag 包含其提交）。
  - ⛔ **不把 `spent-source` / `migration` 等 W3 上游 en 粘连缺陷计入 W1 承诺**（实测二者均**不在** W1 的 39 个批次清单内：`grep -lx spent-source .github/plans/t4973-batches/w1_*_b*.ids` 为空；二者在 `w3.ids` 内 = 1/1）。它们属 5072 §6 已登记的上游快照缺陷，本计划仅引用、不修复、不追加承诺。
  - ⛔ 不新增/修改 `scripts/`、`pipeline/`、CI 配置；不重写父计划正文；不归档父计划。
  - ⛔ 不 `git push`；不动 `iaea_fusion.html`（未跟踪）与 `.opencode/`。

## 事实基线（2026-11-02 实测；执行时逐阶段重测，禁止沿用）

| # | 断言 | 实测值 | 复现命令（仓根） |
|---|------|--------|------------------|
| B1 | HEAD | `115da749251f6a8c94e8a1d4ea0ce3c412c614bf` | `git rev-parse HEAD` |
| B2 | 工作区 | 仅未跟踪 `iaea_fusion.html`（不得提交） | `git status --porcelain` |
| B3 | registry 规模 | `validate_registry` exit 0（3076 concepts / 6152 definitions / 3203 evidence） | `.venv/bin/python -m pipeline.validate_registry` |
| B4 | 结构+W1 质量门禁 | `is_clean: true`、`non_zero_metrics: {}` | `.venv/bin/python scripts/registry_row_audit.py --audit` |
| B5 | 批验收自检 | `27/27 assertions passed`、exit 0 | `.venv/bin/python scripts/registry_batch_verify.py --self-test` |
| B6 | W1 批次规模 | **39 个批次文件 / 756 个唯一 id** | `ls .github/plans/t4973-batches/w1_*_b*.ids \| wc -l`；`cat .github/plans/t4973-batches/w1_*_b*.ids \| sort -u \| wc -l` |
| B7 | W1 definitions | 1512 行（en+zh 各 756）；`聚变/核工程术语` 占位 **0** | 见 §S4 T4.1 step 0 |
| B8 | W1 来源分布 | `corpus` 1329 / `GB/T-4960.9` 133 / URL 与 `ITER-glossary`+`IAEA-safety-glossary` 50 | 见 §S4 T4.1 step 0 |
| B9 | 未勾项 | M1 `:979`、M3 `:981`、M4 `:982` 均为 `- [ ]` | `grep -n '^- \[ \] M[134]:' .github/plans/terminology-coverage-and-definition-quality.md` |
| B10 | zh 串冲突全集 | **恰好 1 条**：`物理溅射` → alias of `sputtering`，同时是 `physical-sputtering` 的 `preferred_zh` | 见 §S2 T2.1 扫描脚本 |
| B11 | 5072 状态 | frontmatter `status: "active"`；日志 T3.2 = 独立验收 PASS | `sed -n '10p' .github/plans/5072-w3a-evidence-definition-backfill.md` |
| B12 | 5072 未发布 | `git tag --contains d84aabc` = 0；`git tag --contains 115da74` = 0 | 同左 |
| B13 | 5110 已发布 | tag `v2026.10.30` → `fa34be1`；`contract OK: terms=6375` | `git rev-parse --short v2026.10.30^{commit}`；`.venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.30` |
| B14 | T0.4/T0.5 修复映射表 | `category-map-shift99.tsv` = 99 数据行（+1 表头）；`category-map-sixcol80.tsv` = 80 数据行（+1 表头） | `wc -l .github/plans/t4973-batches/category-map-{shift99,sixcol80}.tsv` |
| B15 | 规范 category 白名单 | 16 类（`concept,nuclear-fusion,metric,method,code,device,system,material,diagnostic,company,organization,doc,limit,effect,facility,principle`） | `pipeline/validate_registry.py` |

## 需求分解（CoT Stage 1）

```text
REQUIREMENT（父代理委派 prompt 原文要点）
  按用户批准顺序执行四阶段：状态回写 → 术语冲突查证 → 小样目视核验 → 分批语义抽检；
  只写新计划 .github/plans/5184-four-stage-closeout.md；不改数据；
  状态只勾证据确凿项；冲突阶段默认只出证据裁决建议、不授权 aliases 修复；
  语义抽检须原文/上下文人工复核，不能仅脚本；每 5 批组 ≥8 行确定性样本；
  分 ≤15min checkpoints；report/样本写 docs/reviews/t5184/；每阶段独立 commit #T-5184、不 push。
↓
CONSTRAINTS
  1) 四阶段严格串行（S1 的状态行是 S2/S3/S4 的证据索引；S2/S3/S4 各自只动自己的状态行）。
  2) 数据只读：terms/ artifacts/ pipeline/ scripts/ 零 diff（逐阶段 git diff 断言）。
  3) 状态写入必须与证据一一对应：无证据不勾；`FAIL`/`UNDECIDABLE` 不转 PASS；已发布/未发布不得对调。
  4) 抽样必须确定性（sha256 排序 + 样本集 sha256 落盘），不得"随机挑看着顺眼的"。
  5) 语义判定只用三值 `PASS|FAIL|UNDECIDABLE`；必须逐条给出**原始语料 + 定义文本 + 适用性推理**；真实源不可得一律 `UNDECIDABLE`，禁止代理指标（文本出现/文本去重）替代语义判断。
  6) 不为通过而虚构证据：仓内上游快照无某串 ≠ 上游否定某用法；无网/无条目一律记 UNDECIDABLE。
↓
BOUNDARY
  IN：docs/reviews/t5184/{README,status-writeback,m3-*,m4-*,m1-*}.md|tsv；
      父计划 M1/M3/M4 三行状态文字（仅这三行 + 一条 S1 索引行）；
      5072 frontmatter status + 一条日期化状态注记；PM #5184 备注（经 pm-coordinator）。
  OUT：所有 terms/ 数据；aliases 修复；5110 重发；5072 数据发布声明；W3 缺陷修复；
       新增脚本；父计划其他章节；push；归档父计划。
↓
ACCEPTANCE（二元）
  A1 四份报告齐备且每份有机械可跑的完整性断言；
  A2 **20 个 Task 各 1 个 commit**、均含 #T-5184、均未 push、均只含该 Task 声明文件；
  A3 M1/M3/M4 的勾选状态 == 证据状态（M3 允许"查证完成但仍待用户裁决"⇒ 保持未勾；M1/M4 仅当全 PASS 才勾）；
  A4 64 行抽检每行含原始语料/定义文本/适用性推理/三值判定；FAIL+UNDECIDABLE 数 == 待定台账行数。
```

## 假设清单（CoT Stage 2）

1. `[假设]` W1 = `w1_a`(4 批, 67 ids) + `w1_b`(34 批, 679) + `w1_c`(1 批, 10) = **39 批 / 756 ids**；「每 5 批组」的**唯一口径**为：按 `a01..a04, b01..b34, c01` 顺序编号 1–39 后**连续 5 个一批组**，余 4 批成末组（G8）。若执行时批文件数 ≠ 39 或唯一 id 数 ≠ 756 → 先停下更新本表，不得沿用组表。
2. `[假设]` `物理溅射` 冲突**恰好 1 条**（B10）。若扫描出 >1 → 全部登记入报告，**不扩大修复范围**，并在报告中标注新增条目。
3. `[假设]` S3 的 10 行目视样本可由 `category-map-*.tsv` 的行号**确定性定位**（无需随机）。
4. `[假设]` M4 的"目视"由执行 agent 实际打印 8 列并逐列判断即可完成，不需要 GUI/截图。
5. `[假设]` 5072 日志 T3.2 的独立验收结论可信但我方仍**重跑机械门禁**（27/27、placeholder=0、evidence=854）后才回写状态；重跑失败 ⇒ 不写 done，登记为待复核。
6. `[假设]` `v2026.10.30` 的"已发布"状态以**本地证据**（tag + origin/master 包含 + dist 资产 + contract OK）为准；GitHub Release 页面不做网络核验（本计划不引入网络依赖）。
7. `[假设]` `UNDECIDABLE` 是**合法终态**：真实源不可得（无网、上游快照无条目、仅有标签）时必须用它，且不计 PASS；不得为了勾选而补证或改判。
8. `[假设]` 父计划 M1/M3/M4 行文字在执行期间不被他人改写；若漂移 → 按 `grep -n 'M1:'` 重新定位，禁止按行号盲改。

## 核心设计决策（CoT Stage 3）

### D1 — 状态回写「只写事实，不写愿望」
- **选择**：S1 只回写三类可机械复现的事实：① 5072 执行完成但数据未发布；② 5110/`v2026.10.30` 已发布无需重发；③ M1/M3/M4 仍未勾 + 指向 `docs/reviews/t5184/`。
- **备选**：在 S1 一次性勾掉 M1/M4（"反正后面会做"）。**拒绝**：违反"状态只勾证据确凿项"，且会让后续阶段失去可失败信号。
- **风险**：状态文字再次与事实漂移 → 用 B12/B13 两条命令作为 S1 的硬门禁。

### D2 — 冲突查证「出证据 + 出建议，不动数据」
- **选择**：S2 产出 `m3-physical-sputtering.md`：冲突事实（3 张表的原行）、语义分析（`sputtering`=溅射 / `physical-sputtering`=物理溅射）、影响面（查询扩展/别名回指）、三选项（A 删除该 zh 别名 / B 改 `physical-sputtering.preferred_zh` / C 维持）与推荐、可逆性、需用户裁决。
- **拒绝**：直接删 `aliases.tsv` 那行。理由：父计划 M3 的语义是"人工裁决"，且本任务未获数据修复授权（父代理 prompt：默认只输出证据裁决建议）。
- **可失败信号**：报告必须能回答"若维持现状，`物理溅射` 查询会命中哪个 concept"——用 `scripts/registry_coverage_report.py` 的只读输出或别名反查命令给出，不允许只写定性判断。

### D3 — 确定性抽样：sha256 排序取前 8
- **选择**：组内 id 去重排序 → 逐个 `printf '%s' "$id" | sha256sum | cut -c1-16` → 按 hash 升序取前 8。
- **备选 A**：按 ids 文件行序取前 8。**拒绝**：`w1_b` 批次文件按字母序生成，前 8 会系统性偏向同一字母段，样本不具代表性。
- **备选 B**：`shuf -n 8`。**拒绝**：不可复现，无法审计。
- **可失败信号**：样本集 sha256 必须可由第三方用同一命令重算得到（AC 断言相等）。

### D4 — 语义复核：逐条原始语料 + 定义文本 + 适用性推理 + 三值判定（不做"代理硬门"）
- **选择**：每条抽检记录必须含 4 个**内容**字段，而非可被脚本伪造的代理指标：
  1. `原始语料`：**可得**时贴逐字原文 + `file:line`；**不可得**时写 `不可得` + 原因（无网 / 上游快照无对应条目 / 仅有来源标签）；
  2. `定义文本`：该 id 的 en 与 zh `definition` 逐字 + 两处 `definitions.tsv:<行号>`；
  3. `适用性推理`：≥40 字，回答三点——①该 en 定义是否准确刻画该 concept 在其技术语境中的对象；②zh 是否与 en 等价（增义/漏义/误译）；③是否与同族概念冲突；
  4. `判定` ∈ `{PASS, FAIL, UNDECIDABLE}`：
     - `PASS` = 原始语料**可得**且定义与之无矛盾；
     - `FAIL` = 与语料矛盾 / 增义 / 漏义 / 误译 / 同族概念冲突；
     - `UNDECIDABLE` = 原始语料不可得或语义无法判定 —— **必须写明原因，且不计入 PASS、不得用于勾选状态**。
- **为什么取消代理硬门**：`notes` 逐字出现只证明"复制过文本"，`判断文本去重 ≥60` 只证明"文字不重复"，两者都不能证明语义判断正确；把不可得源头强行判 PASS 才是真正的风险。
- **反例（判 FAIL 或 UNDECIDABLE，不得写 PASS）**：`原始语料: 见 concepts.tsv`（无原文）；`适用性推理` 仅复述 zh；URL 无网却写 PASS。
- **判定口径**：机械 AC 只校验**记录完整性 + 判定枚举 + 台账一致性**；判定**正确性**由阶段独立审查报告（M-A~M-C）与用户复核，不由脚本声明。

### D5 — commit 粒度：**一个 Task 一个 commit**
- **选择**：每个 Task 完成后立即 commit（含 `#T-5184`），只含该 Task 声明文件；只读准备不单独成 Task（已并入其产出 Task）。
- **理由（用户 refine 口径）**：每个 Task 独立可交付、可验收、可回滚；S4 的 8 组各自 commit，某组 FAIL/UNDECIDABLE 不影响其他组继续。
- **例外**：T1.3 / T2.4 / T3.3 / T4.10 这些"状态收口"Task 的 commit 只含状态行 + 该阶段报告，不含数据。
- **口径**：commit 数量 = **20**（S1 3 + S2 4 + S3 3 + S4 10）；**全部不 push**。

## 修改边界总表（逐 Task 限定允许文件）

| 阶段 | ✅ 允许写 | ⛔ 禁止写 | commit 口径 |
|---|---|---|---|
| **S1 状态回写** | `docs/reviews/t5184/README.md`、`docs/reviews/t5184/status-writeback.md`、父计划 M1/M3/M4 三行 + §5072 从句、5072 frontmatter `status` + 1 条注记 | 父计划其他章节；5072 Task/附录/日志正文；`terms/`、`artifacts/`、`pipeline/`、`scripts/`、`CHANGELOG.md` | 3 个（T1.1/T1.2/T1.3） |
| **S2 冲突查证** | `docs/reviews/t5184/m3-evidence-rows.tsv`、`m3-physical-sputtering.md`、父计划 M3 单行 | `terms/registry/{aliases,concepts,definitions,evidence}.tsv`；5072 计划；`scripts/` | 4 个（T2.1–T2.4） |
| **S3 目视核验** | `docs/reviews/t5184/m4-sample.tsv`、`m4-column-semantics.md`、父计划 M4 单行 | 全部 `terms/`、`artifacts/`；`category-map-*.tsv` | 3 个（T3.1–T3.3） |
| **S4 语义抽检** | `docs/reviews/t5184/m1-sample-manifest.tsv`、`m1-group-G1..G8.md`、`m1-summary.md`、父计划 M1 单行 | 全部数据文件；W3 缺陷（`spent-source`/`migration`） | 10 个（T4.1–T4.10） |

**跨 Task 通用纪律**：
1. 每 Task 首步 `git rev-parse HEAD` + `git status --porcelain`；脏文件仅允许 `?? iaea_fusion.html`。
2. **每 Task 1 个 commit**，message 带 `#T-5184`；`git diff --name-only HEAD~1 HEAD` 必须与该 Task 声明文件**逐字相同**（无额外路径）。
3. `git add` 逐文件显式列出，禁止 `git add -A` / `git add .`；不 push、不 squash。
4. **数据零写**：每 Task 末 `git diff --stat -- terms/ artifacts/ pipeline/ scripts/` 为空。
5. **S1 的有限 diff 不按行数卡**：只做「文件白名单 + 内容白名单」（父计划改动行必须命中 `M1|M3|M4|PM #5184|归档仍暂缓`），必要日志/注记允许保留。
6. **格式检查**：`git diff --check`（空白/冲突标记）。**不用 ruff 检查 Markdown**（ruff 不解析 Markdown；本计划无 Python 改动，故不跑 ruff/mypy）。
7. **非阻断**：`FAIL`/`UNDECIDABLE` 只影响对应 M 项勾选与台账，不中断其他 Task（S4 八组独立）。
8. 命令超时：默认 `timeout 300`；git 重操作 `timeout 120`。

---

## 执行计划

> **任务总量**：S1 3 + S2 4 + S3 3 + S4 10 = **20 个 Task**；**每个 Task 独立可交付、独立验收、独立 commit（`#T-5184`）、全部不 push**。
> **墙钟**：S1 55；S2 80；S3 55；S4 240；合计 **≈430 min**。**无单 Task >30 min；每 Task 内 checkpoint ≤15 min**。
> **互不阻断**：某 Task 审查结论为 `FAIL` / `UNDECIDABLE` 时，**只**把该项留未勾并登记台账，**不中断**其他 Task（S3 的 10 行、S4 的 8 组互不依赖）。仅以下情形允许停：检测到数据文件被写（`git diff -- terms/` 非空）、声明文件缺失、越权/授权问题。
> **判定枚举（全计划统一）**：`PASS` / `FAIL` / `UNDECIDABLE`。**`UNDECIDABLE` 不计入 PASS**；真实源不可得一律 `UNDECIDABLE`，禁止写 PASS。
> **通用执行契约（每 Task 隐含适用）**：
> 1. 起始 `git rev-parse HEAD` + `git status --porcelain`（脏文件仅允许 `?? iaea_fusion.html`）。
> 2. 结束 `git add <本 Task 声明文件>`（禁止 `-A`/`.`）→ `git commit -m '<msg> (#T-5184)'` → `git log -1 --format=%H` 记入报告「执行记录」。
> 3. 每 Task 数据只读断言：`git diff --stat -- terms/ artifacts/ pipeline/ scripts/` 为空。
> 4. 命令超时：默认 `timeout 300`；git 重操作 `timeout 120`。
> 5. **文档格式检查不用 ruff**（ruff 不解析 Markdown）；用 `git diff --check` + 必需字段 `grep`。本计划不改 Python，故不跑 ruff/mypy。
> 6. 每 Task 恰 1 个 commit；不合并、不压缩、不 push。
> 7. **先验收、后提交（硬门）**：Task 命令块必须 `set -euo pipefail` 开头；内容 AC + 暂存区范围 AC（`git diff --cached`）**全部 exit 0 之后**才允许 `git commit`。禁止用 `;` 串联「AC → commit」，禁止先提交再补验收（2026-11-03 T1.2 事故：AC 未过仍生成 `52dc8e8`）。AC 失败 ⇒ 记 `BLOCKED`，**不 commit、不标完成**。

### Phase S1: 状态回写（3 Task / 55 min）

#### Task T1.1 — 事实矩阵 + 证据索引（20 min；checkpoint 10/20）
- **依赖**：无；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件（仅 2 个新建）**：`docs/reviews/t5184/README.md`、`docs/reviews/t5184/status-writeback.md`
- **内容**：README = 四阶段表（`| S1 | 产物路径 | 状态 |`）+ 20 Task 索引 + 判定枚举/未勾规则；status-writeback = 事实矩阵（B1/B2/B9/B11/B12/B13 原样输出）+ 5072 结论（执行完成/**数据未进入任何发布 tag**）+ 5110 结论（已发布/无需重发）+ M1/M3/M4 均未勾。
- **命令**：
  ```bash
  cd /home/gw/opt/fusion-terms && mkdir -p docs/reviews/t5184
  { echo "## $(date -Iseconds)"; git rev-parse HEAD; git status --porcelain
    echo "## tags-contain-5072"; git tag --contains d84aabc | wc -l; git tag --contains 115da74 | wc -l
    echo "## tag-5110"; git rev-parse --short v2026.10.30^{commit}; git branch -r --contains v2026.10.30
    echo "## contract"; .venv/bin/python -m pipeline.verify_release_contract --root dist/stage/v2026.10.30
    echo "## 5072-status"; grep -n '^status:' .github/plans/5072-w3a-evidence-definition-backfill.md
    echo "## M-open"; grep -n '^- \[ \] M[134]:' .github/plans/terminology-coverage-and-definition-quality.md
  } 2>&1 | tee /tmp/opencode/t5184-baseline.txt
  git add docs/reviews/t5184/README.md docs/reviews/t5184/status-writeback.md
  git commit -m 'docs(status): baseline fact matrix and closeout evidence index (#T-5184)'
  ```
- **AC**：
  - ✅ `[T-A]` `grep -A2 '## tags-contain-5072' /tmp/opencode/t5184-baseline.txt | grep -c '^0$'` = 2
  - ✅ `[T-A]` `grep -q 'contract OK: .*version=v2026.10.30' /tmp/opencode/t5184-baseline.txt`
  - ✅ `[T-B]` `grep -c '^| S[1-4] |' docs/reviews/t5184/README.md` = 4；`grep -c '^| T[1-4]\.[0-9]' README.md` = 20
  - ✅ `[T-B]` `grep -c '数据未进入任何发布 tag' docs/reviews/t5184/status-writeback.md` ≥ 1；`grep -c '无需重发'` ≥ 1
  - ✅ `[T-C]` `git diff --name-only HEAD~1 HEAD | sort` = `docs/reviews/t5184/README.md` + `docs/reviews/t5184/status-writeback.md`
- **能失败证明**：把 `d84aabc` 换成 tag 内 `3cbaba7`，`git tag --contains` ≥1 ⇒ 第 1 条 FAIL。
- **边界/commit**：只写上述 2 文件；commit 见上。

#### Task T1.2 — 三处状态对齐（20 min；checkpoint 10/20）
- **依赖**：T1.1；**frontier**：是；**执行者**：Dev Orchestrator
- **状态（2026-11-03 收口实测）**：✅ **PASS** — commit `52dc8e8` 内容 AC 4/4 PASS、文件范围 3 文件 OK；范围 AC#5 经 IMPROVE-1 修订为「剥离 diff 标记 → 内容前缀精确锚点 + 行数 = 8 双断言」后由 acceptance-verifier 独立复验 **7/7 PASS**。**历史保留**：初次 AC#5 曾判 FAIL（旧白名单空转且按字面不可满足，命令块未设 `set -e`，AC 失败仍生成 52dc8e8）——该 finding 不撤销、不重写 commit，详见 §Execution Log E1。
- **修改文件（仅 2 个计划文件 + 1 个新报告）**：`.github/plans/5072-w3a-evidence-definition-backfill.md`（仅 frontmatter `status` + 1 条注记）、`.github/plans/terminology-coverage-and-definition-quality.md`（仅 M1/M3/M4 三行 + §5072 从句）、`docs/reviews/t5184/status-writeback.md`（追加「状态回写结果」节）
- **精确改动**：
  1. 5072 `status: "active"` → `status: "done-execution (data unreleased)"`；`---` 后插 1 行：`> **状态回写（2026-11-02，PM #5184）**：执行与独立验收已完成；**数据未进入任何发布 tag**（`git tag --contains d84aabc`=0），不得宣称已发布。`
  2. 父计划 M1/M3/M4 三行行尾各追加：`｜**PM #5184 收口中**：证据见 docs/reviews/t5184/（M1→m1-summary.md；M3→m3-physical-sputtering.md；M4→m4-column-semantics.md），未产出/未通过前保持未勾。`
  3. 父计划 §5072 从句（`理由：PM **5072**（W3a 证据/释义补强）仍为 \`todo\``）后追加：`（2026-11-02 实测：5072 执行完成、独立验收 PASS，但数据未发布；归档仍暂缓。）`
- **命令（`set -euo pipefail`；任一 AC 非零即退出，**禁止**走到 commit）**：
  ```bash
  set -euo pipefail
  cd /home/gw/opt/fusion-terms
  PARENT=.github/plans/terminology-coverage-and-definition-quality.md
  P5072=.github/plans/5072-w3a-evidence-definition-backfill.md
  # 0) 基线（未跟踪脏文件仅允许 .github/plans/5184-four-stage-closeout.md）
  git rev-parse HEAD; git status --porcelain
  # 1) 锚点唯一性（≠1 立即退出：先更新锚点，不编辑、不提交）
  test "$(grep -c '^status: "active"$' "$P5072")" -eq 1
  test "$(grep -c '^- \[ \] M1:' "$PARENT")" -eq 1
  test "$(grep -c '^- \[ \] M3:' "$PARENT")" -eq 1
  test "$(grep -c '^- \[ \] M4:' "$PARENT")" -eq 1
  test "$(grep -c '理由：PM \*\*5072\*\*（W3a 证据/释义补强）仍为 `todo`' "$PARENT")" -eq 1
  # 2) 按「精确改动」1–3 编辑 5 处锚点
  # 3) 内容 AC（任一失败 → set -e 退出，不进入提交）
  test "$(grep -c '^status: "done-execution (data unreleased)"$' "$P5072")" -eq 1
  test "$(grep -c '数据未进入任何发布 tag' "$P5072")" -eq 1
  test "$(grep -c 'PM #5184 收口中' "$PARENT")" -eq 3
  test "$(grep -c '^- \[x\] M[134]:' "$PARENT")" -eq 0
  # 4) 暂存 → 提交前范围 AC（等价于提交后 HEAD~1 HEAD 检查，但先于 commit）
  git add "$P5072" "$PARENT" docs/reviews/t5184/status-writeback.md
  test "$(git diff --cached --name-only | sort)" = "$(printf '%s\n' "$P5072" "$PARENT" docs/reviews/t5184/status-writeback.md | sort)"
  CHANGED="$(git diff --cached -U0 --no-color -- "$PARENT" | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//')"
  test "$(printf '%s\n' "$CHANGED" | wc -l)" -eq 8
  test "$(printf '%s\n' "$CHANGED" | grep -vcE '^- \[ \] M[134]:|^- \*\*未做（用户裁决')" -eq 0
  # 5) 以上全过才提交（AC 未过则本行永不执行）
  git commit -m 'docs(status): reconcile 5072 execution state and open M1/M3/M4 evidence pointers (#T-5184)'
  git log -1 --format='%H %s'
  ```
- **AC（复验时 `HEAD~1`=`86e9b00`、`HEAD`=`52dc8e8`；命令可直接粘贴）**：
  - ✅ `[T-A]` `grep -c '^status: "done-execution (data unreleased)"$' .github/plans/5072-w3a-evidence-definition-backfill.md` = 1
  - ✅ `[T-A]` `grep -c '数据未进入任何发布 tag' .github/plans/5072-w3a-evidence-definition-backfill.md` = 1
  - ✅ `[T-A]` `grep -c 'PM #5184 收口中' .github/plans/terminology-coverage-and-definition-quality.md` = 3
  - ✅ `[T-B]` **未勾保持**：`grep -c '^- \[x\] M[134]:' .github/plans/terminology-coverage-and-definition-quality.md` = 0
  - ✅ `[T-A]` **文件范围**：`git diff --name-only HEAD~1 HEAD | sort` = 恰 3 个声明文件（`.github/plans/5072-w3a-evidence-definition-backfill.md`、`.github/plans/terminology-coverage-and-definition-quality.md`、`docs/reviews/t5184/status-writeback.md`）
  - ✅ `[T-A]` **父计划改动行数**：剥离首个 diff 标记后的内容行恰 **8** 行（= 4 处锚点 × 旧/新）：
    `git diff -U0 --no-color HEAD~1 HEAD -- .github/plans/terminology-coverage-and-definition-quality.md | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//' | wc -l` = **8**
  - ✅ `[T-A]` **父计划白名单外行 = 0**（允许集 = 精确锚点允许的**旧行与新行**，不放宽其它行）：
    `git diff -U0 --no-color HEAD~1 HEAD -- .github/plans/terminology-coverage-and-definition-quality.md | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//' | grep -vcE '^- \[ \] M[134]:|^- \*\*未做（用户裁决'` = **0**
    - 允许集恰为 4 类内容前缀：`- [ ] M1:`、`- [ ] M3:`、`- [ ] M4:`、`- **未做（用户裁决…理由：PM **5072**（W3a 证据/释义补强）`（**旧行 `- **未做…仍为 `todo`，归档…` 与被加的 `…归档仍暂缓。）` 新行都允许**）。
- **AC#5 修正说明（IMPROVE-1，替换原「`grep -E '^[+-][^+-]'` + 词白名单」写法）**：
  - 旧写法对**内容本身以 `- ` 开头**的行（M1/M3/M4 与 §5072 从句）**一行也匹配不到**——diff 行是 `-- [ ] M1:`，`^[+-][^+-]` 第二字符是 `-` ⇒ 该检查**空转通过**。
  - 若按字面收紧后仅保留词白名单，§5072 **被删除的旧行**只含 `PM **5072**`、不含 `M1|M3|M4|PM #5184|归档仍暂缓` ⇒ **必然记 1 条违规**，该 AC **不可满足**（T1.2 因此无法退出）。
  - 现改为「**剥离首个 diff 标记 → 内容前缀精确锚点**」，并加**行数 = 8** 双断言，既覆盖旧行也覆盖新行，且越界改动无处藏身。
- **能失败证明（变异法，逐条可直接跑）**：
  - 去掉 §5072 备用锚点：`git diff -U0 --no-color HEAD~1 HEAD -- .github/plans/terminology-coverage-and-definition-quality.md | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//' | grep -vcE '^- \[ \] M[134]:'` = **2**（旧/新 §5072 行）⇒ 白名单项 FAIL。
  - 模拟越界 1 行：`printf -- '- 其他章节改动\n' | grep -vcE '^- \[ \] M[134]:|^- \*\*未做（用户裁决'` = **1** ⇒ 白名单项 FAIL。
  - 把 M1 改成 `[x]` ⇒ 「未勾保持」FAIL；多改一行正文 ⇒ 行数 8→10 且白名单违约 ≥1。
- **边界/commit**：只改上述 5 处锚点；不碰父计划其他章节、5072 Task/日志正文；commit 见上（**AC 全过才执行**）。

#### Task T1.3 — PM 备注 + README 执行记录（15 min；checkpoint 8/15）
- **依赖**：T1.2（**须 T1.2 的 AC 7/7 全过后**；2026-11-03 收口实测：已满足，IMPROVE-1 修订后独立复验 PASS）；**frontier**：否；**执行者**：Dev Orchestrator + `pm-coordinator`（PM 写操作）
- **修改文件**：`docs/reviews/t5184/README.md`（追加 S1 三 Task 的 commit 哈希与状态）
- **内容**：委派 `pm-coordinator` 给 #5184 写备注（三区块：事实 / 产物路径 / 下一阶段 = S2）；README 记录 `T1.1/T1.2` commit 哈希（`git log --format='%h %s' -n 2`）。
- **AC**：
  - ✅ `[T-A]` pm-coordinator 返回含 `5184` 且写入成功
  - ✅ `[T-B]` `grep -cE '^\\| T1\\.[12] \\|' docs/reviews/t5184/README.md` ≥ 2 且对应行含 7 位以上 commit hash（`grep -cE '[0-9a-f]{7,}'`）
  - ✅ `[T-C]` `git diff --name-only HEAD~1 HEAD` = `docs/reviews/t5184/README.md`
- **能失败证明**：README 只写"已完成"不写 hash ⇒ 第 2 条 FAIL。
- **边界/commit**：`git commit -m 'docs(status): record S1 task commits and PM note (#T-5184)'`。

### Phase S2: 术语冲突查证（4 Task / 80 min，只出证据与建议）

#### Task T2.1 — 冲突全集扫描 + 原行证据（15 min；checkpoint 8/15）
- **依赖**：T1.3；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m3-evidence-rows.tsv`（新）
- **命令**（沿用已干跑通过的扫描；输出 `TOTAL= 1`）：
  ```bash
  cd /home/gw/opt/fusion-terms
  python3 - <<'PY' > docs/reviews/t5184/m3-evidence-rows.tsv
  files={'concepts':'terms/registry/concepts.tsv','aliases':'terms/registry/aliases.tsv',
         'definitions':'terms/registry/definitions.tsv','evidence':'terms/registry/evidence.tsv'}
  ids={'sputtering','physical-sputtering'}
  print('table\tfile_line\traw')
  for t,p in files.items():
      for i,line in enumerate(open(p,encoding='utf-8'),1):
          s=line.rstrip('\n')
          if not s or s.startswith('#'): continue
          c=s.split('\t')
          hit = (c[0].strip()=='物理溅射' or (len(c)>1 and c[1].strip() in ids)) if t=='aliases' else (c[0].strip() in ids)
          if hit: print(f'{t}\t{p}:{i}\t{s}')
  PY
  python3 - <<'PY' | tee /tmp/opencode/t5184-conflicts.txt
  import csv
  zh={}
  for r in csv.reader(open('terms/registry/concepts.tsv',encoding='utf-8'),delimiter='\t'):
      if r and not r[0].startswith('#') and len(r)>3 and r[2].strip(): zh.setdefault(r[2].strip(),[]).append(r[0])
  n=0
  for i,r in enumerate(csv.reader(open('terms/registry/aliases.tsv',encoding='utf-8'),delimiter='\t'),1):
      if not r or r[0].startswith('#') or len(r)<4: continue
      if r[2].strip()=='zh' and r[3].strip()!='forbidden':
          owners=[o for o in zh.get(r[0].strip(),[]) if o!=r[1].strip()]
          if owners: n+=1; print(f'aliases.tsv:{i}\t{r[0]}\talias->{r[1]}\talso_preferred_zh_of={owners}')
  print('TOTAL=',n); assert n==1
  PY
  git add docs/reviews/t5184/m3-evidence-rows.tsv
  git commit -m 'docs(review): dump physical-sputtering conflict rows with line anchors (#T-5184)'
  ```
- **AC**：
  - ✅ `[T-A]` 扫描输出 `TOTAL= 1` 且 exit 0
  - ✅ `[T-B]` `grep -cP '^[a-z]+\tterms/registry/[a-z]+\.tsv:[0-9]+\t' docs/reviews/t5184/m3-evidence-rows.tsv` ≥ 8；四张表各 ≥1
  - ✅ `[T-C]` `git diff --stat -- terms/` 为空；commit 只含该 tsv
- **能失败证明**：临时副本追加一条冲突别名后同脚本 `TOTAL= 2` 且 assert 失败（仓内不动）。
- **边界/commit**：只写该 tsv；commit 见上。

#### Task T2.2 — 下游投影实测（20 min；checkpoint 10/20）
- **依赖**：T2.1；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m3-physical-sputtering.md`（新建 §1 冲突事实 / §2 下游投影）
- **命令**（`PROJECTION_OK` 已干跑通过）：
  ```bash
  python3 - <<'PY'
  import json
  d=json.load(open('artifacts/translation_dict.json',encoding='utf-8'))
  q=json.load(open('artifacts/query_expansions.json',encoding='utf-8'))
  print('A zh2en[物理溅射] =', d['zh2en'].get('物理溅射'))
  print('B en2zh[physical sputtering] =', d['en2zh'].get('physical sputtering'))
  print('C zh2en[化学溅射] =', d['zh2en'].get('化学溅射'))
  print('D alias_index[物理溅射] =', q['alias_index'].get('物理溅射'))
  print('E sputtering.all_terms 含物理溅射 =', '物理溅射' in q['concepts']['sputtering']['all_terms'])
  assert d['zh2en'].get('物理溅射')=='sputtering'
  assert d['en2zh'].get('physical sputtering')=='物理溅射'
  assert d['zh2en'].get('化学溅射')=='chemical sputtering'
  assert q['alias_index'].get('物理溅射')=='sputtering'
  assert '物理溅射' in q['concepts']['sputtering']['all_terms']
  print('PROJECTION_OK')
  PY
  git add docs/reviews/t5184/m3-physical-sputtering.md
  git commit -m 'docs(review): record downstream projections of physical-sputtering alias (#T-5184)'
  ```
- **AC**：
  - ✅ `[T-A]` `PROJECTION_OK` 且 exit 0
  - ✅ `[T-B]` 报告 `for k in 'A zh2en[物理溅射]' 'B en2zh[physical sputtering]' 'C zh2en[化学溅射]' 'D alias_index[物理溅射]' 'E sputtering.all_terms'; do grep -qF "$k" 报告 || echo MISSING; done` 输出为空
  - ✅ `[T-B]` 报告含 5 个实测值（`= sputtering` / `= 物理溅射` / `= chemical sputtering` 等）
  - ✅ `[T-C]` `git diff --stat -- terms/ artifacts/` 为空
- **能失败证明**：若 artifacts 重建导致 `zh2en[物理溅射]` 变化，assert 失败 ⇒ 记录实际值并转 `UNDECIDABLE`，不得改写成 PASS。
- **边界/commit**：只写报告；commit 见上。

#### Task T2.3 — 语义/来源适用性核验（25 min；checkpoint 12/25）
- **依赖**：T2.2；**frontier**：是；**执行者**：Dev Orchestrator（须阅读定义与同族概念）
- **修改文件**：`docs/reviews/t5184/m3-physical-sputtering.md`（追加 §3 语义层级 / §4 来源可得性）
- **必须逐条给出三值判定（每条含 `证据` + `推理` + `判定`）**：
  1. `H1` `sputtering=溅射` 是通用上位概念（依据 `definitions.tsv` 该 id 原文）；
  2. `H2` `physical-sputtering=物理溅射` 与 `chemical-sputtering=化学溅射` 是并列下位概念（依据三条定义原文）；
  3. `H3` `物理溅射` 同时作为 `sputtering` 的 zh alias 是否成立 —— **仓内上游 `artifacts/terminology_sources/*` 无该串时，只能记 `UNDECIDABLE`（缺上游权威）**，不得写成"上游否定该用法"；
  4. `H4` 下游 `zh2en`/`alias_index` 的投影是否造成信息丢失（依据 T2.2 实测）。
- **AC**：
  - ✅ `[T-A]` `grep -c '^### H[1-4]' 报告` = 4，且每节含 `证据:`、`推理:`、`判定:` 各 1
  - ✅ `[T-B]` `grep -c '^判定: \\(PASS\\|FAIL\\|UNDECIDABLE\\)$' 报告` = 4（枚举合法）
  - ✅ `[T-B]` H3 若 `依据: 不可得` 则判定必须为 `UNDECIDABLE`：`awk '/^### H3/,/^### H4/' 报告 | grep -q '不可得' && awk '/^### H3/,/^### H4/' 报告 | grep -q 'UNDECIDABLE'`
  - ✅ `[T-B]` 报告含 3 个 concept 的 `definitions.tsv:<行号>`（≥3 处）
  - ✅ `[T-C]` `git diff --stat -- terms/` 为空
- **能失败证明**：把 H3 写成 `PASS` 并注"上游没有即证明不该有" ⇒ 第 3 条自动 FAIL（不可得必须 UNDECIDABLE）。
- **边界/commit**：不修改数据；`git commit -m 'docs(review): concept-level applicability and source availability for physical-sputtering (#T-5184)'`。

#### Task T2.4 — 三选项建议 + M3 状态注记（20 min；checkpoint 10/20）
- **依赖**：T2.3；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m3-physical-sputtering.md`（§5 选项/推荐/可逆性/待裁决）、父计划 M3 单行
- **内容**：三选项各含 `改动文件 / 机械影响 / 可逆性 / 风险`：A 删除 `物理溅射→sputtering` alias；B 改 `physical-sputtering.preferred_zh`；C 维持并登记歧义。推荐项须引用 §3/§4 的证据编号；**不得**声称已授权。
- **AC**：
  - ✅ `[T-A]` `grep -c '^### 选项 [ABC]' 报告` = 3；每节含 `可逆性:`
  - ✅ `[T-B]` `grep -c '待用户裁决 (D2)' 报告` ≥ 1；`grep -c '已授权\\|用户已批准' 报告` = 0
  - ✅ `[T-B]` **M3 保持未勾**：`grep -c '^- \[x\] M3:' 父计划` = 0，且 M3 行含 `S2 查证完成`
  - ✅ `[T-C]` `git diff --name-only HEAD~1 HEAD | sort` = 报告 + 父计划
- **能失败证明**：勾 `[x] M3` ⇒ 第 3 条 FAIL；写"已授权删除" ⇒ 第 2 条 FAIL。
- **边界/commit**：只出建议；`git commit -m 'docs(review): three-option adjudication proposal for physical-sputtering (pending user decision) (#T-5184)'`。

### Phase S3: 小样目视核验（3 Task / 55 min）

> 抽样唯一口径：`category-map-shift99.tsv` 数据行 1/20/40/60/80（文件行 2/21/41/61/81）+ `category-map-sixcol80.tsv` 数据行 1/16/32/48/64（文件行 2/17/33/49/65）= **10 行**。
> M4 勾选条件：**10 行全部 `PASS`**（含 1 条 `FAIL` 或 `UNDECIDABLE` 即保持未勾）。

#### Task T3.1 — 10 行样本清单 + 机械列断言（15 min；checkpoint 8/15）
- **依赖**：T2.4；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m4-sample.tsv`（新）
- **命令**：`sed -n '2p;21p;41p;61p;81p' category-map-shift99.tsv` + `sed -n '2p;17p;33p;49p;65p' category-map-sixcol80.tsv` 取 concept_id，`grep -nP "^<cid>\t"` 补 `concepts.tsv:<行号>`；随后跑**结构断言**（8 列 / category ∈ 16 类 / 第3列含 CJK / 第4列 ASCII / 第6列 active / 第8列 corpus / sixcol80 的 notes 含 `[domain: `）。
- **AC**（已在计划阶段干跑：`rows_ok=10 canon=10 zh=10 en=10 active=10 src=10 domain=5`）：
  - ✅ `[T-A]` python 断言输出 `M4_COLUMNS_OK` 且 exit 0
  - ✅ `[T-B]` `wc -l docs/reviews/t5184/m4-sample.tsv` = 11；`cut -f4 | tail -n +2 | sort -u | wc -l` = 10
  - ✅ `[T-C]` `git diff --stat -- terms/ .github/plans/t4973-batches/` 为空
- **能失败证明**：`sed` 取到表头（行 1）⇒ `len(cols)==8` 断言失败。
- **commit**：`git commit -m 'docs(review): deterministic 10-row sample manifest for column-semantics check (#T-5184)'`。

#### Task T3.2 — 10 行逐列目视（25 min；checkpoint 12/25）
- **依赖**：T3.1；**frontier**：是；**执行者**：Dev Orchestrator（**必须实际打印并逐列阅读**）
- **修改文件**：`docs/reviews/t5184/m4-column-semantics.md`（新）
- **每行一个 `### <concept_id>` 块，必须含 4 个内容字段**：
  1. `原始列:` —— `awk -F'\t' '{for(i=1;i<=NF;i++) printf "%d=[%s] ",i,$i; print ""}'` 的**原样输出**（证明看到的是当前真实行）；
  2. `逐列适用性推理:` —— ≥30 字，逐列判断：第2列 category 是否与该概念性质相符、第3列是否中文名、第4列是否英文名、第7列 notes 是否描述该概念、第8列 source 是否合理；
  3. `判定:` ∈ `{PASS, FAIL, UNDECIDABLE}`；FAIL 须写缺陷类型（错位/错名/缺列/异语言），UNDECIDABLE 须写 `待定原因:`；
  4. `证据锚点:` —— `concepts.tsv:<行号>` + `definitions.tsv:<en行号>,<zh行号>`。
- **AC**：
  - ✅ `[T-A]` `grep -c '^### ' 报告` = 10；`grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$' 报告` = 10
  - ✅ `[T-B]` 每块字段齐全：`for k in '原始列:' '逐列适用性推理:' '证据锚点:' '判定:'; do test $(grep -c "$k" 报告) -ge 10 || echo MISSING:$k; done` 输出为空
  - ✅ `[T-B]` `grep -c 'concepts.tsv:[0-9]' 报告` ≥ 10 且 `grep -c 'definitions.tsv:[0-9]'` ≥ 10
  - ✅ `[T-B]` 反占位（**仅完整性，不作质量判定**）：`grep -cE 'TODO|待补|见脚本|自动化通过' 报告` = 0
  - ✅ `[T-C]` `git diff --stat -- terms/` 为空
- **能失败证明**：删掉某行 `原始列:` ⇒ 第 2 条 FAIL；把 `FAIL` 写成 `PASS` 但推理里写"第3列是英文" ⇒ 人工复核（M-B）直接暴露（不靠脚本宣称正确性）。
- **commit**：`git commit -m 'docs(review): 10-row column semantics with per-column applicability reasoning (#T-5184)'`。

#### Task T3.3 — 汇总 + M4 状态写回（15 min；checkpoint 8/15）
- **依赖**：T3.2；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m4-column-semantics.md`（追加汇总）、父计划 M4 单行
- **规则**：统计 `PASS/FAIL/UNDECIDABLE`；**仅当 10/10 PASS** 才把 M4 改 `[x]`；否则保持 `[ ]` 并写 `发现 n 条 FAIL + m 条 UNDECIDABLE`。
- **AC**：
  - ✅ `[T-A]` 汇总行格式 `10 行 / PASS <n> / FAIL <m> / UNDECIDABLE <k>` 存在（`grep -c '^10 行 / PASS'` = 1）
  - ✅ `[T-B]` 汇总数与明细一致：`grep -c '^判定: PASS'` == n 等（三值各校验）
  - ✅ `[T-B]` **双向状态**：`if [ "$n" -eq 10 ]; then grep -c '^- \[x\] M4:' 父计划 = 1; else grep -c '^- \[x\] M4:' 父计划 = 0; fi`
  - ✅ `[T-C]` `git show --stat --format= HEAD | grep -c 'terms/'` = 0
- **能失败证明**：n<10 却勾 M4 ⇒ 第 3 条 FAIL。
- **commit**：`git commit -m 'docs(review): M4 summary and evidence-bound status writeback (#T-5184)'`。

### Phase S4: 分批语义抽检（10 Task / 240 min）

> 分组唯一口径：`w1_a_b01..b04` → `w1_b_b01..b34` → `w1_c_b01` 顺序编号 1–39，连续 5 批为 1 组，余 4 批为 G8。
> 抽样唯一口径：组内 id 去重排序后按 `sha256(id)[:16]` 升序取前 8；每组样本集 `sha256` 落 manifest。
> **组间完全独立**：任一组 FAIL/UNDECIDABLE **不阻断**其余组；M1 仅当 64/64 PASS 时勾选。
> **依据可得性规则（统一，禁止假通过）**：
> - `source=corpus` → 依据 = `concepts.tsv` notes 原文 + 行号，**可得**；
> - `source=GB/T-4960.9` → 依据 = `gbt4960_9_diff.tsv` 中 `matched_concept_id` 命中行；**未命中 ⇒ `UNDECIDABLE`（源不可得）**；
> - `source=IAEA-safety-glossary / ITER-glossary` → 依据 = `*_raw.tsv` 归一化命中行；未命中 ⇒ `UNDECIDABLE`；
> - `source=http(s)://…` → 依据 = URL + 取回日期 + 片段；无网或 4xx/5xx ⇒ `UNDECIDABLE`（不得用 `--no-net` 冒充通过）。

#### Task T4.1 — 样本 manifest（20 min；checkpoint 10/20）
- **依赖**：T3.3；**frontier**：是；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m1-sample-manifest.tsv`（新；列 `group batch_scope concept_id sha256_16` + 8 行 `# group_sample_sha256`）
- **命令**：按组循环 `cat $FILES | sort -u` → 每 id `sha256sum | cut -c1-16` → `sort | head -8`；再算每组样本集 hash 追加注释行（**已干跑：64 行，组内 id 数 87/100×6/69**）。
- **AC**：
  - ✅ `[T-A]` `grep -c '^G[1-8]\t' manifest` = 64；每组恰 8 行（`awk` 组计数无 `BAD`）
  - ✅ `[T-B]` 64 个唯一 id（`uniq -d` = 0）；每组样本 ⊆ 该组全 id（`comm -23` = 0）
  - ✅ `[T-B]` 8 个 `group_sample_sha256` 可由 `awk + sort + sha256sum` 复算一致
  - ✅ `[T-C]` `for g in G1..G8; do wc -l < /tmp/opencode/$g.all.ids; done | tr '\n' ' '` = `87 100 100 100 100 100 100 69 `
- **能失败证明**：`head -8` 改 `head -7` ⇒ 第 1 条 FAIL；`sort` 去掉 ⇒ 落盘集与复算 hash 不一致 ⇒ 第 3 条 FAIL。
- **commit**：`git commit -m 'docs(review): 8x8 deterministic W1 sampling manifest with set hashes (#T-5184)'`。

#### Task T4.2 — 组 G1 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G1.md`；**组内 ids = 87**
- **commit**：`git commit -m 'docs(review): W1 group G1 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G1 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.3 — 组 G2 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G2.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G2 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G2 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.4 — 组 G3 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G3.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G3 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G3 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.5 — 组 G4 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G4.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G4 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G4 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.6 — 组 G5 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G5.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G5 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G5 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.7 — 组 G6 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G6.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G6 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G6 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.8 — 组 G7 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G7.md`；**组内 ids = 100**
- **commit**：`git commit -m 'docs(review): W1 group G7 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G7 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### Task T4.9 — 组 G8 语义复核（8 样本 / 25 min；checkpoint 12/25）
- **依赖**：T4.1（组间无依赖）；**frontier**：是；**执行者**：Academic Writer + Dev Orchestrator
- **修改文件（仅 1 个新建）**：`docs/reviews/t5184/m1-group-G8.md`；**组内 ids = 69**
- **commit**：`git commit -m 'docs(review): W1 group G8 semantic review (8 samples) (#T-5184)'`
- **AC**：套用下方「组通用 AC」6 条 + 组特化断言：`awk -v g=G8 '$1==g' manifest | wc -l` = 8；报告 8 个样本 id 与 manifest 该组 8 行**逐行相同**。

#### 组通用 AC 与样本格式（T4.2–T4.9 共用）

- **每条样本（8 条/组）必须含 4 个内容字段 + 1 个判定**：
  1. `原始语料:` —— 按上方「依据可得性规则」贴**逐字原文 + file:line**；不可得写 `不可得: <原因>`；
  2. `定义文本:` —— en 与 zh 逐字 + 两处 `definitions.tsv:<行号>`；
  3. `适用性推理:` —— ≥40 字，必须回答：①该 en 定义是否准确刻画该 concept 在聚变/核工程语境中的对象；②zh 与 en 是否等价（增义/漏义/误译/术语不一致）；③是否与同族概念冲突；
  4. `判定:` + （`FAIL`/`UNDECIDABLE` 时）`缺陷/待定原因:`;
  5. `证据锚点:` —— `concepts.tsv:<行号>`。
- **命令（每样本）**：`grep -nP "^<cid>\t(en|zh)\t" definitions.tsv`；`grep -nP "^<cid>\t" concepts.tsv`；按 source 取依据（`awk -F'\t' -v id=<cid> '$3==id' gbt4960_9_diff.tsv` / `grep -nF "<en前40字符>" *_raw.tsv` / `curl -sS -o /dev/null -w '%{http_code}' <url>`）。
- **组通用 AC（每 Task 逐条执行）**：
  - ✅ `[T-A]` `grep -c '^### ' m1-group-G<k>.md` = 8；`grep -c '^判定: \(PASS\|FAIL\|UNDECIDABLE\)$'` = 8
  - ✅ `[T-B]` 四字段齐全（`for k in '原始语料:' '定义文本:' '适用性推理:' '证据锚点:'; do test $(grep -c "$k" f) -ge 8 || echo MISSING; done` 无输出）
  - ✅ `[T-B]` 不可得行必须三值一致：`grep -c '^原始语料: 不可得'` == `grep -c '^判定: UNDECIDABLE'`
  - ✅ `[T-B]` 缺陷/待定台账：报告末节 `| D<n> | <cid> | <FAIL\|UNDECIDABLE> | 原因 |` 行数 == `FAIL + UNDECIDABLE` 数
  - ✅ `[T-B]` `grep -c 'concepts.tsv:[0-9]'` ≥ 8 且 `grep -c 'definitions.tsv:[0-9]'` ≥ 16
  - ✅ `[T-C]` `git diff --stat -- terms/` 为空；commit 只含本组报告
- **能失败证明**：GB/T 行未命中却写 `PASS` ⇒ 第 3 条（不可得行数 == UNDECIDABLE 数）FAIL；只写 7 条 ⇒ 第 1 条 FAIL。
- **互不阻断**：某组 FAIL/UNDECIDABLE 只影响 M1 勾选，不阻塞其他组。

#### Task T4.10 — 汇总 + M1 状态写回（20 min；checkpoint 10/20）
- **依赖**：T4.2–T4.9；**frontier**：是（各组完成后可做）；**执行者**：Dev Orchestrator
- **修改文件**：`docs/reviews/t5184/m1-summary.md`（新）、父计划 M1 单行
- **内容**：① 覆盖声明 `抽检 64 / 756 = 8.5%`，明写"抽检≠全量语义保证"；② 8 组 × `PASS/FAIL/UNDECIDABLE` 表；③ 缺陷与待定台账（含不可得原因，供后续补证）；④ 来源可得率（corpus/GB-T/IAEA/ITER/URL 各自 `可得/不可得`）；⑤ **M1 勾选 = 64/64 PASS**，否则未勾。
- **AC**：
  - ✅ `[T-A]` `grep -c '^| G[1-8] '` = 8；总计行含 `PASS`/`FAIL`/`UNDECIDABLE`
  - ✅ `[T-B]` 汇总三值数 == 8 个组报告明细之和（逐个 `grep -c` 相加比对）
  - ✅ `[T-B]` **双向状态**：`if sum(PASS)==64 && sum(FAIL)==0 && sum(UNDECIDABLE)==0; then M1=[x]; else M1=[ ]`
  - ✅ `[T-B]` **不假通过**：`UNDECIDABLE` 数 > 0 时 `grep -c '^- \[x\] M1:'` 必须为 0
  - ✅ `[T-C]` `git diff --unified=0 HEAD~1 HEAD -- 父计划 | grep -cE '^[+-].*M[34]:'` = 0（只允许 M1 行变化）
- **能失败证明**：有 UNDECIDABLE 仍勾 M1 ⇒ 第 4 条 FAIL。
- **commit**：`git commit -m 'docs(review): M1 8-group summary, undecidable ledger and evidence-bound status (#T-5184)'`。

## 风险与对策

| # | 风险 | 概率 | 影响 | 对策 | 触发信号 |
|---|------|------|------|------|---------|
| R1 | 状态过度声明（5072 写成已发布） | 中 | 高 | T1.1/T1.2 硬门禁 `git tag --contains`=0 + 报告写"未发布" | 出现"5072 已发布" |
| R2 | 提前勾选（M1/M4 未做先勾） | 中 | 高 | T1.2 断言 `^- \[x\] M[134]:`=0；T3.3/T4.10 双向状态断言 | 断言 FAIL |
| R3 | 越权改数据 | 中 | 高 | 每 Task `git diff --stat -- terms/ artifacts/` 为空；S2 只出建议 | diff 非空 |
| R4 | 抽样不可复现 | 中 | 中 | sha256 排序 + 样本集 hash 落盘 + 复算断言 | hash 不匹配 |
| R5 | **假通过**（源不可得仍判 PASS） | 高 | 高 | 判定枚举强制 `UNDECIDABLE`；"不可得行数 == UNDECIDABLE 数"机械断言；M1/M4 勾选要求全 PASS | 计数不等 |
| R6 | 判定正确性被脚本伪装 | 中 | 高 | 脚本只查完整性/枚举；正确性交 M-A~M-C 人工复核与用户抽核 | 推理字段空泛 |
| R7 | W3 缺陷混入 W1 承诺 | 中 | 中 | 执行前 `grep -lx spent-source/migration w1_*.ids` 为空；summary 明列"引用不修复" | 出现 W3 条目 |
| R8 | 跨阶段基线漂移 | 高 | 中 | 每 Task 首步重测 HEAD/批文件数；漂移先更新锚点 | B6/B10/B14 变化 |
| R9 | 提交夹带未声明文件 | 中 | 中 | 逐文件 `git add`；`git diff --name-only HEAD~1 HEAD` 与声明清单逐字比对 | 出现额外路径 |
| R10 | 一组 FAIL 导致整体停摆 | 中 | 中 | 明确"互不阻断"：组间无依赖，只影响 M1 勾选 | 某组未产出即停工 |
| R11 | 有限 diff 限制卡住必要日志 | 中 | 中 | S1 只做**文件白名单 + 内容白名单**；白名单按**内容前缀精确锚点**判定（含被删旧行），不设行数上限（T1.2 例外：锚点固定 4 处 ⇒ 行数 = 8） | 白名单外改动 |
| R12 | **diff 类 AC 空转或不可满足**（`^[+-][^+-]` 对 `- ` 开头行匹配 0 ⇒ 假通过；词白名单漏被删旧行 ⇒ 必失败） | 中 | 高 | 先剥离首个 diff 标记再比内容前缀；行数 + 白名单双断言；每条 AC 必须给出变异法「能失败证明」 | 反例计数 = 0 或 AC 永远为 0 行 |

## Execution Wave（并行执行波次）

| Wave | 可并行 Task | Frontier | 依赖已完成 |
|------|------------|----------|------------|
| W1 | T1.1 | T1.1 | — |
| W2 | T1.2 | T1.2 | W1 |
| W3 | T1.3 | T1.3 | W2 |
| W4 | T2.1 | T2.1 | W3 |
| W5 | T2.2 | T2.2 | W4 |
| W6 | T2.3 | T2.3 | W5 |
| W7 | T2.4 | T2.4 | W6 |
| W8 | T3.1 | T3.1 | W7 |
| W9 | T3.2 | T3.2 | W8 |
| W10 | T3.3 | T3.3 | W9 |
| W11 | T4.1 | T4.1 | W10 |
| W12 | **T4.2–T4.9（8 个并行）** | 全部 | W11 |
| W13 | T4.10 | T4.10 | W12 |

## Post-Execution Verification

### Automated Verification

| ID | Description | Command | Expected |
|----|-------------|---------|----------|
| V1 | Task commit 数 = 20 且全部带 `#T-5184` | `git log --oneline HEAD~20..HEAD --grep='#T-5184' \| wc -l` | **20** |
| V2 | 未 push | `git status -sb \| head -1` | 含 `ahead` |
| V3 | 数据零改动 | `git diff --stat HEAD~20 HEAD -- terms/ artifacts/ pipeline/ scripts/` | 空 |
| V4 | 报告齐备 | `ls docs/reviews/t5184/{README.md,status-writeback.md,m3-physical-sputtering.md,m4-column-semantics.md,m1-sample-manifest.tsv,m1-summary.md}` + `ls docs/reviews/t5184/m1-group-G{1,2,3,4,5,6,7,8}.md` | 全部存在非空 |
| V5 | 空白/冲突标记 | `git diff --check HEAD~20 HEAD` | 空 |
| V6 | registry 未退化 | `.venv/bin/python -m pipeline.validate_registry` | exit 0 |
| V7 | 结构+W1 质量门禁未退化 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | exit 0 |
| V8 | M 项状态-证据一致 | T1.2 / T2.4 / T3.3 / T4.10 的双向断言 | 全 exit 0 |
| V9 | 样本可复算 | 8 组 `group_sample_sha256` 重算比对 | 8/8 匹配 |

> **不做**：`.venv/bin/ruff format --check` / `ruff check`（ruff 不检查 Markdown；本计划无 Python 改动）。

### Deferred / Probe / Manual

- **Deferred**：D1 无（无服务、无部署）。
- **Probe**：P1 `registry_batch_verify.py --self-test` → `27/27`（环境探针，失败记录不阻塞）；P2 `pytest -q` → exit 0（同）。
- **Manual**：
  - M-A：S2 三选项是否**只**基于实测证据（人读 §3/§4/§5，检查 H3 不可得是否被判 UNDECIDABLE）；
  - M-B：S3 抽 2 条，核对 `原始列:` 原样输出与 `逐列适用性推理` 是否自洽；
  - M-C：S4 抽 4 条（覆盖 corpus 与 GB/T 各 2），核对 `适用性推理` 是否真的引用了原始语料中的具体限定语，而非复述 zh；
  - M-D：确认 M3 仍为未勾且报告写明待裁决点。

## 待裁决 / 已知限制

1. **M3 修复需用户裁决（D2）**：A 删除别名 / B 改名 / C 维持；本计划只出建议，**不改数据**。
2. **`UNDECIDABLE` 是合法结论**：真实源不可得（无网、上游快照无对应条目、仅有来源标签）时，必须记 `UNDECIDABLE` 并进待定台账；**不计 PASS**，M1/M4 相应不勾。
3. **抽检 64/756 = 8.5%**，不构成全量语义保证；机械门禁只覆盖格式/占位/长度。
4. **5072 数据未发布**（`v2026.10.30`=`fa34be1` 早于其全部提交），本计划不触发重发。
5. **W3 已知缺陷不在范围**：`spent-source`/`migration` 等 en 粘连属 5072 §6，W1 清单内不存在，不修不计 FAIL。

## 审查日志

| 轮次 | 聚焦 | 发现问题数 | 已修正 | 剩余 |
|------|------|-----------|--------|------|
| R1 | 结构完整性（阶段/文件/commit） | 4 | 4 | 0 |
| R1.5 | 外部引用事实核查（tag/批数/锚点/脚本模式） | 5 | 5 | 0 |
| R2 | 可执行性（干跑：TOTAL=1、64 样本、10 行断言、27/27） | 6 | 6 | 0 |
| R2.8 | LLM 可执行性（路径/命令/枚举/无歧义） | 3 | 3 | 0 |
| R3 | 风险与边缘（假通过、互不阻断、越权、格式工具误用） | 5 | 5 | 0 |
| **REFINE-1** | **粒度（20 Task 全 ≤30min/checkpoint ≤15）、逐 Task commit、取消语义代理硬门、ruff 范围修正、S1 diff 白名单、非阻断策略** | **6** | **6** | **0** |
| **IMPROVE-1** | **T1.2 AC#5 双缺陷（空转 + 不可满足）、先验收后提交门控、失败与既有 commit 如实登记（未重做任务）** | **3** | **3** | **0** |
| **终止** | **T2 — issue 清零且 AC 可复跑** | | | **0** |

## 执行记录（执行后回填）

| 阶段 | Task | commit | 完成时间 | AC 结果 | 备注 |
|---|---|---|---|---|---|
| S1 | T1.1 | `86e9b00` | 2026-11-03 08:36 | **PASS（4/4）**：`tags-contain-5072` 0/0、`contract OK … version=v2026.10.30`、README 的 S1–S4 行=4 且 T*.* 行=20、`数据未进入任何发布 tag`=1 且 `无需重发`=1、diff 恰 2 文件 | 原始基线 `/tmp/opencode/t5184-baseline.txt` |
| S1 | T1.2 | `52dc8e8` | 2026-11-03 08:39 | **PASS**（IMPROVE-1 修订 AC#5 后独立复验 7/7）；初次 **FAIL（AC#5）** 如实保留 | 初次失败未撤销 commit、未 amend；见 §Execution Log E1 |
| S1 | T1.3 | `791d189` | 2026-11-03 10:28 | **PASS**：pm-coordinator 追加 #5184 备注 + readback `status=doing`；diff 仅 `docs/reviews/t5184/README.md` | Receipt `.receipts/T5184-status-writeback.r1.json` |
| S2 | T2.1 | `f2a520f` | 2026-11-03 10:31 | **PASS**：`m3-evidence-rows.tsv`，`TOTAL= 1`（`aliases.tsv:397`） | 只读扫描，零数据改动 |
| S2 | T2.2 | `d87da10` | 2026-11-03 10:45 | **PASS**：下游投影实测（zh→en 不可达等） | — |
| S2 | T2.3 | `769c168` | 2026-11-03 10:57 | **PASS**：概念级适用性 + 来源可得性；H1/H2 PASS、H3 `UNDECIDABLE`（上游 6 文件 0 命中） | H3 不可得不判 PASS |
| S2 | T2.4 | `fa602ed` | 2026-11-03 11:12 | **PASS**：A/B/C 三选项 + `可逆性:`；父计划 M3 行追加 `S2 查证完成`，**M3 保持未勾** | `已授权/用户已批准` 命中 0；`待用户裁决 (D2)` |
| S3 | T3.1 | `4d8d003` | 2026-11-03 11:33 | **PASS**：`m4-sample.tsv` 10 行确定性清单（shift99 / sixcol80） | 独立复算 10/10 一致 |
| S3 | T3.2 | `477fc7f` | 2026-11-03 11:39 | **PASS**：10 行逐列语义 + 逐列适用性推理 | — |
| S3 | T3.3 | `d16a11d` | 2026-11-03 11:48 | **PASS**：M4 写回 `[x]`；`^判定: PASS$` = 10、FAIL=0、UND=0 | 仅在授权阶段勾选 |
| S4 | T4.1 | `c2d3d3a` | 2026-11-03 11:52 | **PASS**：8×8 manifest + 8 条 `# group_sample_sha256` | 哈希口径见 §E2 |
| S4 | T4.2 | `6dde42b` | 2026-11-03 12:13 | **PASS**：G1 5 PASS / 3 FAIL / 0 UND（87 ids） | — |
| S4 | T4.3 | `76cd84d` | 2026-11-03 12:14 | **PASS**：G2 8/0/0（100 ids） | — |
| S4 | T4.4 | `a174af4` | 2026-11-03 12:14 | **PASS**：G3 8/0/0（100 ids） | — |
| S4 | T4.5 | `488a1c3` | 2026-11-03 12:14 | **PASS**：G4 6/2/0（100 ids） | 报告字段用 `- 原始语料:` 行内形（O5） |
| S4 | T4.6 | `1cf7bab` | 2026-11-03 12:37 | **PASS**：G5 6/2/0（100 ids） | 同上（O5） |
| S4 | T4.7 | `0f335ec` | 2026-11-03 12:37 | **PASS**：G6 6/2/0（100 ids） | 同上（O5） |
| S4 | T4.8 | `44c7d90` | 2026-11-03 12:38 | **PASS**：G7 8/0/0（100 ids） | — |
| S4 | T4.9 | `495f904` | 2026-11-03 12:38 | **PASS**：G8 8/0/0（69 ids） | — |
| S4 | T4.10 | `3d54c3e` | 2026-11-03 13:03 | **PASS**：汇总 64 抽检 = **55 PASS / 9 FAIL / 0 UNDECIDABLE**，台账 D1–D9=9 行 | **FAIL=9 > 0 ⇒ M1 保持未勾** |

**合计**：20 / 20 Task 已提交，全部 `#T-5184`，未 push；执行区间 `115da74..3d54c3e`，`git diff 115da74 3d54c3e -- terms/ artifacts/ pipeline/ scripts/` 为空。

## Execution Log

### E1 — T1.2（2026-11-03）AC FAIL；commit 已生成但任务未完成

```json
{
  "error_id": "E1",
  "task_id": "T1.2",
  "date": "2026-11-03",
  "error_type": "test_failure",
  "summary": "T1.2 内容 AC 4/4 PASS，但 AC#5（父计划 diff 范围门）不可满足：词白名单未容纳 §5072 被删旧行；且旧正则 ^[+-][^+-] 对以 '- ' 开头的内容行匹配 0 行（空转）。命令块以 ';' 串联 AC 与 commit、未设 set -e，AC 失败后仍生成了 52dc8e8。",
  "root_cause_guess": "AC#5 设计同时存在两个机械缺陷：①diff 行内容本身以 '- ' 开头（diff 前缀后紧跟 '-'），^[+-][^+-] 一行也匹配不到 ⇒ 检查空转；②白名单只含 M1|M3|M4|PM #5184|归档仍暂缓，而 §5072 从句被删除的旧行只含 'PM **5072**' ⇒ 收紧后必然违规。叠加命令块缺少 set -e 与 AC→commit 门控。",
  "confidence": "HIGH",
  "retry_suggestion": "改为「剥离首个 diff 标记 → 内容前缀精确锚点」白名单（同时允许 §5072 旧行与新行），并加改动内容行数 = 8 双断言；命令块以 set -euo pipefail 开头，内容 AC + git diff --cached 暂存区范围 AC 全过才 commit。",
  "blocked_downstream": ["T1.3", "S2", "S3", "S4"],
  "attempted_fixes": [
    "IMPROVE-1：仅修改 .github/plans/5184-four-stage-closeout.md（AC#5、命令门控、风险表 R12、审查日志、执行记录、本节）；未改数据、未改 52dc8e8、未产生新 commit、未 push"
  ]
}
```

**事实（`date` 实测 `2026-11-03T08:40:56+08:00`；`git rev-parse HEAD` = `52dc8e8fb1d49b67c5e8167a347e3cdfafffaa2a`）**：

- `86e9b00`（T1.1）：4 条 AC 全 **PASS**（`tags-contain-5072` 0/0；`contract OK … version=v2026.10.30`；README `| S1..S4 |`=4、`| T*.* |`=20；`数据未进入任何发布 tag`=1、`无需重发`=1；diff 恰 2 文件）。
- `52dc8e8`（T1.2）：内容 AC 4/4 **PASS**（status=1、unreleased=1、`PM #5184 收口中`=3、`^- \[x\] M[134]:`=0）；文件范围 **3 文件 OK**；**AC#5 FAIL**——旧写法空转（0 行被检查），按字面收紧则为 1 条违规（§5072 旧行）。工作树提交后干净（仅未跟踪本计划文件），**未 push**。
- **状态判定**：T1.2 **未完成**（AC 未全过）。`52dc8e8` 保留在历史中：**不重写、不 amend、不 revert**；本轮**不重做任务、不改数据、不改其他文件、不 commit**。
- **残留观察（需编排者裁决，本计划未改）**：父计划 §5072 从句的追加位置产出 `` `todo`（2026-11-03 实测：…归档仍暂缓。），归档会误示 `` —— 句中出现 `）。，`。内容仍在该锚点行内、未越界；若需修，应在 T1.2 重执行时把追加点上移为「替换 `todo` 后原有 `。` 之前」，并同步 AC#5 的行内容锚点。

**复验命令（只读，可直接粘贴；期望输出 `3 行`、`8`、`0`、`1/1/3/0`）**：

```bash
cd /home/gw/opt/fusion-terms
PARENT=.github/plans/terminology-coverage-and-definition-quality.md
# 1) 声明文件恰 3 个
git diff --name-only 86e9b00 52dc8e8 | sort
# 2) 父计划改动内容行恰 8（4 锚点 × 旧/新）
git diff -U0 --no-color 86e9b00 52dc8e8 -- "$PARENT" | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//' | wc -l
# 3) 白名单外行恰 0
git diff -U0 --no-color 86e9b00 52dc8e8 -- "$PARENT" | grep -E '^[+-]' | grep -vE '^(---|\+\+\+)' | sed -E 's/^[+-]//' | grep -vcE '^- \[ \] M[134]:|^- \*\*未做（用户裁决'
# 4) 内容 AC（依次期望 1 / 1 / 3 / 0；末条输出 0 时 grep exit=1 属无匹配，正常）
grep -c '^status: "done-execution (data unreleased)"$' .github/plans/5072-w3a-evidence-definition-backfill.md
grep -c '数据未进入任何发布 tag' .github/plans/5072-w3a-evidence-definition-backfill.md
grep -c 'PM #5184 收口中' "$PARENT"
grep -c '^- \[x\] M[134]:' "$PARENT" || true
```

> 复验通过只解除「机械门不可满足」这一缺陷；**T1.2 是否记为完成仍由编排者裁决**（本轮未标完成）。


### E2 — CLOSEOUT（2026-11-03）：20 Task 全量执行完成 + 独立验收 V1–V9 PASS；计划归档

```json
{
  "event_id": "E2",
  "type": "closeout",
  "date": "2026-11-03",
  "date_measured": "Tue Nov  3 03:06:54 PM CST 2026",
  "execution_range": "115da749251f6a8c94e8a1d4ea0ce3c412c614bf..3d54c3ec877159ad3c0222b33c52434b3905426c",
  "commits": 20,
  "tasks_completed": "20/20",
  "acceptance": {
    "report": "/tmp/opencode/t5184-final-acceptance.md",
    "verifier": "acceptance-verifier",
    "verdict": "V1-V9 全 PASS",
    "probes": {"P1": "registry_batch_verify --self-test 27/27 assertions passed", "P2": "pytest -q 178 tests passed"}
  },
  "parent_plan_manual_items": {
    "M1": "未勾 — 抽检 64 中 PASS 55 / FAIL 9 / UNDECIDABLE 0，未达 64/64",
    "M3": "未勾 — S2 查证完成但人工裁决未发生，待用户裁决 (D2)",
    "M4": "已勾 — 10/10 PASS"
  },
  "archive": ".github/plans/completed/5184-four-stage-closeout.md",
  "data_changes": "none (git diff 115da74 3d54c3e -- terms/ artifacts/ pipeline/ scripts/ 为空)"
}
```

**收口动作与边界**：

1. **本 E2 落实的是文档收口，不是第 21 个执行 Task**。只改 `docs/reviews/t5184/README.md` 与计划文件本身（含归档移动）；未改任何数据（`terms/`、`artifacts/`、`pipeline/`、`scripts/`）、未改任何组报告、**未改父计划** `terminology-coverage-and-definition-quality.md`（M1/M3 保持未勾、M4 保持已勾，均按原样）。
2. **哈希口径固定为已验收区间**：所有复算命令锚定 `115da74..3d54c3e`。**禁止**用 `HEAD~20..HEAD`——收口 commit 会使 `HEAD` 前移，`HEAD~20` 会滑出已验收区间，令 commit 计数、数据零改动与行数断言失真。
3. **样本集哈希契约（V9 固化，O3 关闭）**：`sha256('\n'.join(sorted(ids)))`——id **升序排序**、**换行连接**、**不含末尾换行**、UTF-8。本收口独立复算 8/8 MATCH；同组加末尾换行 → MISMATCH（G1 `317638db…053d36a9` vs `03f3c7a9…5bad10c`）。复算脚本见 `docs/reviews/t5184/README.md` §哈希口径与复算例。
4. **表述边界**：64 个样本 `concepts.tsv` 第 8 列 `source` 全为 `corpus`（64/64）⇒ 仅证明「notes 原文仓内可得」，`UNDECIDABLE=0` 结构上成立；**不构成**对 GB/T / IAEA / ITER / URL 外部依据路径的验证（四类零覆盖，O4 保留为非阻塞项）。
5. **E1 保留**：T1.2 初次 AC#5 FAIL 的 finding 与 `52dc8e8` 原样保留，未 amend / 未 revert / 未改写；IMPROVE-1 后的独立复验结论并存记录，不覆盖历史。
6. **归档**：按「已执行的计划 → `completed/`」规则，本文件移动至 `.github/plans/completed/5184-four-stage-closeout.md`；`docs/reviews/t5184/README.md` 以绝对路径指向归档位置。
7. **未 push**：`git status -sb` = `## master...origin/master [ahead N]`，收口 commit 追加于 20 个执行 commit 之后。

**收口复验命令（只读）**：

```bash
cd /home/gw/opt/fusion-terms
git rev-list --count 115da74..3d54c3e                                     # 20（不含收口 commit）
git log --oneline 115da74..3d54c3e --grep='#T-5184' | wc -l              # 20
git diff --stat 115da74 3d54c3e -- terms/ artifacts/ pipeline/ scripts/  # 空
git diff --check 115da74 3d54c3e                                         # 空
test -f .github/plans/completed/5184-four-stage-closeout.md && echo ARCHIVED
test ! -f .github/plans/5184-four-stage-closeout.md && echo MOVED
```
