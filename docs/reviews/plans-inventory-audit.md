# `.github/plans/` 全量盘存审计（2026-11-06）

- **触发**：用户 2026-11-06 授权「现在做全量审计（推荐）」，承接前次 7/24 部分审计的结论。
- **执行基线**：HEAD `2836544`（`master` ahead 42，无 tag，tracked tree clean）。
- **审计范围**：除下述硬排除项外的全部 `.github/plans/*.md`（含 `completed/` 已有的 5 个既往归档，但不改动它们）。
- **动作边界**：只读分析 → 一次有界归档（`git mv`，不改文件内容）→ 本报告。未触碰 `terms/`、`artifacts/`、`pipeline/`、`dist/`、`CHANGELOG.md`；未 push、未打 tag、未建 PM 任务。
- **归档 commit**：`124bb8b docs(plans): archive 13 completed/superseded plans (#T-5184)`（纯 rename，`13 files changed, 0 insertions(+), 0 deletions(-)`）。

## 硬排除项（本次未读内容、未移动、未提交）

| 路径 | 原因 |
|---|---|
| `.github/plans/5184-m3-m1-repair.md` | 本会话在用，故意 untracked |
| `.github/plans/terminology-coverage-and-definition-quality.md` | 父计划，刚在 R11 下更新 |
| `.github/plans/5072-w3a-evidence-definition-backfill.md` | R2/R3 修复需单独授权；已有 `docs/reviews/5072-status-reconciliation.md` |
| `.github/plans/publication-program-lre-scientificdata.md`、`docs/publication/`、`evaluation/` | 另一会话并发工作 |
| `.github/plans/t4973-batches/`（153 个 tracked 产物） | 非计划文档，而是 `scripts/registry_coverage_report.py --emit-lists` 的生成物；README 明确其路径（README:69、脚本:43），移动会破坏幂等校验 |

## 「模板噪声」收敛规则（全程一致适用）

**声明**：checkbox 分两类，只有「任务级完成证据」才计入完成判定。

1. **任务级 checkbox = 证据**：`#### ✅ Task n.m: …` 标题或任务内 `- ✅ …` 验收条目。
2. **清单级 `- [ ]` = 模板噪声，不参与完成判定**：
   - 「回归检查清单」「验收标准」块中的 `- [ ]`——尤其是**从未勾选却与任务块 ✅ 并存**的；
   - 引用**历史基线数字**的条目（如 `concepts.tsv 行数 = 1476`、`≥ 2947`、`≥ 2398`）——注册表此后已扩到 **3075 concepts**（`validate_registry` 权威口径），这些阈值对今天的仓库已无判别力；
   - `无歧义`/probe/deferred/list-style 形式的块。
3. **外部锚点复核**：归档前用**与基线无关的当前事实**复核（concept_id 存在性、`evidence.tsv` 的 `internal:registry-gap-review:batchN` 行数、allowlist 关键 token、`artifacts/*` 当前实测值），而非依赖计划里的旧数字。
4. **例外（升级为 AMBIGUOUS）**：若清单级 `- [ ]` 是**唯一**完成信号（既无 ✅ 任务标题、也无任何完成/归档标记），一律判 (d) 而非 (a)，即使内容看起来已完成。

> 该规则直接修正了前次部分审计里的两处误判：`batch4`/`batch5` 的 7 个未勾选 `- [ ]` 全部是**回归检查清单**条目，而它们的 7/7、9/9 任务标题均为 ✅，且被 `4ce9999` 的归档声明覆盖 —— 它们是 (a)，不是「只带模板勾选框」的疑似未完成项。

## 逐计划分类表

图例：`*` = 本次归档。`✅`/`[ ]` = `- [x]` / `- [ ]` 计数。mtime 为文件 mtime（全部 19 个归档候选在 2026-10-25 / 04-14 被同一批格式化提交触碰，故 mtime 无区分力，证据列改用 git 与数据锚点）。

