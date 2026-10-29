# W3a（T3.1–T3.43，854 个中文首选名）验收记录

- 任务：PM **T-4973** / 计划 `.github/plans/terminology-coverage-and-definition-quality.md` §「Phase 3」
- 验收对象：`dda25c9^..4ead28b`（43 个命名 commit + 1 个冲突台账 commit）
- 记录时间：2026-10-29（`date -Iseconds` = 2026-10-29T11:36:26+08:00）
- 结论：**PARTIAL** — 数据门禁 **全 PASS**、blocking **0**；计划原文的「依据可核验」判据**结构性不可评估**且其**实质内容缺失**，故未签收为 PASS。

---

## 1. 三源交叉核对

| 来源 | 内容 | 结果 |
|---|---|---|
| 计划验收标准（§Phase 3「批次任务统一规格」4 条） | ①`--mode names` exit 0；②同上加 `--check-urls` exit 0；③冲突台账行数与批记录一致；④`validate_registry` exit 0 | ①③④ 实测 PASS；②**判据空转**（见 §3.1） |
| 执行者声明（计划 `## Execution Log` T3.1–T3.43） | 43/43 批、854/854 名、逐批四门禁 | 全部**可复现** |
| 实际产物（仓库当前状态 @ `4ead28b`） | `concepts.tsv` 854 行 `preferred_zh`；`w3-name-conflicts.tsv` 1 行观察 | 与声明一致 |

---

## 2. 独立复跑（本人 + 两个只读 `acceptance-verifier`）

### 2.1 机械门禁（本会话一手复跑）

| # | 命令 | exit | 关键输出 |
|---|---|---:|---|
| V1 | `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file .github/plans/t4973-batches/w3.ids --expect 854 --check-urls` | **0** | `ids=854 expect=854 verdict=PASS` |
| V2 | `.venv/bin/python scripts/registry_batch_verify.py --mode names --ids-file w3_b{01..43}.ids --expect <wc-l> --check-urls` | **0 ×43** | 逐批 `verdict=PASS`（b01–b42 expect 20、b43 expect 14） |
| V3 | `.venv/bin/python scripts/registry_row_audit.py --audit --expect-clean-all` | **0** | `is_clean:true`、`w0_is_clean:true`、7 项 clean 指标全 0、`cols_dist {8:3076}` |
| V4 | `.venv/bin/python -m pipeline.validate_registry` | **0** | `3076 concepts, 10249 aliases, 3203 evidence rows, 6152 definitions` |
| V5 | `.venv/bin/python -m pytest -q` | **0** | 175 passed |
| V6 | D2-6 闸门（`preferred_zh == preferred_en && 无 CJK`） | **0** | `d2_6_residual 0` |
| V7 | 逐列比对 `dda25c9^` vs `HEAD`（脚本化，按 concept_id 对齐） | **0** | 行数 3076→3076、**touched 854**、diff 列模式 `{(2,): 854}`（仅第 3 列）、`touched == w3.ids` **True**、无增删行、表头逐字节相同 |
| V8 | `git diff --stat dda25c9^..HEAD` | — | 仅 2 文件：`concepts.tsv`（854/854）+ `w3-name-conflicts.tsv`（+1） |
| V9 | 冲突扫描（全库 `preferred_zh` 重复 / 新名撞他人 zh-alias，限定 `w3.ids`） | — | `conflicts dup_preferred_zh=0 alias=0` |
| V10 | `.venv/bin/python scripts/registry_coverage_report.py --json` | **0** | `total 3076 / covered 2220 / uncovered 856 / coverage_pct 72.17` |

### 2.2 独立命名抽检（两个 `acceptance-verifier` 会话，只读）

| 会话 | 范围 | 抽样 | 命名 FAIL | 判定 |
|---|---|---:|---:|---|
| `ses_e7a4cd173ffelqcNVMNw15h6sP` | b01–b15（15 批 / 300 ids） | 45 行（3×15） | **0** | 机械项 PASS |
| `ses_e7a4cd173ffdU8NIkpZoWm4QhY` | b16–b43（28 批 / 554 ids） | 85 行（6×14 + 1 组） | **0** | **PARTIAL**（证据缺口） |

合计抽检 **130 行 ≥ 10%（854×10% = 86）**，覆盖 concept/device/material/organization/method 等类别；**0 条命名失败**。

---

## 3. 为什么是 PARTIAL 而不是 PASS

### 3.1 判据②「依据可核验」在 `--mode names` 下**空转**（结构性缺陷，先于 W3a 存在）

```text
check_names(corpus, ids, *, allow_latin_names=frozenset()) -> list[Violation]
check_names 源码中出现 "check_urls": False
dispatch: `if mode == "names": return check_names(corpus, ids)`   # 不传 check_urls
```