| 计划 | mtime | ✅/[ ] | 类 | 证据 | 动作 | 遗留 |
|---|---|---|---|---|---|---|
| `expand-registry-batch3.md` * | 2026-10-25 | 0/8 | (a) DONE | 首行标记「已归档 — 批次 concept 19/19 在 registry 中」；7 个执行 commit（`e944dcc`…`f672dda`, 2026-04-04）全部 `[Plan: expand-registry-batch3] Task n.m`；`evidence.tsv` 有 18 行 `registry-gap-review:batch3`，18 个 concept_id 全部在 `concepts.tsv`；6 个 zh allowlist 术语全部命中。8 个 `[ ]` 全为清单级旧基线 | `git mv` | 声明「19/19」vs 18 条 evidence 差 1：multi/single-module-segment 计 1 家族，属措辞不精确，非缺口 |
| `expand-registry-batch4.md` * | 2026-10-25 | 0/7 | (a) DONE | 首行「已归档 — concept 20/20」；7/7 任务标题 ✅；7 个 `[Plan: expand-registry-batch4]` commit；evidence `batch4` = 19 行，19 个 concept_id 全在；PSA/HAZOP/FMEA/SBO/LBB/SIL/TAA/TMP/RGA/FAT/SAT 全部可在 `translation_dict` 命中（含 `en2zh_short`） | `git mv` | 计划里的 `≥ 2947`/`≥ 2398` 阈值已过期（当前 domain_terms 6375 行 / en2zh 4676 对），仅记录不阻塞 |
| `expand-registry-batch5.md` * | 2026-10-25 | 0/7 | (a) DONE | 首行「已归档 — concept 26/26」；9/9 任务 ✅；9 个 batch5 commit；evidence `batch5` = 25 行，concept_id 全在；allowlist PSA/HAZOP/FMEA/SBO/TMP/RGA/FAT/SAT 各 1 命中；`FLiBe`、`锂靶` 翻译未回归 | `git mv` | 同上，旧阈值（`≥ 2966`）过期 |
| `expand-registry-batch6.md` * | 2026-10-25 | 0/8 | (a) DONE | 首行「已归档 — Task 1.1–5.1 全部完成（7/7）」；8 个 batch6 commit 至 `3b93fb0`（Task 4.1 全量验证导出测试）；evidence `batch6` = 29 行（+1 行在 `b8d4fda` 被 M1 D8 合并 `plasma-termination→plasma-shutdown` 退役），29 个 concept_id 全在；PPS/BDBE/FES/SIC/PIE/CCWS/CHWS/HWC/ACP/NQA 全部命中 | `git mv` | 计划称 30 concepts；退役 1 个后 29 —— 属后续 M1 修复的正常合并，非缺口 |
| `expand-registry-batch7.md` * | 2026-10-25 | 0/8 | (a) DONE | 首行「已归档 — Task 1.1–4.1 全部完成（7/7）」；7 个 batch7 commit；evidence `batch7` = 30 行，concept_id 全在；ET/FT/CCF/SSA/IVC/MSM/PLC/HMI/PCS/PSI/PMI 全部命中 | `git mv` | 旧阈值（`≥ 2640`/`≥ 3111`）过期 |
| `expand-registry-batch8.md` * | 2026-10-25 | 0/9 | (a) DONE | 首行「已归档 — Task 1.1–4.1 全部完成（7/7）」；7 个 batch8 commit；evidence `batch8` = 30 行，concept_id 全在；`hepa-filter`、`detritiation-factor` 在册 | `git mv` | 旧阈值（`≥ 2667`/`≥ 3193`）过期 |
| `expand-registry-batch9.md` * | 2026-10-25 | 0/14 | (a) DONE | 首行「已归档 — Task 1.1–4.1 全部完成（7/7）」；7 个 batch9 commit；evidence `batch9` = 30 行，concept_id 全在；CVS/HEPA/NEG/MIG/RID 唯一映射均命中 | `git mv` | 无 |
| `ai-mistranslation-antipattern-expansion.md` * | 2026-10-25 | 0/7 | (a) DONE | 首行「已归档 — Task 1.1–8.1 全部完成（末次全量验证 @ `9c12d30`）」；`9c12d30` 实存 = 2026-04-13 「Task 8.1: full validation passed」 | `git mv` | 7 个 `[ ]` 全是清单块，含旧基线 `concepts.tsv 行数 = 1476`（今 3208）—— 正是前次审计点名的陈旧项；✅ 标记优先，判 (a) |
| `authoritative-terminology-import.md` * | 2026-10-25 | 0/9 | (a) DONE | 首行「已归档 — Task 1.1–6.1 完成」，并**逐条解释**遗留的 Task 4.x（改由 pdf2md 完成，原 BLOCKED 失效）与 Task 5.2–5.4（未勾选但产物已落地）；`scripts/import_approved_terms.py` 存在 | `git mv` | Task 4.1–4.3 标题仍为 `⏸`、5.2–5.4 仍无 ✅，但正文已给出产物级替代证据 —— 保留原样归档，不做内容编辑 |
| `expand-terminology-coverage.md` * | 2026-10-25 | 0/9 | (a) DONE | 首行「✅ 已完成 — 220 条 concept 全部落地（24/24）」；抽查 `half-value-layer`/`tenth-value-layer`/`dbtt-shift` 均在 `concepts.tsv`；24 个 ✅ 任务标题 | `git mv` | 旧阈值（`query_expansions concepts > 1250`）今为 3075，已满足但不具判别力 |
| `pwi-divertor-fuelling-terminology-expansion.md` * | 2026-10-25 | 0/8 | (a) DONE | 首行「已归档 — Task 1.1–4.2 全部完成（10/10）」；10 个 ✅ 任务 | `git mv` | 旧基线 `1465→1473` 过期 |
| `substitute-supplement-batch80.md` * | 2026-10-25 | 0/7 | (a) DONE | 首行「已归档 — 6/6；5 条替换规则已入 registry 并出现在 `terminology_substitutions.tsv`（Batch 90, `ed8825a`）」；`ed8825a` 实存；`hot-cathode-ion-gauge`/`diamagnetic-flux-signal` 在册；5 个误用词在 `terminology_substitutions.tsv` 命中；`轫致辐射` 不在 `allowlist_zh.txt`（该断言为「不存在」型，可复核） | `git mv` | `vale/terminology_substitute.yml` 在仓库中不存在（计划断言其存在）；但该文件非本次动作产物、也非 CI 门禁，记入遗留 |
| `next-improvement-cycle.md` * | 2026-09-10 | 0/11 | (b) SUPERSEDED | 第 3 行「✅ 已归档 —— 本文为历史执行计划（v2026.03.23 周期），已由 `repo-improvement-2026-03-25.md` 执行计划替代并完成」——被取代方与替代方**均已完成** | `git mv` | 无 |
| `fix-translation-dict-gaps.md` | 2026-04-14 | 0/9 | (a) DONE（弱证据，已归档） | 首行为单独的「✅ 状态：已归档」，无任务计数；8 个 ✅ 任务标题；用户报告的具体 P0 词条已可实证：`lithium ceramic pebble bed`→锂陶瓷球床、`lithium ceramic`→锂陶瓷、`ceramic pebble bed`→陶瓷球床、`WCPB`→水冷球床包层、`nb3sn` 在册 | `git mv` | 计划断言「`增殖包层` 被 deprecated 阻断 zh2en」——今 `blanket` 概念在册且 `增殖包层` 有 alias 行；旧断言的现状未被重新核验 |
| `mcp-dict-improvements-2026-04.md` | 2026-04-14 | 0/7 | (a) DONE（弱证据，已归档） | 同上，单独「✅ 状态：已归档」；9/9 ✅ 任务；四项目标均可实证：`deuterium-tritium`→氘氚、`D-T`→氘氚、`实验包层模块`→test blanket module、`氘氚`→deuterium-tritium、`缓解`↔`mitigation` 双向、`CFETR` 在册、`en2zh_short` 已含 396 条 abbr-lang 条目（正是 Task 2.2 的产出） | `git mv` | `产氚模块` 仍映射到 test blanket module（计划要求「作为 alias 保留」，一致） |
| `repo-improvement-2026-03-25.md` | 2026-04-14 | 0/12 | (a) DONE（弱证据，已归档） | 单独「✅ 状态：已归档」；24/24 ✅ 任务；12 条清单中可独立复核的均通过：`~/.local/bin/rime_import_wordlist.py` 在 `pipeline/` 零引用、`extract()` 由 542 行降到 134 行（`pipeline/extract_candidates.py:1123-1256`）、`CONTRIBUTING.md` 存在 | `git mv` | 一条清单「`git log origin/master --oneline -1` 与本地 HEAD 一致」当前不成立（ahead 42，本会话期间无 push 权限）—— 属环境态而非计划缺陷，不阻断归档 |
| `repo-hardening-2026-03-24.md` | 2026-10-25 | 0/10 | (b) SUPERSEDED | 首行「已归档 —— 由 `repo-hardening-2026-04-14.md` 周期取代并完成（task 23/23）；🔴 项已修复经 `full-repo-2026-03-25.md` 复核确认」；23 个 ✅ 任务；替代方 `repo-hardening-2026-04-14.md` 确实已在 `completed/` | **保留**，见下 ⚠️ | 同上 |
| `short-token-segregation.md` | 2026-04-14 | 0/7 | (a) DONE（弱证据，已归档） | 单独「✅ 状态：已归档」；6/6 ✅ 任务；核心断言可实证：`en2zh` 无 ≤2 字符 ASCII 键、`en2zh_short` 每条含 `concept_id`+`zh`（396 条） | `git mv` | 清单里 `registry_exports.json` 的 `pairs_en2zh_short` 字段未单独核验 |
| `translation-enhancement.md` | 2026-04-14 | 0/7 | (a) DONE（弱证据，已归档） | 单独「✅ 状态：已归档」；12/12 ✅ 任务；主线产出 `translation_dict.json` 存在且三桶完整（en2zh 4676 / en2zh_short 396 / zh2en 3418） | `git mv` | 无 |
| `_project-snapshot.md` | 2026-10-29 | 0/0 | 非计划 | 快照文件不是执行计划 | 不动 | ⚠️ 计数已明显过期：快照写 concepts 3076 / aliases 10249 / evidence 3203 / domain_terms 未列；`validate_registry` 权威口径今天为 **3075 concepts / 10250 aliases / 3202 evidence / 6150 definitions**（注：`3208`/`10270` 是本报告早期用「非注释原始行数」量出的**不同口径**，不是注册表漂移），且 `Updated` 停在 2026-10-29（8 天，刚越 7 天门限） |

### 明确未归档的两项

- **`repo-hardening-2026-03-24.md`**：证据充分为 (b)，**但我决定保留并上报**。理由：(i) 它是 19 份中唯一「mtime 被格式化提交 `8f51d52` 推到 2026-10-25」但仍留在 `plans/` 根下、且文件引用的 `../reviews/full-repo-2026-03-24.md` **在仓库中不存在** 的特殊个例；(ii) 它与已归档的 `5184-four-stage-closeout.md`、`registry-evidence-adoption.md` 同属「历史周期记录」，是否连同类簇一并整理属**策略决定**而非本次有界动作。→ 交用户决定。
- **`fix-translation-dict-gaps` / `mcp-dict-improvements-2026-04` / `repo-improvement-2026-03-25` / `short-token-segregation` / `translation-enhancement`**：这 5 份的完成证据只有「✅ 状态：已归档」这一句，**没有任务计数**（属弱证据档），但两份计划内的断言我已逐条用当前数据实证。按「有归档标记 → (a)」判定并归档；若策略上要求「完成证据必须带任务计数」，这批应回滚 —— 已在「下一步」中列为政策项。

## 分类统计

审计的计划文件共 **17** 份（= 全部 21 个 `plans/*.md` 减去 4 份硬排除，再减去 `_project-snapshot.md` 这个非计划文件）。