⇒ 对 43 批执行的 `--check-urls` **不会探测任何 URL**（仅在 `--mode definitions` 内生效，`registry_batch_verify.py:326/363`）。
计划把「同上加 `--check-urls` → exit 0」当作「依据可核验」的机械判据，但**该 flag 在 names 模式是 no-op** ⇒ 判据②**exit 0 但空洞**，不能作为依据充分的证据。

### 3.2 依据的**实质内容**在当前数据里缺失

| 观测 | 实测值 | 说明 |
|---|---:|---|
| `w3.ids` 内 concept 的 `definition(lang=zh)` 仍为占位模板 | **747 / 854** | 文本形如 `聚变/核工程术语，对应英文“X”`（`definitions.tsv`） |
| `w3.ids` 内 evidence 行的 `quote` 去重后取值数 | **1**（空串） | 854/854 行 quote 为空 ⇒ 无引文可核 |
| b16–b43（554 ids）evidence 来源 | `IAEA-Safety-Glossary-2018` **554/554** | 裸来源名、**非 URL** ⇒ 即便接通 `--check-urls` 也无从探测 |
| 全部 `w3.ids` evidence 行的来源 | `IAEA-Safety-Glossary-2018` 782 / `https://www.iter.org/fusion-glossary` 72 | 仅 72 行带 URL |

⇒ 计划 §Phase 3 开头允许「无仓内出处者依 **D2-5=A** 用 `preferred_en` + 权威仓外 URL（须 200）」。当前实现**没有为这 747 行补 URL / 引文**，因此该路径的**证据部分未落地**（命名本身已落地）。

### 3.3 非阻断的既有缺陷（W3a 未引入）

| 项 | 实测 | 归因 |
|---|---|---|
| `registry_batch_verify.py --self-test` | **19/24 断言通过，exit 1** | W3a 未改任何 `scripts/`（V8）；在基线 `dda25c9^` 上同样失败 ⇒ **先于 W3a 的漂移** |
| 覆盖率报告 `W3a: 0` | `W3a` 桶为 0，而 `coverage_pct` 70.90 → **72.17** | W3a 名字**尚未**写入 `allowlist`（W3a 阶段不写 allowlist）⇒ 桶计数产物，**非**未处理证据 |
| `physical-sputtering` 与 `sputtering` 的 zh 别名重复 | 1 行 | `physical-sputtering` **不在 `w3.ids`**，W3a 未改该行；已在 `w3-name-conflicts.tsv` 登记为 pre-existing，**待人工裁决** |

---

## 4. 判定

| 维度 | 判定 |
|---|---|
| 数据完整性 / 边界（854 名、仅 col3、无冲突、无退化） | **PASS** |
| 命名质量（130 行独立抽检） | **PASS**（0 FAIL） |
| 计划判据②「依据可核验」 | **不可评估（判据空转）+ 实质缺失 747 行** ⇒ **未满足** |
| **综合** | **PARTIAL** — blocking **0**，warnings **4**（§3.1、§3.2、§3.3 两项） |

**未签收为 PASS 的理由**：`docs/ops`/`CONSTITUTION §2` 口径下「门禁绿 ≠ 签收」；本计划自身在 §「T1.B18 / T1.B19 返工」已确立同一判例（机械门禁只判坏模式，不判来源真实性与义项）。因此不得以 43 批 exit 0 宣布依据合格。

**不得据此回退命名**：130 行抽检 0 FAIL、命名冲突 0、列边界 100% 干净 ⇒ 已写入的 854 个名字构成**可用基线**，缺口是**证据/释义**层，不是命名层。

---

## 5. 处置（待用户裁决，未执行）

| 选项 | 内容 | 可逆性 | 成本 |
|---|---|---|---|
| **A（推荐）** | 接受 W3a 命名为机械基线；把「747 行占位释义 + 无引文 evidence」登记为 **known-issue**，另立后续证据/释义任务 | 高（增量追加） | 本轮 0 |
| B | 先补 747 行 zh 释义与可核验出处，再重做 W3a 验收至 PASS | 中 | 高（>10 h，需分批 + 抽检） |
| C | 仅补 evidence 的 `quote`/URL（不改释义），把判据②落到可机器判定 | 高 | 中 |
| D | 修 `registry_batch_verify.py` 让 `--check-urls` 在 names 模式生效（含 self-test 从 19/24 修复） | 高 | 中（涉及脚本变更，需单独授权） |

> **用户裁决（2026-10-29）**：通过 `question` 选择 **A（接受命名基线 + 另立证据任务）**。因此 854 个 `preferred_zh` 作为 W3a 可用基线保留；747 行占位释义、空 quote/裸来源与 names-mode `--check-urls` 空转登记为 **known-issue**，不阻塞命名基线。后续单独登记证据/释义补强任务；W4 终验本轮仍不直接启动。
>
> **边界说明**：后续 allowlist 落地与 W4 准备须按独立阶段的 acceptance criteria 执行；本验收记录不将其冒充为已完成。