| 类 | 数量 | 计划 |
|---|---|---|
| (a) DONE | **14** | 9 份强证据（带任务计数 / 数据锚点）：`batch3/4/5/6/7/8/9`、`ai-mistranslation-antipattern-expansion`、`authoritative-terminology-import`、`expand-terminology-coverage`、`pwi-divertor-fuelling-terminology-expansion`、`substitute-supplement-batch80`；5 份弱证据（仅「✅ 状态：已归档」一句，主要断言已逐条实证）：`fix-translation-dict-gaps`、`mcp-dict-improvements-2026-04`、`repo-improvement-2026-03-25`、`short-token-segregation`、`translation-enhancement` |
| (b) SUPERSEDED | **2** | `next-improvement-cycle`（→ `repo-improvement-2026-03-25`）、`repo-hardening-2026-03-24`（→ `repo-hardening-2026-04-14`） |
| (c) GENUINELY OPEN | **0** | 范围内无「真开放」计划 |
| (d) AMBIGUOUS | **0** | — |

**动作口径**：本次移动 **13 份** = (a) 中 12 份 + (b) 中 1 份（`next-improvement-cycle`）。
**未移动的同档计划 1 份**：(b) 中 `repo-hardening-2026-03-24`（证据充分，但属「历史周期计划」类簇整理，需策略裁决）。

计数校验：14 (a) + 2 (b) = 16 份计划 + `_project-snapshot.md`（非计划）+ **本次移动 13** + **保留 1** → 归档后 `plans/*.md` 余 9 个、`completed/*.md` 为 18 个（原 5 + 13）。

## 保留在 `.github/plans/` 的清单与其开放项

归档后 `.github/plans/` 根下实存 9 个条目（8 个 `.md` + `t4973-batches/` 目录）：

| 文件 | 状态 | 开放项 / 说明 |
|---|---|---|
| `5072-w3a-evidence-definition-backfill.md` | 硬排除（仍在根下） | R2/R3 修复待单独授权 |
| `5184-m3-m1-repair.md` | 硬排除（仍在根下，untracked） | 会话在用 |
| `terminology-coverage-and-definition-quality.md` | 硬排除（仍在根下） | 父计划（R11 刚更新） |
| `publication-program-lre-scientificdata.md` | 硬排除（仍在根下，untracked） | 另一会话并发 |
| `repo-hardening-2026-03-24.md` | (b) SUPERSEDED，**保留待裁决** | 引用 `../reviews/full-repo-2026-03-24.md` 不存在 |
| `_project-snapshot.md` | 非计划（快照） | counts 过期 + `Updated` 2026-10-29（越过 7 天门限） |
| `t4973-batches/`（目录，153 tracked 文件） | 生成物，非计划 | 被 `scripts/registry_coverage_report.py:43` 引用，移动会破坏幂等校验 |
| `completed/`（目录） | 归档区 | 由 5 个增至 18 个 `.md` |

「保留在根下」的开放项汇总：仅 `repo-hardening-2026-03-24.md` 一项属**本次可决策未决**；其余 3 个 `.md` 是硬排除，2 项是硬排除的并发/在办工作。

## 需用户 / 政策裁决的下一步

1. **`repo-hardening-2026-03-24.md` 去留**：(b) 证据充分，但属「历史周期记录」类簇整理，需决定是否与其它历史周期计划一并归档；同时决定是否补一份 `docs/reviews/full-repo-2026-03-24.md` 的缺失说明。
2. **弱证据档位政策**：`fix-translation-dict-gaps`、`mcp-dict-improvements-2026-04`、`repo-improvement-2026-03-25`、`short-token-segregation`、`translation-enhancement` 只有「✅ 状态：已归档」一句、无任务计数。若政策要求「完成证据必须含任务计数或数据锚点」，这 5 份需回滚；本次已逐条用当前数据实证其主要断言（见上表），固判归档。
3. **`_project-snapshot.md` 刷新**：按 `validate_registry` 权威口径应为 concepts **3076→3075**、aliases **10249→10250**、evidence **3203→3202**（definitions 6152→6150 亦可补），`Updated` 2026-10-29 已越 7 天门限。属 doc-maintainer 常规职责，本次未改（不在授权动作内）。⚠️ **口径警告：不得使用「非注释原始行数」（concepts 3408/3208、aliases 11569/10989），该口径与门禁不一致。**
4. **旧基线阈值清理**：已归档计划正文中的 `≥ 2947`、`≥ 2398`、`concepts.tsv 行数 = 1476` 等阈值已永久失真。本次遵守「绝不编辑归档文件内容」，故**只在报告中记录**；若要修正需单独立项（且应在归档前做，现在只能加注）。
5. ~~**`vale/terminology_substitute.yml` 缺失**~~ → **核正（2026-11-06 复测）**：该文件**存在**于 `artifacts/vale/terminology_substitute.yml`（75,738 bytes，mtime 2026-11-04），先前判定为**路径误判**（检索了 `vale/` 而非 `artifacts/vale/`）。⇒ `substitute-supplement-batch80.md` 的断言成立，**无缺口**。
6. **`evidence.tsv` 行数口径**：计数为 3202（`wc -l` 3203 行含表头），快照与 `t4973-batches/final-verification.md` 均写 3203 —— 差 1 是表头，建议统一口径。

## 复核方法（可复跑）

```bash
# 任务级证据
grep -c -E '^#### ✅ Task' .github/plans/completed/expand-registry-batch*.md
# 外部锚点：batchN evidence 行数 + concept_id 全部在 concepts.tsv
awk -F'\t' '$2 ~ /registry-gap-review:batch[0-9]/ {b=$2; sub(/.*batch/,"",b); print b"\t"$1}' \
  terms/registry/evidence.tsv | sort | uniq -c
# 当前注册表实测
python3 -m pipeline.validate_registry
```

---

## 8. 归档策略裁决（2026-11-06，用户授权「做第 2 项」）

### 8.0 先更正一处执行不一致

上文 §4 表格把 5 份「弱证据」计划（`fix-translation-dict-gaps`、`mcp-dict-improvements-2026-04`、`repo-improvement-2026-03-25`、`short-token-segregation`、`translation-enhancement`）的 action 列写为 `git mv`，但 2026-11-06 复核发现**它们当时并未实际移动**（`plans/` 仍在、`completed/` 无；`124bb8b` 的 13 个 R100 移动不含它们）。本次已把「裁决 → 移动」补齐，故该表现已与实际一致。

### 8.1 5 份弱证据计划的逐条核验（每份 ≥2 条机械可核验断言）

| 计划 | 断言（来自计划原文） | 实测 | 结论 |
|---|---|---|---|
| `short-token-segregation` | ① `en2zh` 无 ≤2 字符 ASCII 键（原 39 个）② `en2zh_short` 396 条且每条含 `concept_id`+`zh` | ① **0 个** ② **396 条**，样本 `{'A': {'concept_id':'aspect-ratio','zh':'纵横比'}}`；`schema_version=2` | ✅ 确认归档 |
| `fix-translation-dict-gaps` | ① `lithium ceramic pebble bed`→锂陶瓷球床 ② `lithium ceramic`→锂陶瓷 ③ 术语族可解析（增殖包层/环向场线圈/接触剂量） | ① `en2zh['lithium ceramic pebble bed']='锂陶瓷球床'` ② `='锂陶瓷'` ③ `breeding blanket`/`toroidal field coil`/`contact dose rate` 均可解析；`in-vessel`/`ex-vessel` 概念存在 | ✅ 确认归档 |
| `mcp-dict-improvements-2026-04` | ① `D-T`→氘氚 ② `实验包层模块`→test blanket module | ① `zh2en['D-T']='deuterium-tritium'`、`en2zh['deuterium-tritium']='氘氚'` ② `zh2en['实验包层模块']='test blanket module'`、反向 `=实验包层模块` | ✅ 确认归档 |
| `translation-enhancement` | ① glue 概念落库 ② `internal:translation:glue-vocabulary` 证据存在 | ① `system/mode/device/calculation/material/simulation` 均 1 concept + 2 aliases，`en2zh` 分别 = 系统/模式/装置/计算/材料/模拟 ② 证据行 **25** 条 | ✅ 确认归档 |
| `repo-improvement-2026-03-25` | ① `extract()` 542→≤200 行 ② `--rime-script` 改为 config 驱动 + 回退默认 | ① **135 行**（`pipeline/extract_candidates.py:1123`）② 3 个脚本均读 `rime_cfg.get("import_script")` | ⚠️ **确认归档，但登记一处计划内部矛盾**（见 8.2） |

### 8.2 发现的计划内部矛盾（`repo-improvement-2026-03-25`）

- 修改内容（`:230`）明确要求「改为从 config 加载的值，**否则回退到现有默认值**」⇒ 回退字面量**必须保留**；
- 但验收标准（`:239`）却写「`grep -rn "~/.local/bin/rime_import_wordlist.py" pipeline/` → **0 匹配**」，且 `:537` 该断言**至今未勾**；
- 实测：`config.toml [rime]` **未定义 `import_script`**，故回退字面量必然生效 ⇒ 3 个 tracked 文件仍含该路径（`rime_export.py:93`、`rime_import_safe.py:347`、`generate_dict_yaml.py:151`）。

**裁决**：实现符合「修改内容」的设计意图（config 驱动 + 回退），**不接受 `:239` 的字面 0 匹配口径**（该断言与 `:230` 自相矛盾，不可同时满足）。计划归档文件**内容不改**（冻结原则），矛盾记录于本节。**不**据此重开该计划；若日后要消除硬编码，应另立任务并把 `import_script` 写进 `config.toml`。

### 8.3 `repo-hardening-2026-03-24.md` 去留

| 判据 | 证据 | 结论 |
|---|---|---|
| 被取代 | 首行自述「由 `repo-hardening-2026-04-14.md` 周期取代并完成（task 勾选 23/23）」；取代方**已归档** | 支持归档 |
| 复核存在性 | 引用的替代复核 `.github/reviews/full-repo-2026-03-25.md` **存在**（10,092 B） | 支持 |
| 缺失引用 | `../reviews/full-repo-2026-03-24.md` 不存在 —— **该缺口已由计划首行自行声明** | 不构成阻塞 |
| 23/23 任务 | 头部 `✅ Task N.N` 23 处 | 支持 |

**裁决：归档**（`git mv` → `completed/`，R100，内容零改动）。

### 8.4 执行结果

- 本次移动 **6** 份：上表 5 份 + `repo-hardening-2026-03-24`，全部 **R100（内容零改动）**，单个 commit。
- 计划库现状：**active 4 / completed 25**。active 4 = `5184-m3-m1-repair.md`（在办）、`_project-snapshot.md`（非计划快照）、`publication-program-lre-scientificdata.md`（并发会话）、`terminology-coverage-and-definition-quality.md`（父计划台账）。
- 可逆性：全部为 `git mv`，`git revert` 即还原。

---

## 9. 父计划归档（2026-11-06，用户授权「做父计划归档」）

### 9.1 归档前体检

| 检查 | 结果 |
|---|---|
| 行首未勾项 `^- \[ \]` | **0** |
| 行首已勾项 `^- \[x\]` | **24** |
| `M1`–`M4` 手动验收 | **4/4 已勾**（M1 于 `7be0b14` 按 R11 收口；M3 于 `ea5411d` 关闭） |
| 归档前补齐的 3 项 | `D1`（确认无延期项）、`P1`（负向探针**实测 exit=2** + `ids file not found`，非静默 PASS）、`P2`（实测 `HEAD=e109f88`、`tracked_dirty=0`）｜commit `bd2bb94` |

### 9.2 执行

`git mv .github/plans/terminology-coverage-and-definition-quality.md .github/plans/completed/` ⇒ **R100（内容零改动，sha256 `833be597cfe2a9b6`）**。

**计划库现状：active 3 / completed 26。** active 3 = `5184-m3-m1-repair.md`（在办）、`_project-snapshot.md`（非计划快照）、`publication-program-lre-scientificdata.md`（并发会话）。

### 9.3 旧路径引用面（如实登记，本次不改写）

全仓 15 个 `.md` 引用旧路径 `.github/plans/terminology-coverage-and-definition-quality.md`，分两类：

| 类 | 文件 | 处置 |
|---|---|---|
| 历史留痕（审计产物 / 已完成计划 / 批次台账） | `t4973-batches/{README,red-green,w3a-acceptance}.md`、`completed/{5184-four-stage-closeout,5072-w3a-evidence-definition-backfill,registry-evidence-adoption}.md`、`docs/reviews/t5184/repair-m1-b3-suggestion.md`、`repair-m1-b4-merge.md` | **不改写**（审计产物与已冻结记录；路径语义仍指向同一文件，现位于 `completed/`） |
| 活文档 | 本审计报告、`docs/reviews/5072-status-reconciliation.md` | 本条即登记；后续新写引用请使用 `completed/` 路径 |

**影响评估**：计划引用为 Markdown 文本，不参与任何脚本/门禁解析（`grep` 全库无代码读取该路径）⇒ **零功能影响**，仅为人工跳转便利问题。
